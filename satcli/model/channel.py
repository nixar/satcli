"""Channel model."""

import re

from cement.core.log import get_logger
from cement.core.namespace import get_config

from satcli.core.interface import RHNSatelliteInterface
from satcli.core.exc import SatCLIArgumentError

log = get_logger(__name__)
config = get_config()

class ArchInterface(RHNSatelliteInterface):
    def query(self, regex=None, just_one=False, all_data=False, **filters):
        archs = self.proxy.call('channel.software.listArches')
        arch_objects = []
        for arch in archs:
            append = False
            
            if regex:
                for key in arch:
                    m = re.search(regex, str(arch[key]))
                    if m:
                        append = True
                        break 
            elif len(filters) > 0:
                for key in filters:
                    if arch.has_key(key) and arch[key] == filters[key]:
                        append = True
                        break
            else:
                append = True
            
            if append:
                arch_objects.append(self._objectize(Arch, arch))
        
        if just_one:
            if len(arch_objects) > 1:
                raise SatCLIArgumentError, "More than one arch found!"
            elif len(arch_objects) == 0:
                raise SatCLIArgumentError, "No archs found matching that query!"
            else: 
                return arch_objects[0]
        else:        
            return arch_objects

class Arch(object):
    interface = ArchInterface
    
    def __init__(self):
        self.label = None
        self.name = None
    
    def __repr__(self):
        return '<Arch: name=%s>' % self.name
        
    def __unicode__(self):
        return unicode(self.name)

class ChannelInterface(RHNSatelliteInterface):        
    def query(self, regex=None, just_one=False, all_data=False, **filters):
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
                if all_data:
                    details = self.proxy.call('channel.software.getDetails', 
                                              channel['label'])
                    channel.update(details)
                channel_objects.append(self._objectize(Channel, channel))
        
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
        archs = self.proxy.query(Arch)
        # wtf?
        if c.arch in archs:
            print 'JOHNNY'
        try:
            assert c.label, "channel label missing."
            assert c.name, "channel name missing."
            assert c.summary, "channel summary missing."
            assert c.arch in archs, "invalid architecture.  see 'satcli channel list-archs'."
        except AssertionError, e:
            raise SatCLIArgumentError, str(e)
        
            
        res = self.proxy.call("channel.software.create", c.label, c.name, 
                              c.summary, c.arch_name, c.parent_channel_label)
        if res == 1:
            log.info("successfully created software channel '%s'.")
            return True
        else:
            log.info("failed to create software channel '%s'.")
            return False
    
class Channel(object):
    interface = ChannelInterface
    
    def __init__(self):
        self.id = None
        self.label = None
        self.name = None
        self.arch_label = None
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

        # special objects
        self.arch = property(self._get_arch, self._set_arch) 
        
    def _set_arch(self, arch_obj):
        if arch_obj.__class__ != Arch:
            raise SatCLIRuntimeError, "must pass an Arch() class object."
        self.arch_label = arch_obj.label
    
    def _get_arch(self):
        if self.label:
            return self.proxy.query(Arch, just_one=True, label=self.label)
       

        
    @property
    def latest_packages(self):
        # lookup latest packages with self.label
        pass
    
