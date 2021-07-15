#!/usr/bin/env python3

from datetime import datetime
from json import dumps
from types import SimpleNamespace

from returns.primitives.exceptions import UnwrapFailedError

from api import Api
from jph import Post

api = Api()

try:
    # Print title of post 99
    print(api.getPost(99).title)

    # get post 100
    # add field time
    # print new object as json
    print(
        dumps(
            dict(
                **(api.getPost(100).__dict__),
                time=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            )
        )
    )

    # create new post with:
    # title: "Security Interview Post"
    # UserID: 500
    # Body: "This is an insertion test with a known API"
    response = api.createPostRequest(
        Post(
            title="Security Interview Post",
            userId=500,
            body="This is an insertion test with a known API",
        )
    )

    # create tuple with:
    # id: id from above insertion
    # status code from above post
    # value of "x-Powered-By" header
    new_post = response.json(object_hook=lambda data: SimpleNamespace(**data))
    answer4 = (new_post.id, response.status_code, response.headers["X-Powered-By"])

    # print tuple
    print(answer4)

    # delete the new post
    response = api.deletePostRequest(new_post.id)

    # print status code from delete op
    # print x-content-type-options from response
    print((response.status_code, response.headers["X-Content-Type-Options"]))

except UnwrapFailedError:
    print(
        "One of the requests through 'api' failed to unwrap. This is caused by"
        + "the client failing to reach the endpoint. Check cats have not eaten the"
        + "internet."
    )

except:
    print("I don't know why you're here, or if this is an unhandled edge-case")
