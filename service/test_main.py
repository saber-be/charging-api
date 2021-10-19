from fastapi.testclient import TestClient
from pydantic.error_wrappers import ValidationError
from service.chargeHandler.applyCharge import apply_charge
from service.chargeHandler.EnergyHandler import EnergyHandler
from service.chargeHandler.TimeHandler import TimeHandler
from service.chargeHandler.TransactionHandler import TransactionHandler
from service.main import app
from service.models import CDR, ChargeRequest, ChargeResponse, Components, Rate
import pytest
from datetime import datetime,timedelta
client = TestClient(app)


def test_apply_rate_to_cdr_with_correct_inputs():

    rate = { "energy": 0.3, "time": 2, "transaction": 1 }
    cdr = { "meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230, "timestampStop":"2021-04-05T11:27:00Z" }
    response = client.post("/", json={"cdr": cdr, "rate": rate})
    correct_response = {'components': {'energy': 3.277, 'time': 2.767, 'transaction': 1.0}, 
                        'overall': 7.04}
    assert response.status_code == 200
    assert response.json() == correct_response

def test_apply_rate_to_cdr_with_incorrect_inputs():

    rate = { "energy": -0.3, "time": 2, "transaction": 1 }
    cdr = { "meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230, "timestampStop":"2021-04-05T11:27:00Z" }
    response = client.post("/", json={"cdr": cdr, "rate": rate})
    assert response.status_code == 422

    rate = { "energy": 0.3, "time": 2, "transaction": 1 }
    cdr = { "meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230, "timestampStop":"2021-04-05T10:03:59Z" }
    response = client.post("/", json={"cdr": cdr, "rate": rate})
    assert response.status_code == 422

def test_apply_rate_to_cdr_with_missing_inputs():

    rate = { "energy": 0.3, "transaction": 1 }
    cdr = { "meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230, "timestampStop":"2021-04-05T11:27:00Z" }
    response = client.post("/", json={"cdr": cdr, "rate": rate})
    assert response.status_code == 422

def test_time_handler():
    rate = Rate(energy=0.3,time=2,transaction= 1)
    cdr = CDR(meterStart= 1204307, timestampStart = "2021-04-05T10:04:00Z", meterStop = 1215230, timestampStop = "2021-04-05T11:27:00Z")
    charge_request = ChargeRequest(rate=rate,cdr=cdr)
    time_handler = TimeHandler()
    charge_response = time_handler.handle(charge_request)
    assert charge_response.components.time == 2.767
    assert charge_response.overall == 2.77

def test_energy_handler():
    rate = Rate(energy=0.3,time=2,transaction= 1)
    cdr = CDR(meterStart= 1204307, timestampStart = "2021-04-05T10:04:00Z", meterStop = 1215230, timestampStop = "2021-04-05T11:27:00Z")
    charge_request = ChargeRequest(rate=rate,cdr=cdr)
    energy_handler = EnergyHandler()
    charge_response = energy_handler.handle(charge_request)
    assert charge_response.components.energy == 3.277
    assert charge_response.overall == 3.28

def test_transaction_handler():
    rate = Rate(energy=0.3,time=2,transaction= 1)
    cdr = CDR(meterStart= 1204307, timestampStart = "2021-04-05T10:04:00Z", meterStop = 1215230, timestampStop = "2021-04-05T11:27:00Z")
    charge_request = ChargeRequest(rate=rate,cdr=cdr)
    transaction_handler = TransactionHandler()
    charge_response = transaction_handler.handle(charge_request)
    assert charge_response.components.transaction == 1
    assert charge_response.overall == 1

def test_apply_charge():
    rate = Rate(energy=0.3,time=2,transaction= 1)
    cdr = CDR(meterStart= 1204307, timestampStart = "2021-04-05T10:04:00Z", meterStop = 1215230, timestampStop = "2021-04-05T11:27:00Z")
    charge_request = ChargeRequest(rate=rate,cdr=cdr)
    charge_response = apply_charge(charge_request)
    correct_response = ChargeResponse(components= Components(energy=3.277, time = 2.767, transaction= 1.0), 
                        overall= 7.04)
    assert charge_response == correct_response


def test_Rate_validations():
    with pytest.raises(ValidationError):
        Rate(energy=-1,time=0,transaction=0)
    
    with pytest.raises(ValidationError):
        Rate(energy=0,time=0)
    
    with pytest.raises(ValidationError):
        Rate(time=0,transaction=0)

    with pytest.raises(ValidationError):
        Rate(energy=0,transaction=0)
    
    with pytest.raises(ValidationError):
        Rate()

def test_CDR_validations_times():
    now = datetime.now()
    with pytest.raises(ValidationError):
        CDR(meterStart = 0,
            timestampStart= now,
            meterStop= 10,
            timestampStop = now)


def test_CDR_validations_meters():
    now = datetime.now()
    with pytest.raises(ValidationError):
        CDR(meterStart = 0,
            timestampStart= now,
            meterStop= 0,
            timestampStop = now + timedelta(seconds=1))
    
    with pytest.raises(ValidationError):
        CDR(meterStart = 10,
            timestampStart= now,
            meterStop= 10,
            timestampStop = now + timedelta(seconds=1))

    with pytest.raises(ValidationError):
        CDR(meterStart = 10,
            timestampStart= now,
            meterStop= 8,
            timestampStop = now + timedelta(seconds=1))

