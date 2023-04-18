from pathlib import Path
from polywrap_client import PolywrapClient
from polywrap_core import Uri
from pytest import fixture

from polywrap_client_config_builder.types import ClientConfigBuilder


@fixture
def client(builder: ClientConfigBuilder):
    wrapper_path = Path(__file__).parent.joinpath("wrapper")
    wrapper_uri = Uri.from_str(f"fs/{wrapper_path}")

    config = (
        builder.set_redirect(
            Uri.from_str("wrap://ens/wraps.eth:http@1.1.0"), Uri.from_str("plugin/http")
        )
        .set_redirect(Uri.from_str("wrapper/integration"), wrapper_uri)
        .build()
    )

    return PolywrapClient(config)
