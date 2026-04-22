"""
Module for the Department attribute class.
"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Department(Attribute):
    """Class that represents and validates a Department."""

    def _validate(self, value: str):
        """Validates the department name ("department name")."""
        department_pattern = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        if not department_pattern.fullmatch(value):
            raise EnterpriseManagementException("Invalid department")
