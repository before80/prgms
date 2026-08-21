+++
title = "01-模块"
date = 2026-08-18T08:45:00+08:00
weight = 18
type = "docs"
description = "模块 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/modules.html](https://doc.rust-lang.org/reference/items/modules.html)

r[items.mod]
# 模块

r[items.mod.syntax]
```grammar,items
Module ->
      `unsafe`? `mod` IDENTIFIER `;`
    | `unsafe`? `mod` IDENTIFIER `{`
        InnerAttribute*
        Item*
      `}`
```

r[items.mod.intro]
模块是零个或多个[项][items]的容器。

r[items.mod.def]
*模块项*是一个用花括号包围、具名、并以关键字 `mod` 为前缀的模块。模块项会在构成 crate 的模块树中引入一个新的具名模块。

r[items.mod.nesting]
模块可以任意嵌套。

模块的一个例子：

```rust
mod math {
    type Complex = (f64, f64);
    fn sin(f: f64) -> f64 {
        /* ... */
##       unimplemented!();
    }
    fn cos(f: f64) -> f64 {
        /* ... */
##       unimplemented!();
    }
    fn tan(f: f64) -> f64 {
        /* ... */
##       unimplemented!();
    }
}
```

r[items.mod.namespace]
模块定义在其所在模块或块的[类型命名空间][type namespace]中。

r[items.mod.multiple-items]
在同一模块的同一命名空间中定义多个同名项是错误的。关于限制与遮蔽行为的更多细节，参见[作用域一章][scopes chapter]。

r[items.mod.unsafe]
语法上允许 `unsafe` 关键字出现在 `mod` 关键字之前，但会在语义层面被拒绝。这使宏可以消费该语法并利用 `unsafe` 关键字，再将其从 token 流中移除。

r[items.mod.outlined]
## 模块源文件名

r[items.mod.outlined.intro]
没有函数体的模块从外部文件加载。当模块没有 `path` 属性时，文件路径镜像逻辑[模块路径][module path]。

r[items.mod.outlined.search]
祖先模块路径分量对应目录，模块内容位于以模块名加上 `.rs` 扩展名命名的文件中。例如，下列模块结构可以对应这样的文件系统结构：

模块路径                  | 文件系统路径     | 文件内容
------------------------- | ---------------  | -------------
`crate`                   | `lib.rs`         | `mod util;`
`crate::util`             | `util.rs`        | `mod config;`
`crate::util::config`     | `util/config.rs` |

r[items.mod.outlined.search-mod]
模块文件名也可以是以模块名为目录、内容放在该目录下名为 `mod.rs` 的文件。上面的例子也可以把 `crate::util` 的内容放在名为 `util/mod.rs` 的文件中。不允许同时存在 `util.rs` 和 `util/mod.rs`。

> **注意**
> 在 `rustc` 1.30 之前，使用 `mod.rs` 文件是加载带有嵌套子模块的模块的方式。鼓励使用新的命名约定，因为它更一致，并且避免项目中出现许多名为 `mod.rs` 的文件。

r[items.mod.outlined.path]
### `path` 属性

r[items.mod.outlined.path.intro]
用于加载外部文件模块的目录和文件可以通过 `path` 属性加以影响。

r[items.mod.outlined.path.search]
对于不在内联模块块内的模块上的 `path` 属性，文件路径相对于源文件所在目录。例如，下列代码片段会根据其所在位置使用所示路径：

<!-- ignore: requires external files -->
```rust
#[path = "foo.rs"]
mod c;
```

源文件         | `c` 的文件位置     | `c` 的模块路径
-------------- | ------------------- | ----------------------
`src/a/b.rs`   | `src/a/foo.rs`      | `crate::a::b::c`
`src/a/mod.rs` | `src/a/foo.rs`      | `crate::a::c`

r[items.mod.outlined.path.search-nested]
对于内联模块块内的 `path` 属性，文件路径的相对位置取决于该 `path` 属性所在源文件的种类。“mod-rs”源文件是根模块（如 `lib.rs` 或 `main.rs`）以及文件名为 `mod.rs` 的模块。“non-mod-rs”源文件是所有其他模块文件。mod-rs 文件中内联模块块内的 `path` 属性，其路径相对于该 mod-rs 文件所在目录，并把内联模块分量当作目录。对于 non-mod-rs 文件，规则相同，只是路径以该 non-mod-rs 模块名对应的目录开头。例如，下列代码片段会根据其所在位置使用所示路径：

<!-- ignore: requires external files -->
```rust
mod inline {
    #[path = "other.rs"]
    mod inner;
}
```

源文件         | `inner` 的文件位置        | `inner` 的模块路径
-------------- | --------------------------| ----------------------------
`src/a/b.rs`   | `src/a/b/inline/other.rs` | `crate::a::b::inline::inner`
`src/a/mod.rs` | `src/a/inline/other.rs`   | `crate::a::inline::inner`

将上述内联模块上的 `path` 属性规则与其中的嵌套模块相结合的例子（同时适用于 mod-rs 和 non-mod-rs 文件）：

<!-- ignore: requires external files -->
```rust
#[path = "thread_files"]
mod thread {
    // 从相对于本源文件目录的 `thread_files/tls.rs` 加载 `local_data` 模块。
    #[path = "tls.rs"]
    mod local_data;
}
```

r[items.mod.attributes]
## 模块上的属性

r[items.mod.attributes.intro]
模块与所有项一样接受外部属性。它们也接受内部属性：对于带函数体的模块，位于 `{` 之后；或者位于源文件开头，在可选的 BOM 和 shebang 之后。

r[items.mod.attributes.supported]
在模块上有意义的内置属性有 [`cfg`]、[`deprecated`]、[`doc`]、[lint 检查属性][the lint check attributes]、[`path`] 和 [`no_implicit_prelude`]。模块也接受宏属性。

[`cfg`]: ../conditional-compilation.md
[`deprecated`]: ../attributes/diagnostics.md#the-deprecated-attribute
[`doc`]: ../../rustdoc/the-doc-attribute.html
[`no_implicit_prelude`]: ../names/preludes.md#the-no_implicit_prelude-attribute
[`path`]: #the-path-attribute
[attribute]: ../attributes.md
[items]: ../items.md
[module path]: ../paths.md
[scopes chapter]: ../names/scopes.md
[the lint check attributes]: ../attributes/diagnostics.md#lint-check-attributes
[type namespace]: ../names/namespaces.md
