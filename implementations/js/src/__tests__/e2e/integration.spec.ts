import { Response } from "../../wrap";

import { PolywrapClient } from "@polywrap/client-js";
import { Commands } from "@polywrap/cli-js";
import nock from "nock";
import { getClient } from "../helpers/getClient";

jest.setTimeout(360000);

const defaultReplyHeaders = {
  "access-control-allow-origin": "*",
  "access-control-allow-credentials": "true",
};

describe("e2e tests for HttpPlugin", () => {
  let client: PolywrapClient;

  const wrapperPath = `${__dirname}/integration`;
  const uri = `fs/${wrapperPath}/build`;

  beforeAll(async () => {
    client = getClient();
    await Commands.build({ }, { cwd: wrapperPath });
  });

  it("get", async () => {
    nock("http://www.example.com", {
      reqheaders: { "X-Request-Header": "req-foo" },
    })
      .defaultReplyHeaders(defaultReplyHeaders)
      .get("/api")
      .query({ query: "foo" })
      .reply(200, '{data: "test-response"}', {
        "X-Response-Header": "resp-foo",
      });

    const response = await client.invoke<Response>({
      uri,
      method: "get",
      args: {
        url: "http://www.example.com/api",
        request: {
          responseType: "TEXT",
          urlParams: new Map([["query", "foo"]]),
          headers: new Map([["X-Request-Header", "req-foo"]]),
        },
      },
    });

    if (!response.ok) throw response.error;
    expect(response.value).toBeDefined();
    expect(response.value?.status).toBe(200);
  });

  it("post", async () => {
    nock("http://www.example.com", {
      reqheaders: { "X-Request-Header": "req-foo" },
    })
      .defaultReplyHeaders(defaultReplyHeaders)
      .post("/api", "{data: 'test-request'}")
      .query({ query: "foo" })
      .reply(200, '{data: "test-response"}', {
        "X-Response-Header": "resp-foo",
      });

    const response = await client.invoke<Response>({
      uri,
      method: "post",
      args: {
        url: "http://www.example.com/api",
        request: {
          responseType: "TEXT",
          body: "{data: 'test-request'}",
          urlParams: { query: "foo" },
          headers: new Map([["X-Request-Header", "req-foo"]]),
        },
      },
    });

    if (!response.ok) throw response.error;
    expect(response.value).toBeTruthy();
    expect(response.value?.status).toBe(200);
    expect(response.value?.body).toBeTruthy();
  });
});
