from typing import List
from my_project.auth.dao import agencies_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import Agencies

class AgenciesService(GeneralService):

    _dao = agencies_dao

    def create(self, agency: Agencies) -> None:
        """
        Створює нову агенцію в базі даних.
        """
        self._dao.create(agency)

    def update(self, agency_id: int, agency: Agencies) -> None:
        """
        Оновлює агенцію в базі даних.

        """
        self._dao.update(agency_id, agency)

    def get_all_agencies(self) -> List[Agencies]:
        """
        Отримує всі агенції з бази даних.
        """
        return self._dao.find_all()

    def get_agency_by_id(self, agency_id: int) -> Agencies:
        """
        Отримує агенцію за ID.

        """
        return self._dao.find_by_id(agency_id)

    def get_agencies_by_name(self, name: str) -> List[Agencies]:
        """
        Отримує агентства з таблиці бази даних за назвою.

        """
        return self._dao.find_by_name(name)

    def get_agencies_by_phone(self, phone: str) -> List[Agencies]:
        """
        Отримує агентства з таблиці бази даних за номером телефону.

        """
        return self._dao.find_by_phone(phone)

    def create_multiple_agencies_using_procedure(self) -> None:
        """
        Викликає процедуру для вставки 10 агентств.
        """
        self._dao.create_multiple_using_procedure()

    def call_create_and_insert_procedure(self):
        """
        Викликає збережену процедуру для створення та вставки даних.
        """
        self._dao.call_create_and_insert_procedure()
