"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""


from .orders.agencies_service import AgenciesService
from .orders.animators_service import AnimatorsService
from .orders.animator_agency_contract_service import AnimatorAgencyContractService
from .orders.event_types_service import EventTypesService
from .orders.events_service import EventsService
from .orders.payments_service import PaymentsService


agencies_service = AgenciesService()
animators_service = AnimatorsService()
animator_agency_contract_service = AnimatorAgencyContractService()
event_types_service = EventTypesService()
events_service = EventsService()
payments_service = PaymentsService()
