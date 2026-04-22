"""
Module for the Acronym attribute class.
"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Acronym(Attribute):
    """Class that represents and validates a Acronym."""

    def _validate(self, value: str):
        """Validates the project acronym format ("acronym format")."""

        acronym_pattern = re.compile(r"^[a-zA-Z0-9]{5,10}$")
        if not acronym_pattern.fullmatch(value):
            raise EnterpriseManagementException("Invalid acronym")
