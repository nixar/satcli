"""
This file handles interaction between the Package model, and RHN API Calls.

"""

import re

from cement.core.log import get_logger

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.core.interface import RHNSatelliteInterface, objectize
from satcli.model import root as model

log = get_logger(__name__)

class PackageInterface(RHNSatelliteInterface):   
    def _get_exact_package(packages, filters):
        for p in packages:
            for f in filters:
                if filters[f] != packages[f]:
                    break
            return p
                                                 
    def query(self, regex=None, just_one=False, all_data=False, **filters):
        package_objects = []
        if just_one:
            try:
                assert filters.has_key('name'), "package name required."
                assert filters.has_key('version'), "package version required."
                assert filters.has_key('release'), "package release required."
                assert filters.has_key('arch'), "package arch required."    
            except AssertionError, e:
                raise SatCLIArgumentError, e.args[0]
            
            packages = g.proxy.call('packages.findByNvrea',
                                     filters['name'],
                                     filters['version'],
                                     filters['release'],
                                     filters.get('epoch', ''),
                                     filters['arch']
                                    )
        elif len(filters) > 0:
            lucene = ''
            for key in filters:
                if not filters[key]:
                    continue
                if lucene == '':
                    lucene += "%s:%s" % (key, filters[key])
                else:
                    lucene += " AND %s:%s" % (key, filters[key])
            log.debug("searching package via advanced lucene query '%s'." % lucene)
            packages = g.proxy.call('packages.search.advanced', lucene)   
        elif regex:
            log.debug("searching package via name query '%s'." % regex)
            packages = g.proxy.call('packages.search.name', regex)
        else:
            raise SatCLIArgumentError, 'regex OR filter required.'
              
        if just_one:
            if len(packages) > 1:
                exact_pkg = self._get_exact_package(packages, filters)
                if exact_pkg:
                    if all_data:
                        details = g.proxy.call('packages.getDetails', 
                                               exact_pkg['id'])
                        exact_pkg.update(details)
                    pkg_object = (objectize(model.Package, exact_pkg))
                    return pkg_object
                else:
                    raise SatCLIArgumentError, "More than one package found!"

            elif len(packages) == 0:
                raise SatCLIArgumentError, "No packages found matching that query!"
            else: 
                pkg = packages[0]
                
                # only 1 exists
                if all_data:    
                    details = g.proxy.call('packages.getDetails', pkg['id'])
                    pkg.update(details)
                pkg_object = (objectize(model.Package, pkg))
                return pkg_object
        else:        
            for package in packages:
                if all_data:
                    details = g.proxy.call('packages.getDetails', package['id'])
                    package.update(details)
                package_objects.append(objectize(model.Package, package))    
            return package_objects
            
    def create(self, package_obj):
        #if res == 1:
        #    log.info("successfully created package '%s'." % c.label)
        #    return True
        #else:
        #    log.info("failed to create package '%s'." % c.label)
        #    return False
        pass
        
    def delete(self, package_obj):
        #c = package_obj
        #res = g.proxy.call("package.software.delete", c.label)
        #if res == 1:
        #    log.info("successfully deleted package '%s'." % c.label)
        #    return True
        #else:
        #    log.info("failed to delete package '%s'." % c.label)
        #    return False
        pass