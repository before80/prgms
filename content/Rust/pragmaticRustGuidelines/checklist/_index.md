+++
title = "检查清单"
date = 2026-08-18T18:10:00+08:00
weight = 20
type = "docs"
description = "检查清单 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/guidelines/checklist/index.html](https://microsoft.github.io/rust-guidelines/guidelines/checklist/index.html)

# 检查清单

- **通用**
  - [ ] 遵循上游指南 ([M-UPSTREAM-GUIDELINES])
  - [ ] 使用静态检查 ([M-STATIC-VERIFICATION])
  - [ ] Lint 覆盖应使用 `#[expect]` ([M-LINT-OVERRIDE-EXPECT])
  - [ ] 公开类型实现 Debug ([M-PUBLIC-DEBUG])
  - [ ] 意在被阅读的公开类型实现 Display ([M-PUBLIC-DISPLAY])
  - [ ] 有疑问时拆分 crate ([M-SMALLER-CRATES])
  - [ ] 名称不含含糊词 ([M-WEASEL-WORDS])
  - [ ] 项的名称要短 ([M-SHORT-NAMES])
  - [ ] 优先普通函数而非关联函数 ([M-REGULAR-FN])
  - [ ] 魔法值必须有文档 ([M-DOCUMENTED-MAGIC])
  - [ ] 使用带消息模板的结构化日志 ([M-LOG-STRUCTURED])
- **库 / 互操作性**
  - [ ] 类型是 Send ([M-TYPES-SEND])
  - [ ] 提供原生逃生舱 ([M-ESCAPE-HATCHES])
  - [ ] 不要泄漏外部类型 ([M-DONT-LEAK-TYPES])
  - [ ] 项来自其原始 crate ([M-FOREIGN-REEXPORTS])
  - [ ] 可行时接受 `impl AsRef<>` ([M-IMPL-ASREF])
  - [ ] 可行时接受 `impl RangeBounds<>` ([M-IMPL-RANGEBOUNDS])
  - [ ] 可行时接受 `impl 'IO'`（sans IO） ([M-IMPL-IO])
- **库 / 用户体验**
  - [ ] 抽象不要明显嵌套 ([M-SIMPLE-ABSTRACTIONS])
  - [ ] API 中避免智能指针和包装器 ([M-AVOID-WRAPPERS])
  - [ ] 优先具体类型，其次泛型，再次 dyn trait ([M-DI-HIERARCHY])
  - [ ] 错误是规范结构体 ([M-ERRORS-CANONICAL-STRUCTS])
  - [ ] 规范错误转换使用 `From` 而非 `map_err` ([M-FROM-ERROR])
  - [ ] 复杂类型构造使用 builder ([M-INIT-BUILDER])
  - [ ] 复杂类型初始化层次级联 ([M-INIT-CASCADED])
  - [ ] 服务类型实现 Clone ([M-SERVICES-CLONE])
  - [ ] 核心功能应是固有方法 ([M-ESSENTIAL-FN-INHERENT])
  - [ ] 模块在大小与职责上保持均衡 ([M-BALANCED-MODULES])
  - [ ] 不要定义 prelude ([M-NO-PRELUDE])
  - [ ] 参数顺序保持一致 ([M-PARAMETER-CONSISTENCY])
  - [ ] 集合实现相应的 iter trait ([M-COLLECTION-TRAITS])
  - [ ] 函数使用 `async` 而非返回 Future ([M-ASYNC-FN])
- **库 / 韧性**
  - [ ] I/O 与系统调用可被 mock ([M-MOCKABLE-SYSCALLS])
  - [ ] 测试工具用 feature 门控 ([M-TEST-UTIL])
  - [ ] 集成测试放在 `tests/` 下 ([M-INTEGRATION-TESTS])
  - [ ] 使用合适的类型族 ([M-STRONG-TYPES])
  - [ ] Newtype 守护不变量 ([M-STRONG-TYPES-GUARD])
  - [ ] Builder 在最终 `.build()` 中校验 ([M-BUILD-RESULT])
  - [ ] 不要 glob 再导出项 ([M-NO-GLOB-REEXPORTS])
  - [ ] 避免静态量 ([M-AVOID-STATICS])
  - [ ] 生产代码使用遥测而非 println ([M-LOG-NOT-PRINT])
- **库 / 构建**
  - [ ] 库开箱即用 ([M-OOBE])
  - [ ] 原生 `-sys` crate 无需额外依赖即可编译 ([M-SYS-CRATES])
  - [ ] Feature 是可叠加的 ([M-FEATURES-ADDITIVE])
