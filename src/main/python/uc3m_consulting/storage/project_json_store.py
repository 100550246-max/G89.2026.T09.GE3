from uc3m_consulting.storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE

class ProjectJsonStore(JsonStore):
    """Specialized store for projects."""
    def __init__(self):
        super().__init__()
        self._file_name = PROJECTS_STORE_FILE