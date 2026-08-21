+++
title = "06-可见性与私有性"
date = 2026-08-18T08:45:00+08:00
weight = 101
type = "docs"
description = "可见性与私有性 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/visibility-and-privacy.html](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

r[vis]
# 可见性与私有性

r[vis.syntax]
```grammar,items
Visibility ->
      `pub`
    | `pub` `(` `crate` `)`
    | `pub` `(` `self` `)`
    | `pub` `(` `super` `)`
    | `pub` `(` `in` SimplePath `)`
```

r[vis.intro]
这两个术语经常互换使用，它们试图传达的是对“这个项能在这个位置使用吗？”这一问题的回答。

r[vis.name-hierarchy]
Rust 的名称解析在命名空间的全局层级上运行。层级中的每一级都可以看作是某个项。这些项是上文提到的那些，但也包括外部 crate。声明或定义一个新模块，可以看作是在定义处向该层级中插入一棵新树。

r[vis.privacy]
为了控制接口是否可以跨模块使用，Rust 会检查每一处对项的使用，以判断是否应被允许。私有性警告就是在此处生成的，或者说是“你使用了另一个模块的私有项，但不被允许”。

r[vis.default]
默认情况下，一切都是*私有*的，但有两个例外：`pub` Trait 中的关联项默认公开；`pub` 枚举中的枚举变体默认也公开。当一个项被声明为 `pub` 时，可以认为它对外部世界可访问。例如：

```rust
## fn main() {}
// 声明一个私有结构体
struct Foo;

// 声明一个带有私有字段的公开结构体
pub struct Bar {
    field: i32,
}

// 声明一个带有两个公开变体的公开枚举
pub enum State {
    PubliclyAccessibleState,
    PubliclyAccessibleState2,
}
```

r[vis.access]
基于项是公开还是私有这一概念，Rust 在两种情况下允许访问项：

1. 若一个项是公开的，那么只要能从某个模块 `m` 访问该项的所有祖先模块，就可以从 `m` 外部访问该项。也可能通过再导出来命名该项。见下文。
2. 若一个项是私有的，则当前模块及其后代可以访问它。

这两种情况在创建对外暴露公开 API 同时隐藏内部实现细节的模块层级时出人意料地强大。为帮助说明，下面是一些用例及其含义：

* 库开发者需要把功能暴露给链接其库的 crate。作为第一种情况的结果，这意味着任何外部可用的东西，从根到目标项必须都是 `pub`。链中的任何私有项都会禁止外部访问。

* crate 需要一个对自己全局可用的“辅助模块”，但不想把该辅助模块暴露为公开 API。为此，crate 层级的根处会有一个私有模块，该模块内部再拥有“公开 API”。因为整个 crate 都是根的后代，所以整个本地 crate 都可以通过第二种情况访问这个私有模块。

* 为模块编写单元测试时，常见做法是给被测模块加一个名为 `mod test` 的直接子模块。该模块可以通过第二种情况访问父模块的任何项，这意味着内部实现细节也可以从该子模块无缝测试。

第二种情况提到私有项“可以被”当前模块及其后代访问，但访问一个项的确切含义取决于该项是什么。

r[vis.use]
例如，访问一个模块意味着查看其内部（以导入更多项）。另一方面，访问一个函数意味着调用它。此外，路径表达式和导入语句也被视为访问一个项：仅当目标位于当前可见性作用域内时，该导入/表达式才有效。

下面是一段示例程序，它例证了上述三种情况：

```rust
// 此模块是私有的，意味着外部 crate 无法访问此模块。
// 不过，因为它在当前 crate 的根处是私有的，crate 中的任何模块
// 都可以访问此模块中任何公开可见的项。
mod crate_helper_module {

    // 当前 crate 中的任何东西都可以使用此函数
    pub fn crate_helper() {}

    // 此函数*不能*被 crate 中的其他任何东西使用。它在
    // `crate_helper_module` 之外不是公开可见的，因此只有当前模块及其后代可以访问它。
    fn implementation_detail() {}
}

// 此函数“对根公开”，意味着链接本 crate 的外部 crate 可以使用它。
pub fn public_api() {}

// 与 'public_api' 类似，此模块是公开的，因此外部 crate 可以查看其内部。
pub mod submodule {
    use crate::crate_helper_module;

    pub fn my_method() {
        // 本地 crate 中的任何项都可以通过上述两条规则的组合
        // 调用辅助模块的公开接口。
        crate_helper_module::crate_helper();
    }

    // 此函数对任何不是 `submodule` 后代的模块隐藏
    fn my_implementation() {}

    #[cfg(test)]
    mod test {

        #[test]
        fn test_my_implementation() {
            // 因为此模块是 `submodule` 的后代，所以允许访问
            // `submodule` 内部的私有项，而不会违反私有性。
            super::my_implementation();
        }
    }
}

## fn main() {}
```

