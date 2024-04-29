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
    c_vlan: Optional[int] = None
    service_name: Optional[str] = None
    # control_policy_name_1: Optional[str] = None
    # control_policy_name_2: Optional[str] = None
    ont_port_id: Optional[str] = None


class ONTVoiceServiceModel(BaseConfigModel):
    """ONT Voice Service for L3 1:1 Service Crud User"""

    vlan: Optional[int] = None
    c_vlan: Optional[int] = None
    service_name: Optional[str] = None
    # control_policy_name_1: Optional[str] = None
    # control_policy_name_2: Optional[str] = None
    ont_port_id: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    uri: Optional[str] = None


class ONTConfigModel(BaseConfigModel):
    """ONT Config Data for L3 1:1 Service Crud User"""

    ont_id: str
    serial_number: str
    profile_id: Optional[str] = None
    vendor_id: Optional[str] = None
    data_service: Optional[ONTDataServiceModel] | None
    voice_service: Optional[ONTVoiceServiceModel] | None


class ONTDefaultsModel(BaseConfigModel):
    """ONT Defaults Data for L3 1:1 Service Crud User"""

    profile_id: Optional[str] = None
    vendor_id: Optional[str] = None
    data_service: Optional[ONTDataServiceModel] = None
    voice_service: Optional[ONTVoiceServiceModel] = None


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
        # TODO Fail when either profile_id or vendor_id is None after applying defaults
        profile_id = self.defaults.profile_id
        vendor_id = self.defaults.vendor_id
        data_service = self.defaults.data_service
        voice_service = self.defaults.voice_service
        for ont in self.ont_config:
            if ont.profile_id is None:
                ont.profile_id = profile_id
            if ont.vendor_id is None:
                ont.vendor_id = vendor_id
            if ont.data_service is None:
                ont.data_service = data_service
            else:
                if ont.data_service.vlan is None:
                    ont.data_service.vlan = self.defaults.data_service.vlan
                if ont.data_service.service_name is None:
                    ont.data_service.service_name = (
                        self.defaults.data_service.service_name
                    )
                # if ont.data_service.control_policy_name_1 is None:
                #     ont.data_service.control_policy_name_1 = (
                #         self.defaults.data_service.control_policy_name_1
                #     )
                # if ont.data_service.control_policy_name_2 is None:
                #     ont.data_service.control_policy_name_2 = (
                #         self.defaults.data_service.control_policy_name_2
                #     )
                # c_vlan should be unique and problably not set by default
                # if ont.data_service.c_vlan is None:
                #     ont.data_service.c_vlan = self.defaults.data_service.c_vlan
                if ont.data_service.ont_port_id is None:
                    ont.data_service.ont_port_id = (
                        self.defaults.data_service.ont_port_id
                    )
            if ont.voice_service is None:
                ont.voice_service = voice_service
            else:
                if ont.voice_service.vlan is None:
                    ont.voice_service.vlan = self.defaults.voice_service.vlan
                if ont.voice_service.service_name is None:
                    ont.voice_service.service_name = (
                        self.defaults.voice_service.service_name
                    )
                # if ont.voice_service.control_policy_name_1 is None:
                #     ont.voice_service.control_policy_name_1 = (
                #         self.defaults.voice_service.control_policy_name_1
                #     )
                # if ont.voice_service.control_policy_name_2 is None:
                #     ont.voice_service.control_policy_name_2 = (
                #         self.defaults.voice_service.control_policy_name_2
                #     )
                # c_vlan should be unique and problably not set by default
                if ont.voice_service.ont_port_id is None:
                    ont.voice_service.ont_port_id = (
                        self.defaults.voice_service.ont_port_id
                    )
                # user should be unique and problably not set by default
                if ont.voice_service.password is None:
                    ont.voice_service.password = self.defaults.voice_service.password
                # uri should be unique and problably not set by default
        return self


class ONTsModel(BaseConfigModel):
    """Top level nested Test Data for L3 1:1 Service Crud User"""

    onts: ONTModel


class DataModel(BaseConfigModel):
    """Base Test Data for L3 1:1 Service Crud User"""

    l3_one2one_service_data: Optional[ONTsModel] = None


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params).l3_one2one_service_data
    return validated_params
