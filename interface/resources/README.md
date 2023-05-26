# Datetime Wrapper Interface

| Version | URI                                                                                 | WRAP Version |
|---------|-------------------------------------------------------------------------------------|-|
| 2.0.0   | [`wrap://ens/wraps.eth:http@2.0.0`](https://wrappers.io/v/ens/wraps.eth:http@2.0.0) | 0.1 |

## Interface
```graphql
type Response {
    status: Int!
    statusText: String!
    headers: [HTTPHeader!]
    body: String
    httpVersion: HTTPVersion!
    cookies: [Cookie!]
}

type Request {
    headers: [HTTPHeader!]
    urlParams: Map @annotate(type: "Map<String!, String!>")
    responseType: ResponseType!
    body: String
    formData: [FormDataEntry!]
    timeout: Int
    auth: Auth
    mode: CORSMode
    withCredentials: Boolean
    httpVersion: HTTPVersion
    maxRedirects: Int
    proxy: Proxy
    cookies: [Cookie!]
    cache: CachePolicy
}

type HTTPHeader {
    key: String!
    value: String!
}

type FormDataEntry {
    name: String!
    value: String
    fileName: String
    type: String
}

type Auth {
    basicAuth: BasicAuth
    digestAuth: DigestAuth
    bearerToken: BearerToken
    oauth: OAuth
}

type BasicAuth {
    username: String!
    password: String!
}

type DigestAuth {
    username: String!
    password: String!
    realm: String
    nonce: String
    uri: String
    response: String
    opaque: String
}

type BearerToken {
    token: String!
}

type OAuth {
    consumerKey: String!
    consumerSecret: String!
    accessToken: String!
    tokenSecret: String!
}

type Proxy {
    host: String!
    port: Int!
    auth: BasicAuth
}

type Cookie {
    name: String!
    value: String!
    domain: String
    path: String
    expires: Int
    secure: Boolean
    httpOnly: Boolean
    sameSite: CookieSameSitePolicy
}

enum CookieSameSitePolicy {
    STRICT
    LAX
    NONE
}

enum CORSMode {
    CORS
    NO_CORS
    SAME_ORIGIN
}

enum ResponseType {
    TEXT
    BINARY
}

enum HTTPMethod {
    GET
    POST
    PUT
    DELETE
    HEAD
    PATCH
    OPTIONS
}

enum HTTPVersion {
    HTTP1_1
    HTTP2
    HTTP3
}

enum CachePolicy {
    NO_CACHE
    RELOAD
    NO_STORE
    FORCE_CACHE
    ONLY_IF_CACHED
}

type Module {
    request(url: String!, method: HTTPMethod!, request: Request): Response
    get(url: String!, request: Request): Response
    post(url: String!, request: Request): Response
    put(url: String!, request: Request): Response
    delete(url: String!, request: Request): Response
    head(url: String!, request: Request): Response
    patch(url: String!, request: Request): Response
    options(url: String!, request: Request): Response
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