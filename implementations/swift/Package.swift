// swift-tools-version: 5.7
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "HttpPlugin",
    platforms: [.iOS(.v15), .macOS(.v10_15)],
    products: [
        // Products define the executables and libraries a package produces, and make them visible to other packages.
        .library(
            name: "HttpPlugin",
            targets: ["HttpPlugin"]),
    ],
    dependencies: [
        // Dependencies declare other packages that this package depends on.
        // .package(url: /* package url */, from: "1.0.0"),
        .package(url: "https://github.com/polywrap/swift-client", branch: "main")
    ],
    targets: [
        // Targets are the basic building blocks of a package. A target can define a module or a test suite.
        // Targets can depend on other targets in this package, and on products in packages this package depends on.
        .target(
            name: "HttpPlugin",
            dependencies: [
                .product(name: "PolywrapClient", package: "swift-client"),
            ],
            path: "Source"
        ),
        .testTarget(
            name: "HttpPluginTests",
            dependencies: ["HttpPlugin"],
            path: "Tests"
        ),
    ],
    swiftLanguageVersions: [.v5]
)
