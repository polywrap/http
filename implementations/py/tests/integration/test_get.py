from base64 import b64decode
import json

from polywrap_http_plugin import Response
from polywrap_client import PolywrapClient
from polywrap_core import Uri


def test_simple_get(client: PolywrapClient):
    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={"url": "https://jsonplaceholder.typicode.com/todos/1"},
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 1


def test_params_get(client: PolywrapClient):
    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={
            "url": "https://jsonplaceholder.typicode.com/todos",
            "request": {
                "urlParams": {
                    "id": "1",
                },
                "responseType": 0,
            },
        },
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert len(json.loads(response["body"])) == 1


def test_binary_get(client: PolywrapClient):
    response: Response = client.invoke(
        uri=Uri.from_str("wrapper/integration"),
        method="get",
        args={
            "url": "https://jsonplaceholder.typicode.com/todos/1",
            "request": {
                "responseType": 1,
            },
        },
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(b64decode(response["body"]).decode("utf-8"))["id"] == 1
