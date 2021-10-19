from service.chargeHandler.AbstractHandler import AbstractHandler
from service.models import ChargeRequest, ChargeResponse


class TimeHandler(AbstractHandler):
    def handle(self, charge_request: ChargeRequest) -> ChargeResponse:

        cdr = charge_request.cdr
        rate = charge_request.rate
        time = round(
            (cdr.timestampStop - cdr.timestampStart).seconds * rate.time / 3600, 3)
        self.charge_response.components.time = time
        
        return super().handle(charge_request)
