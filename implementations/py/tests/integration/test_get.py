from base64 import b64decode
import json

from polywrap_http_plugin import HttpHttpResponse
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions


async def test_simple_get(client: PolywrapClient):
    response: HttpHttpResponse = await client.invoke(
        InvokerOptions(
            uri=Uri.from_str("wrapper/integration"),
            method="get",
            args={"url": "https://jsonplaceholder.typicode.com/todos/1"},
        )
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(response["body"])["id"] == 1


async def test_params_get(client: PolywrapClient):
    response: HttpHttpResponse = await client.invoke(
        InvokerOptions(
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
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert len(json.loads(response["body"])) == 1


async def test_binary_get(client: PolywrapClient):
    response: HttpHttpResponse = await client.invoke(
        InvokerOptions(
            uri=Uri.from_str("wrapper/integration"),
            method="get",
            args={
                "url": "https://jsonplaceholder.typicode.com/todos/1",
                "request": {
                    "responseType": 1,
                },
            },
        )
    )

    assert response["status"] == 200
    assert response["body"] is not None
    assert json.loads(b64decode(response["body"]).decode("utf-8"))["id"] == 1
