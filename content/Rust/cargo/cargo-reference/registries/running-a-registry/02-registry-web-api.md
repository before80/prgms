+++
title = "02-注册表 Web API"
date = 2026-07-30T14:49:00+08:00
weight = 54
type = "docs"
description = "注册表 HTTP API 协议"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# Web API {#web-api}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/registry-web-api.html](https://doc.rust-lang.org/cargo/reference/registry-web-api.html)


注册表可在 `config.json` 中定义的位置托管 Web API，以支持下列任一操作。

对于需要认证的请求，Cargo 会包含 `Authorization` 头。头值为 API token。若 token 无效，服务器应以 403 响应码回应。用户应访问注册表网站获取 token，Cargo 可用 [`cargo login`] 命令存储 token，或在命令行上传入 token。

成功响应使用 2xx 响应码。
错误应使用适当的响应码，如 404。
失败响应应具有如下结构的 JSON 对象：

```javascript
{
    // 向用户显示的错误数组。
    "errors": [
        {
            // 作为字符串的错误消息。
            "detail": "error message text"
        }
    ]
}
```

若响应具有此结构，即使响应码为 200，Cargo 也会向用户显示详细消息。
若响应码表示错误且内容不具有此结构，Cargo 会向用户显示旨在帮助调试服务器错误的消息。服务器返回 `errors` 对象可让注册表提供更详细或以用户为中心的错误消息。

为保持向后兼容，服务器应忽略任何意外的查询参数或 JSON 字段。若缺少 JSON 字段，应假定其为 null。端点以路径中的 `v1` 组件进行版本控制，若将来需要任何向后兼容回退，由 Cargo 负责处理。

Cargo 为所有请求将 `User-Agent` 头设为 Cargo 版本，例如 `cargo/1.32.0 (8610973aa 2019-01-02)`。用户可在配置值中修改此设置。添加于 1.29。

其他头因端点而异，见下文文档。

## 发布（Publish） {#publish}
- 端点：`/api/v1/crates/new`
- 方法：PUT
- 认证：包含
- 头：
    - `Content-Type`：`application/octet-stream`
    - `Accept`：`application/json`
- 正文：包含（见下文）

发布端点用于发布 crate 的新版本。服务器应验证 crate、使其可供下载，并将其加入索引。

不要求在发送成功响应之前更新索引。
成功响应后，Cargo 会在短时间内轮询索引，以确认新 crate 已加入。
若短时间后 crate 仍未出现在索引中，Cargo 会显示警告，告知用户新 crate 尚不可用。

Cargo 发送的数据正文为：

- 表示 JSON 数据长度的 32 位无符号小端整数。
- 作为 JSON 对象的包元数据。
- 表示 `.crate` 文件长度的 32 位无符号小端整数。
- `.crate` 文件。

以下是带注释的 JSON 对象示例。其中包含 [crates.io] 施加的一些限制说明，仅用于说明可能进行的验证类型，不应视为 [crates.io] 所施加限制的穷尽列表。

```javascript
{
    // 包的名称。
    "name": "foo",
    // 正在发布的包版本。
    "vers": "0.1.0",
    // 包的直接依赖数组。
    "deps": [
        {
            // 依赖的名称。
            // 若依赖从原始包名重命名，
            // 这是原始名称。新包名存放在
            // `explicit_name_in_toml` 字段中。
            "name": "rand",
            // 此依赖的 semver 需求。
            "version_req": "^0.6",
            // 为此依赖启用的特性（字符串）数组。
            "features": ["i128_support"],
            // 是否为可选依赖的布尔值。
            "optional": false,
            // 是否启用默认特性的布尔值。
            "default_features": true,
            // 依赖的目标平台。
            // 若不是目标依赖则为 null。
            // 否则为字符串，如 "cfg(windows)"。
            "target": null,
            // 依赖种类。
            // "dev"、"build" 或 "normal"。
            "kind": "normal",
            // 此依赖所在注册表索引的 URL，以字符串表示。
            // 若未指定或为 null，则假定依赖在当前注册表中。
            "registry": null,
            // 若依赖已重命名，这是新包名的字符串。
            // 若未指定或为 null，则此依赖未重命名。
            "explicit_name_in_toml": null,
        }
    ],
    // 为包定义的特性集合。
    // 每个特性映射到它启用的特性或依赖数组。
    // Cargo 不对特性名称施加限制，但 crates.io
    // 要求字母数字 ASCII、`_` 或 `-` 字符。
    "features": {
        "extras": ["rand/simd_support"]
    },
    // 作者字符串列表。
    // 可为空。
    "authors": ["Alice <a@example.com>"],
    // 清单中的 description 字段。
    // 可为 null。crates.io 要求至少有一些内容。
    "description": null,
    // 指向此包文档网站的 URL 字符串。
    // 可为 null。
    "documentation": null,
    // 指向此包主页网站的 URL 字符串。
    // 可为 null。
    "homepage": null,
    // README 文件内容的字符串。
    // 可为 null。
    "readme": null,
    // crate 中 README 文件的相对路径字符串。
    // 可为 null。
    "readme_file": null,
    // 包的关键词字符串数组。
    "keywords": [],
    // 包的分类字符串数组。
    "categories": [],
    // 包的许可证字符串。
    // 可为 null。crates.io 要求设置 `license` 或 `license_file`。
    "license": null,
    // crate 中许可证文件的相对路径字符串。
    // 可为 null。
    "license_file": null,
    // 指向此包源码仓库网站的 URL 字符串。
    // 可为 null。
    "repository": null,
    // 「状态」徽章的可选对象。每个值是任意字符串到字符串映射的对象。
    // crates.io 对徽章格式有特殊解释。
    "badges": {
        "travis-ci": {
            "branch": "master",
            "repository": "rust-lang/cargo"
        }
    },
    // 包清单中的 `links` 字符串值，未指定则为 null。
    // 此字段可选，默认为 null。
    "links": null,
    // 最低支持的 Rust 版本（可选）
    // 必须是不带运算符的有效版本需求（例如不能有 `=`）
    "rust_version": null
}
```

