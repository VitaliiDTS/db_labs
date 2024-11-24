from typing import List
from my_project.auth.dao import animator_agency_contract_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import AnimatorAgencyContract


class AnimatorAgencyContractService(GeneralService):
    _dao = animator_agency_contract_dao

    def create(self, contract: AnimatorAgencyContract) -> None:
        self._dao.create(contract)

    def get_all_contracts(self) -> List[AnimatorAgencyContract]:
        return self._dao.find_all()

    def get_contract_by_id(self, contract_id: int) -> AnimatorAgencyContract:
        return self._dao.find_by_id(contract_id)

    def update(self, contract_id: int, contract: AnimatorAgencyContract) -> None:
        self._dao.update(contract_id, contract)

    def delete(self, contract_id: int) -> None:
        self._dao.delete(contract_id)
