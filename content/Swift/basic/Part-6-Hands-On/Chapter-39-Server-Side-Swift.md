+++
title = "第39章 选读：服务端 Swift"
weight = 390
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十九章：选读：服务端 Swift

> Swift 不只活在手机和电脑里。借助异步运行时、事件驱动网络和服务端框架，它也能写 API、后台任务和实时服务。语言核心不变，变化的是运行环境、部署方式和并发边界。

## 39.1 服务端 Swift 的组成

典型技术栈：

| 层 | 常见选择 |
| --- | --- |
| HTTP 框架 | Vapor、Hummingbird |
| 异步网络 | SwiftNIO |
| 数据库 | Fluent、SQLKit、PostgreSQL/MySQL 驱动 |
| 序列化 | Codable、JSON |
| 部署 | Docker、Linux 服务、云平台 |

服务端代码通常是长期运行进程，因此内存泄漏、阻塞 I/O、错误吞吐和并发隔离比命令行工具更关键。

## 39.2 一个最小路由

以 Vapor 风格的接口表示：

```swift
import Vapor

func routes(_ app: Application) throws {
    app.get("health") { req async -> String in
        "ok"
    }

    app.get("users", ":id") { req async throws -> UserDTO in
        guard let id = req.parameters.get("id", as: Int.self) else {
            throw Abort(.badRequest)
        }
        return try await UserService().find(id: id)
    }
}
```

请求处理函数是异步的，`await` 表示可能在数据库或下游服务上等待。不要让一个慢请求阻塞整个事件循环。

## 39.3 请求与模型

服务端的第一件事是定义"请求长什么样、返回什么"，把 JSON 的形状变成类型：

```swift
struct CreateUserRequest: Content {
    let name: String
    let email: String
}

struct UserDTO: Content {
    let id: Int
    let name: String
}

func create(_ req: Request) async throws -> UserDTO {
    let input = try req.content.decode(CreateUserRequest.self)
    return try await UserService().create(name: input.name, email: input.email)
}
```

外部输入永远要校验。空名字、重复邮箱、超长字段和非法编码都不应该进入数据库。

## 39.4 并发与共享状态

服务端会同时处理很多请求。共享缓存、计数器和连接池都必须正确处理并发：

```swift
actor RequestCounter {
    private var count = 0

    func increment() -> Int {
        count += 1
        return count
    }
}
```

actor 适合保护进程内的可变状态；数据库连接池、文件系统和外部服务则由各自的客户端库维护并发约束。

## 39.5 配置与秘密

配置不应该硬编码：

```swift
let port = Environment.get("PORT").flatMap(Int.init) ?? 8080
let databaseURL = Environment.get("DATABASE_URL") ?? "sqlite://local.db"
```

密钥、令牌和连接串通过环境变量、密钥管理服务或部署平台注入。日志里不要输出秘密，错误响应也不要暴露内部堆栈。

## 39.6 测试与部署

服务端测试通常分层：

- 路由测试：输入请求，检查状态码和返回体。
- 服务测试：用内存数据库验证业务规则。
- 集成测试：验证真实数据库、迁移和事务。
- 压测：验证并发下的尾延迟和资源占用。

Docker 部署时建议：

```dockerfile
FROM swift:6.3
WORKDIR /app
COPY . .
RUN swift build -c release
CMD [".build/release/App"]
```

生产镜像应使用多阶段构建，移除编译器和源码，只保留运行产物与必要动态库。

## 39.7 官方资料与延伸阅读

- [Swift 官方文档](https://www.swift.org/documentation/)
- [SwiftNIO](https://github.com/apple/swift-nio)
- [Vapor](https://vapor.codes/)
- [Hummingbird](https://hummingbird-project.io/)
- [Swift on Server](https://www.swift.org/server/)

服务端 Swift 的生态还在发展。先掌握语言、并发和模块边界，再选择框架；框架会换，基础不会。

## 39.8 本章小结

| 主题 | 关键结论 |
| --- | --- |
| HTTP 框架 | 处理路由、请求和响应 |
| 异步 I/O | 避免阻塞事件循环 |
| 共享状态 | 用 actor、连接池或专用服务保护 |
| 配置 | 环境变量或密钥服务注入 |
| 测试 | 路由、服务、集成、压测分层 |
| 部署 | 发布构建 + 多阶段容器镜像 |

## 39.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 在请求处理里做阻塞 I/O | 会拖慢整个事件循环 |
| 把秘密提交进仓库 | 使用环境变量或密钥管理 |
| 共享全局可变状态 | 用 actor 或受控服务保护 |
| 只测正常请求 | 覆盖非法输入、超时和下游失败 |
| 直接把错误堆栈返回客户端 | 暴露内部实现，存在安全风险 |
| 生产镜像包含完整工具链 | 使用多阶段构建减小体积和攻击面 |

## 39.10 结语

到这里，Swift 快速入门的主线结束了。你走过了语法、类型、内存、并发、工程和实战，剩下的不是“背完语言”，而是持续把真实问题拆成清晰的类型、边界和测试。语言是工具，判断力才是长期资产。
