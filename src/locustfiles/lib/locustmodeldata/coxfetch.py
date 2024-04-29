"""
Data models for ONT Crud User

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional, List
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
    class_validators,
    field_validator,
)


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class FetchModel(BaseConfigModel):
    """Top level nested Test Data for User"""

    fixed_max_user_count: Optional[int] = 0
    random_device: Optional[bool] = False
    all_synced_devices_pool: Optional[bool] = False
    device_name_pool: Optional[List[str]] = []

    @field_validator("device_name_pool")
    @classmethod
    def remove_dupes_from_device_name_pool(cls, value):
        """Remove duplicate device names from pool"""
        return list(set(value))


class DataModel(BaseConfigModel):
    """VLAN CRUD data model base class"""

    cox_fetch_data: Optional[FetchModel] = None


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for Cox Fetch User.
    Ignore all other params.
    """
    validated_params = DataModel(**params).cox_fetch_data
    return validated_params
