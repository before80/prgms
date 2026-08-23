+++
title = "17-Pin"
date = 2026-08-22T19:00:00+08:00
weight = 20
type = "docs"
description = "Pin"
isCJKLanguage = true
draft = false

+++

> 译文 · 基于 [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)

# Pin {#pinning}


> 原文链接: [https://rust-lang.github.io/async-book/part-reference/pinning.html](https://rust-lang.github.io/async-book/part-reference/pinning.html)


Pin 是一个出了名的难以掌握的概念，具有一些微妙且令人困惑的性质。本节将深入探讨该主题（可以说过于深入）。Pin 是 Rust 中 async 编程实现的关键[^design]，但完全有可能在从未遇到 Pin 的情况下走得很远，当然更不必对其有深入理解。

第一节将给出 Pin 的摘要，希望对大多数 async 程序员来说已足够。本章其余部分面向实现者、其他做高级或底层 async 编程的人，以及好奇的读者。

摘要之后，本章会先介绍移动语义的一些背景，再进入 Pin。我们将涵盖一般思想，然后是 `Pin` 和 `Unpin` 类型、Pin 如何实现其目标，以及若干在实践中使用 Pin 的主题。随后有关于 Pin 与 async 编程的章节，以及 Pin 的一些替代与扩展（给真正好奇的读者）。章节末尾有一些替代解释与参考资料的链接。

[^design]: 值得指出的是，Pin 是专门为实现 async Rust 而设计的底层构建块。虽然它并非直接与 async Rust 绑定，也可用于其他目的，但它并非设计为通用机制，尤其不是开箱即用的自引用字段解决方案。将 Pin 用于 async 代码以外的任何用途，通常只有在包裹在厚厚抽象层中时才可行，因为那会需要大量繁琐且难以推理的 unsafe 代码。


## TL;DR

`Pin` 将指针标记为指向一个在 drop 之前不会移动的对象。Pin 并非内建于语言或编译器；它通过简单地限制对 pointee 的可变引用的访问来工作。在 unsafe 代码中打破 Pin 相当容易，但就像 unsafe 代码中的所有安全保证一样，不这样做是程序员的责任。

通过保证对象不会移动，Pin 使得从一个结构体字段到另一字段的引用是安全的（有时称为自引用）。async 函数的实现需要这一点（async 函数被实现为数据结构，其中变量存储为字段，由于变量可能相互引用，实现 async 函数的 future 的字段必须能够相互引用）。大多数情况下，程序员不必意识到这一细节，但在直接处理 future 时，你可能需要了解，因为 `Future::poll` 的签名要求 `self` 被固定。

如果你通过引用使用 future，你可能需要用 `pin!(...)` 固定引用，以确保该引用仍实现 `Future` trait（这常与 `select` 宏一起出现）。同样，如果你想手动对 future 调用 `poll`（通常是因为你在实现另一个 future），你需要对它的固定引用（使用 `pin!` 或确保参数具有固定类型）。如果你在实现 future，或出于其他原因已有固定引用，并希望对对象内部进行可变访问，你需要理解下面关于固定字段的章节，以知道如何操作以及何时安全。


## 移动语义

讨论 Pin 及相关主题时，*位置*（place）的概念很有用。位置是一块内存（有地址），值可以存在于其中。引用并不真正指向值，而是指向位置。这就是为什么 `*ref = ...` 说得通：解引用得到的是位置，而不是值的副本。位置对语言实现者很熟悉，但在编程语言中通常是隐式的（在 Rust 中也是隐式的）。程序员通常对位置有良好的直觉，但可能不会显式地以「位置」来思考。

除了引用，变量和字段访问也求值为位置。事实上，任何可以出现在赋值左侧的东西在运行时都必须是位置（这就是为什么在编译器术语中位置被称为「左值」lvalue）。

在 Rust 中，可变性是位置的属性，因借用而被「冻结」也是（我们可以说该位置被借用了）。

Rust 中的赋值会*移动*数据（大多数情况下；一些简单数据有复制语义，但这不太重要）。当我们写 `let b = a;` 时，在由 `a` 标识的位置的内存中的数据被移动到由 `b` 标识的位置。这意味着赋值之后，数据存在于 `b` 处，而不再存在于 `a` 处。换句话说，赋值改变了对象的地址[^compiler]。

如果存在指向被移走的位置的指针，这些指针将无效，因为它们不再指向该对象。这就是为什么借用引用会阻止移动：`let r = &a; let b = a;` 是非法的，`r` 的存在阻止 `a` 被移动。

编译器只知道从对象外部进入对象的引用（例如上面的例子，或对对象某字段的引用）。完全在对象内部的引用对编译器是不可见的。想象如果我们被允许写类似这样的东西：

```rust,norun
struct Bad {
    field: u64,
    r: &'self u64,
}
```

我们可以有一个 `Bad` 的实例 `b`，其中 `b.r` 指向 `b.field`。在 `let a = b;` 中，指向 `b.field` 的内部引用 `b.r` 对编译器不可见，因此看起来没有对 `b` 的引用，移动到 `a` 似乎没问题。然而如果那样发生了，移动之后 `a.r` 将不会如我们所愿指向 `a.field`，而是指向 `b.field` 旧位置处的无效内存，违反 Rust 的安全保证。

移动数据不限于值。数据也可以从唯一引用中移出。解引用 `Box` 会将数据从堆移动到栈。`take`、`replace` 和 `swap`（均在 [`std::mem`](https://doc.rust-lang.org/std/mem/index.html) 中）从可变引用（`&mut T`）中移出数据。从 `Box` 移出会使被指向的位置无效。从可变引用移出会使位置仍然有效，但包含不同的数据。


[^compiler]: 我们在这里有点混淆了源代码和运行时。为绝对清楚：变量在运行时不存在。（编译后的）代码片段可能被执行多次（例如在循环中，或在被多次调用的函数中）。每次执行时，源代码中的变量在运行时将由不同的地址表示。

抽象地说，移动通过将位从源复制到目标然后擦除源位来实现。然而，编译器可以用多种方式优化这一点。


## Pin（固定）

重要说明：我将从讨论 Pin 的抽象概念开始，这与任何特定类型所表达的不完全相同。我们会随着进展使概念更具体，最终得到不同类型含义的精确定义，但这些类型中没有哪一个与我们开始的 Pin 概念完全相同。

对象被固定（pinned）是指它不会被移动或以其他方式失效。如我上文所述，这不是新概念——借用对象会在借用期间阻止对象被移动。对象能否移动在 Rust 类型中并非显式表达，尽管编译器知道（这就是为什么你会看到「cannot move out of」错误消息）。与借用（及借用导致的对移动的临时限制）相反，被固定是永久的。对象可以从未固定变为已固定，但一旦固定就必须保持固定直到被 drop[^inherent]。

正如指针类型反映 pointee 的所有权和可变性（例如 `Box` vs `&`，`&mut` vs `&`），我们也希望在指针类型中反映「固定性」。这不是指针的属性——指针本身不被固定或可移动——而是被指向位置的属性：pointee 能否从其位置移出。

粗略地说，`Pin<Box<T>>` 是指向拥有的、已固定对象的指针，`Pin<&mut T>` 是指向唯一借用的、可变的、已固定对象的指针（cf. `&mut T` 是指向唯一借用的、可变的、可能固定也可能未固定的对象的指针）。

Pin 概念直到 1.0 之后才加入 Rust，出于向后兼容的原因，无法显式表达*对象*是否被固定。我们只能表达引用指向的是已固定还是未固定的对象。

Pin 与可变性正交。对象可能是可变的且已固定（`Pin<&mut T>`）或未固定（`&mut T`）（即对象可被修改，且要么被固定在位要么可移动），或不可变且已固定（`Pin<&T>`）或未固定（`T`）（即对象不可修改，且要么不可移动要么可移动但不可修改）。注意 `&T` 不能被修改或移动，但并非被固定，因为其不可移动性只是暂时的。


[^inherent]: 永久性并非 Pin 的根本方面，它是 Rust 中 Pin 的框架及其周围安全保证的一部分。如果 Pin 可以是临时的且能安全表达，消费者能依赖 Pin 保证的时间范围，那么临时 Pin 也是可以的。然而，以当今 Rust 或任何合理扩展，这都不可能。


### `Unpin`

尽管移动与不移动是我们介绍 Pin 的方式，且名称在某种程度上暗示这一点，`Pin` 实际上并不能告诉你 pointee 是否真的会移动。

什么？唉。

Pin 实际上是一份关于有效性的契约，而非关于移动。它保证*如果对象是地址敏感的，那么*其地址不会改变（因此从其派生的地址，例如其字段的地址，也不会改变）。Rust 中大多数数据并非地址敏感。它可以四处移动而一切正常。`Pin` 保证 pointee 就其地址而言保持有效。如果 pointee 是地址敏感的，则它不能被移动；如果不是地址敏感的，则是否移动无关紧要。

`Unpin` 是一个表达对象是否地址敏感的 trait。如果对象实现 `Unpin`，则它*不*是地址敏感的。如果对象是 `!Unpin`，则它是地址敏感的。或者，如果我们将 Pin 视为将对象固定在其位置的行为，则 `Unpin` 意味着撤销该行为并允许对象移动是安全的。

`Unpin` 是自动 trait，大多数类型是 `Unpin`。只有具有 `!Unpin` 字段或显式选择退出的类型才不是 `Unpin`。你可以通过 [`PhantomPinned`](https://doc.rust-lang.org/std/marker/struct.PhantomPinned.html) 字段选择退出，或（若使用 nightly）通过 `impl !Unpin for ... {}`。

对于实现 `Unpin` 的类型，`Pin` 基本上什么都不做。`Pin<Box<T>>` 和 `Pin<&mut T>` 可以像 `Box<T>` 和 `&mut T` 一样使用。事实上，对于 `Unpin` 类型，固定的和普通指针可以用 `Pin::new` 和 `Pin::into_inner` 自由相互转换。值得重申：`Pin<...>` 并不保证 pointee 不会移动，只保证如果它是 `!Unpin` 则 pointee 不会移动。

上述内容的实际含义是：处理 `Unpin` 类型和 Pin 比处理非 `Unpin` 类型容易得多，事实上 `Pin` 标记对 `Unpin` 类型和指向 `Unpin` 类型的指针基本上没有效果，你基本上可以忽略所有 Pin 保证和要求。

`Unpin` 不应被理解为单独对象的属性；`Unpin` 改变的唯一内容是对象如何与 `Pin` 交互。在 Pin 上下文之外使用 `Unpin` 边界不会影响编译器行为或对对象能做什么。使用 `Unpin` 的唯一理由是与 Pin 结合，或将该边界传播到与 Pin 一起使用的地方。


### `Pin`

[`Pin`](https://doc.rust-lang.org/std/pin/struct.Pin.html) 是一个标记类型，对类型检查很重要，但会被编译掉且在运行时不存在（`Pin<Ptr>` 保证与 `Ptr` 具有相同的内存布局和 ABI）。它是指针（如 `Box`）的包装，因此行为像指针类型，但不增加一层间接，`Box<Foo>` 和 `Pin<Box<Foo>>` 在程序运行时是相同的。最好将 `Pin` 视为指针的修饰符，而非指针本身。

`Pin<Ptr>` 意味着 `Ptr` 的 pointee（而非 `Ptr` 本身）被固定。也就是说，`Pin` 保证 pointee（而非指针）在 pointee 被 drop 之前就其地址而言保持有效。如果 pointee 是地址敏感的（即 `!Unpin`），则 pointee 不会被移动。


### 固定值

对象创建时并非已固定。对象开始时未固定（可自由移动），当指向它的固定指针被创建时变为已固定。如果对象是 `Unpin`，用 `Pin::new` 这很简单；然而，如果对象不是 `Unpin`，固定它必须确保无法通过别名移动或使其失效。

要在堆上固定对象，可以用 [`Box::pin`](https://doc.rust-lang.org/std/boxed/struct.Box.html#method.pin) 创建新的固定 `Box`，或用 [`Box::into_pin`](https://doc.rust-lang.org/std/boxed/struct.Box.html#method.into_pin) 将现有 `Box` 转换为固定 `Box`。无论哪种情况，你都会得到 `Pin<Box<T>>`。其他一些指针（如 `Arc` 和 `Rc`）有类似机制。对于没有的指针，或你自己的指针类型，你需要用 [`Pin::new_unchecked`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.new_unchecked) 创建固定指针[^box-pin]。这是 unsafe 函数，因此程序员必须确保维护 `Pin` 的不变量。即 pointee 在任何情况下、在其析构函数被调用之前都将保持有效。确保这一点有一些微妙细节，请参阅该函数的[文档](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.new_unchecked)或下文 [Pin 如何工作](#how-pinning-works) 一节。

`Box::pin` 将对象固定到堆上的位置。要在栈上固定对象，可以使用 [`pin`](https://doc.rust-lang.org/std/pin/macro.pin.html) 宏创建并固定可变引用（`Pin<&mut T>`）[^not-stack]。

Tokio 也有 [`pin`](https://docs.rs/tokio/latest/tokio/macro.pin.html) 宏，与 std 宏做同样的事，并支持在宏内向变量赋值。futures-rs 和 pin-utils crate 有曾常用的 `pin_mut` 宏，现已弃用，推荐使用 std 宏。

你也可以用 `Pin::static_ref` 和 `Pin::static_mut` 固定静态引用。

[^box-pin]: `Box`（及其他 std 指针）在 Pin 实现或编译器中也没有特殊处理。`Box` 使用 `Pin` API 中的 unsafe 函数实现 `Box::pin`。由于 `Box` 的安全保证，`Pin` 的安全要求得到满足。

[^not-stack]: 这仅在非 async 函数中严格说是固定到栈上。在 async 函数中，所有局部变量分配在 async 伪栈上，因此被固定的位置很可能作为底层 async 函数的 future 的一部分存储在堆上。


### 使用固定类型

理论上，使用固定指针就像使用任何其他指针类型。然而，因为它不是最直观的抽象，且没有语言支持，使用固定指针往往相当不易用。使用 Pin 最常见的情况是与 future 和 stream 打交道，下文会更详细说明这些具体情况。

由于 `Pin` 对 `Deref` 的实现，将固定指针用作不可变借用引用是轻而易举的。你基本上可以把 `Pin<Ptr<T>>` 当作 `&T`，必要时使用显式 `deref()`。同样，用 `as_ref()` 得到 `Pin<&T>` 相当容易。

处理固定类型最常见的方式是使用 `Pin<&mut T>`（例如在 [`Future::poll`](https://doc.rust-lang.org/std/future/trait.Future.html#tymethod.poll) 中），然而产生固定对象最容易的方式是 `Box::pin`，它给出 `Pin<Box<T>>`。你可以用 [`Pin::as_mut`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.as_mut) 将后者转换为前者。然而，没有语言对重用引用的支持（隐式再借用），你必须不断调用 `as_mut` 而不是重用结果。例如（来自 `as_mut` 文档），

```rust,norun
impl Type {
    fn method(self: Pin<&mut Self>) {
        // 做某事
    }

    fn call_method_twice(mut self: Pin<&mut Self>) {
        // `method` 会消费 `self`，因此通过 `as_mut` 再借用 `Pin<&mut Self>`。
        self.as_mut().method();
        self.as_mut().method();
    }
}
```

如果你需要以其他方式访问被固定的 pointee，可以通过 [`Pin::into_inner_unchecked`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.into_inner_unchecked) 做到。然而这是 unsafe 的，你必须*非常*小心确保尊重 `Pin` 的安全要求。


### Pin 如何工作

`Pin` 是指针的简单包装结构体（即 newtype）。通过要求其泛型参数上的 `Deref` 边界才能做任何有用的事，它被强制只用于指针，但这只是为了表达意图，而非为了保持安全。与大多数 newtype 包装一样，`Pin` 的存在是为了在编译时表达不变量，而非任何运行时效果。事实上，在大多数情况下，`Pin` 和 Pin 机制在编译过程中会完全消失。

精确地说，`Pin` 表达的不变量是关于有效性的，而不仅仅是可移动性。这也是一种仅在指针被固定之后才适用的有效性不变量——在此之前 `Pin` 没有效果，对固定之前发生什么不做要求。一旦指针被固定，`Pin` 要求（并在安全代码中保证）被指向的对象在对象的析构函数被调用之前保持在内存中的同一地址有效。

对于不可变指针（例如借用引用），`Pin` 没有效果——由于 pointee 不能被修改或替换，没有使其失效的危险。

对于允许修改的指针（例如 `Box` 或 `&mut`），直接访问该指针或访问 pointee 的可变引用（`&mut`）可能允许修改或移动 pointee。`Pin` 简单地不提供任何（非 `unsafe`）方式获取对指针或可变引用的直接访问。指针向其 pointee 提供可变引用的通常方式是实现 [`DerefMut`](https://doc.rust-lang.org/std/ops/trait.DerefMut.html)，`Pin` 仅在 pointee 是 `Unpin` 时实现 `DerefMut`。

这一实现极其简单！总结：`Pin` 是围绕指针的包装结构体，仅提供对 pointee 的不可变访问（若 pointee 是 `Unpin` 则还提供可变访问）。其余都是细节（以及 unsafe 代码中的微妙不变量）。为方便起见，`Pin` 提供在 `Pin` 类型之间转换的设施（总是安全的，因为指针无法逃离 `Pin`）等。

`Pin` 还提供用于创建固定指针和访问底层数据的 unsafe 函数。与所有 `unsafe` 函数一样，维护安全不变量是程序员的责任，而非编译器。不幸的是，Pin 的安全不变量有些分散，在不同地方强制执行，难以用全局统一的方式描述。此处不详细描述，请参阅文档，但我会尝试总结（详见[模块文档](https://doc.rust-lang.org/std/pin/index.html)）：

- 创建新的固定指针 [`new_unchecked`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.new_unchecked)。程序员必须确保 pointee 被固定（即遵守 Pin 不变量）。这一要求可能仅由指针类型满足（例如 `Box` 的情况），或可能需要 pointee 类型参与（例如 `&mut` 的情况）。这包括（但不限于）：
  - 在 `Deref` 和 `DerefMut` 中不从 `self` 移出。
  - 正确实现 `Drop`，见 [drop 保证](https://doc.rust-lang.org/std/pin/index.html#subtle-details-and-the-drop-guarantee)。
  - 若需要 Pin 保证，则选择退出 `Unpin`（使用 [`PhantomPinned`](https://doc.rust-lang.org/std/marker/struct.PhantomPinned.html)）。
  - pointee 不能是 `#[repr(packed)]`。
- 访问固定值 [`into_inner_unchecked`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.into_inner_unchecked)、[`get_unchecked_mut`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.get_unchecked_mut)、[`map_unchecked`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.map_unchecked) 和 [`map_unchecked_mut`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.map_unchecked_mut)。从访问数据的时刻直到其析构函数运行，强制执行 Pin 保证（包括不移动数据）成为程序员的责任（注意这一责任范围超出 unsafe 调用，适用于底层数据发生的任何事）。
- 不提供任何其他从固定类型移出数据的方式（那需要 unsafe 实现）。


#### 固定指针类型

我们说过 `Pin` 包装指针类型。常见看到 `Pin<Box<T>>`、`Pin<&T>` 和 `Pin<&mut T>`。严格来说，固定指针类型的唯一要求是实现 `Deref`。然而，除了使用 unsafe 代码（通过 `new_unchecked`），没有其他方式为任何其他指针类型创建 `Pin<Ptr>`。这样做对指针类型有要求以确保 Pin 契约：

- 指针的 `Deref` 和 `DerefMut` 实现不得从其 pointee 移出。
- 在创建 `Pin` 之后的任何时候，都不可能获得 pointee 的 `&mut` 引用，即使在 `Pin` 被 drop 之后（这就是为什么不能安全地从 `&mut T` 构造 `Pin<&mut T>`）。这必须通过多步或引用保持为真（这阻止使用 `Rc` 或 `Arc`）。
- 指针的 `Drop` 实现不得移动（或以其他方式使无效）其 pointee。

更多细节见 `new_unchecked` [文档](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.new_unchecked)。

### Pin 与 `Drop`

Pin 契约适用于被固定对象被 drop 之前（技术上，指其 `drop` 方法返回时，而非被调用时）。这通常相当直接，因为对象销毁时 `drop` 会自动调用。如果你手动管理对象生命周期，可能需要额外思考。如果你有一个（或可能是）被固定的对象且该对象不是 `Unpin`，则必须在释放或重用对象内存或地址之前调用其 `drop` 方法（使用 [`drop_in_place`](https://doc.rust-lang.org/std/ptr/fn.drop_in_place.html)）。详情见 [std 文档](https://doc.rust-lang.org/std/pin/index.html#drop-guarantee)。

如果你在实现地址敏感类型（即 `!Unpin` 的类型），则必须格外注意 `Drop` 实现。尽管 `drop` 中的 self 类型是 `&mut Self`，你必须将 self 类型视为 `Pin<&mut Self>`。换句话说，你必须确保对象在 `drop` 函数返回之前保持有效。在源代码中使这一点显式的一种方式是遵循以下惯用法：

```rust,norun
impl Drop for Type {
    fn drop(&mut self) {
        // `new_unchecked` 是可以的，因为我们知道该值在 drop 之后不会再被使用。
        inner_drop(unsafe { Pin::new_unchecked(self)});

        fn inner_drop(this: Pin<&mut Self>) {
            // 实际的 drop 代码写在这里。
        }
    }
}
```

注意有效性要求将取决于被实现的类型。精确定义这些要求，尤其关于对象销毁，是推荐的，尤其当可能涉及多个对象时（例如侵入式链表）。确保这里的正确性可能会很有趣！

### 方法中的固定 self

在固定类型上调用方法会引出对这些方法中 self 类型的思考。如果方法不需要修改 `self`，你仍可使用 `&self`，因为 `Pin<...>` 可以解引用为借用引用。然而，如果你需要修改 `self`（且你的类型不是 `Unpin`），你需要在 `&mut self` 和 `self: Pin<&mut Self>` 之间选择（尽管固定指针不能隐式强制为后者，但可以用 `Pin::as_mut` 轻松转换）。

使用 `&mut self` 使实现容易，但意味着该方法不能在已固定对象上调用。使用 `self: Pin<&mut Self>` 意味着要考虑 pin projection（见下一节），且只能在已固定对象上调用。虽然这一切有点令人困惑，但当你记住 Pin 是分阶段的概念时直觉上说得通——对象开始时未固定，在某个时刻经历阶段变化变为已固定。`&mut self` 方法是在第一阶段（未固定）可调用的，`self: Pin<&mut Self>` 方法是在第二阶段（已固定）可调用的。

注意 `drop` 接受 `&mut self`（尽管它可能在任一阶段被调用）。这是由于语言的限制和向后兼容的愿望。它在编译器中需要特殊处理，并带有安全要求。


### 固定字段、结构固定与 pin projection

给定对象被固定，这对它的字段的「固定性」告诉我们什么？答案取决于数据类型实现者的选择，没有普适答案（事实上同一对象的不同字段可以不同）。

如果对象的固定性传播到字段，我们说该字段体现「结构固定」（structural pinning），或说 Pin 随该字段被投影。此时应有投影方法 `fn get_field(self: Pin<&mut Self>) -> Pin<&mut Field>`。如果字段不是结构固定的，则投影方法签名应为 `fn get_field(self: Pin<&mut Self>) -> &mut Field`。实现任一方法（或实现类似代码）需要 `unsafe` 代码，任一选择都有安全含义。Pin 传播必须一致，字段必须始终是结构固定的或始终不是，字段在某些时候结构固定、某些时候不是几乎总是不健全的。

如果字段是聚合数据类型的地址敏感部分，Pin 应投影到该字段。也就是说，如果被固定的聚合依赖于该字段被固定，则 Pin 必须投影到该字段。例如，如果聚合的另一部分有指向该字段的引用，或字段内部有自引用，则 Pin 必须投影到该字段。另一方面，对于泛型集合，Pin 不需要投影到其内容，因为集合不依赖它们的行为（这是因为集合不能依赖其所含泛型项的实现，因此集合本身不能依赖其项的地址）。

编写 unsafe 代码时，你只能假定 Pin 保证适用于结构上被固定的字段。另一方面，你可以安全地将非结构固定字段视为可移动的，不必担心它们的 Pin 要求。特别地，即使某字段不是 `Unpin`，只要该字段始终被视为非结构固定，结构体仍可以是 `Unpin`。

如果字段是结构固定的，则聚合结构体上的 Pin 要求延伸到该字段。在任何情况下，在聚合被固定时都不能移动字段内容（这总是需要 unsafe 代码）。结构固定字段必须在被移动（包括释放）之前被 drop，即使在 panic 的情况下也是如此，这意味着在聚合的 `Drop` 实现中必须小心。此外，除非所有结构固定字段都是 `Unpin`，否则聚合结构体不能是 `Unpin`。


#### 用于 pin projection 的宏

有宏可帮助 pin projection。

[pin-project](https://docs.rs/pin-project/latest/pin_project/) crate 提供 `#[pin_project]` 属性宏（以及 `#[pin]` 辅助属性），通过为标注类型创建可通过该类型上 `project` 方法访问的固定版本来为你实现安全的 pin projection。

[Pin-project-lite](https://docs.rs/pin-project-lite/latest/pin_project_lite/) 是使用声明式宏（`pin_project!`）的替代，工作方式与 pin-project 非常相似。Pin-project-lite 是轻量级的，因为它不是过程宏，因此不会向项目添加实现过程宏的依赖。然而，它不如 pin-project 表达力强，也不提供自定义错误消息。若想避免添加过程宏依赖，推荐 pin-project-lite；否则推荐 pin-project。

Pin-utils 提供 [`unsafe_pinned`](https://docs.rs/pin-utils/latest/pin_utils/macro.unsafe_pinned.html) 宏帮助实现 pin projection，但整个 crate 已弃用，推荐使用上述 crate 及 std 中的功能。


### 赋值给固定指针

[向固定指针赋值](https://doc.rust-lang.org/std/pin/index.html#assigning-pinned-data)通常是安全的。虽然不能以通常方式完成（`*p = ...`），但可以用 [`Pin::set`](https://doc.rust-lang.org/std/pin/struct.Pin.html#method.set)。更一般地，你可以用 unsafe 代码向 pointee 的字段赋值。

使用 `Pin::set` 总是安全的，因为先前被固定的 pointee 会被 drop，满足 Pin 要求，且新 pointee 在移入固定位置完成之前未被固定。向单个字段赋值不会自动违反 Pin 要求，但必须小心确保对象整体保持有效。例如，如果向某字段赋值，则引用该字段的任何其他字段仍必须对新对象有效（这不是 Pin 要求的一部分，但可能是对象其他不变量的一部分）。

将一固定对象复制到另一固定位置只能在 unsafe 代码中完成，如何维护安全取决于具体对象。没有一般性地违反 Pin 要求——被替换的对象不移动，被复制的对象也不移动。然而，被替换对象的有效性可能有通常由 Pin 保护的安全要求，但在这种情况下必须由程序员建立。例如，如果我们有一个有两个字段 `a` 和 `b` 的结构体，其中 `b` 引用 `a`，该引用需要 Pin 才能保持有效。如果这样的结构体被复制到另一位置，则 `b` 的值必须更新为指向新的 `a` 而非旧的。


## Pin 与 async 编程

希望你可以做所有你想用 async Rust 做的事而从不担心 Pin。有时你会碰到需要 Pin 的边角情况，如果你想实现 future、运行时或类似东西，你需要了解 Pin。本节我会解释原因。

Async 函数被实现为 future（见 TODO 节——这是摘要概述，确保我们在别处更深入地用例子解释）。在每个 await 点，函数的执行可能暂停，在此期间存活变量的值必须保存。它们本质上成为结构体的字段（是 enum 的一部分）。这样的变量可能引用保存在 future 中的其他变量，例如考虑，

```rust,norun
async fn foo() {
  let a = ...;
  let b = &a;
  bar().await;
  // 使用 b
}
```

这里生成的 future 对象会类似：

```rust,norun
struct Foo {
  a: A,
  b: &'self A,  // 不变量 `self.b == &self.a`
}
```

（我简化了一些，忽略执行状态等，但重要的是变量/字段）。

这在直觉上说得通，不幸的是 Rust 中不存在 `'self`。而且有好理由！记住 Rust 对象可以移动，因此如下代码会是不健全的：

```rust,norun
let f1 = Foo { ... }; // f1.b == &f1.a
let f2 = f1; // f2.b == &f1.a，但 f1 已不存在，因为它移到了 f2
```

注意这不仅是无法命名生存期的问题，即使我们使用裸指针，这样的代码仍然不正确。

然而，如果我们知道一旦创建，`Foo` 的实例就永远不会移动，那么一切就能正常工作。（编译器内部对此类情况有类似 `'self` 的概念，作为程序员，我们必须使用裸指针和 unsafe 代码）。这种不移动的概念正是 Pin 所描述的。

我们在 `Future::poll` 的签名中看到这一要求，其中 `self`（future）的类型是 `Pin<&mut Self>`。大多数情况下，使用 async/await 时，编译器负责固定和取消固定，作为程序员你不必担心。


### 手动固定

有些地方 Pin 会穿透 async/await 的抽象。根本上这是由于 `Future::poll` 和 `Stream::poll_next` 签名中的 `Pin`。直接（而非通过 async/await）使用 future 和 stream 时，我们可能需要考虑 Pin 才能让事情工作。需要固定类型的一些常见原因：

- 轮询 future 或 stream——在应用代码中或实现你自己的 future 时。
- 使用装箱的 future。如果你使用装箱的 future（或 stream）并因此写出 future 类型而非使用 async 函数，你可能会在那些类型中看到很多 `Pin<...>`，并需要用 `Box::pin` 创建 future。
- 实现 future——在 `poll` 内部，`self` 被固定，因此你需要使用 pin projection 和/或 unsafe 代码来获取 `self` 字段的可变访问。
- 组合 future 或 stream。这大多只是工作，但如果你需要取得 future 的引用然后轮询它（例如在循环外定义 future 并在循环内的 `select!` 中使用），你需要固定该引用才能像 future 一样使用该引用。
- 处理 stream——目前 Rust 围绕 stream 的抽象比 future 少，因此你更可能使用组合子方法（技术上不要求 Pin，但似乎使围绕引用或创建 future/stream 的问题更普遍），甚至手动 `poll`，而非处理 future 时。


## 替代与扩展

本节面向对 Pin 周围语言设计好奇的读者。如果你只想阅读、理解并编写 async 程序，绝对不必读本节。

Pin 难以理解且可能感觉有点笨拙，因此人们常想知道是否有更好的替代或变体。我会介绍几种替代并说明它们为何要么不行，要么比你可能预期的更复杂。

不过在此之前，理解 Pin 的历史背景很重要。如果你在设计一门全新语言并想支持 async/await、自引用或不可移动类型，肯定有比 Rust 的 Pin 更好的方式。然而，async/await、future 和 Pin 是在 Rust 1.0 发布之后加入的，并在强向后兼容保证的语境下设计。除这一硬性要求外，还希望在合理时间框架内设计和实现该特性。某些解决方案（例如涉及线性类型）需要基础研究、设计和实现，考虑到 Rust 项目的资源和约束，现实地要以十年计。

### 替代方案

首先，考虑使 Rust 类型默认不可移动的一类解决方案。注意这是对 Rust 基本语义的重大改变；此类中的任何解决方案可能需要大量努力才能实现向后兼容（我不推测特定方案是否可能，但借助自动 trait、derive 属性、edition、迁移工具等，或许可能）。

一种提议（实际上是一组提议，因为语义有多种定义方式）是有一个 `Move` 标记 trait（类似 `Copy`），标记对象为可移动，所有其他类型不可移动。与 `Pin` 相反，这是值的属性而非指针的属性，因此影响范围大得多，例如若 `b` 不实现 `Move`，则 `let a = b;` 会是错误。

这种方法的根本问题是：当今 Pin 是分阶段概念（位置开始时未固定，然后变为已固定），而类型适用于值的整个生存期。（Pin 也最好理解为位置的属性而非值的属性，但类型适用于值；这是否是任何基于 trait 的方法的根本问题，我不知道）。这在两篇博文中探讨：[Two Ways Not to Move](https://theincredibleholk.org/blog/2024/07/15/two-ways-not-to-move/) 和 [Ergonomic Self-Referential Types for Rust](https://blog.yoshuawuyts.com/self-referential-types/#immovable-types)。

此外，任何 `Move` trait 可能会有[向后兼容](https://without.boats/blog/pin/)问题，并导致「传染性边界」（即 `Move` 或 `!Move` 会在很多很多地方被要求）。

另一种提议是支持类似 C++ 的移动构造函数。然而，这会破坏 Rust 对象总是可以按位移动的基本不变量。那会使 Rust 更不可预测，从而使 Rust 程序更难理解和调试。这是最糟糕的一种向后不兼容变更，因为它会静默破坏 unsafe 代码，因为它改变了代码作者可能做出的基本假设。此外，如此根本变更所需的设计和实现工作量会巨大。除了这些实际问题，甚至不清楚是否可行：移动构造函数可用于修复被移动对象内的引用，但可能有来自对象外部的、指向被移动对象的引用无法修复。

另一种不同类型的潜在解决方案是偏移引用的思想。这是相对而非绝对的引用，即作为对另一字段偏移引用的字段在对象在内存中移动时仍总是指向同一对象内部。偏移指针的问题是字段必须是偏移指针或绝对指针之一。但 async 函数中的引用成为字段，有时引用 future 对象内部内存，有时引用外部内存。


### 扩展

有多项提议使 Pin 更强大和/或更易使用。这些大多是提议以各种方式使 Pin 成为语言中更一等的一部分，而非纯库概念（它们常包括 std 和语言的扩展）。我会介绍几个较成熟的想法，它们彼此相关，共同目标是通过使创建和使用固定位置更容易来改善 Pin 的易用性，尤其在结构固定和 `drop` 周围。

[Pinned places](https://without.boats/blog/pinned-places/) 延续 Pin 是位置而非值或类型的属性的思想，向引用添加类似 `mut` 的 `pin`/`pinned` 修饰符。这与再借用和方法解析集成，改善固定 `self` 的方法调用的 ergonomics。

[`UnpinCell`](https://without.boats/blog/unpin-cell/) 将固定位置思想扩展以支持字段的原生 pin projection。[MinPin](https://smallcultfollowing.com/babysteps/blog/2024/11/05/minpin/) 是更精简（且向后兼容）的原生 pin projection 和更好 `drop` 支持的提议。

[`Overwrite` trait](https://smallcultfollowing.com/babysteps/series/overwrite-trait/) 是提议的 trait，显式区分修改对象一部分的权限（`foo.f = ...`）和覆盖整个对象的权限（`*foo = ...`），后者对当前所有可变引用都允许。该提议还包括不可变字段。`Overwrite` 是 `Unpin` 的某种替代，（与固定位置的一些思想一起）可以改善使用 Pin。不幸的是，虽然可以向后兼容地采用，过渡会比其他扩展多很多工作。


## 参考资料

- [std 文档](https://doc.rust-lang.org/std/pin/index.html) `Pin` 等行为与保证的权威来源。文档很好。
  - [`Pin`](https://doc.rust-lang.org/std/pin/struct.Pin.html)、[`Unpin`](https://doc.rust-lang.org/std/marker/trait.Unpin.html)、[`pin` 宏](https://doc.rust-lang.org/std/pin/macro.pin.html)
- [RFC 2349](https://rust-lang.github.io/rfcs/2349-pin.html) 提出 Pin 的 RFC。稳定化的 API 与这里提议的略有不同，但 RFC 中对核心概念和理由有很好的解释。
- 一些解释 Pin 的博文或其他资源：
  - [Pin](https://without.boats/blog/pin/)，WithoutBoats（Pin 的主要设计者）关于 Pin 的历史、语境和理由，以及为何它是难懂的概念。
  - [Why is std::pin::Pin so weird?](https://sander.saares.eu/2024/11/06/why-is-stdpinpin-so-weird/) 深入 Pin 设计理由及实践中使用 Pin。
  - [Pin, Unpin, and why Rust needs them](https://blog.cloudflare.com/pin-and-unpin-in-rust/)
  - [async/await 的 Pin 一节](https://os.phil-opp.com/async-await/#pinning)
  - [Pin and suffering](https://fasterthanli.me/articles/pin-and-suffering) 以非常对话的风格、大量例子透彻讲解理解 async 代码与 Pin 的博文。
  - Jon Gjengset 的 *Rust for Rustaceans* 一书对为何 Pin 对 async/await 实现是必要的以及 Pin 如何工作有出色描述。
