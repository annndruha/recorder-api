from datetime import datetime
from typing import List

from pydantic import constr, BaseModel, Field, field_validator


# General Schemas
class SuccessResponseSchema(BaseModel):
    detail: str = 'Some message'


class ErrorResponseSchema(BaseModel):
    error: str = 'Some error explanation'


class ForbiddenSchema(BaseModel):
    detail: str = 'Unauthorized. Given ADMIN_TOKEN not accepted'


# Device Schemas
class DeviceSchema(BaseModel):
    device_id: int = 42
    device_name: constr(strip_whitespace=True, min_length=3) = "my_device_name"
    device_token: str = "UPPERCASE_TOKEN"
    created_date: datetime


class FieldsType(BaseModel):
    field_name: str = 'PostgreSQL database column name'
    field_type: str = 'PostgreSQL database type'

    # @field_validator('column_name', mode='before')
    # def validate_pages(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError('column_name must be str')
    #     return value
    #
    # @field_validator('column_type', mode='before')
    # def validate_pages(self, value: str):
    #     if not isinstance(value, str):
    #         raise ValueError('column_type must be str')
    #     return value


class FieldsTypes(BaseModel):
    fields: List[FieldsType]


class ListDevicesSchema(BaseModel):
    devices: List[DeviceSchema]


# Measurements Schemas
class MeasurementSchema(BaseModel):
    primary_key: int
    timestamp: datetime
    device_id: int
    temperature: float
    humidity: float


class ListMeasurementsSchema(BaseModel):
    length: int
    timestamps: List[datetime]
    temperatures: List[float]
    humiditys: List[float]
