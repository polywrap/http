Pod::Spec.new do |s|
    s.name             = 'HttpPlugin'
    s.version          = '0.0.1'
    s.summary          = 'Http plugin'
    s.homepage         = 'https://github.com/polywrap/http'
    s.license          = 'MIT'
    s.author           = { 'Cesar' => 'cesar@polywrap.io' }
  
    s.source_files = 'implementations/swift/Source/**/*.swift'
    s.swift_version  = "5.0"
    s.ios.deployment_target = '13.0'
    s.osx.deployment_target = '10.15'
    s.source = { :git => "https://github.com/polywrap/http.git", :branch => 'feat/swift-implementation' }
    s.static_framework = true
    s.dependency 'PolywrapClient', '= 0.0.6'
  end