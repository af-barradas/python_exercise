import logging


def validate_inputs(data, columns):
    if not isinstance(data, list):
        raise TypeError("Data must be a list")
    if not data:
        raise ValueError("Data cannot be empty")
    if not isinstance(columns, list):
        raise TypeError("Columns must be a list")
    if not columns:
        logging.warning("No columns specified")
        return False
    return True
