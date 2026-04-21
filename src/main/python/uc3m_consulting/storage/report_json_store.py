from uc3m_consulting.storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE

class ReportJsonStore(JsonStore):
    """Specialized store for reports."""
    def __init__(self):
        super().__init__()
        self._file_name = TEST_NUMDOCS_STORE_FILE