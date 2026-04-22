"""
Module for the StartingDate attribute class.
"""
import re
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class StartingDate(Attribute):
    """Class that represents and validates the starting date."""

    def _validate(self, value: str):
        """Validates the project starting date format and constraints ("date validation")."""
        date_format = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        if not date_format.fullmatch(value):
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
