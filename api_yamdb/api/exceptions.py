from rest_framework.exceptions import ValidationError


class AlreadyExistException(ValidationError):
    default_code = 'existing_field'


class AlreadyExistUserException(ValidationError):
    default_detail = 'Такой пользователь уже существует'
    code = 'existing_user'
