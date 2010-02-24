"""
This is the ExampleController for the satcli application.  This can be used
to expose commands to the example namespace which will be accessible under:

    $ satcli example --help
  
"""

from cement.core.namespace import get_config
from cement.core.log import get_logger
from cement.core.controller import CementController, expose
from cement.core.hook import run_hooks

from satcli.model.example import ExampleModel

log = get_logger(__name__)

class ExampleController(CementController):
    @expose(namespace='example') # no template
    def ex1(self, cli_opts, cli_args):
        """
        This is how to expose a subcommand because it will be under the 
        'example' namespace.  You would access this subcommand as:
    
            $ satcli example ex1
        
        """

        # You can get the root application config like this:
        config = get_config('root')
        
        # Or you can get your example namespace config like this:
        config = get_config('example')
        
        # You can print or log output however you like since this function
        # does not render out to a template.
        
        # Commands are all passed the cli_opts, cli_args from the command line.
        # So if you have added cli options in your satcli.bootstrap.example
        # file, you could access them here as:
        #
        #   cli_opts.<your_option>
        #   cli_args[0] # first argument *after* your command
        #
        
        # Here we show how to run a hook that we've defined in
        # satcli.bootstrap.example:
        for res in run_hooks('my_example_hook'):
            print res
        
        # This command has no template, but if we return something we
        # can still access the json output via --json.
        return dict(foo='bar')
        
    @expose(namespace='example')
    def ex1_help(self, cli_opts, cli_args):
        """
        Help methods are found by way of <command>_help.  This would be
        executed when you run:
        
            $ satcli example ex1-help
        
        """
        print "This is the help method for ex1."
    
    @expose('satcli.templates.example.ex2', namespace='example')    
    def ex2(self, cli_opts, cli_args): 
        """
        This is another command, also in the 'example' namespace but that is
        rendered by a genshi template.  
        
        Notice that you can specify the namespace via the decorator parameters.
        If a plugin has any non-root commands they are grouped under a 
        single command to the base cli application.  For example, you will 
        see root commands and namespaces* when you execute:
        
            $ satcli --help
            
            
        If 'example' has local commands, you will see 'example*' show up in 
        the root commands list, and then the subcommands will be seen under:
        
            $ satcli myplugin --help
            
        
        This is done to give different options in how your application works.
        
        """
        
        # Here we are using our Example model, and then returning a dictionary
        # to our @expose() decorator where it will be rendered with Genshi.
        example = ExampleModel()
        example.label = 'This is my Example Model'

        # You can see if options where passed.  These are set in 
        # satcli/bootstrap/example.py:
        if cli_opts.foo:
            # --foo was passed, do something
            log.info('%s passed by --foo option' % cli_opts.foo)

        return dict(foo=cli_opts.foo, example=example, items=['one', 'two', 'three'])

    @expose(namespace='root')
    def cmd2(self, cli_opts, cli_args):
        """This command will be displayed under the root namespace."""
        foo = "In satcli.controllers.example.cmd2()"
        print foo
        return dict(foo=foo)
