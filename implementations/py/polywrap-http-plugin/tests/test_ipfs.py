from typing import cast
from polywrap_http_plugin import HttpResponse, http_plugin
from polywrap_client import PolywrapClient, PolywrapClientConfig
from polywrap_core import Uri, IUriResolver, InvokerOptions
from polywrap_uri_resolvers import StaticResolver, RecursiveResolver
from polywrap_uri_resolvers.uri_resolver_aggregator import UriResolverAggregator
from polywrap_uri_resolvers.legacy import FsUriResolver, SimpleFileReader
from pathlib import Path


async def test_plugin():
    resolver = RecursiveResolver(
        UriResolverAggregator(
            [
                cast(IUriResolver, FsUriResolver(file_reader=SimpleFileReader())),
                cast(IUriResolver, StaticResolver({Uri("wrap://ens/wraps.eth:http@1.1.0"): http_plugin()})),
            ]
        )
    )

    config = PolywrapClientConfig(resolver=resolver)
    client = PolywrapClient(config)

    ipfs_wrapper_path = Path(__file__).parent.joinpath("ipfs-wrapper")
    ipfs_wrapper_uri = Uri(f"fs/{ipfs_wrapper_path}")

    result = await client.invoke(
        InvokerOptions(
            uri=ipfs_wrapper_uri,
            method="cat",
            args={
                "cid": "QmZ4d7KWCtH3xfWFwcdRXEkjZJdYNwonrCwUckGF1gRAH9",
                "ipfsProvider": "https://ipfs.io",
            },
        )
    )

    assert result.is_err() == False
    response = cast(HttpResponse, result.unwrap())
    assert response["status"] == 200
    assert response["body"] is not None
    assert response["body"].startswith(b"<svg")
