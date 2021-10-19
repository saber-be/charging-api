from pydantic import BaseModel, Field, root_validator
import datetime


class CDR(BaseModel):
    meterStart: int = Field(..., ge=0,
                            description="meter value of the electricity meter when the charging process was started")

    timestampStart: datetime.datetime = Field(
        ..., description="timestamp (according to ISO 8601) when the charging process was started")

    meterStop: int = Field(..., gt=0,
                           description="meter value of the electricity meter when the charging process was stopped")

    timestampStop: datetime.datetime = Field(
        ..., description="timestamp (according to ISO 8601) when the charging process was stopped")

    @root_validator
    def check_meters(cls, values):
        meterStart, meterStop = values.get(
            'meterStart'), values.get('meterStop')
        if meterStop <= meterStart:
            raise ValueError(
                'cdr.meterStop should be greater than cdr.meterStart')
        return values

    @root_validator
    def check_timestamps(cls, values):
        timestampStart, timestampStop = values.get(
            'timestampStart'), values.get('timestampStop')
        if timestampStop <= timestampStart:
            raise ValueError(
                'cdr.timestampStop should be greater than cdr.timestampStart')
        return values


class Components(BaseModel):
    energy: float = Field(0, ge=0)
    time: float = Field(0, ge=0)
    transaction: float = Field(0, ge=0)


class Rate(Components):
    energy: float = Field(..., ge=0,
                          description="rate the charging process based on the energy consumed")
    time: float = Field(..., ge=0,
                        description="rate the charging process based on its duration")
    transaction: float = Field(..., ge=0,
                               description="fees per charging process")


class ChargeRequest(BaseModel):
    rate: Rate = Field(...)
    cdr: CDR = Field(..., title="charge detail record")


class ChargeResponse(BaseModel):
    overall: float = 0
    components: Components = Components(energy=0, time=0, transaction=0)
