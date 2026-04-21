
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attributes.attribute import Attribute

class Cif(Attribute):
    """Class that represents and validates a Cif."""

    def _validate(self, value: str):
        if not isinstance(value, str):
            raise EnterpriseManagementException("CIF code must be a string")
        pattern = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not pattern.fullmatch(value):
            raise EnterpriseManagementException("Invalid CIF format")

        cif_letter = value[0]
        cif_block_number = value[1:8]
        cif_unit = value[8]

        even_position_sum = 0
        odd_position_sum = 0

        for position in range(len(cif_block_number)):
            if position % 2 == 0:
                double_value = int(cif_block_number[position]) * 2
                if double_value > 9:
                    even_position_sum = even_position_sum + (double_value // 10) + (double_value % 10)
                else:
                    even_position_sum = even_position_sum + double_value
            else:
                odd_position_sum = odd_position_sum + int(cif_block_number[position])

        total_sum = even_position_sum + odd_position_sum
        unit_total_sum = total_sum % 10
        base_digit = 10 - unit_total_sum

        if base_digit == 10:
            base_digit = 0

        control_characters = "JABCDEFGHI"

        if cif_letter in ('A', 'B', 'E', 'H'):
            if str(base_digit) != cif_unit:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif cif_letter in ('P', 'Q', 'S', 'K'):
            if control_characters[base_digit] != cif_unit:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")