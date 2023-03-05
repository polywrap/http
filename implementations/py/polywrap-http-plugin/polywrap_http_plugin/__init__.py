import base64
from pathlib import Path
from typing import List, Optional, TypedDict, Union, cast
from enum import Enum
import json

from httpx import AsyncClient, Response
from polywrap_plugin import PluginModule, PluginPackage
from polywrap_core import Invoker
from polywrap_result import Ok, Result
from polywrap_manifest import WrapManifest
from polywrap_msgpack.generic_map import GenericMap


class HttpResponseType(Enum):
    TEXT = "TEXT"
    BINARY = "BINARY"


class FormDataEntry(TypedDict):
    name: str
    value: Optional[str]
    fileName: Optional[str]
    type: Optional[str]


class HttpRequest(TypedDict):
    headers: Optional[GenericMap[str, str]]
    urlParams: Optional[GenericMap[str, str]]
    responseType: Union[HttpResponseType, str, int]
    body: Optional[str]
    formData: Optional[List[FormDataEntry]]
    timeout: Optional[int]

class HttpResponse(TypedDict):
    status: int
    statusText: str
    headers: Optional[GenericMap[str, str]]
    body: Optional[str]


class ArgsGet(TypedDict):
    url: str
    request: Optional[HttpRequest]


class ArgsPost(TypedDict):
    url: str
    request: Optional[HttpRequest]


def isResponseBinary(args: ArgsGet) -> bool:
    if args.get("request") is None:
        return False
    if not args["request"]:
        return False
    if isinstance(args["request"]["responseType"], int) and args["request"]["responseType"] == 1:
        return True
    if isinstance(args["request"]["responseType"], str) and args["request"]["responseType"] == "BINARY":
        return True
    return args["request"]["responseType"] == HttpResponseType.BINARY


class HttpPlugin(PluginModule[None]):
    def __init__(self):
        super().__init__(None)
        self.client = AsyncClient()

    async def get(self, args: ArgsGet, invoker: Invoker) -> Result[HttpResponse]:
        res: Response
        if args.get("request") is None:
            res = await self.client.get(args["url"])
        elif args["request"] is not None:
            res = await self.client.get(
                args["url"],
                params=args["request"]["urlParams"],
                headers=args["request"]["headers"],
                timeout=cast(float, args["request"]["timeout"]),
            )
        else:
            res = await self.client.get(args["url"])

        if isResponseBinary(args):
            return Ok(
                HttpResponse(
                    status=res.status_code,
                    statusText=res.reason_phrase,
                    headers=GenericMap(dict(res.headers)),
                    body=base64.b64encode(res.content).decode(),
                )
            )

        return Ok(
            HttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=res.text,
            )
        )

    async def post(self, args: ArgsPost, invoker: Invoker) -> Result[HttpResponse]:
        res: Response
        if args.get("request") is None:
            res = await self.client.post(args["url"])
        elif args["request"] is not None:
            content = (
                args["request"]["body"].encode()
                if args["request"]["body"] is not None
                else None
            )
            res = await self.client.post(
                args["url"],
                content=content,
                params=args["request"]["urlParams"],
                headers=args["request"]["headers"],
                timeout=cast(float, args["request"]["timeout"]),
            )
        else:
            res = await self.client.post(args["url"])

        if args["request"] is not None and args["request"]["responseType"] == HttpResponseType.BINARY:
            return Ok(
                HttpResponse(
                    status=res.status_code,
                    statusText=res.reason_phrase,
                    headers=GenericMap(dict(res.headers)),
                    body=base64.b64encode(res.content).decode(),
                )
            )

        return Ok(
            HttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=res.text,
            )
        )


def http_plugin():
    manifest_path = Path(__file__).parent.joinpath("manifest.json")
    with open(manifest_path, "r") as f:
        json_manifest = json.load(f)
        manifest = WrapManifest(**json_manifest)
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
