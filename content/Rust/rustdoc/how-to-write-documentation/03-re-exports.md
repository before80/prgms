+++
title = "03-重导出"
date = 2026-08-01T07:35:00+08:00
weight = 43
type = "docs"
description = "重导出项的文档行为"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [The rustdoc book](https://doc.rust-lang.org/rustdoc/)

# 重导出 {#re-exports}


> 原文链接: [https://doc.rust-lang.org/rustdoc/write-documentation/re-exports.html](https://doc.rust-lang.org/rustdoc/write-documentation/re-exports.html)


先解释什么是重导出。为此用一个例子：我们正在编写一个库（名为 `lib`），其中一些类型分散在子模块中：

```rust
pub mod sub_module1 {
    pub struct Foo;
}
pub mod sub_module2 {
    pub struct AnotherFoo;
}
```

用户可以这样导入：

```rust,ignore (inline)
use lib::sub_module1::Foo;
use lib::sub_module2::AnotherFoo;
```

但如果你希望这些类型直接在 crate 根可用，或不希望模块对用户可见？这就用到重导出：

```rust,ignore (inline)
// `sub_module1` 和 `sub_module2` 在外部不可见。
mod sub_module1 {
    pub struct Foo;
}
mod sub_module2 {
    pub struct AnotherFoo;
}
// 我们重导出这两个类型：
pub use crate::sub_module1::Foo;
pub use crate::sub_module2::AnotherFoo;
```

现在用户可以这样做：

```rust,ignore (inline)
use lib::{Foo, AnotherFoo};
```

并且由于 `sub_module1` 和 `sub_module2` 都是私有的，用户无法导入它们。

有趣的是，为该 crate 生成的文档会直接在 crate 根显示 `Foo` 和 `AnotherFoo`，这意味着它们已被内联。关于重导出项是否会内联，有几条规则需要了解。

## 内联规则 {#inlining-rules}

若公开项来自私有模块，它会被内联：

```rust,ignore (inline)
mod private_module {
    pub struct Public;
}
pub mod public_mod {
    // `Public` 会在此内联，因为 `private_module` 是私有的。
    pub use super::private_module::Public;
}
// `Public` 不会在此内联，因为 `public_mod` 是公开的。
pub use self::public_mod::Public;
```

同样，若项从其任一祖先继承了 `#[doc(hidden)]`，它也会被内联：

```rust,ignore (inline)
#[doc(hidden)]
pub mod public_mod {
    pub struct Public;
}
// `Public` 会被内联，因为其父级（`public_mod`）有 `#[doc(hidden)]`。
pub use self::public_mod::Public;
```

若项本身有 `#[doc(hidden)]`，则不会被内联（也不会出现在生成的文档中）：

```rust,ignore (inline)
// 该结构体不会可见。
#[doc(hidden)]
pub struct Hidden;

// 该重导出不会可见。
pub use self::Hidden as InlinedHidden;
```

不过，若仍希望重导出本身可见，可以在其上添加 `#[doc(inline)]` 属性：

```rust,ignore (inline)
// 该结构体不会可见。
#[doc(hidden)]
pub struct Hidden;

#[doc(inline)]
pub use self::Hidden as InlinedHidden;
```

这种情况下，生成的文档中会有 `pub use self::Hidden as InlinedHidden;`，但没有指向 `Hidden` 项的链接。

回到 `#[doc(hidden)]`：若有多个重导出且其中一些有 `#[doc(hidden)]`，则只有这些（且仅这些）不会出现在文档中：

```rust,ignore (inline)
mod private_mod {
    /// 第一
    pub struct InPrivate;
}

/// 第二
#[doc(hidden)]
pub use self::private_mod::InPrivate as Hidden;
/// 第三
pub use self::Hidden as Visible;
```

这种情况下，`InPrivate` 会作为 `Visible` 被内联。但其文档会是 `第一 第三` 而不是 `第一 第二 第三`，因为带有「第二」文档的那个重导出有 `#[doc(hidden)]`，因此其所有属性都被忽略。

## 用 `#[doc(inline)]` 内联 {#inlining-with-docinline}

若想强制内联某项，可以使用 `#[doc(inline)]` 属性：

```rust,ignore (inline)
pub mod public_mod {
    pub struct Public;
}
#[doc(inline)]
pub use self::public_mod::Public;
```

有了这段代码，即使 `public_mod::Public` 是公开的且已出现在文档中，`Public` 类型也会同时出现在 crate 根和 `public_mod` 模块中。

## 用 `#[doc(no_inline)]` 阻止内联 {#preventing-inlining-with-docno-inline}

与 `#[doc(inline)]` 相反，若想阻止某项被内联，可以使用 `#[doc(no_inline)]`：

```rust,ignore (inline)
mod private_mod {
    pub struct Public;
}
#[doc(no_inline)]
pub use self::private_mod::Public;
```

在生成的文档中，你会在 crate 根看到一个重导出，而不是直接看到该类型。

## 属性 {#attributes}

当项被内联时，其文档注释和大部分属性会一并内联：

```rust,ignore (inline)
mod private_mod {
    /// 第一
    #[cfg(a)]
    pub struct InPrivate;
    /// 第二
    #[cfg(b)]
    pub use self::InPrivate as Second;
}

/// 第三
#[doc(inline)]
#[cfg(c)]
pub use self::private_mod::Second as Visible;
```

这种情况下，`Visible` 的文档会是 `第一 第二 第三`，其 `cfg` 也会有：`#[cfg(a)]`、`#[cfg(b)]` 和 `#[cfg(c)]`。

[文档内链接（intra-doc links）](04-linking-to-items-by-name/) 相对于文档注释的定义位置解析。

不过有少数属性不会被内联：
 * `#[doc(alias="")]`
 * `#[doc(inline)]`
 * `#[doc(no_inline)]`
 * `#[doc(hidden)]`（因为重导出本身及其属性都被忽略）。

其余属性在内联时都会继承，使文档行为与该项直接定义在展示位置时一致。

若项通过 glob 重导出内联，这些规则同样适用：

```rust,ignore (inline)
mod private_mod {
    /// 第一
    #[cfg(a)]
    pub struct InPrivate;
}

#[cfg(c)]
pub use self::private_mod::*;
```

否则，显示的属性来自被重导出的项，重导出本身上的属性会被忽略：

```rust,ignore (inline)
mod private_mod {
    /// 第一
    #[cfg(a)]
    pub struct InPrivate;
}

#[cfg(c)]
pub use self::private_mod::InPrivate;
```

在上述情况中，`cfg(c)` 不会显示在文档里。
