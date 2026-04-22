"""
Module for the Description attribute class.
"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Description(Attribute):
    """Class that represents and validates a Description."""
    def _validate(self, value: str):
        """Validates the project description format ("description format")."""
        description_pattern = re.compile(r"^.{10,30}$")
        if not description_pattern.fullmatch(value):
            raise EnterpriseManagementException("Invalid description format")
