
from cement.core.namespace import CementNamespace, register_namespace

channel = CementNamespace(
    label='channel', 
    controller='ChannelController',
    description='Channel Plugin for Satellite CLI',
    )

channel.options.add_option('-t', '--type', action='store',
    dest='type', default=None, help='channel type [all, mine, popular...]'
    )
channel.options.add_option('--count', action='store',
    dest='popularity_count', default=None, help='popularity count (number of servers)'
    )
channel.options.add_option('-l', '--label', action='store',
    dest='label', default=None, help='channel label'
    )

# Officialize and register the namespace
register_namespace(channel)
