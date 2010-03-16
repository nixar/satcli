"""Bootstrap the errata namespace."""

from cement.core.namespace import CementNamespace, register_namespace

errata = CementNamespace(
    label='errata', 
    controller='ErrataController',
    )

errata.options.add_option('-a', '--advisory', action='store', dest='advisory', 
    default=None, help='errata advisory name', metavar="ERRATA")

# Officialize and register the namespace
register_namespace(errata)