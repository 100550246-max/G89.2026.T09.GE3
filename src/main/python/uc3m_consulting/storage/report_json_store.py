"""
Module for the report_json_store class
"""
from uc3m_consulting.storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE

class ReportJsonStore(JsonStore):
    """Specialized store for reports."""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ReportJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self._file_name = TEST_NUMDOCS_STORE_FILE
