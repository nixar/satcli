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
    
    
    
    # HELP COMMANDS
    
    @expose('satcli.templates.errata.show-help', namespace='errata')
    def show_help(self, *args, **kw):
        return dict()