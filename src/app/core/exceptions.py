class AppException(Exception):
    """Base para excepciones de la aplicación"""

    pass


class HeroNotFoundError(AppException):
    pass


class PersistenceError(AppException):
    """Error de infraestructura / persistencia"""

    pass


class TokenCreationError(AppException):
    pass


class TokenDecodeError(AppException):
    pass
