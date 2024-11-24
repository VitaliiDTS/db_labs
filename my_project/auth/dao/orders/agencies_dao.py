from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.agencies import Agencies

class AgenciesDAO(GeneralDAO):

    _domain_type = Agencies

    def create(self, agency: Agencies) -> None:
        """
        Додає нову агенцію в базу даних.
        """
        self._session.add(agency)
        self._session.commit()

    def find_all(self) -> List[Agencies]:
        """
        Отримує всі агенції з таблиці бази даних.
        """
        return self._session.query(Agencies).all()

    def find_by_name(self, name: str) -> List[Agencies]:
        """
        Отримує агентства з таблиці бази даних за полем name.

        """
        return self._session.query(Agencies).filter(Agencies.name == name).order_by(Agencies.name).all()

    def find_by_phone(self, phone: str) -> List[Agencies]:
        """
        Отримує агентства з таблиці бази даних за полем 'phone'.

        """
        return self._session.query(Agencies).filter(Agencies.phone == phone).order_by(Agencies.phone.desc()).all()

    def find_by_id(self, agency_id: int) -> Agencies:
        """
        Отримує агентство за ID.

        """
        return self._session.query(Agencies).filter(Agencies.id == agency_id).first()
