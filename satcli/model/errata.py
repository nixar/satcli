"""errata model."""

from cement.core.log import get_logger
from cement.core.namespace import get_config

from satcli import app_globals as g
from satcli.core.interface import RHNSatelliteInterface
from satcli.core.exc import SatCLIArgumentError
from satcli.model.channel import Channel

log = get_logger(__name__)
config = get_config()

class Errata(object):
    def __init__(self):
        self.advisory = None
        self.issue_date = None
        self.update_date = None
        self.last_modified_date = None
        self.synopsis = None
        self.release = None
        self.type = None
        self.product = None
        self.topic = None
        self.description = None
        self.references = None
        self.notes = None
        self.solution = None

    def _set_affected_channels(self, channels):
        self.affected_channels = channels
    def _get_affected_channels(self):
        affected_channels = g.proxy.call('errata.applicableToChannels', 
                                              self.advisory)
        return affected_channels
    affected_channels = property(_get_affected_channels, _set_affected_channels)
    