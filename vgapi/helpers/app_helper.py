""" General helpers that can be used application-wide. """

X_WARNINGS_KEY = 'X-API-WARNINGS'
X_WARNINGS_DESC = 'API Warnings (non-fatal)'

class GeneralValidationError(Exception):
    pass

def check_unsupported_fields(passed, valid):
    """ Warn API users about unsupported fields they've passed us.
    Args:
        passed -- iterable of passed fields
        valid -- iterable of valid fields
    Returns:
        Warning message string
    
    """
    ret = None
    fields_diff = set(passed) - valid

    if fields_diff:
        ret = "Unupported fields: {}".format(fields_diff)

    return ret

def set_fields(item, req_data,  updateable):
    """ Utility for setting specified model attributes from passed-in data

    Args:
        item -- object to be updated
        req_data -- JSON data passed in via an API call
        updatable -- allowed fields

    """

    passed_fields = req_data.keys()

    for attr in updateable:
            if attr not in passed_fields:
                continue

            setattr(item, attr, req_data.get(attr))
