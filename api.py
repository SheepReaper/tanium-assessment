from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

from returns.pipeline import flow
from returns.pointfree import alt

from jph import JPHClient

if TYPE_CHECKING:
    from typing import Callable, Optional

    from requests.models import Response
    from returns.result import Result

    from jph import Post


class Api:
    """This "Application's" API (intentionally minimal to satisfy requirements)"""

    def __init__(self, client: Optional[JPHClient] = None):
        # NOTE: This is here so we can inject a mock client
        self._client = client or JPHClient()

    def _gen_flow(
        self, func: Callable[[], Result[Response, Exception]]
    ) -> Result[Response, Exception]:
        """Generate a new returns flow with a default handler for client errors

        Args:
            func (Callable[[], Result[Response, Exception]]): An action that returns a returns container

        Returns:
            Result[Response, Exception]: Represents either a Success or an Exception
        """
        handle_error: Callable[[Exception], None] = lambda error: print(
            [
                "The JPH client threw an error, check the exception to see what went wrong",
                error,
            ]
        )

        return flow(func(), alt(handle_error))

    def createPostRequest(self, new_post: Post) -> Response:
        """Creates a post and returns a Response unless the client fails

        Args:
            new_post (Post): A new Post to create

        Returns:
            Response: A regular requests.Response object
        """
        return self._gen_flow(lambda: self._client.post("posts", new_post)).unwrap()

    def deletePostRequest(self, post_id: int) -> Response:
        """Deletes a post and returns a Response unless the client fails

        Args:
            post_id (int): The identifier of the Post you wish to delete

        Returns:
            Response: A regular requests.Response object
        """
        return self._gen_flow(lambda: self._client.delete("posts", post_id)).unwrap()

    def getPost(self, id: int) -> Post:
        """Gets a single Post, provided that it exists. Returns the actual Entity and not a Response

        Args:
            id (int): The identifier of the Post you would like

        Returns:
            Post: The actual Post
        """
        return (
            self._gen_flow(lambda: self._client.get("posts", id))
            .unwrap()
            .json(object_hook=lambda data: SimpleNamespace(**data))
        )
