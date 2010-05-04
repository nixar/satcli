"""Bootstrap the channel namespace."""

from cement.core.namespace import CementNamespace, register_namespace

channel = CementNamespace(
    label='channel', 
    controller='ChannelController',
    )

channel.options.add_option('-t', '--chan-type', action='store', dest='type', 
    default=None, help='channel type [all, mine, popular...]')
channel.options.add_option('--count', action='store', dest='popularity_count', 
    default=None, help='popularity count (number of servers)')
channel.options.add_option('-c', '--channel', action='store',
    dest='label', default=None, help='channel label')
channel.options.add_option('--chan-id', action='store', dest='id',
    default=None, help='channel id')
channel.options.add_option('--chan-name', action='store', dest='name',
    default=None, help='channel name')
channel.options.add_option('--chan-arch', action='store', dest='arch_name',
    default=None, help='channel arch label')
channel.options.add_option('--chan-summary', action='store', dest='summary',
    default=None, help='channel summary')
channel.options.add_option('--chan-desc', action='store', dest='description',
    default=None, help='channel summary', metavar="DESC")
channel.options.add_option('--chan-maint-name', action='store', 
    dest='maintainer_name', default=None, help="channel maintainer's name",
    metavar="NAME")
channel.options.add_option('--chan-maint-email', action='store', 
    dest='maintainer_email', default=None, help="channel maintainer's email",
    metavar="EMAIL")
channel.options.add_option('--chan-maint-phone', action='store', 
    dest='maintainer_phone', default=None, help="channel maintainer's phone",
    metavar="PHONE")
channel.options.add_option('--chan-gpg-url', action='store', dest='gpg_key_url',
    default=None, help="channel gpg key url")
channel.options.add_option('--chan-gpg-id', action='store', dest='gpg_key_id',
    default=None, help="channel gpg key id")
channel.options.add_option('--chan-gpg-fp', action='store', dest='gpg_key_fp',
    default=None, help="channel gpg key finger print")
channel.options.add_option('--chan-eol', action='store', dest='end_of_life',
    default=None, help="channel end of life")
channel.options.add_option('--chan-parent', action='store', 
    dest='parent_channel_label', default=None, help="channel parent label",
    metavar='LABEL')
channel.options.add_option('--rpms', action='store', dest='rpms', 
    default=None, help="rpm(s) path (i.e '/path/to/*.rpm') [quoted]", metavar="PATH")    
channel.options.add_option('--srpms', action='store', dest='srpms', 
    default=None, help='source rpms path (i.e /path/to/*.srpm)', metavar="PATH")    
# Officialize and register the namespace
register_namespace(channel)
