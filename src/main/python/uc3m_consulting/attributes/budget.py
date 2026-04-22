"""
Module for the Budget attribute class.
"""
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Budget(Attribute):
    """Class that represents and validates a Budget."""

    def _validate(self, value: str):
        """Validates the project budget amount and format ("budget validation")."""
        try:
            float_budget = float(value)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        float_budget_string = str(float_budget)
        if '.' in float_budget_string:
            decimals = len(float_budget_string.split('.')[1])
            if decimals > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if float_budget < 50000 or float_budget > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")
