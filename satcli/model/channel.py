"""Channel model."""

from datetime import datetime as dt
from datetime import timedelta

from cement.core.log import get_logger
from cement.core.namespace import get_config

from satcli import app_globals as g
from satcli.core.interface import RHNSatelliteInterface, objectize
from satcli.core.exc import SatCLIArgumentError
from satcli.model.arch import Arch
from satcli.model.errata import Errata

log = get_logger(__name__)
config = get_config()

class Channel(object):
    def __init__(self):
        self.id = None
        self.label = None
        self.name = None
        self.arch_name = None
        self.summary = None
        self.description = None
        self.maintainer_name = None
        self.maintainer_email = None
        self.maintainer_phone = None
        self.support_policy = None
        self.gpg_key_url = None
        self.gpg_key_id = None
        self.gpg_key_fp = None
        self.end_of_life = None
        self.parent_channel_label = None
        self.packages = None
        self.systems = None
        
    def _set_arch(self, arch_obj):
        self.arch_name = arch_obj.label
    def _get_arch(self):
        arch = g.proxy.query(Arch, just_one=True, name=self.arch_name)
        return arch    
    arch = property(_get_arch, _set_arch)
    
    def _set_errata(self):
        raise SatCLIRuntimeError, "can not set errata this way."
        
    def _get_recent_errata(self, *args, **kw):
        errata_objects = []
        since = dt.now() - timedelta(days=14)
        errata = g.proxy.call("channel.software.listErrata", self.label, since)
        for e in errata:
            details = g.proxy.call('errata.getDetails', e['advisory_name'])
            e.update(details)
            errata_objects.append(objectize(Errata, e))
        return errata_objects
        
    def _get_all_errata(self, *args, **kw):
        errata_objects = []
        errata = g.proxy.call("channel.software.listErrata", self.label)
        for e in errata:
            details = g.proxy.call('errata.getDetails', e['advisory_name'])
            e.update(details)
            errata_objects.append(objectize(Errata, e))
        return errata_objects
        
    errata = property(_get_all_errata, _set_errata)
    recent_errata = property(_get_recent_errata, _set_errata)