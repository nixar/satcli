import sys, os
from pkg_resources import get_distribution
import xmlrpclib
 
from cement.core.namespace import get_config
from cement.core.log import get_logger
from rosendale.helpers.cache.simple_cache import SimpleCache
 
from satcli import user_cache
from satcli.appmain import KNOWN_COMPAT
 
log = get_logger(__name__)
        
class RHNSatelliteProxy(object):
    def __init__(self):
        self.token = None
        self.session = None
        self.user = None
        self.config = get_config()
        log.debug('initializing RHNSatelliteProxy()')
    
    def get_user_pass(self):
        password = ''
        
        if self.config.has_key('user'):
            self.user = self.config['user']
        else:
            self.user = raw_input('%s username: ' % \
                        self.config['server_type'].capitalize())
                
        if self.config.has_key('password') and self.config['password']:
            password = self.config['password']
        else:
            try:
                os.system('stty -echo')
                password = raw_input('%s Password for %s: ' % \
                    (self.config['server_type'].capitalize(), self.user))
                os.system('stty echo')
                print
            except:
                os.system('stty echo')
                print     
        return (self.user, password)
                  
    def get_session(self, use_cache=True, user=None, password=None):
        """
        Get a session with the server.
        
        Optional keyword arguments:
        
            use_cache
                Whether to used a cache token or not
            
            force_auth
                Force the user to provide auth credentials
                
            user
                RHN username
                
            pass 
                RHN Password
        
        """
        log.debug('attempting to get rhn session')
        global user_cache
        if self.config['use_ssl']:
            uri = "https://%s:%s/rpc/api" % (self.config['server'], 
                                             self.config['port'])
        else:
            uri = "http://%s:%s/rpc/api" % (self.config['server'], 
                                            self.config['port'])
            
        self.session = xmlrpclib.ServerProxy(uri, allow_none=True)
        self.user = user
            
        if self.user:
            if password:
                pass
            else:
                try:
                    os.system('stty -echo')
                    password = raw_input('%s Password for %s: ' % \
                        (self.config['server_type'].capitalize(), self.user))
                    os.system('stty echo')
                    print
                except:
                    os.system('stty echo')
                    print            
                
        elif use_cache and user_cache.get('rhn_session_key'):
            # token is cached, lets validate it
            self.token = user_cache.get('rhn_session_key')
            try:
                res = self.call('user.listUsers')
            except xmlrpclib.Fault, e:
                self.token = None
                user_cache.drop('rhn_session_key')
  
        else:
            (self.user, password) = self.get_user_pass()
        
        # If the token wasn't cached        
        if not self.token:
            # get the session token
            try:
                (self.user, password) = self.get_user_pass()
                self.token = self.session.auth.login(self.user, password)
            except xmlrpclib.Fault, e:
                print "xmlrpclib.Fault => %s" % e
                sys.exit(1)
           
        # Verify we have a session                
        if self.token:
            user_cache.store('rhn_session_key', self.token)
            self.verify_compatibility()
        else:
            log.error("Unable to obtain session!")
            sys.exit(1)
    
    def verify_compatibility(self):
        log.debug('verifying rhn api compatibility')
        res = self.session.api.getVersion()
        if res not in KNOWN_COMPAT:
            log.warn(
                "Proxy API v%s has unknown compatibility with dstation v%s" \
                    % (res, get_distribution('dstation').version)
                )
        
    def call(self, path, *args, **kwargs):
        log.debug('making call to rhn: self.session.%s(self.token, %s)' % (path, [str(x) for x in args]))
        res = eval("self.session.%s(self.token, *args)" % path)
        return res
 
    def noauth_call(self, path, *args, **kwargs):
        log.debug('making call to rhn: self.session.%s(%s)' % (path, [str(x) for x in args]))
        res = eval("self.session.%s(*args)" % path)
        return res
        