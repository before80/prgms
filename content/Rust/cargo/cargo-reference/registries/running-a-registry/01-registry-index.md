+++
title = "01-注册表索引"
date = 2026-07-30T14:49:00+08:00
weight = 53
type = "docs"
description = "注册表索引格式"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 索引格式 {#index-format}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/registry-index.html](https://doc.rust-lang.org/cargo/reference/registry-index.html)


以下定义索引的格式。偶尔会添加新特性，仅从引入它们的 Cargo 版本起才能理解。较旧版本的 Cargo 可能无法使用利用新特性的包。不过，较旧包的格式不应改变，因此较旧版本的 Cargo 应能使用它们。

## 索引配置 {#index-configuration}
索引的根目录包含名为 `config.json` 的文件，其中包含 Cargo 用于访问注册表的 JSON 信息。以下是 [crates.io] 配置文件的示例：

```javascript
{
    "dl": "https://crates.io/api/v1/crates",
    "api": "https://crates.io"
}
```

各键为：
- `dl`：用于下载索引中所列 crate 的 URL。该值可包含以下标记，将被替换为对应值：

  - `{crate}`：crate 的名称。
  - `{version}`：crate 的版本。
  - `{prefix}`：根据 crate 名称计算的目录前缀。例如，名为 `cargo` 的 crate 前缀为 `ca/rg`。细节见下文。
  - `{lowerprefix}`：`{prefix}` 的小写变体。
  - `{sha256-checksum}`：crate 的 sha256 校验和。

  若没有任何标记，则在末尾追加 `/{crate}/{version}/download`。
- `api`：Web API 的基 URL。此键可选，但若未指定，[`cargo publish`] 等命令将无法工作。Web API 见下文。此 URL 不应有尾部斜杠。
- `auth-required`：表示这是否为私有注册表，要求所有操作（包括 API 请求、crate 下载与稀疏索引更新）均需认证。


## 下载端点 {#download-endpoint}
下载端点应发送所请求包的 `.crate` 文件。
Cargo 支持 https、http 与 file URL、HTTP 重定向、HTTP1 与 HTTP2。
TLS 支持的确切细节取决于 Cargo 运行的平台、Cargo 版本及其编译方式。

若在 `config.json` 中设置了 `auth-required: true`，http(s) 下载请求将包含 `Authorization` 头。

## 索引文件 {#index-files}
索引仓库的其余部分为每个包包含一个文件，文件名为包名的小写形式。包的每个版本在文件中占独立一行。文件按分层目录组织：

- 名称长度为 1 个字符的包放在名为 `1` 的目录中。
- 名称长度为 2 个字符的包放在名为 `2` 的目录中。
- 名称长度为 3 个字符的包放在目录 `3/{first-character}` 中，其中 `{first-character}` 是包名的第一个字符。
- 所有其他包存放在名为 `{first-two}/{second-two}` 的目录中，顶层目录是包名的前两个字符，下一层子目录是包名的第三、四个字符。例如，`cargo` 会存放在名为 `ca/rg/cargo` 的文件中。

> 注意：尽管索引文件名是小写的，`Cargo.toml` 与索引 JSON 数据中包含包名的字段是区分大小写的，可包含大小写字符。

上述目录名根据转换为小写的包名计算；由标记 `{lowerprefix}` 表示。使用未经大小写转换的原始包名时，所得目录名由标记 `{prefix}` 表示。例如，包 `MyCrate` 的 `{prefix}` 为 `My/Cr`，`{lowerprefix}` 为 `my/cr`。一般而言，推荐使用 `{prefix}` 而非 `{lowerprefix}`，但各有利弊。在大小写不敏感的文件系统上使用 `{prefix}` 会导致（无害但不优雅的）目录别名。例如，`crate` 与 `CrateTwo` 的 `{prefix}` 值分别为 `cr/at` 与 `Cr/at`；在 Unix 机器上它们是不同的，但在 Windows 上会别名到同一目录。使用规范化大小写的目录可避免别名，但在大小写敏感的文件系统上，更难支持缺少 `{prefix}`/`{lowerprefix}` 的较旧 Cargo 版本。例如，nginx 重写规则可以轻松构造 `{prefix}`，但无法执行大小写转换来构造 `{lowerprefix}`。

## 名称限制 {#name-restrictions}
注册表应考虑对加入其索引的包名施加限制。Cargo 本身允许名称包含任意 [字母数字][alphanumeric]、`-` 或 `_` 字符。[crates.io] 施加了自己的限制，包括以下内容：

- 仅允许 ASCII 字符。
- 仅字母数字、`-` 与 `_` 字符。
- 首字符必须是字母。
- 不区分大小写的冲突检测。
- 防止 `-` 与 `_` 的差异。
- 在特定长度以下（最大 64）。
- 拒绝保留名，如 Windows 特殊文件名「nul」。

注册表应考虑纳入类似限制，并考虑安全影响，例如 [IDN 同形异义攻击](https://en.wikipedia.org/wiki/IDN_homograph_attack) 以及 [UTR36](https://www.unicode.org/reports/tr36/) 与 [UTS39](https://www.unicode.org/reports/tr39/) 中的其他问题。

## 版本唯一性 {#version-uniqueness}
索引*必须*确保每个包的每个版本只出现一次。
这包括忽略 SemVer 构建元数据。
例如，索引*不得*包含版本为 `1.0.7` 与 `1.0.7+extra` 的两个条目。

## JSON 模式 {#json-schema}
包文件中的每一行包含一个 JSON 对象，描述该包已发布的一个版本。以下是带注释的美化打印示例，说明条目的格式。

```javascript
{
    // 包的名称。
    // 只能包含字母数字、`-` 或 `_` 字符。
    "name": "foo",
    // 此行所描述的包版本。
    // 必须是符合 https://semver.org/ 上语义化版本 2.0.0 规范的有效版本号。
    "vers": "0.1.0",
    // 包的直接依赖数组。
    "deps": [
        {
            // 依赖的名称。
            // 若依赖从原始包名重命名，
            // 这是新名称。原始包名存放在
            // `package` 字段中。
            "name": "rand",
            // 此依赖的 SemVer 需求。
            // 必须是在
            // https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html
            // 定义的有效版本需求。
            "req": "^0.6",
            // 为此依赖启用的特性（字符串）数组。
            // 自 Cargo 1.84 起，未指定时默认为 `[]`。
            "features": ["i128_support"],
            // 是否为可选依赖的布尔值。
            // 自 Cargo 1.84 起，未指定时默认为 `false`。
            "optional": false,
            // 是否启用默认特性的布尔值。
            // 自 Cargo 1.84 起，未指定时默认为 `true`。
            "default_features": true,
            // 依赖的目标平台。
            // 若未指定或为 `null`，则不是目标依赖。
            // 否则为字符串，如 "cfg(windows)"。
            "target": null,
            // 依赖种类。
            // "dev"、"build" 或 "normal"。
            // 若未指定或为 `null`，默认为 "normal"。
            "kind": "normal",
            // 此依赖所在注册表索引的 URL，以字符串表示。
            // 若未指定或为 `null`，则假定依赖在当前注册表中。
            "registry": null,
            // 若依赖已重命名，这是实际包名的字符串。
            // 若未指定或为 `null`，则此依赖未重命名。
            "package": null,
        }
    ],
    // `.crate` 文件的 SHA256 校验和。
    "cksum": "d867001db0e2b6e0496f9fac96930e2d42233ecd3ca0413e0753d4c7695d289c",
    // 为包定义的特性集合。
    // 每个特性映射到它启用的特性或依赖数组。
    // 自 Cargo 1.84 起，未指定时默认为 `{}`。
    "features": {
        "extras": ["rand/simd_support"]
    },
    // 此版本是否已被撤回（yank）的布尔值。
    "yanked": false,
    // 包清单中的 `links` 字符串值，未指定则为 null。
    // 此字段可选，默认为 null。
    "links": null,
    // 无符号 32 位整数值，表示此条目的模式版本。
    //
    // 若未指定，应解释为默认值 1。
    //
    // Cargo（从版本 1.51 起）会忽略它不认识的版本。
    // 这提供了一种安全地向索引条目引入变更的方法，
    // 并允许较旧版本的 cargo 忽略它不理解的较新条目。
    // 早于 1.51 的版本会忽略此字段，
    // 因而可能误读索引条目的含义。
    //
    // 当前值为：
    //
    // * 1：此处文档所述的模式，不含较新添加内容。
    //      在 Rust 1.51 及更新版本中受支持。
    // * 2：添加了 `features2` 字段。
    //      在 Rust 1.60 及更新版本中受支持。
    "v": 2,
    // 此可选字段包含使用新的、扩展语法的特性。
    // 具体而言，是命名空间特性（`dep:`）与弱依赖
    // （`pkg?/feat`）。
    //
    // 与 `features` 分开，因为早于 1.19 的版本
    // 会因无法解析新语法而加载失败，即使有
    // `Cargo.lock` 文件也是如此。
    //
    // Cargo 会将此处列出的任何值与 "features" 字段合并。
    //
    // 若包含此字段，应将 "v" 字段至少设为 2。
    //
    // 注册表不必将扩展特性语法用于此字段，
    // 允许将它们包含在 "features" 字段中。
    // 仅当注册表希望支持早于 1.19 的 cargo 版本时才有必要使用此字段，
    // 实践中仅 crates.io 需要，因为那些较旧版本不支持其他注册表。
    "features2": {
        "serde": ["dep:serde", "chrono?/serde"]
    }
    // 最低支持的 Rust 版本（可选）
    // 必须是不带运算符的有效版本需求（例如不能有 `=`）
    "rust_version": "1.60",
    // 此包版本的发布时间（可选）。
    //
    // 格式是 ISO8601 的子集：
    // - `yyyy-mm-ddThh:mm:ssZ`
    // - 无小数秒
    // - 始终为 UTC 时区的 `Z`，不支持时区偏移
    // - 字段零填充
    //
    // 示例：2025-11-12T19:30:12Z
    //
    // 这应是原始发布时间，不应因任何状态变更（如 `yanked`）而改变。
    "pubtime": "2025-11-12T19:30:12Z"
}
```

JSON 对象在添加后不应修改，但 `yanked` 字段除外，其值可随时更改。

> **注意**：索引 JSON 格式与 [发布 API][Publish API] 以及 [`cargo metadata`] 的 JSON 格式有细微差别。
> 若你使用其中之一作为生成索引条目的来源，鼓励仔细检查它们之间的文档差异。
>
> 对于 [发布 API][Publish API]，差异为：
>
> * `deps`
>     * `name` —— 当依赖在 `Cargo.toml` 中[重命名][renamed]时，发布 API 将原始包名放在 `name` 字段，将别名放在 `explicit_name_in_toml` 字段。
>       索引将别名放在 `name` 字段，将原始包名放在 `package` 字段。
>     * `req` —— 发布 API 字段称为 `version_req`。
> * `cksum` —— 发布 API 不指定校验和，必须由注册表在加入索引前计算。
> * `features` —— 某些特性可能放在 `features2` 字段中。
>   注意：这仅是对 [crates.io] 的遗留要求；其他注册表不必操心修改特性映射。
>   `v` 字段指示 `features2` 字段的存在。
> * 发布 API 包含若干其他字段，如 `description` 与 `readme`，它们不出现在索引中。
>   这些旨在让注册表更容易获取关于 crate 的元数据以在网站上显示，而无需解压并解析 `.crate` 文件。
>   这些额外信息通常添加到注册表服务器上的数据库中。
> * 尽管此处包含 `rust_version`，[crates.io] 会忽略此字段，
>   而改为从 `.crate` 文件中的 `Cargo.toml` 读取。
>
> 对于 [`cargo metadata`]，差异为：
>
> * `vers` —— `cargo metadata` 字段称为 `version`。
> * `deps`
>   * `name` —— 当依赖在 `Cargo.toml` 中[重命名][renamed]时，`cargo metadata` 将原始包名放在 `name` 字段，将别名放在 `rename` 字段。
>     索引将别名放在 `name` 字段，将原始包名放在 `package` 字段。
>   * `default_features` —— `cargo metadata` 字段称为 `uses_default_features`。
>   * `registry` —— `cargo metadata` 用 `null` 表示依赖来自 [crates.io]。
>     索引用 `null` 表示依赖来自与索引相同的注册表。
>     创建索引条目时，非 [crates.io] 的注册表应将 `null` 翻译为 `https://github.com/rust-lang/crates.io-index`，并将匹配当前索引的 URL 翻译为 `null`。
>   * `cargo metadata` 包含一些额外字段，如 `source` 与 `path`。
> * 索引包含额外字段，如 `yanked`、`cksum` 与 `v`。

[renamed]: ../../../specifying-dependencies/#renaming-dependencies-in-cargotoml
[Publish API]: ../02-registry-web-api/#publish
[`cargo metadata`]: ../../../../cargo-commands/manifest-commands/05-cargo-metadata/

## 索引协议 {#index-protocols}
Cargo 支持两种远程注册表协议：`git` 与 `sparse`。`git` 协议将索引文件存放在 git 仓库中，`sparse` 协议通过 HTTP 获取各个文件。

### Git 协议 {#git-protocol}
git 协议在索引 URL 中没有协议前缀。例如 [crates.io] 的 git 索引 URL 为 `https://github.com/rust-lang/crates.io-index`。

Cargo 将 git 仓库缓存在磁盘上，以便高效地增量获取更新。

### Sparse 协议 {#sparse-protocol}
稀疏协议在注册表 URL 中使用 `sparse+` 协议前缀。例如，[crates.io] 的稀疏索引 URL 为 `sparse+https://index.crates.io/`。

稀疏协议使用单独的 HTTP 请求下载每个索引文件。由于这会产生大量小型 HTTP 请求，支持流水线与 HTTP/2 的服务器可显著提升性能。

#### 稀疏认证 {#sparse-authentication}
Cargo 会在获取任何其他文件之前尝试获取 `config.json` 文件。若服务器以 HTTP 401 响应，则 Cargo 假定注册表需要认证，并在包含认证 token 的情况下重新尝试请求 `config.json`。

认证失败（或缺少认证 token）时，服务器可包含带有 `Cargo login_url="<URL>"` 质询的 `www-authenticate` 头，以指示用户可前往何处获取 token。

需要认证的注册表必须在 `config.json` 中设置 `auth-required: true`。

#### 缓存 {#caching}
Cargo 缓存 crate 元数据文件，并捕获服务器对每个条目的 `ETag` 或 `Last-Modified` HTTP 头。刷新 crate 元数据时，Cargo 发送 `If-None-Match` 或 `If-Modified-Since` 头，以允许服务器在本地缓存有效时以 HTTP 304「Not Modified」响应，从而节省时间与带宽。若同时存在 `ETag` 与 `Last-Modified` 头，Cargo 仅使用 `ETag`。

#### 缓存失效 {#cache-invalidation}
若注册表使用某种缓存对索引文件访问的 CDN 或代理，则建议注册表在文件更新时实现某种形式的缓存失效。若这些缓存未更新，用户可能在缓存清除前无法访问新 crate。

#### 不存在的 Crate {#nonexistent-crates}
对于不存在的 crate，注册表应以 404「Not Found」、410「Gone」或 451「Unavailable For Legal Reasons」代码响应。

#### 稀疏限制 {#sparse-limitations}
由于注册表的 URL 存储在锁文件中，不建议同时以两种协议提供注册表。关于过渡计划的讨论正在 issue [#10964] 中进行。[crates.io] 注册表是例外，因为使用稀疏协议时 Cargo 会在内部替换为等效的 git URL。

若注册表确实同时提供两种协议，目前建议选择一种协议作为规范协议，并对另一种协议使用[源替换][source replacement]。


[`cargo publish`]: ../../../../cargo-commands/publishing-commands/05-cargo-publish/
[alphanumeric]: https://doc.rust-lang.org/std/primitive.char.html#method.is_alphanumeric
[crates.io]: https://crates.io/
[source replacement]: ../../../specifying-dependencies/02-source-replacement/
[#10964]: https://github.com/rust-lang/cargo/issues/10964
