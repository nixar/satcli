
from cement.core.controller import CementController

from satcli.proxy import RHNSatelliteProxy

class SatCLIController(CementController):
    def __init__(self, cli_opts=None, cli_args=None):
        CementController.__init__(self, cli_opts, cli_args)
        self.cli_opts = cli_opts
        self.cli_args = cli_args
        
        self.proxy = RHNSatelliteProxy()
        
        if self.cli_opts.user:
            self.proxy.get_session(use_cache=False)
        else:
            self.proxy.get_session()  
