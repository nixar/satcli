"""
This controller handles interactions with the following API handlers:

    ErrataHandler
    
"""

import sys, os
from glob import glob
from commands import getstatusoutput as gso

from cement.core.exc import CementArgumentError
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks
from cement.core.namespace import get_config
from rosendale.helpers.error import abort_on_error

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.model import root as model
from satcli.core.controller import SatCLIController

log = get_logger(__name__)
config = get_config()

class ErrataController(SatCLIController):  
    @expose('satcli.templates.errata.show', namespace='errata')
    def show(self, *args, **kw):
        errors = []
        if not self.cli_opts.advisory:
            if len(sys.argv) >= 4:
                self.cli_opts.advisory = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'errata -a/--advisory required.'))
        abort_on_error(errors)
        errata = g.proxy.query(model.Errata, just_one=True, 
                               advisory=self.cli_opts.advisory)
        return dict(errata=errata)
    
    @expose(namespace='errata')
    def create(self, *args, **kw):
        errors = []
        channels = []
        if not self.cli_opts.advisory:
            errors.append(('SatCLIArgumentError', 
                           'errata -a/--advisory required.'))
        if not self.cli_opts.rpms:
            errors.append(('SatCLIArgumentError', 
                           'errata --rpms required.'))                   
        if not self.cli_opts.channel and not self.cli_opts.channels_file:
            errors.append(('SatCLIArgumentError', 
                           'errata -c/--channel or --channels-file required.'))                   
        if self.cli_opts.channel:
            _channels = self.cli_opts.channel.split(',')
            for _c in _channels:
                channels.append(_c)
        if self.cli_opts.channels_file:
            if os.path.exists(self.cli_opts.channels_file):
                f = open(self.cli_opts.channels_file, 'r')
                for line in f.readlines():
                    channels.append(line.strip('\n'))
            else:
                log.warn("channels file '%s' doesn't exist!" % \
                         self.cli_opts.channels_file)
            
        
        abort_on_error(errors)

        rpms = glob(str(self.cli_opts.rpms))
        for r in rpms:
            nosig_txt = ''
            if config['allow_nosig']:
                nosig_txt = '--nosig'
            cmd = "%s %s -u %s -p %s --server %s %s" % \
                (config['cmd_rhnpush'], r, config['user'], config['password'], 
                 config['server'], nosig_txt)
            gso(cmd)
        if self.cli_opts.srpm:
            if os.path.exists(self.cli_opts.srpm):
                nosig_txt = ''
                if config['allow_nosig']:
                    nosig_txt = '--nosig'
                    cmd = "%s %s --source -u %s -p %s --server %s %s" % \
                        (config['cmd_rhnpush'], self.cli_opts.srpm, config['user'], 
                         config['password'], config['server'], nosig_txt)
                    gso(cmd)
                else:
                    log.warn("SRPM '%s' doesn't exist!" % self.cli_opts.srpm)    
        return dict()
    
    @expose('satcli.templates.errata.list', namespace='errata')
    def list(self, *args, **kw):
        errors = []
        all_errata = [] # list of tuples, 0 is the errata data, 1 is the errata dict

        if self.cli_opts.channel:
            channels = []
            labels = self.cli_opts.channel.split(',')
            for label in labels:
                channels.append(g.proxy.query(model.Channel, label=label, 
                                just_one=True))
        else:
            channels = g.proxy.query(model.Channel)
                           
        abort_on_error(errors)
        for c in channels:
            if self.cli_opts.all:
                errata = c.errata
            else:
                errata = c.recent_errata
            for e in errata:
                all_errata.append((e.issue_date, e))

        all_errata.sort()
        all_errata.reverse()
        
        return dict(errata=all_errata)
    
    # HELP COMMANDS
    
    @expose('satcli.templates.errata.show-help', namespace='errata')
    def show_help(self, *args, **kw):
        return dict()