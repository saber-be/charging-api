from service.chargeHandler.Handler import Handler
from service.chargeHandler.AbstractHandler import AbstractHandler
from service.models import ChargeRequest, ChargeResponse


class EnergyHandler(AbstractHandler):
    def handle(self, charge_request: ChargeRequest) -> ChargeResponse:
        cdr = charge_request.cdr
        rate = charge_request.rate
        energy = round((cdr.meterStop-cdr.meterStart) * rate.energy / 1000, 3)
        self.charge_response.components.energy = energy

        return super().handle(charge_request)
