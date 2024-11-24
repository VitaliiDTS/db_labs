from typing import List
from my_project.auth.dao import events_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import Events

class EventsService(GeneralService):
    _dao = events_dao

    def create(self, event: Events) -> None:
        self._dao.create(event)

    def update(self, event_id: int, event: Events) -> None:
        self._dao.update(event_id, event)

    def get_all_events(self) -> List[Events]:
        return self._dao.find_all()

    def get_event_by_id(self, event_id: int) -> Events:
        return self._dao.find_by_id(event_id)

    def delete_event(self, event_id: int) -> None:
        self._dao.delete(event_id)
