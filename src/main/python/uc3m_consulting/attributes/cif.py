"""
Module for the CIF attribute class.
"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

# pylint: disable=too-few-public-methods
class Cif(Attribute):
    """Class that represents and validates a Cif."""

    # pylint: disable=too-many-branches
    def _validate(self, value: str):
        """Validates the CIF format and control character ("check digit")."""
        if not isinstance(value, str):
            raise EnterpriseManagementException("CIF code must be a string")
        pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not pattern.fullmatch(value):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letter = value[0]
        cif_block_number = value[1:8]
        cif_unit = value[8]

        even_sum = 0
        odd_sum = 0

        for pos, digit_char in enumerate(cif_block_number):
            digit = int(digit_char)
            if pos % 2 == 0:
                double_val = digit * 2
                even_sum += (double_val // 10) + (double_val % 10)
            else:
                odd_sum += digit

        total_sum = even_sum + odd_sum
        base_digit = (10 - (total_sum % 10)) % 10
        control_chars = "JABCDEFGHI"

        if cif_letter in ('A', 'B', 'E', 'H'):
            if str(base_digit) != cif_unit:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_letter in ('P', 'Q', 'S', 'K'):
            if control_chars[base_digit] != cif_unit:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
