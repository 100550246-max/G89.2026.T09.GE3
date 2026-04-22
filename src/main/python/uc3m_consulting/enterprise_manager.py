"""Module """
import re
import json

from datetime import datetime, timezone
from freezegun import freeze_time

from uc3m_consulting.attributes.acronym import Acronym
from uc3m_consulting.attributes.department import Department
from uc3m_consulting.attributes.description import Description
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.storage.project_json_store import ProjectJsonStore
from uc3m_consulting.storage.document_json_store import DocumentJsonStore
from uc3m_consulting.storage.report_json_store import ReportJsonStore


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


    def find_docs(self, date_str):
        """
        Generates a JSON report counting valid documents for a specific date.

        Checks cryptographic hashes and timestamps to ensure historical data integrity.
        Saves the output to 'resultado.json'.

        Args:
            date_str (str): date to query.

        Returns:
            number of documents found if report is successfully generated and saved.

        Raises:
            EnterpriseManagementException: On invalid date, file IO errors,
                missing data, or cryptographic integrity failure.
        """
        date_pattern = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        valid_date = date_pattern.fullmatch(date_str)
        if not valid_date:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        # open documents
        doc_store = DocumentJsonStore()
        document_list = doc_store.load_list(empty_if_missing=False)


        documents_count = 0

        # loop to find
        for document in document_list:
            register_timestamp = document["register_date"]

            # string conversion for easy match
            document_date_str = datetime.fromtimestamp(register_timestamp).strftime("%d/%m/%Y")

            if document_date_str == date_str:
                document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)
                with freeze_time(document_datetime):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    project_document = ProjectDocument(document["project_id"], document["file_name"])
                    if project_document.document_signature == document["document_signature"]:
                        documents_count = documents_count + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if documents_count == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        current_timestamp = datetime.now(timezone.utc).timestamp()
        report_data = {"Querydate":  date_str,
             "ReportDate": current_timestamp,
             "Numfiles": documents_count
             }

        report_store = ReportJsonStore()
        report_list = report_store.load_list(empty_if_missing=True)
        report_list.append(report_data)
        report_store.save_list(report_list)

        return documents_count