要使 Rust 程序通过私有性检查，所有路径都必须是上述两条规则下的有效访问。这包括所有 use 语句、表达式、类型等。

r[vis.scoped]
## `pub(in path)`、`pub(crate)`、`pub(super)` 和 `pub(self)`

r[vis.scoped.intro]
除了公开和私有之外，Rust 还允许用户将项声明为仅在给定作用域内可见。`pub` 限制的规则如下：

r[vis.scoped.in]
- `pub(in path)` 使项在所提供的 `path` 内可见。`path` 必须是解析到正在声明可见性的项的某个祖先模块的简单路径。`path` 中的每个标识符都必须直接指代一个模块（而不是由 `use` 语句引入的名称）。

r[vis.scoped.crate]
- `pub(crate)` 使项在当前 crate 内可见。

r[vis.scoped.super]
- `pub(super)` 使项对父模块可见。这等价于 `pub(in super)`。

r[vis.scoped.self]
- `pub(self)` 使项对当前模块可见。这等价于 `pub(in self)`，或者根本不使用 `pub`。

r[vis.scoped.edition2018]
> [!EDITION-2018]
> 从 2018 edition 开始，`pub(in path)` 的路径必须以 `crate`、`self` 或 `super` 开头。2015 edition 还可以使用以 `::` 开头的路径，或从 crate 根出发的模块。

下面是一个例子：

```rust
pub mod outer_mod {
    pub mod inner_mod {
        // 此函数在 `outer_mod` 内可见
        pub(in crate::outer_mod) fn outer_mod_visible_fn() {}
        // 与上面相同，这仅在 2015 edition 中有效。
        pub(in outer_mod) fn outer_mod_visible_fn_2015() {}

        // 此函数对整个 crate 可见
        pub(crate) fn crate_visible_fn() {}

        // 此函数在 `outer_mod` 内可见
        pub(super) fn super_mod_visible_fn() {
            // 此函数可见，因为我们在同一个 `mod` 中
            inner_mod_visible_fn();
        }

        // 此函数仅在 `inner_mod` 内可见，
        // 这与保持私有相同。
        pub(self) fn inner_mod_visible_fn() {}
    }
    pub fn foo() {
        inner_mod::outer_mod_visible_fn();
        inner_mod::crate_visible_fn();
        inner_mod::super_mod_visible_fn();

        // 此函数不再可见，因为我们在 `inner_mod` 之外
        // 错误！`inner_mod_visible_fn` 是私有的
        //inner_mod::inner_mod_visible_fn();
    }
}

fn bar() {
    // 此函数仍然可见，因为我们在同一个 crate 中
    outer_mod::inner_mod::crate_visible_fn();

    // 此函数不再可见，因为我们在 `outer_mod` 之外
    // 错误！`super_mod_visible_fn` 是私有的
    //outer_mod::inner_mod::super_mod_visible_fn();

    // 此函数不再可见，因为我们在 `outer_mod` 之外
    // 错误！`outer_mod_visible_fn` 是私有的
    //outer_mod::inner_mod::outer_mod_visible_fn();

    outer_mod::foo();
}

fn main() { bar() }
```

> **注意**
> 此语法只是给项的可见性额外增加了一层限制。它并不保证该项在指定作用域的所有部分都可见。要访问一个项，直到当前作用域为止的所有父项也必须仍然可见。

r[vis.reexports]
## 再导出与可见性

r[vis.reexports.intro]
Rust 允许通过 `pub use` 声明公开再导出项。因为这是公开声明，所以允许根据上述规则在当前模块中使用该项。它本质上允许对再导出的项进行公开访问。例如，下面的程序是有效的：

```rust
pub use self::implementation::api;

mod implementation {
    pub mod api {
        pub fn f() {}
    }
}

## fn main() {}
```

这意味着任何外部 crate 引用 `implementation::api::f` 都会因违反私有性而报错，而路径 `api::f` 则被允许。

r[vis.reexports.private-item]
再导出私有项时，可以认为是允许“私有性链”通过再导出被短路，而不是像通常那样穿过命名空间层级。
