// NOTE: This is an auto-generated file.
// All modifications will be overwritten.

import PolywrapClient
import Foundation

// Env START //


// Env END //

// Objects START //

public struct Response: Codable {
    var status: Int32
    var statusText: String
    var headers: [String: String]?
    var body: String?
}

public struct Request: Codable {
    var headers: [String: String]?
    var urlParams: [String: String]?
    var responseType: ResponseType
    var body: String?
    var formData: Array<FormDataEntry>?
    var timeout: UInt32?
}

public struct FormDataEntry: Codable {
    var name: String
    var value: String?
    var fileName: String?
    var type: String?
}


// Objects END //

// Enums START //

public enum ResponseType: String, Codable {
    case TEXT
    case BINARY
}


// Enums END //

// Imported objects START //


// Imported objects END //

// Imported envs START //


// Imported envs END //

// Imported enums START //


// Imported enums END //

// Imported modules START //

// Imported Modules END //
