from typing import List
from my_project.auth.service import agencies_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import Agencies
class AgenciesController(GeneralController):

    _service = agencies_service

    def create_agency(self, agency: Agencies) -> None:
        """
        Створює нову агенцію в базі даних.

        """
        self._service.create(agency)

    def find_all(self) -> List[Agencies]:
        """
        Отримує всі агенції з бази даних.

        """
        return self._service.get_all_agencies()

    def find_by_id(self, agency_id: int) -> Agencies:
        """
        Отримує агенцію за ID.

        """
        return self._service.get_agency_by_id(agency_id)

    def update_agency(self, agency_id: int, agency: Agencies) -> None:
        """
        Оновлює агенцію за ID.

        """
        self._service.update(agency_id, agency)

    def delete_agency(self, agency_id: int) -> None:
        """
        Видаляє агенцію за ID.

        """
        self._service.delete(agency_id)

    def get_agencies_by_name(self, name: str) -> List[Agencies]:
        """
        Отримує агенції за назвою.

        """
        return self._service.get_agencies_by_name(name)

    def get_agencies_by_phone(self, phone: str) -> List[Agencies]:
        """
        Отримує агенції за номером телефону.
        """
        return self._service.get_agencies_by_phone(phone)
