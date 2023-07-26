import PolywrapClient

protocol Plugin: PluginModule {
    func get(_ args: ArgsGet, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response
    func post(_ args: ArgsPost, _ env: VoidCodable?, _ invoker: Invoker) throws -> Response
}
