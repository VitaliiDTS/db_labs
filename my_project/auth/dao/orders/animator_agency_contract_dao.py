from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain import AnimatorAgencyContract


class AnimatorAgencyContractDAO(GeneralDAO):
    _domain_type = AnimatorAgencyContract

    def create(self, contract: AnimatorAgencyContract) -> None:
        self._session.add(contract)
        self._session.commit()

    def find_all(self) -> List[AnimatorAgencyContract]:
        return self._session.query(AnimatorAgencyContract).all()

    def find_by_id(self, contract_id: int) -> AnimatorAgencyContract:
        return self._session.query(AnimatorAgencyContract).get(contract_id)

    def update(self, contract_id: int, contract: AnimatorAgencyContract) -> None:
        existing_contract = self.find_by_id(contract_id)
        if existing_contract:
            existing_contract.contract_start_date = contract.contract_start_date
            existing_contract.contract_end_date = contract.contract_end_date
            existing_contract.animators_id = contract.animators_id
            existing_contract.agencies_id = contract.agencies_id
            self._session.commit()

    def delete(self, contract_id: int) -> None:
        contract = self.find_by_id(contract_id)
        if contract:
            self._session.delete(contract)
            self._session.commit()
