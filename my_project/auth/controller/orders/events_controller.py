from typing import List
from my_project.auth.service import events_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import Events


class EventsController(GeneralController):
    _service = events_service

    def create_event(self, event: Events) -> None:
        self._service.create(event)

    def find_all(self) -> List[Events]:
        return self._service.get_all_events()

    def find_by_id(self, event_id: int) -> Events:
        return self._service.get_event_by_id(event_id)

    def update_event(self, event_id: int, event: Events) -> None:
        self._service.update(event_id, event)

    def delete_event(self, event_id: int) -> None:
        self._service.delete_event(event_id)
