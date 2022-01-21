class DatabaseException(Exception):
    orig = None


class WrongPassword(DatabaseException):
    orig = "wrong_password"


class UserNotFound(DatabaseException):
    orig = "user_not_found"
