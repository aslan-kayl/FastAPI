


class BooklyException(Exception):
    """This is the base class for all bookly errors"""
    pass

class InvalidToken(BooklyException):
    """User has provided invalid token"""
    pass

class RevokedToken(BooklyException):
    """User has provided a token that has been revoked"""
    pass

class AccessTokenRequired(BooklyException):
    """User has provided a refresh token when an access token is needed"""
    pass

class RefreshTokenRequired(BooklyException):
    """User has provided an access token when a refresh token is needed"""
    pass

class UserAlreadyExists(BooklyException):
    """User has provided an email for a user who exists during sing up."""
    pass

class InvalidCredentials(BooklyException):
    """User has provided wrong email or password during log in."""
    pass

class InsuffcientPermission(BooklyException):
    """User does not have the neccessary permission to perform an action."""
    pass

class TagNotFound(BooklyException):
    """Book Not Found"""
    pass

class InvalidToken(BooklyException):
    """User has provided invalid token"""
    pass

class UserNotFound(BooklyException):
    """User Not Found"""
    pass