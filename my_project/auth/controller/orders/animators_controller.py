from typing import List
from my_project.auth.service import animators_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import Animators


class AnimatorsController(GeneralController):
    _service = animators_service

    def create_animator(self, animator: Animators) -> None:
        self._service.create(animator)

    def find_all(self) -> List[Animators]:
        return self._service.get_all_animators()

    def find_by_id(self, animator_id: int) -> Animators:
        return self._service.get_animator_by_id(animator_id)

    def update_animator(self, animator_id: int, animator: Animators) -> None:
        self._service.update(animator_id, animator)

    def delete_animator(self, animator_id: int) -> None:
        self._service.delete(animator_id)

    def get_animators_by_name(self, name: str) -> List[Animators]:
        return self._service.get_animators_by_name(name)

    def get_animators_by_phone(self, phone: str) -> List[Animators]:
        return self._service.get_animators_by_phone(phone)
