
from .orders.agencies_dao import AgenciesDAO
from .orders.animators_dao import AnimatorsDAO
from .orders.animator_agency_contract_dao import AnimatorAgencyContractDAO
from .orders.event_types_dao import EventTypesDAO
from .orders.events_dao import EventsDAO
from .orders.payments_dao import PaymentsDAO

agencies_dao = AgenciesDAO()
animators_dao = AnimatorsDAO()
animator_agency_contract_dao = AnimatorAgencyContractDAO()
event_types_dao = EventTypesDAO()
events_dao = EventsDAO()
payments_dao = PaymentsDAO()
