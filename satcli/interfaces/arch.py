
from satcli import app_globals as g
from satcli.core.exc import SatCLIArgumentError
from satcli.core.interface import RHNSatelliteInterface
from satcli.model import root as model

class ArchInterface(RHNSatelliteInterface):
    def query(self, regex=None, just_one=False, all_data=False, **filters):
        archs = g.proxy.call('channel.software.listArches')
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
                arch_objects.append(self._objectize(model.Arch, arch))
        
        if just_one:
            if len(arch_objects) > 1:
                raise SatCLIArgumentError, "More than one arch found!"
            elif len(arch_objects) == 0:
                raise SatCLIArgumentError, "No archs found matching that query!"
            else: 
                return arch_objects[0]
        else:        
            return arch_objects