+++
title = "06-配置"
date = 2026-07-30T14:49:00+08:00
weight = 42
type = "docs"
description = ".cargo/config.toml 配置项参考"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 配置 {#configuration}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/config.html](https://doc.rust-lang.org/cargo/reference/config.html)


本文档说明 Cargo 的配置系统如何工作，以及可用的键与配置项。关于通过清单（manifest）对包（package）进行配置，请参阅[清单格式](../the-manifest-format/)。

## 层级结构 {#hierarchical-structure}

Cargo 允许为特定包进行本地配置，也允许进行全局配置。它会在当前目录及所有父目录中查找配置文件。例如，若在 `/projects/foo/bar/baz` 调用 Cargo，则按以下顺序探测并合并下列配置文件：

* `/projects/foo/bar/baz/.cargo/config.toml`
* `/projects/foo/bar/.cargo/config.toml`
* `/projects/foo/.cargo/config.toml`
* `/projects/.cargo/config.toml`
* `/.cargo/config.toml`
* `$CARGO_HOME/config.toml`，默认路径为：
    * Windows：`%USERPROFILE%\.cargo\config.toml`
    * Unix：`$HOME/.cargo/config.toml`

在此结构下，你可以为每个包指定配置，甚至将其纳入版本控制。你也可以在主目录的配置文件中指定个人默认值。

若同一键在多个配置文件中出现，其值将被合并。数字、字符串和布尔值以更深目录中的配置为准，祖先目录中的值优先级较低，主目录优先级最低。数组将被拼接，优先级更高的项会出现在合并后数组的靠后位置。

目前，从工作空间（workspace）调用 Cargo 时，不会读取工作空间内 crate 的配置文件。即，若工作空间包含两个 crate：`/projects/foo/bar/baz/mylib` 与 `/projects/foo/bar/baz/mybin`，且存在 `/projects/foo/bar/baz/mylib/.cargo/config.toml` 与 `/projects/foo/bar/baz/mybin/.cargo/config.toml`，从工作空间根目录（`/projects/foo/bar/baz/`）调用 Cargo 时不会读取这些配置文件。

> **注意：** Cargo 也会读取不带 `.toml` 扩展名的配置文件，例如 `.cargo/config`。`.toml` 扩展名支持自 1.39 版加入，且为推荐形式。若两种文件都存在，Cargo 将使用不带扩展名的文件。

## 配置格式 {#configuration-format}
配置文件采用 [TOML 格式][toml]（与清单相同），在节（table）内使用简单的键值对。以下是所有设置的快速概览，详细说明见下文。

```toml
paths = ["/path/to/override"] # path 依赖覆盖

[alias]     # 命令别名
b = "build"
c = "check"
t = "test"
r = "run"
rr = "run --release"
recursive_example = "rr --example recursions"
space_example = ["run", "--release", "--", "\"command list\""]

[build]
warnings = "warn"             # 调整警告的有效 lint 级别
jobs = 1                      # 并行任务数，默认为 CPU 核心数
rustc = "rustc"               # Rust 编译器工具
rustc-wrapper = "…"           # 用此包装器代替 `rustc`
rustc-workspace-wrapper = "…" # 对工作空间成员用此包装器代替 `rustc`
rustdoc = "rustdoc"           # 文档生成工具
target = "triple"             # 为目标三元组构建（`cargo install` 会忽略）
target-dir = "target"         # 生成产物的路径
build-dir = "target"          # 中间构建产物的路径
rustflags = ["…", "…"]        # 传给所有编译器调用的自定义标志
rustdocflags = ["…", "…"]     # 传给 rustdoc 的自定义标志
incremental = true            # 是否启用增量编译
dep-info-basedir = "…"        # dep 文件中目标路径的基目录

[credential-alias]
# 为凭据提供程序定义别名。
my-alias = ["/usr/bin/cargo-credential-example", "--argument", "value", "--flag"]

[doc]
browser = "chromium"          # 与 `cargo doc --open` 一起使用的浏览器，
                              # 覆盖 `BROWSER` 环境变量

[env]
# 为 Cargo 运行的任何进程设置 ENV_VAR_NAME=value
ENV_VAR_NAME = "value"
# 即使环境中已存在也强制设置
ENV_VAR_NAME_2 = { value = "value", force = true }
# `value` 相对于 `.cargo/config.toml` 的父目录，环境变量将为完整绝对路径
ENV_VAR_NAME_3 = { value = "relative/path", relative = true }

[future-incompat-report]
frequency = 'always' # 何时显示未来不兼容报告的通知

[cache]
auto-clean-frequency = "1 day"   # 自动清理缓存的频率

[cargo-new]
vcs = "none"              # 使用的 VCS（'git'、'hg'、'pijul'、'fossil'、'none'）

[http]
debug = false               # HTTP 调试
proxy = "host:port"         # libcurl 格式的 HTTP 代理
ssl-version = "tlsv1.3"     # 使用的 TLS 版本
ssl-version.max = "tlsv1.3" # 最大 TLS 版本
ssl-version.min = "tlsv1.1" # 最小 TLS 版本
timeout = 30                # 每次 HTTP 请求的超时（秒）
low-speed-limit = 10        # 网络超时阈值（字节/秒）
cainfo = "cert.pem"         # 证书颁发机构（CA）捆绑包路径
proxy-cainfo = "cert.pem"   # 代理 CA 捆绑包路径
check-revoke = true         # 检查 SSL 证书吊销
multiplexing = true         # HTTP/2 多路复用
user-agent = "…"            # User-Agent 头

[install]
root = "/some/path"         # `cargo install` 目标目录

[net]
retry = 3                   # 网络重试次数
git-fetch-with-cli = true   # 对 git 操作使用 `git` 可执行文件
offline = true              # 不访问网络

[net.ssh]
known-hosts = ["..."]       # 已知 SSH 主机密钥

[patch.<registry>]
# 与 Cargo.toml 中 [patch] 的键相同
[profile.<name>]         # 通过配置修改配置文件（profile）设置。
inherits = "dev"         # 继承 [profile.dev] 的设置。
opt-level = 0            # 优化级别。
debug = true             # 包含调试信息。
split-debuginfo = '...'  # 调试信息拆分行为。
strip = "none"           # 移除符号或调试信息。
debug-assertions = true  # 启用调试断言。
overflow-checks = true   # 启用运行时整数溢出检查。
lto = false              # 设置链接时优化。
panic = 'unwind'         # panic 策略。
incremental = true       # 增量编译。
codegen-units = 16       # 代码生成单元数。
rpath = false            # 设置 rpath 链接选项。
[profile.<name>.build-override]  # 覆盖构建脚本设置。
# 与普通配置文件相同的键。
[profile.<name>.package.<name>]  # 为包覆盖配置文件。
# 与普通配置文件相同的键（不含 `panic`、`lto` 和 `rpath`）。
[resolver]
lockfile-path = "…"  # 覆盖锁文件路径
incompatible-rust-versions = "allow"  # 指定解析器对此类版本的处理方式

[registries.<name>]  # crates.io 以外的注册表
index = "…"          # 注册表索引 URL
token = "…"          # 注册表认证令牌
credential-provider = "cargo:token" # 此注册表的凭据提供程序。

[registries.crates-io]
protocol = "sparse"  # 访问 crates.io 使用的协议。

[registry]
default = "…"        # 默认注册表名称
token = "…"          # crates.io 认证令牌
credential-provider = "cargo:token"           # crates.io 的凭据提供程序。
global-credential-providers = ["cargo:token"] # 默认使用的全局凭据提供程序。

[source.<name>]      # 源定义与替换
replace-with = "…"   # 用给定命名源替换此源
directory = "…"      # 目录源路径
registry = "…"       # 注册表源 URL
local-registry = "…" # 本地注册表源路径
git = "…"            # git 仓库源 URL
branch = "…"         # git 仓库分支名
tag = "…"            # git 仓库标签名
rev = "…"            # git 仓库修订版本

[target.<triple>]
linker = "…"              # 使用的链接器
runner = "…"              # 运行可执行文件的包装器
rustflags = ["…", "…"]    # `rustc` 的自定义标志
rustdocflags = ["…", "…"] # `rustdoc` 的自定义标志

[target.<cfg>]
linker = "…"            # 使用的链接器
runner = "…"            # 运行可执行文件的包装器
rustflags = ["…", "…"]  # `rustc` 的自定义标志

[target.<triple>.<links>] # `links` 构建脚本覆盖
rustc-link-lib = ["foo"]
rustc-link-search = ["/path/to/foo"]
rustc-flags = "-L /some/path"
rustc-cfg = ['key="value"']
rustc-env = {key = "value"}
rustc-cdylib-link-arg = ["…"]
metadata_key1 = "value"
metadata_key2 = "value"

[term]
quiet = false                    # cargo 输出是否静默
verbose = false                  # cargo 是否提供详细输出
color = 'auto'                   # cargo 是否彩色输出
hyperlinks = true                # cargo 是否在输出中插入链接
unicode = true                   # cargo 是否可用非 ASCII Unicode 字符渲染输出
progress.when = 'auto'           # cargo 是否显示进度条
progress.width = 80              # 进度条宽度
progress.term-integration = true # cargo 是否向终端模拟器报告进度
```

## 环境变量 {#environment-variables}
除 TOML 配置文件外，Cargo 也可通过环境变量配置。对于形如 `foo.bar` 的每个配置键，也可使用环境变量 `CARGO_FOO_BAR` 定义其值。键会转为大写，点与连字符转为下划线。例如，`target.x86_64-unknown-linux-gnu.runner` 也可由环境变量 `CARGO_TARGET_X86_64_UNKNOWN_LINUX_GNU_RUNNER` 定义。

环境变量优先于 TOML 配置文件。目前仅支持通过环境变量定义整数、布尔、字符串及某些数组值。[下文说明](#configuration-keys)会标明哪些键支持环境变量；其余键因[技术原因](https://github.com/rust-lang/cargo/issues/5416)暂不支持。

除上述机制外，Cargo 还识别若干其他特定[环境变量][env]。

## 命令行覆盖 {#command-line-overrides}

Cargo 也接受通过 `--config` 命令行选项进行任意配置覆盖。参数应为 TOML 语法的 `KEY=VALUE`，或指向额外配置文件的路径：

```console
# 使用 TOML 语法的 KEY=VALUE
cargo --config net.git-fetch-with-cli=true fetch

# 使用配置文件路径
cargo --config ./path/to/my/extra-config.toml fetch
```

`--config` 可多次指定，值按从左到右顺序合并，合并逻辑与多个配置文件生效时相同。以此方式指定的配置值优先于环境变量，环境变量优先于配置文件。

当 `--config` 提供的是额外配置文件时，该文件的加载遵循与直接通过 `--config` 指定选项相同的优先级规则。

以下是 Bourne shell 语法示例：

```console
# 多数 shell 需要转义。
cargo --config http.proxy=\"http://example.com\" …

# 可使用空格。
cargo --config "net.git-fetch-with-cli = true" …

# TOML 数组示例。单引号便于读写。
cargo --config 'build.rustdocflags = ["--html-in-header", "header.html"]' …

# 复杂 TOML 键示例。
cargo --config "target.'cfg(all(target_arch = \"arm\", target_os = \"none\"))'.runner = 'my-runner'" …

# 覆盖配置文件设置示例。
cargo --config profile.dev.package.image.opt-level=3 …
```

## 包含额外配置文件 {#including-extra-configuration-files}
配置可通过顶层 `include` 键包含其他配置文件。这便于在多个项目间共享配置，或将复杂配置拆分为多个文件。

### `include` {#include}
* 类型：字符串或表的数组
* 默认：无
* 环境变量：不支持

加载额外配置文件。路径相对于包含它们的配置文件。仅接受以 `.toml` 结尾的路径。

支持以下格式：

```toml
# 路径数组
include = [
    "frodo.toml",
    "samwise.toml",
]

# 内联表以获得更多控制
include = [
    { path = "required.toml" },
    { path = "optional.toml", optional = true },
]
```

> **注意：** 为便于阅读并避免混淆，建议：
> - 将 `include` 放在配置文件顶部
> - 每行一个 include，便于版本控制 diff
> - 需要可选 include 时使用内联表语法

使用表语法时，支持以下字段：

* `path`（字符串，必填）：要包含的配置文件路径。
* `optional`（布尔，默认：`false`）：若为 `true`，缺失文件会被静默跳过，而非报错。

`include` 的合并行为与其他配置值不同：

1. 首先从 `include` 路径加载配置值。
    * 被包含文件从左到右加载，后加载文件的值优先于先加载的。
    * 若被包含文件也含 `include` 键，此步骤会递归。
2. 然后，配置文件自身的值合并到已包含配置之上，优先级最高。

## 相对于配置的路径 {#config-relative-paths}
配置文件中的路径可以是绝对路径、相对路径，或不带路径分隔符的裸名称。对不带路径分隔符的可执行文件路径，将使用 `PATH` 环境变量搜索可执行文件。对非可执行文件，路径相对于定义该配置值的位置。

具体规则：

* 对环境变量，路径相对于当前工作目录。
* 对直接从 [`--config KEY=VALUE`](#command-line-overrides) 选项加载的配置值，路径相对于当前工作目录。
* 对配置文件，路径相对于定义配置文件的目录的父目录，无论这些文件来自[层级探测](#hierarchical-structure)还是 [`--config <path>`](#command-line-overrides) 选项。

> **注意：** 为与现有 `.cargo/config.toml` 探测行为保持一致，设计上通过 `--config <path>` 传入的配置文件中的路径，也相对于该配置文件本身向上两级。
>
> 为避免意外结果，经验法则是将额外配置文件放在与项目中发现的 `.cargo/config.toml` 同级。例如，给定项目 `/my/project`，建议将配置文件放在 `/my/project/.cargo`，或同级新目录，如 `/my/project/.config`。

```toml
# 相对路径示例。
[target.x86_64-unknown-linux-gnu]
runner = "foo"  # 在 `PATH` 中搜索 `foo`。

[source.vendored-sources]
# 目录相对于 `.cargo/config.toml` 所在位置的父目录。
# 例如 `/my/project/.cargo/config.toml` 会得到 `/my/project/vendor`。
directory = "vendor"
```

## 带参数的可执行文件路径 {#executable-paths-with-arguments}

某些 Cargo 命令会调用外部程序，可配置为路径加若干参数。

值可以是字符串数组，如 `['/path/to/program', 'somearg']`，或空格分隔的字符串，如 `'/path/to/program somearg'`。若可执行文件路径含空格，必须使用数组形式。

若 Cargo 向程序传递其他参数（如要打开或运行的路径），它们会追加在该选项值的最后一个指定参数之后。若指定程序不含路径分隔符，Cargo 会在 `PATH` 中搜索其可执行文件。

## 凭据 {#credentials}

含敏感信息的配置值存储在 `$CARGO_HOME/credentials.toml` 文件中。使用 [`cargo:token`] 凭据提供程序时，该文件由 [`cargo login`] 与 [`cargo logout`] 自动创建和更新。

某些 Cargo 命令（如 [`cargo publish`]）使用令牌对远程注册表进行身份验证。应注意保护令牌并保密。

其格式与 Cargo 配置文件相同。

```toml
[registry]
token = "…"   # crates.io 访问令牌

[registries.<name>]
token = "…"   # 命名注册表的访问令牌
```

与大多数其他配置值一样，令牌也可通过环境变量指定。[crates.io] 的令牌可用 `CARGO_REGISTRY_TOKEN` 环境变量指定。其他注册表的令牌可用 `CARGO_REGISTRIES_<name>_TOKEN` 形式的环境变量指定，其中 `<name>` 为注册表名称的大写形式。

> **注意：** Cargo 也会读写不带 `.toml` 扩展名的凭据文件，例如 `.cargo/credentials`。`.toml` 扩展名支持自 1.39 版加入。1.68 版起，Cargo 默认写入带扩展名的文件。但为向后兼容，当两种文件都存在时，Cargo 会读写不带扩展名的文件。

## 配置键 {#configuration-keys}

本节记录所有配置键。含可变部分的键用尖括号标注，如 `target.<triple>`，其中 `<triple>` 可以是任意[目标三元组][target triple]，例如 `target.x86_64-pc-windows-msvc`。

### `paths` {#paths}
* 类型：字符串（路径）数组
* 默认：无
* 环境变量：不支持

本地包路径数组，用作依赖覆盖。更多信息见[覆盖依赖指南](../specifying-dependencies/01-overriding-dependencies/#paths-overrides)。

### `[alias]` {#alias}
* 类型：字符串或字符串数组
* 默认：见下文
* 环境变量：`CARGO_ALIAS_<name>`

`[alias]` 表定义 CLI 命令别名。例如，运行 `cargo b` 等价于运行 `cargo build`。表中每个键是子命令，值是要运行的实际命令。值可以是字符串数组，首元素为命令，其余为参数；也可以是字符串，会按空格拆分为子命令与参数。Cargo 内置以下别名：

```toml
[alias]
b = "build"
c = "check"
d = "doc"
t = "test"
r = "run"
rm = "remove"
```

别名不得重新定义已有内置命令。

别名可递归：

```toml
[alias]
rr = "run --release"
recursive_example = "rr --example recursions"
```

### `[build]` {#build}
`[build]` 表控制构建时操作与编译器设置。

#### `build.warnings` {#buildwarnings}
* 类型：字符串
* 默认：`"warn"`
* 环境变量：`CARGO_BUILD_WARNINGS`

调整本地包 lint 警告的有效级别。
允许级别：
* `"warn"`：继续将 lint 作为警告输出（默认）。
* `"allow"`：隐藏 lint。
* `"deny"`：对有 lint 警告的 crate 报错。
  使用 `--keep-going` 可查看所有依赖 crate 的 lint 警告。

仅影响作为 lint 的警告（即级别可调），例如非 lint 警告或通过 `--verbose --verbose` 可见的依赖警告不受影响。

> **MSRV：** 自 1.97 起生效。

#### `build.jobs` {#buildjobs}
* 类型：整数或字符串
* 默认：逻辑 CPU 数量
* 环境变量：`CARGO_BUILD_JOBS`

设置并行运行的最大编译器进程数。若为负数，则最大进程数为逻辑 CPU 数加上该值。不得为 0。若提供字符串 `default`，则恢复为默认值。

可用 `--jobs` CLI 选项覆盖。

#### `build.rustc` {#buildrustc}
* 类型：字符串（程序路径）
* 默认：`"rustc"`
* 环境变量：`CARGO_BUILD_RUSTC` 或 `RUSTC`

设置用于 `rustc` 的可执行文件。

#### `build.rustc-wrapper` {#buildrustc-wrapper}
* 类型：字符串（程序路径）
* 默认：无
* 环境变量：`CARGO_BUILD_RUSTC_WRAPPER` 或 `RUSTC_WRAPPER`

设置代替 `rustc` 执行的包装器。传给包装器的第一个参数是实际要使用的可执行文件路径（即若设置了 `build.rustc` 则用该值，否则为 `"rustc"`）。

#### `build.rustc-workspace-wrapper` {#buildrustc-workspace-wrapper}
* 类型：字符串（程序路径）
* 默认：无
* 环境变量：`CARGO_BUILD_RUSTC_WORKSPACE_WRAPPER` 或 `RUSTC_WORKSPACE_WRAPPER`

设置仅对工作空间成员代替 `rustc` 执行的包装器。构建无工作空间的单包项目时，该包视为工作空间。传给包装器的第一个参数是实际可执行文件路径（即若设置了 `build.rustc` 则用该值，否则为 `"rustc"`）。它会影响文件名哈希，使包装器产生的产物单独缓存。

若同时设置 `rustc-wrapper` 与 `rustc-workspace-wrapper`，它们会嵌套：最终调用为 `$RUSTC_WRAPPER $RUSTC_WORKSPACE_WRAPPER $RUSTC`。

#### `build.rustdoc` {#buildrustdoc}
* 类型：字符串（程序路径）
* 默认：`"rustdoc"`
* 环境变量：`CARGO_BUILD_RUSTDOC` 或 `RUSTDOC`

设置用于 `rustdoc` 的可执行文件。

#### `build.target` {#buildtarget}
* 类型：字符串或字符串数组
* 默认：主机平台
* 环境变量：`CARGO_BUILD_TARGET`

默认编译的[目标平台三元组][target triple]。

可选值：
- `rustc --print target-list` 支持的任意目标。
- `"host-tuple"`，内部替换为主机目标。这在交叉编译部分 crate 且不想将主机指定为目标时很有用（例如共享项目中可能被多台主机使用的 `xtask`）。
- 自定义目标规范文件路径。更多信息见[自定义目标查找路径](https://doc.rust-lang.org/rustc/targets/custom.html#custom-target-lookup-path)。

可用 `--target` CLI 选项覆盖。

```toml
[build]
target = ["x86_64-unknown-linux-gnu", "i686-unknown-linux-gnu"]
```

#### `build.target-dir` {#buildtarget-dir}
* 类型：字符串（路径）
* 默认：`"target"`
* 环境变量：`CARGO_BUILD_TARGET_DIR` 或 `CARGO_TARGET_DIR`

所有编译器输出的路径。未指定时默认为工作空间根目录下的 `target` 目录。

可用 `--target-dir` CLI 选项覆盖。

更多信息见[构建缓存文档](../09-build-cache/)。

#### `build.build-dir` {#buildbuild-dir}
* 类型：字符串（路径）
* 默认：默认为 `build.target-dir` 的值
* 环境变量：`CARGO_BUILD_BUILD_DIR`

存储中间构建产物的目录。中间产物由 Rustc/Cargo 在构建过程中产生。

此选项支持路径模板。

可用模板变量：
* `{workspace-root}` 解析为当前工作空间根。
* `{cargo-cache-home}` 解析为 `CARGO_HOME`
* `{workspace-path-hash}` 解析为清单路径的哈希

更多信息见[构建缓存文档](../09-build-cache/)。

#### `build.rustflags` {#buildrustflags}
* 类型：字符串或字符串数组
* 默认：无
* 环境变量：`CARGO_BUILD_RUSTFLAGS` 或 `CARGO_ENCODED_RUSTFLAGS` 或 `RUSTFLAGS`

传给 `rustc` 的额外命令行标志。值可以是字符串数组或空格分隔的字符串。

额外标志有四个互斥来源，按顺序检查，使用第一个：

1. `CARGO_ENCODED_RUSTFLAGS` 环境变量。
2. `RUSTFLAGS` 环境变量。
3. 所有匹配的 `target.<triple>.rustflags` 与 `target.<cfg>.rustflags` 配置项拼接。
4. `build.rustflags` 配置值。

也可通过 [`cargo rustc`] 命令传递额外标志。

若使用 `--target` 标志（或 [`build.target`](#buildtarget)），标志仅传给目标编译器。为主机构建的内容（如构建脚本或 proc macro）不会收到这些参数。无 `--target` 时，标志会传给所有编译器调用（含构建脚本与 proc macro），因为依赖是共享的。若有不想传给构建脚本或 proc macro 的参数且为主机构建，请用[主机三元组][target triple]传递 `--target`。

不建议传入 Cargo 通常自行管理的标志。例如，由[配置文件（profiles）](../05-profiles/)驱动的标志，最好通过相应配置文件设置处理。

> **注意：** 由于直接向编译器传标志的低层特性，这可能与未来可能自行发出相同或类似标志的 Cargo 版本冲突，从而干扰你指定的标志。Cargo 在此领域未必始终向后兼容。

#### `build.rustdocflags` {#buildrustdocflags}
* 类型：字符串或字符串数组
* 默认：无
* 环境变量：`CARGO_BUILD_RUSTDOCFLAGS` 或 `CARGO_ENCODED_RUSTDOCFLAGS` 或 `RUSTDOCFLAGS`

传给 `rustdoc` 的额外命令行标志。值可以是字符串数组或空格分隔的字符串。

额外标志有四个互斥来源，按顺序检查，使用第一个：

1. `CARGO_ENCODED_RUSTDOCFLAGS` 环境变量。
2. `RUSTDOCFLAGS` 环境变量。
3. 所有匹配的 `target.<triple>.rustdocflags` 与 `target.<cfg>.rustdocflags` 配置项拼接。
4. `build.rustdocflags` 配置值。

也可通过 [`cargo rustdoc`] 命令传递额外标志。

> **注意：** 由于直接向编译器传标志的低层特性，这可能与未来可能自行发出相同或类似标志的 Cargo 版本冲突，从而干扰你指定的标志。Cargo 在此领域未必始终向后兼容。

#### `build.incremental` {#buildincremental}
* 类型：布尔
* 默认：来自配置文件
* 环境变量：`CARGO_BUILD_INCREMENTAL` 或 `CARGO_INCREMENTAL`

是否执行[增量编译]。

在设置了 `CI` 的环境中，未设置时默认为 `CARGO_BUILD_INCREMENTAL=false`。
否则默认使用[配置文件](../05-profiles/#incremental)中的值。

`CARGO_INCREMENTAL` 环境变量可设为 `1` 强制为所有配置文件启用增量编译，或 `0` 禁用。该环境变量覆盖配置设置。

#### `build.dep-info-basedir` {#builddep-info-basedir}
* 类型：字符串（路径）
* 默认：无
* 环境变量：`CARGO_BUILD_DEP_INFO_BASEDIR`

从 [dep info](../09-build-cache/#dep-info-files) 文件路径中剥离给定路径前缀。此配置旨在将绝对路径转为相对路径，供需要相对路径的工具使用。

设置本身是相对于配置的路径。例如，值为 `"."` 会剥离所有以 `.cargo` 目录父目录开头的路径。

#### `build.pipelining` {#buildpipelining}
此选项已弃用且未使用。Cargo 始终启用流水线（pipelining）。

### `[credential-alias]` {#credential-alias}
* 类型：字符串或字符串数组
* 默认：空
* 环境变量：`CARGO_CREDENTIAL_ALIAS_<name>`

`[credential-alias]` 表定义凭据提供程序别名。
这些别名可在 `registry.global-credential-providers` 数组中引用，或作为 `registries.<NAME>.credential-provider` 下特定注册表的凭据提供程序。

若指定为字符串，值会按空格拆分为路径与参数。

例如，定义名为 `my-alias` 的别名：

```toml
[credential-alias]
my-alias = ["/usr/bin/cargo-credential-example", "--argument", "value", "--flag"]
```
更多信息见[注册表身份验证](../registries/registry-authentication/)。

### `[doc]` {#doc}
`[doc]` 表定义 [`cargo doc`] 命令的选项。

#### `doc.browser` {#docbrowser}
* 类型：字符串或字符串数组（[带参数的程序路径]）
* 默认：`BROWSER` 环境变量，或缺失时以系统特定方式打开链接

此选项设置 [`cargo doc`] 使用的浏览器，在使用 `--open` 打开文档时覆盖 `BROWSER` 环境变量。

### `[cargo-new]` {#cargo-new}
`[cargo-new]` 表定义 [`cargo new`] 命令的默认值。

#### `cargo-new.name` {#cargo-newname}
此选项已弃用且未使用。

#### `cargo-new.email` {#cargo-newemail}
此选项已弃用且未使用。

#### `cargo-new.vcs` {#cargo-newvcs}
* 类型：字符串
* 默认：`"git"` 或 `"none"`
* 环境变量：`CARGO_CARGO_NEW_VCS`

指定初始化新仓库时使用的版本控制系统。
有效值为 `git`、`hg`（Mercurial）、`pijul`、`fossil` 或 `none` 以禁用此行为。默认为 `git`，若已在 VCS 仓库内则为 `none`。可用 `--vcs` CLI 选项覆盖。

### `[env]` {#env}
`[env]` 节允许为构建脚本、rustc 调用、`cargo run` 与 `cargo build` 设置额外环境变量。

```toml
[env]
OPENSSL_DIR = "/opt/openssl"
```

默认情况下，指定变量不会覆盖环境中已存在的值。可通过 `force` 标志更改此行为。

设置 `relative` 标志时，值作为相对于包含 `config.toml` 的 `.cargo` 目录父目录的配置相对路径求值。环境变量的值将为完整绝对路径。

```toml
[env]
TMPDIR = { value = "/home/tmp", force = true }
OPENSSL_DIR = { value = "vendor/openssl", relative = true }
```

### `[future-incompat-report]` {#future-incompat-report}
`[future-incompat-report]` 表控制[未来不兼容报告](../14-future-incompat-report/)的设置。

#### `future-incompat-report.frequency` {#future-incompat-reportfrequency}
* 类型：字符串
* 默认：`"always"`
* 环境变量：`CARGO_FUTURE_INCOMPAT_REPORT_FREQUENCY`

控制当未来不兼容报告可用时，向终端显示通知的频率。可选值：

* `always`（默认）：命令（如 `cargo build`）产生未来不兼容报告时始终显示通知
* `never`：从不显示通知

### `[cache]` {#cache}
`[cache]` 表定义 Cargo 缓存的设置。

#### 全局缓存 {#global-caches}

运行 `cargo` 命令时，Cargo 会自动跟踪你在全局缓存中使用的文件。
Cargo 会定期删除一段时间未使用的文件。
需从网络下载的文件若 3 个月未使用会被删除。无需网络即可生成的文件若 1 个月未使用会被删除。

自动删除仅在运行已做大量工作的命令时进行，例如所有构建命令（`cargo build`、`cargo test`、`cargo check` 等）以及 `cargo fetch`。

若 Cargo 处于离线状态（如使用 `--offline` 或 `--frozen`），自动删除会禁用，以免删除长时间离线时可能需要的产物。

> **注意：** 此跟踪目前仅针对 Cargo 主目录中的全局缓存实现。
> 包括从注册表与 git 依赖下载的注册表索引与源文件。
> 构建产物跟踪尚未实现，见 [cargo#13136](https://github.com/rust-lang/cargo/issues/13136)。
>
> 此外，有不稳定特性支持*手动*触发缓存清理，并进一步自定义配置选项。
> 更多信息见[不稳定章节](../17-unstable-features/#gc)。

#### `cache.auto-clean-frequency` {#cacheauto-clean-frequency}
* 类型：字符串
* 默认：`"1 day"`
* 环境变量：`CARGO_CACHE_AUTO_CLEAN_FREQUENCY`

此选项定义 Cargo 自动删除全局缓存中未使用文件的频率。
*不*定义文件必须有多旧，这些阈值见[上文](#global-caches)。

支持以下设置：

* `"never"` —— 从不删除旧文件。
* `"always"` —— 每次运行 Cargo 都检查删除旧文件。
* 整数后跟 "seconds"、"minutes"、"hours"、"days"、"weeks" 或 "months" —— 最多在给定时间范围内检查删除旧文件。

### `[http]` {#http}
`[http]` 表定义 HTTP 行为设置，包括获取 crate 依赖与访问远程 git 仓库。

#### `http.debug` {#httpdebug}
* 类型：布尔
* 默认：false
* 环境变量：`CARGO_HTTP_DEBUG`

若为 `true`，启用 HTTP 请求调试。设置 `CARGO_LOG=network=debug` 环境变量可查看调试信息（或使用 `network=trace` 获取更多信息）。

在公开位置发布此输出日志时请谨慎。输出可能包含带认证令牌的头，切勿泄露！发布前请审查日志。

#### `http.proxy` {#httpproxy}
* 类型：字符串
* 默认：无
* 环境变量：`CARGO_HTTP_PROXY` 或 `HTTPS_PROXY` 或 `https_proxy` 或 `http_proxy`

设置 HTTP 与 HTTPS 代理。格式为 [libcurl 格式]，如 `[protocol://]host[:port]`。若未设置，Cargo 也会检查全局 git 配置中的 `http.proxy`。若均未设置，`HTTPS_PROXY` 或 `https_proxy` 为 HTTPS 请求设置代理，`http_proxy` 为 HTTP 请求设置代理。

#### `http.timeout` {#httptimeout}
* 类型：整数
* 默认：30
* 环境变量：`CARGO_HTTP_TIMEOUT` 或 `HTTP_TIMEOUT`

设置每次 HTTP 请求的超时（秒）。

#### `http.cainfo` {#httpcainfo}
* 类型：字符串（路径）
* 默认：无
* 环境变量：`CARGO_HTTP_CAINFO`

证书颁发机构（CA）捆绑包文件路径，用于验证 TLS 证书。未指定时，Cargo 尝试使用系统证书。

#### `http.proxy-cainfo` {#httpproxy-cainfo}
* 类型：字符串（路径）
* 默认：未设置时回退到 `http.cainfo`
* 环境变量：`CARGO_HTTP_PROXY_CAINFO`

证书颁发机构（CA）捆绑包文件路径，用于验证代理 TLS 证书。

#### `http.check-revoke` {#httpcheck-revoke}
* 类型：布尔
* 默认：true（Windows）false（其他平台）
* 环境变量：`CARGO_HTTP_CHECK_REVOKE`

决定是否执行 TLS 证书吊销检查。此功能仅在 Windows 上有效。

#### `http.ssl-version` {#httpssl-version}
* 类型：字符串或 min/max 表
* 默认：无
* 环境变量：`CARGO_HTTP_SSL_VERSION`

设置使用的最低 TLS 版本。接受字符串，可能值为 `"default"`、`"tlsv1"`、`"tlsv1.0"`、`"tlsv1.1"`、`"tlsv1.2"` 或 `"tlsv1.3"`。

也可使用含 `min` 与 `max` 两个键的表，各接受同类型字符串，指定 TLS 版本的最小与最大范围。

默认最低版本为 `"tlsv1.0"`，最大为平台支持的最新版本，通常为 `"tlsv1.3"`。

#### `http.low-speed-limit` {#httplow-speed-limit}
* 类型：整数
* 默认：10
* 环境变量：`CARGO_HTTP_LOW_SPEED_LIMIT`

此设置控制慢连接的超时行为。若平均传输速度（字节/秒）在 [`http.timeout`](#httptimeout) 秒（默认 30 秒）内低于给定值，则连接视为过慢，Cargo 会中止并重试。

#### `http.multiplexing` {#httpmultiplexing}
* 类型：布尔
* 默认：true
* 环境变量：`CARGO_HTTP_MULTIPLEXING`

为 `true` 时，Cargo 尝试使用 HTTP/2 多路复用。
允许多个请求共用同一连接，获取多个文件时通常可提升性能。为 `false` 时，Cargo 使用 HTTP 1.1 且不使用流水线。

#### `http.user-agent` {#httpuser-agent}
* 类型：字符串
* 默认：Cargo 版本
* 环境变量：`CARGO_HTTP_USER_AGENT`

指定自定义 User-Agent 头。未指定时默认为包含 Cargo 版本的字符串。

### `[install]` {#install}
`[install]` 表定义 [`cargo install`] 命令的默认值。

#### `install.root` {#installroot}
* 类型：字符串（路径）
* 默认：Cargo 主目录
* 环境变量：`CARGO_INSTALL_ROOT`

设置 [`cargo install`] 安装可执行文件的根目录路径。可执行文件位于根目录下的 `bin` 目录。

为跟踪已安装可执行文件信息，此根目录下还会创建 `.crates.toml` 与 `.crates2.json` 等额外文件。

未指定时默认为 Cargo 主目录（默认为主目录下的 `.cargo`）。

可用 `--root` 命令行选项覆盖。

### `[net]` {#net}
`[net]` 表控制网络配置。

#### `net.retry` {#netretry}
* 类型：整数
* 默认：3
* 环境变量：`CARGO_NET_RETRY`

可能偶发网络错误的重试次数。

#### `net.git-fetch-with-cli` {#netgit-fetch-with-cli}
* 类型：布尔
* 默认：false
* 环境变量：`CARGO_NET_GIT_FETCH_WITH_CLI`

若为 `true`，Cargo 使用 `git` 可执行文件获取注册表索引与 git 依赖。若为 `false`，则使用内置 `git` 库。

设为 `true` 在你有 Cargo 不支持的特别身份验证需求时可能有帮助。关于 git 身份验证设置，见 [Git 身份验证](../../appendix/02-git-authentication/)。

#### `net.offline` {#netoffline}
* 类型：布尔
* 默认：false
* 环境变量：`CARGO_NET_OFFLINE`

若为 `true`，Cargo 避免访问网络，尝试使用本地缓存数据继续。若为 `false`，Cargo 按需访问网络，遇到网络错误则报错。

可用 `--offline` 命令行选项覆盖。

#### `net.ssh` {#netssh}
`[net.ssh]` 表包含 SSH 连接设置。

#### `net.ssh.known-hosts` {#netsshknown-hosts}
* 类型：字符串数组
* 默认：见说明
* 环境变量：不支持

`known-hosts` 数组包含连接 SSH 服务器（如 SSH git 依赖）时应接受为有效的主机密钥列表。每项应为类似 OpenSSH `known_hosts` 文件的字符串格式。每项应以一个或多个逗号分隔的主机名开头，空格，密钥类型名，空格，以及 base64 编码的密钥。例如：

```toml
[net.ssh]
known-hosts = [
    "example.com ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIFO4Q5T0UV0SQevair9PFwoxY9dl4pQl3u5phoqJH3cF"
]
```

Cargo 会尝试从 OpenSSH 支持的常见位置加载已知主机密钥，并与 Cargo 配置文件中列出的项合并。
若有匹配项且密钥正确，则允许连接。

Cargo 内置 [github.com][github-keys] 的主机密钥。若密钥变更，可将新密钥添加到配置或 known_hosts 文件。

更多细节见 [Git 身份验证](../../appendix/02-git-authentication/#ssh-known-hosts)。

[github-keys]: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints

### `[patch]` {#patch}
与在 [`Cargo.toml` 中使用 `[patch]`](../specifying-dependencies/01-overriding-dependencies/#the-patch-section) 覆盖依赖相同，你也可在 Cargo 配置文件中覆盖依赖，使补丁应用于任何受影响的构建。格式与 `Cargo.toml` 中使用的完全相同。

由于 `.cargo/config.toml` 文件通常不纳入源代码控制，应优先在 `Cargo.toml` 中打补丁，以确保其他开发者能在各自环境中编译你的 crate。通过 Cargo 配置文件打补丁通常仅在外部构建工具自动生成补丁节时合适。

若给定依赖同时在 Cargo 配置文件与 `Cargo.toml` 中被补丁，则使用配置文件中的补丁。若多个配置文件补丁同一依赖，使用标准 Cargo 配置合并，优先使用离当前目录最近的定义，`$HOME/.cargo/config.toml` 优先级最低。

此类 `[patch]` 节中的相对 `path` 依赖相对于其所在配置文件解析。

### `[profile]` {#profile}
`[profile]` 表可全局更改配置文件设置，并覆盖 `Cargo.toml` 中的设置。语法与选项与 `Cargo.toml` 中的配置文件相同。选项详情见[配置文件章节]。

[配置文件章节]: ../05-profiles/

#### `[profile.<name>.build-override]` {#profilenamebuild-override}
* 环境变量：`CARGO_PROFILE_<name>_BUILD_OVERRIDE_<key>`

build-override 表覆盖构建脚本、proc macro 及其依赖的设置。键与普通配置文件相同。更多细节见[覆盖节](../05-profiles/#overrides)。

#### `[profile.<name>.package.<name>]` {#profilenamepackagename}
* 环境变量：不支持

package 表覆盖特定包的设置。键与普通配置文件相同，但不包含 `panic`、`lto` 与 `rpath`。更多细节见[覆盖节](../05-profiles/#overrides)。

#### `profile.<name>.codegen-units` {#profilenamecodegen-units}
* 类型：整数
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_CODEGEN_UNITS`

见 [codegen-units](../05-profiles/#codegen-units)。

#### `profile.<name>.debug` {#profilenamedebug}
* 类型：整数或布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_DEBUG`

见 [debug](../05-profiles/#debug)。

#### `profile.<name>.split-debuginfo` {#profilenamesplit-debuginfo}
* 类型：字符串
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_SPLIT_DEBUGINFO`

见 [split-debuginfo](../05-profiles/#split-debuginfo)。

#### `profile.<name>.debug-assertions` {#profilenamedebug-assertions}
* 类型：布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_DEBUG_ASSERTIONS`

见 [debug-assertions](../05-profiles/#debug-assertions)。

#### `profile.<name>.incremental` {#profilenameincremental}
* 类型：布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_INCREMENTAL`

见 [incremental](../05-profiles/#incremental)。

#### `profile.<name>.lto` {#profilenamelto}
* 类型：字符串或布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_LTO`

见 [lto](../05-profiles/#lto)。

#### `profile.<name>.overflow-checks` {#profilenameoverflow-checks}
* 类型：布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_OVERFLOW_CHECKS`

见 [overflow-checks](../05-profiles/#overflow-checks)。

#### `profile.<name>.opt-level` {#profilenameopt-level}
* 类型：整数或字符串
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_OPT_LEVEL`

见 [opt-level](../05-profiles/#opt-level)。

#### `profile.<name>.panic` {#profilenamepanic}
* 类型：字符串
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_PANIC`

见 [panic](../05-profiles/#panic)。

#### `profile.<name>.rpath` {#profilenamerpath}
* 类型：布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_RPATH`

见 [rpath](../05-profiles/#rpath)。

#### `profile.<name>.strip` {#profilenamestrip}
* 类型：字符串或布尔
* 默认：见配置文件文档。
* 环境变量：`CARGO_PROFILE_<name>_STRIP`

见 [strip](../05-profiles/#strip)。

### `[resolver]` {#resolver}
`[resolver]` 表覆盖本地开发的[依赖解析行为](../specifying-dependencies/03-dependency-resolution/)（例如不包括 `cargo install`）。

#### `resolver.lockfile-path` {#resolverlockfile-path}
* 类型：字符串（路径）
* 默认：`<workspace_root>/Cargo.lock`
* 环境变量：`CARGO_RESOLVER_LOCKFILE_PATH`

指定解析依赖时使用的锁文件路径。
此选项在只读源代码目录中工作时很有用。

路径必须以 `Cargo.lock` 结尾。

> **MSRV：** 需要 1.97+

#### `resolver.incompatible-rust-versions` {#resolverincompatible-rust-versions}
* 类型：字符串
* 默认：见 [`resolver`](../specifying-dependencies/03-dependency-resolution/#resolver-versions) 文档
* 环境变量：`CARGO_RESOLVER_INCOMPATIBLE_RUST_VERSIONS`

解析依赖版本时，选择如何处理 `package.rust-version` 不兼容的版本。
值包括：
- `allow`：将 `rust-version` 不兼容的版本视为普通版本
- `fallback`：仅在没有其他匹配版本时才考虑 `rust-version` 不兼容的版本

可用以下方式覆盖：
- `--ignore-rust-version` CLI 选项
- 将依赖的版本要求设得高于任何 `rust-version` 兼容的版本
- 用 `--precise` 向 `cargo update` 指定版本

更多细节见 [resolver](../specifying-dependencies/03-dependency-resolution/#rust-version) 章节。

> **MSRV：**
> - `allow` 任意版本支持
> - `fallback` 自 1.84 起生效

### `[registries]` {#registries}

`[registries]` 表用于指定额外[注册表][registries]。每个命名注册表对应一个子表。

#### `registries.<name>.index` {#registriesnameindex}
* 类型：字符串（url）
* 默认：无
* 环境变量：`CARGO_REGISTRIES_<name>_INDEX`

指定注册表索引的 URL。

#### `registries.<name>.token` {#registriesnametoken}
* 类型：字符串
* 默认：无
* 环境变量：`CARGO_REGISTRIES_<name>_TOKEN`

指定给定注册表的认证令牌。此值应仅出现在[凭据](#credentials)文件中。用于 [`cargo publish`] 等需要身份验证的注册表命令。

可用 `--token` 命令行选项覆盖。

#### `registries.<name>.credential-provider` {#registriesnamecredential-provider}
* 类型：字符串或路径与参数的数组
* 默认：无
* 环境变量：`CARGO_REGISTRIES_<name>_CREDENTIAL_PROVIDER`

指定给定注册表的凭据提供程序。若未设置，将使用 [`registry.global-credential-providers`](#registryglobal-credential-providers) 中的提供程序。

若指定为字符串，路径与参数会按空格拆分。路径或参数含空格时使用数组。

若值存在于 [`[credential-alias]`](#credential-alias) 表中，将使用该别名。

更多信息见[注册表身份验证](../registries/registry-authentication/)。

#### `registries.crates-io.protocol` {#registriescrates-ioprotocol}
* 类型：字符串
* 默认：`"sparse"`
* 环境变量：`CARGO_REGISTRIES_CRATES_IO_PROTOCOL`

指定访问 crates.io 使用的协议。允许值为 `git` 或 `sparse`。

`git` 会使 Cargo 从 <https://github.com/rust-lang/crates.io-index/> 克隆曾在 crates.io 发布的所有包的完整索引。
这可能因索引体积带来性能影响。
`sparse` 是较新的协议，通过 HTTPS 从 <https://index.crates.io/> 仅下载必要内容。
在多数情况下解析新依赖时可显著提升性能。

关于注册表协议的更多信息见[注册表章节](../registries/)。

### `[registry]` {#registry}
`[registry]` 表控制未指定时使用的默认注册表。

#### `registry.index` {#registryindex}
此值不再接受，不应使用。

#### `registry.default` {#registrydefault}
* 类型：字符串
* 默认：`"crates-io"`
* 环境变量：`CARGO_REGISTRY_DEFAULT`

[`registries` 表](#registries)中注册表的名称，作为 [`cargo publish`] 等注册表命令的默认注册表。

可用 `--registry` 命令行选项覆盖。

#### `registry.credential-provider` {#registrycredential-provider}
* 类型：字符串或路径与参数的数组
* 默认：无
* 环境变量：`CARGO_REGISTRY_CREDENTIAL_PROVIDER`

指定 [crates.io] 的凭据提供程序。若未设置，将使用 [`registry.global-credential-providers`](#registryglobal-credential-providers) 中的提供程序。

若指定为字符串，路径与参数会按空格拆分。路径或参数含空格时使用数组。

若值存在于 `[credential-alias]` 表中，将使用该别名。

更多信息见[注册表身份验证](../registries/registry-authentication/)。

#### `registry.token` {#registrytoken}
* 类型：字符串
* 默认：无
* 环境变量：`CARGO_REGISTRY_TOKEN`

指定 [crates.io] 的认证令牌。此值应仅出现在[凭据](#credentials)文件中。用于 [`cargo publish`] 等需要身份验证的注册表命令。

可用 `--token` 命令行选项覆盖。

#### `registry.global-credential-providers` {#registryglobal-credential-providers}
* 类型：数组
* 默认：`["cargo:token"]`
* 环境变量：`CARGO_REGISTRY_GLOBAL_CREDENTIAL_PROVIDERS`

指定全局凭据提供程序列表。若未通过 `registries.<name>.credential-provider` 为特定注册表设置凭据提供程序，Cargo 将使用此列表中的提供程序。列表靠后的提供程序优先级更高。

路径与参数按空格拆分。若路径或参数含空格，应在 [`[credential-alias]`](#credential-alias) 表中定义凭据提供程序，并在此通过别名引用。

更多信息见[注册表身份验证](../registries/registry-authentication/)。

### `[source]` {#source}
`[source]` 表定义可用的注册表源。更多信息见[源替换]。每个命名源对应一个子表。源应只定义一种类型（directory、registry、local-registry 或 git）。

[源替换]: ../specifying-dependencies/02-source-replacement/

#### `source.<name>.replace-with` {#sourcenamereplace-with}
* 类型：字符串
* 默认：无
* 环境变量：不支持

若设置，用给定命名源或命名注册表替换此源。

#### `source.<name>.directory` {#sourcenamedirectory}
* 类型：字符串（路径）
* 默认：无
* 环境变量：不支持

设置用作目录源的目录路径。

#### `source.<name>.registry` {#sourcenameregistry}
* 类型：字符串（url）
* 默认：无
* 环境变量：不支持

设置注册表源的 URL。

#### `source.<name>.local-registry` {#sourcenamelocal-registry}
* 类型：字符串（路径）
* 默认：无
* 环境变量：不支持

设置用作本地注册表源的目录路径。

#### `source.<name>.git` {#sourcenamegit}
* 类型：字符串（url）
* 默认：无
* 环境变量：不支持

设置 git 仓库源的 URL。

#### `source.<name>.branch` {#sourcenamebranch}
* 类型：字符串
* 默认：无
* 环境变量：不支持

设置 git 仓库的分支名。

若未设置 `branch`、`tag` 或 `rev`，默认为 `master` 分支。

#### `source.<name>.tag` {#sourcenametag}
* 类型：字符串
* 默认：无
* 环境变量：不支持

设置 git 仓库的标签名。

若未设置 `branch`、`tag` 或 `rev`，默认为 `master` 分支。

#### `source.<name>.rev` {#sourcenamerev}
* 类型：字符串
* 默认：无
* 环境变量：不支持

设置 git 仓库使用的[修订版本][revision]。

若未设置 `branch`、`tag` 或 `rev`，默认为 `master` 分支。


### `[target]` {#target}
`[target]` 表用于为特定平台目标指定设置。子表可以是[平台三元组][target triple]或 [`cfg()` 表达式]。当目标平台匹配 `<triple>` 值或 `<cfg>` 表达式时，使用给定值。

```toml
[target.thumbv7m-none-eabi]
linker = "arm-none-eabi-gcc"
runner = "my-emulator"
rustflags = ["…", "…"]

[target.'cfg(all(target_arch = "arm", target_os = "none"))']
runner = "my-arm-wrapper"
rustflags = ["…", "…"]
```

`cfg` 值来自编译器内置项（运行 `rustc --print=cfg` 查看）以及传给 `rustc` 的额外 `--cfg` 标志（如 `RUSTFLAGS` 中定义的）。不要尝试匹配 `debug_assertions`、`test`、Cargo 特性如 `feature="foo"`，或[构建脚本]设置的值。

若使用目标规范 JSON 文件，[`<triple>`] 值为文件名主干。
例如 `--target foo/bar.json` 会匹配 `[target.bar]`。

#### `target.<triple>.ar` {#targettriplear}
此选项已弃用且未使用。

#### `target.<triple>.linker` {#targettriplelinker}
* 类型：字符串（程序路径）
* 默认：无
* 环境变量：`CARGO_TARGET_<triple>_LINKER`

指定编译 [`<triple>`] 时传给 `rustc` 的链接器（通过 [`-C linker`]）。默认不覆盖链接器。

#### `target.<cfg>.linker` {#targetcfglinker}
与[目标链接器](#targettriplelinker)类似，但使用 [`cfg()` 表达式]。若 [`<triple>`] 与 `<cfg>` 链接器均匹配，`<triple>` 优先。若有多个 `<cfg>` 链接器匹配当前目标则报错。

#### `target.<triple>.runner` {#targettriplerunner}
* 类型：字符串或字符串数组（[带参数的程序路径]）
* 默认：无
* 环境变量：`CARGO_TARGET_<triple>_RUNNER`

若提供 runner，目标 [`<triple>`] 的可执行文件将通过指定 runner 调用，实际可执行文件作为参数传入。适用于 [`cargo run`]、[`cargo test`] 与 [`cargo bench`] 命令。默认直接运行编译后的可执行文件。

#### `target.<cfg>.runner` {#targetcfgrunner}
与[目标 runner](#targettriplerunner)类似，但使用 [`cfg()` 表达式]。若 [`<triple>`] 与 `<cfg>` runner 均匹配，`<triple>` 优先。若有多个 `<cfg>` runner 匹配当前目标则报错。

#### `target.<triple>.rustflags` {#targettriplerustflags}
* 类型：字符串或字符串数组
* 默认：无
* 环境变量：`CARGO_TARGET_<triple>_RUSTFLAGS`

为此 [`<triple>`] 向编译器传递一组自定义标志。
值可以是字符串数组或空格分隔的字符串。

关于指定额外标志的不同方式，见 [`build.rustflags`](#buildrustflags)。

#### `target.<cfg>.rustflags` {#targetcfgrustflags}
与[目标 rustflags](#targettriplerustflags)类似，但使用 [`cfg()` 表达式]。若多个 `<cfg>` 与 [`<triple>`] 项匹配当前目标，标志会拼接。

#### `target.<triple>.rustdocflags` {#targettriplerustdocflags}
* 类型：字符串或字符串数组
* 默认：无
* 环境变量：`CARGO_TARGET_<triple>_RUSTDOCFLAGS`

为此 [`<triple>`] 向编译器传递一组自定义标志。
值可以是字符串数组或空格分隔的字符串。

关于指定额外标志的不同方式，见 [`build.rustdocflags`](#buildrustdocflags)。

#### `target.<cfg>.rustdocflags` {#targetcfgrustdocflags}
与[目标 rustdocflags](#targettriplerustdocflags)类似，但使用 [`cfg()` 表达式]。若多个 `<cfg>` 与 [`<triple>`] 项匹配当前目标，标志会拼接。

#### `target.<triple>.<links>` {#targettriplelinks}
links 子表提供[覆盖构建脚本]的方式。指定后，给定 `links` 库的构建脚本不会运行，而是使用给定值。

```toml
[target.x86_64-unknown-linux-gnu.foo]
rustc-link-lib = ["foo"]
rustc-link-search = ["/path/to/foo"]
rustc-flags = "-L /some/path"
rustc-cfg = ['key="value"']
rustc-env = {key = "value"}
rustc-cdylib-link-arg = ["…"]
metadata_key1 = "value"
metadata_key2 = "value"
```

### `[term]` {#term}
`[term]` 表控制终端输出与交互。

#### `term.quiet` {#termquiet}
* 类型：布尔
* 默认：false
* 环境变量：`CARGO_TERM_QUIET`

控制 Cargo 是否显示日志消息。

指定 `--quiet` 标志会覆盖并强制静默输出。
指定 `--verbose` 标志会覆盖并禁用静默输出。

#### `term.verbose` {#termverbose}
* 类型：布尔
* 默认：false
* 环境变量：`CARGO_TERM_VERBOSE`

控制 Cargo 是否显示额外详细消息。

指定 `--quiet` 标志会覆盖并禁用详细输出。
指定 `--verbose` 标志会覆盖并强制详细输出。

#### `term.color` {#termcolor}
* 类型：字符串
* 默认：`"auto"`
* 环境变量：`CARGO_TERM_COLOR`

控制终端是否使用彩色输出。可能值：

* `auto`（默认）：自动检测终端是否支持彩色。
* `always`：始终显示彩色。
* `never`：从不显示彩色。

可用 `--color` 命令行选项覆盖。

#### `term.hyperlinks` {#termhyperlinks}
* 类型：布尔
* 默认：自动检测
* 环境变量：`CARGO_TERM_HYPERLINKS`

控制终端是否使用超链接。

#### `term.unicode` {#termunicode}
* 类型：布尔
* 默认：自动检测
* 环境变量：`CARGO_TERM_UNICODE`

控制输出是否可用非 ASCII Unicode 字符渲染。

#### `term.progress.when` {#termprogresswhen}
* 类型：字符串
* 默认：`"auto"`
* 环境变量：`CARGO_TERM_PROGRESS_WHEN`

控制终端是否显示进度条。可能值：

* `auto`（默认）：智能判断是否显示进度条。
* `always`：始终显示进度条。
* `never`：从不显示进度条。

#### `term.progress.width` {#termprogresswidth}
* 类型：整数
* 默认：无
* 环境变量：`CARGO_TERM_PROGRESS_WIDTH`

设置进度条宽度。

#### `term.progress.term-integration` {#termprogressterm-integration}
* 类型：布尔
* 默认：自动检测
* 环境变量：`CARGO_TERM_PROGRESS_TERM_INTEGRATION`

向终端模拟器报告进度，以便在任务栏等位置显示。

[`cargo bench`]: ../../cargo-commands/build-commands/01-cargo-bench/
[`cargo login`]: ../../cargo-commands/publishing-commands/01-cargo-login/
[`cargo logout`]: ../../cargo-commands/publishing-commands/02-cargo-logout/
[`cargo doc`]: ../../cargo-commands/build-commands/06-cargo-doc/
[`cargo new`]: ../../cargo-commands/package-commands/03-cargo-new/
[`cargo publish`]: ../../cargo-commands/publishing-commands/05-cargo-publish/
[`cargo run`]: ../../cargo-commands/build-commands/11-cargo-run/
[`cargo rustc`]: ../../cargo-commands/build-commands/12-cargo-rustc/
[`cargo test`]: ../../cargo-commands/build-commands/14-cargo-test/
[`cargo rustdoc`]: ../../cargo-commands/build-commands/13-cargo-rustdoc/
[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/
[env]: ../07-environment-variables/
[`cfg()` 表达式]: https://doc.rust-lang.org/reference/conditional-compilation.html
[构建脚本]: ../build-scripts/
[`-C linker`]: https://doc.rust-lang.org/rustc/codegen-options/index.html#linker
[覆盖构建脚本]: ../build-scripts/#overriding-build-scripts
[toml]: https://toml.io/
[增量编译]: ../05-profiles/#incremental
[带参数的程序路径]: #executable-paths-with-arguments
[libcurl 格式]: https://everything.curl.dev/transfers/conn/proxies#proxy-types
[revision]: https://git-scm.com/docs/gitrevisions
[registries]: ../registries/
[`cargo:token`]: ../registries/registry-authentication/#cargotoken
[crates.io]: https://crates.io/
[target triple]: ../../appendix/01-glossary/#target
[`<triple>`]: ../../appendix/01-glossary/#target
