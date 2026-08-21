+++
title = "13-闭包类型"
date = 2026-08-18T08:45:00+08:00
weight = 78
type = "docs"
description = "闭包类型 — The Rust Reference"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [The Rust Reference](https://doc.rust-lang.org/reference/)

> 原文链接: [https://doc.rust-lang.org/reference/types/closure.html](https://doc.rust-lang.org/reference/types/closure.html)

r[type.closure]
# 闭包类型

r[type.closure.intro]
[闭包表达式][closure expression]产生一个具有无法写出的唯一匿名类型的闭包值。闭包类型大致等价于包含被捕获值的结构体。例如，下面的闭包：

```rust
#[derive(Debug)]
struct Point { x: i32, y: i32 }
struct Rectangle { left_top: Point, right_bottom: Point }

fn f<F : FnOnce() -> String> (g: F) {
    println!("{}", g());
}

let mut rect = Rectangle {
    left_top: Point { x: 1, y: 1 },
    right_bottom: Point { x: 0, y: 0 }
};

let c = || {
    rect.left_top.x += 1;
    rect.right_bottom.x += 1;
    format!("{:?}", rect.left_top)
};
f(c); // 打印 "Point { x: 2, y: 1 }"。
```

会生成大致如下的闭包类型：

<!-- ignore: simplified -->
```rust
// 注意：这并非实际的转换方式，仅用于
// 说明。

struct Closure<'a> {
    left_top : &'a mut Point,
    right_bottom_x : &'a mut i32,
}

impl<'a> FnOnce<()> for Closure<'a> {
    type Output = String;
    extern "rust-call" fn call_once(self, args: ()) -> String {
        self.left_top.x += 1;
        *self.right_bottom_x += 1;
        format!("{:?}", self.left_top)
    }
}
```

因此对 `f` 的调用工作起来就像：

<!-- ignore: continuation of above -->
```rust
f(Closure{ left_top: &mut rect.left_top, right_bottom_x: &mut rect.right_bottom.x });
```

r[type.closure.capture]
## 捕获模式

r[type.closure.capture.intro]
*捕获模式* 决定环境中的[位置表达式][place expression]如何被借用或移动到闭包中。捕获模式有：

1. 不可变借用（`ImmBorrow`）—— 位置表达式被捕获为[共享引用][shared reference]。
2. 唯一不可变借用（`UniqueImmBorrow`）—— 这类似于不可变借用，但必须如下文[所述](#unique-immutable-borrows-in-captures)那样是唯一的。
3. 可变借用（`MutBorrow`）—— 位置表达式被捕获为[可变引用][mutable reference]。
4. 移动（`ByValue`）—— 位置表达式通过[移动该值][moving the value]被捕获到闭包中。

r[type.closure.capture.precedence]
环境中的位置表达式从与该被捕获值在闭包体内使用方式兼容的第一种模式被捕获。该模式不受闭包周围代码的影响，例如所涉及变量或字段的生命周期，或闭包自身的生命周期。

[moving the value]: ../expressions.md#moved-and-copied-types
[mutable reference]: pointer.md#mutable-references-mut
[place expression]: ../expressions.md#place-expressions-and-value-expressions
[shared reference]: pointer.md#references--and-mut

r[type.closure.capture.copy]
### `Copy` 值

实现了 [`Copy`] 且被移动到闭包中的值以 `ImmBorrow` 模式捕获。

```rust
let x = [0; 1024];
let c = || {
    let y = x; // x 以 ImmBorrow 捕获
};
```

r[type.closure.async.input]
### Async 输入捕获

Async 闭包总是捕获所有输入参数，无论它们是否在函数体内被使用。

## 捕获精度

r[type.closure.capture.precision.capture-path]
*捕获路径* 是以环境中的一个变量开始、后跟零个或多个来自该变量的位置投影的序列。

r[type.closure.capture.precision.place-projection]
*位置投影* 是应用于变量的[字段访问][field access]、[元组索引][tuple index]、[解引用][dereference]（以及自动解引用）、[数组或切片索引][array or slice index]表达式，或[模式解构][pattern destructuring]。

> **注意**
> 在 `rustc` 中，模式解构脱糖为一系列解引用以及字段或元素访问。

r[type.closure.capture.precision.intro]
闭包借用或移动捕获路径，该路径可能根据下述规则被截断。

例如：

```rust
struct SomeStruct {
    f1: (i32, i32),
}
let s = SomeStruct { f1: (1, 2) };

let c = || {
    let x = s.f1.1; // s.f1.1 以 ImmBorrow 捕获
};
c();
```

此处捕获路径是局部变量 `s`，后跟字段访问 `.f1`，然后是元组索引 `.1`。此闭包捕获对 `s.f1.1` 的不可变借用。

[field access]: ../expressions/field-expr.md
[pattern destructuring]: patterns.destructure
[tuple index]: ../expressions/tuple-expr.md#tuple-indexing-expressions
[dereference]: ../expressions/operator-expr.md#the-dereference-operator
[array or slice index]: ../expressions/array-expr.md#array-and-slice-indexing-expressions

r[type.closure.capture.precision.shared-prefix]
### 共享前缀

当捕获路径以及该路径的某个祖先都被闭包捕获时，祖先路径以两种捕获中最高的捕获模式捕获，`CaptureMode = max(AncestorCaptureMode, DescendantCaptureMode)`，使用严格弱序：

`ImmBorrow < UniqueImmBorrow < MutBorrow < ByValue`

注意这可能需要递归应用。

```rust
// 在此例中，有三条不同的捕获路径共享一个祖先：
## fn move_value<T>(_: T){}
let s = String::from("S");
let t = (s, String::from("T"));
let mut u = (t, String::from("U"));

let c = || {
    println!("{:?}", u); // u 以 ImmBorrow 捕获
    u.1.truncate(0); // u.1 以 MutBorrow 捕获
    move_value(u.0.0); // u.0.0 以 ByValue 捕获
};
c();
```

总体而言，此闭包将以 `ByValue` 捕获 `u`。

r[type.closure.capture.precision.dereference-shared]
### 最右侧共享引用截断

若捕获路径中的解引用应用于共享引用，则捕获路径在该路径中最右侧的解引用处被截断。

允许这种截断是因为通过共享引用读取的字段将始终通过共享引用或副本读取。这有助于在额外精度从借用检查角度看并无收益时减小捕获的大小。

之所以是 *最右侧* 的解引用，是为了帮助避免不必要地更短的生命周期。考虑下面的例子：

```rust
struct Int(i32);
struct B<'a>(&'a i32);

struct MyStruct<'a> {
   a: &'static Int,
   b: B<'a>,
}

fn foo<'a, 'b>(m: &'a MyStruct<'b>) -> impl FnMut() + 'static {
    let c = || drop(&m.a.0);
    c
}
```

若这捕获 `m`，则闭包将不再长于 `'static`，因为 `m` 受 `'a` 约束。相反，它以 `ImmBorrow` 捕获 `(*(*m).a)`。

r[type.closure.capture.precision.wildcard]
### 通配符模式绑定

r[type.closure.capture.precision.wildcard.reads]
闭包只捕获需要被读取的数据。用[通配符模式][wildcard pattern]绑定值不会读取该值，因此该位置不被捕获。

```rust
struct S; // 一个非 `Copy` 类型。
let x = S;
let c = || {
    let _ = x;  // 不捕获 `x`。
};
let c = || match x {
    _ => (), // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.wildcard.destructuring]
解构元组、结构体和单变体枚举本身不会导致读取或捕获该位置。

> **注意**
> 标有 [`#[non_exhaustive]`][attributes.type-system.non_exhaustive] 的枚举始终被视为具有多个变体。参见 *[type.closure.capture.precision.discriminants.non_exhaustive]*。

```rust
struct S; // 一个非 `Copy` 类型。

// 解构元组不会导致读取或捕获。
let x = (S,);
let c = || {
    let (..) = x; // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();

// 解构单元结构体不会导致读取或捕获。
let x = S;
let c = || {
    let S = x; // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();

// 解构结构体不会导致读取或捕获。
struct W<T>(T);
let x = W(S);
let c = || {
    let W(..) = x; // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();

// 解构单变体枚举不会导致读取
// 或捕获。
enum E<T> { V(T) }
let x = E::V(S);
let c = || {
    let E::V(..) = x; // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.wildcard.fields]
与 [RestPattern]（`..`）或 [StructPatternEtCetera]（也是 `..`）匹配的字段不被读取，这些字段也不被捕获。

```rust
struct S; // 一个非 `Copy` 类型。
let x = (S, S);
let c = || {
    let (x0, ..) = x;  // 以 `ByValue` 捕获 `x.0`。
};
// 闭包只捕获了第一个元组字段。
x.1; // 正确：`x.1` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.wildcard.array-slice]
不支持对数组和切片的部分捕获；即使与通配符模式匹配、索引或子切片一起使用，也总是捕获整个切片或数组。

```rust
struct S; // 一个非 `Copy` 类型。
let mut x = [S, S];
let c = || {
    let [x0, _] = x; // 以 `ByValue` 捕获全部 `x`。
};
let _ = &mut x[1]; // 错误：对已移动值的借用。
```

r[type.closure.capture.precision.wildcard.initialized]
用通配符匹配的值仍然必须已初始化。

```rust
let x: u8;
let c = || {
    let _ = x; // 错误：绑定 `x` 未初始化。
};
```

[wildcard pattern]: ../patterns.md#wildcard-pattern

r[type.closure.capture.precision.discriminants]
### 为读取判别式而捕获

r[type.closure.capture.precision.discriminants.reads]
若模式匹配读取判别式，则包含该判别式的位置以 `ImmBorrow` 捕获。

r[type.closure.capture.precision.discriminants.multiple-variant]
匹配具有多于一个变体的枚举的某个变体会读取判别式，以 `ImmBorrow` 捕获该位置。

```rust
struct S; // 一个非 `Copy` 类型。
let mut x = (Some(S), S);
let c = || match x {
    (None, _) => (),
//   ^^^^
// 此模式需要读取判别式，这
// 导致 `x.0` 以 `ImmBorrow` 捕获。
    _ => (),
};
let _ = &mut x.0; // 错误：不能将 `x.0` 可变地借用。
//           ^^^
// 闭包仍然存活，因此 `x.0` 在此处
// 仍然被不可变地借用。
c();
```

```rust
## struct S; // 一个非 `Copy` 类型。
## let x = (Some(S), S);
let c = || match x { // 以 `ImmBorrow` 捕获 `x.0`。
    (None, _) => (),
    _ => (),
};
// 尽管因读取判别式而捕获了 `x.0`，
// `x.1` 并未被捕获。
x.1; // 正确：`x.1` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.discriminants.single-variant]
匹配单变体枚举的唯一变体不会读取判别式，也不会捕获该位置。

```rust
enum E<T> { V(T) } // 一个单变体枚举。
let x = E::V(());
let c = || {
    let E::V(_) = x; // 不捕获 `x`。
};
x; // 正确：`x` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.discriminants.non_exhaustive]
若对枚举应用了 [`#[non_exhaustive]`][attributes.type-system.non_exhaustive]，则就决定是否发生读取而言，该枚举被视为具有多个变体，即使它实际上只有一个变体。

r[type.closure.capture.precision.discriminants.uninhabited-variants]
即使除正在匹配的变体之外的所有变体都无居住值，使该模式[不可反驳][patterns.refutable]，只要在其他情况下会读取判别式，就仍然会读取。

```rust
enum Empty {}
let mut x = Ok::<_, Empty>(42);
let c = || {
    let Ok(_) = x; // 以 `ImmBorrow` 捕获 `x`。
};
let _ = &mut x; // 错误：不能将 `x` 可变地借用。
c();
```


r[type.closure.capture.precision.range-patterns]
### 捕获与范围模式

r[type.closure.capture.precision.range-patterns.reads]
匹配[范围模式][patterns.range]会读取被匹配的位置，即使该范围包含该类型的所有可能值，并以 `ImmBorrow` 捕获该位置。

```rust
let mut x = 0u8;
let c = || {
    let 0..=u8::MAX = x; // 以 `ImmBorrow` 捕获 `x`。
};
let _ = &mut x; // 错误：不能将 `x` 可变地借用。
c();
```

r[type.closure.capture.precision.slice-patterns]
### 捕获与切片模式

r[type.closure.capture.precision.slice-patterns.slices]
将切片与[切片模式][patterns.slice]匹配（除了只有单个[剩余模式][patterns.rest]的模式，即 `[..]`）被视为从切片读取长度，并以 `ImmBorrow` 捕获该切片。

```rust
let x: &mut [u8] = &mut [];
let c = || match x { // 以 `ImmBorrow` 捕获 `*x`。
    &mut [] => (),
//       ^^
// 这匹配恰好零个元素的切片。要知道
// 被匹配者是否匹配，必须读取长度，导致
// 该切片被捕获。
    _ => (),
};
let _ = &mut *x; // 错误：不能将 `*x` 可变地借用。
c();
```

```rust
let x: &mut [u8] = &mut [];
let c = || match x { // 不捕获 `*x`。
    [..] => (),
//   ^^ 剩余模式。
};
let _ = &mut *x; // 正确
c();
```

> **注意**
> 或许令人惊讶的是，尽管长度包含在指向切片的（宽）*指针* 中，被视为被读取并被捕获的是 *被指对象*（切片）的位置。
>
> ```rust
> fn f<'l: 's, 's>(x: &'s mut &'l [u8]) -> impl Fn() + 'l {
>     // 闭包长于 `'l`，因为它捕获 `**x`。若
>     // 它捕获的是 `*x`，它将活得不够长，
>     // 无法满足 `impl Fn() + 'l` 约束。
>     || match *x { // 以 `ImmBorrow` 捕获 `**x`。
>         &[] => (),
>         _ => (),
>     }
> }
> ```
>
> 这样，该行为与在被匹配者中解引用到切片是一致的。
>
> ```rust
> fn f<'l: 's, 's>(x: &'s mut &'l [u8]) -> impl Fn() + 'l {
>     || match **x { // 以 `ImmBorrow` 捕获 `**x`。
>         [] => (),
>         _ => (),
>     }
> }
> ```
>
> 细节参见 [Rust PR #138961](https://github.com/rust-lang/rust/pull/138961)。

r[type.closure.capture.precision.slice-patterns.arrays]
由于数组的长度由其类型固定，将数组与切片模式匹配本身不会捕获该位置。

```rust
let x: [u8; 1] = [0];
let c = || match x { // 不捕获 `x`。
    [_] => (), // 长度是固定的。
};
x; // 正确：`x` 可以在此处被移动。
c();
```

r[type.closure.capture.precision.move-dereference]
### 在 move 上下文中捕获引用

因为不允许从引用中移出字段，`move` 闭包只会捕获捕获路径中直到但不包括第一次解引用引用的前缀。引用本身将被移动到闭包中。

```rust
struct T(String, String);

let mut t = T(String::from("foo"), String::from("bar"));
let t_mut_ref = &mut t;
let mut c = move || {
    t_mut_ref.0.push_str("123"); // 以 ByValue 捕获 `t_mut_ref`
};
c();
```

r[type.closure.capture.precision.raw-pointer-dereference]
### 裸指针解引用

因为解引用裸指针是 `unsafe` 的，闭包只会捕获捕获路径中直到但不包括第一次解引用裸指针的前缀。

```rust
struct T(String, String);

let t = T(String::from("foo"), String::from("bar"));
let t_ptr = &t as *const T;

let c = || unsafe {
    println!("{}", (*t_ptr).0); // 以 ImmBorrow 捕获 `t_ptr`
};
c();
```

r[type.closure.capture.precision.union]
### 联合体字段

因为访问联合体字段是 `unsafe` 的，闭包只会捕获捕获路径中直到联合体本身的前缀。

```rust
union U {
    a: (i32, i32),
    b: bool,
}
let u = U { a: (123, 456) };

let c = || {
    let x = unsafe { u.a.0 }; // 以 ByValue 捕获 `u`
};
c();

// 这也包括对字段的写入。
let mut u = U { a: (123, 456) };

let mut c = || {
    u.b = true; // 以 MutBorrow 捕获 `u`
};
c();
```

r[type.closure.capture.precision.unaligned]
### 指向未对齐 `struct` 的引用

因为创建指向结构体中未对齐字段的引用是[未定义行为][undefined behavior]，闭包只会捕获捕获路径中直到但不包括第一次进入使用[`packed` 表示][the `packed` representation]的结构体的字段访问的前缀。这包括所有字段，即使是对齐的字段，以防止将来结构体中任何字段发生变化时的兼容性问题。

```rust
#[repr(packed)]
struct T(i32, i32);

let t = T(2, 5);
let c = || {
    let a = t.0; // 以 ImmBorrow 捕获 `t`
};
// 从 `t` 复制出来是可以的。
let (a, b) = (t.0, t.1);
c();
```

类似地，取未对齐字段的地址也会捕获整个结构体：

```rust
#[repr(packed)]
struct T(String, String);

let mut t = T(String::new(), String::new());
let c = || {
    let a = std::ptr::addr_of!(t.1); // 以 ImmBorrow 捕获 `t`
};
let a = t.0; // 错误：不能从 `t.0` 移出，因为它已被借用
c();
```

但若它不是 packed 的，上面的代码可以工作，因为它精确捕获该字段：

```rust
struct T(String, String);

let mut t = T(String::new(), String::new());
let c = || {
    let a = std::ptr::addr_of!(t.1); // 以 ImmBorrow 捕获 `t.1`
};
// 此处的移动是允许的。
let a = t.0;
c();
```

[undefined behavior]: ../behavior-considered-undefined.md
[the `packed` representation]: ../type-layout.md#the-alignment-modifiers

r[type.closure.capture.precision.box-deref]
### `Box` 与其他 `Deref` 实现

[`Box`] 的 [`Deref`] trait 实现与其他 `Deref` 实现的处理方式不同，因为它被视为特殊实体。

例如，让我们看看涉及 `Rc` 和 `Box` 的例子。`*rc` 脱糖为对 `Rc` 上定义的 trait 方法 `deref` 的调用，但由于 `*box` 被区别对待，可以精确捕获 `Box` 的内容。

[`Box`]: ../special-types-and-traits.md#boxt
[`Deref`]: ../special-types-and-traits.md#deref-and-derefmut

r[type.closure.capture.precision.box-non-move.not-moved]
#### 非 `move` 闭包中的 `Box`

在非 `move` 闭包中，若 `Box` 的内容未被移动到闭包体中，则精确捕获 `Box` 的内容。

```rust
struct S(String);

let b = Box::new(S(String::new()));
let c_box = || {
    let x = &(*b).0; // 以 ImmBorrow 捕获 `(*b).0`
};
c_box();

// 将 `Box` 与另一种实现 Deref 的类型对比：
let r = std::rc::Rc::new(S(String::new()));
let c_rc = || {
    let x = &(*r).0; // 以 ImmBorrow 捕获 `r`
};
c_rc();
```

r[type.closure.capture.precision.box-non-move.moved]
然而，若 `Box` 的内容被移动到闭包中，则整个 box 被捕获。这样做是为了最小化需要移动到闭包中的数据量。

```rust
// 这与上面的例子相同，只是闭包
// 移动该值而不是取其引用。

struct S(String);

let b = Box::new(S(String::new()));
let c_box = || {
    let x = (*b).0; // 以 ByValue 捕获 `b`
};
c_box();
```

r[type.closure.capture.precision.box-move.read]
#### `move` 闭包中的 `Box`

与在非 `move` 闭包中移动 `Box` 的内容类似，在 `move` 闭包中读取 `Box` 的内容将捕获整个 `Box`。

```rust
struct S(i32);

let b = Box::new(S(10));
let c_box = move || {
    let x = (*b).0; // 以 ByValue 捕获 `b`
};
```

r[type.closure.unique-immutable]
## 捕获中的唯一不可变借用

捕获可以通过一种称为 _唯一不可变借用_ 的特殊借用发生，它不能在语言的其他任何地方使用，也无法显式写出。它发生在修改可变引用的所指对象时，如下面的例子：

```rust
let mut b = false;
let x = &mut b;
let mut c = || {
    // 对 `x` 的 ImmBorrow 和 MutBorrow。
    let a = &x;
    *x = true; // `x` 以 UniqueImmBorrow 捕获
};
// 下面这一行是错误：
// let y = &x;
c();
// 然而，下面是正确的。
let z = &x;
```

在这种情况下，可变地借用 `x` 是不可能的，因为 `x` 不是 `mut` 的。但与此同时，不可变地借用 `x` 会使赋值非法，因为 `& &mut` 引用可能不是唯一的，因此不能安全地用于修改值。于是使用唯一不可变借用：它不可变地借用 `x`，但像可变借用一样，它必须是唯一的。

在上面的例子中，取消注释 `y` 的声明会产生错误，因为它会违反闭包对 `x` 借用的唯一性；`z` 的声明是合法的，因为闭包的生命周期在块结束时已到期，释放了该借用。

r[type.closure.call]
## 调用 trait 与强制转换

r[type.closure.call.intro]
所有闭包类型都实现 [`FnOnce`]，表明它们可以通过消耗闭包的所有权被调用一次。此外，一些闭包实现更具体的调用 trait：

r[type.closure.call.fn-mut]
* 不从任何被捕获变量中移出的闭包实现 [`FnMut`]，表明它可以通过可变引用被调用。

r[type.closure.call.fn]
* 不修改或从任何被捕获变量中移出的闭包实现 [`Fn`]，表明它可以通过共享引用被调用。

> **注意**
> `move` 闭包仍然可能实现 [`Fn`] 或 [`FnMut`]，即使它们按移动捕获变量。这是因为闭包类型所实现的 trait 由闭包对被捕获值做了什么决定，而不是由它如何捕获它们决定。

r[type.closure.non-capturing]
*不捕获的闭包* 是不从其环境中捕获任何东西的闭包。非 async、不捕获的闭包可以被强制转换为具有匹配签名的函数指针（例如 `fn()`）。

```rust
let add = |x, y| x + y;

let mut x = add(5,7);

type Binop = fn(i32, i32) -> i32;
let bo: Binop = add;
x = bo(5,7);
```

r[type.closure.async.traits]
### Async 闭包 trait

r[type.closure.async.traits.fn-family]
Async 闭包在是否实现 [`FnMut`] 或 [`Fn`] 上有进一步的限制。

Async 闭包返回的 [`Future`] 具有与闭包类似的捕获特征。它根据位置表达式的使用方式从 async 闭包中捕获它们。若 async 闭包具有以下性质之一，则称它对其 [`Future`] *出借*：

- 该 `Future` 包含可变捕获。
- 该 async 闭包按值捕获，除非该值通过解引用投影访问。

若 async 闭包对其 `Future` 出借，则 *不* 实现 [`FnMut`] 和 [`Fn`]。始终实现 [`FnOnce`]。

> **示例**：关于可变捕获的第一条可以用下面说明：
>
> ```rust
> fn takes_callback<Fut: Future>(c: impl FnMut() -> Fut) {}
>
> fn f() {
>     let mut x = 1i32;
>     let c = async || {
>         x = 2;  // x 以 MutBorrow 捕获
>     };
>     takes_callback(c);  // 错误：async 闭包未实现 `FnMut`
> }
> ```
>
> 关于常规值捕获的第二条可以用下面说明：
>
> ```rust
> fn takes_callback<Fut: Future>(c: impl Fn() -> Fut) {}
>
> fn f() {
>     let x = &1i32;
>     let c = async move || {
>         let a = x + 2;  // x 以 ByValue 捕获
>     };
>     takes_callback(c);  // 错误：async 闭包未实现 `Fn`
> }
> ```
>
> 第二条的例外可以通过使用解引用来说明，这确实允许实现 `Fn` 和 `FnMut`：
>
> ```rust
> fn takes_callback<Fut: Future>(c: impl Fn() -> Fut) {}
>
> fn f() {
>     let x = &1i32;
>     let c = async move || {
>         let a = *x + 2;
>     };
>     takes_callback(c);  // 正确：实现 `Fn`
> }
> ```

r[type.closure.async.traits.async-family]
Async 闭包以实现 [`Fn`]、[`FnMut`] 和 [`FnOnce`] 的类似方式实现 [`AsyncFn`]、[`AsyncFnMut`] 和 [`AsyncFnOnce`]；也就是说，取决于其函数体中对被捕获变量的使用。

r[type.closure.traits]
### 其他 trait

r[type.closure.traits.intro]
所有闭包类型都实现 [`Sized`]。此外，若其所存储捕获的类型允许，闭包类型还实现以下 trait：

* [`Clone`]
* [`Copy`]
* [`Sync`]
* [`Send`]

r[type.closure.traits.behavior]
[`Send`] 和 [`Sync`] 的规则与普通结构体类型匹配，而 [`Clone`] 和 [`Copy`] 的行为如同[派生][derived]。对于 [`Clone`]，被捕获值的克隆顺序未指定。

由于捕获常常通过引用进行，产生以下一般规则：

* 若所有被捕获值都是 [`Sync`] 的，则闭包是 [`Sync`] 的。
* 若所有通过非唯一不可变引用捕获的值都是 [`Sync`] 的，并且所有通过唯一不可变或可变引用、复制或移动捕获的值都是 [`Send`] 的，则闭包是 [`Send`] 的。
* 若闭包不以唯一不可变或可变引用捕获任何值，并且它通过复制或移动捕获的所有值分别是 [`Clone`] 或 [`Copy`] 的，则闭包是 [`Clone`] 或 [`Copy`] 的。

[`Clone`]: ../special-types-and-traits.md#clone
[`Copy`]: ../special-types-and-traits.md#copy
[`Send`]: ../special-types-and-traits.md#send
[`Sized`]: ../special-types-and-traits.md#sized
[`Sync`]: ../special-types-and-traits.md#sync
[closure expression]: ../expressions/closure-expr.md
[derived]: ../attributes/derive.md

r[type.closure.drop-order]
## Drop 顺序

若闭包按值捕获复合类型（如结构体、元组和枚举）的某个字段，则该字段的生命周期现在将与闭包绑定。因此，复合类型的不相交字段有可能在不同时间被 drop。

```rust
{
    let tuple =
      (String::from("foo"), String::from("bar")); // --+
    { //                                               |
        let c = || { // ----------------------------+  |
            // tuple.0 被捕获到闭包中              |  |
            drop(tuple.0); //                       |  |
        }; //                                       |  |
    } // 'c' 和 'tuple.0' 在此处 drop ------------+  |
} // tuple.1 在此处 drop -----------------------------+
```

r[type.closure.capture.precision.edition2018.entirety]
## 2018 edition 及之前

### 闭包类型的差异

在 2018 edition 及之前，闭包总是捕获整个变量，而不使用其精确捕获路径。这意味着对于[闭包类型](#closure-types)一节中使用的例子，生成的闭包类型会看起来大致如下：

<!-- ignore: simplified -->
```rust
struct Closure<'a> {
    rect : &'a mut Rectangle,
}

impl<'a> FnOnce<()> for Closure<'a> {
    type Output = String;
    extern "rust-call" fn call_once(self, args: ()) -> String {
        self.rect.left_top.x += 1;
        self.rect.right_bottom.x += 1;
        format!("{:?}", self.rect.left_top)
    }
}
```

而对 `f` 的调用会如下工作：

<!-- ignore: continuation of above -->
```rust
f(Closure { rect: rect });
```

r[type.closure.capture.precision.edition2018.composite]
### 捕获精度的差异

复合类型如结构体、元组和枚举总是被整体捕获，而不是按各个字段。因此，为了捕获单个字段，可能有必要先借用到局部变量：

```rust
## use std::collections::HashSet;
#
struct SetVec {
    set: HashSet<u32>,
    vec: Vec<u32>
}

impl SetVec {
    fn populate(&mut self) {
        let vec = &mut self.vec;
        self.set.iter().for_each(|&n| {
            vec.push(n);
        })
    }
}
```

若闭包改为直接使用 `self.vec`，则它会试图以可变引用捕获 `self`。但由于 `self.set` 已经被借用来迭代，代码将无法编译。

r[type.closure.capture.precision.edition2018.move]
若使用了 `move` 关键字，则所有捕获都是按移动，或者对于 `Copy` 类型按复制，无论借用是否可行。`move` 关键字通常用于允许闭包长于被捕获的值，例如当闭包被返回或用于生成新线程时。

r[type.closure.capture.precision.edition2018.wildcard]
无论数据是否会被闭包读取，即在通配符模式的情况下，若在闭包中提及在闭包外定义的变量，该变量就会被整体捕获。

r[type.closure.capture.precision.edition2018.drop-order]
### Drop 顺序的差异

由于复合类型被整体捕获，按值捕获其中一种复合类型的闭包会在闭包被 drop 的同时 drop 整个被捕获变量。

```rust
{
    let tuple =
      (String::from("foo"), String::from("bar"));
    {
        let c = || { // --------------------------+
            // tuple 被捕获到闭包中               |
            drop(tuple.0); //                     |
        }; //                                     |
    } // 'c' 和 'tuple' 在此处 drop ------------+
}
```
