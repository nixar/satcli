"""
This is the RootController for the satcli application.  This can be used
to expose commands to the root namespace which will be accessible under:

    $ satcli --help
  
"""

from cement import namespaces
from cement.core.exc import CementArgumentError
from cement.core.controller import CementController, expose
from cement.core.namespace import get_config
from cement.core.log import get_logger

from satcli import user_cache
from satcli.lib.proxy import RHNSatelliteProxy

log = get_logger(__name__)
config = get_config()

class RootController(CementController):
    @expose('satcli.templates.root.error', is_hidden=True)
    def error(self, *args, **kw):
        """
        This can be called when catching exceptions.  It expects an 
        'errors' dictionary to be passed via **kwargs.
        
        """
        if kw.get('errors', None):
            return dict(errors=kw['errors'])
    
    @expose(is_hidden=True)
    def default(self, cli_opts, cli_args):
        """
        This is the default command method.  If no commands are passed to
        satcli, this one will be executed.  By default it raises an
        exception.
        
        """
        raise CementArgumentError, "A command is required. See --help?"
    
    @expose()
    def freeform(self, cli_opts, cli_args):
        """
        Takes an API path (i.e. auth.login) and args (i.e username) and
        attempts to make a call to the RHN Proxy.  Useful for development.
        """
        cmd = cli_args.pop(0)
        path = cli_args.pop(0)
        args = cli_args
 
        proxy = RHNSatelliteProxy()
        
        if cli_opts.user:
            proxy.get_session(use_cache=False)
        else:
            proxy.get_session()    
            
        try:
            res = proxy.call(path, *args)
        except xmlrpclib.Fault, e:
            res = proxy.noauth_call(path, *args)
        
        print
        print "Freeform API Call Output"
        print "-" * 77
        print res
        print
    
    @expose()
    def freeform_help(self, cli_opts, cli_args):
        print
        print "Attempt to make an API call to the RHN Proxy:"
        print
        print "$ satcli freeform 'user.getLoggedInTime' 'johndoe'"
        print
 
