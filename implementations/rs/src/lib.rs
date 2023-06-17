use crate::{wrap::wrap_info::get_manifest, parse_request::parse_request, parse_response::parse_response};
use multipart::client::lazy::Multipart;
use polywrap_core::invoker::Invoker;
use polywrap_plugin::{error::PluginError, implementor::plugin_impl, JSON};
use ureq::{Request as UreqRequest, Response as UreqResponse};
use std::{io::Cursor, sync::Arc};
use wrap::{
    module::{ArgsGet, ArgsPost, Module},
    types::{Response, ResponseType, FormDataEntry},
};
pub mod wrap;
pub mod parse_response;
pub mod parse_request;

pub enum RequestMethod {
    GET,
    POST,
}

#[derive(Debug)]
pub struct HttpPlugin;

#[plugin_impl]
impl Module for HttpPlugin {
    fn get(
        &mut self,
        args: &ArgsGet,
        _: Arc<dyn Invoker>,
    ) -> Result<Option<Response>, PluginError> {
        let response = parse_request(&args.url, args.request.clone(), RequestMethod::GET)
            .unwrap()
            .call()
            .map_err(|e| PluginError::InvocationError {
                exception: e.to_string(),
            })?;

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
    ) -> Result<Option<Response>, PluginError> {
        let request = parse_request(
            &args.url,
            args.request.clone(),
            RequestMethod::POST,
        )
        .unwrap();

        let response_type = if let Some(r) = &args.request {
            r.response_type
        } else {
            ResponseType::TEXT
        };

        let response = if let Some(r) = &args.request {
            if let Some(body) = &r.body {
                handle_json(request, body)?
            } else if let Some(form_data) = &r.form_data {
                handle_form_data(request, form_data)?
            } else {
                request.call().map_err(|e| PluginError::InvocationError {
                    exception: e.to_string(),
                })?
            }
        } else {
            request.call().map_err(|e| PluginError::InvocationError {
                exception: e.to_string(),
            })?
        };
        let parsed_response = parse_response(response, response_type)?;

        Ok(Some(parsed_response))
    }
}

fn handle_form_data(request: UreqRequest, form_data: &Vec<FormDataEntry>) -> Result<UreqResponse, PluginError> {
    let mut multipart = Multipart::new();
    for entry in form_data.iter() {
        if entry._type.is_some() {
            if let Some(v) = &entry.value {
                let buf = base64::decode(v).unwrap();
                let cursor = Cursor::new(buf);
                let file_name = if let Some(f) = &entry.file_name {
                    Some(f.as_str())
                } else {
                    None
                };
                multipart.add_stream(entry.name.as_str(), cursor, file_name, None);
            };
        } else {
            if let Some(v) = &entry.value {
                multipart.add_text(entry.name.as_str(), v);
            };
        }
    }
    // Send the request with the multipart/form-data
    let mdata = multipart.prepare().unwrap();
    request
        .set(
            "Content-Type",
            &format!("multipart/form-data; boundary={}", mdata.boundary()),
        )
        .send(mdata)
        .map_err(|e| PluginError::InvocationError {
            exception: e.to_string(),
        })
}

fn handle_json(request: UreqRequest, body: &String) -> Result<UreqResponse, PluginError> {
    let value = JSON::from_str::<JSON::Value>(body.as_str());
    if let Ok(json) = value {
        request
            .send_json(json)
            .map_err(|e| PluginError::InvocationError {
                exception: e.to_string(),
            })
    } else {
        return Err(PluginError::JSONError(value.unwrap_err()));
    }
}