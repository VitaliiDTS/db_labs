from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import Animators


class AnimatorsDAO(GeneralDAO):
    _domain_type = Animators

    def create(self, animator: Animators) -> None:
        self._session.add(animator)
        self._session.commit()

    def find_all(self) -> List[Animators]:
        return self._session.query(Animators).all()

    def update(self, animator_id: int, animator: Animators) -> None:
        existing_animator = self.find_by_id(animator_id)
        if existing_animator:
            existing_animator.name = animator.name
            existing_animator.surname = animator.surname
            existing_animator.date_of_birth = animator.date_of_birth
            existing_animator.phone = animator.phone
            existing_animator.email = animator.email
            self._session.commit()

    def delete(self, animator_id: int) -> None:
        animator = self.find_by_id(animator_id)
        if animator:
            self._session.delete(animator)
            self._session.commit()

    def find_by_id(self, animator_id: int) -> Animators:
        return self._session.query(Animators).get(animator_id)

    def find_by_name(self, name: str) -> List[Animators]:
        return self._session.query(Animators).filter(Animators.name == name).all()

    def find_by_phone(self, phone: str) -> List[Animators]:
        return self._session.query(Animators).filter(Animators.phone == phone).all()
