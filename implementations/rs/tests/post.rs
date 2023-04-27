use http_plugin_rs::wrap::types::HttpHttpResponse as HttpResponse;
use http_plugin_rs::HttpPlugin;
use polywrap_client::{
    client::PolywrapClient,
    core::{
        client::ClientConfig,
        resolvers::{
            static_resolver::{StaticResolver, StaticResolverLike},
            uri_resolution_context::UriPackage,
        },
        uri::Uri,
    },
    msgpack::msgpack,
    plugin::{
        package::PluginPackage,
        JSON::{from_str, json},
    },
};
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
    value: u32
}

#[test]
fn post_method() {
    let body = json!({
        "value": 5
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
    let expected_response: ExpectedResponse = from_str(&response.body.unwrap()).unwrap();
    assert_eq!(expected_response.id, 201);
    assert_eq!(expected_response.value, 5);
}
