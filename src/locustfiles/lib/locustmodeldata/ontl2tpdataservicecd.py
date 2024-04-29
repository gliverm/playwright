"""
Data models for L3 1:1 Service Crud User

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional, List
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class ONTDataServiceModel(BaseConfigModel):
    """ONT Data Service for L3 1:1 Service Crud User"""

    vlan: Optional[int] = None
    service_name: Optional[str] = None
    ont_port_id: Optional[str] = None


class ONTConfigModel(BaseConfigModel):
    """ONT Config Data for L3 1:1 Service Crud User"""

    ont_id: str
    subscriber_id: str
    device_name: Optional[str] = None
    data_service: Optional[ONTDataServiceModel] | None


class ONTDefaultsModel(BaseConfigModel):
    """ONT Defaults Data for L3 1:1 Service Crud User"""

    device_name: Optional[str] = None
    data_service: Optional[ONTDataServiceModel] = None


class ONTModel(BaseConfigModel):
    """ONT Data for L3 1:1 Service Crud User"""

    force_delete: str
    defaults: ONTDefaultsModel
    ont_config: List[ONTConfigModel]

    @field_validator("force_delete")
    @classmethod
    def force_delete_must_be_valid(cls, value: str) -> str:
        """Validate ont force_delete"""
        if value.lower() not in ["false", "true"]:
            raise ValueError("ont force_delete must be 'true' or 'false'")
        return value.lower()

    @model_validator(mode="after")
    def fill_in_ont_config_defaults(self) -> "ONTModel":
        """Fill in ONT defaults for ONT config"""
        # TODO Remove duplicate ONT IDs
        # TODO Check for expected populated values
        data_service = self.defaults.data_service
        device_name = self.defaults.device_name
        for ont in self.ont_config:
            if ont.device_name is None:
                ont.device_name = device_name
            if ont.data_service is None:
                ont.data_service = data_service
            else:
                if ont.data_service.vlan is None:
                    ont.data_service.vlan = self.defaults.data_service.vlan
                if ont.data_service.service_name is None:
                    ont.data_service.service_name = (
                        self.defaults.data_service.service_name
                    )
                if ont.data_service.ont_port_id is None:
                    ont.data_service.ont_port_id = (
                        self.defaults.data_service.ont_port_id
                    )
        return self


class ONTsModel(BaseConfigModel):
    """Top level nested Test Data for L3 1:1 Service Crud User"""

    onts: ONTModel


class DataModel(BaseConfigModel):
    """Base Test Data for L3 1:1 Service Crud User"""

    ont_l2tp_data_service_data: Optional[ONTsModel] = None


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params).ont_l2tp_data_service_data
    return validated_params
