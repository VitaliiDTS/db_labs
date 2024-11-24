"""
2022
apavelchak@gmail.com
© Andrii Pavelchak
"""


from .orders.agencies_controller import AgenciesController
from .orders.animators_controller import AnimatorsController
from .orders.animator_agency_contract_controller import AnimatorAgencyContractController
from .orders.event_types_controller import EventTypesController
from .orders.events_controller import EventsController


agencies_controller = AgenciesController()
animators_controller = AnimatorsController()
animator_agency_contract_controller = AnimatorAgencyContractController()
event_types_controller = EventTypesController()
events_controller = EventsController()
