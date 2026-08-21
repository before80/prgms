+++
title = "第1章 通用"
date = 2026-08-18T18:10:00+08:00
weight = 30
type = "docs"
description = "通用指南 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/universal/index.html](https://microsoft.github.io/rust-guidelines/guidelines/universal/index.html)

# 通用

## 遵循上游指南 (M-UPSTREAM-GUIDELINES) {#M-UPSTREAM-GUIDELINES}

*本条守护：代码库体现社区经验，且不令用户或贡献者意外。*

本书指南是对现有 Rust 指南的补充，尤其是：

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/checklist.html)
- [Rust Style Guide](https://doc.rust-lang.org/nightly/style-guide/)
- [Rust Design Patterns](https://rust-unofficial.github.io/patterns//intro.html)
- [Rust Reference - Undefined Behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

我们建议你一并阅读，并在本书条目之外同样加以落实。请特别留意下列条目，它们经常被遗忘：

- [ ] [C-CONV](https://rust-lang.github.io/api-guidelines/naming.html#ad-hoc-conversions-follow-as_-to_-into_-conventions-c-conv) - 临时转换
  遵循 `as_`、`to_`、`into_` 约定
- [ ] [C-GETTER](https://rust-lang.github.io/api-guidelines/naming.html#getter-names-follow-rust-convention-c-getter) - Getter 名称遵循 Rust 约定
- [ ] [C-COMMON-TRAITS](https://rust-lang.github.io/api-guidelines/interoperability.html#c-common-traits) - 类型积极实现常用 trait
  - `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Default`, `Debug`
  - 类型需要被展示时实现 `Display`
- [ ] [C-CTOR](https://rust-lang.github.io/api-guidelines/predictability.html?highlight=new#constructors-are-static-inherent-methods-c-ctor) -
  构造器是静态固有方法
  - 尤其是即使已有 `Foo::default()`，也应提供 `Foo::new()`
- [ ] [C-FEATURE](https://rust-lang.github.io/api-guidelines/naming.html#feature-names-are-free-of-placeholder-words-c-feature) - Feature 名称
  不含占位词

## 使用静态检查 (M-STATIC-VERIFICATION) {#M-STATIC-VERIFICATION}

*本条守护：一致性，并远离常见问题。*

项目应当使用下列静态检查工具来维持代码质量。这些工具可以
配置为在开发者本机日常工作中运行，也应当作为提交门禁的一部分。

* [compiler lints](https://doc.rust-lang.org/rustc/lints/index.html) 提供大量 lint，用于避免缺陷并提升代码质量。
* [clippy lints](https://doc.rust-lang.org/clippy/) 包含数百条 lint，用于避免缺陷并提升代码质量。
* [rustfmt](https://github.com/rust-lang/rustfmt) 保证源码格式一致。
* [cargo-audit](https://crates.io/crates/cargo-audit) 检查 crate 依赖中的安全漏洞。
* [cargo-hack](https://crates.io/crates/cargo-hack) 验证 crate feature 的所有组合都能正常工作。
* [cargo-udeps](https://crates.io/crates/cargo-udeps) 检测 Cargo.toml 中未使用的依赖。
* [miri](https://github.com/rust-lang/miri) 验证 unsafe 代码的正确性。

### 编译器 Lint

Rust 编译器的诊断通常非常出色。除默认诊断外，项目
应当显式启用下列编译器 lint：

```toml
[lints.rust]
ambiguous_negative_literals = "warn"
missing_debug_implementations = "warn"
redundant_imports = "warn"
redundant_lifetimes = "warn"
trivial_numeric_casts = "warn"
unsafe_op_in_unsafe_fn = "warn"
unused_lifetimes = "warn"
```

### Clippy Lint

对于 clippy，项目应当启用所有主要 lint 分类，并额外启用 `restriction` lint 组中的若干条目。
不需要的 lint（例如数值转换）可以按需逐条关闭：

```toml
[lints.clippy]
cargo = { level = "warn", priority = -1 }
complexity = { level = "warn", priority = -1 }
correctness = { level = "warn", priority = -1 }
pedantic = { level = "warn", priority = -1 }
perf = { level = "warn", priority = -1 }
style = { level = "warn", priority = -1 }
suspicious = { level = "warn", priority = -1 }
# nursery = { level = "warn", priority = -1 }  # 可选，可能带来更多误报

# 下列额外 lint 来自 `restriction` 与 `nursery` 组，用于禁止源码中的特定
# 写法，以提高一致性、质量和简洁度
allow_attributes_without_reason = "warn"
as_pointer_underscore = "warn"
assertions_on_result_states = "warn"
clone_on_ref_ptr = "warn"
deref_by_slicing = "warn"
disallowed_script_idents = "warn"
empty_drop = "warn"
empty_enum_variants_with_brackets = "warn"
empty_structs_with_brackets = "warn"
fn_to_numeric_cast_any = "warn"
if_then_some_else_none = "warn"
map_err_ignore = "warn"
redundant_type_annotations = "warn"
renamed_function_params = "warn"
semicolon_outside_block = "warn"
undocumented_unsafe_blocks = "warn"
unnecessary_safety_comment = "warn"
unnecessary_safety_doc = "warn"
unneeded_field_pattern = "warn"
unused_result_ok = "warn"
too_long_first_doc_paragraph = "warn"

# 否则可能干扰结构化日志。
literal_string_with_formatting_args = "allow"

# 在此定义自定义退出项
# ...
```

## Lint 覆盖应使用 `#[expect]` (M-LINT-OVERRIDE-EXPECT) {#M-LINT-OVERRIDE-EXPECT}

*本条守护：一份不过时、整洁的 lint 集合。*

在子模块或具体项上覆盖项目全局 lint 时，应当使用 `#[expect]`，而非 `#[allow]`。

若所标记的警告实际并未出现，预期 lint 会发出警告，从而防止陈旧 lint 堆积。
不过，`#[allow]` 在生成代码中仍然有用，也可以出现在宏里。

覆盖应当附带 `reason`：

```rust
#[expect(clippy::unused_async, reason = "API fixed, will use I/O later")]
pub async fn ping_server() {
  // 目前只是占位
}
```

## 公开类型实现 Debug (M-PUBLIC-DEBUG) {#M-PUBLIC-DEBUG}

*本条守护：便于调试，且不泄露敏感数据。*

crate 暴露的所有公开类型都应当实现 `Debug`。多数类型可通过 `#[derive(Debug)]` 完成：

```rust
#[derive(Debug)]
struct Endpoint(String);
```

设计用于保存敏感数据的类型也应当实现 `Debug`，但要通过自定义实现。
该实现必须配有单元测试，确保敏感数据当前不会泄露，将来也不会。

```rust
use std::fmt::{Debug, Formatter};

struct UserSecret(String);

impl Debug for UserSecret {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        write!(f, "UserSecret(...)")
    }
}

#[test]
fn test() {
    let key = "552d3454-d0d5-445d-ab9f-ef2ae3a8896a";
    let secret = UserSecret(key.to_string());
    let rendered = format!("{:?}", secret);

    assert!(rendered.contains("UserSecret"));
    assert!(!rendered.contains(key));
}
```

## 意在被阅读的公开类型实现 Display (M-PUBLIC-DISPLAY) {#M-PUBLIC-DISPLAY}

*本条守护：可用性。*

若上游消费者（无论是开发者还是最终用户）预期会阅读你的类型，该类型应当实现 `Display`。这尤其包括：

- 错误类型，`std::error::Error` 要求它们实现 `Display`
- 字符串类数据的包装器

`Display` 的实现应当遵循 Rust 惯例；这包括换行与转义序列的呈现方式。
[M-PUBLIC-DEBUG] 中关于敏感数据的处理同样适用。

[M-PUBLIC-DEBUG]: ./#M-PUBLIC-DEBUG

## 有疑问时拆分 crate (M-SMALLER-CRATES) {#M-SMALLER-CRATES}

*本条守护：更快的编译时间与良好的模块化。*

你应当宁可 crate 偏多，也不要偏少：这会显著改善编译时间——尤其是
在开发这些 crate 期间——并防止组件循环依赖。

本质上，如果一个子模块可以独立使用，其内容就应当迁到单独的 crate。

拆分 crate 可能导致你无法再访问某些 `pub(crate)` 字段或方法。在许多情况下，这是可取的
副作用，应当促使你设计更灵活的抽象，让用户也能获得类似的使用便利。

有时则应当把各个 crate 重新并入单一的 _umbrella crate_，例如处理 proc macro 或运行时。
因技术原因拆出的功能（例如 `foo_proc` proc macro crate）应当始终再导出。除此之外，再导出应当慎用。

> ### 💡  Feature 与 Crate
>
> 经验法则是：可以合理独立使用的项适合做成 crate。Feature 应当解锁无法
> 独立存在的额外功能。对于伞形 crate（见下），feature 也可用于启用组成部件（但那时功能
> 已经抽到 crate 里了）。
>
> 例如，若你定义了一个包含下列模块的 `web` crate，只需要客户端调用的用户也得为服务端代码的编译买单：
>
> ```text
> web::server
> web::client
> web::protocols
> ```
>
> 相反，你应当引入独立 crate，让用户可以按需挑选：
>
> ```text
> web_server
> web_client
> web_protocols
> ```

## 名称不含含糊词 (M-WEASEL-WORDS) {#M-WEASEL-WORDS}

*本条守护：可读性。*

符号名称，尤其是类型和 trait 名称，应当不含那些并不能真正
增加信息的含糊词。常见问题包括 `Service`、`Manager` 和 `Factory`。

你的库完全可能包含或与预订服务通信&mdash;甚至持有一个名为 `booking_service` 的 `HttpClient`
实例&mdash;但代码中很少应当出现 `BookingService` _类型_。

处理大量预订的项直接叫 `Bookings` 即可。若职责更具体，就应把那一特质
追加到名称上。它把这些项提交到别处？叫 `BookingDispatcher` 会更有帮助。

`Manager` 同样如此。所有代码都在管理 _某样东西_，因此这个头衔很少有用。除极少数
例外，生命周期问题也不应交给某个 manager。项按需要的方式创建，其销毁由 `Drop` 管辖，且只由 `Drop` 管辖。

至于工厂，至少应当避开这个术语。虽然 `FooFactory` 这一概念有其用处，其规范的
Rust 名称是 `Builder`（参见 [M-INIT-BUILDER](../libraries/02-ux/#M-INIT-BUILDER)）。能反复产出项的构建器仍然是构建器。

此外，把工厂（构建器）作为参数接受，是把面向对象概念生搬进 Rust 的非惯用法。若
需要可重复实例化，函数应当要求 `impl Fn() -> Foo`，而不是 `FooBuilder` 或
类似类型。相反，独立的构建器有其用处，但主要用于降低围绕可选值的参数组合
复杂度（同样见 [M-INIT-BUILDER](../libraries/02-ux/#M-INIT-BUILDER)）。

## 项的名称要短 (M-SHORT-NAMES) {#M-SHORT-NAMES}

*本条守护：惯用代码。*

应当遵循 Rust 关于项标识符宜短的约定：

- 标识符不应由超过 2 个短词复合而成（用 `AppConfig` 而非 `GlobalApplicationConfig`），
- 模块或 crate 信息不应写进前缀（用 `foo::Id` 而非 `foo::FooId`），尤其当直接的上级项已经足够描述时——此时用户应在需要时用限定名在本地消歧（`fn convert(foo::Id) -> bar::Id`）。
- 优先使用缩写（用 `CallbackFn` 而非 `CallbackFunction`），

任何规则都可以在局部合理时打破，但在单个 crate 范围内，这些例外应当是 _例外_，并且动机充分。

## 优先普通函数而非关联函数 (M-REGULAR-FN) {#M-REGULAR-FN}

*本条守护：可读性。*

关联函数应当主要用于实例创建，而非通用计算。

与某些面向对象语言不同，普通函数在 Rust 中是一等公民，不需要模块或 _类_ 来托管。因此，并不明显属于某个接收者的功能，
不应放在类型的 `impl` 块中：

```rust
struct Database {}

impl Database {
    // 可以，关联函数用于创建实例
    fn new() -> Self {}

    // 可以，以 `&self` 为接收者的普通方法
    fn query(&self) {}

    // 不可以，此函数与 `Database` 没有直接关系，
    // 因此不应作为关联函数放在 `Database` 下。
    fn check_parameters(p: &str) {}
}

// 作为普通函数则没问题
fn check_parameters(p: &str) {}
```

普通函数更符合惯例，并减少调用方不必要的噪音。不过，trait 的关联函数完全符合惯例：

```rust
pub trait Default {
    fn default() -> Self;
}

struct Foo;

impl Default for Foo {
    fn default() -> Self { Self }
}
```

## 魔法值必须有文档 (M-DOCUMENTED-MAGIC) {#M-DOCUMENTED-MAGIC}

*本条守护：可维护性与安全的重构。*

生产代码中的硬编码 _魔法_ 值必须附带注释。注释应当说明：

- 为何选择该值，
- 更改该值时不明显的副作用，
- 与该常量交互的外部系统。

应当优先使用具名常量，而非内联值。

```rust
// 不好：相对明显这是等待一天，但看不出为什么
wait_timeout(60 * 60 * 24).await // 最多等待一天

// 较好
wait_timeout(60 * 60 * 24).await // 足够大，确保服务器
                                 // 能完成处理。设得太低可能
                                 // 导致我们中止合法请求。基于
                                 // `api.foo.com` 的超时策略。

// 最好

/// 我们等待服务器的时长。
///
/// 足够大，确保服务器
/// 能完成处理。设得太低可能
/// 导致我们中止合法请求。基于
/// `api.foo.com` 的超时策略。
const UPSTREAM_SERVER_TIMEOUT: Duration = Duration::from_secs(60 * 60 * 24);
```

## 使用带消息模板的结构化日志 (M-LOG-STRUCTURED) {#M-LOG-STRUCTURED}

*本条守护：低成本日志与强过滤。*

日志应当使用带具名属性的结构化事件，以及遵循
[message templates](https://messagetemplates.org/) 规范的消息模板。

> **注意：** 示例使用 [`tracing`](https://docs.rs/tracing/) crate 的 `event!` 宏，
但这些原则适用于任何支持结构化日志的日志 API（例如 `log`、
`slog`、自定义遥测系统）。

### 避免字符串格式化

字符串格式化会在运行时分配内存。消息模板把格式化推迟到查看时。
我们建议消息模板包含所有具名属性，以便在查看时更易检查。

```rust
// 不好：字符串格式化会导致分配
tracing::info!("file opened: {}", path);
tracing::info!(format!("file opened: {}", path));

// 好：带具名属性的消息模板
event!(
    name: "file.open.success",
    Level::INFO,
    file.path = path.display(),
    "file opened: {{file.path}}",
);
```

> **注意**：在消息模板中使用 `{{property}}` 语法，这样既保留字面文本，
> 又转义了 Rust 的格式化语法。字符串格式化推迟到查看日志时进行。

### 为事件命名

使用分层的点分记法：`<component>.<operation>.<state>`

```rust
// 不好：未命名事件
event!(
    Level::INFO,
    file.path = file_path,
    "file {{file.path}} processed succesfully",
);

// 好：已命名事件
event!(
    name: "file.processing.success", // 事件标识符
    Level::INFO,
    file.path = file_path,
    "file {{file.path}} processed succesfully",
);
```

已命名事件可以跨日志条目进行分组和过滤。

### 遵循 OpenTelemetry 语义约定

如有需要，对常见属性使用 [OTel semantic conventions](https://opentelemetry.io/docs/specs/semconv/)。
这有助于标准化与互操作。

```rust
event!(
    name: "file.write.success",
    Level::INFO,
    file.path = path.display(),         // 标准 OTel 名称
    file.size = bytes_written,          // 标准 OTel 名称
    file.directory = dir_path,          // 标准 OTel 名称
    file.extension = extension,         // 标准 OTel 名称
    file.operation = "write",           // 自定义名称
    "{{file.operation}} {{file.size}} bytes to {{file.path}} in {{file.directory}} extension={{file.extension}}",
);
```

常见约定：

- HTTP: `http.request.method`, `http.response.status_code`, `url.scheme`, `url.path`, `server.address`
- 文件: `file.path`, `file.directory`, `file.name`, `file.extension`, `file.size`
- 数据库: `db.system.name`, `db.namespace`, `db.operation.name`, `db.query.text`
- 错误: `error.type`, `error.message`, `exception.type`, `exception.stacktrace`

### 脱敏敏感数据

不要记录明文敏感数据，否则可能导致隐私与安全事故。

```rust
// 不好：可能记录敏感数据
event!(
    name: "file.operation.started",
    Level::INFO,
    user.email = user.email,  // 敏感数据
    file.name = "license.txt",
    "reading file {{file.name}} for user {{user.email}}",
);

// 好：脱敏敏感部分
event!(
    name: "file.operation.started",
    Level::INFO,
    user.email.redacted = redact_email(user.email),
    file.name = "license.txt",
    "reading file {{file.name}} for user {{user.email.redacted}}",
);
```

敏感数据包括电子邮件地址、会暴露用户身份的文件路径、包含密钥或令牌的文件名、
含有 PII 的文件内容、带会话 ID 的临时文件路径等等。可考虑使用 [`data_privacy`](https://crates.io/crates/data_privacy) crate 以保持脱敏方式一致。

### 延伸阅读

- [Message Templates Specification](https://messagetemplates.org/)
- [OpenTelemetry Semantic Conventions](https://opentelemetry.io/docs/specs/semconv/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
