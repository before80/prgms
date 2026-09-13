# swift sdk
Perform operations on Swift SDKs.

## Overview {#Overview}
By default, Swift Package Manager compiles code for the host platform on which you run it. Swift 6.1 introduced SDKs (through [SE-0387](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0387-cross-compilation-destinations.md)) to support cross-compilation.

SDKs are tightly coupled with the toolchain used to create them. Supported SDKs are distributed by the Swift project with links on the [installation page](https://www.swift.org/install/) for macOS and Linux, and included in the distribution for Windows.

Additionally, the Swift project provides the tooling repository [swift-sdk-generator](https://github.com/swiftlang/swift-sdk-generator) that you can use to create a custom SDK for your preferred platform.
