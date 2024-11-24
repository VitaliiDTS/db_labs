from typing import List
from my_project.auth.service import event_types_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import EventTypes


class EventTypesController(GeneralController):

    _service = event_types_service

    def create_event_type(self, event_type: EventTypes) -> None:
        """
        Створює новий тип події в базі даних.

        """
        self._service.create(event_type)

    def find_all(self) -> List[EventTypes]:
        """
        Отримує всі типи подій з бази даних.

        """
        return self._service.get_all_event_types()

    def find_by_id(self, event_type_id: int) -> EventTypes:
        """
        Отримує тип події за ID.

        """
        return self._service.get_event_type_by_id(event_type_id)

    def update_event_type(self, event_type_id: int, event_type: EventTypes) -> None:
        """
        Оновлює тип події за ID.

        """
        self._service.update(event_type_id, event_type)

    def delete_event_type(self, event_type_id: int) -> None:
        """
        Видаляє тип події за ID.

        """
        self._service.delete(event_type_id)

    def get_event_types_by_name(self, name: str) -> List[EventTypes]:
        """
        Отримує типи подій за назвою.

        """
        return self._service.get_event_types_by_name(name)
