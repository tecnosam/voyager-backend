
class InvalidTokenException(Exception):
    def __str__(self) -> str:
        return super().__str__()
    pass

class UserNotFoundException( Exception ):
    def __str__( self ) -> str:
        return super().__str__()

class UserExistsException( Exception ):
    def __str__( self ) -> str:
        return "user %s already exists" % super().__str__()

class PostNotFoundException( Exception ):
    def __str__(self) -> str:
        return "post %s does not exist" % super().__str__()