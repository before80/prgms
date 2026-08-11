+++
title = "18.2 用 Trait 对象抽象共享行为"
date = 2026-08-05T08:44:00+08:00
weight = 88
type = "docs"
description = "用 trait 对象在运行时对不同类型实现共享行为，并说明动态分发"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Trait 对象抽象共享行为 {#trait}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html](https://doc.rust-lang.org/stable/book/ch18-02-trait-objects.html)


## 用 Trait 对象抽象共享行为 {#using-trait-objects-to-abstract-over-shared-behavior}

　　在第 8 章我们提到，向量的一个限制是只能存储单一类型的元素。我们在示例 8-9 中做了变通：定义了带有保存整数、浮点数与文本变体的 `SpreadsheetCell` 枚举。这样我们就能在每个单元格中存储不同类型的数据，同时仍有一个表示一行单元格的向量。当我们可互换的项是编译时已知的固定类型集合时，这是完全好的方案。

　　不过有时我们希望库的用户能扩展在特定情境下合法的类型集合。为展示如何做到这一点，我们将创建一个图形用户界面（GUI）工具示例：遍历项列表，对每一项调用 `draw` 方法将其绘制到屏幕上——这是 GUI 工具的常见技术。我们将创建一个名为 `gui` 的库 crate，包含 GUI 库的结构。该 crate 可能包含一些供人使用的类型，如 `Button` 或 `TextField`。此外，`gui` 的用户会想创建自己可被绘制的类型：例如，一位程序员可能添加 `Image`，另一位可能添加 `SelectBox`。

　　在编写库时，我们无法知道并定义其他程序员可能想创建的全部类型。但我们知道 `gui` 需要跟踪许多不同类型的值，并需要对这些不同类型的值各自调用 `draw` 方法。它不必确切知道调用 `draw` 时会发生什么，只需知道该值会提供可供我们调用的该方法。

　　若在有继承的语言中做这件事，我们可能定义一个名为 `Component` 的类，其上有名为 `draw` 的方法。其他类如 `Button`、`Image` 与 `SelectBox` 会继承自 `Component`，从而继承 `draw` 方法。它们可以各自覆盖 `draw` 以定义自定义行为，但框架可以把所有类型都当作 `Component` 实例并调用 `draw`。但因为 Rust 没有继承，我们需要另一种方式来组织 `gui` 库，以允许用户创建与库兼容的新类型。

### 为共同行为定义 Trait

　　为实现我们希望 `gui` 具备的行为，我们将定义名为 `Draw` 的 trait，其上有一个名为 `draw` 的方法。然后可以定义一个接受 trait 对象的向量。*Trait 对象*既指向实现了我们指定 trait 的类型的实例，也指向一张在运行时用于查找该类型上 trait 方法的表。我们通过指定某种指针（如引用或 `Box<T>` 智能指针），再跟 `dyn` 关键字，再指定相关 trait，来创建 trait 对象。（我们将在第 20 章[「动态大小类型与 `Sized` Trait」][dynamically-sized]中讨论为何 trait 对象必须使用指针。）我们可以用 trait 对象代替泛型或具体类型。凡是使用 trait 对象的地方，Rust 的类型系统都会在编译期确保该上下文中使用的任何值都实现了该 trait 对象的 trait。因此，我们不必在编译期知道全部可能的类型。

　　我们提到过，在 Rust 中我们避免把结构体与枚举称为“对象”，以便与其他语言中的对象区分开。在结构体或枚举中，结构体字段中的数据与 `impl` 块中的行为是分开的，而在其他语言中，当数据与行为合为一体时，这一概念往往被称为“对象”。Trait 对象与其他语言中的对象不同之处在于：我们不能向 trait 对象添加数据。Trait 对象也不像其他语言中的对象那样普遍有用：它们的特定目的是跨共同行为做抽象。

　　示例 18-3 展示了如何定义带有一个名为 `draw` 的方法的 `Draw` trait。

**文件名：`src/lib.rs`**
```rust
pub trait Draw {
    fn draw(&self);
}
```

**示例 18-3：`Draw` trait 的定义**

　　这一语法应与我们在第 10 章讨论如何定义 trait 时看起来很熟悉。接下来是一些新语法：示例 18-4 定义了名为 `Screen` 的结构体，它持有名为 `components` 的向量。该向量的类型是 `Box<dyn Draw>`，这是一个 trait 对象；它代表 `Box` 内任何实现了 `Draw` trait 的类型。

**文件名：`src/lib.rs`**
```rust
pub struct Screen {
    pub components: Vec<Box<dyn Draw>>,
}
```

**示例 18-4：定义带有 `components` 字段的 `Screen` 结构体，该字段持有实现了 `Draw` trait 的 trait 对象向量**

　　在 `Screen` 结构体上，我们将定义名为 `run` 的方法，它会对每个 `components` 调用 `draw` 方法，如示例 18-5 所示。

**文件名：`src/lib.rs`**
```rust
impl Screen {
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

**示例 18-5：`Screen` 上的 `run` 方法，对每个组件调用 `draw`**

　　这与定义使用带 trait 约束的泛型类型参数的结构体的工作方式不同。泛型类型参数一次只能替换成一种具体类型，而 trait 对象允许在运行时用多种具体类型填补该 trait 对象。例如，我们可以像示例 18-6 那样用泛型类型与 trait 约束定义 `Screen` 结构体。

**文件名：`src/lib.rs`**
```rust
pub struct Screen<T: Draw> {
    pub components: Vec<T>,
}

impl<T> Screen<T>
where
    T: Draw,
{
    pub fn run(&self) {
        for component in self.components.iter() {
            component.draw();
        }
    }
}
```

**示例 18-6：用泛型与 trait 约束实现的另一种 `Screen` 结构体及其 `run` 方法**

　　这会把我们限制为：一个 `Screen` 实例的组件列表要么全是 `Button` 类型，要么全是 `TextField` 类型。若你永远只有同质集合，使用泛型与 trait 约束更可取，因为定义会在编译期单态化为使用具体类型。

　　另一方面，使用 trait 对象的方法时，一个 `Screen` 实例可以持有同时包含 `Box<Button>` 与 `Box<TextField>` 的 `Vec<T>`。我们先看看这如何工作，再谈运行时性能影响。

### 实现 Trait

　　现在我们添加一些实现 `Draw` trait 的类型。我们将提供 `Button` 类型。同样，真正实现 GUI 库超出了本书范围，因此 `draw` 方法体中不会有有用的实现。为想象实现可能长什么样，`Button` 结构体可能有 `width`、`height` 与 `label` 字段，如示例 18-7 所示。

**文件名：`src/lib.rs`**
```rust
pub struct Button {
    pub width: u32,
    pub height: u32,
    pub label: String,
}

impl Draw for Button {
    fn draw(&self) {
        // code to actually draw a button
    }
}
```

**示例 18-7：实现了 `Draw` trait 的 `Button` 结构体**

　　`Button` 上的 `width`、`height` 与 `label` 字段会与其他组件上的字段不同；例如，`TextField` 类型可能有那些相同字段再加上 `placeholder` 字段。我们想在屏幕上绘制的每种类型都会实现 `Draw` trait，但会在 `draw` 方法中使用不同代码来定义如何绘制该特定类型，就像这里的 `Button`（如前所述，没有实际 GUI 代码）。例如，`Button` 类型可能还有另一个 `impl` 块，包含与用户点击按钮时发生的事相关的方法。这类方法不适用于像 `TextField` 这样的类型。

　　若使用我们库的人决定实现带有 `width`、`height` 与 `options` 字段的 `SelectBox` 结构体，他们也会在 `SelectBox` 类型上实现 `Draw` trait，如示例 18-8 所示。

**文件名：`src/main.rs`**
```rust
use gui::Draw;

struct SelectBox {
    width: u32,
    height: u32,
    options: Vec<String>,
}

impl Draw for SelectBox {
    fn draw(&self) {
        // code to actually draw a select box
    }
}
```

**示例 18-8：另一个 crate 使用 `gui` 并在 `SelectBox` 结构体上实现 `Draw` trait**

　　我们库的用户现在可以编写他们的 `main` 函数来创建 `Screen` 实例。他们可以把 `SelectBox` 与 `Button` 各自放进 `Box<T>` 变成 trait 对象，再添加到 `Screen` 实例。然后可以在 `Screen` 实例上调用 `run` 方法，它会对每个组件调用 `draw`。示例 18-9 展示了这一实现。

**文件名：`src/main.rs`**
```rust
use gui::{Button, Screen};

fn main() {
    let screen = Screen {
        components: vec![
            Box::new(SelectBox {
                width: 75,
                height: 10,
                options: vec![
                    String::from("Yes"),
                    String::from("Maybe"),
                    String::from("No"),
                ],
            }),
            Box::new(Button {
                width: 50,
                height: 10,
                label: String::from("OK"),
            }),
        ],
    };

    screen.run();
}
```

**示例 18-9：用 trait 对象存储实现同一 trait 的不同类型的值**

　　编写库时我们并不知道有人可能添加 `SelectBox` 类型，但我们的 `Screen` 实现能够操作并绘制这个新类型，因为 `SelectBox` 实现了 `Draw` trait，也就实现了 `draw` 方法。

　　这种只关心值响应哪些消息、而不关心值的具体类型的概念，类似于动态类型语言中的*鸭子类型*（duck typing）：若它走起来像鸭子、叫起来像鸭子，那它一定是鸭子！在示例 18-5 中 `Screen` 上 `run` 的实现里，`run` 不必知道每个组件的具体类型。它不检查组件是 `Button` 还是 `SelectBox` 的实例，只是对组件调用 `draw` 方法。通过把 `components` 向量中值的类型指定为 `Box<dyn Draw>`，我们规定了 `Screen` 需要的是我们可以对其调用 `draw` 方法的值。

　　用 trait 对象与 Rust 的类型系统编写类似鸭子类型代码的优势在于：我们永远不必在运行时检查值是否实现了特定方法，也不必担心若值未实现某方法我们却调用了它而得到错误。若值没有实现 trait 对象所需的 trait，Rust 就不会编译我们的代码。

　　例如，示例 18-10 展示了若我们试图用 `String` 作为组件创建 `Screen` 会发生什么。

**文件名：`src/main.rs`**
```rust
use gui::Screen;

fn main() {
    let screen = Screen {
        components: vec![Box::new(String::from("Hi"))],
    };

    screen.run();
}
```

**示例 18-10：试图使用未实现 trait 对象所需 trait 的类型**

　　我们会得到这个错误，因为 `String` 没有实现 `Draw` trait：

```console
$ cargo run
   Compiling gui v0.1.0 (file:///projects/gui)
error[E0277]: the trait bound `String: Draw` is not satisfied
  --> src/main.rs:5:26
   |
 5 |         components: vec![Box::new(String::from("Hi"))],
   |                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ the trait `Draw` is not implemented for `String`
   |
help: the trait `Draw` is implemented for `Button`
  --> src/lib.rs:23:1
   |
23 | impl Draw for Button {
   | ^^^^^^^^^^^^^^^^^^^^
   = note: required for the cast from `Box<String>` to `Box<dyn Draw>`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `gui` (bin "gui") due to 1 previous error
```

　　这个错误让我们知道：要么我们向 `Screen` 传了本意以外的东西，因而应传不同类型；要么应在 `String` 上实现 `Draw`，以便 `Screen` 能对其调用 `draw`。

### 执行动态分发

　　回想第 10 章[「使用泛型的代码的性能」][performance-of-code-using-generics]中我们关于编译器对泛型执行的单态化过程的讨论：编译器会为每个用来替换泛型类型参数的具体类型生成函数与方法的非泛型实现。单态化产生的代码做的是*静态分发*（static dispatch），即编译器在编译期就知道你在调用哪个方法。这与*动态分发*（dynamic dispatch）相对，后者是编译器在编译期无法判断你在调用哪个方法。在动态分发的情形下，编译器发出的代码会在运行时才知道要调用哪个方法。

　　当我们使用 trait 对象时，Rust 必须使用动态分发。编译器不知道可能与使用 trait 对象的代码一起使用的全部类型，因此不知道要调用哪个类型上实现的哪个方法。相反，在运行时，Rust 使用 trait 对象内部的指针来知道要调用哪个方法。这种查找会带来静态分发所没有的运行时开销。动态分发还会阻止编译器选择内联方法的代码，进而阻止某些优化；而且 Rust 对何处可以使用、何处不能使用动态分发有一些规则，称为 *dyn 兼容性*（dyn compatibility）。那些规则超出了本讨论范围，但你可以在[参考手册][dyn-compatibility]中阅读更多内容。不过，我们确实在示例 18-5 所写、并在示例 18-9 中得以支持的代码里获得了额外灵活性，因此这是需要权衡的取舍。

[performance-of-code-using-generics]: ../../generics/01-syntax/#performance-of-code-using-generics
[dynamically-sized]: ../../advanced-features/03-advanced-types/#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility
