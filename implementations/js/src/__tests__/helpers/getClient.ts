import {
  RecursiveResolver,
  PackageToWrapperCacheResolver,
  WrapperCache,
  StaticResolver,
} from "@polywrap/uri-resolvers-js";
import {defaultPackages, defaultInterfaces, PolywrapClient} from "@polywrap/client-js";
import { fileSystemPlugin } from "temp-fs-plugin-js";
import { fileSystemResolverPlugin } from "@polywrap/fs-resolver-plugin-js";
import { ExtendableUriResolver } from "@polywrap/uri-resolver-extensions-js";
import { httpPlugin } from "../..";
import {Uri} from "@polywrap/core-js";

export const pluginUri = "ens/wraps.eth:http@1.1.0";

export const getClient = () => {
  return new PolywrapClient(
    {
      interfaces: [
        {
          interface: ExtendableUriResolver.extInterfaceUri,
          implementations: [Uri.from(defaultPackages.fileSystemResolver)],
        },
      ],
      resolver: RecursiveResolver.from(
        PackageToWrapperCacheResolver.from(
          [
            StaticResolver.from([
              {
                uri: Uri.from(pluginUri),
                package: httpPlugin({}),
              },
              {
                uri: Uri.from(defaultPackages.fileSystemResolver),
                package: fileSystemResolverPlugin({}),
              },
              {
                uri: Uri.from(defaultInterfaces.fileSystem),
                package: fileSystemPlugin({}),
              },
            ]),
            new ExtendableUriResolver(),
          ],
          new WrapperCache()
        )
      ),
    },
    { noDefaults: true }
  );
};
