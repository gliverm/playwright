"""
SMx API calls using the Locust shim layer.
The intention is that these are re-usable for any use-case.
Eventually it may make sense further modularize the API calls
as the class grows.
"""

import locustfiles.lib.smxuserapi.base as Base


def get_ont_serial_number(vendor_id, serial_number):
    """Return ONT serial number"""
    if vendor_id.upper() == "CXNK" and len(serial_number) < 12:
        serial_number = (
            vendor_id
            + ("0" * (12 - len(vendor_id) - len(serial_number)))
            + serial_number
        )
    return serial_number


class SMxFastHTTPUser(Base.SMxFastHTTPUser):
    """Base class for all SMx API calls tuned for customer GTT."""

    # ----- VLAN CRUD ----- #

    def create_config_device_vlan(self, client, device_name: str, configuration: dict):
        """Create a VLAN"""
        route = f"/config/device/{device_name}/vlan"
        return self.client_post(client, route, data=configuration)

    def read_config_device_vlan(self, client, device_name: str, vlan_id: int):
        """ "Read VLAN"""
        route = f"/config/device/{device_name}/vlan/{vlan_id}"
        if self.group_requests:
            group_name = f"/config/device/{device_name}/vlan/[vlan_id]"
        else:
            group_name = None
        return self.client_get(client, route, group_name=group_name)

    def update_config_device_vlan(
        self,
        client,
        device_name: str,
        configuration: dict,
    ):
        """Update VLAN.
        Note that this is a PUT vs a PATCH requiring all fields
        including the modified field.
        """
        route = f"/config/device/{device_name}/vlan"
        return self.client_put(client, route, data=configuration)

    def delete_config_device_vlan(self, client, device_name: str, vlan_id: int):
        """Delete VLAN"""
        route = f"/config/device/{device_name}/vlan/{vlan_id}"
        if self.group_requests:
            group_name = f"/config/device/{device_name}/vlan/[vlan_id]"
        else:
            group_name = None
        return self.client_delete(client, route, group_name=group_name)

    # ----- Device CRUD ----- #

    def get_config_device_state(self, client, device_name: str):
        """Get OLT state"""
        route = f"/config/device/{device_name}"
        fields = ("state",)
        params = {
            "fields": ",".join(fields),
        }
        return self.client_get(client, route, params)

    # ----- ONT CRUD ----- #

    def create_config_device_ont(
        self, client, device_name: str, vendor_id: str, configuration: dict
    ):
        """Create ont"""
        route = f"/config/device/{device_name}/ont"
        configuration["serial-number"] = get_ont_serial_number(
            vendor_id, configuration["serial-number"]
        )
        return self.client_post(client, route, data=configuration)

    def delete_config_device_ont(
        self, client, device_name: str, ont_id: str, forced_delete="false"
    ):
        """Delete ONT by ont_id"""

        route = f"/config/device/{device_name}/ont?ont-id={ont_id}&force-delete={forced_delete}"
        if self.group_requests:
            group_name = f"/config/device/{device_name}/ont/[ont_id]"
        else:
            group_name = None
        return self.client_delete(client, route, group_name=group_name)

    # ----- Subscriber CRUD ----- #

    def create_ems_subscriber(self, client, configuration: dict):
        """Create a basic subscriber.
        Only the account name and customer ID are required.
        """
        route = f"/ems/subscriber"
        return self.client_post(client, route, data=configuration)

    def delete_ems_subscriber(
        self, client, account_id: str, org_id: str, forced: bool = False
    ):
        """Delete subscriber"""
        forced_str = "true" if forced else "false"
        route = f"/ems/subscriber/org/{org_id}/account/{account_id}?force-delete={forced_str}"
        if self.group_requests:
            group_name = f"/ems/subscriber/org/{org_id}/account/[account_id]"
        else:
            group_name = None
        return self.client_delete(client, route, group_name=group_name)

    # ----- Subscriber Service CRUD ----- #

    def create_ems_service(self, client, configuration: dict):
        """Create a subscriber service"""

        route = "/ems/service"
        return self.client_post(client, route, data=configuration)

    def delete_ems_service(
        self, client, device_name: str, service_name: str, ont_id: str, ont_port_id: str
    ):
        """Delete subscriber service by service name"""
        route = f"/ems/service?device-name={device_name}&ont-id={ont_id}&ont-port-id={ont_port_id}&service-name={service_name}"
        if self.group_requests:
            group_name = f"/ems/service?device-name={device_name}&ont-id=[ont_id]&ont-port-id=[ont_port_id]&service-name=[service]"
        else:
            group_name = None
        return self.client_delete(client, route, group_name=group_name)

    def update_subscriber_service(self, client, configuration: dict):
        """Update a subscriber data service"""
        route = "/ems/service"
        return self.client_put(client, route, configuration)

    def update_ems_service_device_activation(
        self,
        client,
        device_name: str,
        ont_id: str,
        ont_port_id: str,
        vlan_id: str,
        cTag: str,
        action: str,
    ):
        """Update a subscriber service as 'activate' or 'deactivate' using 'pause' or 'resume' action"""
        # TODO string too long, need to refactor
        route = f"/ems/service/device/{device_name}/ont/{ont_id}/port/{ont_port_id}/vlan/{vlan_id}?cTag={cTag}&action={action}"
        return self.client_put(client, route)

    # ----- Added for Cox Fetch Specific ----- #

    def get_config_device_gui_onts(
        self, client, device_name: str, fields: dict = {}, offset=0, limit=20
    ):
        """Get ONT info stored in SMx database"""
        route = f"/config/device/{device_name}/gui/ont"
        params = {
            "fields": ",".join(fields),
            "offset": offset,
            "limit": limit,
        }
        return self.client_get(client, route, params)

    def get_config_device_ont(
        self, client, device_name: str, ont_id: int, fields: dict = {}
    ):
        """Get ONT info from SMx database - not contacting the actual OLT to get ONTs"""
        route = f"/config/device/{device_name}/ont"
        params = {
            "ont-id": ont_id,
            "fields": ",".join(fields),
        }
        return self.client_get(client, route, params)

    def get_config_device_ontport(
        self, client, device_name: str, ont_id: int, fields: dict = {}
    ):
        """Get ONT port info
        Undiscoverd ONT returns more info than in query string - not sure if correct
        """
        route = f"/config/device/{device_name}/ontport"
        params = {
            "ont-id": ont_id,
            "fields": ",".join(fields),
        }
        return self.client_get(client, route, params)

    def get_performance_device_ont(
        self,
        client,
        device_name: str,
        ont_id: int,
        refresh: bool = True,
        fields: dict = {},
    ):
        """Get real time status for an ONT"""
        route = f"/performance/device/{device_name}/ont/{ont_id}/status"
        params = {
            "refresh": refresh,
            "fields": ",".join(fields),
        }
        if self.group_requests:
            group_name = f"/performance/device/{device_name}/ont/[ont_id]/status"
        else:
            group_name = None
        return self.client_get(client, route, params, group_name=group_name)

    def get_ems_service_ont(
        self, client, device_name: str, ont_id: int, fields: dict = {}
    ):
        """Get ONT service info"""
        route = f"/ems/service"
        params = {
            "device-name": device_name,
            "ont-id": ont_id,
            "fields": ",".join(fields),
        }
        return self.client_get(client, route, params)
