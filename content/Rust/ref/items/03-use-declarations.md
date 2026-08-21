+++
title = "03-use 声明"
date = 2026-08-18T08:45:00+08:00
weight = 20
type = "docs"
description = "use 声明 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/use-declarations.html](https://doc.rust-lang.org/reference/items/use-declarations.html)

r[items.use]
# use 声明

r[items.use.syntax]
```grammar,items
UseDeclaration -> `use` UseTree `;`

UseTree ->
      (SimplePath? `::`)? `*`
    | (SimplePath? `::`)? `{` (UseTree ( `,`  UseTree )* `,`?)? `}`
    | SimplePath ( `as` ( IDENTIFIER | `_` ) )?
```

r[items.use.intro]
*use 声明*创建一或多个与某个其他[路径][path]同义的局部名称绑定。通常用 `use` 声明来缩短引用模块项所需的路径。这些声明可以出现在[模块][modules]和[块][blocks]中，通常位于顶部。`use` 声明有时也称为*导入*；若它是公开的，则称为*再导出*。

[path]: ../paths.md
[modules]: modules.md
[blocks]: ../expressions/block-expr.md

r[items.use.forms]
use 声明支持若干便利的简写：

r[items.use.forms.multiple]
* 使用花括号语法 `use a::b::{c, d, e::f, g::h::i};` 同时绑定具有公共前缀的一组路径

r[items.use.forms.self]
* 使用 `self` 关键字同时绑定具有公共前缀的一组路径及其公共父模块，例如 `use a::b::{self, c, d::e};`

r[items.use.forms.as]
* 使用语法 `use p::q::r as x;` 将目标名称重新绑定为新的局部名称。也可以与前两项特性组合：`use a::b::{self as ab, c as abc}`。

r[items.use.forms.glob]
* 使用星号通配符语法 `use a::b::*;` 绑定匹配给定前缀的所有路径。

r[items.use.forms.nesting]
* 多次嵌套上述特性的分组，例如 `use a::b::{self as ab, c, d::{*, e::f}};`

`use` 声明的一个例子：

```rust
use std::collections::hash_map::{self, HashMap};

fn foo<T>(_: T){}
fn bar(map1: HashMap<String, usize>, map2: hash_map::HashMap<String, usize>){}

fn main() {
    // use 声明也可以出现在函数内部
    use std::option::Option::{Some, None};

    // 等价于 'foo(vec![std::option::Option::Some(1.0f64),
    // std::option::Option::None]);'
    foo(vec![Some(1.0f64), None]);

    // `hash_map` 和 `HashMap` 都在作用域中。
    let map1 = HashMap::new();
    let map2 = hash_map::HashMap::new();
    bar(map1, map2);
}
```

r[items.use.visibility]
## `use` 的可见性

r[items.use.visibility.intro]
与项一样，`use` 声明默认对其所在模块私有。同样与项一样，若以 `pub` 关键字限定，`use` 声明可以是公开的。这样的 `use` 声明用于*再导出*一个名称。因此，公开的 `use` 声明可以把某个公开名称*重定向*到不同的目标定义：甚至可以是位于另一个模块中、具有私有规范路径的定义。

r[items.use.visibility.unambiguous]
若这样一连串重定向形成环，或无法唯一解析，则构成编译期错误。

再导出的一个例子：

```rust
mod quux {
    pub use self::foo::{bar, baz};
    pub mod foo {
        pub fn bar() {}
        pub fn baz() {}
    }
}

fn main() {
    quux::bar();
    quux::baz();
}
```

在此例中，模块 `quux` 再导出了在 `foo` 中定义的两个公开名称。

r[items.use.path]
## `use` 路径

r[items.use.path.intro]
`use` 项中允许的[路径][paths]遵循 [SimplePath] 语法，并类似于表达式中可以使用的路径。它们可以为以下对象创建绑定：

* 可命名的[项][items]
* [枚举变体][Enum variants]
* [内置类型][Built-in types]
* [属性][Attributes]
* [Derive 宏][Derive macros]
* [`macro_rules`]

