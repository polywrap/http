import json
from typing import cast
from polywrap_http_plugin import http_plugin, HttpHttpResponse
from polywrap_client import PolywrapClient
from polywrap_core import Uri, UriResolver, InvokerOptions, ClientConfig
from polywrap_uri_resolvers import StaticResolver, RecursiveResolver
from polywrap_uri_resolvers import UriResolverAggregator
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader


async def test_plugin():
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                cast(UriResolver, FsUriResolver(file_reader=SimpleFileReader())),
                cast(UriResolver, StaticResolver({Uri.from_str("plugin/http"): http_plugin()})),
            ]
        )
    )

    config = ClientConfig(resolver=resolver)
    client = PolywrapClient(config)
    response: HttpHttpResponse = await client.invoke(
        InvokerOptions(
            uri=Uri.from_str("plugin/http"),
            method="get",
            args={"url": "https://httpbin.org/get"},
        )
    )
    assert response["body"] is not None
    assert json.loads(response["body"])["url"] == "https://httpbin.org/get"
