"""Base interface class to setup CRUD operations."""
        
def objectize(obj, dictionary):
    """Set attributes of an object from a dictionary."""
    o = obj()
    for key in dictionary:
        setattr(o, key, dictionary[key])
    return o
    
class RHNSatelliteInterface(object):
    def __init__(self):
        pass
    
    def query(self, regex=None, just_one=False, all_data=True, **filters):
        raise SatCLIRuntimeError, \
            "RHNSatelliteInterface.search must be subclassed"
    
    def create(self):
        raise SatCLIRuntimeError, \
            "RHNSatelliteInterface.create must be subclassed"
    
    def update(self):
        raise SatCLIRuntimeError, \
            "RHNSatelliteInterface.update must be subclassed"
            
    def delete(self):
        raise SatCLIRuntimeError, \
            "RHNSatelliteInterface.delete must be subclassed"