

from flask import Flask

from .error_handler import err_handler_bp


def register_routes(app: Flask) -> None:

    app.register_blueprint(err_handler_bp)


    from .orders.agencies_route import agencies_bp
    from .orders.animators_route import animators_bp
    from .orders.animator_agency_contract_route import animator_agens_contracts_bp
    from .orders.event_types_route import event_types_bp
    from .orders.events_route import events_bp
    from .orders.payments_route import payments_bp


    app.register_blueprint(agencies_bp)
    app.register_blueprint(animators_bp)
    app.register_blueprint(animator_agens_contracts_bp)
    app.register_blueprint(event_types_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(payments_bp)
