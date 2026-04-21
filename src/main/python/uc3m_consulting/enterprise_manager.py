"""Module """
import re
import json

from datetime import datetime, timezone
from freezegun import freeze_time

from uc3m_consulting.attributes.acronym import Acronym
from uc3m_consulting.attributes.description import Description
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.attributes.cif import Cif
from uc3m_consulting.attributes.acronym import Acronym

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    def read_json_store(self, file_path: str, empty_if_missing: bool = False):
        """Reads a JSON file and returns his content. Extracted for avoiding duplicated code."""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                return json.load(file)
        except FileNotFoundError as ex:
            if empty_if_missing:
                return []
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

    def write_json_store(self, file_path: str, data_list: list):
        """Writes a data list in a JSON file. Extracted for avoiding duplicated code."""
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as file:
                json.dump(data_list, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex

    def validate_starting_date(self, starting_date):
        """validates the  date format  using regex"""
        date_format = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        valid_date_format = date_format.fullmatch(starting_date)

        if not valid_date_format:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(starting_date, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return starting_date

    @staticmethod
    def validate_cif(cif:str):
        Cif(cif)
        return True

    def validate_acronym(self, project_acronym:str):
        Acronym(project_acronym)
        return True

    def validate_description(self, project_description:str):
        Description(project_description)
        return True

    def validate_department(self, department: str):
        """Validates the department name."""
        department_pattern = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        if not department_pattern.fullmatch(department):
            raise EnterpriseManagementException("Invalid department")

    def validate_budget(self, budget: str):
        """Validates the project budget amount and format."""
        try:
            float_budget = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        float_budget_string = str(float_budget)
        if '.' in float_budget_string:
            decimals = len(float_budget_string.split('.')[1])
            if decimals > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if float_budget < 50000 or float_budget > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")


    #pylint: disable=too-many-arguments, too-many-positional-arguments
    def register_project(self,
                         company_cif: str,
                         project_acronym: str,
                         project_description: str,
                         department: str,
                         date: str,
                         budget: str):

        """registers a new project"""

        # Validations:
        self.validate_cif(company_cif)
        self.validate_acronym(project_acronym)
        self.validate_description(project_description)
        self.validate_department(department)
        self.validate_budget(budget)
        self.validate_starting_date(date)

        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        transfer_list = self.read_json_store(PROJECTS_STORE_FILE, empty_if_missing=True)

        for transfer_item in transfer_list:
            if transfer_item == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        transfer_list.append(new_project.to_json())

        self.write_json_store(PROJECTS_STORE_FILE, transfer_list)

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
        document_list = self.read_json_store(TEST_DOCUMENTS_STORE_FILE, empty_if_missing=False)


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

        report_list = self.read_json_store(TEST_NUMDOCS_STORE_FILE, empty_if_missing=True)
        report_list.append(report_data)

        self.write_json_store(TEST_NUMDOCS_STORE_FILE, report_list)

        return documents_count
