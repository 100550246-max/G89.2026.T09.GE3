"""
Module for the QueryDate attribute class.
"""
import re
from datetime import datetime
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class QueryDate(Attribute):
    """Class representing and validating a date for queries."""

    def _validate(self, value: str):
        """Validates the date format for history queries ("date format validation")."""
        date_format = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        if not date_format.fullmatch(value):
            raise EnterpriseManagementException("Invalid date format")

        try:
            datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex
