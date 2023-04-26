use std::sync::Arc;

use crate::wrap::wrap_info::get_manifest;
use mapping::{parse_request, parse_response};
use polywrap_client::{
    core as polywrap_core, msgpack as polywrap_msgpack, plugin as polywrap_plugin,
};
use polywrap_core::invoke::Invoker;
use polywrap_plugin::{error::PluginError, implementor::plugin_impl, JSON};
use wrap::{
    module::{ArgsGet, ArgsPost, Module},
    types::{HttpHttpResponse as HttpResponse, HttpHttpResponseType as ResponseType},
};
pub mod mapping;
pub mod wrap;

#[derive(Debug)]
pub struct HttpPlugin {}

#[plugin_impl]
impl Module for HttpPlugin {
    fn get(
        &mut self,
        args: &ArgsGet,
        _: Arc<dyn Invoker>,
    ) -> Result<Option<HttpResponse>, PluginError> {
        let response = parse_request(&args.url, args.request.clone(), mapping::RequestMethod::GET)
            .unwrap()
            .call()
            .map_err(|e| PluginError::ModuleError(e.to_string()))?;

        let response_type = if let Some(r) = &args.request {
            r.response_type
        } else {
            ResponseType::TEXT
        };

        let parsed_response = parse_response(response, response_type)?;

        Ok(Some(parsed_response))
    }

    fn post(
        &mut self,
        args: &ArgsPost,
        _: Arc<dyn Invoker>,
    ) -> Result<Option<HttpResponse>, PluginError> {
        let response = parse_request(
            &args.url,
            args.request.clone(),
            mapping::RequestMethod::POST,
        )
        .unwrap()
        .call()
        .map_err(|e| PluginError::ModuleError(e.to_string()))?;

        let response_type = if let Some(r) = &args.request {
            r.response_type
        } else {
            ResponseType::TEXT
        };

        let parsed_response = parse_response(response, response_type)?;

        Ok(Some(parsed_response))
    }
}
