# my_project/auth/domain/animator_agency_contract.py
from __future__ import annotations
from datetime import date
from typing import Dict, Any

from my_project import db

class AnimatorAgencyContract(db.Model):
    __tablename__ = "animator_agency_contract"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date   = db.Column(db.Date, nullable=False)
    animators_id        = db.Column(db.Integer, db.ForeignKey("animators.id"), nullable=False)
    agencies_id         = db.Column(db.Integer, db.ForeignKey("agencies.id"), nullable=False)

    animator = db.relationship("Animators", backref="contracts")
    agency   = db.relationship("Agencies", backref="contracts")

    def __repr__(self) -> str:
        return (
            f"AnimatorAgencyContract(id={self.id}, "
            f"start={self.contract_start_date}, end={self.contract_end_date}, "
            f"animators_id={self.animators_id}, agencies_id={self.agencies_id})"
        )


    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "contract_start_date": self.contract_start_date.isoformat(),
            "contract_end_date": self.contract_end_date.isoformat(),
            "animators_id": self.animators_id,
            "agencies_id": self.agencies_id,
        }

    @staticmethod
    def _to_date(v: Any) -> date:
        if isinstance(v, date):
            return v

        return date.fromisoformat(str(v))

    @staticmethod
    def create_from_dto(dto: Dict[str, Any]) -> "AnimatorAgencyContract":
        return AnimatorAgencyContract(
            contract_start_date=AnimatorAgencyContract._to_date(dto.get("contract_start_date")),
            contract_end_date=AnimatorAgencyContract._to_date(dto.get("contract_end_date")),
            animators_id=int(dto.get("animators_id")),
            agencies_id=int(dto.get("agencies_id")),
        )
