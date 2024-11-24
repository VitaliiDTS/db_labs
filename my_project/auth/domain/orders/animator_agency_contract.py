from datetime import date
from my_project import db
from my_project.auth.domain import Agencies
from my_project.auth.domain import Animators


class AnimatorAgencyContract(db.Model):
    __tablename__ = 'animator_agency_contract'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contract_start_date = db.Column(db.Date, nullable=False)
    contract_end_date = db.Column(db.Date, nullable=False)
    animators_id = db.Column(db.Integer, db.ForeignKey('animators.id'), nullable=False)
    agencies_id = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)

    animator = db.relationship('Animators', backref='contracts')
    agency = db.relationship('Agencies', backref='contracts')

    def put_into_dto(self):
        return {
            'id': self.id,
            'contract_start_date': self.contract_start_date,
            'contract_end_date': self.contract_end_date,
            'animators_id': self.animators_id,
            'agencies_id': self.agencies_id
        }

    @staticmethod
    def create_from_dto(data):
        return AnimatorAgencyContract(
            contract_start_date=data['contract_start_date'],
            contract_end_date=data['contract_end_date'],
            animators_id=data['animators_id'],
            agencies_id=data['agencies_id']
        )
