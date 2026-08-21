+++
title = "08-联合体"
date = 2026-08-18T08:45:00+08:00
weight = 25
type = "docs"
description = "联合体 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/items/unions.html](https://doc.rust-lang.org/reference/items/unions.html)

r[items.union]
# 联合体

r[items.union.syntax]
```grammar,items
Union ->
    `union` IDENTIFIER GenericParams? WhereClause? `{` StructFields? `}`
```

r[items.union.intro]
联合体声明使用与结构体声明相同的语法，只是用 `union` 代替 `struct`。

r[items.union.namespace]
联合体声明在其所在模块或块的[类型命名空间][type namespace]中定义给定名称。

```rust
#[repr(C)]
union MyUnion {
    f1: u32,
    f2: f32,
}
```

r[items.union.common-storage]
联合体的关键性质是其所有字段共享同一存储。因此，写入联合体的一个字段可以覆盖其他字段，联合体的大小由其最大字段的大小决定。

r[items.union.field-restrictions]
联合体字段类型被限制为以下类型子集：

r[items.union.field-copy]
- `Copy` 类型

r[items.union.field-references]
- 引用（任意 `T` 的 `&T` 和 `&mut T`）

r[items.union.field-manually-drop]
- `ManuallyDrop<T>`（任意 `T`）

r[items.union.field-tuple]
- 只包含允许的联合体字段类型的元组和数组

r[items.union.drop]
这一限制特别保证了联合体字段永远不需要被析构。与结构体和枚举一样，可以为联合体 `impl Drop`，以手动定义它被析构时发生什么。

r[items.union.fieldless]
编译器不接受没有任何字段的联合体，但宏可以接受它们。

r[items.union.init]
## 联合体的初始化

r[items.union.init.intro]
联合体类型的值可以使用与结构体类型相同的语法创建，只不过必须恰好指定一个字段：

```rust
## union MyUnion { f1: u32, f2: f32 }
#
let u = MyUnion { f1: 1 };
```

r[items.union.init.result]
上面的表达式创建类型为 `MyUnion` 的值，并使用字段 `f1` 初始化存储。可以使用与结构体字段相同的语法访问该联合体：

```rust
## union MyUnion { f1: u32, f2: f32 }
#
## let u = MyUnion { f1: 1 };
let f = unsafe { u.f1 };
```

r[items.union.fields]
## 读写联合体字段

r[items.union.fields.intro]
联合体没有“活动字段”的概念。相反，每次联合体访问都只是把存储解释为用于该次访问的字段的类型。

r[items.union.fields.read]
读取联合体字段会按该字段的类型读取联合体的各个位。

r[items.union.fields.offset]
字段可能具有非零偏移（使用 [C 表示][the C representation]时除外）；此时从字段偏移处开始读取各位。

r[items.union.fields.validity]
程序员有责任确保数据在该字段的类型下是合法的。未能做到会导致[未定义行为][undefined behavior]。例如，从[布尔类型][boolean type]的字段读取值 `3` 是未定义行为。实际上，对使用 [C 表示][the C representation]的联合体先写后读，类似于把用于写入的类型 [`transmute`] 到用于读取的类型。

r[items.union.fields.read-safety]
因此，所有对联合体字段的读取都必须放在 `unsafe` 块中：

```rust
## union MyUnion { f1: u32, f2: f32 }
## let u = MyUnion { f1: 1 };
#
unsafe {
    let f = u.f1;
}
```

使用联合体的代码通常会在不安全的联合体字段访问外包一层安全封装。

r[items.union.fields.write-safety]
相比之下，写入联合体字段是安全的，因为它们只是覆盖任意数据，而不能导致未定义行为。（注意联合体字段类型永远不能具有析构胶水，因此写入联合体字段永远不会隐式析构任何东西。）

r[items.union.pattern]
## 对联合体进行模式匹配

r[items.union.pattern.intro]
访问联合体字段的另一种方式是使用模式匹配。

r[items.union.pattern.one-field]
对联合体字段的模式匹配使用与结构体模式相同的语法，只不过模式必须恰好指定一个字段。

r[items.union.pattern.safety]
由于模式匹配就像用特定字段读取联合体，因此也必须放在 `unsafe` 块中。

```rust
## union MyUnion { f1: u32, f2: f32 }
#
fn f(u: MyUnion) {
    unsafe {
        match u {
            MyUnion { f1: 10 } => { println!("ten"); }
            MyUnion { f2 } => { println!("{}", f2); }
        }
    }
}
```

> **警告**
> 模式中子模式的测试顺序未指定。即使整个模式并不匹配，模式中命名的联合体字段仍可能被读取。除非联合体字段持有其类型的合法值，否则读取该字段是未定义行为（参见 [items.union.fields.validity]）。不能依赖模式中的其他部分来阻止这次读取。
>
> 特别是，在实现 C 风格的带标签联合体时，避免在单个模式中同时匹配标签和对应的联合体字段：即使标签不匹配，联合体字段仍可能被读取。
>
> 要仅在条件成立时读取联合体字段，应在求值顺序已指定的独立步骤中先测试条件再读取字段。对于 C 带标签联合体，先匹配标签，再在匹配的分支内读取联合体字段：
>
> ```rust
> #[repr(u32)]
> enum Tag { I, F }
>
> #[repr(C)]
> union U {
>     i: i32,
>     f: f32,
> }
>
> #[repr(C)]
> struct Value {
>     tag: Tag,
>     u: U,
> }
>
> fn is_zero(v: Value) -> bool {
>     match v.tag {
>         Tag::I => unsafe { v.u.i == 0 },
>         Tag::F => unsafe { v.u.f == 0.0 },
>     }
> }
> ```

r[items.union.ref]
## 对联合体字段的引用

r[items.union.ref.intro]
由于联合体字段共享同一存储，获得对联合体一个字段的写访问可以同时获得对其余字段的写访问。

r[items.union.ref.borrow]
借用检查规则必须据此调整。因此，若联合体的一个字段被借用，则其所有其余字段在同一生命周期内也被借用。

```rust
## union MyUnion { f1: u32, f2: f32 }
// 错误：不能在同一时间将 `u`（经由 `u.f2`）可变借用超过一次
fn test() {
    let mut u = MyUnion { f1: 1 };
    unsafe {
        let b1 = &mut u.f1;
//                    ---- 第一次可变借用发生在这里（经由 `u.f1`）
        let b2 = &mut u.f2;
//                    ^^^^ 第二次可变借用发生在这里（经由 `u.f2`）
        *b1 = 5;
    }
//  - 第一次借用在这里结束
    assert_eq!(unsafe { u.f1 }, 5);
}
```

r[items.union.ref.use]
如你所见，在许多方面（布局、安全性和所有权除外）联合体的行为与结构体完全相同，这很大程度上是因为它们从结构体继承了语法形态。对于许多未提及的 Rust 语言方面也是如此（例如私有性、名称解析、类型推断、泛型、trait 实现、固有实现、连贯性、模式检查，等等）。

[`transmute`]: std::mem::transmute
[boolean type]: ../types/boolean.md
[the C representation]: ../type-layout.md#reprc-unions
[type namespace]: ../names/namespaces.md
[undefined behavior]: ../behavior-considered-undefined.md
