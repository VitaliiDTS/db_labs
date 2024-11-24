from typing import List
from my_project.auth.dao import event_types_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import EventTypes


class EventTypesService(GeneralService):

    _dao = event_types_dao

    def create(self, event_type: EventTypes) -> None:
        """
        Створює новий тип події в базі даних.
        """
        self._dao.create(event_type)

    def update(self, event_type_id: int, event_type: EventTypes) -> None:
        """
        Оновлює тип події в базі даних.

        """
        self._dao.update(event_type_id, event_type)

    def get_all_event_types(self) -> List[EventTypes]:
        """
        Отримує всі типи подій з бази даних.
        """
        return self._dao.find_all()

    def get_event_type_by_id(self, event_type_id: int) -> EventTypes:
        """
        Отримує тип події за ID.

        """
        return self._dao.find_by_id(event_type_id)

    def get_event_types_by_name(self, name: str) -> List[EventTypes]:
        """
        Отримує типи подій з таблиці бази даних за назвою.

        """
        return self._dao.find_by_name(name)
