"""This package contains the HTTP plugin."""
import base64
from io import BytesIO, StringIO
from typing import Dict, List, Optional, cast

from httpx import Client
from httpx._types import RequestFiles
from httpx import Response as HttpxResponse
from polywrap_core import InvokerClient, UriPackageOrWrapper
from polywrap_msgpack import GenericMap
from polywrap_plugin import PluginPackage

from .wrap import ArgsGet, ArgsPost, Module, Response, ResponseType, manifest, FormDataEntry


def _is_response_binary(args: ArgsGet) -> bool:
    if args.get("request") is None:
        return False
    if not args["request"]:
        return False
    if not args["request"].get("responseType"):
        return False
    if args["request"]["responseType"] == 1:
        return True
    if args["request"]["responseType"] == "BINARY":
        return True
    return args["request"]["responseType"] == ResponseType.BINARY


class HttpPlugin(Module[None]):
    """HTTP plugin."""

    def __init__(self):
        """Initialize the HTTP plugin."""
        super().__init__(None)
        self.client = Client()

    async def get(
        self, args: ArgsGet, client: InvokerClient[UriPackageOrWrapper], env: None
    ) -> Optional[Response]:
        """Make a GET request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = self.client.get(args["url"])
        elif args["request"] is not None:
            res = self.client.get(
                args["url"],
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
            )
        else:
            res = self.client.get(args["url"])

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )

    async def post(
        self, args: ArgsPost, client: InvokerClient[UriPackageOrWrapper], env: None
    ) -> Optional[Response]:
        """Make a POST request to the given URL."""
        res: HttpxResponse
        if args.get("request") is None:
            res = self.client.post(args["url"])
        elif args["request"] is not None:
            content = (
                args["request"]["body"].encode()
                if args["request"]["body"] is not None
                else None
            )

            files = self._get_files_from_form_data(args["request"].get("formData") or [])

            res = self.client.post(
                args["url"],
                content=content,
                files=files,
                params=args["request"].get("urlParams"),
                headers=args["request"].get("headers"),
                timeout=cast(float, args["request"].get("timeout")),
            )
        else:
            res = self.client.post(args["url"])

        if _is_response_binary(args):
            return Response(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return Response(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )
    
    def _get_files_from_form_data(self, form_data: List[FormDataEntry]) -> RequestFiles:
        files: RequestFiles = {}
        for entry in form_data:
            file_content = cast(str, entry["value"]) if entry.get("value") else ""
            if entry.get("type"):
                file_content = (
                    base64.b64decode(cast(str, entry["value"]).encode())
                    if entry.get("value")
                    else bytes()
                )
            files[entry["name"]] = file_content
        return files


def http_plugin():
    """Factory function for the HTTP plugin."""
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