- **宏**
  - [ ] 宏是最后手段 ([M-MACRO-LAST-RESORT])
  - [ ] 优先示例宏而非过程宏 ([M-EXAMPLE-OVER-PROC])
  - [ ] 宏不谎报签名 ([M-MACROS-DONT-LIE])
  - [ ] 宏假定位于主 crate ([M-MACRO-MAIN-CRATE])
  - [ ] 第三方项来自隐藏的 `_private` 模块 ([M-MACRO-HELPERS])
  - [ ] 过程宏应有独立的 impl crate（含测试） ([M-PROC-IMPL])
  - [ ] 过程宏不产生隐含或隐藏项 ([M-PROC-IMPLIED-ITEMS])
- **应用**
  - [ ] 应用使用 mimalloc ([M-MIMALLOC-APPS])
  - [ ] 应用可以使用 Anyhow 或其衍生库 ([M-APP-ERROR])
  - [ ] 应用面向可行的最高 target-cpu ([M-TARGET-CPU])
- **FFI**
  - [ ] 在 FFI 库之间隔离 DLL 状态 ([M-ISOLATE-DLL-STATE])
  - [ ] 业务逻辑属于核心 crate，FFI 只做转译 ([M-FFI-TRANSLATES])
  - [ ] FFI crate 遵循既有命名约定 ([M-FFI-NAMING])
- **正确性**
  - [ ] Unsafe 需要理由，应当避免 ([M-UNSAFE])
  - [ ] Unsafe 意味着未定义行为 ([M-UNSAFE-IMPLIES-UB])
  - [ ] 所有代码必须是健全的 ([M-UNSOUND])
  - [ ] Panic 表示「停止程序」 ([M-PANIC-IS-STOP])
  - [ ] 检测到的编程错误是 panic 而非 error ([M-PANIC-ON-BUG])
  - [ ] 从 panic 继续执行是最后手段 ([M-PANIC-CONTINUATION])
  - [ ] 自定义 panic 要有有用的消息 ([M-PANIC-MESSAGE])
- **性能**
  - [ ] 优化吞吐量，避免空转 ([M-THROUGHPUT])
  - [ ] 尽早识别、剖析并优化热路径 ([M-HOTPATH])
  - [ ] 长时间任务应有让出点 ([M-YIELD-POINTS])
  - [ ] 尽可能复用分配 ([M-MEM-REUSE])
  - [ ] 库的遥测不得拖垮性能 ([M-LOG-OVERHEAD])
  - [ ] 嵌套类型层次应避免不必要的间接 ([M-AVOID-INDIRECTION])
  - [ ] 不可变自有序列使用 boxed slice 与 string ([M-BOX-DST])
  - [ ] 构建完成后收缩集合以贴合容量 ([M-SHRINK-TO-FIT])
  - [ ] 尽可能使用快速 hasher ([M-FAST-HASHER])
  - [ ] 创建集合时给予足够初始容量 ([M-INITIAL-CAPACITY])
  - [ ] 热路径 `async` 函数减小栈尺寸 ([M-ASYNC-STACK-SIZE])
- **项目**
  - [ ] 公共设置来自 workspace 的 Cargo.toml ([M-CARGO-WORKSPACE])
  - [ ] workspace 列出并为所有 crate 指定版本 ([M-CRATES-IN-WORKSPACE])
  - [ ] 所有 crate 作为兄弟目录放在同一文件夹 ([M-CRATES-FLAT-FOLDER])
  - [ ] 新 crate 面向最新 edition ([M-LATEST-EDITION])
  - [ ] 保守地更新 MSRV ([M-MSRV])
- **文档**
  - [ ] 首句一行，约 15 个英文词 ([M-FIRST-DOC-SENTENCE])
  - [ ] 具备完备的模块文档 ([M-MODULE-DOCS])
  - [ ] 文档包含规范章节 ([M-CANONICAL-DOCS])
  - [ ] 为 `pub use` 项标记 `#[doc(inline)]` ([M-DOC-INLINE])
- **AI**
  - [ ] 面向 AI 使用来设计 ([M-DESIGN-FOR-AI])
  - [ ] 项只通过一条路径可见 ([M-SINGLE-ITEM-PATH])
  - [ ] 避免元设计文档 ([M-NO-META-DESIGN-DOCUMENTATION])
  - [ ] 测试不断言常识性事实 ([M-TAUTOLOGICAL-TESTS])
  - [ ] Rust 代码解决 Rust 问题 ([M-RUST-SHAPED])

