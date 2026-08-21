+++
title = "检查清单"
date = 2026-08-18T21:50:00+08:00
weight = 20
type = "docs"
description = "检查清单 — Rust API Guidelines"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

> 原文链接: [https://rust-lang.github.io/api-guidelines/checklist.html](https://rust-lang.github.io/api-guidelines/checklist.html)

# 检查清单

- **命名** *(crate 与 Rust 命名约定一致)*
  - [ ] 大小写遵循 RFC 430 ([C-CASE])
  - [ ] 临时转换遵循 `as_`、`to_`、`into_` 约定 ([C-CONV])
  - [ ] Getter 名称遵循 Rust 约定 ([C-GETTER])
  - [ ] 集合上产生迭代器的方法遵循 `iter`、`iter_mut`、`into_iter` ([C-ITER])
  - [ ] 迭代器类型名与产生它们的方法匹配 ([C-ITER-TY])
  - [ ] Feature 名称不含占位词 ([C-FEATURE])
  - [ ] 名称使用一致的词序 ([C-WORD-ORDER])
- **互操作性** *(crate 与其他库功能良好交互)*
  - [ ] 类型积极实现常用 trait ([C-COMMON-TRAITS])
    - `Copy`, `Clone`, `Eq`, `PartialEq`, `Ord`, `PartialOrd`, `Hash`, `Debug`,
      `Display`, `Default`
  - [ ] 转换使用标准 trait `From`、`AsRef`、`AsMut` ([C-CONV-TRAITS])
  - [ ] 集合实现 `FromIterator` 与 `Extend` ([C-COLLECT])
  - [ ] 数据结构实现 Serde 的 `Serialize`、`Deserialize` ([C-SERDE])
  - [ ] 类型在可能时是 `Send` 和 `Sync` ([C-SEND-SYNC])
  - [ ] 错误类型有意义且行为良好 ([C-GOOD-ERR])
  - [ ] 二进制数值类型提供 `Hex`、`Octal`、`Binary` 格式化 ([C-NUM-FMT])
  - [ ] 泛型读写函数按值接受 `R: Read` 与 `W: Write` ([C-RW-VALUE])
- **宏** *(crate 提供行为良好的宏)*
  - [ ] 输入语法能让人联想到输出 ([C-EVOCATIVE])
  - [ ] 项宏与属性良好组合 ([C-MACRO-ATTR])
  - [ ] 项宏在任何允许项的地方都能工作 ([C-ANYWHERE])
  - [ ] 项宏支持可见性说明符 ([C-MACRO-VIS])
  - [ ] 类型片段足够灵活 ([C-MACRO-TY])
- **文档** *(crate 文档充分)*
  - [ ] Crate 级文档详尽并含示例 ([C-CRATE-DOC])
  - [ ] 所有项都有 rustdoc 示例 ([C-EXAMPLE])
  - [ ] 示例使用 `?`，不用 `try!`，不用 `unwrap` ([C-QUESTION-MARK])
  - [ ] 函数文档包含错误、panic 与安全性考量 ([C-FAILURE])
  - [ ] 正文包含指向相关内容的超链接 ([C-LINK])
  - [ ] Cargo.toml 包含所有常用元数据 ([C-METADATA])
    - `authors`、`description`、`license`、`homepage`、`documentation`、`repository`、
      `keywords`、`categories`
  - [ ] 发行说明记录所有重要变更 ([C-RELNOTES])
  - [ ] Rustdoc 不展示无帮助的实现细节 ([C-HIDDEN])
- **可预测性** *(crate 使代码易读且行为与外观一致)*
  - [ ] 智能指针不添加固有方法 ([C-SMART-PTR])
  - [ ] 转换位于所涉最具体的类型上 ([C-CONV-SPECIFIC])
  - [ ] 有明确接收者的函数应是方法 ([C-METHOD])
  - [ ] 函数不使用输出参数 ([C-NO-OUT])
  - [ ] 运算符重载不令人意外 ([C-OVERLOAD])
  - [ ] 只有智能指针实现 `Deref` 与 `DerefMut` ([C-DEREF])
  - [ ] 构造器是静态固有方法 ([C-CTOR])
- **灵活性** *(crate 支持多样的现实用例)*
  - [ ] 函数暴露中间结果以避免重复工作 ([C-INTERMEDIATE])
  - [ ] 由调用方决定数据复制与存放位置 ([C-CALLER-CONTROL])
  - [ ] 函数用泛型尽量减少对参数的假设 ([C-GENERIC])
  - [ ] 若可能作为 trait object 有用则保持对象安全 ([C-OBJECT])
- **类型安全** *(crate 有效利用类型系统)*
  - [ ] Newtype 提供静态区分 ([C-NEWTYPE])
  - [ ] 参数通过类型传达含义，而非 `bool` 或 `Option` ([C-CUSTOM-TYPE])
  - [ ] 一组标志使用 `bitflags` 而非枚举 ([C-BITFLAG])
  - [ ] Builder 使复杂值的构造成为可能 ([C-BUILDER])
- **可靠性** *(crate 不太可能做错事)*
  - [ ] 函数校验其参数 ([C-VALIDATE])
  - [ ] 析构器永不失败 ([C-DTOR-FAIL])
  - [ ] 可能阻塞的析构器提供替代方案 ([C-DTOR-BLOCK])
- **可调试性** *(crate 便于调试)*
  - [ ] 所有公开类型实现 `Debug` ([C-DEBUG])
  - [ ] `Debug` 表示永不空 ([C-DEBUG-NONEMPTY])
- **面向未来** *(crate 可改进而不破坏用户代码)*
  - [ ] 密封 trait 防止下游实现 ([C-SEALED])
  - [ ] 结构体字段为私有 ([C-STRUCT-PRIVATE])
  - [ ] Newtype 封装实现细节 ([C-NEWTYPE-HIDE])
  - [ ] 数据结构不重复派生 trait 约束 ([C-STRUCT-BOUNDS])
- **必要事项** *(对在意者而言至关重要)*
  - [ ] 稳定 crate 的公开依赖也是稳定的 ([C-STABLE])
  - [ ] Crate 及其依赖使用宽松许可证 ([C-PERMISSIVE])

[C-CASE]: ../naming/#c-case
[C-CONV]: ../naming/#c-conv
[C-GETTER]: ../naming/#c-getter
[C-ITER]: ../naming/#c-iter
[C-ITER-TY]: ../naming/#c-iter-ty
[C-FEATURE]: ../naming/#c-feature
[C-WORD-ORDER]: ../naming/#c-word-order
[C-COMMON-TRAITS]: ../interoperability/#c-common-traits
[C-CONV-TRAITS]: ../interoperability/#c-conv-traits
[C-COLLECT]: ../interoperability/#c-collect
[C-SERDE]: ../interoperability/#c-serde
[C-SEND-SYNC]: ../interoperability/#c-send-sync
[C-GOOD-ERR]: ../interoperability/#c-good-err
[C-NUM-FMT]: ../interoperability/#c-num-fmt
[C-RW-VALUE]: ../interoperability/#c-rw-value
[C-EVOCATIVE]: ../macros/#c-evocative
[C-MACRO-ATTR]: ../macros/#c-macro-attr
[C-ANYWHERE]: ../macros/#c-anywhere
[C-MACRO-VIS]: ../macros/#c-macro-vis
[C-MACRO-TY]: ../macros/#c-macro-ty
[C-CRATE-DOC]: ../documentation/#c-crate-doc
[C-EXAMPLE]: ../documentation/#c-example
[C-QUESTION-MARK]: ../documentation/#c-question-mark
[C-FAILURE]: ../documentation/#c-failure
[C-LINK]: ../documentation/#c-link
[C-METADATA]: ../documentation/#c-metadata
[C-HTML-ROOT]: ../documentation/#c-html-root
[C-RELNOTES]: ../documentation/#c-relnotes
[C-HIDDEN]: ../documentation/#c-hidden
[C-SMART-PTR]: ../predictability/#c-smart-ptr
[C-CONV-SPECIFIC]: ../predictability/#c-conv-specific
[C-METHOD]: ../predictability/#c-method
[C-NO-OUT]: ../predictability/#c-no-out
[C-OVERLOAD]: ../predictability/#c-overload
[C-DEREF]: ../predictability/#c-deref
[C-CTOR]: ../predictability/#c-ctor
[C-INTERMEDIATE]: ../flexibility/#c-intermediate
[C-CALLER-CONTROL]: ../flexibility/#c-caller-control
[C-GENERIC]: ../flexibility/#c-generic
[C-OBJECT]: ../flexibility/#c-object
[C-NEWTYPE]: ../type-safety/#c-newtype
[C-CUSTOM-TYPE]: ../type-safety/#c-custom-type
[C-BITFLAG]: ../type-safety/#c-bitflag
[C-BUILDER]: ../type-safety/#c-builder
[C-VALIDATE]: ../dependability/#c-validate
[C-DTOR-FAIL]: ../dependability/#c-dtor-fail
[C-DTOR-BLOCK]: ../dependability/#c-dtor-block
[C-DEBUG]: ../debuggability/#c-debug
[C-DEBUG-NONEMPTY]: ../debuggability/#c-debug-nonempty
[C-SEALED]: ../future-proofing/#c-sealed
[C-STRUCT-PRIVATE]: ../future-proofing/#c-struct-private
[C-NEWTYPE-HIDE]: ../future-proofing/#c-newtype-hide
[C-STRUCT-BOUNDS]: ../future-proofing/#c-struct-bounds
[C-STABLE]: ../necessities/#c-stable
[C-PERMISSIVE]: ../necessities/#c-permissive
