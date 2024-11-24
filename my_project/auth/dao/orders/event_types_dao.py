from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import EventTypes

class EventTypesDAO(GeneralDAO):

    _domain_type = EventTypes

    def create(self, event_type: EventTypes) -> None:
        """
        Додає новий тип події в базу даних.
        """
        self._session.add(event_type)
        self._session.commit()

    def find_all(self) -> List[EventTypes]:
        """
        Отримує всі типи подій з таблиці бази даних.
        """
        return self._session.query(EventTypes).all()

    def find_by_name(self, name: str) -> List[EventTypes]:
        """
        Отримує типи подій за полем 'name'.

        """
        return self._session.query(EventTypes).filter(EventTypes.name == name).order_by(EventTypes.name).all()

    def find_by_id(self, event_type_id: int) -> EventTypes:
        """
        Отримує тип події за ID.

        """
        return self._session.query(EventTypes).filter(EventTypes.id == event_type_id).first()

