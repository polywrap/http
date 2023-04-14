from polywrap_http_plugin import http_plugin
from polywrap_client import PolywrapClient
from polywrap_core import Uri, InvokerOptions
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader
from polywrap_client_config_builder import PolywrapClientConfigBuilder
from pathlib import Path


async def test_plugin():
    builder = (
        PolywrapClientConfigBuilder()
        .add_resolver(FsUriResolver(file_reader=SimpleFileReader()))
        .set_package(Uri.from_str("wrap://ens/wraps.eth:http@1.1.0"), http_plugin())
    )

    config = builder.build()
    client = PolywrapClient(config)

    ipfs_wrapper_path = Path(__file__).parent.joinpath("ipfs-wrapper")
    ipfs_wrapper_uri = Uri.from_str(f"fs/{ipfs_wrapper_path}")

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
    assert result.startswith(b"<svg")
