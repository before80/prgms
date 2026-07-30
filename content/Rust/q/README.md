# Rust FAQ for Go Developers

`new-topics/` 是对原 `topics/` 的整套重写版：面向**熟悉 Go、初学 Rust** 的读者，按由浅入深的学习顺序组织。文件统一保留 Hugo front matter、问题锚点、热度标签，并尽量提供术语解释、Rust 示例和 Go 对比；正文只保留 `## Qn...` 作为问题标题层级，其余说明用粗体标签。

当前总览：

- `54` 个主题文件
- `944` 道问答
- `1517` 个 Rust 代码块
- `565` 个 Go 代码块
- 全量校验：`validate.py -> 0 error / 0 warning`

## Heat Tags

- `hot`：高频问题，论坛 / Stack Overflow / 新手最容易卡住
- `common`：日常开发经常遇到
- `occasional`：特定场景才会碰到
- `advanced`：进阶与底层细节

## Topic Index

| # | 中文主题 | File | Q Count | weight |
|---|---|---|---:|---:|
| 01 | 安装 | [01-installation.md](01-installation.md) | 22 | 10 |
| 02 | 更新与版本管理 | [02-updating.md](02-updating.md) | 15 | 20 |
| 03 | 编译 | [03-compilation.md](03-compilation.md) | 18 | 30 |
| 04 | 运行 | [04-running.md](04-running.md) | 18 | 40 |
| 05 | 注释与文档 | [05-comments.md](05-comments.md) | 15 | 50 |
| 06 | 变量与可变性 | [06-variables.md](06-variables.md) | 18 | 60 |
| 07 | 常量与静态量 | [07-constants.md](07-constants.md) | 14 | 70 |
| 08 | 数据类型 | [08-data-types.md](08-data-types.md) | 20 | 80 |
| 09 | 函数 | [09-functions.md](09-functions.md) | 20 | 90 |
| 10 | 控制流 | [10-control-flow.md](10-control-flow.md) | 18 | 100 |
| 11 | 所有权 | [11-ownership.md](11-ownership.md) | 22 | 110 |
| 12 | 引用与借用 | [12-references-and-borrowing.md](12-references-and-borrowing.md) | 22 | 120 |
| 13 | 切片 | [13-slices.md](13-slices.md) | 16 | 130 |
| 14 | 字符串与文本 | [14-strings-and-text.md](14-strings-and-text.md) | 21 | 140 |
| 15 | 内存与分配 | [15-memory-and-allocation.md](15-memory-and-allocation.md) | 19 | 150 |
| 16 | 结构体 | [16-structs.md](16-structs.md) | 19 | 160 |
| 17 | 枚举 | [17-enums.md](17-enums.md) | 19 | 170 |
| 18 | 模式匹配 | [18-pattern-matching.md](18-pattern-matching.md) | 19 | 180 |
| 19 | 常见集合 | [19-collections.md](19-collections.md) | 25 | 190 |
| 20 | 迭代器与闭包 | [20-iterators-and-closures.md](20-iterators-and-closures.md) | 25 | 200 |
| 21 | 错误处理 | [21-error-handling.md](21-error-handling.md) | 22 | 210 |
| 22 | 包、Crate 与模块 | [22-packages-crates-and-modules.md](22-packages-crates-and-modules.md) | 20 | 220 |
| 23 | Cargo 工作流 | [23-cargo-workflow.md](23-cargo-workflow.md) | 24 | 230 |
| 24 | 测试 | [24-testing.md](24-testing.md) | 23 | 240 |
| 25 | 泛型 | [25-generics.md](25-generics.md) | 19 | 250 |
| 26 | Trait | [26-traits.md](26-traits.md) | 22 | 260 |
| 27 | 生命周期 | [27-lifetimes.md](27-lifetimes.md) | 20 | 270 |
| 28 | 智能指针 | [28-smart-pointers.md](28-smart-pointers.md) | 20 | 280 |
| 29 | 并发与线程 | [29-concurrency-and-threads.md](29-concurrency-and-threads.md) | 21 | 290 |
| 30 | 高级函数与闭包 | [30-advanced-functions-and-closures.md](30-advanced-functions-and-closures.md) | 16 | 300 |
| 31 | 异步编程 | [31-async-programming.md](31-async-programming.md) | 25 | 310 |
| 32 | 宏 | [32-macros.md](32-macros.md) | 18 | 320 |
| 33 | 高级 Trait | [33-advanced-traits.md](33-advanced-traits.md) | 16 | 330 |
| 34 | 高级类型 | [34-advanced-types.md](34-advanced-types.md) | 16 | 340 |
| 35 | Unsafe Rust | [35-unsafe-rust.md](35-unsafe-rust.md) | 18 | 350 |
| 36 | Serde 与序列化 | [36-serde-and-serialization.md](36-serde-and-serialization.md) | 17 | 360 |
| 37 | 文件系统、Path 与 IO | [37-filesystem-path-and-io.md](37-filesystem-path-and-io.md) | 15 | 370 |
| 38 | 命令行与 clap | [38-cli-with-clap.md](38-cli-with-clap.md) | 16 | 380 |
| 39 | 日志与 tracing | [39-logging-and-tracing.md](39-logging-and-tracing.md) | 14 | 390 |
| 40 | HTTP 客户端与服务端 | [40-http-client-and-server.md](40-http-client-and-server.md) | 15 | 400 |
| 41 | 时间与日期 | [41-time-and-dates.md](41-time-and-dates.md) | 14 | 410 |
| 42 | 正则表达式 | [42-regex.md](42-regex.md) | 13 | 420 |
| 43 | 数据库与 SQL | [43-database-and-sql.md](43-database-and-sql.md) | 15 | 430 |
| 44 | 配置管理 | [44-configuration.md](44-configuration.md) | 14 | 440 |
| 45 | gRPC 与 Protobuf | [45-grpc-and-protobuf.md](45-grpc-and-protobuf.md) | 14 | 450 |
| 46 | 密码学与哈希 | [46-cryptography-and-hashing.md](46-cryptography-and-hashing.md) | 14 | 460 |
| 47 | WebAssembly | [47-webassembly.md](47-webassembly.md) | 14 | 470 |
| 48 | 缓存与 Redis | [48-caching-and-redis.md](48-caching-and-redis.md) | 12 | 480 |
| 49 | 部署与 Docker | [49-deployment-and-docker.md](49-deployment-and-docker.md) | 12 | 490 |
| 50 | TCP/UDP 与套接字 | [50-tcp-udp-and-sockets.md](50-tcp-udp-and-sockets.md) | 12 | 500 |
| 51 | 性能剖析与基准 | [51-profiling-and-benchmarking.md](51-profiling-and-benchmarking.md) | 12 | 510 |
| 52 | HTTP 进阶与实时通信 | [52-http-advanced-and-realtime.md](52-http-advanced-and-realtime.md) | 12 | 520 |
| 53 | 消息队列与事件流 | [53-messaging-and-event-streams.md](53-messaging-and-event-streams.md) | 12 | 530 |
| 54 | 可观测性：指标与 OTel | [54-observability-metrics-and-otel.md](54-observability-metrics-and-otel.md) | 12 | 540 |

## New Topics Added

相较于旧版 `topics/`，重写时插入：`14`/`20`/`23`/`24`/`29`。

生态与工程追加：`36`–`54`（serde、IO、CLI、日志、HTTP、时间、正则、数据库、配置、gRPC、密码学、WASM、缓存/Redis、部署/Docker、TCP/UDP、剖析与基准、HTTP 进阶、消息队列、可观测性）。

## Validation Notes

`check_code.py --go` 的 skipped 主要来自 toml/bash、生态 crate 的 `text` 示意、stable/nightly 边界说明。

## Suggested Reading Order

1. `01-10`：工具链与语言基础
2. `11-20`：所有权到迭代器
3. `21-29`：工程化与并发
4. `30-35`：异步与高级类型 / unsafe
5. `36-54`：日常工程生态（序列化到可观测性）
