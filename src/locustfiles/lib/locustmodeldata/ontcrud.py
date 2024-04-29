"""
Data models for ONT Crud User

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional, List
from pydantic import (
    BaseModel,
    ConfigDict,
    model_validator,
)


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class ONTDefaultsModel(BaseConfigModel):
    """ONT Defaults Data for ONT Crud User"""

    profile_id: Optional[str] = None
    vendor_id: Optional[str] = None


class ONTConfigModel(BaseConfigModel):
    """ONT Config Data for ONT Crud User"""

    ont_id: str
    serial_number: str
    profile_id: Optional[str] = None
    vendor_id: Optional[str] = None


class OntModel(BaseConfigModel):
    """ "ONT CRUD data model"""

    force_delete: str
    defaults: ONTDefaultsModel
    ont_config: List[ONTConfigModel]

    @model_validator(mode="after")
    def process_ont_configuration(self) -> "OntModel":
        """Post process ont_configuration to ensure list of unique ONT IDs
        Order is kept intact from the order of the input data
        """
        # TODO Logic to remove duplicate ONTs
        ont_id_list = []
        profile_id = self.defaults.profile_id
        vendor_id = self.defaults.vendor_id
        for ont in self.ont_config:
            if ont.ont_id not in ont_id_list:
                if ont.profile_id is None:
                    ont.profile_id = profile_id
                if ont.vendor_id is None:
                    ont.vendor_id = vendor_id
                if ont.profile_id is None or ont.vendor_id is None:
                    raise ValueError(
                        f"ONT {ont.ont_id} is missing ONT profile_id or vendor_id"
                    )
                ont_id_list.append(ont.ont_id)

        return self


class OntsModel(BaseConfigModel):
    """Top level nested Test Data for ONT Crud User"""

    onts: OntModel


class DataModel(BaseConfigModel):
    """VLAN CRUD data model base class"""

    ont_crud_data: Optional[OntsModel] = None


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params).ont_crud_data
    return validated_params
