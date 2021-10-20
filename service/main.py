from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from service.chargeHandler.applyCharge import apply_charge
from service.models import ChargeRequest, ChargeResponse

description = """
## Charging Station Management System
- **Swagger UI: [/docs](/docs)**
- **ReDoc UI: [/redoc](/redoc)**
"""

tags_metadata = [
    {
        "name": "Charging APIs",
    },
    {
        "name": "redirects",
    },
]

app = FastAPI(title="CSMS", description=description,
              openapi_tags=tags_metadata)


@app.post("/rate", response_model=ChargeResponse, description="Will apply the given rate to the corresponding CDR.", tags=["Charging APIs"])
async def apply_rate(charge_request: ChargeRequest) -> ChargeResponse:
    return apply_charge(charge_request)


@app.get("/", response_class=RedirectResponse, tags=["redirects"])
async def docs_redirect():
    return '/docs'
