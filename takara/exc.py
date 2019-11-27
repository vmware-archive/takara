class TakaraBaseException(Exception):
    '''
    Base exception where all of Takara's exceptions derive
    '''


class TakaraError(TakaraBaseException):
    '''
    General purpose Takara exception to signal an error
    '''


class UnitExistsError(TakaraBaseException):
    '''
    Raised when trying to create a unit that is already present
    '''


class UnitMissingError(TakaraBaseException):
    '''
    Raised when trying to access a unit that is not present
    '''


class PathMissingError(TakaraBaseException):
    '''
    Raised when trying to access an unavailiable path
    '''


class UnsealError(TakaraBaseException):
    '''
    Raised when the system fails to unseal a unit
    '''
