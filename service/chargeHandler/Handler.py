from __future__ import annotations
from abc import ABC, abstractmethod
from service.models import ChargeRequest, ChargeResponse


class Handler(ABC):
    """
    The Verifier interface declares a method for building the chain of verifiers.
    """
    charge_response: ChargeResponse

    @abstractmethod
    def set_next(self, verifier: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, rate_cdr: ChargeRequest) -> ChargeResponse:
        pass
