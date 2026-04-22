from uc3m_consulting.storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE

class DocumentJsonStore(JsonStore):
    """Specialized store for test documents."""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(DocumentJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self._file_name = TEST_DOCUMENTS_STORE_FILE