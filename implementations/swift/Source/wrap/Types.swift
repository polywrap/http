public struct ArgsGet: Codable {
    var url: String
    var request: Request?

    public init(url: String, request: Request? = nil) {
        self.url = url
        self.request = request
    }
}

public struct ArgsPost: Codable {
    var url: String
    var request: Request?

    public init(url: String, request: Request? = nil) {
        self.url = url
        self.request = request
    }
}

public struct Response: Codable {
    var status: Int
    var statusText: String
    var headers: [String: String]?
    var body: String?
}

public struct Request: Codable {
    var headers: [String: String]?
    var urlParams: [String: String]?
    var responseType: ResponseType
    var body: String?
    var formData: [FormDataEntry]?
    var timeout: UInt32?

    public init(
        headers: [String: String]? = nil,
        urlParams: [String: String]? = nil,
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

public enum ResponseType: Codable {
    case TEXT
    case BINARY
}

public struct FormDataEntry: Codable {
    var name: String
    var value: String?
    var fileName: String?
    var type: String?
}
