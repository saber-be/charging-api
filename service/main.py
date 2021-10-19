from fastapi import FastAPI
from service.models import ChargeRequest, ChargeResponse
from service.chargeHandler.applyCharge import apply_charge
app = FastAPI()


@app.post("/")
async def apply_rate_to_cdr(charge_request: ChargeRequest) -> ChargeResponse:
    return apply_charge(charge_request)
 
