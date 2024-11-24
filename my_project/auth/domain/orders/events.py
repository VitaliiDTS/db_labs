from __future__ import annotations
from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto

class Events(db.Model, IDto):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    # Foreign key and relationship to `EventTypes`
    event_types_id = db.Column(db.Integer, db.ForeignKey("event_types.id"), nullable=False)
    event_type = db.relationship("EventTypes", back_populates="events")

    def __repr__(self) -> str:
        return (
            f"Events({self.id}, date='{self.date}', start_time='{self.start_time}', "
            f"end_time='{self.end_time}', address='{self.address}', total_price={self.total_price}, "
            f"event_types_id={self.event_types_id})"
        )

    def put_into_dto(self) -> Dict[str, Any]:
        """
        Puts domain object into DTO without relationship
        :return: DTO object as dictionary
        """
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "address": self.address,
            "total_price": self.total_price,
            "event_types_id": self.event_types_id
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Events:
        """
        Creates domain object from DTO
        :param dto_dict: DTO object
        :return: Domain object
        """
        return Events(
            date=dto_dict.get("date"),
            start_time=dto_dict.get("start_time"),
            end_time=dto_dict.get("end_time"),
            address=dto_dict.get("address"),
            total_price=dto_dict.get("total_price"),
            event_types_id=dto_dict.get("event_types_id")
        )
