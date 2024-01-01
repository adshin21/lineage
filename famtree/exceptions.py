
class NotAValidInteger(Exception):
    """
    Raises when encounter type conversion to int
    on an invalid int data tyep
    """
    msg = "Value is not a valid integer"
