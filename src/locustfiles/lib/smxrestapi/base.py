"""
Module containing requests to SMx API that should not be tracked by Locust.
Basic requests response is returned.
"""
import requests
import json

# Suppress SSL certificate verification errors
requests.packages.urllib3.disable_warnings()


class SmxRequest:
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

    def get(self, route: str, params: dict = {}):
        """Get request"""
        url = self.get_url(route)
        response = requests.get(
            url=url,
            auth=self.auth,
            headers=self.headers,
            params=params,
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    def post(self, route: str, params: dict = {}):
        """HTTP POST function to mainly used to create.
        Consider data as json to be dump to string or used as-is.
        """
        url = self.get_url(route)
        # Following is in place to diagnose issue with SMx API
        # swagger_body=json.dumps(params)
        response = requests.post(
            url=url,
            auth=self.auth,
            headers=self.headers,
            data=json.dumps(params),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response

    def put(self, route: str, params: dict = {}):
        """HTTP PUT function to mainly used to update."""
        url = self.get_url(route)
        response = requests.put(
            url=url,
            auth=self.auth,
            headers=self.headers,
            data=json.dumps(params),
            verify=self.verify,
            timeout=self.timeout,
        )
        return response
