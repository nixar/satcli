
from cement.core.namespace import get_config
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from satcli.model.example import ExampleModel

log = get_logger(__name__)
config = get_config()

class MirrorController(CementController):    
    def __init__(self):
        CementController.__init__(self)
        self.proxy = RHNSatelliteProxy()
        