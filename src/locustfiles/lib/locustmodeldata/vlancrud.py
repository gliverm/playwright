"""
Data models for VLAN Crud User

Modularize the locustfile to allow for re-use of common code and data models.
"""

from typing import Optional, List
from collections import OrderedDict
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    PositiveInt,
    conlist,
)


class BaseConfigModel(BaseModel):
    """Base configuration for common data model configuration"""

    # ----- Model config attributes
    model_config = ConfigDict(extra="ignore")


class VlanRangeModel(BaseConfigModel):
    """Class to validate VLAN range"""

    range: conlist(PositiveInt, min_length=2, max_length=3)

    @field_validator("range")
    @classmethod
    def range_processed(cls, value):
        """Validate range for start < stop"""
        if value[0] > value[1]:
            raise ValueError(f"VLAN range {range} invalid.  Start > Stop.")
        return value


class CrudDataModel(BaseConfigModel):
    """VLAN Data for VLAN Crud User"""

    vlan_ids: list[VlanRangeModel | list[PositiveInt] | PositiveInt]

    @field_validator("vlan_ids")
    @classmethod
    def vlan_ids_processed(cls, value):
        """Post process vlan_ids into a list and ensure list of unique VLAN IDs
        Order is kept intact from the order of the input data
        """
        if type(value) == int:
            return [value]
        else:
            vlan_ids_list = []
            for vlan in value:
                if type(vlan) == int:
                    vlan_ids_list.append(vlan)
                elif type(vlan) == list:
                    vlan_ids_list.extend(vlan)
                elif type(vlan) == VlanRangeModel:
                    vlan_ids_list.extend(range(*vlan.range))
            return list(OrderedDict.fromkeys(vlan_ids_list))  # ensure no duplicates


class DataModel(BaseConfigModel):
    """VLAN CRUD data model base class"""

    vlan_crud_data: Optional[CrudDataModel] = None


# --------------------


def validate_test_data(params) -> dict:
    """Validate test data for L3 1:1 Service Crud User.
    Ignore all other params.
    """
    validated_params = DataModel(**params).vlan_crud_data
    return validated_params
