import XCTest
@testable import HttpPlugin

struct ExpectedResponse: Decodable {
    var success: String
    
    init(success: String) {
        self.success = success
    }
}

final class HttpPluginTests: XCTestCase {
    func testGet() async throws {
        let plugin = HttpPlugin()
        let headers = ["Accept":"application/json"]
        let request = Request(headers: headers, responseType: .TEXT)
        let args = ArgsGet(url: "https://reqbin.com/echo/get/json", request: request)
        let response = try await plugin.get(args)
        
        if let body = response.body {
            let r = try! JSONDecoder().decode(ExpectedResponse.self, from: body.data(using: .utf8)!)
            XCTAssert(r.success == "true")
        }
    }
    
    func testUrlParams() async throws {
        let plugin = HttpPlugin()
        let request = Request(urlParams: ["a": "a", "b": "b"], responseType: ResponseType.TEXT)
        let builtRequest = plugin.buildRequestConfig(url: "cool-domain.com", request: request)
        
        if let url = builtRequest.url?.absoluteString {
            XCTAssert(url.contains("a=a"))
            XCTAssert(url.contains("b=b"))
        }
    }
    
    
    func testPost() async throws {
        let plugin = HttpPlugin()
        let headers = ["Accept":"application/json"]
        let body = "{\"Id\":78912,\"Customer\":\"Jason Sweet\",\"Quantity\":1,\"Price\":18.00}"
        let request = Request(headers: headers, responseType: .TEXT, body: body)
        let args = ArgsPost(url: "https://reqbin.com/echo/post/json", request: request)
        let response = try await plugin.post(args)
        
        if let body = response.body {
            let r = try! JSONDecoder().decode(ExpectedResponse.self, from: body.data(using: .utf8)!)
            XCTAssert(r.success == "true")
        }
    }
    
    func testGetManifest() async throws {
        let resolver = HttpUriResolverPlugin()
        let args = ArgsTryResolverUri(authority: "https", path: "https://raw.githubusercontent.com/polywrap/wrap-test-harness/v0.2.1/wrappers/subinvoke/00-subinvoke/implementations/as")
        let response = try await resolver.tryResolveUri(args)
        XCTAssert(response?.manifest is [UInt8])
    }
}
