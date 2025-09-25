from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.payments import Payments

class PaymentsDAO(GeneralDAO):

    _domain_type = Payments

    def create(self, payment: Payments) -> None:
        """
        Додає новий платіж в базу даних.
        """
        self._session.add(payment)
        self._session.commit()

    def find_all(self) -> List[Payments]:
        """
        Отримує всі платежі з таблиці бази даних.
        """
        return self._session.query(Payments).all()

    def find_by_id(self, payment_id: int) -> Payments:
        """
        Отримує платіж за ID.
        """
        return self._session.query(Payments).filter(Payments.id == payment_id).first()

    def get_amount_statistic(self, operation: str) -> float:
        """
        Викликає функцію для отримання статистики по стовпцю amount.
        """
        return self._session.execute(f"SELECT get_amount_statistic('{operation}')").scalar()
