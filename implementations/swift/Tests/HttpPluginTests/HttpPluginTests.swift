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
        
        let r = try! JSONDecoder().decode(ExpectedResponse.self, from: response)
        XCTAssert(r.success == "true")
    }
    
    func testUrlParams() async throws {
        let plugin = HttpPlugin()
        let request = Request(urlParams: ["a": "a", "b": "b"], responseType: ResponseType.TEXT)
        let builtRequest = plugin.buildRequestConfig(url: "cool-domain.com", request: request)
        XCTAssert(builtRequest.url?.absoluteString == Optional("cool-domain.com?a=a&b=b"))
    }
    
    
    func testPost() async throws {
        let plugin = HttpPlugin()
        let headers = ["Accept":"application/json"]
        let body = "{\"Id\":78912,\"Customer\":\"Jason Sweet\",\"Quantity\":1,\"Price\":18.00}"
        let request = Request(headers: headers, responseType: .TEXT, body: body)
        let args = ArgsPost(url: "https://reqbin.com/echo/post/json", request: request)
        let response = try await plugin.post(args)
        
        let r = try! JSONDecoder().decode(ExpectedResponse.self, from: response)
        XCTAssert(r.success == "true")
    }
}
