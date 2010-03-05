"""
This controller handles interactions with the following API handlers:

    ChannelHandler
    ChannelAccessHandler
    ChannelOrgHandler
    ChannelSoftwareHandler
    
"""

from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from satcli.exc import SatCLIArgumentError
from satcli.model import root as model
from satcli.controller import SatCLIController

log = get_logger(__name__)

class ChannelController(SatCLIController):        
    @expose()
    def test(self, *args, **kw):
        channels = self.proxy.query(model.Channel, regex='php-4', just_one=True)
        for c in channels:
            print c.label
        
    @expose(namespace='channel')
    def query(self, *args, **kw):
        if self.cli_opts.regex:
            channels = self.proxy.query(model.Channel, self.cli_opts.regex)
            for channel in channels:
                print channel.label
                
        elif self.cli_opts.filter:
            pass
        
    @expose(namespace='channel')
    def list(self, *args, **kw):
        known = ['all', 'my', 'popular', 'redhat', 'retired', 
                 'shared', 'software']
                 
        if not self.cli_opts.type:
            #channels = self.proxy.call('channel.listAllChannels')
            channels = self.proxy.search(Channel)
            
        elif self.cli_opts.type.lower() == 'popular':
            if not self.cli_opts.popularity_count:
                raise SatCLIArgumentError, "Server popularity count required."
                
            channels = self.proxy.call('channel.listPopularChannels', 
                                       int(self.cli_opts.popularity_count))
        else:
            type = self.cli_opts.type.lower()
            if not type in known:
                raise SatCLIArgumentError, "Invalid channel type."
            if type == 'redhat':
                type = 'RedHat'
            else:
                type = type.capitalize()
                
            channels = self.proxy.call('channel.list%sChannels' % type)
                
        for channel in channels:
            print channel['label']
        return dict(channels=channels)
    
    @expose('satcli.templates.channel.list-help', namespace='channel')
    def list_help(self, *args, **kw):
        return dict()
    
    @expose('satcli.templates.channel.show', namespace='channel')
    def show(self, *args, **kw):
        
        return dict(channel=channel)
    
    @expose('satcli.templates.channel.list-packages', namespace='channel')
    def list_packages(self, *args, **kw):
        if not self.cli_opts.label:
            raise SatCLIArgumentError, 'channel -l/--label required'
        if self.cli_opts.all:
            call_path = 'channel.software.listAllPackages'
        else:
            call_path = 'channel.software.listLatestPackages'
            
        packages = self.proxy.call(call_path, self.cli_opts.label)
        return dict(packages=packages)
    
    @expose('satcli.templates.channel.list-packages-help', namespace='channel')
    def list_packages_help(self, *args, **kw):
        return dict()
