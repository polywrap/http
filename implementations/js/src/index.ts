import {
  CoreClient,
  Module,
  Args_get,
  Args_post,
  Http_Response,
  manifest,
} from "./wrap";
import { fromAxiosResponse, toAxiosRequestConfig, toFormData } from "./util";

import axios, { AxiosResponse, AxiosRequestConfig  } from "axios";
import { PluginFactory, PluginPackage } from "@polywrap/plugin-js";

type NoConfig = Record<string, never>;

export class HttpPlugin extends Module<NoConfig> {
  public async get(
    args: Args_get,
    _client: CoreClient
  ): Promise<Http_Response | null> {
    const response = await this._execGet<string>(
      args.url,
      toAxiosRequestConfig(args.request || undefined)
    );
    return fromAxiosResponse(response);
  }

  public async post(
    args: Args_post,
    _client: CoreClient
  ): Promise<Http_Response | null> {
    let response: AxiosResponse;
    if (args.request?.body) {
      response = await this._execPost(
        args.url,
        toAxiosRequestConfig(args.request),
        args.request.body
      );
    } else if (args.request?.formData) {
      const data = toFormData(args.request.formData);
      const config = toAxiosRequestConfig(args.request);
      config.headers = {
        ...(config.headers as Record<string, unknown>),
        ...data.getHeaders(),
      };
      response = await this._execPost(args.url, config, data);
    } else if (args.request) {
      response = await this._execPost(args.url, toAxiosRequestConfig(args.request));
    } else {
      response = await this._execPost(args.url, toAxiosRequestConfig(undefined));
    }
    return fromAxiosResponse(response);
  }

  private async _execGet<T = any>(
    url: string,
    config: AxiosRequestConfig
  ): Promise<AxiosResponse> {
    const finalize = this._createFinalizer(url, config);
    return await axios.get<T>(url, config)
      .then((resp) => {
        finalize();
        return resp;
      });
  }

  private async _execPost(
    url: string,
    config: AxiosRequestConfig,
    data?: any
  ): Promise<AxiosResponse> {
    const finalize = this._createFinalizer(url, config);
    return axios.post(url, data, config)
      .then((resp) => {
        finalize();
        return resp;
      });
  }

  private _createFinalizer(
    url: string,
    config?: AxiosRequestConfig
  ): () => void {
    if (!config?.timeout || config.timeout <= 0) {
      return () => {};
    }

    const source = axios.CancelToken.source();
    config.cancelToken = source.token;

    const timeout = setTimeout(
      () => {
        source.cancel(`HTTP Timeout - Exceeded ${config.timeout}ms @ ${url}`);
      },
      config.timeout
    );

    return () => clearTimeout(timeout);
  }
}

export const httpPlugin: PluginFactory<NoConfig> = () =>
  new PluginPackage(new HttpPlugin({}), manifest);

export const plugin = httpPlugin;
