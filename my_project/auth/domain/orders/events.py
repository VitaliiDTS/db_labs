from __future__ import annotations
from typing import Dict, Any, Optional
from datetime import date as _date, time as _time, datetime as _dt

from my_project import db
from my_project.auth.domain.i_dto import IDto


def _to_date(v: Any) -> Optional[_date]:
    """Приймає date | str | None -> повертає date | None."""
    if v is None or isinstance(v, _date):
        return v
    if isinstance(v, str) and v.strip():
        # підтримка формату 'YYYY-MM-DD'
        return _date.fromisoformat(v)
    return None


def _to_time(v: Any) -> Optional[_time]:
    """Приймає time | str | None -> повертає time | None."""
    if v is None or isinstance(v, _time):
        return v
    if isinstance(v, str) and v.strip():
        # підтримка 'HH:MM' або 'HH:MM:SS'
        return _time.fromisoformat(v)
    return None


class Events(db.Model, IDto):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    address = db.Column(db.String(60), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)

    event_types_id = db.Column(db.Integer, db.ForeignKey("event_types.id"), nullable=False)
    event_type = db.relationship("EventTypes", back_populates="events")

    # зв'язок з Payments (має бути back_populates="event" у моделі Payments)
    payments = db.relationship("Payments", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"Events({self.id}, date='{self.date}', start_time='{self.start_time}', "
            f"end_time='{self.end_time}', address='{self.address}', total_price={self.total_price}, "
            f"event_types_id={self.event_types_id})"
        )

    def put_into_dto(self) -> Dict[str, Any]:
        """Безпечна серіалізація у JSON-DTO."""
        d = self.date
        st = self.start_time
        et = self.end_time

        def _iso(v: Any) -> Optional[str]:
            if v is None:
                return None
            # якщо це date/time — isoformat(); інакше просто str(...)
            return v.isoformat() if hasattr(v, "isoformat") else str(v)

        return {
            "id": self.id,
            "date": _iso(d),
            "start_time": _iso(st),
            "end_time": _iso(et),
            "address": self.address,
            "total_price": int(self.total_price) if self.total_price is not None else None,
            "event_types_id": self.event_types_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Events:
        """Створює доменний об’єкт з DTO, гарантовано парсить дату/час."""
        return Events(
            date=_to_date(dto_dict.get("date")),
            start_time=_to_time(dto_dict.get("start_time")),
            end_time=_to_time(dto_dict.get("end_time")),
            address=dto_dict.get("address"),
            total_price=int(dto_dict.get("total_price")) if dto_dict.get("total_price") is not None else 0,
            event_types_id=int(dto_dict.get("event_types_id")) if dto_dict.get("event_types_id") is not None else None,
        )
