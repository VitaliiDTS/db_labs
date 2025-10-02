from typing import List
from my_project.auth.dao import payments_dao
from my_project.auth.service.general_service import GeneralService
from my_project.auth.domain import Payments

class PaymentsService(GeneralService):

    _dao = payments_dao

    def create(self, payment: Payments) -> None:

        self._dao.create(payment)

    def get_all_payments(self) -> List[Payments]:

        return self._dao.find_all()

    def get_payment_by_id(self, payment_id: int) -> Payments:

        return self._dao.find_by_id(payment_id)

    def get_amount_statistic(self, operation: str) -> float:

        return self._dao.get_amount_statistic(operation)
