// NOTE: This is an auto-generated file.
//       All modifications will be overwritten.

import PolywrapClient
import Foundation

public struct ArgsGet: Codable {
    var url: String,
    var request: Request?,
}

public struct ArgsPost: Codable {
    var url: String,
    var request: Request?,
}


protocol Plugin: PluginModule {
    func get(_ args: ArgsGet, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response?

    func post(_ args: ArgsPost, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response?
}
