import {
  Http_Request,
  Http_Response,
  Http_FormDataEntry,
  Http_ResponseType,
} from "./wrap";

import {
  Options as KyOptions,
  KyResponse
} from "ky-universal";

export function toKyOptions(request: Http_Request): {
  options: KyOptions,
  responseType: Http_ResponseType
 } {
  const {
    headers,       // Map<Types.String, Types.String> | null;
    urlParams,     // Map<Types.String, Types.String> | null;
    responseType,  // Types.Http_ResponseType;
    body,          // Types.String | null;
    formData,      // Array<Types.Http_FormDataEntry> | null;
    timeout        // Types.UInt32 | null;
  } = request;

  const options: KyOptions = {
    headers: headers ? mapToRecord(headers) : undefined,
    searchParams: urlParams ? mapToRecord(urlParams) : undefined,
    body: formData ? toFormData(formData) : body ? body : undefined,
    timeout: timeout ? timeout : undefined
  };

  return {
    options,
    responseType
  }
}

/**
 * Convert KyResponse to Response
 *
 * @param kyResponse
 * @param responseType
 */
export async function fromKyResponse(
  kyResponse: KyResponse,
  responseType: Http_ResponseType
): Promise<Http_Response> {
  const responseHeaders = new Map<string, string>();
  kyResponse.headers.forEach(
    (value: string, key: string) => {
      responseHeaders.set(
        key,
        Array.isArray(value)
          ? value.join(" ")
          : value
      );
    }
  )

  const response: Http_Response = {
    status: kyResponse.status,
    statusText: kyResponse.statusText,
    headers: responseHeaders,
  };

  if (responseType == "BINARY") {
    // encode response as base64
    response.body = Buffer.from(
      await kyResponse.arrayBuffer()
    ).toString("base64");
  } else if (responseType == "TEXT") {
    response.body = await kyResponse.text();
  } else {
    throw Error(
      `HttpPlugin: Unknown response type "${responseType}"`
    );
  }

  return response;
}

export function mapToRecord<V>(
  map: Map<string, V>
): Record<string, V> {
  const record: Record<string, V> = { };
  for (const entry of map.entries()) {
    record[entry[0]] = entry[1];
  }
  return record;
}

export function toFormData(entries: Http_FormDataEntry[]): FormData {
  const fd = new FormData();
  entries.forEach((entry) => {
    let value: string | Blob = "";

    if (entry.value) {
      value = entry.type
        ? new Blob([entry.value], { type: entry.type })
        : entry.value;
    }
    fd.append(entry.name, value, entry.fileName || undefined);
  });
  return fd;
}
