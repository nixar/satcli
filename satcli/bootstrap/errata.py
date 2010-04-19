"""Bootstrap the errata namespace."""

from cement.core.namespace import CementNamespace, register_namespace

errata = CementNamespace(
    label='errata', 
    controller='ErrataController',
    )

errata.options.add_option('-a', '--advisory-name', action='store', dest='advisory', 
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
errata.options.add_option('--synopsis', action='store', dest='synopsis', 
    default=None, help="errata synopsis (summary)", metavar="TEXT")    
errata.options.add_option('--topic', action='store', dest='topic', 
    default=None, help="errata topic", metavar="TEXT")    
errata.options.add_option('--product', action='store', dest='product', 
    default=None, help="errata product", metavar="TEXT")    
errata.options.add_option('--description', action='store', dest='description', 
    default=None, help="errata description", metavar="TEXT")    
errata.options.add_option('--references', action='store', dest='references', 
    default=None, help="errata references", metavar="TEXT")    
errata.options.add_option('--notes', action='store', dest='notes', 
    default=None, help="errata notes", metavar="TEXT")    
errata.options.add_option('--solution', action='store', dest='solution', 
    default=None, help="errata solution", metavar="TEXT")    
errata.options.add_option('--keywords', action='store', dest='keywords', 
    default=None, help="errata keywords (comma separated)", metavar="STR")    
errata.options.add_option('--type', action='store', dest='advisory_type', 
    default=None, help="errata type [bug, enhancement, security]", metavar="STR")    
errata.options.add_option('--publish', action='store_true', dest='publish', 
    default=None, help="whether to publish errata")    

# Officialize and register the namespace
register_namespace(errata)