# @polywrap/http-plugin-js

Http plugin currently supports two different methods `GET` and `POST`. Similar to calling axios, when defining request you need to specify a response type. Headers and query parameters may also be defined.

## Response Types

`TEXT` - The server will respond with text, the HTTP plugin will return the text as-is.

`BINARY` - The server will respond with binary data (_ArrayBuffer_), the HTTP plugin will encode as a **base64** string and return it.

## GET request

Below is sample invocation of the `GET` request with custom request headers and query parameters (`urlParams`).

```ts
const result = await client.invoke<Response>({
  uri: "wrapscan.io/polywrap/http@1.0",
  method: "get",
  args: {
    url: "http://www.example.com/api",
    request: {
      responseType: "TEXT",
      urlParams: [{key: "query", value: "foo"}],
      headers: [{key: "X-Request-Header", value: "req-foo"}],
    }
  }
})
```

## POST request

Below is sample invocation of the `POST` request with custom request headers and query parameters (`urlParams`). It is also possible to set request body as shown below.

```ts
const response = await polywrapClient.invoke<Response>({
  uri: "wrapscan.io/polywrap/http@1.0",
  method: "post",
  args: {
    url: "http://www.example.com/api",
    request: {
      responseType: "TEXT",
      urlParams: [{key: "query", value: "foo"}],
      headers: [{key: "X-Request-Header", value: "req-foo"}],
      body: "{data: 'test-request'}",
    }
  }
})
```
