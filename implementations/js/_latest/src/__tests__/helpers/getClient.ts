import { httpPlugin } from "../..";

import {
  PolywrapClient,
  ClientConfigBuilder
} from "@polywrap/client-js";

export const pluginUri = "ens/wraps.eth:http@1.1.0";

export const getClient = () => {
  const config = new ClientConfigBuilder()
    .addDefaults()
    .addPackage(
      pluginUri,
      httpPlugin({ })
    ).build();
  return new PolywrapClient(config);
};
