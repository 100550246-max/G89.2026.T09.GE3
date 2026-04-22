"""
Module for the json_store class
"""
import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class JsonStore:
    """Base class for managing data persistence in JSON format."""

    def __init__(self):
        self._file_name = ""

    def load_list(self, empty_if_missing: bool = False):
        """Loads a list of data from a JSON file."""
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError as ex:
            if empty_if_missing:
                return []
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def save_list(self, data_list: list):
        """Saves a list of data into a JSON file."""
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
