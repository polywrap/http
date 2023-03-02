import json
from typing import cast
from polywrap_http_plugin import http_plugin, HttpResponse
from polywrap_client import PolywrapClient, PolywrapClientConfig
from polywrap_core import Uri, IUriResolver, InvokerOptions
from polywrap_uri_resolvers import StaticResolver, RecursiveResolver
from polywrap_uri_resolvers.uri_resolver_aggregator import UriResolverAggregator
from polywrap_uri_resolvers.legacy import FsUriResolver, SimpleFileReader


async def test_plugin():
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                cast(IUriResolver, FsUriResolver(file_reader=SimpleFileReader())),
                cast(IUriResolver, StaticResolver({Uri("plugin/http"): http_plugin()})),
            ]
        )
    )

    config = PolywrapClientConfig(resolver=resolver)
    client = PolywrapClient(config)
    #     wrapper = wrapper_res.unwrap()
    #     res = await wrapper.invoke(InvokerOptions(uri=Uri("plugin/http"), method="get", args={
    #         "url": "https://httpbin.org/get"
    #     }), client)

    #     print(res)

    #     if res.is_err():
    #         print(res.unwrap_err())
    #         assert 1 == 2
    #     else:
    #         print(res.unwrap())
    #         assert 2 == 3

    result = await client.invoke(
        InvokerOptions(
            uri=Uri("plugin/http"),
            method="get",
            args={"url": "https://httpbin.org/get"},
        )
    )

    assert result.is_err() == False
    response = cast(HttpResponse, result.unwrap())
    assert response["body"] is not None
    assert json.loads(response["body"])["url"] == "https://httpbin.org/get"
