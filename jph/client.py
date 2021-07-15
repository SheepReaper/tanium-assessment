from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import urljoin

from requests import delete, get, post
from returns.pipeline import flow
from returns.result import safe

from .types import JPHRequestOptions

if TYPE_CHECKING:
    from typing import Dict, Optional

    from requests.models import Response
    from returns.result import Result

    from model import JPHType


class JPHClient:
    """Mostly generic python client to access JSONPlaceholder API on typicode.com
    We're using returns lib: https://github.com/dry-python/returns to catch all the little
    reasons that web requests might fail and robustly return wrapped objects (Success/Exception)
    Keep in mind that everything returned is wrapped"""

    DEFAULT_ENDPOINT = "https://jsonplaceholder.typicode.com/"
    DEFAULT_HEADERS: Dict[str, str] = {}

    _handlers = {"DELETE": delete, "GET": get, "POST": post}

    def __init__(
        self, endpoint: Optional[str] = None, headers: Optional[Dict[str, str]] = None
    ):
        # NOTE: This is here to inject bad values to misconfigure the client

        self._endpoint = endpoint or self.DEFAULT_ENDPOINT
        self._headers = headers or self.DEFAULT_HEADERS

    @safe
    def _make_request(self, options: JPHRequestOptions) -> Response:
        """Dynamically selects the request handler and wraps it in a returns container for ease of use

        Args:
            options (JPHRequestOptions): Options bag to generate the request with

        Returns:
            Response: A regular requests.Response
        """

        with_or_without = (
            f"{options.resource}/{options.resource_id}"
            if options.resource_id
            else options.resource
        )

        response = self._handlers[options.method](
            urljoin(self._endpoint, with_or_without),
            data=(vars(options.data) if options.data else None),
        )

        response.raise_for_status()

        return response

    def _gen_flow(
        self,
        method: str,
        resource: str,
        resource_id: Optional[int] = None,
        data: Optional[JPHType] = None,
    ) -> Result[Response, Exception]:
        """Generate a flow with the options provided

        Args:
            method (str): HTTP method as string
            resource (str): Desired resource on the API
            resource_id (Optional[int], optional): Optional resource identifier to locate. Defaults to None.
            data (Optional[JPHType], optional): Optional data object. For like POST requests. Defaults to None.

        Returns:
            Result[Response, Exception]: Represents either a Response if Success or an Exception if Failure
        """

        return flow(
            JPHRequestOptions(
                method=method, resource=resource, resource_id=resource_id, data=data
            ),
            self._make_request,
        )

    def delete(self, resource: str, resource_id: int) -> Result[Response, Exception]:
        """Send an HTTP DELETE request via the client and wrap the Response in a Result

        Args:
            resource (str): The desired resource
            resource_id (int): The identifier of the resource to delete

        Returns:
            Result[Response, Exception]: Represents either a Response if Success or an Exception if Failure
        """

        return self._gen_flow("DELETE", resource, resource_id)

    def get(
        self, resource: str, resource_id: Optional[int] = None
    ) -> Result[Response, Exception]:
        """Send an HTTP GET request via the client and wrap the Response in a Result

        Args:
            resource (str): The desired resource
            resource_id (Optional[int], optional): Optional identifier of a specific Entity to locate. Defaults to None.

        Returns:
            Result[Response, Exception]: Represents either a Response if Success or an Exception if Failure
        """

        return self._gen_flow("GET", resource, resource_id)

    def post(self, resource: str, data: JPHType) -> Result[Response, Exception]:
        """Send an HTTP POST request via the client and wrap the Response in a Result

        Args:
            resource (str): The desired resource
            data (JPHType): The payload object to post to the API

        Returns:
            Result[Response, Exception]: Represents either a Response if Success or an Exception if Failure
        """

        return self._gen_flow("POST", resource, data=data)
