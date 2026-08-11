+++
title = "01-凭证提供者协议"
date = 2026-07-30T14:49:00+08:00
weight = 51
type = "docs"
description = "凭证提供者协议细节"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 凭证提供者协议 {#credential-provider-protocol}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/credential-provider-protocol.html](https://doc.rust-lang.org/cargo/reference/credential-provider-protocol.html)


本文档说明如何构建 Cargo 凭证提供者。关于设置或使用凭证提供者，见 [注册表认证](../../)。

使用外部凭证提供者时，Cargo 通过 stdin/stdout 以单行 JSON 消息与凭证提供者通信。

Cargo 总会以 `--cargo-plugin` 参数执行凭证提供者。这使得凭证提供者可执行文件可以具备超出 Cargo 所需的额外功能。额外参数通过 JSON 的 `args` 字段包含。

## JSON 消息 {#json-messages}
本文档中的 JSON 消息为便于阅读而添加了换行。
实际消息不得包含换行。

### Credential hello {#credential-hello}
* 发送方：凭证提供者
* 用途：在进程启动时标识所支持的协议
```javascript
{
    "v":[1]
}
```

Cargo 发送的请求会包含一个 `v` 字段，其值为此处列出的某个版本。
若 Cargo 不支持凭证提供者提供的任何版本，将报错并关闭凭证进程。

### 注册表信息 {#registry-information}
* 发送方：Cargo
本身不是独立消息。作为 `registry` 字段包含在 Cargo 发送的所有消息中。
```javascript
{
    // 注册表的索引 URL
    "index-url":"https://github.com/rust-lang/crates.io-index",
    // 配置中的注册表名称（可选）
    "name": "crates-io",
    // 尝试访问需认证注册表时收到的 HTTP 头（可选）
    "headers": ["WWW-Authenticate: cargo"]
}
```

### Login 请求 {#login-request}
* 发送方：Cargo
* 用途：收集并存储凭证
```javascript
{
    // 协议版本
    "v":1,
    // 要执行的操作：login
    "kind":"login",
    // 注册表信息（见「注册表信息」）
    "registry":{"index-url":"sparse+https://registry-url/index/", "name": "my-registry"},
    // 用户从 stdin 或命令行指定的 token（可选）
    "token": "<the token value>",
    // 用户可访问以获取 token 的 URL（可选）
    "login-url": "http://registry-url/login",
    // 额外的命令行参数（可选）
    "args":[]
}
```

若设置了 `token` 字段，凭证提供者应使用所提供的 token。若未设置 `token`，则凭证提供者应提示用户输入 token。

除配置中可能传给凭证提供者的参数外，`cargo login` 还支持通过 `cargo login -- <additional args>` 传递额外命令行参数。这些额外参数会排在 Cargo 配置中的参数之后，包含在 `args` 字段中。

### Read 请求 {#read-request}
* 发送方：Cargo
* 用途：获取用于读取 crate 信息的凭证
```javascript
{
    // 协议版本
    "v":1,
    // 请求种类：获取凭证
    "kind":"get",
    // 要执行的操作：读取 crate 信息
    "operation":"read",
    // 注册表信息（见「注册表信息」）
    "registry":{"index-url":"sparse+https://registry-url/index/", "name": "my-registry"},
    // 额外的命令行参数（可选）
    "args":[]
}
```

### Publish 请求 {#publish-request}
* 发送方：Cargo
* 用途：获取用于发布 crate 的凭证
```javascript
{
    // 协议版本
    "v":1,
    // 请求种类：获取凭证
    "kind":"get",
    // 要执行的操作：发布 crate
    "operation":"publish",
    // Crate 名称
    "name":"sample",
    // Crate 版本
    "vers":"0.1.0",
    // Crate 校验和
    "cksum":"...",
    // 注册表信息（见「注册表信息」）
    "registry":{"index-url":"sparse+https://registry-url/index/", "name": "my-registry"},
    // 额外的命令行参数（可选）
    "args":[]
}
```

### Get 成功响应 {#get-success-response}
* 发送方：凭证提供者
* 用途：将凭证交给 Cargo
```javascript
{"Ok":{
    // 响应种类：这是 get 请求
    "kind":"get",
    // 要发送给注册表的 token
    "token":"...",
    // 缓存控制。可为以下之一：
    // * "never"：不缓存
    // * "session"：缓存到当前 cargo 会话结束
    // * "expires"：缓存到过期（仍限于当前 cargo 会话）
    "cache":"expires",
    // Unix 时间戳（仅当 "cache": "expires" 时）
    "expiration":1693942857,
    // token 是否与操作无关？
    "operation_independent":true
}}
```

`token` 会作为 `Authorization` HTTP 头的值发送给注册表。

`operation_independent` 表示该 token 是否可跨不同操作（如发布或获取）缓存。一般应为 `true`，除非提供者希望生成限定于特定操作的 token。

### Login 成功响应 {#login-success-response}
* 发送方：凭证提供者
* 用途：表示登录成功
```javascript
{"Ok":{
    // 响应种类：这是 login 请求
    "kind":"login"
}}
```

### Logout 成功响应 {#logout-success-response}
* 发送方：凭证提供者
* 用途：表示登出成功
```javascript
{"Ok":{
    // 响应种类：这是 logout 请求
    "kind":"logout"
}}
```

### 失败响应（URL 不支持） {#failure-response-url-not-supported}
* 发送方：凭证提供者
* 用途：向 Cargo 提供错误信息
```javascript
{"Err":{
    "kind":"url-not-supported"
}}
```
若凭证提供者仅处理特定注册表 URL，而给定 URL 不受支持，则发送此响应。若有其他可用提供者，Cargo 将尝试下一个。

### 失败响应（未找到） {#failure-response-not-found}
* 发送方：凭证提供者
* 用途：向 Cargo 提供错误信息
```javascript
{"Err":{
    // 错误：在提供者中找不到凭证。
    "kind":"not-found"
}}
```
若找不到凭证则发送此响应。这对凭证不可用的 `get` 请求，或没有可清除内容的 `logout` 请求是预期行为。

### 失败响应（操作不支持） {#failure-response-operation-not-supported}
* 发送方：凭证提供者
* 用途：向 Cargo 提供错误信息
```javascript
{"Err":{
    // 错误：在提供者中找不到凭证。
    "kind":"operation-not-supported"
}}
```
若凭证提供者不支持所请求的操作则发送此响应。
若提供者仅支持 `get` 而收到 `login` 请求，应以此错误响应。

### 失败响应（其他） {#failure-response-other}
* 发送方：凭证提供者
* 用途：向 Cargo 提供错误信息
```javascript
{"Err":{
    // 错误：其他失败
    "kind":"other",
    // 要显示的错误消息字符串
    "message": "free form string error message",
    // 错误的详细因果链（可选）
    "caused-by": ["cause 1", "cause 2"]
}}
```

## 请求读取用 token 的通信示例： {#example-communication-to-request-a-token-for-reading}
1. Cargo 启动凭证进程，捕获 stdin 与 stdout。
2. 凭证进程向 Cargo 发送 Hello 消息
    ```javascript
    { "v": [1] }
   ```
3. Cargo 向凭证进程发送 CredentialRequest 消息（为便于阅读已添加换行）。
    ```javascript
    {
        "v": 1,
        "kind": "get",
        "operation": "read",
        "registry":{"index-url":"sparse+https://registry-url/index/"}
    }
    ```
4. 凭证进程向 Cargo 发送 CredentialResponse（为便于阅读已添加换行）。
    ```javascript
    {
        "token": "...",
        "cache": "session",
        "operation_independent": true
    }
    ```
5. Cargo 关闭通向凭证提供者的 stdin 管道，进程退出。
6. 在与该注册表交互时，Cargo 在会话剩余期间（直到 Cargo 退出）使用该 token。
