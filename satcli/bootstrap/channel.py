
from cement.core.namespace import CementNamespace, register_namespace

channel = CementNamespace(
    label='channel', 
    controller='ChannelController',
    description='Channel Plugin for Satellite CLI',
    )

channel.options.add_option('-t', '--type', action='store', dest='type', 
    default=None, help='channel type [all, mine, popular...]')
channel.options.add_option('--count', action='store', dest='popularity_count', 
    default=None, help='popularity count (number of servers)')
channel.options.add_option('-l', '--label', action='store',
    dest='label', default=None, help='channel label')
channel.options.add_option('--id', action='store', dest='id',
    default=None, help='channel id')
channel.options.add_option('--name', action='store', dest='name',
    default=None, help='channel name')
channel.options.add_option('--arch', action='store', dest='arch_name',
    default=None, help='channel arch label')
channel.options.add_option('--summary', action='store', dest='summary',
    default=None, help='channel summary')
channel.options.add_option('--description', action='store', dest='description',
    default=None, help='channel summary', metavar="DESC")
channel.options.add_option('--maintainer-name', action='store', 
    dest='maintainer_name', default=None, help="channel maintainer's name",
    metavar="NAME")
channel.options.add_option('--maintainer-email', action='store', 
    dest='maintainer_email', default=None, help="channel maintainer's email",
    metavar="EMAIL")
channel.options.add_option('--maintainer-phone', action='store', 
    dest='maintainer_phone', default=None, help="channel maintainer's phone",
    metavar="PHONE")
channel.options.add_option('--gpg-url', action='store', dest='gpg_key_url',
    default=None, help="channel gpg key url")
channel.options.add_option('--gpg-id', action='store', dest='gpg_key_id',
    default=None, help="channel gpg key id")
channel.options.add_option('--gpg-fp', action='store', dest='gpg_key_fp',
    default=None, help="channel gpg key finger print")
channel.options.add_option('--eol', action='store', dest='end_of_life',
    default=None, help="channel end of life")
channel.options.add_option('--parent-label', action='store', 
    dest='parent_channel_label', default=None, help="channel parent label")
channel.options.add_option('--regex', action='store', dest='regex',
    default=None, help="channel query string [regular expression]")    
# Officialize and register the namespace
register_namespace(channel)
