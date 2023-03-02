from pathlib import Path
from typing import List, Optional, Dict, TypedDict, cast
from enum import Enum
import json

from httpx import AsyncClient, Response
from polywrap_plugin import PluginModule, PluginPackage
from polywrap_core import Invoker
from polywrap_result import Ok, Result
from polywrap_manifest import WrapManifest


class HttpResponseType(Enum):
    TEXT = "TEXT"
    BINARY = "BINARY"


class FormDataEntry(TypedDict):
    name: str
    value: Optional[str]
    fileName: Optional[str]
    type: Optional[str]


class HttpRequest(TypedDict):
    headers: Optional[Dict[str, str]]
    urlParams: Optional[Dict[str, str]]
    responseType: HttpResponseType
    body: Optional[str]
    formData: Optional[List[FormDataEntry]]
    timeout: Optional[int]

class HttpResponse(TypedDict):
    status: int
    statusText: str
    headers: Optional[Dict[str, str]]
    body: Optional[str]


class ArgsGet(TypedDict):
    url: str
    request: Optional[HttpRequest]


class ArgsPost(TypedDict):
    url: str
    request: Optional[HttpRequest]


class HttpPlugin(PluginModule[None, HttpResponse]):
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

        return Ok(
            HttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=dict(res.headers),
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

        return Ok(
            HttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=dict(res.headers),
                body=res.text,
            )
        )


def http_plugin():
    manifest_path = Path(__file__).parent.joinpath("manifest.json")
    with open(manifest_path, "r") as f:
        json_manifest = json.load(f)
        manifest = WrapManifest(**json_manifest)
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
