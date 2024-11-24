from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import Events

class EventsDAO(GeneralDAO):
    _domain_type = Events

    def create(self, event: Events) -> None:
        self._session.add(event)
        self._session.commit()

    def find_all(self) -> List[Events]:
        return self._session.query(Events).all()

    def find_by_id(self, event_id: int) -> Events:
        return self._session.query(Events).filter(Events.id == event_id).first()

