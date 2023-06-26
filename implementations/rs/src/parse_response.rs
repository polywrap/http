use std::collections::BTreeMap;

use polywrap_plugin::{error::PluginError};

use crate::wrap::types::{ResponseType, Response};

pub fn parse_response(
    response: ureq::Response,
    encoding: ResponseType,
) -> Result<Response, PluginError> {
    let headers = response
        .headers_names()
        .iter()
        .map(|header_name| {
            (
                header_name.to_string(),
                response.header(header_name).unwrap().to_string(),
            )
        })
        .collect::<BTreeMap<String, String>>();
    let status = response.status();
    let status_text = response.status_text().to_string();

    let mut reader = response.into_reader();
    let mut data = vec![];
    reader.read_to_end(&mut data).unwrap();

    let data = match encoding {
        ResponseType::BINARY => base64::encode(data),
        _ => String::from_utf8_lossy(&data).to_string(),
    };

    Ok(Response {
        status: status.into(),
        status_text,
        headers: Some(headers),
        body: Some(data),
    })
}