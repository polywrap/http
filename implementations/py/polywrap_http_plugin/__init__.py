import base64
from typing import Optional, cast

from httpx import AsyncClient, Response as HttpxResponse
from polywrap_plugin import PluginPackage
from polywrap_core import InvokerClient, UriPackageOrWrapper
from polywrap_msgpack import GenericMap

from .wrap import HttpHttpResponse, HttpHttpResponseType, ArgsGet, ArgsPost, manifest, Module


def isResponseBinary(args: ArgsGet) -> bool:
    if args.get("request") is None:
        return False
    if not args["request"]:
        return False
    if args["request"]["responseType"] == 1:
        return True
    if args["request"]["responseType"] == "BINARY":
        return True
    return args["request"]["responseType"] == HttpHttpResponseType.BINARY


class HttpPlugin(Module[None]):
    def __init__(self):
        super().__init__(None)
        self.client = AsyncClient()

    async def get(self, args: ArgsGet, client: InvokerClient[UriPackageOrWrapper], env: None) -> Optional[HttpHttpResponse]:
        res: HttpxResponse
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
            return HttpHttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return HttpHttpResponse(
            status=res.status_code,
            statusText=res.reason_phrase,
            headers=GenericMap(dict(res.headers)),
            body=res.text,
        )

    async def post(self, args: ArgsPost, client: InvokerClient[UriPackageOrWrapper], env: None) -> Optional[HttpHttpResponse]:
        res: HttpxResponse
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

        if args["request"] is not None and args["request"]["responseType"] == HttpHttpResponseType.BINARY:
            return HttpHttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=base64.b64encode(res.content).decode(),
            )

        return HttpHttpResponse(
                status=res.status_code,
                statusText=res.reason_phrase,
                headers=GenericMap(dict(res.headers)),
                body=res.text,
            )


def http_plugin():
    return PluginPackage(module=HttpPlugin(), manifest=manifest)
