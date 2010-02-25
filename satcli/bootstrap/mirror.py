
from cement.core.namespace import CementNamespace, register_namespace, \
                                  get_config

mirror = CementNamespace(
    label='mirror', 
    controller='MirrorController',
    description='Mirror Plugin for Satellite CLI',
    )

mirror.config['verify'] = False

# Example namespace options.  These options show up under:
#
#   $ satcli example --help
#
example.options.add_option('-V', '--verify', action='store_true',
    dest='verify', default=None, help='Verify MD5 of files (costly)'
    )

# Officialize and register the namespace
register_namespace(example)

@register_hook()
def validate_config_hook(*args, **kwargs):
    config = get_config()
    required_settings = ['mirror_dir', 'lockfile_dir']
    for s in required_settings:
        if not config['mirror'].has_key(s):
            raise CementConfigError, "config['mirror']['%s'] value missing!" % s
    
    if not os.path.exists(config['mirror']['mirror_dir']):
        os.makedirs(config['mirror']['mirror_dir'])

