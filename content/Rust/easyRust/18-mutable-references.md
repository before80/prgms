+++
title = "18-可变引用"
date = 2026-08-21T12:46:00+08:00
weight = 19
type = "docs"
description = "可变引用 — Easy Rust 中文译本"
isCJKLanguage = true
draft = false
+++

> 译文 · 基于 [Easy Rust](https://dhghomon.github.io/easy_rust/)

> 原文链接: [https://dhghomon.github.io/easy_rust/Chapter_17.html](https://dhghomon.github.io/easy_rust/Chapter_17.html)

> 中文参考：[kumakichi/easy_rust_chs](https://kumakichi.github.io/easy_rust_chs/)

# 可变引用

如果您想使用一个引用来改变数据，您可以使用一个可变引用。对于可变引用，您可以写 `&mut` 而不是 `&`。

```rust
fn main() {
    let mut my_number = 8; // 别忘了这里要写 mut！
    let num_ref = &mut my_number;
}
```

那么这两种类型是什么呢？`my_number`是`i32`，`num_ref`是`&mut i32`(我们说是 "可变引用`i32`")。

所以我们用它来给my_number加10。但是你不能写`num_ref += 10`，因为`num_ref`不是`i32`的值，它是一个`&i32`。其实这个值就在`i32`里面。为了达到值所在的地方，我们用`*`。`*`的意思是 "我不要引用，我要引用对应的值"。换句话说，一个`*`与`&`是相反的。另外，一个`*`抹去了一个`&`。

```rust
fn main() {
    let mut my_number = 8;
    let num_ref = &mut my_number;
    *num_ref += 10; // 用 * 修改 i32 的值。
    println!("{}", my_number);

    let second_number = 800;
    let triple_reference = &&&second_number;
    println!("Second_number = triple_reference? {}", second_number == ***triple_reference);
}
```

这个打印:

```text
18
Second_number = triple_reference? true
```

因为使用`&`叫做 "引用"，所以使用`*`叫做 "**de**referencing"。

Rust有两个规则，分别是可变引用和不可变引用。它们非常重要，但也很容易记住，因为它们很有意义。

- **规则1**。如果你只有不可变引用，你可以有任意多的引用。1个也行，3个也行，1000个也行，没问题。
- **规则2**: 如果你有一个可变引用，你只能有一个。另外，你不能同时使用一个不可变引用**和**一个可变引用。

这是因为可变引用可以改变数据。如果你在其他引用读取数据时改变数据，你可能会遇到问题。


一个很好的理解方式是思考一个Powerpoint演示。

情况一是关于**只有一个可变引用**

情境一 一个员工正在编写一个Powerpoint演示文稿，他希望他的经理能帮助他。他希望他的经理能帮助他。该员工将自己的登录信息提供给经理，并请他帮忙进行编辑。现在，经理对该员工的演示文稿有了一个 "可变引用"。经理可以做任何他想做的修改，然后把电脑还给他。这很好，因为没有人在看这个演示文稿。

情况二是关于**只有不可变引用**

情况二 该员工要给100个人做演示。现在这100个人都可以看到该员工的数据。
 他们都有一个 "不可改变的引用"，即员工的介绍。这很好，因为他们可以看到它，但没有人可以改变数据。

情况三是**有问题的情况**

情况三 员工把他的登录信息给了经理 他的经理现在有了一个 "可变引用"。然后员工去给100个人做演示，但是经理还是可以登录。这是不对的，因为经理可以登录，可以做任何事情。也许他的经理会登录电脑，然后开始给他的母亲打一封邮件! 现在这100人不得不看着经理给他母亲写邮件，而不是演示。这不是他们期望看到的。

下面是一个可变借用与不可变借用的例子:

```rust
fn main() {
    let mut number = 10;
    let number_ref = &number;
    let number_change = &mut number;
    *number_change += 10;
    println!("{}", number_ref); // ⚠️
}
```

编译器打印了一个有用的信息来告诉我们问题所在。

```text
error[E0502]: cannot borrow `number` as mutable because it is also borrowed as immutable
 --> src\main.rs:4:25
  |
3 |     let number_ref = &number;
  |                      ------- immutable borrow occurs here
4 |     let number_change = &mut number;
  |                         ^^^^^^^^^^^ mutable borrow occurs here
5 |     *number_change += 10;
6 |     println!("{}", number_ref);
  |                    ---------- immutable borrow later used here
```

然而，这段代码可以工作。为什么会这样？

```rust
fn main() {
    let mut number = 10;
    let number_change = &mut number; // 创建可变引用
    *number_change += 10; // 用可变引用加 10
    let number_ref = &number; // 创建不可变引用
    println!("{}", number_ref); // 打印不可变引用
}
```

它打印出`20`没有问题。它能工作是因为编译器足够聪明，能够理解我们的代码。它知道我们使用了`number_change`来改变`number`，但没有再使用它。所以这里没有问题。我们并没有将不可变和可变引用一起使用。

早期在Rust中，这种代码实际上会产生错误，但现在的编译器更聪明了。它不仅能理解我们输入的内容，还能理解我们如何使用所有的东西。

## 再谈shadowing

还记得我们说过，shadowing不会**破坏**一个值，而是**屏蔽**它吗？现在我们可以用引用来看看这个问题。

```rust
fn main() {
    let country = String::from("Austria");
    let country_ref = &country;
    let country = 8;
    println!("{}, {}", country_ref, country);
}
```

这是打印`Austria, 8`还是`8, 8`？它打印的是`Austria, 8`。首先我们声明一个`String`，叫做`country`。然后我们给这个字符串创建一个引用`country_ref`。然后我们用8来shadowing国家，这是一个`i32`。但是第一个`country`并没有被销毁，所以`country_ref`仍然写着 "Austria"，而不是 "8"。下面是同样的代码，并加了一些注释来说明它的工作原理。

```rust
fn main() {
    let country = String::from("Austria"); // 现在有一个叫 country 的 String
    let country_ref = &country; // country_ref 是指向这份数据的引用。它不会变
    let country = 8; // 现在有一个叫 country 的 i8 变量。但它和另一个无关，也和 country_ref 无关
    println!("{}, {}", country_ref, country); // country_ref 仍然指向我们给它的 String::from("Austria") 的数据。
}
```
