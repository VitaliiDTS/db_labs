from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto

class Payments(db.Model, IDto):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    payment_methods = db.Column(db.String(10), nullable=False)
    events_id = db.Column(db.Integer, db.ForeignKey('events.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    event = db.relationship("Events", back_populates="payments")

    def __repr__(self) -> str:
        return f"Payments({self.id}, {self.amount}, {self.status}, '{self.payment_methods}', {self.events_id})"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "amount": self.amount,
            "status": self.status,
            "payment_methods": self.payment_methods,
            "events_id": self.events_id,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Payments:
        return Payments(
            amount=dto_dict.get("amount"),
            status=dto_dict.get("status"),
            payment_methods=dto_dict.get("payment_methods"),
            events_id=dto_dict.get("events_id"),
        )
