+++
title = "4.2 点运算符"
date = 2026-08-06T17:08:00+08:00
weight = 24
type = "docs"
description = "点运算符的自动解引用与转换"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 点运算符


> 原文链接: [https://doc.rust-lang.org/nomicon/dot-operator.html](https://doc.rust-lang.org/nomicon/dot-operator.html)


　　点运算符会做大量魔法来转换类型。
　　它会自动引用、自动解引用并强制转换，直到类型匹配。
　　方法查找的详细机制见[此处][method_lookup]，
　　下面是概述主要步骤的简要说明。

　　设我们有带 receiver（`self`、`&self` 或 `&mut self` 参数）的函数 `foo`。
　　若调用 `value.foo()`，编译器须先确定 `Self` 的类型，才能调用正确的函数实现。
　　本例设 `value` 的类型为 `T`。

　　为更清楚说明调用的是哪个类型上的函数，我们使用[完全限定语法][fqs]。

- 首先，编译器检查能否直接调用 `T::foo(value)`。
　　这叫「按值」方法调用。
- 若无法调用（例如函数类型不对，或未为 `Self` 实现 trait），编译器尝试自动添加引用。
　　即尝试 `<&T>::foo(value)` 和 `<&mut T>::foo(value)`。
　　这叫「自动引用」（autoref）方法调用。
- 若这些候选都不行，则解引用 `T` 并重试。
　　这使用 `Deref` trait——若 `T: Deref<Target = U>`，则用 `U` 而非 `T` 重试。
　　若无法解引用 `T`，还可尝试 _unsizing_ `T`。
　　即若 `T` 有编译期已知的大小参数，为解析方法而「忘记」它。
　　例如此 unsizing 步骤可通过「忘记」数组大小，把 `[i32; 2]` 转为 `[i32]`。

　　方法查找算法示例：

```rust,ignore
let array: Rc<Box<[T; 3]>> = ...;
let first_entry = array[0];
```

　　编译器如何计算层层间接引用后的 `array[0]`？
　　首先，`array[0]` 只是 [`Index`][index] trait 的语法糖——
　　编译器把 `array[0]` 转为 `array.index(0)`。
　　然后检查 `array` 是否实现 `Index`，以便调用该函数。

　　接着检查 `Rc<Box<[T; 3]>>` 是否实现 `Index`，但没有，`<&Rc<Box<[T; 3]>>>` 和 `<&mut Rc<Box<[T; 3]>>>` 也没有。
　　都不行，编译器把 `Rc<Box<[T; 3]>>` 解引用为 `Box<[T; 3]>` 并重试。
　　`Box<[T; 3]>`、`&Box<[T; 3]>` 和 `&mut Box<[T; 3]>` 都不实现 `Index`，再解引用。
　　`[T; 3]` 及其自动引用也不实现 `Index`。
　　无法解引用 `[T; 3]`，编译器 unsizing 为 `[T]`。
　　最后 `[T]` 实现 `Index`，可调用实际的 `index` 函数。

　　点运算符更复杂示例：

```rust
fn do_stuff<T: Clone>(value: &T) {
    let cloned = value.clone();
}
```

　　`cloned` 是什么类型？
　　首先编译器检查能否按值调用。
　　`value` 的类型是 `&T`，`clone` 函数签名为 `fn clone(&T) -> T`。
　　编译器知道 `T: Clone`，判定 `cloned: T`。

　　若去掉 `T: Clone` 限制会怎样？无法按值调用，因为没有 `T` 的 `Clone` 实现。
　　编译器尝试 autoref 调用。
　　此时函数签名为 `fn clone(&&T) -> &T`，因为 `Self = &T`。
　　编译器看到 `&T: Clone`，推断 `cloned: &T`。

　　autoref 行为还可产生微妙效果：

```rust
# use std::sync::Arc;
#
#[derive(Clone)]
struct Container<T>(Arc<T>);

fn clone_containers<T>(foo: &Container<i32>, bar: &Container<T>) {
    let foo_cloned = foo.clone();
    let bar_cloned = bar.clone();
}
```

　　`foo_cloned` 和 `bar_cloned` 是什么类型？
　　已知 `Container<i32>: Clone`，编译器按值调用 `clone`，得 `foo_cloned: Container<i32>`。
　　但 `bar_cloned` 实际类型是 `&Container<T>`。
　　这似乎不合理——我们加了 `#[derive(Clone)]`，按理应已实现 `Clone`！
　　细看 `derive` 宏生成的代码（大致）：

```rust,ignore
impl<T> Clone for Container<T> where T: Clone {
    fn clone(&self) -> Self {
        Self(Arc::clone(&self.0))
    }
}
```

　　derive 的 `Clone` 实现[仅在 `T: Clone` 时定义][clone]，
　　因此对泛型 `T` 没有 `Container<T>: Clone` 的实现。
　　编译器接着检查 `&Container<T>` 是否实现 `Clone`，确实实现了。
　　因此推断 `clone` 通过 autoref 调用，`bar_cloned` 类型为 `&Container<T>`。

　　可手动实现 `Clone`，不要求 `T: Clone`：

```rust,ignore
impl<T> Clone for Container<T> {
    fn clone(&self) -> Self {
        Self(Arc::clone(&self.0))
    }
}
```

　　类型检查器推断 `bar_cloned: Container<T>`。

[fqs]: ../book/ch19-03-advanced-traits.html#fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name
[method_lookup]: https://rustc-dev-guide.rust-lang.org/hir-typeck/method-lookup.html
[index]: ../std/ops/trait.Index.html
[clone]: ../std/clone/trait.Clone.html#derivable