成功响应包含如下 JSON 对象：

```javascript
{
    // 向用户显示的警告的可选对象。
    "warnings": {
        // 无效并被忽略的分类字符串数组。
        "invalid_categories": [],
        // 无效并被忽略的徽章名称字符串数组。
        "invalid_badges": [],
        // 向用户显示的任意警告字符串数组。
        "other": []
    }
}
```

## Yank {#yank}
- 端点：`/api/v1/crates/{crate_name}/{version}/yank`
- 方法：DELETE
- 认证：包含
- 头：
    - `Accept`：`application/json`
- 正文：无

yank 端点会将给定 crate 版本在索引中的 `yank` 字段设为 `true`。

成功响应包含如下 JSON 对象：

```javascript
{
    // 表示 yank 成功，始终为 true。
    "ok": true,
}
```

## Unyank {#unyank}
- 端点：`/api/v1/crates/{crate_name}/{version}/unyank`
- 方法：PUT
- 认证：包含
- 头：
    - `Accept`：`application/json`
- 正文：无

unyank 端点会将给定 crate 版本在索引中的 `yank` 字段设为 `false`。

成功响应包含如下 JSON 对象：

```javascript
{
    // 表示 unyank 成功，始终为 true。
    "ok": true,
}
```

## 所有者（Owners） {#owners}
Cargo 本身没有用户与所有者的固有概念，但它提供 `owner` 命令以协助管理谁有权控制 crate。具体如何处理用户与所有者由注册表决定。关于 [crates.io] 如何通过 GitHub 用户与团队处理所有者，见[发布文档][publishing documentation]。

### 所有者：列出 {#owners-list}
- 端点：`/api/v1/crates/{crate_name}/owners`
- 方法：GET
- 认证：包含
- 头：
    - `Accept`：`application/json`
- 正文：无

owners 端点返回 crate 的所有者列表。

成功响应包含如下 JSON 对象：

```javascript
{
    // crate 所有者的数组。
    "users": [
        {
            // 所有者的唯一无符号 32 位整数。
            "id": 70,
            // 所有者的唯一用户名。
            "login": "github:rust-lang:core",
            // 所有者的名称。
            // 可选，可为 null。
            "name": "Core",
        }
    ]
}
```

### 所有者：添加 {#owners-add}
- 端点：`/api/v1/crates/{crate_name}/owners`
- 方法：PUT
- 认证：包含
- 头：
    - `Content-Type`：`application/json`
    - `Accept`：`application/json`
- 正文：包含（见下文）

PUT 请求会向注册表发送请求，以向 crate 添加新所有者。如何处理该请求由注册表决定。例如，[crates.io] 会向用户发送邀请，用户必须接受后才会被添加。

请求应包含如下 JSON 对象：

```javascript
{
    // 要添加的所有者的 `login` 字符串数组。
    "users": ["login_name"]
}
```

成功响应包含如下 JSON 对象：

```javascript
{
    // 表示添加成功，始终为 true。
    "ok": true,
    // 向用户显示的字符串。
    "msg": "user ehuss has been invited to be an owner of crate cargo"
}
```

### 所有者：移除 {#owners-remove}
- 端点：`/api/v1/crates/{crate_name}/owners`
- 方法：DELETE
- 认证：包含
- 头：
    - `Content-Type`：`application/json`
    - `Accept`：`application/json`
- 正文：包含（见下文）

DELETE 请求会从 crate 移除所有者。请求应包含如下 JSON 对象：

```javascript
{
    // 要移除的所有者的 `login` 字符串数组。
    "users": ["login_name"]
}
```

成功响应包含如下 JSON 对象：

```javascript
{
    // 表示移除成功，始终为 true。
    "ok": true
    // 向用户显示的字符串。目前被 cargo 忽略。
    "msg": "owners successfully removed",
}
```

## 搜索（Search） {#search}
- 端点：`/api/v1/crates`
- 方法：GET
- 认证：不包含
- 头：
    - `Accept`：`application/json`
- 正文：无
- 查询参数：
    - `q`：搜索查询字符串。
    - `per_page`：结果数量，默认 10，最大 100。

搜索请求会按服务器定义的条件搜索 crate。

成功响应包含如下 JSON 对象：

```javascript
{
    // 结果数组。
    "crates": [
        {
            // crate 的名称。
            "name": "rand",
            // 可用的最高版本。
            "max_version": "0.6.1",
            // crate 的文本描述。
            "description": "Random number generators and other randomness functionality.\n",
        }
    ],
    "meta": {
        // 服务器上可用的结果总数。
        "total": 119
    }
}
```

## 登录（Login） {#login}
- 端点：`/me`

「login」端点并非实际的 API 请求。它的存在仅供 [`cargo login`] 命令显示一个 URL，指示用户在 Web 浏览器中访问以登录并获取 API token。

[`cargo login`]: ../../../../cargo-commands/publishing-commands/01-cargo-login/
[`cargo package`]: ../../../../cargo-commands/publishing-commands/04-cargo-package/
[`cargo publish`]: ../../../../cargo-commands/publishing-commands/05-cargo-publish/
[alphanumeric]: https://doc.rust-lang.org/std/primitive.char.html#method.is_alphanumeric
[config]: ../../../06-configuration/
[crates.io]: https://crates.io/
[publishing documentation]: ../../../../cargo-guide/09-publishing-on-crates-io/#cargo-owner
