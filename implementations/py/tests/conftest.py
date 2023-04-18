from typing import Any
from pytest import fixture
from pytest_mock import MockerFixture

from polywrap_http_plugin import http_plugin
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from polywrap_uri_resolvers import FsUriResolver, SimpleFileReader
from polywrap_client_config_builder import PolywrapClientConfigBuilder


@fixture
def builder():
    return PolywrapClientConfigBuilder().add_resolver(
        FsUriResolver(file_reader=SimpleFileReader())
    ).set_package(
        Uri.from_str("plugin/http"), http_plugin()
    )


@fixture
def client(builder: PolywrapClientConfigBuilder):
    config = builder.build()
    return PolywrapClient(config)
