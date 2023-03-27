import Foundation

public struct ArgsGet {
    var url: String
    var request: Request?

    init(url: String, request: Request? = nil) {
        self.url = url
        self.request = request
    }
}

public struct ArgsPost {
    var url: String
    var request: Request?
    
    init(url: String, request: Request? = nil) {
        self.url = url
        self.request = request
    }
}

public struct Response {
    var status: Int
    var statusText: String
    var headers: Dictionary<String, String>?
    var body: String?
}

public struct Request {
    var headers: Dictionary<String, String>?
    var urlParams: Dictionary<String, String>?
    var responseType: ResponseType
    var body: String?
    var formData: [FormDataEntry]?
    var timeout: UInt32?
    
    init(
        headers: Dictionary<String, String>? = nil,
        urlParams: Dictionary<String, String>? = nil,
        responseType: ResponseType,
        body: String? = nil,
        formData: [FormDataEntry]? = nil,
        timeout: UInt32? = nil
    ) {
        self.headers = headers
        self.urlParams = urlParams
        self.responseType = responseType
        self.body = body
        self.formData = formData
        self.timeout = timeout
    }
}

enum ResponseType {
    case TEXT
    case BINARY
}

struct FormDataEntry {
    var name: String
    var value: String?
    var fileName: String?
    var type: String?
}

public class HttpPlugin {
    public init() {
    }
    
    public func get(_ args: ArgsGet) async throws -> Data {
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
    
    public func post(_ args: ArgsPost) async throws -> Data {
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
    
    func get(args: ArgsGet, completion: @escaping (Result<Data, Error>) -> Void) {
        let request = buildRequestConfig(url: args.url, request: args.request)
        let session = URLSession.shared
        let task = session.dataTask(with: request) { (data, response, error) in
            if let error = error {
                // handle error
                completion(.failure(error))
            } else if let data = data {
                // handle response
                completion(.success(data))
            } else {
                // handle unexpected error
            }
        }
        task.resume()
    }
    
    func post(args: ArgsPost, completion: @escaping (Result<Data, Error>) -> Void) {
        var request = buildRequestConfig(url: args.url, request: args.request)
        request.httpMethod = "post"
        let session = URLSession.shared
        let task = session.dataTask(with: request) { (data, response, error) in
            if let error = error {
                // handle error
                completion(.failure(error))
            } else if let data = data {
                // handle response
                completion(.success(data))
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
}
