__import__('pkg_resources').declare_namespace(__name__)

import os

from rosendale.helpers.cache.simple_cache import SimpleCache

from satcli.core.globals import AppGlobals

user_cache = SimpleCache(
    os.path.join(os.environ['HOME'], '.satcli.cache'),
    mode=0640
    )
    
app_globals = AppGlobals()