use http_plugin_rs::HttpPlugin;
use polywrap_client::client::PolywrapClient;
use polywrap_core::{
    client::ClientConfig,
    resolvers::static_resolver::{StaticResolver, StaticResolverLike},
    uri::Uri,
};
use polywrap_plugin::{package::PluginPackage};
use std::{sync::Arc};


mod get;
mod post;

pub fn get_client() -> PolywrapClient {
    let http_plugin = HttpPlugin {};
    let plugin_pkg: PluginPackage = http_plugin.into();
    let package = Arc::new(plugin_pkg);

    let resolver = StaticResolver::from(vec![StaticResolverLike::Package(
        Uri::try_from("plugin/http").unwrap(),
        package,
    )]);

    PolywrapClient::new(ClientConfig {
        resolver: Arc::new(resolver),
        interfaces: None,
        envs: None,
    })
}
