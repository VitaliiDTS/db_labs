from __future__ import annotations
from typing import Dict, Any
from my_project import db
from my_project.auth.domain.i_dto import IDto

class Animators(db.Model, IDto):
    __tablename__ = "animators"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False)
    surname = db.Column(db.String(25), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(60), nullable=False)

    def __repr__(self) -> str:
        return f"Animators({self.id}, '{self.name}', '{self.surname}', '{self.date_of_birth}', '{self.phone}', '{self.email}')"

    def put_into_dto(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "date_of_birth": str(self.date_of_birth),
            "phone": self.phone,
            "email": self.email,
        }

    @staticmethod
    def create_from_dto(dto_dict: Dict[str, Any]) -> Animators:
        return Animators(
            name=dto_dict.get("name"),
            surname=dto_dict.get("surname"),
            date_of_birth=dto_dict.get("date_of_birth"),
            phone=dto_dict.get("phone"),
            email=dto_dict.get("email"),
        )
