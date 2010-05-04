"""
This controller handles mirroring functions, which mirror RHN channels
to local Yum repos.
"""

import os
import re
from urllib2 import urlopen
from hashlib import md5

from cement.core.namespace import get_config
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError, SatCLIRuntimeError
from satcli.model import root as model
from satcli.core.controller import SatCLIController

log = get_logger(__name__)

class LocalRepo(object):
    def __init__(self, label):
        self.config = get_config('mirror')
        self.label = label
        self.synced_files = []
        self.attempted_files = []
        self.modified = False
        self.local_dir = re.sub('\%\(mirror_dir\)', self.config['mirror_dir'], 
                                self.config[self.label]['path'])
        self.channel = g.proxy.query(model.Channel, just_one=True, 
                                     all_data=True, label=label)
        # get the package list
        if self.config[self.label]['only_latest']:
            call_path = 'channel.software.listLatestPackages'
        else:
            call_path = 'channel.software.listAllPackages'    
        self.packages = g.proxy.call(call_path, self.label)

        # base mirror config
        run_createrepo = self.config.get('run_createrepo', None)
        run_yumarch = self.config.get('run_yumarch', None)
        only_latest = self.config.get('only_latest', None)
        
        # per channel config
        self.run_createrepo = self.config[self.label]\
                                .get('run_createrepo', run_createrepo)
        self.run_yumarch = self.config[self.label]\
                                .get('run_yumarch', run_yumarch)
        self.only_latest = self.config[self.label]\
                                .get('only_latest', only_latest)
    
        # create out local dir if missing
        if not os.path.exists(self.local_dir):
            os.makedirs(self.local_dir)

    def _fast_sync(self, package, force=False):
        file = "%s-%s-%s.%s.rpm" % (package['name'], 
                                    package['version'],
                                    package['release'],
                                    package['arch_label'])
        full_path = os.path.join(self.local_dir, file)

        self.attempted_files.append(file)
        if not os.path.exists(full_path) or force == True:
            self.fetch_package(package, full_path)
            self.modified = True
            
        self.synced_files.append(file) 
        
    def sync(self, verify=False, force=False):
        for p in self.packages:
            if verify:
                # self._slow_sync(p)
                raise SatCLIRuntimeError, "_slow_sync() not implemented."                
            else:
                self._fast_sync(p, force)
        
        # finally, create the repo
        if self.modified and self.run_createrepo:
            log.info("running createrepo: %s" % self.label)
            os.system("%s %s" % (self.config['createrepo_path'], self.local_dir))
        if self.modified and self.run_yumarch:
            log.info("running yum-arch: %s" % self.label)
            os.system("%s %s" % (self.config['yumarch_path'], self.local_dir))
            
        # clean up files that aren't in packages
        for file in os.listdir(self.local_dir):
            if file not in self.synced_files and file.endswith('.rpm'):
                log.debug("cleanup: %s" % file)
                os.remove(os.path.join(self.local_dir, file))
                
    def fetch_package(self, package, local_path):
        # FIX ME:
        # need to do an md5 sum here, but the cost sucks because you have to
        # make a call for each package to get its md5 sum
        log.info("fetching %s/%s-%s-%s.%s.rpm ...." % (self.channel.label, 
                                                       package['name'],
                                                       package['version'],
                                                       package['release'],
                                                       package['arch_label']))
        url = g.proxy.call('packages.getPackageUrl', package['id'])
        f = open(local_path, 'w')
        data = urlopen(url).read()
        f.write(data)
        f.close()
            
    
class MirrorController(SatCLIController):  
    def mirror(self, channel):
        config = get_config('mirror')
        repo = LocalRepo(channel)
        
        #print repo.packages
        
        try:
            repo.sync(verify=self.cli_opts.verify, force=self.cli_opts.force)
        except KeyboardInterrupt, e:
            log.warn('Caught KeyboardInterrupt => Attempting to exit clean...')
            # remove the last file attempted
            if len(repo.attempted_files) > 0:
                last_path = os.path.join(
                    repo.local_dir, repo.attempted_files[-1])
                if os.path.exists(last_path):
                    log.debug('cleanup: removing last attempted file %s' \
                              % last_path)
                    os.remove(last_path)
            raise SatCLIRuntimeError, "Caught KeyboardInterrupt"
            
        log.info("mirroring of '%s' complete." % repo.label)
        
    @expose(namespace='mirror')
    def sync(self, *args, **kw): 
        config = get_config('mirror')

        if not self.cli_opts.channel:
            raise SatCLIArgumentError, "Must pass a channel label (or 'all')"
    
        if self.cli_opts.channel == 'all':
            for c in config.sections:
                self.mirror(c)
        else:
            if self.cli_opts.channel in config.sections:
                self.mirror(self.cli_opts.channel)
            else:
                raise SatCLIArgumentError, \
                    "channel '%s' doesn't exist in the config." % \
                    self.cli_opts.channel
                sys.exit(1)
        