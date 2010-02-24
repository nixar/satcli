
from cement.core.hook import define_hook
from cement.core.namespace import CementNamespace, register_namespace

define_hook('my_example_hook')

# Setup the 'example' namespace object
example = CementNamespace(
    label='example', 
    controller='ExampleController',
    description='Example Plugin for Satellite CLI',
    )

# Example namespace default configurations, overwritten by the [example] 
# section of the applications config file(s).  Once registered, this dict is
# accessible as:
#
#   namespaces['example'].config
#
example.config['foo'] = 'bar'

# Example namespace options.  These options show up under:
#
#   $ satcli example --help
#
example.options.add_option('-F', '--foo', action='store',
    dest='foo', default=None, help='Example Foo Option'
    )

# Officialize and register the namespace
register_namespace(example)

