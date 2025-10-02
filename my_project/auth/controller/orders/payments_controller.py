from my_project.auth.service import payments_service
from my_project.auth.controller.general_controller import GeneralController
from my_project.auth.domain import Payments
from typing import List

class PaymentsController(GeneralController):

    _service = payments_service

    def create_payment(self, payment: Payments) -> None:

        self._service.create(payment)

    def get_all_payments(self) -> List[Payments]:

        return self._service.get_all_payments()

    def get_payment_by_id(self, payment_id: int) -> Payments:

        return self._service.get_payment_by_id(payment_id)

    def get_amount_statistic(self, operation: str) -> float:

        return self._service.get_amount_statistic(operation)

    def update_payment(self, payment_id: int, payment: Payments) -> None:
        self._service.update(payment_id, payment)

    def delete_payment(self, payment_id: int) -> None:
        self._service.delete(payment_id)

    def get_amount_statistic(self, operation: str) -> float:
        return self._service.get_amount_statistic(operation)