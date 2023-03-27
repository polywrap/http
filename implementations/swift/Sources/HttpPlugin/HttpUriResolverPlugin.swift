//
//  File.swift
//  
//
//  Created by Cesar Brazon on 27/3/23.
//

import Foundation

public struct ArgsTryResolverUri {
    var authority: String
    var path: String
    init(authority: String, path: String) {
        self.authority = authority
        self.path = path
    }
}

public struct MaybeUriOrManifest {
    var uri: String?
    var manifest: [UInt8]?
    init(uri: String? = nil, manifest: [UInt8]? = nil) {
        self.uri = uri
        self.manifest = manifest
    }
}

public enum ResolverError: Error {
    
}

public typealias ResultType = Result<MaybeUriOrManifest?, ResolverError>

public class HttpUriResolverPlugin {
    var module: HttpPlugin = HttpPlugin()
    init() {
        
    }
    
    public func tryResolveUri(_ args: ArgsTryResolverUri) async throws -> MaybeUriOrManifest? {
        if args.authority != "http" && args.authority != "https" {
            return nil
        }
        
        let manifestSearchPattern = "wrap.info"
        let url = args.path + "/" + manifestSearchPattern
        do {
            let result = try await module.get(ArgsGet(url: url, request: Request(responseType: .BINARY)))
            if let body = result.body {
                if let data = Data(base64Encoded: body) {
                    let buffer = [UInt8](data)
                    return MaybeUriOrManifest(manifest: Optional(buffer))
                }
            }
            return MaybeUriOrManifest()
        } catch {
            return MaybeUriOrManifest()
        }
    }
}
