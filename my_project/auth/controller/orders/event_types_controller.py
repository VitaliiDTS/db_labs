from typing import List
from my_project.auth.service import event_types_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import EventTypes


class EventTypesController(GeneralController):

    _service = event_types_service

    def create_event_type(self, event_type: EventTypes) -> None:

        self._service.create(event_type)

    def find_all(self) -> List[EventTypes]:

        return self._service.get_all_event_types()

    def find_by_id(self, event_type_id: int) -> EventTypes:

        return self._service.get_event_type_by_id(event_type_id)

    def update_event_type(self, event_type_id: int, event_type: EventTypes) -> None:

        self._service.update(event_type_id, event_type)

    def delete_event_type(self, event_type_id: int) -> None:

        self._service.delete(event_type_id)

    def get_event_types_by_name(self, name: str) -> List[EventTypes]:

        return self._service.get_event_types_by_name(name)
