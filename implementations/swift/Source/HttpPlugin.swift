import Foundation

import PolywrapClient

public enum PluginError: Error {
    case BadRequest
}

public class HttpPlugin: Plugin {
    public var methodsMap: [String: PluginMethod] = [:]

    public func get(_ args: ArgsGet, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response {
        return try runBlocking {
            return try await withCheckedThrowingContinuation{ continuation in
                get(args: args) { result in
                    switch result {
                    case .success(let value):
                        continuation.resume(returning: value)
                        
                    case .failure(let error):
                        continuation.resume(throwing: error)
                    }
                }
            }
        }
    }
    
    public func post(_ args: ArgsPost, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response {
        return try runBlocking {
            return try await withCheckedThrowingContinuation{ continuation in
                post(args: args) { result in
                    switch result {
                    case .success(let value):
                        continuation.resume(returning: value)
                        
                    case .failure(let error):
                        continuation.resume(throwing: error)
                    }
                }
            }
        }
    }
    
    func get(args: ArgsGet, completion: @escaping (Result<Response, Error>) -> Void) {
        let request = buildRequestConfig(url: args.url, request: args.request)
        let responseType = (args.request?.responseType != nil ? args.request?.responseType : ResponseType.TEXT)!
    
        executeRequest(request: request, responseType: responseType) { result in
            switch result {
            case .success(let response):
                return completion(.success(response))
            case .failure(let error):
                return completion(.failure(error))
            }
        }
    }
    
    func post(args: ArgsPost, completion: @escaping (Result<Response, Error>) -> Void) {
        var request = buildRequestConfig(url: args.url, request: args.request)
        request.httpMethod = "post"
        let responseType = (args.request?.responseType != nil ? args.request?.responseType : ResponseType.TEXT)!
    
        executeRequest(request: request, responseType: responseType) { result in
            switch result {
            case .success(let response):
                return completion(.success(response))
            case .failure(let error):
                return completion(.failure(error))
            }
        }
    }
    
    func executeRequest(request: URLRequest, responseType: ResponseType, completion: @escaping (Result<Response, Error>) -> Void) -> Void {
        let task = URLSession.shared.dataTask(with: request) { (data, response, error) in
            if let error = error {
                // handle error
                completion(.failure(error))
            } else if let data = data {
                // handle response
                let response = self.buildResponse(data: data, httpResponse: response, responseType: responseType)
                completion(.success(response))
            } else {
                // handle unexpected error
            }
        }
        task.resume()
    }
    
    func buildRequestConfig(url: String, request: Request?) -> URLRequest {
        var urlComponents = URLComponents(string: url)
        
        if request?.urlParams != nil {
            if let params = request?.urlParams as? [String: String] {
                urlComponents?.queryItems = params.map { URLQueryItem(name: $0.key, value: $0.value) }
            }
        }

        let url = URL(string: urlComponents?.url?.absoluteString ?? url)!
        var urlRequest = URLRequest(url: url)
        
        if request?.headers != nil {
            if let headers = request?.headers as? [String: String] {
                for (header, value) in headers {
                    urlRequest.setValue(value, forHTTPHeaderField: header)
                }
            }
        }
        
        if request?.body != nil {
            let jsonBody = request?.body!.data(using: .utf8)
            urlRequest.httpBody = jsonBody
        }

        return urlRequest
    }
    
    func buildResponse(data: Data, httpResponse: URLResponse?, responseType: ResponseType) -> Response {
        var body: String
        switch responseType {
        case .TEXT:
            body = String(data: data, encoding: .utf8)!
        case .BINARY:
            body = data.base64EncodedString()
        }
        
        let httpResponse = httpResponse as? HTTPURLResponse
        let text = statusText(forStatusCode: httpResponse!.statusCode)
        let response = Response.init(status: httpResponse!.statusCode, statusText: text, body: body)
        return response
    }
    
    func statusText(forStatusCode statusCode: Int) -> String {
        switch statusCode {
        case 200:
            return "OK"
        case 201:
            return "Created"
        case 204:
            return "No Content"
        case 400:
            return "Bad Request"
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not Found"
        case 500:
            return "Internal Server Error"
        default:
            return "Unknown"
        }
    }
}

func getHttpPlugin() -> Plugin {
    var plugin = HttpPlugin()
    plugin.addMethod(name: "get", closure: plugin.get)
    plugin.addMethod(name: "post", closure: plugin.post)
    return plugin
}
