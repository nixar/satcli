"""Channel model."""

import re

from cement.core.log import get_logger
from cement.core.namespace import get_config

from satcli.interface import RHNSatelliteInterface

log = get_logger(__name__)
config = get_config()

class ChannelInterface(RHNSatelliteInterface):        
    def query(self, just_one=False, regex=None, **kw):
        filters = kw
        channels = self.proxy.call('channel.listAllChannels')
        channel_objects = []
        for channel in channels:
            append = False
            
            if regex:
                for key in channel:
                    m = re.search(regex, str(channel[key]))
                    if m:
                        append = True
                        break 
            elif len(filters) > 0:
                for key in filters:
                    if channel.has_key(key) and channel[key] == filters[key]:
                        append = True
                        break
            else:
                append = True
            
            if append:
                channel_objects.append(self._objectize(Channel, channel))
        
        if just_one:
            if len(channel_objects) > 1:
                raise SatCLIArgumentError, "More than one channel found!"
            else: 
                return channel_objects[0]
        else:        
            return channel_objects
    
class Channel(object):
    interface = ChannelInterface
    
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
    
    @property
    def latest_packages(self):
        # lookup latest packages with self.label
        pass
    
