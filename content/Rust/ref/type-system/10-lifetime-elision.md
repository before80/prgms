+++
title = "10-生命周期省略"
date = 2026-08-18T08:45:00+08:00
weight = 93
type = "docs"
description = "生命周期省略 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/lifetime-elision.html](https://doc.rust-lang.org/reference/lifetime-elision.html)

r[lifetime-elision]
# 生命周期省略

Rust 有一些规则，允许在编译器可以推断出合理默认选择的各种位置省略生命周期。

r[lifetime-elision.function]
## 函数中的生命周期省略

r[lifetime-elision.function.intro]
为了使常见模式更符合人体工学，可以在[函数项][function item]、[函数指针][function pointer]和[闭包 trait][closure trait]签名中 *省略* 生命周期参数。以下规则用于为被省略的生命周期推断生命周期参数。

r[lifetime-elision.function.lifetimes-not-inferred]
省略无法推断的生命周期参数是错误。

r[lifetime-elision.function.explicit-placeholder]
占位生命周期 `'_` 也可以用于以相同方式推断生命周期。对于路径中的生命周期，更推荐使用 `'_`。

r[lifetime-elision.function.only-functions]
Trait 对象生命周期遵循[下文](#default-trait-object-lifetimes)讨论的不同规则。

r[lifetime-elision.function.implicit-lifetime-parameters]
* 参数中每个被省略的生命周期都成为一个不同的生命周期参数。

r[lifetime-elision.function.output-lifetime]
* 若参数中恰好使用了一个生命周期（无论是否省略），则该生命周期被赋给 *所有* 被省略的输出生命周期。

r[lifetime-elision.function.receiver-lifetime]
在方法签名中还有另一条规则

* 若接收者的类型为 `&Self` 或 `&mut Self`，则该指向 `Self` 的引用的生命周期被赋给所有被省略的输出生命周期参数。

示例：

```rust
## trait T {}
## trait ToCStr {}
## struct Thing<'a> {f: &'a i32}
## struct Command;
#
## trait Example {
fn print1(s: &str);                                   // 已省略
fn print2(s: &'_ str);                                // 同样已省略
fn print3<'a>(s: &'a str);                            // 展开后

fn debug1(lvl: usize, s: &str);                       // 已省略
fn debug2<'a>(lvl: usize, s: &'a str);                // 展开后

fn substr1(s: &str, until: usize) -> &str;            // 已省略
fn substr2<'a>(s: &'a str, until: usize) -> &'a str;  // 展开后

fn get_mut1(&mut self) -> &mut dyn T;                 // 已省略
fn get_mut2<'a>(&'a mut self) -> &'a mut dyn T;       // 展开后

fn args1<T: ToCStr>(&mut self, args: &[T]) -> &mut Command;                  // 已省略
fn args2<'a, 'b, T: ToCStr>(&'a mut self, args: &'b [T]) -> &'a mut Command; // 展开后

fn other_args1<'a>(arg: &str) -> &'a str;             // 已省略
fn other_args2<'a, 'b>(arg: &'b str) -> &'a str;      // 展开后

fn new1(buf: &mut [u8]) -> Thing<'_>;                 // 已省略 - 更推荐
fn new2(buf: &mut [u8]) -> Thing;                     // 已省略
fn new3<'a>(buf: &'a mut [u8]) -> Thing<'a>;          // 展开后
## }

type FunPtr1 = fn(&str) -> &str;                      // 已省略
type FunPtr2 = for<'a> fn(&'a str) -> &'a str;        // 展开后

type FunTrait1 = dyn Fn(&str) -> &str;                // 已省略
type FunTrait2 = dyn for<'a> Fn(&'a str) -> &'a str;  // 展开后
```

```rust
// 以下例子展示了不允许省略生命周期参数的情形。

## trait Example {
// 无法推断，因为没有可从中推断的参数。
fn get_str() -> &str;                                 // 非法

// 无法推断，无法确定是从第一个还是第二个参数借用。
fn frob(s: &str, t: &str) -> &str;                    // 非法
## }
```

r[lifetime-elision.trait-object]
## 默认 trait 对象生命周期

r[lifetime-elision.trait-object.intro]
[Trait 对象][trait object]所持有引用的假定生命周期称为其 _默认对象生命周期约束_。这些在 [RFC 599] 中定义，并在 [RFC 1156] 中修订。

r[lifetime-elision.trait-object.explicit-bound]
当生命周期约束被完全省略时，使用这些默认对象生命周期约束，而不是上面定义的生命周期参数省略规则。

r[lifetime-elision.trait-object.explicit-placeholder]
若使用 `'_` 作为生命周期约束，则该约束遵循通常的省略规则。

r[lifetime-elision.trait-object.containing-type]
若 trait 对象用作泛型类型的类型实参，则首先使用包含类型尝试推断约束。

r[lifetime-elision.trait-object.containing-type-unique]
* 若包含类型有唯一约束，则该约束即为默认值。

r[lifetime-elision.trait-object.containing-type-explicit]
* 若包含类型有多于一个约束，则必须指定显式约束。

r[lifetime-elision.trait-object.trait-bounds]
若上述规则都不适用，则使用该 trait 上的约束：

r[lifetime-elision.trait-object.trait-unique]
* 若该 trait 定义时带有单个生命周期 _约束_，则使用该约束。

r[lifetime-elision.trait-object.static-lifetime]
* 若任何生命周期约束使用了 `'static`，则使用 `'static`。

r[lifetime-elision.trait-object.default]
* 若该 trait 没有生命周期约束，则在表达式中推断生命周期，在表达式之外为 `'static`。

```rust
// 对于以下 trait...
trait Foo { }

// 这两者相同，因为 Box<T> 在 T 上没有生命周期约束
type T1 = Box<dyn Foo>;
type T2 = Box<dyn Foo + 'static>;

// ...下面这些也相同：
impl dyn Foo {}
impl dyn Foo + 'static {}

// ...下面这些也相同，因为 &'a T 要求 T: 'a
type T3<'a> = &'a dyn Foo;
type T4<'a> = &'a (dyn Foo + 'a);

// std::cell::Ref<'a, T> 也要求 T: 'a，因此这些相同
type T5<'a> = std::cell::Ref<'a, dyn Foo>;
type T6<'a> = std::cell::Ref<'a, dyn Foo + 'a>;
```

```rust
// 这是一个错误的例子。
## trait Foo { }
struct TwoBounds<'a, 'b, T: ?Sized + 'a + 'b> {
    f1: &'a i32,
    f2: &'b i32,
    f3: T,
}
type T7<'a, 'b> = TwoBounds<'a, 'b, dyn Foo>;
//                                  ^^^^^^^
// 错误：无法从上下文推断此对象类型的生命周期约束
```

r[lifetime-elision.trait-object.innermost-type]
注意是最内层的对象设定约束，因此 `&'a Box<dyn Foo>` 仍然是 `&'a Box<dyn Foo + 'static>`。

```rust
// 对于以下 trait...
trait Bar<'a>: 'a { }

// ...这两者相同：
type T1<'a> = Box<dyn Bar<'a>>;
type T2<'a> = Box<dyn Bar<'a> + 'a>;

// ...下面这些也相同：
impl<'a> dyn Bar<'a> {}
impl<'a> dyn Bar<'a> + 'a {}
```

r[lifetime-elision.const-static]
## `const` 和 `static` 的省略

r[lifetime-elision.const-static.implicit-static]
引用类型的 [const][constant] 和 [static] 声明除非指定了显式生命周期，否则都具有 *隐式* 的 `'static` 生命周期。因此，上面涉及 `'static` 的常量声明可以不写生命周期。

```rust
// STRING: &'static str
const STRING: &str = "bitstring";

struct BitsNStrings<'a> {
    mybits: [u32; 2],
    mystring: &'a str,
}

// BITS_N_STRINGS: BitsNStrings<'static>
const BITS_N_STRINGS: BitsNStrings<'_> = BitsNStrings {
    mybits: [1, 2],
    mystring: STRING,
};
```

r[lifetime-elision.const-static.fn-references]
注意，若 `static` 或 `const` 项包含函数或闭包引用，而这些引用自身又包含引用，编译器会首先尝试标准省略规则。若无法用其通常规则解析生命周期，则会报错。例如：

```rust
## struct Foo;
## struct Bar;
## struct Baz;
## fn somefunc(a: &Foo, b: &Bar, c: &Baz) -> usize {42}
// 解析为 `for<'a> fn(&'a str) -> &'a str`。
const RESOLVED_SINGLE: fn(&str) -> &str = |x| x;

// 解析为 `for<'a, 'b, 'c> Fn(&'a Foo, &'b Bar, &'c Baz) -> usize`。
const RESOLVED_MULTIPLE: &dyn Fn(&Foo, &Bar, &Baz) -> usize = &somefunc;
```

```rust
## struct Foo;
## struct Bar;
## struct Baz;
## fn somefunc<'a,'b>(a: &'a Foo, b: &'b Bar) -> &'a Baz {unimplemented!()}
// 没有足够的信息将返回引用的生命周期相对于
// 参数生命周期进行约束，因此这是错误。
const RESOLVED_STATIC: &dyn Fn(&Foo, &Bar) -> &Baz = &somefunc;
//                                            ^
// 此函数的返回类型包含借用值，但签名
// 并未说明它是从第 1 个还是第 2 个参数借用的
```

[closure trait]: types/closure.md
[constant]: items/constant-items.md
[function item]: types/function-item.md
[function pointer]: types/function-pointer.md
[RFC 599]: https://github.com/rust-lang/rfcs/blob/master/text/0599-default-object-bound.md
[RFC 1156]: https://github.com/rust-lang/rfcs/blob/master/text/1156-adjust-default-object-bounds.md
[static]: items/static-items.md
[trait object]: types/trait-object.md
