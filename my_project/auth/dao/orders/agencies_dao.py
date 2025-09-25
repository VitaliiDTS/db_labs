from typing import List
from my_project.auth.dao.general_dao import GeneralDAO
from my_project.auth.domain.orders.agencies import Agencies
from sqlalchemy import text


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

    def create_multiple_using_procedure(self) -> None:
        """
        Викликає збережену процедуру для вставки 10 агентств у базу даних.
        """
        try:
            self._session.execute("CALL Insert10Agencies()")
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise e

    def call_create_and_insert_procedure(self):
        """
        Викликає збережену процедуру для створення та вставки даних.
        """
        try:
            self._session.execute(text("CALL create_and_insert_into_new_tables()"))
            self._session.commit()
        except Exception as e:
            self._session.rollback()
            raise Exception(f"Error executing stored procedure: {str(e)}")