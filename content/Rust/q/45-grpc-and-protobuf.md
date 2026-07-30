+++
title = "45-grpc-and-protobuf"
date = 2026-07-28T14:49:00+08:00
weight = 450
type = "docs"
description = "面向 Go 用户讲清 tonic/prost、build.rs 生成、unary 与流式、Status 与 proto 兼容"
isCJKLanguage = true
draft = false

+++

# gRPC 与 Protobuf (gRPC and Protobuf)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**
- 你是否听说 Rust 做 gRPC 要用 tonic + prost，却分不清各自干什么、和 `protoc-gen-go` 怎么对照？
- 你是否不知道 `build.rs` 何时跑、生成代码放哪、客户端怎么 dial、服务端怎么挂 unary？
- 你是否纠结：流式 RPC、metadata/interceptor、`Status` 错误码、TLS vs 明文该怎么记？
- 你是否想知道：proto 怎么改才兼容、何时该 gRPC 而不是 HTTP+JSON、workspace 里 proto 怎么摆？

**术语速查表：**
| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| gRPC | gRPC Remote Procedure Calls | 远程过程调用框架 | 基于 HTTP/2 + Protobuf 的 RPC | 同名 `google.golang.org/grpc` |
| Protobuf | Protocol Buffers | 协议缓冲区 | 接口与消息的 IDL + 二进制编码 | `protobuf` / `protoc` |
| `.proto` | — | 接口描述文件 | 定义 `service` / `message` | 同左 |
| **tonic** | — | Rust gRPC 框架 | 基于 hyper/tower 的 async gRPC | `google.golang.org/grpc` |
| **prost** | — | Rust Protobuf 编解码 | 把 `.proto` 生成 Rust 结构体与编解码 | `protobuf` / `protoimpl` |
| `build.rs` | — | Cargo 构建脚本 | 编译前跑，常用来调代码生成 | `go generate` / 插件生成 |
| unary | — | 一元 RPC | 一请求一响应 | 普通 `rpc Foo(Req) returns (Resp)` |
| streaming | — | 流式 RPC | 客户端/服务端/双向持续发消息 | stream 关键字 |
| metadata | — | 元数据 | 类似 HTTP Header 的键值对 | `metadata.MD` |
| interceptor | — | 拦截器 | 包在调用前后的横切逻辑 | unary/stream interceptor |
| Status | — | gRPC 状态 | 错误码 + 可选 message / details | `status.Status` / `codes.Code` |
| TLS | Transport Layer Security | 传输层安全 | 加密与身份校验的传输 | 同概念 |
| IDL | Interface Definition Language | 接口定义语言 | 用 `.proto` 描述契约 | 同概念 |
| codegen | code generation | 代码生成 | 从 `.proto` 生成语言绑定 | `protoc-gen-go` 等 |
| deadline / timeout | — | 截止时间/超时 | 客户端限制本次 RPC 最长等待 | `context.WithTimeout` |
| health check | — | 健康检查 | 标准健康探活服务，供编排/负载均衡探测 | `grpc_health_v1` |
| reflection | server reflection | 服务反射 | 运行时暴露服务描述，便于 grpcurl 等无本地 proto 调试 | gRPC reflection |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**
| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q8](#q8), [Q11](#q11) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q9](#q9), [Q10](#q10), [Q12](#q12), [Q13](#q13) |
| `occasional` | [Q14](#q14) |
| `advanced` | — |

---

## Q1. 为什么 Rust 生态常用 tonic + prost，而不是自己手写 Protobuf？ {#q1}
**Tags:** `hot` `beginner` `tonic` `prost` `gRPC`
**适用版本:** tonic 0.12+ / prost 0.13+（以 crates.io 当前稳定组合为准）

**一句话答案：**
**tonic** 管 gRPC 传输与服务/客户端骨架；**prost** 管 `.proto` → Rust 类型与编解码。两者分工清晰、跟 Tokio/tower 生态对齐，是当前事实上的默认组合——不必也不该从零手写 wire 格式。

**解答：**
职责表：

| 层 | crate | 干什么 |
|----|-------|--------|
| 消息编解码 | prost | `message` → `struct` + encode/decode |
| gRPC 运行时 | tonic | HTTP/2、`service` trait、客户端 stub、Status |
| 代码生成胶水 | tonic-build / prost-build | 在 `build.rs` 里读 `.proto` 生成 Rust |

依赖示意：

```toml
[dependencies]
tonic = "0.12"
prost = "0.13"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }

[build-dependencies]
tonic-build = "0.12"
```

心智模型（对照 Go）：

```text
.go 侧：protoc + protoc-gen-go + protoc-gen-go-grpc  →  *.pb.go
.rs 侧：build.rs + tonic-build（内部用 prost）       →  OUT_DIR 里的 .rs
```

手写 Protobuf 只在极少数「超小、固定、无演进」场景有意义；一有 `service`、字段演进、多语言互通，就走 `.proto` + 生成。

**Go 对比：**
- **Go 怎么做**：`protoc-gen-go` / `protoc-gen-go-grpc`（或 buf）生成，再 `grpc.NewServer`。
- **Rust 为什么不同**：同样是 codegen，只是生成挂在 Cargo `build.rs`，运行时选 tonic。
- **Go 程序员易踩的坑**：在 Rust 里找「官方 std gRPC」——没有；选 tonic+prost 即可。

**记忆点：**
- prost = 消息；tonic = RPC。
- 默认栈：tonic + prost + tonic-build。

---

## Q2. `build.rs` 怎么从 `.proto` 生成代码？生成物在哪？ {#q2}
**Tags:** `hot` `build.rs` `tonic-build` `codegen`
**适用版本:** tonic-build 0.12+；Cargo build script

**一句话答案：**
在 `build.rs` 里调 `tonic_build::compile_protos("proto/hello.proto")`（或 `configure().compile_protos(...)`）；Cargo 编译前跑它，生成文件进 `OUT_DIR`，业务代码用 `include!(concat!(env!("OUT_DIR"), "/....rs"))` 或 tonic 生成的 `include_proto!` 接入。

**解答：**
最小 `build.rs`：

```text
fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::compile_protos("proto/hello.proto")?;
    // 让 Cargo 在 proto 变更时重跑
    println!("cargo:rerun-if-changed=proto/hello.proto");
    Ok(())
}
```

对应 `.proto`：

```text
syntax = "proto3";
package hello;

service Greeter {
  rpc SayHello (HelloRequest) returns (HelloReply);
}

message HelloRequest { string name = 1; }
message HelloReply { string message = 1; }
```

在 `lib.rs` / `main.rs` 接入（示意）：

```text
pub mod hello {
    tonic::include_proto!("hello"); // package 名
}
```

要点：
- 生成物**默认不进** `src/`，而在 `target/.../out/`（`OUT_DIR`），避免手改生成代码。
- proto 路径相对 **crate 根**（有 `Cargo.toml` 的目录）。
- 改 `.proto` 必须让 build script 重跑：`rerun-if-changed` 或依赖文件列表。

**Go 对比：**
```go
//go:generate protoc --go_out=. --go-grpc_out=. hello.proto
```
- **Go 怎么做**：常把 `*.pb.go` 提交进仓库，或 CI/`go generate` 产出。
- **Rust 为什么不同**：习惯编译期生成进 `OUT_DIR`，不强制提交生成文件。
- **Go 程序员易踩的坑**：在 `src/` 里找 `hello.rs` 找不到——去 `include_proto!` / `OUT_DIR`。

**记忆点：**
- 生成 = `build.rs` + tonic-build。
- 使用 = `tonic::include_proto!("package")`。

---

## Q3. 最小 unary 服务端怎么写？ {#q3}
**Tags:** `hot` `server` `unary` `tonic`
**适用版本:** tonic 0.12+；tokio 1.x

**一句话答案：**
实现生成出来的 `Greeter` trait（方法返回 `Result<Response<Reply>, Status>`），再 `Server::builder().add_service(...).serve(addr).await`。**unary**（一元 RPC）就是一请求一响应，对标 Go 普通非 stream 方法。

**解答：**

```toml
[dependencies]
tonic = "0.12"
prost = "0.13"
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
```

服务端骨架（text，需先 codegen）：

```text
use tonic::{transport::Server, Request, Response, Status};
use hello::greeter_server::{Greeter, GreeterServer};
use hello::{HelloReply, HelloRequest};

pub struct MyGreeter;

#[tonic::async_trait]
impl Greeter for MyGreeter {
    async fn say_hello(
        &self,
        request: Request<HelloRequest>,
    ) -> Result<Response<HelloReply>, Status> {
        let name = request.into_inner().name;
        Ok(Response::new(HelloReply {
            message: format!("hello {name}"),
        }))
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let addr = "127.0.0.1:50051".parse()?;
    Server::builder()
        .add_service(GreeterServer::new(MyGreeter))
        .serve(addr)
        .await?;
    Ok(())
}
```

流程：listen → 解码请求 → 调你的 impl → 编码响应 / 或返回 `Status`。

**Go 对比：**
```go
type server struct{ hellopb.UnimplementedGreeterServer }
func (s *server) SayHello(ctx context.Context, in *hellopb.HelloRequest) (*hellopb.HelloReply, error) {
    return &hellopb.HelloReply{Message: "hello " + in.Name}, nil
}
grpc.NewServer() // + RegisterGreeterServer + Serve
```
- **Go 怎么做**：嵌未实现基类 + `RegisterXxxServer`。
- **Rust 为什么不同**：实现 trait + `XxxServer::new` 挂到 tonic `Server`。
- **Go 程序员易踩的坑**：忘 `#[tonic::async_trait]`，trait 方法签名对不上。

**记忆点：**
- impl 生成 trait → `add_service` → `serve`。
- 失败用 `Status`，成功用 `Response::new`。

---

## Q4. 客户端怎么 dial / 调 unary？ {#q4}
**Tags:** `hot` `client` `Channel` `dial`
**适用版本:** tonic 0.12+

**一句话答案：**
用 `XxxClient::connect("http://127.0.0.1:50051").await`（或先建 `Channel` 再 `new`）拿到客户端，再 `client.say_hello(Request::new(...)).await`。对标 Go 的 `grpc.Dial` + 生成的 `NewXxxClient`。

**解答：**

```text
use hello::greeter_client::GreeterClient;
use hello::HelloRequest;
use tonic::Request;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut client = GreeterClient::connect("http://127.0.0.1:50051").await?;

    let resp = client
        .say_hello(Request::new(HelloRequest {
            name: "world".into(),
        }))
        .await?
        .into_inner();

    println!("{}", resp.message);
    Ok(())
}
```

常见变体：

```text
use tonic::transport::Channel;

let channel = Channel::from_static("http://127.0.0.1:50051")
    .connect()
    .await?;
let mut client = GreeterClient::new(channel);
```

注意：
- 明文开发常用 `http://`；生产 TLS 见 [Q9](#q9)。
- `connect` 失败是传输层错误；RPC 业务失败多在返回的 `Err(Status)`。
- 复用同一个 `Channel` / client（内部可克隆）比每次新建更省。

**Go 对比：**
```go
conn, err := grpc.Dial("127.0.0.1:50051", grpc.WithInsecure())
c := hellopb.NewGreeterClient(conn)
reply, err := c.SayHello(ctx, &hellopb.HelloRequest{Name: "world"})
```
- **Go 怎么做**：`Dial` + `NewXxxClient` + 调方法。
- **Rust 为什么不同**：`connect`/`Channel` + 生成的 `XxxClient`，全是 async。
- **Go 程序员易踩的坑**：写成阻塞式调用、或地址漏了 scheme（`http://`）。

**记忆点：**
- dial ≈ `connect` / `Channel::connect`。
- 调完 `.await?`，再用 `.into_inner()` 取消息。

---

## Q5. 和 Go 的生成物怎么对照？ {#q5}
**Tags:** `common` `codegen` `Go` `对照`
**适用版本:** 概念对照；与具体插件版本无关

**一句话答案：**
Go 的 `XxxClient` / `XxxServer` / `UnimplementedXxxServer` / `RegisterXxxServer`，在 Rust 里对应 tonic 生成的 `xxx_client::XxxClient`、`xxx_server::Xxx` trait + `XxxServer`；消息类型两边都是 `message` 生成的结构体，只是 Rust 用 prost 字段类型（`String`、`i32`、`Option<...>` 等）。

**解答：**
对照表：

| Go 生成物 | Rust（tonic/prost） |
|-----------|---------------------|
| `HelloRequest` struct | `HelloRequest` struct（prost） |
| `GreeterClient` | `greeter_client::GreeterClient` |
| `GreeterServer` 接口 | `greeter_server::Greeter` trait |
| `RegisterGreeterServer` | `GreeterServer::new(impl)` + `add_service` |
| `UnimplementedGreeterServer` | 实现 trait 时必须写全方法（或看生成辅助） |
| `status.Error(codes.X, msg)` | `Status::new(Code::X, msg)` |

消息字段习惯差异：

```text
// proto: optional string nickname = 2; 或 proto3 隐式
// Go:    GetNickname() string / 指针视生成选项
// Rust:  常为 Option<String> 或 String（取决于 proto/字段规则与配置）
```

包名：`package hello;` → Rust 模块常通过 `include_proto!("hello")` 引入；Go 则是 `option go_package`。

**Go 对比：**
- **Go 怎么做**：生成文件进 package，直接 `import`。
- **Rust 为什么不同**：生成在 `OUT_DIR`，用宏/include 挂进你的模块树。
- **Go 程序员易踩的坑**：找 `RegisterGreeterServer` 函数——tonic 是 `add_service(GreeterServer::new(...))`。

**记忆点：**
- Client/Server 名字两边都在，挂载方式不同。
- 字段空值语义看 prost 生成类型，别假设和 Go getter 一模一样。

---

## Q6. 流式 RPC 该怎么建立直觉？ {#q6}
**Tags:** `common` `streaming` `Stream`
**适用版本:** tonic 0.12+（streaming API）

**一句话答案：**
四种形态：unary、server streaming、client streaming、bidi。Rust 里流多半是 `Stream`/`ReceiverStream` 一类异步流；服务端方法签名会变成「返回流」或「接收流」，而不是单个 `Request<T>`/`Response<T>`。

**解答：**
直觉表：

| 种类 | proto | 心智 |
|------|-------|------|
| unary | `rpc Foo(Req) returns (Resp)` | 一次来回 |
| server stream | `returns (stream Resp)` | 请求一次，响应多条 |
| client stream | `rpc Foo(stream Req) returns (Resp)` | 请求多条，响应一次 |
| bidi | `stream` 两边都有 | 两边都能持续发 |

服务端 server-streaming 示意（签名级，非完整程序）：

```text
// 生成 trait 方法大致形如：
// type SayHelloStream = Pin<Box<dyn Stream<Item = Result<HelloReply, Status>> + Send>>;
// async fn say_hello_stream(&self, request: Request<HelloRequest>)
//     -> Result<Response<Self::SayHelloStream>, Status>;
```

客户端读流：对返回的 stream 做 `while let Some(item) = stream.next().await`。

和 HTTP+JSON「自己 chunk 响应」不同：gRPC 流有帧协议与 `Status` 收尾；半开/取消要和 `context`/`CancellationToken` 一起想。

**Go 对比：**
```go
stream, err := c.Foo(ctx)
for {
    msg, err := stream.Recv()
    // ...
}
```
- **Go 怎么做**：`Send`/`Recv` 循环。
- **Rust 为什么不同**：偏 `Stream` + `.await`；类型在生成 trait 的 associated type 上。
- **Go 程序员易踩的坑**：把流当成「普通 Vec 一次性返回」——背压与取消语义会丢。

**记忆点：**
- 先分清四种 RPC，再记 API 名。
- 流 = 异步 `Stream`，不是 `Vec`。

---

## Q7. metadata 和 interceptor 怎么用？ {#q7}
**Tags:** `common` `metadata` `interceptor` `auth`
**适用版本:** tonic 0.12+

**一句话答案：**
**metadata** 像 HTTP Header：用 `request.metadata()` / `MetadataMap` 读写；**interceptor** 在调用前后统一插逻辑（鉴权、日志、trace），对标 Go 的 interceptor，底层常落在 tower `Layer`/`Service` 上。

**解答：**
客户端塞 metadata：

```text
use tonic::metadata::MetadataValue;
use tonic::Request;

let mut req = Request::new(HelloRequest { name: "a".into() });
req.metadata_mut().insert(
    "authorization",
    MetadataValue::from_str("Bearer TOKEN")?,
);
```

服务端读：

```text
let auth = request.metadata().get("authorization");
```

拦截器直觉（示意）：

```text
// 客户端：带拦截器的 Channel / with_interceptor
// 服务端：ServiceBuilder / interceptor 包一层，校验 metadata 再放行
// 失败：return Err(Status::unauthenticated("missing token"));
```

适合放 interceptor 的：鉴权、deadline 透传、请求日志、trace id。业务分支仍放在具体 RPC 方法里。

**Go 对比：**
```go
md := metadata.Pairs("authorization", "Bearer TOKEN")
ctx := metadata.NewOutgoingContext(ctx, md)
```
- **Go 怎么做**：`metadata` + unary/stream interceptor。
- **Rust 为什么不同**：API 名不同，但「Header + 中间件」模型一致；常接 tower。
- **Go 程序员易踩的坑**：把业务错误塞进 metadata 当主通道——主结果仍应是消息或 `Status`。

**记忆点：**
- 凭证/trace → metadata。
- 横切 → interceptor；业务 → 方法体。

---

## Q8. `Status` 和错误码怎么用？ {#q8}
**Tags:** `hot` `Status` `Code` `error`
**适用版本:** tonic 0.12+（`tonic::Status` / `Code`）

**一句话答案：**
RPC 失败返回 `Err(Status::new(Code::..., "message"))`（或 `Status::not_found(...)` 等助手）；成功才 `Ok(Response::new(...))`。对标 Go 的 `status.Error(codes.NotFound, ...)`——不要用「随便一个 String」当 gRPC 错误协议。

**解答：**

```text
use tonic::{Code, Status};

fn reject_empty(name: &str) -> Result<(), Status> {
    if name.is_empty() {
        return Err(Status::invalid_argument("name is empty"));
    }
    Ok(())
}

// 等价：
// Err(Status::new(Code::InvalidArgument, "name is empty"))
```

常见码（记语义，不必背全表）：

| Code | 典型场景 |
|------|----------|
| `Ok` | 成功（通常不必手动返回） |
| `InvalidArgument` | 参数不合法 |
| `NotFound` | 资源不存在 |
| `AlreadyExists` | 冲突创建 |
| `PermissionDenied` / `Unauthenticated` | 鉴权/认证 |
| `Unavailable` | 过载/依赖暂时不可用 |
| `Internal` | 未预期的服务端错误 |

客户端：

```text
match client.say_hello(req).await {
    Ok(resp) => { /* resp.into_inner() */ }
    Err(status) => {
        eprintln!("code={:?} msg={}", status.code(), status.message());
    }
}
```

**Go 对比：**
```go
return nil, status.Error(codes.InvalidArgument, "name is empty")
```
- **Go 怎么做**：`google.golang.org/grpc/status` + `codes`。
- **Rust 为什么不同**：同模型，类型在 `tonic::Status`。
- **Go 程序员易踩的坑**：`Err` 里塞 anyhow 字符串却不转 `Status`——客户端看不到标准 code。

**记忆点：**
- 失败 = `Status` + `Code`。
- 先选对 code，再写给人看的 message。

---

## Q9. TLS 和明文传输怎么选？ {#q9}
**Tags:** `common` `TLS` `plaintext` `security`
**适用版本:** tonic transport；tls feature 视版本开启

**一句话答案：**
本地开发可以明文（`http://` + 无 TLS）；生产默认 TLS（证书、可选 mTLS）。tonic 用 `ServerTlsConfig` / `ClientTlsConfig`（需打开相应 feature）；不要把开发期 `WithInsecure` 习惯直接带进生产。

**解答：**

```text
// 开发：明文
GreeterClient::connect("http://127.0.0.1:50051").await?;
Server::builder().add_service(...).serve(addr).await?;
```

```toml
# 生产常需打开 tls 相关 feature（名称以当前 tonic 文档为准）
tonic = { version = "0.12", features = ["tls"] }
```

TLS 直觉（示意）：

```text
// 服务端：Server::builder().tls_config(ServerTlsConfig::new().identity(...))?
// 客户端：Endpoint::from_static("https://...").tls_config(ClientTlsConfig::new()....)?
```

选型：
- 本机 / docker 内网联调：明文可接受，但别暴露到公网。
- 跨主机、公网、合规：TLS；服务间常再加 mTLS 或网格发证。
- 负载均衡 / 网关终结 TLS 时，后端是否明文由威胁模型决定。

**Go 对比：**
```go
grpc.WithTransportCredentials(insecure.NewCredentials()) // 仅开发
credentials.NewClientTLSFromFile(...)                    // 生产
```
- **Go 怎么做**：Dial option 选 insecure vs TLS credentials。
- **Rust 为什么不同**：同样分明文 URL 与 `tls_config`；feature 要记得开。
- **Go 程序员易踩的坑**：生产仍 `http://` + 无 TLS；或证书路径/SNI 配错。

**记忆点：**
- 开发明文、生产 TLS。
- 证书与 feature 配齐再 `serve`/`connect`。

---

## Q10. proto 怎么演进才兼容？ {#q10}
**Tags:** `common` `protobuf` `compatibility` `evolution`
**适用版本:** proto3 惯例；与语言无关的规则

**一句话答案：**
**不要改已发布字段的编号与类型**；新增字段用新 number；废弃用 `deprecated` / 保留号；未知字段要能被老/新实现安全忽略。破坏性改动（删字段号再利用、改类型）会静默坏数据。

**解答：**
安全：

```text
message User {
  string name = 1;
  string email = 2;           // 新增：新号
  reserved 3;                 // 删除过的号要 reserved
  reserved "old_nickname";
}
```

危险：

```text
// 把 field 2 从 string 改成 int64 —— wire 上可能解成乱数据
// 删掉 field 2 后又用 2 表示别的意思 —— 新旧客户端互炸
```

规则摘要：
- 字段号是契约，比字段名更重要。
- `optional` / `repeated` 变更要谨慎，读写双方都要理解。
- 枚举只追加，别改已有值含义。
- 先扩后缩：先部署能忽略新字段的一方，再写新字段。

**Go 对比：**
- **Go 怎么做**：同一套 Protobuf 兼容规则；和语言无关。
- **Rust 为什么不同**：无差别——prost/tonic 不替你保证演进策略。
- **Go 程序员易踩的坑**：以为「只在 Rust 侧改 struct」就行——真正契约在 `.proto`。

**记忆点：**
- 新字段新号；旧号不复用。
- 类型与号一旦发布就冻结。

---

## Q11. 什么时候用 gRPC，什么时候用 HTTP + JSON？ {#q11}
**Tags:** `hot` `architecture` `JSON` `选型`
**适用版本:** 架构选型；与具体版本无关

**一句话答案：**
服务间、强契约、要流式/多语言 codegen、在意二进制与 HTTP/2 多路复用 → 倾向 gRPC；浏览器优先、对外公共 API、需要随手 curl/JSON 调试 → 倾向 HTTP+JSON（axum/reqwest 那套）。很多系统对外 JSON、对内 gRPC。

**解答：**

| 维度 | gRPC + Protobuf | HTTP + JSON |
|------|-----------------|-------------|
| 契约 | `.proto` 强类型 | OpenAPI / 手写 struct |
| 浏览器 | 需 grpc-web 或网关 | 天生友好 |
| 调试 | grpcurl / 反射 | curl / 浏览器 |
| 流式 | 一等公民 | SSE/WebSocket 等另拼 |
| 生态学习点 | tonic/prost/build.rs | 见 [40-http](../40-http-client-and-server/) |

```text
// 对内：settlement.v1.Billing/Charge  —— gRPC
// 对外：POST /api/v1/charges         —— JSON
```

别为了「时髦」把所有 CRUD 都上 gRPC；也别在低延迟、多语言内部网格里死守手写 JSON。

**Go 对比：**
- **Go 怎么做**：同样纠结；内部常 gRPC，网关转 REST。
- **Rust 为什么不同**：选型逻辑相同；只是栈变成 tonic vs axum。
- **Go 程序员易踩的坑**：以为 Rust 只能选一个——可以并存。

**记忆点：**
- 对内强契约 / 流式 → gRPC。
- 对外浏览器 / 易调试 → HTTP+JSON。

---

## Q12. workspace 里 proto 怎么组织比较干净？ {#q12}
**Tags:** `common` `workspace` `proto` `layout`
**适用版本:** Cargo workspace；tonic-build

**一句话答案：**
常见两种：**独立 `proto` / `api` crate** 只放 `.proto` + `build.rs` + 生成模块，业务 crate 依赖它；或每个服务 crate 自带 `proto/`。多服务共享消息时，优先「一个 api crate」，避免每人生成一份互相漂。

**解答：**
推荐布局：

```text
workspace/
  Cargo.toml                 # members = ["api", "greeter", "client"]
  api/
    Cargo.toml               # tonic/prost + build-dependencies tonic-build
    build.rs
    proto/
      hello/v1/hello.proto
    src/lib.rs               # include_proto! / 再导出
  greeter/                   # 依赖 api，只写业务 impl
  client/                    # 依赖 api，只写调用
```

`api` 的 `lib.rs` 示意：

```text
pub mod hello {
    tonic::include_proto!("hello");
}
```

原则：
- `.proto` 单一来源（single source of truth）。
- 生成代码只在一处编译，版本锁定在一个 crate。
- breaking change 跟 api crate 的 semver 走。
- buf/lint 一类工具可放在仓库根，与语言无关。

**Go 对比：**
```text
// 类似：单独 module 放 api/hello/v1 ；业务服务 import 该 module
```
- **Go 怎么做**：独立 `api` module + 生成 Go 代码常提交或统一 generate。
- **Rust 为什么不同**：用 workspace member crate 承接 `build.rs`，依赖图更清晰。
- **Go 程序员易踩的坑**：每个二进制复制一份 `.proto` 各自 `compile_protos`——字段一漂就灾难。

**记忆点：**
- 共享契约 → 独立 api crate。
- 业务 crate 只依赖，不各自偷偷生成。

---

## Q13. deadline / timeout 在 tonic 客户端怎么设？ {#q13}
**Tags:** `common` `timeout` `deadline` `client`
**适用版本:** tonic 0.12+；tokio 1.x

**一句话答案：**
单次 RPC：给 **`Request` 设 `timeout`**（tonic 会据此发 gRPC 截止时间）；整条连接/通道：在 **`Channel` 上挂 tower timeout**；再外层还可用 `tokio::time::timeout` 包住 `.await`。对标 Go 的 `context.WithTimeout`——要显式设，默认不会「随便帮你 几秒就断」。

**解答：**

```toml
[dependencies]
tonic = "0.12"
tokio = { version = "1", features = ["macros", "rt-multi-thread", "time"] }
```

按请求设超时（最常用）：

```text
use std::time::Duration;
use tonic::Request;

let mut request = Request::new(HelloRequest {
    name: "world".into(),
});
request.set_timeout(Duration::from_secs(3));

let resp = client.say_hello(request).await?;
```

通道级超时（该 client 上每次调用都受影响，示意）：

```text
use std::time::Duration;
use tonic::transport::Channel;

let channel = Channel::from_static("http://127.0.0.1:50051")
    .timeout(Duration::from_secs(5))
    .connect()
    .await?;
let mut client = GreeterClient::new(channel);
```

外层再包一层（防「连接挂起」等）：

```text
use tokio::time::{timeout, Duration};

let fut = client.say_hello(Request::new(HelloRequest {
    name: "world".into(),
}));
match timeout(Duration::from_secs(3), fut).await {
    Ok(Ok(resp)) => println!("{}", resp.into_inner().message),
    Ok(Err(status)) => eprintln!("rpc: {status}"),
    Err(_) => eprintln!("client-side timeout"),
}
```

超时后客户端多看到 `Status` 的 `DeadlineExceeded` / 传输错误；服务端若尊重 deadline，应尽快停工（别无视取消还硬算）。异步取消心智见 [31-async](../31-async-programming/)。

**Go 对比：**
```go
ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
defer cancel()
resp, err := client.SayHello(ctx, req)
```
- **Go 怎么做**：几乎总是 `context` 带 deadline。
- **Rust 为什么不同**：tonic 用 `Request::set_timeout` / tower 层；没有每个函数必传的 `Context` 参数。
- **Go 程序员易踩的坑**：假设「没设超时也有默认 几秒」——没有；慢调用会一直挂。

**记忆点：**
- 单次调用 → `request.set_timeout`。
- 通道默认 → `Channel::timeout`；再加 `tokio::time::timeout` 作保险。

---

## Q14. health check / 反射要不要一上来就上？ {#q14}
**Tags:** `occasional` `health` `reflection` `ops`
**适用版本:** tonic 生态（`tonic-health` / `tonic-reflection`）；非 Hello World 必选项

**一句话答案：**
**不必**一上来就装。本地把 unary 跑通（[Q3](#q3)/[Q4](#q4)）优先；上 **K8s/负载均衡探活** 再加 **health check**；要用 **grpcurl** 且不想分发 `.proto` 再加 **reflection**。生产反射常只开内网或关掉。

**解答：**
分工：

| 能力 | 干什么 | 什么时候加 |
|------|--------|------------|
| health（`grpc.health.v1`） | 标准探活：serving / not serving | 编排 readiness/liveness、LB |
| reflection | 运行时暴露服务描述 | 调试、grpcurl 无本地 proto |
| 业务服务 | 真正 RPC | 第一天就要 |

挂载示意（text，依赖另加）：

```toml
[dependencies]
tonic-health = "0.12"
tonic-reflection = "0.12"
```

```text
// 示意：Server::builder()
//   .add_service(health_service)
//   .add_service(reflection_service) // 仅开发/内网
//   .add_service(GreeterServer::new(...))
//   .serve(addr)
```

建议节奏：

1. 先契约 + unary/流式 + `Status`（本篇前几题）。
2. 部署到有探针的环境 → `tonic-health`，并把业务「依赖库/下游挂了」反映到 not serving。
3. 调试体验不够 → 开发 profile 开 reflection；对外默认关。

别把 reflection 当成「可以不写 `.proto` 的借口」——契约仍在 proto；反射只是运维/调试便利。

**Go 对比：**
- **Go 怎么做**：同样常挂 `grpc_health_v1` 与 reflection 插件；生产多关反射。
- **Rust 为什么不同**：换成 `tonic-health` / `tonic-reflection`，时机判断相同。
- **Go 程序员易踩的坑**：教程一抄就把反射暴露到公网。

**记忆点：**
- Hello World 不需要 health/反射。
- 探活 → health；无 proto 调试 → reflection（慎对公网）。
