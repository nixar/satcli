"""SatCLI exception classes."""

class SatCLIError(Exception):
    """Generic errors."""
    def __init__(self, value, code=1):
        Exception.__init__(self)
        self.msg = value
        self.code = code
    
    def __str__(self):
        return self.msg
        
class SatCLIConfigError(SatCLIError):
    """Config parsing and setup errors."""
    def __init__(self, value):
        code = 10
        SatCLIError.__init__(self, value, code)

class SatCLIRuntimeError(SatCLIError):
    """Runtime errors."""
    def __init__(self, value):
        code = 20
        SatCLIError.__init__(self, value, code)
        
class SatCLIInternalServerError(SatCLIError):
    """Unknown or private internal errors."""
    def __init__(self, value):
        code = 30
        SatCLIError.__init__(self, value, code)
        
class SatCLIArgumentError(SatCLIError):
    """Argument errors."""
    def __init__(self, value):
        code = 40
        SatCLIError.__init__(self, value, code)
