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

# Officialize and register the namespace
register_namespace(errata)