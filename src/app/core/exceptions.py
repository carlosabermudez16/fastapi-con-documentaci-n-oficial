from fastapi import status


class AppException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Application error"

    def __init__(self, detail=None):
        if detail:
            self.detail = detail


class HeroNotFoundError(AppException):
    pass


class TokenCreationError(AppException):
    pass


class TokenDecodeError(AppException):
    pass


class PersistenceError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Database / persistence error"


class CreateModelError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error creating model"


class UpdateModelError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error updating model"


class DeleteModelError(AppException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Error deleting model"


class ModelSerializationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Error converting schema to ORM model"


class RegisterNotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Record not found"


class DuplicateRegisterError(AppException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Email already registered"


class AccountNotVerified(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Account Not Verified: Please check your email for verification details"
