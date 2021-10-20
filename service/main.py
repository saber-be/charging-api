from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from service.chargeHandler.applyCharge import apply_charge
from service.models import ChargeRequest, ChargeResponse

app = FastAPI()


@app.post("/rate",response_model=ChargeResponse,description="Will apply the given rate to the corresponding CDR.")
async def apply_rate(charge_request: ChargeRequest) -> ChargeResponse:
    return apply_charge(charge_request)

@app.get("/",response_class=RedirectResponse)
async def docs_redirect():
    return '/docs'
 
