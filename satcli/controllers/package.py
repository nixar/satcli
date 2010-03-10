"""
This controller handles interactions with the following API handlers:

    packages
    packages.provider
    packages.search
    
"""

import sys
import re

from cement.core.exc import CementArgumentError
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks
from rosendale.helpers.error import abort_on_error

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.model import root as model
from satcli.core.controller import SatCLIController

log = get_logger(__name__)

class PackageController(SatCLIController):  
    def _get_package(self, full_package):
        """
        Get a package object based on a full package name.
        
        Required Arguments:
        
            full_package
                RPM package name in the format name-version-release-arch.
        """
        # FIX ME: This regex is weak sauce, needs improvement
        m = re.match('(^[a-zA-Z].*)-([\d].*)-(.*)-(.*)', full_package)
        if m:
            name = m.group(1)
            version = m.group(2)
            release = m.group(3)
            arch = m.group(4)   
        else:
            errors.append(('SatCLIArgumentError',
                "invalid --pkg, need form 'name-version-release-arch'"))
            abort_on_error(errors)
        package = g.proxy.query(model.Package, just_one=True, all_data=True,
                                name=name, version=version, release=release, 
                                arch=arch)
        return package
                                     
    @expose('satcli.templates.package.show', namespace='package')
    def show(self, *args, **kw):
        errors = []
        if not self.cli_opts.full_package:
            if len(sys.argv) >= 4:
                self.cli_opts.full_package = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'package -p/--pkg required.'))
        abort_on_error(errors)
        package = self._get_package(self.cli_opts.full_package)
        return dict(package=package)

    @expose(namespace='package')
    def search(self, *args, **kw):
        errors = []
        
        if self.cli_opts.full_package:
            # FIX ME: This regex is weak sauce, needs improvement
            m = re.match('(^[a-zA-Z].*)-([\d].*)-(.*)-(.*)', 
                         self.cli_opts.full_package)
            if m:
                name = m.group(1)
                version = m.group(2)
                release = m.group(3)
                arch = m.group(4)   
            else:
                errors.append(('SatCLIArgumentError',
                    "invalid --pkg, need form 'name-version-release-arch'"))
                abort_on_error(errors)
            packages = g.proxy.query(model.Package, name=name, 
                                     version=version, release=release, arch=arch)
        elif self.cli_opts.query:
            packages = g.proxy.query(model.Package, regex=self.cli_opts.query)
        else:
            # explicit search
            packages = g.proxy.query(model.Package,
                                     name=self.cli_opts.name, 
                                     version=self.cli_opts.version, 
                                     release=self.cli_opts.release, 
                                     arch=self.cli_opts.arch,
                                     epoch=self.cli_opts.epoch,
                                     description=self.cli_opts.description,
                                     summary=self.cli_opts.summary)
        for p in packages:
            print "%s-%s-%s-%s" % (p.name, p.version, p.release, p.arch)
        return dict(packages=packages)
    
    @expose('satcli.templates.package.search-help', namespace='package')
    def search_help(self, *args, **kw):
        return dict()
    
    @expose('satcli.templates.package.show-help', namespace='package')
    def show_help(self, *args, **kw):
        return dict()
    