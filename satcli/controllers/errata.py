"""
This controller handles interactions with the following API handlers:

    ErrataHandler
    
"""

import sys, os
from pyrpm.rpm import RPM
from pyrpm import rpmdefs
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
    def publish(self, *args, **kw):
        errors = []
        channels = []
        if not self.cli_opts.advisory:
            if len(sys.argv) >= 4:
                self.cli_opts.advisory = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'errata -a/--advisory required.'))

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
        errata = g.proxy.call('errata.publish', self.cli_opts.advisory, channels)
        return dict()    
    
    @expose(namespace='errata')
    def create(self, *args, **kw):
        config = get_config()
        
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
        
        if not self.cli_opts.synopsis:
            errors.append(('SatCLIArgumentError', 
                           'errata --synopsis required.'))
        
        if not self.cli_opts.product:
            errors.append(('SatCLIArgumentError', 
                           'errata --product required.'))
        
        if not self.cli_opts.advisory_type:
            errors.append(('SatCLIArgumentError', 
                           'errata --type required.'))
        
        if not self.cli_opts.advisory_type in ['bug', 'enhancement', 'security']:
            errors.append(('SatCLIArgumentError',
                       'errata --type must be one of bug, enhancement, security.'))                   

        if not self.cli_opts.description:
            errors.append(('SatCLIArgumentError', 
                           'errata --description required.'))
                           
        abort_on_error(errors)
                
        if not self.cli_opts.topic:
            self.cli_opts.topic = "%s update." % self.cli_opts.advisory_type.capitalize()
        
        if not self.cli_opts.solution:
            self.cli_opts.solution = config['errata']['solution']
        
        if self.cli_opts.keywords:
            self.cli_opts.keywords = self.cli_opts.keywords.split(',')
        else:
            self.cli_opts.keywords = []


        rpms = glob(str(self.cli_opts.rpms))
        rpms_data = []
        package_ids = []
        for r in rpms:
            nosig_txt = ''
            if config['allow_nosig']:
                nosig_txt = '--nosig'
            cmd = "%s %s -u %s -p %s --server %s %s" % \
                (config['cmd_rhnpush'], r, config['user'], 
                 config['password'], 
                 config['server'], nosig_txt)
            gso(cmd)
            rpm = RPM(file(r))  
            package = g.proxy.query(model.Package, just_one=True,
                                name=rpm[rpmdefs.RPMTAG_NAME], 
                                version=rpm[rpmdefs.RPMTAG_VERSION], 
                                release=rpm[rpmdefs.RPMTAG_RELEASE], 
                                arch=rpm[rpmdefs.RPMTAG_ARCH])
            rpms_data.append(package)
        if self.cli_opts.srpm:
            if os.path.exists(self.cli_opts.srpm):
                rpm = RPM(file(r))  
                nosig_txt = ''
                if config['allow_nosig']:
                    nosig_txt = '--nosig'
                    cmd = "%s %s --source -u %s -p %s --server %s %s" % \
                        (config['cmd_rhnpush'], self.cli_opts.srpm, 
                         config['user'], config['password'], 
                         config['server'], nosig_txt)
                    gso(cmd)
                else:
                    log.warn("SRPM '%s' doesn't exist!" % self.cli_opts.srpm)    

        for p in rpms_data:
            package_ids.append(p.id)
        
        if self.cli_opts.advisory_type == 'bug':
            self.cli_opts.advisory_type = 'Bug Fix Advisory'
        elif self.cli_opts.advisory_type == 'enhancement':
            self.cli_opts.advisory_type = 'Product Enhancement Advisory'
        elif self.cli_opts.advisory_type == 'security':
            self.cli_opts.advisory_type = 'Security Advisory'        
            
            
        e = model.Errata()
        e.synopsis = self.cli_opts.synopsis
        e.advisory_name = self.cli_opts.advisory
        e.advisory_release = 1
        e.advisory_type = self.cli_opts.advisory_type
        e.product = self.cli_opts.product
        e.topic = self.cli_opts.topic
        e.description = self.cli_opts.description
        e.references = self.cli_opts.references or ''
        e.notes = self.cli_opts.notes or ''
        e.solution = self.cli_opts.solution
        e.bug_ids = []
        e.keywords = self.cli_opts.keywords or []
        e.package_ids = package_ids
        e.publish = self.cli_opts.publish
        e.channels = channels       
        g.proxy.create(e)
        res = g.proxy.query(model.Errata, just_one=True, all_data=True,
                            advisory=self.cli_opts.advisory)     
        return dict(errata=res)
    
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
    
    @expose(namespace='errata')
    def delete(self, *args, **kw):            
        errors = []
        if not self.cli_opts.advisory:
            if len(sys.argv) >= 4:
                self.cli_opts.advisory = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'errata -a/--advisory required.'))
        abort_on_error(errors)
        res = raw_input("Permanantly delete advisory '%s'? [y/N] " % \
                        self.cli_opts.advisory)
        if not res.lower() in ['y', 'yes']:
            sys.exit(1)

        errata = g.proxy.query(model.Errata, just_one=True, all_data=True,
                               advisory=self.cli_opts.advisory)
        g.proxy.delete(errata)
        return dict()
        
    # HELP COMMANDS
    
    @expose('satcli.templates.errata.show-help', namespace='errata')
    def show_help(self, *args, **kw):
        return dict()