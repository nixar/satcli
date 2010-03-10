
from cement.core.controller import CementController

from satcli import app_globals as g
from satcli.core.proxy import RHNSatelliteProxy

class SatCLIController(CementController):
    def __init__(self, cli_opts=None, cli_args=None):
        CementController.__init__(self, cli_opts, cli_args)
        self.cli_opts = cli_opts
        self.cli_args = cli_args
        
        g.proxy = RHNSatelliteProxy()
        
        if self.cli_opts.user:
            g.proxy.get_session(use_cache=False)
        else:
            g.proxy.get_session()  
