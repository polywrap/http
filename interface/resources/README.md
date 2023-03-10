# HTTP Wrapper Interface

| Version | URI | WRAP Version |
|-|-|-|
| 1.0.0 | [`wrap://ens/wrappers.polywrap.eth:http@1.0.0`](https://wrappers.io/v/ens/wrappers.polywrap.eth:http@1.0.0) | 0.1 |
| 1.1.0 | [`wrap://ens/wrappers.polywrap.eth:http@1.1.0`](https://wrappers.io/v/ens/wrappers.polywrap.eth:http@1.1.0) | 0.1 |

## Interface
```graphql
type Response {
    status: Int!
    statusText: String!
    headers: Map @annotate(type: "Map<String!, String!>")
    body: String
}

type Request {
    headers: Map @annotate(type: "Map<String!, String!>")
    urlParams: Map @annotate(type: "Map<String!, String!>")
    responseType: ResponseType!
    """The body of the request. If present, the `formData` property will be ignored."""
    body: String
    """
    An alternative to the standard request body, 'formData' is expected to be in the 'multipart/form-data' format.
    If present, the `body` property is not null, `formData` will be ignored.
    Otherwise, if formData is not null, the following header will be added to the request: 'Content-Type: multipart/form-data'.
    """
    formData: [FormDataEntry!]
    timeout: UInt32
}

type FormDataEntry {
    """FormData entry key"""
    name: String!
    """If 'type' is defined, value is treated as a base64 byte string"""
    value: String
    """File name to report to the server"""
    fileName: String
    """MIME type (https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types). Defaults to empty string."""
    type: String
}

enum ResponseType {
    TEXT
    BINARY
}

type Module {
    get(url: String!, request: Request): Response
    post(url: String!, request: Request): Response
}
```

## Usage
```graphql
#import { Module } into Http from "ens/wrappers.polywrap.eth:http@1.1.0"

type Module implements Http_Module {}
```

And implement the `get` + `post` methods within your programming language of choice.

## Source Code
[Link](https://github.com/polywrap/http)

## Known Implementations
[Link](https://github.com/polywrap/http/tree/master/implementations)