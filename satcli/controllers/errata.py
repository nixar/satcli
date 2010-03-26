"""
This controller handles interactions with the following API handlers:

    ErrataHandler
    
"""

import sys

from cement.core.exc import CementArgumentError
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks
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
    
    @expose('satcli.templates.errata.show', namespace='errata')
    def create(self, *args, **kw):
        errors = []
        errata = []
        if not self.cli_opts.advisory:
            errors.append(('SatCLIArgumentError', 
                           'errata -a/--advisory required.'))
        abort_on_error(errors)
        channels = g.proxy.query(model.Channel)
        for c in channels:
            errata.append(c.errata)
        
        print errata
        return dict(errata=errata)
    
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