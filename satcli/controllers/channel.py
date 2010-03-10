"""
This controller handles interactions with the following API handlers:

    ChannelHandler
    ChannelAccessHandler
    ChannelOrgHandler
    ChannelSoftwareHandler
    
"""

import sys

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

class ChannelController(SatCLIController):  
    @expose('satcli.templates.channel.show', namespace='channel')
    def show(self, *args, **kw):
        errors = []
        if not self.cli_opts.label:
            if len(sys.argv) >= 4:
                self.cli_opts.label = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'channel -l/--label required.'))
        abort_on_error(errors)
        channel = g.proxy.query(model.Channel, just_one=True, 
                                   label=self.cli_opts.label)
        return dict(channel=channel)
        
    @expose(namespace='channel')
    def create(self, *args, **kw):
        try:
            assert self.cli_opts.label, "channel -l/--label rquired."
            assert self.cli_opts.name, "channel --name required."
            assert self.cli_opts.summary, "channel --summary required."
            assert self.cli_opts.arch_name, "channel --arch required."
        except AssertionError, e:
            raise SatCLIArgumentError, str(e)
            
        c = model.Channel()
        c.label = self.cli_opts.label
        c.name = self.cli_opts.name
        c.summary = self.cli_opts.summary
        c.arch_name = self.cli_opts.arch_name
        c.parent_channel_label = self.cli_opts.parent_channel_label or ''
        g.proxy.create(c)
    
    @expose(namespace='channel')
    def delete(self, *args, **kw):            
        errors = []
        if not self.cli_opts.label:
            if len(sys.argv) >= 4:
                self.cli_opts.label = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError', 
                               'channel -l/--label required.'))
        abort_on_error(errors)
        res = raw_input("Permanantly delete channel '%s'? [y/N] " % \
                        self.cli_opts.label)
        if not res.lower() in ['y', 'yes']:
            sys.exit(1)

        channel = g.proxy.query(model.Channel, just_one=True, 
                                label=self.cli_opts.label)
        g.proxy.delete(channel)
        return dict()
        
    @expose(namespace='channel')
    def search(self, *args, **kw):
        errors = []
        if not self.cli_opts.regex:
            if len(sys.argv) >= 4:
                self.cli_opts.regex = sys.argv[3]
            else:
                errors.append(('SatCLIArgumentError',
                               "A search string (-r/--regex) is required for query."))
        abort_on_error(errors)
                
        channels = g.proxy.query(model.Channel, self.cli_opts.regex, all_data=False)
        for channel in channels:
            print channel.label        
        return dict(channels=channels)
        
    @expose(namespace='channel')
    def list(self, *args, **kw):
        known = ['all', 'my', 'popular', 'redhat', 'retired', 
                 'shared', 'software']
                 
        if not self.cli_opts.type:
            #channels = self.proxy.call('channel.listAllChannels')
            channels = g.proxy.query(model.Channel, all_data=False)
            
        elif self.cli_opts.type.lower() == 'popular':
            if not self.cli_opts.popularity_count:
                raise SatCLIArgumentError, "Server popularity count required."
                
            channels = g.proxy.call('channel.listPopularChannels', 
                                       int(self.cli_opts.popularity_count))
        else:
            type = self.cli_opts.type.lower()
            if not type in known:
                raise SatCLIArgumentError, "Invalid channel type."
            if type == 'redhat':
                type = 'RedHat'
            else:
                type = type.capitalize()
                
            channels = g.proxy.call('channel.list%sChannels' % type)
            
        for channel in channels:
            print channel.label
            
        return dict(channels=channels)
        
    @expose(namespace='channel')
    def list_packages(self, *args, **kw):
        if not self.cli_opts.label:
            if len(sys.argv) >= 4:
                self.cli_opts.label = sys.argv[3]
            else:
                raise SatCLIArgumentError, 'channel -l/--label required'
        if self.cli_opts.all:
            call_path = 'channel.software.listAllPackages'
        else:
            call_path = 'channel.software.listLatestPackages'
            
        # FIX ME: Need to update with package model once ready
        packages = g.proxy.call(call_path, self.cli_opts.label)
        for p in packages:
            print "%s-%s-%s.%s" % (p['name'], p['version'], p['release'], 
                                   p['arch_label'])
        return dict(packages=packages)
    
    @expose(namespace='channel')
    def list_systems(self, *args, **kw):
        if not self.cli_opts.label:
            if len(sys.argv) >= 4:
                self.cli_opts.label = sys.argv[3]
            else:
                raise SatCLIArgumentError, 'channel -l/--label required'
        
        call_path = 'channel.software.listSubscribedSystems'
        
        # FIX ME: Need to update with system model once ready    
        systems = g.proxy.call(call_path, self.cli_opts.label)
        for s in systems:
            print s['id']
        return dict(systems=systems)
        
    @expose(namespace='channel')
    def list_archs(self, *args, **kw):
        archs = g.proxy.query(model.Arch)
        for arch in archs:
            print arch.name
        return dict(archs=archs)


    # Help Commands
    @expose('satcli.templates.channel.list-help', namespace='channel')
    def list_help(self, *args, **kw):
        return dict()
    
    @expose('satcli.templates.channel.list-packages-help', namespace='channel')
    def list_packages_help(self, *args, **kw):
        return dict()
    
    @expose('satcli.templates.channel.show-help', namespace='channel')
    def show_help(self, *args, **kw):
        return dict()
    
    @expose('satcli.templates.channel.search-help', namespace='channel')
    def query_help(self, *args, **kw):
        return dict()