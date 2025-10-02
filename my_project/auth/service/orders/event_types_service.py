from typing import List
from my_project.auth.dao import event_types_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import EventTypes


class EventTypesService(GeneralService):

    _dao = event_types_dao

    def create(self, event_type: EventTypes) -> None:

        self._dao.create(event_type)

    def update(self, event_type_id: int, event_type: EventTypes) -> None:

        self._dao.update(event_type_id, event_type)

    def get_all_event_types(self) -> List[EventTypes]:

        return self._dao.find_all()

    def get_event_type_by_id(self, event_type_id: int) -> EventTypes:

        return self._dao.find_by_id(event_type_id)

    def get_event_types_by_name(self, name: str) -> List[EventTypes]:

        return self._dao.find_by_name(name)
