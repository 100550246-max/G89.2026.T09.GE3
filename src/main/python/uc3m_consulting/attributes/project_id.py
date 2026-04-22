"""
Module for the ProjectId attribute class.
"""
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class ProjectId(Attribute):
    """Validates that the ID of a Project is valid."""

    def _validate(self, value: str):
        """Validates that the project ID is a non-empty string ("project ID validation")."""
        if not isinstance(value, str) or not value.strip():
            raise EnterpriseManagementException("Invalid project ID")
