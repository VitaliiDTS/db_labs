from .orders.animators_controller import AnimatorsController
from .orders.agencies_controller import AgenciesController
from .orders.events_controller import EventsController
from .orders.event_types_controller import EventTypesController
from .orders.payments_controller import PaymentsController
from .orders.animator_agency_contract_controller import AnimatorAgencyContractController


animators_controller = AnimatorsController()
agencies_controller = AgenciesController()
events_controller = EventsController()
event_types_controller = EventTypesController()
payments_controller = PaymentsController()
animator_agency_contract_controller = AnimatorAgencyContractController()

__all__ = [
    "animators_controller",
    "agencies_controller",
    "events_controller",
    "event_types_controller",
    "payments_controller",
    "animator_agency_contract_controller",
    "AnimatorsController",
    "AgenciesController",
    "EventsController",
    "EventTypesController",
    "PaymentsController",
    "AnimatorAgencyContractController",
]
