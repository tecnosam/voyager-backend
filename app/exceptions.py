
class InvalidTokenException(Exception):
    def __str__(self) -> str:
        return super().__str__()
    pass

class UserNotFoundException( Exception ):
    def __str__( self ) -> str:
        return super().__str__()
