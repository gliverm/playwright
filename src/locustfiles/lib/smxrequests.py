"""
Module containing requests to SMx API that should not be tracked by Locust.
Basic requests response is returned.
"""
import requests

# Suppress SSL certificate verification errors
requests.packages.urllib3.disable_warnings()


class SmxRequests:
    def __init__(self, base_url, username, password, headers, verify=False, timeout=60):
        self.base_url = base_url
        self.auth = (username, password)
        self.headers = headers
        self.verify = verify
        self.timeout = timeout

    def get_url(self, route: str) -> str:
        """Return api url"""
        return f"{self.base_url}{route}"

    def delete(self, route: str):
        """Delete request"""
        url = self.get_url(route)
        response = requests.delete(
            url=url,
            auth=self.auth,
            headers=self.headers,
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    def delete_config_device_ont(self, device_name, ont_id):
        """Delete config device ONT by ont_id and forced"""

        route = f"/config/device/{device_name}/ont?ont-id={ont_id}&force-delete=true"
        return self.delete(route)

    def delete_config_device_vlan(self, device_name, vlan_id):
        """Delete config device VLAN by vlan_id"""

        route = f"/config/device/{device_name}/vlan/{vlan_id}"
        return self.delete(route)
