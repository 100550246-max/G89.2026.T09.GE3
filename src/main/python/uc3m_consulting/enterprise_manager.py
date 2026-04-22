"""Module """
from datetime import datetime, timezone
from freezegun import freeze_time

from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.storage.project_json_store import ProjectJsonStore
from uc3m_consulting.storage.document_json_store import DocumentJsonStore
from uc3m_consulting.storage.report_json_store import ReportJsonStore
from uc3m_consulting.attributes.query_date import QueryDate


class EnterpriseManager:
    """Class for providing the methods for managing the orders"""

    # 1. Variable estática y privada para guardar la única instancia
    __instance = None

    # 2. Control de creación de la instancia
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(EnterpriseManager, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        pass

    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):

        """registers a new project"""

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        store = ProjectJsonStore()
        transfer_list = store.load_list(empty_if_missing=True)

        for transfer_item in transfer_list:
            if transfer_item == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        transfer_list.append(new_project.to_json())
        store.save_list(transfer_list)

        return new_project.project_id

    def _is_document_valid(self, document: dict) -> bool:
        """Checks if the document cryptographic signature is valid"""
        register_timestamp = document["register_date"]
        document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)

        with freeze_time(document_datetime):
            project_document = ProjectDocument(document["project_id"], document["file_name"])
            if project_document.document_signature == document["document_signature"]:
                return True
            raise EnterpriseManagementException("Inconsistent document signature")

    def find_docs(self, date_str: str):
        """Generates a JSON report counting valid documents for a specific date."""
        QueryDate(date_str)

        doc_store = DocumentJsonStore()
        document_list = doc_store.load_list(empty_if_missing=False)

        documents_count = 0

        for document in document_list:
            register_timestamp = document["register_date"]
            document_date_str = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")

            if document_date_str == date_str:
                if self._is_document_valid(document):
                    documents_count += 1

        if documents_count == 0:
            raise EnterpriseManagementException("No documents found")

        report_data = {
            "Querydate": date_str,
            "ReportDate": datetime.now(timezone.utc).timestamp(),
            "Numfiles": documents_count
        }

        report_store = ReportJsonStore()
        report_list = report_store.load_list(empty_if_missing=True)
        report_list.append(report_data)
        report_store.save_list(report_list)

        return documents_count
