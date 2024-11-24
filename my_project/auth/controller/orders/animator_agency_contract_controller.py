from typing import List
from my_project.auth.service import animator_agency_contract_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import AnimatorAgencyContract


class AnimatorAgencyContractController(GeneralController):
    _service = animator_agency_contract_service

    def create_contract(self, contract: AnimatorAgencyContract) -> None:
        self._service.create(contract)

    def find_all(self) -> List[AnimatorAgencyContract]:
        return self._service.get_all_contracts()

    def find_by_id(self, contract_id: int) -> AnimatorAgencyContract:
        return self._service.get_contract_by_id(contract_id)

    def update_contract(self, contract_id: int, contract: AnimatorAgencyContract) -> None:
        self._service.update(contract_id, contract)

    def delete_contract(self, contract_id: int) -> None:
        self._service.delete(contract_id)
