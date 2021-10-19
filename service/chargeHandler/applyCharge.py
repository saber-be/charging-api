from service.models import ChargeRequest, ChargeResponse
from service.chargeHandler.EnergyHandler import EnergyHandler
from service.chargeHandler.TimeHandler import TimeHandler
from service.chargeHandler.TransactionHandler import TransactionHandler


def apply_charge(charge_request: ChargeRequest) -> ChargeResponse:

    charge_handler = TimeHandler()
    charge_handler.set_next(EnergyHandler()) \
                  .set_next(TransactionHandler())
    return charge_handler.handle(charge_request) 
    