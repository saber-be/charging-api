from abc import abstractmethod
from service.models import ChargeRequest, ChargeResponse
from service.chargeHandler.Handler import Handler
class AbstractHandler(Handler):

    _next_handler: Handler = None
    def __init__(self) -> None:
        self.charge_response = ChargeResponse()
        
    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler
    def calc_overall_charge_value(self):
        overall = 0
        for key,value in self.charge_response.components:
            overall += value

        return round(overall,2) 
    @abstractmethod
    def handle(self, charge_request: ChargeRequest) -> ChargeResponse:
        
        self.charge_response.overall = self.calc_overall_charge_value()
        if self._next_handler:
            self._next_handler.charge_response = self.charge_response
            return self._next_handler.handle(charge_request)

        return self.charge_response