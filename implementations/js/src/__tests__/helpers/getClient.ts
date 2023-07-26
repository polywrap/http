import { httpPlugin } from "../..";

import {
  PolywrapClient,
  PolywrapClientConfigBuilder
} from "@polywrap/client-js";

export const pluginUri = "wrapscan.io/polywrap/http@1.0";

export const getClient = () => {
  const config = new PolywrapClientConfigBuilder()
    .addDefaults()
    .setPackage(
      pluginUri,
      httpPlugin({ })
    ).build();
  return new PolywrapClient(config);
};
