from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

class ProjectId(Attribute):
    """Validates that the ID of a Project is valid."""
    def _validate(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise EnterpriseManagementException("Invalid project ID")