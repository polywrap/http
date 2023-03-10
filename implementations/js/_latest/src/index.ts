import {
  CoreClient,
  Module,
  Args_get,
  Args_post,
  Http_Response,
  manifest,
} from "./wrap";
import { toKyOptions, fromKyResponse } from "./util";

import { PluginFactory, PluginPackage } from "@polywrap/plugin-js";
import ky from "ky-universal";

type NoConfig = Record<string, never>;

export class HttpPlugin extends Module<NoConfig> {
  public async get(
    args: Args_get,
    _client: CoreClient
  ): Promise<Http_Response | null> {
    const { options, responseType } = toKyOptions(
      args.request || { responseType: "TEXT" }
    );

    const response = await ky.get(
      args.url,
      options
    );

    return fromKyResponse(response, responseType);
  }

  public async post(
    args: Args_post,
    _client: CoreClient
  ): Promise<Http_Response | null> {
    const { options, responseType } = toKyOptions(
      args.request || { responseType: "TEXT" }
    );

    const response = await ky.post(
      args.url,
      options
    );

    return fromKyResponse(response, responseType);
  }
}

export const httpPlugin: PluginFactory<NoConfig> = () =>
  new PluginPackage(new HttpPlugin({}), manifest);

export const plugin = httpPlugin;
