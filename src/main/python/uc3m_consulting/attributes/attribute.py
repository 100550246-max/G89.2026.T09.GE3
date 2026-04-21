
class Attribute:
    """Base class for the attributes of the system"""
    def __init__(self, value):
        self._validate(value)
        self._value = value

    def _validate(self, value):
        """The son classes overwrite this method to validate the value"""
        pass
    @property
    def value(self):
        return self._value