"""
Data models for Devices Parameters
These parameters are typically used within a locust file
and include the smx namd and device name being tested.

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class DataModel(BaseConfigModel):
    """Global parameters commonly used for all Locust files"""

    smx_name: str
    device_name: Optional[str | list[str]] = []

    @field_validator("device_name")
    @classmethod
    def change_device_names_to_list(cls, value: str | list[str]) -> list[str]:
        """Validate device_names"""
        if isinstance(value, str):
            return [value]
        return value


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params)
    return validated_params
