"""
This is the application's core code.  Unless you know the "ins-and-outs" of
The Cement CLI Application Framework, you probably should not modify the 
main() function of this file.

"""

import sys
import xmlrpclib
from pkg_resources import get_distribution

from cement.core.exc import CementArgumentError, CementConfigError, \
                            CementRuntimeError
from cement.core.log import get_logger
from cement.core.app_setup import lay_cement
from cement.core.configuration import ensure_api_compat
from cement.core.command import run_command

from satcli.config import default_config
from satcli.exc import SatCLIArgumentError, SatCLIConfigError, \
                       SatCLIRuntimeError
                       
REQUIRED_CEMENT_API = '0.7-0.8:20100210'
KNOWN_COMPAT = ['10.8']

VERSION = get_distribution('satcli').version
BANNER = """
satcli v%s - Command Line Interface for the RHN Satellite Server
Copyright (C) 2010 BJ Dierkes <wdierkes@rackspace.com>
Distributed under the GNU General Public License v2
 
This version is known to be compatible with the following Satellite Server 
API Versions:
 
%s
""" % (VERSION, KNOWN_COMPAT)

def main():
    try:
        ensure_api_compat(__name__, REQUIRED_CEMENT_API)    
        lay_cement(config=default_config, banner=BANNER)
    
        log = get_logger(__name__)
        log.debug("Cement Framework Initialized!")

        if not len(sys.argv) > 1:
            sys.argv.append('default')
        
        run_command(sys.argv[1])
            
    except CementArgumentError, e:
        print("CementArgumentError > %s" % e)
        sys.exit(e.code)
    except CementConfigError, e:
        print("CementConfigError > %s" % e)
        sys.exit(e.code)
    except CementRuntimeError, e:
        print("CementRuntimeError > %s" % e)
        sys.exit(e.code)
    except SatCLIArgumentError, e:
        print("SatCLIArgumentError > %s" % e)
        sys.exit(e.code)
    except SatCLIConfigError, e:
        print("SatCLIConfigError > %s" % e)
        sys.exit(e.code)
    except SatCLIRuntimeError, e:
        print("SatCLIRuntimeError > %s" % e)
        sys.exit(e.code)
    except xmlrpclib.Fault, e:
        print("xmlrpclib.Fault > %s" % e)
    sys.exit(0)
        
if __name__ == '__main__':
    main()
    
