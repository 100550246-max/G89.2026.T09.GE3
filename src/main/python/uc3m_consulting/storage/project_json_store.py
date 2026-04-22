"""
Module for the project_json_store class
"""
from uc3m_consulting.storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE

class ProjectJsonStore(JsonStore):
    """Specialized store for projects."""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ProjectJsonStore, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        super().__init__()
        self._file_name = PROJECTS_STORE_FILE
