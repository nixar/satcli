"""
This file handles interaction between the Errata model, and RHN API Calls.

"""

import re

from cement.core.log import get_logger

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.core.interface import RHNSatelliteInterface, objectize
from satcli.model import root as model

log = get_logger(__name__)

class ErrataInterface(RHNSatelliteInterface):                                    
    def query(self, regex=None, just_one=False, all_data=False, **filters):
        errata_objects = []
        all_errata = []
        
        # this would be the shortest possible query
        if filters.get('advisory', None):
            errata = g.proxy.call('errata.getDetails', filters['advisory'])
            errata['advisory'] = filters['advisory']
            all_errata.append(errata)
            
        elif filters.get('channel', None):
            errata = g.proxy.call('channel.software.listErrata', 
                                  filters['channel'])
            for e in errata:
                all_errata.append(e)
            
        else:
            # LONG QUERY    
            channels = g.proxy.call('channel.listAllChannels')
        
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
                    errata_objects.append(objectize(model.Channel, channel))
        
        # FIX ME: do something if all_data=True ?
        for e in all_errata:
            errata_objects.append(objectize(model.Errata, e))
                
        if just_one:
            if len(errata_objects) > 1:
                raise SatCLIArgumentError, "More than one channel found!"
            elif len(errata_objects) == 0:
                raise SatCLIArgumentError, "No channels found matching that query!"
            else: 
                return errata_objects[0]
        else:        
            return errata_objects