import XCTest
@testable import HttpPlugin
import PolywrapClient

struct ExpectedResponse: Decodable {
    var success: String
    
    init(success: String) {
        self.success = success
    }
}

func getClient() throws -> (PolywrapClient, Uri) {
    let uri = try Uri("plugin/http")
    let httpPlugin = getHttpPlugin()
    let package = PluginPackage(httpPlugin)
    let builder = BuilderConfig().addPackage(uri, package)
    return (builder.build(), uri)
}

final class HttpPluginTests: XCTestCase {
    func testGet() async throws {
        let (client, uri) = try getClient()
        let args = ArgsGet(url: "https://jsonplaceholder.typicode.com/todos", request: nil)
        
        let response: Response = try client.invoke(uri: uri, method: "get", args: args, env: nil)
            
        XCTAssertEqual(response.status, 200)
        
        if let body = response.body {
            if let data = body.data(using: .utf8) {
                if let jsonArray = try JSONSerialization.jsonObject(with: data, options: []) as? [[String: Any]] {
                    XCTAssertEqual(jsonArray[0]["userId"] as! Int, 1)
                   } else {
                    XCTFail("Error serializing body to JSON")
                }
            } else {
                XCTFail("Error converting body to data")
            }
        } else {
            XCTFail("Body attribute not found in response")
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
        let (client, uri) = try getClient()
        let headers = ["Accept":"application/json"]
        let body = "{\"Id\":78912,\"Customer\":\"Jason Sweet\",\"Quantity\":1,\"Price\":18.00}"

        let request = Request(headers: headers, responseType: .TEXT, body: body)
        let args = ArgsPost(url: "https://reqbin.com/echo/post/json", request: request)
        let response: Response = try client.invoke(uri: uri, method: "post", args: args, env: nil)

        if let body = response.body {
            let r = try! JSONDecoder().decode(ExpectedResponse.self, from: body.data(using: .utf8)!)
            XCTAssertEqual(r.success, "true")
        } else {
            XCTFail("Body attribute not found in response")
        }
    }
}
