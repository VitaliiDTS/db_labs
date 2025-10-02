from typing import List
from my_project.auth.service import agencies_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import Agencies
class AgenciesController(GeneralController):

    _service = agencies_service

    def create_agency(self, agency: Agencies) -> None:

        self._service.create(agency)

    def find_all(self) -> List[Agencies]:

        return self._service.get_all_agencies()

    def find_by_id(self, agency_id: int) -> Agencies:

        return self._service.get_agency_by_id(agency_id)

    def update_agency(self, agency_id: int, agency: Agencies) -> None:

        self._service.update(agency_id, agency)

    def delete_agency(self, agency_id: int) -> None:

        self._service.delete(agency_id)

    def get_agencies_by_name(self, name: str) -> List[Agencies]:

        return self._service.get_agencies_by_name(name)

    def get_agencies_by_phone(self, phone: str) -> List[Agencies]:

        return self._service.get_agencies_by_phone(phone)

    def create_multiple_agencies_using_procedure(self) -> None:

        self._service.create_multiple_agencies_using_procedure()

    def call_create_and_insert_procedure(self):

        self._service.call_create_and_insert_procedure()