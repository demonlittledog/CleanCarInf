from voluptuous import Schema, Invalid, Required
def CheckGender(value):
    if isinstance(value, str) and (value == 'F' or value == 'M'):
        # actually here, we can transform the value, and return an updated value as the result of the validation
        return value