[M-UPSTREAM-GUIDELINES]: ../universal/#M-UPSTREAM-GUIDELINES
[M-STATIC-VERIFICATION]: ../universal/#M-STATIC-VERIFICATION
[M-LINT-OVERRIDE-EXPECT]: ../universal/#M-LINT-OVERRIDE-EXPECT
[M-PUBLIC-DEBUG]: ../universal/#M-PUBLIC-DEBUG
[M-PUBLIC-DISPLAY]: ../universal/#M-PUBLIC-DISPLAY
[M-SMALLER-CRATES]: ../universal/#M-SMALLER-CRATES
[M-WEASEL-WORDS]: ../universal/#M-WEASEL-WORDS
[M-SHORT-NAMES]: ../universal/#M-SHORT-NAMES
[M-REGULAR-FN]: ../universal/#M-REGULAR-FN
[M-DOCUMENTED-MAGIC]: ../universal/#M-DOCUMENTED-MAGIC
[M-LOG-STRUCTURED]: ../universal/#M-LOG-STRUCTURED
[M-LOG-NOT-PRINT]: ../libraries/03-resilience/#M-LOG-NOT-PRINT
[M-TYPES-SEND]: ../libraries/01-interoperability/#M-TYPES-SEND
[M-DONT-LEAK-TYPES]: ../libraries/01-interoperability/#M-DONT-LEAK-TYPES
[M-FOREIGN-REEXPORTS]: ../libraries/01-interoperability/#M-FOREIGN-REEXPORTS
[M-ESCAPE-HATCHES]: ../libraries/01-interoperability/#M-ESCAPE-HATCHES
[M-STRONG-TYPES]: ../libraries/03-resilience/#M-STRONG-TYPES
[M-STRONG-TYPES-GUARD]: ../libraries/03-resilience/#M-STRONG-TYPES-GUARD
[M-NO-GLOB-REEXPORTS]: ../libraries/03-resilience/#M-NO-GLOB-REEXPORTS
[M-ESSENTIAL-FN-INHERENT]: ../libraries/02-ux/#M-ESSENTIAL-FN-INHERENT
[M-MOCKABLE-SYSCALLS]: ../libraries/03-resilience/#M-MOCKABLE-SYSCALLS
[M-SIMPLE-ABSTRACTIONS]: ../libraries/02-ux/#M-SIMPLE-ABSTRACTIONS
[M-AVOID-WRAPPERS]: ../libraries/02-ux/#M-AVOID-WRAPPERS
[M-DI-HIERARCHY]: ../libraries/02-ux/#M-DI-HIERARCHY
[M-ERRORS-CANONICAL-STRUCTS]: ../libraries/02-ux/#M-ERRORS-CANONICAL-STRUCTS
[M-FROM-ERROR]: ../libraries/02-ux/#M-FROM-ERROR
[M-INIT-BUILDER]: ../libraries/02-ux/#M-INIT-BUILDER
[M-BUILD-RESULT]: ../libraries/03-resilience/#M-BUILD-RESULT
[M-INIT-CASCADED]: ../libraries/02-ux/#M-INIT-CASCADED
[M-SERVICES-CLONE]: ../libraries/02-ux/#M-SERVICES-CLONE
[M-IMPL-ASREF]: ../libraries/01-interoperability/#M-IMPL-ASREF
[M-IMPL-RANGEBOUNDS]: ../libraries/01-interoperability/#M-IMPL-RANGEBOUNDS
[M-IMPL-IO]: ../libraries/01-interoperability/#M-IMPL-IO
[M-BALANCED-MODULES]: ../libraries/02-ux/#M-BALANCED-MODULES
[M-NO-PRELUDE]: ../libraries/02-ux/#M-NO-PRELUDE
[M-PARAMETER-CONSISTENCY]: ../libraries/02-ux/#M-PARAMETER-CONSISTENCY
[M-COLLECTION-TRAITS]: ../libraries/02-ux/#M-COLLECTION-TRAITS
[M-ASYNC-FN]: ../libraries/02-ux/#M-ASYNC-FN
[M-TEST-UTIL]: ../libraries/03-resilience/#M-TEST-UTIL
[M-INTEGRATION-TESTS]: ../libraries/03-resilience/#M-INTEGRATION-TESTS
[M-AVOID-STATICS]: ../libraries/03-resilience/#M-AVOID-STATICS
[M-OOBE]: ../libraries/04-building/#M-OOBE
[M-SYS-CRATES]: ../libraries/04-building/#M-SYS-CRATES
[M-FEATURES-ADDITIVE]: ../libraries/04-building/#M-FEATURES-ADDITIVE
[M-APP-ERROR]: ../applications/#M-APP-ERROR
[M-MIMALLOC-APPS]: ../applications/#M-MIMALLOC-APPS
[M-TARGET-CPU]: ../applications/#M-TARGET-CPU
[M-ISOLATE-DLL-STATE]: ../ffi/#M-ISOLATE-DLL-STATE
[M-FFI-TRANSLATES]: ../ffi/#M-FFI-TRANSLATES
[M-FFI-NAMING]: ../ffi/#M-FFI-NAMING
[M-UNSAFE]: ../correctness/#M-UNSAFE
[M-UNSAFE-IMPLIES-UB]: ../correctness/#M-UNSAFE-IMPLIES-UB
[M-UNSOUND]: ../correctness/#M-UNSOUND
[M-PANIC-IS-STOP]: ../correctness/#M-PANIC-IS-STOP
[M-PANIC-ON-BUG]: ../correctness/#M-PANIC-ON-BUG
[M-PANIC-CONTINUATION]: ../correctness/#M-PANIC-CONTINUATION
[M-PANIC-MESSAGE]: ../correctness/#M-PANIC-MESSAGE
[M-HOTPATH]: ../performance/#M-HOTPATH
[M-THROUGHPUT]: ../performance/#M-THROUGHPUT
[M-YIELD-POINTS]: ../performance/#M-YIELD-POINTS
[M-MEM-REUSE]: ../performance/#M-MEM-REUSE
[M-LOG-OVERHEAD]: ../performance/#M-LOG-OVERHEAD
[M-AVOID-INDIRECTION]: ../performance/#M-AVOID-INDIRECTION
[M-BOX-DST]: ../performance/#M-BOX-DST
[M-SHRINK-TO-FIT]: ../performance/#M-SHRINK-TO-FIT
[M-FAST-HASHER]: ../performance/#M-FAST-HASHER
[M-INITIAL-CAPACITY]: ../performance/#M-INITIAL-CAPACITY
[M-ASYNC-STACK-SIZE]: ../performance/#M-ASYNC-STACK-SIZE
[M-CARGO-WORKSPACE]: ../project/#M-CARGO-WORKSPACE
[M-CRATES-IN-WORKSPACE]: ../project/#M-CRATES-IN-WORKSPACE
[M-CRATES-FLAT-FOLDER]: ../project/#M-CRATES-FLAT-FOLDER
[M-LATEST-EDITION]: ../project/#M-LATEST-EDITION
[M-MSRV]: ../project/#M-MSRV
[M-FIRST-DOC-SENTENCE]: ../documentation/#M-FIRST-DOC-SENTENCE
[M-MODULE-DOCS]: ../documentation/#M-MODULE-DOCS
[M-CANONICAL-DOCS]: ../documentation/#M-CANONICAL-DOCS
[M-DOC-INLINE]: ../documentation/#M-DOC-INLINE
[M-MACRO-LAST-RESORT]: ../macros/#M-MACRO-LAST-RESORT
[M-EXAMPLE-OVER-PROC]: ../macros/#M-EXAMPLE-OVER-PROC
[M-MACROS-DONT-LIE]: ../macros/#M-MACROS-DONT-LIE
[M-MACRO-MAIN-CRATE]: ../macros/#M-MACRO-MAIN-CRATE
[M-MACRO-HELPERS]: ../macros/#M-MACRO-HELPERS
[M-PROC-IMPL]: ../macros/#M-PROC-IMPL
[M-PROC-IMPLIED-ITEMS]: ../macros/#M-PROC-IMPLIED-ITEMS
[M-DESIGN-FOR-AI]: ../ai/#M-DESIGN-FOR-AI
[M-SINGLE-ITEM-PATH]: ../ai/#M-SINGLE-ITEM-PATH
[M-NO-META-DESIGN-DOCUMENTATION]: ../ai/#M-NO-META-DESIGN-DOCUMENTATION
[M-TAUTOLOGICAL-TESTS]: ../ai/#M-TAUTOLOGICAL-TESTS
[M-RUST-SHAPED]: ../ai/#M-RUST-SHAPED
