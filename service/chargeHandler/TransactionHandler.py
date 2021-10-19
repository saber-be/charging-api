from service.chargeHandler.AbstractHandler import AbstractHandler
from service.models import ChargeRequest, ChargeResponse


class TransactionHandler(AbstractHandler):
    def handle(self, charge_request: ChargeRequest) -> ChargeResponse:

        rate = charge_request.rate

        self.charge_response.components.transaction = rate.transaction

        return super().handle(charge_request)
