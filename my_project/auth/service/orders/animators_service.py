from typing import List
from my_project.auth.dao import animators_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import Animators


class AnimatorsService(GeneralService):
    _dao = animators_dao

    def create(self, animator: Animators) -> None:
        self._dao.create(animator)

    def get_all_animators(self) -> List[Animators]:
        return self._dao.find_all()

    def get_animator_by_id(self, animator_id: int) -> Animators:
        return self._dao.find_by_id(animator_id)

    def update(self, animator_id: int, animator: Animators) -> None:
        self._dao.update(animator_id, animator)

    def delete(self, animator_id: int) -> None:
        self._dao.delete(animator_id)

    def get_animators_by_name(self, name: str) -> List[Animators]:
        return self._dao.find_by_name(name)

    def get_animators_by_phone(self, phone: str) -> List[Animators]:
        return self._dao.find_by_phone(phone)
