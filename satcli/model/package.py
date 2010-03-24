
"""Package model."""

from cement.core.log import get_logger
from cement.core.namespace import get_config

from satcli import app_globals as g
from satcli.core.interface import RHNSatelliteInterface
from satcli.core.exc import SatCLIArgumentError

log = get_logger(__name__)
config = get_config()

class Package(object):
    def __init__(self):
        self.id = None
        self.name = None
        self.summary = None
        self.description = None
        self.version = None
        self.release = None
        self.arch = None
        self.epoch = None
        self.provider = None
        self.build_host = None
        self.md5sum = None
        self.vendor = None
        self.cookie = None
        self.license = None
        self.file = None
        self.build_date = None
        self.last_modified_date = None
        self.size = None
        self.path = None
        self.payload_size = None

    def _set_url(self, url):
        raise SatCLIRuntimeError, "package url can not be set!"
    def _get_url(self):
        url = g.proxy.call("packages.getPackageUrl", self.id)
        return url
    url = property(_get_url, _set_url)