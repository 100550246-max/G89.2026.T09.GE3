"""
Module for the FileName attribute class.
"""
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class FileName(Attribute):
    """Validates the file name."""
    def _validate(self, value: str):
        """Validates that the file name is a non-empty string ("file name validation")."""
        if not isinstance(value, str) or not value.strip():
            raise EnterpriseManagementException("Invalid file name")
