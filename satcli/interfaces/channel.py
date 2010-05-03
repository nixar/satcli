"""
This file handles interaction between the Channel model, and RHN API Calls.

"""

import re

from cement.core.log import get_logger

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.core.interface import RHNSatelliteInterface, objectize
from satcli.model import root as model

log = get_logger(__name__)

class ChannelInterface(RHNSatelliteInterface):        
    def query(self, regex=None, just_one=False, all_data=False, **filters):
        channels = g.proxy.call('channel.listAllChannels')
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
                if all_data:
                    details = g.proxy.call('channel.software.getDetails', 
                                              channel['label'])
                    channel.update(details)
                channel_objects.append(objectize(model.Channel, channel))
        
        if just_one:
            if len(channel_objects) > 1:
                raise SatCLIArgumentError, "More than one channel found!"
            elif len(channel_objects) == 0:
                raise SatCLIArgumentError, "No channels found matching that query!"
            else: 
                return channel_objects[0]
        else:        
            return channel_objects
    
    def create(self, channel_obj):
        archs = []
        c = channel_obj
        
        try:
            assert c.label, "channel label missing."
            assert c.name, "channel name missing."
            assert c.summary, "channel summary missing."
            assert c.arch.label # this causes a lookup on the arch property
        except AssertionError, e:
            raise SatCLIArgumentError, str(e)
            
        res = g.proxy.call("channel.software.create", c.label, c.name, 
                              c.summary, c.arch.label, c.parent_channel_label)
        if res == 1:
            log.info("successfully created channel '%s'." % c.label)
            return True
        else:
            log.info("failed to create channel '%s'." % c.label)
            return False
    
    def delete(self, channel_obj):
        c = channel_obj
        res = g.proxy.call("channel.software.delete", c.label)
        if res == 1:
            log.info("successfully deleted channel '%s'." % c.label)
            return True
        else:
            log.info("failed to delete channel '%s'." % c.label)
            return False
