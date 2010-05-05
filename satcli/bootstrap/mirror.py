
import os

from cement.core.opt import init_parser
from cement.core.hook import register_hook
from cement.core.namespace import CementNamespace, register_namespace, \
                                  get_config
                                  

config = get_config()
mirror = CementNamespace(
    label='mirror', 
    controller='MirrorController'
    )

mirror.config['verify'] = False
mirror.config['mirror_dir'] = os.path.join(config['datadir'], 'mirror')
mirror.options.add_option('-V', '--verify', action='store_true',
    dest='verify', default=None, help='Verify MD5 of files (costly)')
mirror.options.add_option('--channel', action='store',
    dest='channel', default=None, help='channel to sync/mirror')    
register_namespace(mirror)
    
@register_hook()
def validate_config_hook(*args, **kwargs):
    config = get_config('mirror')
    required_settings = ['mirror_dir']
    for s in required_settings:
        if not config.has_key(s):
            raise CementConfigError, "config['mirror']['%s'] value missing!" % s
    
    if not os.path.exists(config['mirror_dir']):
        os.makedirs(config['mirror_dir'])

