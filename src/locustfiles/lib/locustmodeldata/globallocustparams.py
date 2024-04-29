"""
Data models for Common Locust Parameters

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    conlist,
    field_validator,
    PositiveInt,
    NonNegativeFloat,
)


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class DataModel(BaseConfigModel):
    """Global parameters commonly used for all Locust files"""

    insecure: Optional[bool] = True
    network_timeout: Optional[int] = Field(ge=1, le=120, default=60)
    connection_timeout: Optional[int] = Field(ge=1, le=120, default=60)
    wait_time_between: Optional[
        conlist(NonNegativeFloat, min_length=2, max_length=2)
    ] = [
        0,
        0,
    ]
    rest_delay_time_between: Optional[
        conlist(NonNegativeFloat, min_length=2, max_length=2)
    ] = [0, 0]
    group_requests: Optional[bool] = True
    log_tracked_failed_responses: Optional[bool] = False
    skip_clenup: Optional[bool] = False
    cleanup_ramp_down: Optional[int] = 10
    cleanup_time_between: Optional[conlist(PositiveInt, min_length=2, max_length=2)] = [
        0,
        0,
    ]

    @field_validator("cleanup_time_between")
    @classmethod
    def range_processed(cls, value):
        """Validate range for start < stop"""
        if value[0] > value[1]:
            raise ValueError(
                f"Cleanup time between range {range} invalid.  Start > Stop."
            )
        return value

    @field_validator("rest_delay_time_between")
    @classmethod
    def wait_time_between_range(cls, value):
        """Validate rest_delay_time_between range values are start <= stop"""
        if value[0] > value[1]:
            raise ValueError(f"rest_delay_time_between {value} invalid.  Start > Stop.")
        return value


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params)
    return validated_params
