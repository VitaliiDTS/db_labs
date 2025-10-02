from __future__ import annotations
from typing import Dict, Any

from my_project import db
from my_project.auth.domain.i_dto import IDto

class Agencies(db.Model, IDto):
    __tablename__ = "agencies"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(60))
    phone = db.Column(db.String(12))
    email = db.Column(db.String(60))

    def __repr__(self) -> str:
        return f"Agencies({self.id}, '{self.name}', '{self.address}', '{self.phone}', '{self.email}')"

    def put_into_dto(self) -> Dict[str, Any]:

        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "email": self.email,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Agencies:

        return Agencies(
            name=dto_dict.get("name"),
            address=dto_dict.get("address"),
            phone=dto_dict.get("phone"),
            email=dto_dict.get("email"),
        )
