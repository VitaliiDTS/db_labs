from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto


class EventTypes(db.Model):
    __tablename__ = 'event_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    description = db.Column(db.String(300), nullable=False)

    events = db.relationship("Events", back_populates="event_type", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Event-types({self.id}, '{self.name}', '{self.description}')"

    def put_into_dto(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> EventTypes:

        return EventTypes(
            name=dto_dict.get("name"),
            description=dto_dict.get("description"),
        )
