use http_plugin_rs::wrap::types::HttpHttpResponse as HttpResponse;
use http_plugin_rs::HttpPlugin;
use polywrap_client::client::PolywrapClient;
use polywrap_core::resolvers::static_resolver::{StaticResolver, StaticResolverLike};
use polywrap_core::{
    client::ClientConfig, resolvers::uri_resolution_context::UriPackage, uri::Uri,
};
use polywrap_msgpack::msgpack;
use polywrap_plugin::{package::PluginPackage, JSON::{json, from_str}};
use serde::{Deserialize, Serialize};
use std::sync::{Arc, Mutex};

fn get_client() -> PolywrapClient {
    let http_plugin = HttpPlugin {};
    let plugin_pkg: PluginPackage = http_plugin.into();
    let package = Arc::new(Mutex::new(plugin_pkg));

    let resolver = StaticResolver::from(vec![StaticResolverLike::Package(UriPackage {
        uri: Uri::try_from("plugin/http").unwrap(),
        package,
    })]);

    PolywrapClient::new(ClientConfig {
        resolver: Arc::new(resolver),
        interfaces: None,
        envs: None,
    })
}

#[derive(Debug, Serialize, Deserialize)]
struct ExpectedResponse {
    id: u32,
}

#[test]
fn post_method() {
    let body = json!({
        "id": "some",
        "value": 123
    });
    let response = get_client()
        .invoke::<HttpResponse>(
            &Uri::try_from("plugin/http").unwrap(),
            "post",
            Some(&msgpack!({
                "url": "https://jsonplaceholder.typicode.com/todos",
                "request": {
                    "responseType": "TEXT",
                    "body": body.to_string()
                }
            })),
            None,
            None,
        )
        .unwrap();

    assert_eq!(response.status, 201);
    assert_ne!(response.body, None);
    let body: ExpectedResponse = from_str(&response.body.unwrap()).unwrap();
    assert_eq!(body.id, 201);
}
