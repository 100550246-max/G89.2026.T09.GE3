"""
Module containing the base class for attributes.
"""

# pylint: disable=too-few-public-methods
class Attribute:
    """Base class for the attributes of the system"""
    def __init__(self, value):
        self._validate(value)
        self._value = value

    def _validate(self, value):
        """The child classes overwrite this method to validate the value"""

    @property
    def value(self):
        """Returns the internal value of the attribute ("getter method")."""
        return self._value
