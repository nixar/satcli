"""Bootstrap the package namespace."""

from cement.core.namespace import CementNamespace, register_namespace

package = CementNamespace(
    label='package', 
    controller='PackageController',
    )

package.options.add_option('-p', '--pkg', action='store', dest='full_package', 
    default=None, help='package name-version-release-arch', metavar="PKG")
package.options.add_option('--pkg-name', action='store', dest='name', 
    default=None, help='package name')
package.options.add_option('--pkg-summary', action='store', dest='summary', 
    default=None, help='package summary')
package.options.add_option('--pkg-desc', action='store', dest='description', 
    default=None, help='package description')
package.options.add_option('--pkg-version', action='store', dest='version', 
    default=None, help='package version')
package.options.add_option('--pkg-release', action='store', dest='release', 
    default=None, help='package release')
package.options.add_option('--pkg-arch', action='store', dest='arch', 
    default=None, help='package arch')
package.options.add_option('--pkg-epoch', action='store', dest='epoch', 
    default=None, help='package epoch')
package.options.add_option('--pkg-provider', action='store', dest='provider', 
    default=None, help='package provider')

# Officialize and register the namespace
register_namespace(package)