r[items.use.path.disallowed]
它们不能导入[关联项][associated items]、[泛型参数][generic parameters]、[局部变量][local variables]、带 [`Self`] 的路径，或[工具属性][tool attributes]。更多限制见下文。

r[items.use.path.namespace]
`use` 会为所导入实体的所有[命名空间][namespaces]创建绑定，例外是 `self` 导入只从类型命名空间导入（如下所述）。例如，下列代码说明了为同一名称在两个命名空间中创建绑定：

```rust
mod stuff {
    pub struct Foo(pub i32);
}

// 导入 `Foo` 类型和 `Foo` 构造器。
use stuff::Foo;

fn example() {
    let ctor = Foo; // 使用值命名空间中的 `Foo`。
    let x: Foo = ctor(123); // 使用类型命名空间中的 `Foo`。
}
```

r[items.use.path.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，`use` 路径相对于 crate 根。例如：
>
> ```rust
> mod foo {
>     pub mod example { pub mod iter {} }
>     pub mod baz { pub fn foobaz() {} }
> }
> mod bar {
>     // 从 crate 根解析 `foo`。
>     use foo::example::iter;
>     // `::` 前缀显式从 crate 根解析 `foo`。
>     use ::foo::baz::foobaz;
> }
>
> # fn main() {}
> ```
>
> 2015 edition 不允许 use 声明引用 [extern prelude]。因此，在 2015 edition 中仍需 [`extern crate`] 声明才能在 `use` 声明中引用外部 crate。从 2018 edition 开始，`use` 声明可以用与 `extern crate` 相同的方式指定外部 crate 依赖。

r[items.use.as]
## `as` 重命名

`as` 关键字可用于更改导入实体的名称。例如：

```rust
// 为函数 `foo` 创建一个非公开别名 `bar`。
use inner::foo as bar;

mod inner {
    pub fn foo() {}
}
```

r[items.use.multiple-syntax]
## 花括号语法

r[items.use.multiple-syntax.intro]
可以在路径的最后一段使用花括号，从前一段导入多个实体；若没有前一段，则从当前作用域导入。花括号可以嵌套，从而形成路径树，其中每一组路径段在逻辑上与其父级组合以构成完整路径。

```rust
// 创建对以下名称的绑定：
// - `std::collections::BTreeSet`
// - `std::collections::hash_map`
// - `std::collections::hash_map::HashMap`
use std::collections::{BTreeSet, hash_map::{self, HashMap}};
```

r[items.use.multiple-syntax.empty]
空花括号不导入任何内容，但仍会验证前导路径是可访问的。
<!-- This is slightly wrong, see: https://github.com/rust-lang/rust/issues/61826 -->

r[items.use.multiple-syntax.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，路径相对于 crate 根，因此诸如 `use {foo, bar};` 的导入会从 crate 根导入名称 `foo` 和 `bar`；而从 2018 开始，这些名称相对于当前作用域。

r[items.use.self]
## `self` 导入

r[items.use.self.intro]
关键字 `self` 可以在[花括号语法][brace syntax]中使用，以父实体自身的名称为其创建绑定。

```rust
mod stuff {
    pub fn foo() {}
    pub fn bar() {}
}
mod example {
    // 为 `stuff` 和 `foo` 创建绑定。
    use crate::stuff::{self, foo};
    pub fn baz() {
        foo();
        stuff::bar();
    }
}
## fn main() {}
```

> **注意**
> `self` 也可以用作路径的第一段。将 `self` 用作第一段与在 `use` 花括号内使用在逻辑上相同；它表示父段的当前模块，若没有父段则表示当前模块。关于前导 `self` 的含义，参见路径一章中的 [`self`]。

r[items.use.self.trailing]
`self` 可以出现在 `use` 路径的最后一段，前面带有 `::`。形式为 `P::self` 的路径等价于 `P::{self}`，而 `P::self as name` 等价于 `P::{self as name}`。

```rust
mod m {
    pub enum E { V1, V2 }
}
use m::self as _; // 等价于 `use m::{self as _};`。
use m::E::self; // 等价于 `use m::E::{self};`。
## fn main() {}
```

> **注意**
> 关于前导路径的限制，参见 [paths.qualifiers.mod-self.trailing]。

r[items.use.self.module]
当在[花括号语法][brace syntax]中使用 `self` 时，花括号组之前的路径必须解析为[模块][module]、[枚举][enumeration]或 [trait]。

```rust
mod m {
    pub enum E { V1, V2 }
    pub trait Tr { fn f(&self); }
}
use m::{self as _}; // 可以：模块可以作为 `self` 的父级。
use m::E::{self, V1}; // 可以：枚举可以作为 `self` 的父级。
use m::Tr::{self}; // 可以：trait 可以作为 `self` 的父级。
## fn main() {}
```

```rust
struct S {}
use S::{self as _}; // 错误：结构体不能作为 `self` 的父级。
## fn main() {}
```

r[items.use.self.namespace]
`self` 只从父实体的[类型命名空间][type namespace]创建绑定。例如，在下列代码中只导入了 `foo` 模块：

```rust
mod bar {
    pub mod foo {}
    pub fn foo() {}
}

// 这只导入模块 `foo`。函数 `foo` 位于
// 值命名空间中，不会被导入。
use bar::foo::{self};

fn main() {
    foo(); //~ ERROR `foo` is a module
}
```

r[items.use.glob]
## Glob 导入

r[items.use.glob.intro]
字符 `*` 可以用作 `use` 路径的最后一段，以从前一段实体导入所有可导入的实体。例如：

```rust
// 创建指向 `bar` 的非公开别名。
use foo::*;

mod foo {
    fn i_am_private() {}
    enum Example {
        V1,
        V2,
    }
    pub fn bar() {
        // 为 `Example` 枚举的 `V1` 和 `V2` 创建局部别名
        use Example::*;
        let x = V1;
    }
}
```

r[items.use.glob.shadowing]
项和具名导入允许在同一[命名空间][namespace]中遮蔽来自 glob 导入的名称。也就是说，若同一命名空间中已有另一项定义了该名称，则 glob 导入会被遮蔽。例如：

```rust
// 这会创建对 `clashing::Foo` 元组结构体构造器的绑定，
// 但不会导入其类型，因为那会与这里定义的 `Foo` 结构体冲突。
//
// 注意，此处的定义顺序并不重要。
use clashing::*;
struct Foo {
    field: f32,
}

fn do_stuff() {
    // 使用来自 `clashing::Foo` 的构造器。
    let f1 = Foo(123);
    // 结构体表达式使用上面定义的 `Foo` 结构体的类型。
    let f2 = Foo { field: 1.0 };
    // 由于 glob 导入，`Bar` 也在作用域中。
    let z = Bar {};
}

mod clashing {
    pub struct Foo(pub i32);
    pub struct Bar {}
}
```

> **注意**
> 关于不允许遮蔽的情况，参见[名称解析歧义][name resolution ambiguities]。

r[items.use.glob.last-segment-only]
`*` 不能用作第一段或中间段。

r[items.use.glob.self-import]
`*` 不能用于将模块的内容导入其自身（例如 `use self::*;`）。

r[items.use.glob.edition2018]
> [!EDITION-2018]
> 在 2015 edition 中，路径相对于 crate 根，因此诸如 `use *;` 的导入是合法的，表示从 crate 根导入一切。这不能在 crate 根本身中使用。

r[items.use.as-underscore]
## 下划线导入

r[items.use.as-underscore.intro]
可以使用带下划线的形式 `use path as _` 导入项而不绑定到名称。这在导入 trait 以便使用其方法、却又不想导入该 trait 的符号时特别有用，例如该 trait 的符号可能与另一符号冲突。另一个例子是链接外部 crate 而不导入其名称。

```rust
mod foo {
    pub trait Zoo {
        fn zoo(&self) {}
    }

    impl<T> Zoo for T {}
}

use self::foo::Zoo as _;
struct Zoo;  // 下划线导入避免了与此项的名称冲突。

fn main() {
    let z = Zoo;
    z.zoo();
}
```

r[items.use.as-underscore.glob]
星号 glob 导入会以不可命名的形式导入用 `_` 导入的项。

r[items.use.as-underscore.macro]
这些唯一且不可命名的符号在宏展开之后创建，以便宏可以安全地多次发出对 `_` 导入的引用。例如，下列代码不应产生错误：

```rust
macro_rules! m {
    ($item: item) => { $item $item }
}

m!(use std as _;);
// 这会展开为：
// use std as _;
// use std as _;
```

r[items.use.restrictions]
## 限制

下列规则是合法 `use` 声明的限制。

r[items.use.restrictions.crate-alias]
使用 `crate` 导入当前 crate 时，必须使用 `as` 来定义绑定名称。

> [!EXAMPLE]
> ```rust
> use crate as root;
> use crate::{self as root2};
>
> // 不允许：
> // use crate;
> // use crate::{self};
> ```

r[items.use.restrictions.macro-crate-alias]
在宏转写器中使用 [`$crate`] 导入当前 crate 时，必须使用 `as` 来定义绑定名称。

> [!EXAMPLE]
> ```rust
> macro_rules! import_crate_root {
>     () => {
>         use $crate as my_crate;
>         use $crate::{self as my_crate2};
>     };
> }
> ```

r[items.use.restrictions.self-alias]
使用 `self` 导入当前模块时，必须使用 `as` 来定义绑定名称。

> [!EXAMPLE]
> ```rust
> use {self as this_module};
> use self as this_module2;
> use self::{self as this_module3};
>
> // 不允许：
> // use {self};
> // use self;
> // use self::{self};
> ```

r[items.use.restrictions.super-alias]
使用 `super` 导入父模块时，必须使用 `as` 来定义绑定名称。

> [!EXAMPLE]
> ```rust
> mod a {
>     mod b {
>         use super as parent;
>         use super::{self as parent2};
>         use self::super as parent3;
>         use super::super as grandparent;
>         use super::super::{self as grandparent2};
>
>         // 不允许：
>         // use super;
>         // use super::{self};
>         // use self::super;
>         // use super::super;
>         // use super::super::{self};
>     }
> }
> ```

r[items.use.restrictions.extern-prelude]
不能导入作为 [extern prelude] 的 `::`。

> [!EXAMPLE]
> ```rust
> use ::{self as root}; //~ Error
> ```

> [!EDITION-2018]
> 在 2015 edition 中，前缀 `::` 指向 crate 根，因此 `use ::{self as root};` 是允许的，因为它与 `use crate::{self as root};` 相同。从 2018 edition 开始，`::` 前缀指向 extern prelude，不能直接导入。
>
> ```rust
> use ::{self as root}; //~ Ok
> ```

r[items.use.restrictions.duplicate-name]
与任何项定义一样，`use` 导入不能在模块或块的同一命名空间中创建同名的重复绑定。

r[items.use.restrictions.variant]
`use` 路径不能通过[类型别名][type alias]引用枚举变体。

> [!EXAMPLE]
> ```rust
> enum MyEnum {
>   MyVariant
> }
> type TypeAlias = MyEnum;
>
> use MyEnum::MyVariant; //~ OK
> use TypeAlias::MyVariant; //~ ERROR
> ```

[`$crate`]: paths.qualifiers.macro-crate
[Attributes]: ../attributes.md
[brace syntax]: items.use.multiple-syntax
[Built-in types]: ../types.md
[Derive macros]: macro.proc.derive
[Enum variants]: enumerations.md
[enumeration]: items.enum
[`extern crate`]: extern-crates.md
[`macro_rules`]: ../macros-by-example.md
[`self`]: ../paths.md#self
[associated items]: associated-items.md
[extern prelude]: ../names/preludes.md#extern-prelude
[generic parameters]: generics.md
[items]: ../items.md
[local variables]: ../variables.md
[module]: items.mod
[name resolution ambiguities]: names.resolution.expansion.imports.ambiguity
[namespace]: ../names/namespaces.md
[namespaces]: ../names/namespaces.md
[paths]: ../paths.md
[tool attributes]: ../attributes.md#tool-attributes
[trait]: items.traits
[type alias]: type-aliases.md
[type namespace]: ../names/namespaces.md
