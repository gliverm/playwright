"""
Base class for all SMx API calls to be the parent of all
customer client classes.
"""
import json
from locust.contrib.fasthttp import FastResponse
from locustfiles.lib.base_logger import getlogger

LOGGER = getlogger(__name__)


class SMxFastHTTPUser:
    """Base class for all SMx API calls."""

    def __init__(
        self,
        rooturl,
        username,
        password,
        port=443,
        group_requests=True,
        log_error_response=False,
    ):
        """
        Initialize the SMx API session.
        """
        self.rooturl = rooturl
        self.auth = (username, password)
        self.port = port
        self.group_requests = group_requests
        self.log_error_response = log_error_response

    def get_url(self, route: str) -> str:
        """Return api url"""
        return f"{self.rooturl}{route}"

    def log_tracked_error_response(self, response):
        """Log responses not in the 200 range"""
        if self.log_error_response and not (200 <= response.status_code <= 299):
            LOGGER.error(
                f"Tracked failed response: {response.request.method} {response.url} {response.status_code} {response.text}"
            )

    def client_get(
        self,
        client,
        route: str,
        params: dict = {},
        ignore_status: list = [],
        group_name: str = None,
    ) -> FastResponse:
        """Perform client get request"""
        url = self.get_url(route)
        if group_name is not None:
            group_name = self.get_url(group_name)
        with client.get(
            url,
            name=group_name,
            auth=self.auth,
            params=params,
            catch_response=True,
        ) as response:
            if response.status_code in ignore_status:
                response.success()
            else:
                self.log_tracked_error_response(response)
            return response

    def client_post(
        self,
        client,
        route: str,
        data: dict = {},
        ignore_status: list = [],
        group_name: str = None,
    ) -> FastResponse:
        """Perform client post request"""
        url = self.get_url(route)
        if group_name is not None:
            group_name = self.get_url(group_name)
        payload = json.dumps(data)
        with client.post(
            url,
            name=group_name,
            auth=self.auth,
            data=payload,
            catch_response=True,
        ) as response:
            if response.status_code in ignore_status:
                response.success()
            else:
                self.log_tracked_error_response(response)
            return response

    def client_put(
        self,
        client,
        route: str,
        data: dict = {},
        ignore_status: list = [],
        group_name: str = None,
    ) -> FastResponse:
        """Perform client put request"""
        url = self.get_url(route)
        if group_name is not None:
            group_name = self.get_url(group_name)
        payload = json.dumps(data)
        with client.put(
            url,
            name=group_name,
            auth=self.auth,
            data=payload,
            catch_response=True,
        ) as response:
            if response.status_code in ignore_status:
                response.success()
            else:
                self.log_tracked_error_response(response)
            return response

    def client_delete(
        self,
        client,
        route: str,
        ignore_status: list = [],
        group_name: str = None,
    ) -> FastResponse:
        """Perform client delete request"""
        url = self.get_url(route)
        if group_name is not None:
            group_name = self.get_url(group_name)
        with client.delete(
            url,
            name=group_name,
            auth=self.auth,
            catch_response=True,
        ) as response:
            if response.status_code in ignore_status:
                response.success()
            else:
                self.log_tracked_error_response(response)
            return response
