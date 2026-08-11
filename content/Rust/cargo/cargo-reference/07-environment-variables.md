+++
title = "07-环境变量"
date = 2026-07-30T14:49:00+08:00
weight = 43
type = "docs"
description = "Cargo 识别的环境变量一览"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The Cargo Book](https://doc.rust-lang.org/cargo/)

# 环境变量 {#environment-variables}


> 原文链接: [https://doc.rust-lang.org/cargo/reference/environment-variables.html](https://doc.rust-lang.org/cargo/reference/environment-variables.html)


Cargo 会设置并读取若干环境变量，你的代码可以检测或覆盖它们。以下按 Cargo 与之交互的时机，列出 Cargo 设置的环境变量：

## Cargo 读取的环境变量 {#environment-variables-cargo-reads}
你可以覆盖这些环境变量，以改变 Cargo 在你系统上的行为：

* `CARGO_LOG` --- Cargo 使用 [`tracing`] crate 显示调试日志消息。可将 `CARGO_LOG` 环境变量设为 `trace`、`debug` 或 `warn` 等值以启用调试日志。通常仅在调试时使用。更多细节见[调试日志][Debug logging]。
* `CARGO_HOME` --- Cargo 在本地缓存 registry 索引与 crate 的 git 检出。默认存放在 `$HOME/.cargo`（Windows 上为 `%USERPROFILE%\.cargo`），此变量可覆盖该目录位置。crate 一旦被缓存，`clean` 命令不会将其移除。更多细节见[指南](../../cargo-guide/10-cargo-home/)。
* `CARGO_TARGET_DIR` --- 所有生成产物的存放位置，相对于当前工作目录。也可通过 [`build.target-dir`] 在配置中设置。
* `CARGO` --- 若已设置，Cargo 在构建 crate、执行构建脚本及外部子命令时会转发该值，而不是使用其自动检测到的路径。Cargo 不会直接执行该值，它应始终指向与 `cargo` 行为完全一致的命令，因为使用该变量的用户会期望如此。
* `RUSTC` --- Cargo 将执行此指定的编译器，而不是运行 `rustc`。也可通过 [`build.rustc`] 在配置中设置。
* `RUSTC_WRAPPER` --- Cargo 将执行此指定的包装器，而不是直接运行 `rustc`；包装器的命令行参数为 rustc 调用，第一个参数为实际 rustc 的路径。可用于设置 `sccache` 等构建缓存工具。也可通过 [`build.rustc-wrapper`] 在配置中设置。设为空字符串会覆盖配置，使 cargo 不再使用包装器。
* `RUSTC_WORKSPACE_WRAPPER` --- 对于工作空间成员，Cargo 将执行此指定的包装器，而不是直接运行 `rustc`；包装器的命令行参数为 rustc 调用，第一个参数为实际 rustc 的路径。在不含工作空间的单包项目中，该包被视为工作空间。它会影响文件名哈希，使包装器产生的产物单独缓存。也可通过 [`build.rustc-workspace-wrapper`] 在配置中设置。设为空字符串会覆盖配置，使 cargo 不再对工作空间成员使用包装器。若同时设置了 `RUSTC_WRAPPER` 与 `RUSTC_WORKSPACE_WRAPPER`，它们会嵌套：最终调用为 `$RUSTC_WRAPPER $RUSTC_WORKSPACE_WRAPPER $RUSTC`。
* `RUSTDOC` --- Cargo 将执行此指定的 `rustdoc` 实例，而不是运行 `rustdoc`。也可通过 [`build.rustdoc`] 在配置中设置。
* `RUSTDOCFLAGS` --- 传给 Cargo 执行的所有 `rustdoc` 调用的自定义标志的空格分隔列表。与 [`cargo rustdoc`] 不同，这适用于向*所有* `rustdoc` 实例传递标志。更多设置方式见 [`build.rustdocflags`]。该字符串按空白分割；若要更稳健地编码多个参数，见 `CARGO_ENCODED_RUSTDOCFLAGS`。
* `CARGO_ENCODED_RUSTDOCFLAGS` --- 传给 Cargo 执行的所有 `rustdoc` 调用的自定义标志列表，以 `0x1f`（ASCII 单元分隔符）分隔。
* `RUSTFLAGS` --- 传给 Cargo 执行的所有编译器调用的自定义标志的空格分隔列表。与 [`cargo rustc`] 不同，这适用于向*所有*编译器实例传递标志。更多设置方式见 [`build.rustflags`]。该字符串按空白分割；若要更稳健地编码多个参数，见 `CARGO_ENCODED_RUSTFLAGS`。
* `CARGO_ENCODED_RUSTFLAGS` --- 传给 Cargo 执行的所有编译器调用的自定义标志列表，以 `0x1f`（ASCII 单元分隔符）分隔。
* `CARGO_INCREMENTAL` --- 设为 1 时，Cargo 会强制为当前编译启用[增量编译][incremental compilation]；设为 0 时强制禁用。若未设置此环境变量，则使用 cargo 的默认值。另见 [`build.incremental`] 配置项。
* `CARGO_CACHE_RUSTC_INFO` --- 设为 0 时，Cargo 不会尝试缓存编译器版本信息。
* `HTTPS_PROXY` 或 `https_proxy` 或 `http_proxy` --- 使用的 HTTP 代理，更多细节见 [`http.proxy`]。
* `HTTP_TIMEOUT` --- HTTP 超时（秒），更多细节见 [`http.timeout`]。
* `TERM` --- 设为 `dumb` 时禁用进度条。
* `BROWSER` --- 使用 [`cargo doc`] 的 `--open` 标志打开文档时执行的 Web 浏览器，更多细节见 [`doc.browser`]。
* `RUSTFMT` --- [`cargo fmt`](https://github.com/rust-lang/rustfmt) 将执行此指定的 `rustfmt` 实例，而不是运行 `rustfmt`。

### 配置环境变量 {#configuration-environment-variables}
Cargo 会读取部分配置值对应的环境变量。更多细节见[配置章节][config-env]。支持的环境变量汇总如下：

* `CARGO_ALIAS_<name>` --- 命令别名，见 [`alias`]。
* `CARGO_BUILD_JOBS` --- 并行任务数，见 [`build.jobs`]。
* `CARGO_BUILD_RUSTC` --- `rustc` 可执行文件，见 [`build.rustc`]。
* `CARGO_BUILD_RUSTC_WRAPPER` --- `rustc` 包装器，见 [`build.rustc-wrapper`]。
* `CARGO_BUILD_RUSTC_WORKSPACE_WRAPPER` --- 仅用于工作空间成员的 `rustc` 包装器，见 [`build.rustc-workspace-wrapper`]。
* `CARGO_BUILD_RUSTDOC` --- `rustdoc` 可执行文件，见 [`build.rustdoc`]。
* `CARGO_BUILD_TARGET` --- 默认目标平台，见 [`build.target`]。
* `CARGO_BUILD_TARGET_DIR` --- 默认输出目录，见 [`build.target-dir`]。
* `CARGO_BUILD_BUILD_DIR` --- 默认构建目录，见 [`build.build-dir`]。
* `CARGO_BUILD_RUSTFLAGS` --- 额外的 `rustc` 标志，见 [`build.rustflags`]。
* `CARGO_BUILD_RUSTDOCFLAGS` --- 额外的 `rustdoc` 标志，见 [`build.rustdocflags`]。
* `CARGO_BUILD_INCREMENTAL` --- 增量编译，见 [`build.incremental`]。
* `CARGO_BUILD_DEP_INFO_BASEDIR` --- dep-info 相对目录，见 [`build.dep-info-basedir`]。
* `CARGO_CACHE_AUTO_CLEAN_FREQUENCY` --- 配置自动缓存清理的运行频率，见 [`cache.auto-clean-frequency`]。
* `CARGO_CARGO_NEW_VCS` --- 使用 [`cargo new`] 时的默认版本控制系统，见 [`cargo-new.vcs`]。
* `CARGO_FUTURE_INCOMPAT_REPORT_FREQUENCY` --- 未来不兼容报告通知的生成频率，见 [`future-incompat-report.frequency`]。
* `CARGO_HTTP_DEBUG` --- 启用 HTTP 调试，见 [`http.debug`]。
* `CARGO_HTTP_PROXY` --- 启用 HTTP 代理，见 [`http.proxy`]。
* `CARGO_HTTP_TIMEOUT` --- HTTP 超时，见 [`http.timeout`]。
* `CARGO_HTTP_CAINFO` --- TLS 证书颁发机构（CA）文件，见 [`http.cainfo`]。
* `CARGO_HTTP_PROXY_CAINFO` --- 代理 TLS 证书 CA 文件，见 [`http.proxy-cainfo`]。
* `CARGO_HTTP_CHECK_REVOKE` --- 禁用 TLS 证书吊销检查，见 [`http.check-revoke`]。
* `CARGO_HTTP_SSL_VERSION` --- 使用的 TLS 版本，见 [`http.ssl-version`]。
* `CARGO_HTTP_LOW_SPEED_LIMIT` --- HTTP 低速限制，见 [`http.low-speed-limit`]。
* `CARGO_HTTP_MULTIPLEXING` --- 是否使用 HTTP/2 多路复用，见 [`http.multiplexing`]。
* `CARGO_HTTP_USER_AGENT` --- HTTP User-Agent 头，见 [`http.user-agent`]。
* `CARGO_INSTALL_ROOT` --- [`cargo install`] 的默认目录，见 [`install.root`]。
* `CARGO_NET_RETRY` --- 网络错误重试次数，见 [`net.retry`]。
* `CARGO_NET_GIT_FETCH_WITH_CLI` --- 启用使用 `git` 可执行文件进行 fetch，见 [`net.git-fetch-with-cli`]。
* `CARGO_NET_OFFLINE` --- 离线模式，见 [`net.offline`]。
* `CARGO_PROFILE_<name>_BUILD_OVERRIDE_<key>` --- 覆盖构建脚本配置文件，见 [`profile.<name>.build-override`]。
* `CARGO_PROFILE_<name>_CODEGEN_UNITS` --- 设置代码生成单元数，见 [`profile.<name>.codegen-units`]。
* `CARGO_PROFILE_<name>_DEBUG` --- 包含何种调试信息，见 [`profile.<name>.debug`]。
* `CARGO_PROFILE_<name>_DEBUG_ASSERTIONS` --- 启用/禁用调试断言，见 [`profile.<name>.debug-assertions`]。
* `CARGO_PROFILE_<name>_INCREMENTAL` --- 启用/禁用增量编译，见 [`profile.<name>.incremental`]。
* `CARGO_PROFILE_<name>_LTO` --- 链接时优化，见 [`profile.<name>.lto`]。
* `CARGO_PROFILE_<name>_OVERFLOW_CHECKS` --- 启用/禁用溢出检查，见 [`profile.<name>.overflow-checks`]。
* `CARGO_PROFILE_<name>_OPT_LEVEL` --- 设置优化级别，见 [`profile.<name>.opt-level`]。
* `CARGO_PROFILE_<name>_PANIC` --- 使用的 panic 策略，见 [`profile.<name>.panic`]。
* `CARGO_PROFILE_<name>_RPATH` --- rpath 链接选项，见 [`profile.<name>.rpath`]。
* `CARGO_PROFILE_<name>_SPLIT_DEBUGINFO` --- 控制调试文件输出行为，见 [`profile.<name>.split-debuginfo`]。
* `CARGO_PROFILE_<name>_STRIP` --- 控制符号和/或调试信息的剥离，见 [`profile.<name>.strip`]。
* `CARGO_REGISTRIES_<name>_CREDENTIAL_PROVIDER` --- registry 的凭证提供程序，见 [`registries.<name>.credential-provider`]。
* `CARGO_REGISTRIES_<name>_INDEX` --- registry 索引 URL，见 [`registries.<name>.index`]。
* `CARGO_REGISTRIES_<name>_TOKEN` --- registry 认证令牌，见 [`registries.<name>.token`]。
* `CARGO_REGISTRY_CREDENTIAL_PROVIDER` --- [crates.io] 的凭证提供程序，见 [`registry.credential-provider`]。
* `CARGO_REGISTRY_DEFAULT` --- `--registry` 标志的默认 registry，见 [`registry.default`]。
* `CARGO_REGISTRY_GLOBAL_CREDENTIAL_PROVIDERS` --- 未定义特定提供程序的 registry 的全局凭证提供程序。见 [`registry.global-credential-providers`]。
* `CARGO_REGISTRY_TOKEN` --- [crates.io] 的认证令牌，见 [`registry.token`]。
* `CARGO_TARGET_<triple>_LINKER` --- 使用的链接器，见 [`target.<triple>.linker`]。triple 必须[转换为大写和下划线](../06-configuration/#environment-variables)。
* `CARGO_TARGET_<triple>_RUNNER` --- 可执行文件运行器，见 [`target.<triple>.runner`]。
* `CARGO_TARGET_<triple>_RUSTFLAGS` --- 针对某目标的额外 `rustc` 标志，见 [`target.<triple>.rustflags`]。
* `CARGO_TERM_QUIET` --- 安静模式，见 [`term.quiet`]。
* `CARGO_TERM_VERBOSE` --- 默认终端详细程度，见 [`term.verbose`]。
* `CARGO_TERM_COLOR` --- 默认颜色模式，见 [`term.color`]。
* `CARGO_TERM_PROGRESS_WHEN` --- 默认进度条显示模式，见 [`term.progress.when`]。
* `CARGO_TERM_PROGRESS_WIDTH` --- 默认进度条宽度，见 [`term.progress.width`]。

[`cargo doc`]: ../../cargo-commands/build-commands/06-cargo-doc/
[`cargo install`]: ../../cargo-commands/package-commands/02-cargo-install/
[`cargo new`]: ../../cargo-commands/package-commands/03-cargo-new/
[`cargo rustc`]: ../../cargo-commands/build-commands/12-cargo-rustc/
[`cargo rustdoc`]: ../../cargo-commands/build-commands/13-cargo-rustdoc/
[config-env]: ../06-configuration/#environment-variables
[crates.io]: https://crates.io/
[incremental compilation]: ../05-profiles/#incremental
[`alias`]: ../06-configuration/#alias
[`build.jobs`]: ../06-configuration/#buildjobs
[`build.rustc`]: ../06-configuration/#buildrustc
[`build.rustc-wrapper`]: ../06-configuration/#buildrustc-wrapper
[`build.rustc-workspace-wrapper`]: ../06-configuration/#buildrustc-workspace-wrapper
[`build.rustdoc`]: ../06-configuration/#buildrustdoc
[`build.target`]: ../06-configuration/#buildtarget
[`build.target-dir`]: ../06-configuration/#buildtarget-dir
[`build.build-dir`]: ../06-configuration/#buildbuild-dir
[`build.rustflags`]: ../06-configuration/#buildrustflags
[`build.rustdocflags`]: ../06-configuration/#buildrustdocflags
[`build.incremental`]: ../06-configuration/#buildincremental
[`build.dep-info-basedir`]: ../06-configuration/#builddep-info-basedir
[`doc.browser`]: ../06-configuration/#docbrowser
[`cache.auto-clean-frequency`]: ../06-configuration/#cacheauto-clean-frequency
[`cargo-new.name`]: ../06-configuration/#cargo-newname
[`cargo-new.email`]: ../06-configuration/#cargo-newemail
[`cargo-new.vcs`]: ../06-configuration/#cargo-newvcs
[`future-incompat-report.frequency`]: ../06-configuration/#future-incompat-reportfrequency
[`http.debug`]: ../06-configuration/#httpdebug
[`http.proxy`]: ../06-configuration/#httpproxy
[`http.timeout`]: ../06-configuration/#httptimeout
[`http.cainfo`]: ../06-configuration/#httpcainfo
[`http.proxy-cainfo`]: ../06-configuration/#httpproxy-cainfo
[`http.check-revoke`]: ../06-configuration/#httpcheck-revoke
[`http.ssl-version`]: ../06-configuration/#httpssl-version
[`http.low-speed-limit`]: ../06-configuration/#httplow-speed-limit
[`http.multiplexing`]: ../06-configuration/#httpmultiplexing
[`http.user-agent`]: ../06-configuration/#httpuser-agent
[`install.root`]: ../06-configuration/#installroot
[`net.retry`]: ../06-configuration/#netretry
[`net.git-fetch-with-cli`]: ../06-configuration/#netgit-fetch-with-cli
[`net.offline`]: ../06-configuration/#netoffline
[`profile.<name>.build-override`]: ../06-configuration/#profilenamebuild-override
[`profile.<name>.codegen-units`]: ../06-configuration/#profilenamecodegen-units
[`profile.<name>.debug`]: ../06-configuration/#profilenamedebug
[`profile.<name>.debug-assertions`]: ../06-configuration/#profilenamedebug-assertions
[`profile.<name>.incremental`]: ../06-configuration/#profilenameincremental
[`profile.<name>.lto`]: ../06-configuration/#profilenamelto
[`profile.<name>.overflow-checks`]: ../06-configuration/#profilenameoverflow-checks
[`profile.<name>.opt-level`]: ../06-configuration/#profilenameopt-level
[`profile.<name>.panic`]: ../06-configuration/#profilenamepanic
[`profile.<name>.rpath`]: ../06-configuration/#profilenamerpath
[`profile.<name>.split-debuginfo`]: ../06-configuration/#profilenamesplit-debuginfo
[`profile.<name>.strip`]: ../06-configuration/#profilenamestrip
[`registries.<name>.credential-provider`]: ../06-configuration/#registriesnamecredential-provider
[`registries.<name>.index`]: ../06-configuration/#registriesnameindex
[`registries.<name>.token`]: ../06-configuration/#registriesnametoken
[`registry.credential-provider`]: ../06-configuration/#registrycredential-provider
[`registry.default`]: ../06-configuration/#registrydefault
[`registry.global-credential-providers`]: ../06-configuration/#registryglobal-credential-providers
[`registry.token`]: ../06-configuration/#registrytoken
[`target.<triple>.linker`]: ../06-configuration/#targettriplelinker
[`target.<triple>.runner`]: ../06-configuration/#targettriplerunner
[`target.<triple>.rustflags`]: ../06-configuration/#targettriplerustflags
[`term.quiet`]: ../06-configuration/#termquiet
[`term.verbose`]: ../06-configuration/#termverbose
[`term.color`]: ../06-configuration/#termcolor
[`term.progress.when`]: ../06-configuration/#termprogresswhen
[`term.progress.width`]: ../06-configuration/#termprogresswidth

## Cargo 为 crate 设置的环境变量 {#environment-variables-cargo-sets-for-crates}

Cargo 在编译 crate 时会向 crate 暴露这些环境变量。注意，使用 `cargo run` 和 `cargo test` 运行二进制文件时同样适用。要在 Rust 程序中获取这些变量中的任一值，可以这样做：

```rust,ignore
let version = env!("CARGO_PKG_VERSION");
```

此时 `version` 将包含 `CARGO_PKG_VERSION` 的值。

注意，若 manifest 中未提供某个值，对应的环境变量会被设为空字符串 `""`。

* `CARGO` --- 执行构建的 `cargo` 二进制文件路径。
* `CARGO_MANIFEST_DIR` --- 包含包 manifest 的目录。
* `CARGO_MANIFEST_PATH` --- 包 manifest 的路径。
* `CARGO_PKG_VERSION` --- 包的完整版本。
* `CARGO_PKG_VERSION_MAJOR` --- 包的主版本号。
* `CARGO_PKG_VERSION_MINOR` --- 包的次版本号。
* `CARGO_PKG_VERSION_PATCH` --- 包的补丁版本号。
* `CARGO_PKG_VERSION_PRE` --- 包的预发布版本。
* `CARGO_PKG_AUTHORS` --- 包 manifest 中作者列表，以冒号分隔。
* `CARGO_PKG_NAME` --- 包的名称。
* `CARGO_PKG_DESCRIPTION` --- 包 manifest 中的描述。
* `CARGO_PKG_HOMEPAGE` --- 包 manifest 中的主页。
* `CARGO_PKG_REPOSITORY` --- 包 manifest 中的仓库。
* `CARGO_PKG_LICENSE` --- 包 manifest 中的许可证。
* `CARGO_PKG_LICENSE_FILE` --- 包 manifest 中的许可证文件。
* `CARGO_PKG_RUST_VERSION` --- 包 manifest 中的 Rust 版本。注意，这是包支持的最低 Rust 版本，而非当前 Rust 版本。
* `CARGO_PKG_README` --- 包 README 文件的路径。
* `CARGO_CRATE_NAME` --- 当前正在编译的 crate 名称。它是 [Cargo 目标][Cargo target] 的名称，其中 `-` 转换为 `_`，例如库、二进制、示例、集成测试或 benchmark 的名称。
* `CARGO_BIN_NAME` --- 当前正在编译的二进制文件名称。仅对[二进制文件][binaries]或二进制[示例][examples]设置。此名称不包含 `.exe` 等文件扩展名。
* `OUT_DIR` --- 若包有构建脚本，则设为构建脚本应放置输出的文件夹。更多信息见下文。（仅在编译期间设置。）Cargo 不保证该目录为空，且构建之间不会清理。
* `CARGO_BIN_EXE_<name>` --- 二进制目标可执行文件的绝对路径。仅在构建[集成测试][integration test]或 benchmark 时设置。可与 [`env` 宏][`env` macro] 配合使用，以查找用于测试的可执行文件。`<name>` 为二进制目标的名称，原样使用。例如，名为 `my-program` 的二进制文件对应 `CARGO_BIN_EXE_my-program`。除非二进制文件有未启用的必需特性，否则在构建测试时会自动构建二进制文件。
* `CARGO_PRIMARY_PACKAGE` --- 若正在构建的包是主包（primary），则设置此环境变量。主包是用户在命令行上选择的包，通过 `-p` 标志或基于当前目录与默认工作空间成员的默认值。构建依赖时不会设置此变量，除非依赖同时也是在命令行上选择的工作空间成员。仅在编译包时设置（运行二进制文件或测试时不设置）。
* `CARGO_TARGET_TMPDIR` --- 仅在构建[集成测试][integration test]或 benchmark 代码时设置。这是 target 目录内的路径，集成测试或 benchmark 可在此自由放置测试/bench 所需的任何数据。Cargo 会初始创建此目录，但不以任何方式管理其内容，由测试代码负责。

[Cargo target]: ../the-manifest-format/01-cargo-targets/
[binaries]: ../the-manifest-format/01-cargo-targets/#binaries
[examples]: ../the-manifest-format/01-cargo-targets/#examples
[integration test]: ../the-manifest-format/01-cargo-targets/#integration-tests
[`env` macro]: https://doc.rust-lang.org/std/macro.env.html

### 动态库路径 {#dynamic-library-paths}

Cargo 在使用 `cargo run`、`cargo test` 等命令编译和运行二进制文件时，也会设置动态库路径。这有助于定位构建过程中涉及的共享库。变量名取决于平台：

* Windows：`PATH`
* macOS：`DYLD_FALLBACK_LIBRARY_PATH`
* Unix：`LD_LIBRARY_PATH`
* AIX：`LIBPATH`

Cargo 启动时会从现有值扩展该值。macOS 有特殊处理：若尚未设置 `DYLD_FALLBACK_LIBRARY_PATH`，会添加默认的 `$HOME/lib:/usr/local/lib:/usr/lib`。

Cargo 包含以下路径：

* 通过 [`rustc-link-search` 指令](../build-scripts/#rustc-link-search)从任何构建脚本包含的搜索路径。`target` 目录外的路径会被移除。若系统上其他库需要在搜索路径中，运行 Cargo 的用户有责任正确设置环境。
* 基础输出目录（如 `target/debug`）及 `deps` 目录。这主要用于支持 proc-macro。
* rustc sysroot 库路径。对大多数用户通常不重要。

## Cargo 为构建脚本设置的环境变量 {#environment-variables-cargo-sets-for-build-scripts}

Cargo 运行构建脚本时会设置若干环境变量。由于构建脚本编译时这些变量尚未设置，上述使用 `env!` 的示例无效，而需要在构建脚本运行时获取值：

```rust,ignore
use std::env;
let out_dir = env::var("OUT_DIR").unwrap();
```

此时 `out_dir` 将包含 `OUT_DIR` 的值。

* `CARGO` --- 执行构建的 `cargo` 二进制文件路径。
* `CARGO_MANIFEST_DIR` --- 正在构建的包（包含构建脚本的包）的 manifest 所在目录。注意，这也是构建脚本启动时的当前工作目录。
* `CARGO_MANIFEST_PATH` --- 包 manifest 的路径。
* `CARGO_MANIFEST_LINKS` --- manifest 的 `links` 值。
* `CARGO_MAKEFLAGS` --- 包含 Cargo [jobserver] 实现并行化子进程所需的参数。build.rs 中的 rustc 或 cargo 调用已可读取 `CARGO_MAKEFLAGS`，但 GNU Make 要求标志直接作为参数或通过 `MAKEFLAGS` 环境变量指定。目前 Cargo 不设置 `MAKEFLAGS` 变量，但调用 GNU Make 的构建脚本可将其设为 `CARGO_MAKEFLAGS` 的内容。
* `CARGO_FEATURE_<name>` --- 对于正在构建的包中每个已激活的特性，会存在此环境变量，其中 `<name>` 为特性名称的大写形式，且 `-` 转换为 `_`。
* `CARGO_CFG_<cfg>` --- 对于正在构建的包中每个[配置选项][configuration]，此环境变量包含配置的值，其中 `<cfg>` 为配置名称的大写形式，且 `-` 转换为 `_`。布尔配置若已设置则存在，否则不存在。多值配置会合并为单个变量，值以 `,` 分隔。这包括编译器内置值（可通过 `rustc --print=cfg` 查看）以及构建脚本和传给 `rustc` 的额外标志（如 `RUSTFLAGS` 中定义的）设置的值。这些变量的一些示例如下：
    * `CARGO_CFG_FEATURE` --- 正在构建的包中每个已激活的特性。
    * `CARGO_CFG_UNIX` --- 在 [类 Unix 平台][unix-like platforms] 上设置。
    * `CARGO_CFG_WINDOWS` --- 在 [类 Windows 平台][windows-like platforms] 上设置。
    * `CARGO_CFG_TARGET_FAMILY=unix,wasm` --- [目标族][target family]。
    * `CARGO_CFG_TARGET_OS=macos` --- [目标操作系统][target operating system]。
    * `CARGO_CFG_TARGET_ARCH=x86_64` --- CPU [目标架构][target architecture]。
    * `CARGO_CFG_TARGET_VENDOR=apple` --- [目标厂商][target vendor]。
    * `CARGO_CFG_TARGET_ENV=gnu` --- [目标环境][target environment] ABI。
    * `CARGO_CFG_TARGET_ABI=eabihf` --- [目标 ABI][target ABI]。
    * `CARGO_CFG_TARGET_POINTER_WIDTH=64` --- CPU [指针宽度][pointer width]。
    * `CARGO_CFG_TARGET_ENDIAN=little` --- CPU [目标字节序][target endianness]。
    * `CARGO_CFG_TARGET_FEATURE=mmx,sse` --- 已启用的 CPU [目标特性][target features] 列表。
  > 注意，不同[目标 triple][Target Triple] 有不同的 `cfg` 值集合，因此一个目标 triple 中存在的变量在另一个中可能不可用。
  >
  > 某些 cfg 值（如 `test`）不可用。
  >
  > **提示：** 若要类型化 API 读取这些值，考虑使用 [`build-rs`] crate，而不是手动解析环境变量。另请注意，构建脚本中应使用 `CARGO_CFG_*` 变量，而不是 `cfg!` 宏或 `#[cfg]` 属性，后者检查的是*主机*平台，而非*目标*平台。
* `OUT_DIR` --- 应放置所有输出和中间产物的文件夹。此文件夹位于正在构建的包的构建目录内，且对该包唯一。Cargo 在构建之间不会清理或重置此目录，其内容可能在重建之间保留。构建脚本不应假设 `OUT_DIR` 为空，并负责管理或清理其创建的文件。
* `TARGET` --- 正在编译的目标 triple。原生代码应为此 triple 编译。更多信息见[目标 Triple][Target Triple] 说明。
* `HOST` --- Rust 编译器的主机 triple。
* `NUM_JOBS` --- 顶层并行度。可用于向 `make` 等系统传递 `-j` 参数。注意解读此环境变量时应谨慎。出于历史原因仍会提供，但较新版本的 Cargo 例如不需要运行 `make -j`，而可将 `MAKEFLAGS` 环境变量设为 `CARGO_MAKEFLAGS` 的内容，以在子 make 调用中启用 Cargo 的 GNU Make 兼容 [jobserver]。
* `DEBUG` --- 若将生成任何 [`debug`] 信息则为 `true`，否则为 `false`。
* `OPT_LEVEL` --- 当前正在构建的配置文件对应的 [`opt-level`] 变量值。
* `PROFILE` --- release 构建为 `release`，其他构建为 `debug`。这基于[配置文件][profile]是否继承自 [`dev`] 或 [`release`] 配置文件。不推荐使用此环境变量。使用 `OPT_LEVEL` 等其他环境变量能更准确地反映实际使用的设置。
* `DEP_<links>_<key>` --- 关于这组环境变量的更多信息，见构建脚本文档中的 [`links`][links]。
* `RUSTC`、`RUSTDOC` --- Cargo 解析使用的编译器和文档生成器，传给构建脚本以便其同样使用。
* `RUSTC_WRAPPER` --- Cargo 使用的 `rustc` 包装器（若有）。见 [`build.rustc-wrapper`]。
* `RUSTC_WORKSPACE_WRAPPER` --- Cargo 对工作空间成员使用的 `rustc` 包装器（若有）。见 [`build.rustc-workspace-wrapper`]。
* `RUSTC_LINKER` --- Cargo 为当前目标解析使用的链接器二进制文件路径（若已指定）。链接器可通过编辑 `.cargo/config.toml` 更改；更多信息见 [cargo 配置][cargo-config] 文档。
* `CARGO_ENCODED_RUSTFLAGS` --- Cargo 调用 `rustc` 时使用的额外标志，以 `0x1f` 字符（ASCII 单元分隔符）分隔。见 [`build.rustflags`]。注意，自 Rust 1.55 起，`RUSTFLAGS` 会从环境中移除；脚本应改用 `CARGO_ENCODED_RUSTFLAGS`。
* `CARGO_PKG_<var>` --- 包信息变量，名称和值与 [crate 构建期间提供的变量][variables set for crates] 相同。

[`tracing`]: https://docs.rs/tracing
[Debug logging]: https://doc.crates.io/contrib/implementation/debugging.html#logging
[unix-like platforms]: https://doc.rust-lang.org/reference/conditional-compilation.html#unix-and-windows
[windows-like platforms]: https://doc.rust-lang.org/reference/conditional-compilation.html#unix-and-windows
[target family]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_family
[target operating system]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_os
[target architecture]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_arch
[target vendor]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_vendor
[target environment]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_env
[target ABI]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_abi
[pointer width]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_pointer_width
[target endianness]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_endian
[target features]: https://doc.rust-lang.org/reference/conditional-compilation.html#target_feature
[links]: ../build-scripts/#the-links-manifest-key
[configuration]: https://doc.rust-lang.org/reference/conditional-compilation.html
[jobserver]: https://www.gnu.org/software/make/manual/html_node/Job-Slots.html
[cargo-config]: ../06-configuration/
[Target Triple]: ../../appendix/01-glossary/#target
[variables set for crates]: #environment-variables-cargo-sets-for-crates
[profile]: ../05-profiles/
[`dev`]: ../05-profiles/#dev
[`release`]: ../05-profiles/#release
[`debug`]: ../05-profiles/#debug
[`opt-level`]: ../05-profiles/#opt-level
[`build-rs`]: https://crates.io/crates/build-rs

## Cargo 为 `cargo test` 设置的环境变量 {#environment-variables-cargo-sets-for-cargo-test}
Cargo 运行测试时会设置若干环境变量。可在测试运行时获取值：

```rust,ignore
use std::env;
let out_dir = env::var("CARGO_BIN_EXE_foo").unwrap();
```

* `CARGO_BIN_EXE_<name>` --- 二进制目标可执行文件的绝对路径。仅在运行[集成测试][integration test]或 benchmark 时设置。`<name>` 为二进制目标的名称，原样使用。例如，名为 `my-program` 的二进制文件对应 `CARGO_BIN_EXE_my-program`。除非二进制文件有未启用的必需特性，否则在构建测试时会自动构建二进制文件。

## Cargo 为第三方子命令设置的环境变量 {#environment-variables-cargo-sets-for-3rd-party-subcommands}
Cargo 向第三方子命令（即放在 `$PATH` 中、名为 `cargo-foobar` 的程序）暴露此环境变量：

* `CARGO` --- 执行构建的 `cargo` 二进制文件路径。
* `CARGO_MAKEFLAGS` --- 包含 Cargo [jobserver] 实现并行化子进程所需的参数。仅在 Cargo 检测到 jobserver 存在时设置。

有关环境的扩展信息，可运行 `cargo metadata`。
