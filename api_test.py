from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

import requests
import requests_mock
from pytest import raises
from returns.primitives.exceptions import UnwrapFailedError
from returns.result import Success

from api import Api
from jph import JPHClient, Post

if TYPE_CHECKING:
    from typing import Optional

    from requests.models import Response
    from returns.result import Result


class MockClient(JPHClient):
    """Quick and dirty mock version of the client so we can unit test just the api methods"""

    def __init__(self):
        with requests_mock.Mocker() as m:
            m.register_uri("GET", "http://good", json={"id": 1})
            m.register_uri("GET", "http://bad", status_code=404)
            self.GOOD_RESPONSE = requests.get("http://good")
            self.BAD_RESPONSE = requests.get("http://bad")

    def delete(self, resource: str, resource_id: int) -> Result[Response, Exception]:
        if resource != "posts" or resource_id != 1:
            return Success(self.BAD_RESPONSE)

        return Success(self.GOOD_RESPONSE)

    def get(
        self, resource: str, resource_id: Optional[int]
    ) -> Result[Response, Exception]:
        if resource != "posts" or resource_id != 1:
            return Success(self.BAD_RESPONSE)

        return Success(self.GOOD_RESPONSE)

    def post(self, resource: str, data: Post) -> Result[Response, Exception]:
        if resource != "posts" or data is None:
            raise ValueError

        return Success(self.GOOD_RESPONSE)


def test_create_post_fails_unwrap_on_client_error():
    bad_client = JPHClient("lolbadendpoint")
    api = Api(bad_client)

    with raises(UnwrapFailedError):
        api.createPostRequest(Post())


def test_delete_post_fails_unwrap_on_client_error():
    bad_client = JPHClient("lolbadendpoint")
    api = Api(bad_client)

    with raises(UnwrapFailedError):
        api.deletePostRequest(1)


def test_get_post_fails_unwrap_on_client_error():
    bad_client = JPHClient("lolbadendpoint")
    api = Api(bad_client)

    with raises(UnwrapFailedError):
        api.getPost(1)


def test_create_post_succeeds():
    assert (
        Api(MockClient())
        .createPostRequest(Post())
        .json(object_hook=lambda data: SimpleNamespace(**data))
        .id
        == 1
    )


def test_delete_valid_post_succeeds():
    assert Api(MockClient()).deletePostRequest(1).status_code == 200


def test_delete_invalid_post_fails():
    assert Api(MockClient()).deletePostRequest(-1).status_code == 404


def test_get_post_succeeds():

    assert Api(MockClient()).getPost(1).id == 1
