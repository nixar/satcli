"""
The bootstrap module should be used to setup parts of your application
that need to exist before all controllers are loaded.  It is best used to 
define hooks, setup namespaces, and the like.  The root namespace is 
already bootstrapped by Cement, however you can extend that functionality
by importing additional bootstrap files here.
"""

from cement.core.exc import CementConfigError
from cement.core.opt import init_parser
from cement.core.hook import register_hook

# Register root options
@register_hook()
def options_hook(*args, **kwargs):
    # This hook allows us to append options to the root namespace
    root_options = init_parser()
    root_options.add_option('--json', action='store_true',
        dest='enable_json', default=None, 
        help='render output as json (Cement CLI-API)')
    root_options.add_option('--debug', action='store_true',
        dest='debug', default=None, help='toggle debug output')
    root_options.add_option('--quiet', action='store_true',
        dest='quiet', default=None, help='disable console logging')
    root_options.add_option('--all', action='store_true',
        dest='all', default=None, help='disable full output when applicable')
    root_options.add_option('-r', '--regex', action='store', dest='regex',
        default=None, help="query string [regular expression]")    
    root_options.add_option('-q', '--query', action='store', dest='query',
        default=None, help="query string [plain]")
    return ('root', root_options)

@register_hook()
def validate_config_hook(*args, **kwargs):
    config = kwargs.get('config', None)
    if not config:
        print("WARNING: broken hook.  missing 'config' keyword argument.")
    else:
        required_settings = ['user', 'password', 'server', 'port', 'use_ssl']
        for s in required_settings:
            if not config.has_key(s):
                raise CementConfigError, "config['%s'] value missing!" % s
            
@register_hook()
def options_hook(*args, **kwargs):
    """
    Pass back an OptParse object, options will be merged into the global
    options.
    """
    global_options = init_parser()
    global_options.add_option('--user', action ='store', 
        dest='user', default=None, help='RHN user name'
        ) 
    global_options.add_option('--pass', action='store', 
        dest='password', default=None, help='RHN user password'
        ) 
    global_options.add_option('--server', action ='store', 
        dest='server', default=None, help='RHN server hostname'
        ) 
    global_options.add_option('--port', action ='store', 
        dest='port', default=None, help='RHN server port'
        )    
    return ('root', global_options)
    
# Import all additional (non-plugin) bootstrap libraries here    

from satcli.bootstrap import channel, package
