+++
title = "更新日志"
date = 2026-08-18T18:10:00+08:00
weight = 140
type = "docs"
description = "更新日志 — Pragmatic Rust Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/)

> 原文链接: [https://microsoft.github.io/rust-guidelines/changelog/index.html](https://microsoft.github.io/rust-guidelines/changelog/index.html)

# 更新日志

本页记录《务实的 Rust 指南》的重要变更。

## 2026.6

本次更新大幅扩展了指南，新增 41 条准则，涵盖宏、性能、项目布局、FFI、AI 辅助开发等方面：

| 准则 | 标题 |
|---|---|
| [M-ASYNC-FN](../libraries/02-ux/#M-ASYNC-FN) | 函数使用 `async` 而非返回 Future |
| [M-ASYNC-STACK-SIZE](../performance/#M-ASYNC-STACK-SIZE) | 热路径 `async` 函数减小栈尺寸 |
| [M-AVOID-INDIRECTION](../performance/#M-AVOID-INDIRECTION) | 嵌套类型层次应避免不必要的间接 |
| [M-BALANCED-MODULES](../libraries/02-ux/#M-BALANCED-MODULES) | 模块在大小与职责上保持均衡 |
| [M-BOX-DST](../performance/#M-BOX-DST) | 不可变自有序列使用 boxed slice 与 string |
| [M-BUILD-RESULT](../libraries/03-resilience/#M-BUILD-RESULT) | Builder 在最终 `.build()` 中校验 |
| [M-CARGO-WORKSPACE](../project/#M-CARGO-WORKSPACE) | 公共设置来自 workspace 的 Cargo.toml |
| [M-COLLECTION-TRAITS](../libraries/02-ux/#M-COLLECTION-TRAITS) | 集合实现相应的 iter trait |
| [M-CRATES-FLAT-FOLDER](../project/#M-CRATES-FLAT-FOLDER) | 所有 crate 作为兄弟目录放在同一文件夹 |
| [M-CRATES-IN-WORKSPACE](../project/#M-CRATES-IN-WORKSPACE) | workspace 列出并为所有 crate 指定版本 |
| [M-EXAMPLE-OVER-PROC](../macros/#M-EXAMPLE-OVER-PROC) | 优先示例宏而非过程宏 |
| [M-FAST-HASHER](../performance/#M-FAST-HASHER) | 尽可能使用快速 hasher |
| [M-FFI-NAMING](../ffi/#M-FFI-NAMING) | FFI crate 遵循既有命名约定 |
| [M-FFI-TRANSLATES](../ffi/#M-FFI-TRANSLATES) | 业务逻辑属于核心 crate，FFI 只做转译 |
| [M-FOREIGN-REEXPORTS](../libraries/01-interoperability/#M-FOREIGN-REEXPORTS) | 项来自其原始 crate |
| [M-FROM-ERROR](../libraries/02-ux/#M-FROM-ERROR) | 规范错误转换使用 `From` 而非 `map_err` |
| [M-INITIAL-CAPACITY](../performance/#M-INITIAL-CAPACITY) | 创建集合时给予足够初始容量 |
| [M-INTEGRATION-TESTS](../libraries/03-resilience/#M-INTEGRATION-TESTS) | 集成测试放在 `tests/` 下 |
| [M-LATEST-EDITION](../project/#M-LATEST-EDITION) | 新 crate 面向最新 edition |
| [M-LOG-NOT-PRINT](../libraries/03-resilience/#M-LOG-NOT-PRINT) | 生产代码使用遥测而非 println |
| [M-LOG-OVERHEAD](../performance/#M-LOG-OVERHEAD) | 库的遥测不得拖垮性能 |
| [M-MACRO-HELPERS](../macros/#M-MACRO-HELPERS) | 第三方项来自隐藏的 `_private` 模块 |
| [M-MACRO-LAST-RESORT](../macros/#M-MACRO-LAST-RESORT) | 宏是最后手段 |
| [M-MACRO-MAIN-CRATE](../macros/#M-MACRO-MAIN-CRATE) | 宏假定位于主 crate |
| [M-MACROS-DONT-LIE](../macros/#M-MACROS-DONT-LIE) | 宏不谎报签名 |
| [M-MEM-REUSE](../performance/#M-MEM-REUSE) | 尽可能复用分配 |
| [M-MSRV](../project/#M-MSRV) | 保守地更新 MSRV |
| [M-NO-META-DESIGN-DOCUMENTATION](../ai/#M-NO-META-DESIGN-DOCUMENTATION) | 避免元设计文档 |
| [M-NO-PRELUDE](../libraries/02-ux/#M-NO-PRELUDE) | 不要定义 prelude |
| [M-PANIC-CONTINUATION](../correctness/#M-PANIC-CONTINUATION) | 从 panic 继续执行是最后手段 |
| [M-PANIC-MESSAGE](../correctness/#M-PANIC-MESSAGE) | 自定义 panic 要有有用的消息 |
| [M-PARAMETER-CONSISTENCY](../libraries/02-ux/#M-PARAMETER-CONSISTENCY) | 参数顺序保持一致 |
| [M-PROC-IMPL](../macros/#M-PROC-IMPL) | 过程宏应有独立的 impl crate（含测试） |
| [M-PROC-IMPLIED-ITEMS](../macros/#M-PROC-IMPLIED-ITEMS) | 过程宏不产生隐含或隐藏项 |
| [M-RUST-SHAPED](../ai/#M-RUST-SHAPED) | Rust 代码解决 Rust 问题 |
| [M-SHORT-NAMES](../universal/#M-SHORT-NAMES) | 项的名称要短 |
| [M-SHRINK-TO-FIT](../performance/#M-SHRINK-TO-FIT) | 构建完成后收缩集合以贴合容量 |
| [M-SINGLE-ITEM-PATH](../ai/#M-SINGLE-ITEM-PATH) | 项只通过一条路径可见 |
| [M-STRONG-TYPES-GUARD](../libraries/03-resilience/#M-STRONG-TYPES-GUARD) | Newtype 守护不变量 |
| [M-TARGET-CPU](../applications/#M-TARGET-CPU) | 应用面向可行的最高 target-cpu |
| [M-TAUTOLOGICAL-TESTS](../ai/#M-TAUTOLOGICAL-TESTS) | 测试不断言常识性事实 |

我们还移除了按准则单独版本化的做法。

## 2025

《务实的 Rust 指南》首次发布。
