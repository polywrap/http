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
    msgpack::{msgpack, serialize},
    plugin::{package::PluginPackage, Map, JSON},
};
use serde::{Deserialize, Serialize};
use std::{
    collections::BTreeMap,
    sync::{Arc, Mutex},
};

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
fn simple_get() {
    let response = get_client()
        .invoke::<HttpResponse>(
            &Uri::try_from("plugin/http").unwrap(),
            "get",
            Some(&msgpack!({
                "url": "https://jsonplaceholder.typicode.com/todos/1",
            })),
            None,
            None,
        )
        .unwrap();
    assert_eq!(response.status, 200);
    assert_ne!(response.body, None);
    let body: ExpectedResponse = JSON::from_str(&response.body.unwrap()).unwrap();
    assert_eq!(body.id, 1);
}

#[derive(Debug, Serialize, Deserialize)]
struct GetArgs {
    url: String,
    request: Request,
}

#[derive(Debug, Serialize, Deserialize)]
struct Request {
    #[serde(rename = "urlParams")]
    url_params: Map<String, String>,
    #[serde(rename = "responseType")]
    response_type: String,
}

#[test]
fn params_get() {
    let mut params = Map(BTreeMap::new());
    params.0.insert("id".to_string(), "1".to_string());

    let args = GetArgs {
        url: "https://jsonplaceholder.typicode.com/todos".to_string(),
        request: Request {
            url_params: params,
            response_type: "TEXT".to_string(),
        },
    };
    let response = get_client()
        .invoke::<HttpResponse>(
            &Uri::try_from("plugin/http").unwrap(),
            "get",
            Some(&serialize(args).unwrap()),
            None,
            None,
        )
        .unwrap();
    assert_eq!(response.status, 200);
    assert_ne!(response.body, None);
    let response: JSON::Value = JSON::from_str(response.body.unwrap().as_str()).unwrap();
    if let JSON::Value::Array(r) = response {
        assert_eq!(r.len(), 1)
    } else {
        panic!("Error in params_get test")
    }
}
