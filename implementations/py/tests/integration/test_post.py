from base64 import b64decode
import json
from polywrap_http_plugin import Response
from polywrap_client import PolywrapClient
from polywrap_core import Uri


def test_simple_post(client: PolywrapClient):
    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="post",
        args={
            "url": "https://jsonplaceholder.typicode.com/todos",
            "request": {
                "responseType": 0,
                "body": json.dumps(
                    {
                        "title": "foo",
                        "body": "bar",
                        "userId": 1,
                    }
                ),
            },
        },
    )

    assert response["status"] == 201
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 201


def test_binary_post(client: PolywrapClient):
    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="post",
        args={
            "url": "https://jsonplaceholder.typicode.com/todos",
            "request": {
                "responseType": 1,
                "body": json.dumps(
                    {
                        "title": "foo",
                        "body": "bar",
                        "userId": 1,
                    }
                ),
            },
        },
    )

    assert response["status"] == 201
    assert response["body"] is not None
    assert json.loads(b64decode(response["body"]).decode("utf-8"))["id"] == 201