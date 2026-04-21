from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

class FileName(Attribute):
    """Validates the file name."""
    def _validate(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise EnterpriseManagementException("Invalid file name")