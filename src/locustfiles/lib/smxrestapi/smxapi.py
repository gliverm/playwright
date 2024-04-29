"""
SMx API calls requests only.
The intention is that these are re-usable for any use-case.
Eventually it may make sense further modularize the API calls
as the class grows.
"""
# TODO Reduce profile create that have commonalities to a single function
# TODO Reduce profile delete that have commonalities to a single function


import locustfiles.lib.smxrestapi.base as Base


class SMxRequests(Base.SmxRequest):
    """GTT Requests class for SMx API
    These requests at this time are fairly generic and can be re-used.
    """

    def delete_config_device_ont(self, device_name, ont_id, forced_delete="false"):
        """Delete config device ONT by ont_id."""

        route = f"/config/device/{device_name}/ont?ont-id={ont_id}&force-delete={forced_delete}"
        return self.delete(route)

    def delete_config_device_vlan(self, device_name, vlan_id):
        """Delete config device VLAN by vlan_id"""

        route = f"/config/device/{device_name}/vlan/{vlan_id}"
        return self.delete(route)

    def get_ont_serial_number(self, vendor_id, serial_number):
        """Return ONT serial number"""
        if vendor_id.upper() == "CXNK" and len(serial_number) < 12:
            serial_number = (
                vendor_id
                + ("0" * (12 - len(vendor_id) - len(serial_number)))
                + serial_number
            )
        return serial_number

    def create_config_device_ont(self, device_name: str, configuration: dict):
        """Create an ONT"""
        route = f"/config/device/{device_name}/ont"

        if (
            "vendor-id" in configuration.keys()
            and "serial-number" in configuration.keys()
        ):
            configuration["serial-number"] = self.get_ont_serial_number(
                configuration["vendor-id"], configuration["serial-number"]
            )

        return self.post(route, params=configuration)

    def create_config_device_vlan(self, device_name: str, configuration: dict):
        """Create a VLAN"""

        route = f"/config/device/{device_name}/vlan"
        return self.post(route, params=configuration)

    def create_ems_profile_dhcp_v4_server_pool(self, configuration: dict):
        """Create a DHCPv4 server pool"""

        route = "/ems/profile/dhcp-v4-server-pool"
        return self.post(route, params=configuration)

    def delete_ems_profile_dhcp_v4_server_pool(self, pool_name: str):
        """Delete a DHCPv4 server pool"""

        route = f"/ems/profile/dhcp-v4-server-pool/{pool_name}"
        return self.delete(route)

    def create_ems_profile_dhcp_v4_server_profile(self, configuration: dict):
        """Create a DHCPv4 server profile"""

        route = "/ems/profile/dhcp-v4-server-profile"
        return self.post(route, params=configuration)

    def delete_ems_profile_dhcp_v4_server_profile(self, dhcp_profile: str):
        """Delete a DHCPv4 server profile"""

        route = f"/ems/profile/dhcp-v4-server-profile/{dhcp_profile}"
        return self.delete(route)

    def create_ems_profile_dhcp_v6_server_pool(self, configuration: dict):
        """Create a DHCPv6 server pool"""

        route = "/ems/profile/dhcp-v6-server-pool"
        return self.post(route, params=configuration)

    def delete_ems_profile_dhcp_v6_server_pool(self, name: str):
        """Delete a DHCPv6 server pool"""

        route = f"/ems/profile/dhcp-v6-server-pool/{name}"
        return self.delete(route)

    def create_ems_profile_dhcp_v6_server_profile(self, configuration: dict):
        """Create a DHCPv6 server profile"""

        route = "/ems/profile/dhcp-v6-server-profile"
        return self.post(route, params=configuration)

    def delete_ems_profile_dhcp_v6_server_profile(self, dhcp_profile: str):
        """Delete a DHCPv6 server profile"""

        route = f"/ems/profile/dhcp-v6-server-profile/{dhcp_profile}"
        return self.delete(route)

    def create_ems_profile_class_map(self, configuration: dict):
        """Create a class-map"""

        route = "/ems/profile/class-map"
        return self.post(route, params=configuration)

    def delete_ems_profile_class_map(self, name: str):
        """Delete a class-map"""

        route = f"/ems/profile/class-map/{name}"
        return self.delete(route)

    def create_ems_profile_policy_map(self, configuration: dict):
        """Create a policy-map"""

        route = "/ems/profile/policy-map"
        return self.post(route, params=configuration)

    def delete_ems_profile_policy_map(self, name: str):
        """Delete a policy-map"""

        route = f"/ems/profile/policy-map/{name}"
        return self.delete(route)

    def create_ems_profile_control_policy(self, configuration: dict):
        """Create a control_policy"""

        route = "/ems/profile/control-policy"
        return self.post(route, params=configuration)

    def delete_ems_profile_control_policy(self, name: str):
        """Delete a control_policy"""

        route = f"/ems/profile/control-policy/{name}"
        return self.delete(route)

    def create_ems_profile_sip_profile(self, configuration: dict):
        """Create a SIP profile"""

        route = "/ems/profile/sip-profile"
        return self.post(route, params=configuration)

    def delete_ems_profile_sip_profile(self, name: str):
        """Delete a SIP profile"""

        route = f"/ems/profile/sip-profile/{name}"
        return self.delete(route)

    def create_config_service_template(self, configuration: dict):
        """Create a service template"""

        route = "/config/service-template"
        return self.post(route, params=configuration)

    def get_config_service_template(self, name: str):
        """Get real time status for an ONT"""

        route = f"/config/service-template/{name}"
        return self.get(route)

    def delete_config_service_template(self, name: str):
        """Delete a service template"""

        route = f"/config/service-template/{name}"
        return self.delete(route)

    def create_config_profile_sync_class_map_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync class map ethernet to device"""

        route = f"/config/profile/sync/class-map/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_class_map_ip_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync class map ip to device"""

        route = f"/config/profile/sync/classMap-ip/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_policy_map_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync policy map to device"""

        route = f"/config/profile/sync/policy-map/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_control_policy_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync policy map to device"""

        route = f"/config/profile/sync/control-policy/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_sip_profile_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync sip profile to device"""

        route = f"/config/profile/sync/sip-profile/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_dhcp_v4_server_pool_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync dhcp v4 server pool to device"""

        route = f"/config/profile/sync/dhcp-v4-server-pool/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_dhcp_v4_server_profile_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync dhcp v4 server profile to device"""

        route = f"/config/profile/sync/dhcp-v4-server-profile/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_dhcp_v6_server_pool_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync dhcp v6 server pool to device"""

        route = f"/config/profile/sync/dhcp-v6-server-pool/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_config_profile_sync_dhcp_v6_server_profile_to_device(
        self, device_name: str, profile_name: str
    ):
        """Create a profile sync dhcp v6 server profile to device"""

        route = f"/config/profile/sync/dhcp-v6-server-profile/{profile_name}"
        configuration = {
            "device-names": [device_name],
        }
        return self.post(route, params=configuration)

    def create_ems_subscriber(self, configuration: dict):
        """Create a subscriber"""

        route = f"/ems/subscriber"
        return self.post(route, params=configuration)

    def delete_ems_subscriber(self, org_id: str, account_name: str):
        """Delete a subscriber"""

        route = f"/ems/subscriber/org/{org_id}/account/{account_name}"
        return self.delete(route)

    def delete_config_device_sip_profile(self, device_name: str, name: str):
        """Delete a sip_profile"""

        route = f"/config/device/{device_name}/sip-profile/{name}"
        return self.delete(route)

    def delete_config_device_control_policy(self, device_name: str, name: str):
        """Delete a control policy"""

        route = f"/config/device/{device_name}/control-policy/{name}"
        return self.delete(route)

    def delete_config_device_policy_map(self, device_name: str, name: str):
        """Delete a policy map"""

        route = f"/config/device/{device_name}/policy-map/{name}"
        return self.delete(route)

    def delete_config_device_class_map(self, device_name: str, name: str):
        """Delete a class map"""

        route = f"/config/device/{device_name}/classMap-ip/{name}"
        return self.delete(route)

    def delete_config_device_dhcp_v6_server_profile(self, device_name: str, name: str):
        """Delete a DHCPv6 server profile"""

        route = f"/config/device/{device_name}/dhcp-v6-server-profile/{name}"
        return self.delete(route)

    def delete_config_device_dhcp_v6_server_pool(self, device_name: str, name: str):
        """Delete a DHCPv6 server pool"""

        route = f"/config/device/{device_name}/dhcp-v6-server-pool/{name}"
        return self.delete(route)

    def delete_config_device_dhcp_v4_server_profile(self, device_name: str, name: str):
        """Delete a DHCPv4 server profile"""

        route = f"/config/device/{device_name}/dhcp-v4-server-profile/{name}"
        return self.delete(route)

    def delete_config_device_dhcp_v4_server_pool(self, device_name: str, name: str):
        """Delete a DHCPv4 server pool"""

        route = f"/config/device/{device_name}/dhcp-v4-server-pool/{name}"
        return self.delete(route)

    def create_ems_service(self, configuration: dict):
        """Create a service"""

        route = "/ems/service"
        return self.post(route, params=configuration)

    def delete_ems_service(
        self, device_name: str, ont_id: str, ont_port_id: str, service_name: str
    ):
        route = f"/ems/service?device-name={device_name}&ont-id={ont_id}&ont-port-id={ont_port_id}&service-name={service_name}"
        return self.delete(route)

    def update_ems_service(self, configuration: dict):
        """Update a service"""

        route = "/ems/service"
        return self.put(route, params=configuration)

    def get_config_device(self, fields: dict, offset=0, limit=2000):
        """Get device info"""
        route = f"/config/device"
        params = {
            "fields": ",".join(fields),
            "offset": offset,
            "limit": limit,
        }
        return self.get(route, params)

    def get_config_device_gui_ont(
        self, device_name: str, fields: dict, offset=0, limit=20
    ):
        """Get ONT info stored in SMx database"""
        route = f"/config/device/{device_name}/gui/ont"
        params = {
            "fields": ",".join(fields),
            "offset": offset,
            "limit": limit,
        }
        return self.get(route, params)
