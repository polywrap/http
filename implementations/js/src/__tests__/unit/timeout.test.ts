import { HttpPlugin } from "../..";
import { Http_ResponseTypeEnum, CoreClient } from "../../wrap";

describe("test timeouts", () => {
  const plugin = new HttpPlugin({});

  test("timeout works", async () => {
    const resp = await plugin.get(
      {
        url: 'https://ipfs.io/api/v0/cat',
        request: {
          urlParams: new Map().set(
            'arg',
            'QmaM318ABUXDhc5eZGGbmDxkb2ZgnbLxigm5TyZcCsh1Kw/wrap.info'
          ),
          responseType: Http_ResponseTypeEnum.BINARY,
          timeout: 10
        }
      },
      {} as CoreClient
    ).catch((err) => err);

    expect(resp?.message).toMatch(
      "HTTP Timeout - Exceeded 10ms"
    );
  });
});
