# Datetime Wrapper Interface

| Version | URI                                                                                 | WRAP Version |
|---------|-------------------------------------------------------------------------------------|-|
| 2.0.0   | [`wrap://ens/wraps.eth:http@2.0.0`](https://wrappers.io/v/ens/wraps.eth:http@2.0.0) | 0.1 |

## Interface
```graphql
type Response {
    status: Int!
    statusText: String!
    headers: Map @annotate(type: "Map<String!, String!>")
    body: String
}

type Request {
    url: String!
    method: HTTPMethod!
    headers: Map @annotate(type: "Map<String!, String!>")
    body: String
    timeout: Int
}

enum HTTPMethod {
    GET
    POST
    PUT
    DELETE
    HEAD
    PATCH
    OPTIONS
    CONNECT
    TRACE
}

type Module {
    request(request: Request): Response
}
```

## Usage
```graphql
#import * from "ens/wraps.eth:http@2.0.0"
```

And implement the interface methods within your programming language of choice.

## Source Code
[Link](https://github.com/polywrap/std/http)

## Known Implementations
[Link](https://github.com/polywrap/http/tree/master/implementations)