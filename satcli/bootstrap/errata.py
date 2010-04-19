"""Bootstrap the errata namespace."""

from cement.core.namespace import CementNamespace, register_namespace

errata = CementNamespace(
    label='errata', 
    controller='ErrataController',
    )

errata.options.add_option('-a', '--errata-advisory', action='store', dest='advisory', 
    default=None, help='errata advisory name', metavar="ERRATA")
errata.options.add_option('--since', action='store', dest='start_date', 
    default=None, help='errata start date (YYYY-MM-DD) (default: 1 month ago)', metavar="DATE")
errata.options.add_option('-c', '--channel', action='store', dest='channel', 
    default=None, help='channel labels (comma separated)', metavar="LABEL")
errata.options.add_option('--rpms', action='store', dest='rpms', 
    default=None, help="rpm(s) path (i.e '/path/to/*.rpm') [quoted]", metavar="PATH")    
errata.options.add_option('--srpm', action='store', dest='srpm', 
    default=None, help='source rpm path (i.e /path/to/foo-1.2-3.srpm)', metavar="PATH")    

errata.options.add_option('--channels-file', action='store', 
    dest='channels_file', default=None, 
    help='channels list file (one per line)', metavar="PATH")

# Officialize and register the namespace
register_namespace(errata)