+++
title = "15.5 RefCell<T> 与内部可变性模式"
date = 2026-08-05T08:44:00+08:00
weight = 72
type = "docs"
description = "用 RefCell<T> 在运行时检查借用，并实现内部可变性"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# RefCell<T> 与内部可变性模式 {#refcell-t}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch15-05-interior-mutability.html](https://doc.rust-lang.org/stable/book/ch15-05-interior-mutability.html)


## `RefCell<T>` 与内部可变性模式

　　**内部可变性**（interior mutability）是 Rust 中的一种设计模式：即便存在指向某数据的不可变引用，仍允许你修改该数据；通常借用规则禁止这种做法。为了修改数据，该模式在数据结构内部使用 `unsafe` 代码，以绕开 Rust 通常对修改与借用的规则。`unsafe` 代码向编译器表明：我们手动检查规则，而不是依赖编译器代劳；第 20 章会更深入讨论不安全代码。

　　只有当我们能确保借用规则会在运行时被遵守（即便编译器无法保证）时，才能使用遵循内部可变性模式的类型。相关的 `unsafe` 代码被包装在安全 API 中，外层类型仍然是不可变的。

　　下面通过遵循内部可变性模式的 `RefCell<T>` 类型来探索这一概念。

### 在运行时强制执行借用规则

　　与 `Rc<T>` 不同，`RefCell<T>` 表示对其所持数据的单一所有权。那么 `RefCell<T>` 与像 `Box<T>` 这样的类型有何不同？回想第 4 章学过的借用规则：

- 在任意给定时刻，要么只能有一个可变引用，要么可以有任意数量的不可变引用（但不能两者兼有）。
- 引用必须始终有效。

　　对于引用与 `Box<T>`，借用规则的不变量在**编译期**强制执行。对于 `RefCell<T>`，这些不变量在**运行时**强制执行。使用引用时若破坏这些规则，会得到编译错误；使用 `RefCell<T>` 时若破坏这些规则，程序会 panic 并退出。

　　在编译期检查借用规则的优点是：错误会在开发过程中更早被发现，且由于分析已提前完成，对运行时性能没有影响。因此，多数情况下在编译期检查借用规则是最佳选择，这也是 Rust 的默认做法。

　　改为在运行时检查借用规则的优点是：某些内存安全的场景会被允许，而这些场景若按编译期检查会被禁止。像 Rust 编译器这样的静态分析本质上是保守的。有些代码属性无法通过分析代码检测到：最著名的例子是停机问题（Halting Problem），这超出了本书范围，但很值得自行研究。

　　因为有些分析不可能完成，若 Rust 编译器无法确定代码是否符合所有权规则，它可能会拒绝一个正确的程序——就此而言它是保守的。若 Rust 接受了不正确的程序，用户就无法信任 Rust 做出的保证。然而，若 Rust 拒绝了正确的程序，程序员会感到不便，但不会发生灾难性后果。当你确信代码遵循借用规则，而编译器却无法理解并保证这一点时，`RefCell<T>` 类型就很有用。

　　与 `Rc<T>` 类似，`RefCell<T>` 只适用于单线程场景；若在多线程上下文中使用，会得到编译期错误。第 16 章会讨论如何在多线程程序中获得类似 `RefCell<T>` 的功能。

　　这里总结一下选择 `Box<T>`、`Rc<T>` 或 `RefCell<T>` 的理由：

- `Rc<T>` 允许多个所有者共享同一数据；`Box<T>` 与 `RefCell<T>` 是单一所有者。
- `Box<T>` 允许在编译期检查的不可变或可变借用；`Rc<T>` 只允许在编译期检查的不可变借用；`RefCell<T>` 允许在运行时检查的不可变或可变借用。
- 因为 `RefCell<T>` 允许在运行时检查的可变借用，即便 `RefCell<T>` 本身是不可变的，你也可以修改其内部的值。

　　修改不可变值内部的值，就是内部可变性模式。下面看一个内部可变性有用的情形，并弄清它如何成为可能。

### 使用内部可变性

　　借用规则的一个后果是：当你有一个不可变值时，不能可变地借用它。例如，这段代码无法编译：

```rust
fn main() {
    let x = 5;
    let y = &mut x;
}
```

　　若尝试编译，会得到如下错误：

```console
$ cargo run
   Compiling borrowing v0.1.0 (file:///projects/borrowing)
error[E0596]: cannot borrow `x` as mutable, as it is not declared as mutable
 --> src/main.rs:3:13
  |
3 |     let y = &mut x;
  |             ^^^^^^ cannot borrow as mutable
  |
help: consider changing this to be mutable
  |
2 |     let mut x = 5;
  |         +++

For more information about this error, try `rustc --explain E0596`.
error: could not compile `borrowing` (bin "borrowing") due to 1 previous error
```

　　不过有些情形下，让值在自己的方法中修改自身、对外却表现为不可变，会很有用。值的方法之外的代码不能修改该值。使用 `RefCell<T>` 是获得内部可变性的一种方式，但 `RefCell<T>` 并未完全绕开借用规则：编译器中的借用检查器允许这种内部可变性，借用规则改为在运行时检查。若违反规则，你会得到 `panic!`，而不是编译错误。

　　下面通过一个实际例子，看看如何用 `RefCell<T>` 修改不可变值，以及为何有用。

#### 用模拟对象做测试

　　测试时，程序员有时会用一种类型代替另一种类型，以便观察特定行为并断言其实现正确。这种占位类型称为**测试替身**（test double）。可以联想像影视中的替身演员：有人代替演员完成特别棘手的场面。运行测试时，测试替身代替其他类型上场。**模拟对象**（mock object）是一类特定的测试替身：它们记录测试期间发生的事情，以便你断言正确的操作确实发生了。

　　Rust 没有其他语言那种意义上的对象，标准库也不像某些语言那样内置模拟对象功能。不过，你完全可以创建一个结构体来达到与模拟对象相同的目的。

　　我们要测试的场景是：创建一个库，对照最大值跟踪某个值，并根据当前值离最大值有多近发送消息。例如，该库可用于跟踪用户被允许发起的 API 调用次数配额。

　　我们的库只提供这些功能：跟踪值离最大值有多近，以及在什么时候应发送什么消息。使用该库的应用程序应提供发送消息的机制：可以直接向用户显示消息、发邮件、发短信，或做别的事。库不必知道这些细节；它只需要某个实现了我们提供的 `Messenger` 特征的东西。示例 15-20 展示了库代码。

**文件名：`src/lib.rs`**
```rust
pub trait Messenger {
    fn send(&self, msg: &str);
}

pub struct LimitTracker<'a, T: Messenger> {
    messenger: &'a T,
    value: usize,
    max: usize,
}

impl<'a, T> LimitTracker<'a, T>
where
    T: Messenger,
{
    pub fn new(messenger: &'a T, max: usize) -> LimitTracker<'a, T> {
        LimitTracker {
            messenger,
            value: 0,
            max,
        }
    }

    pub fn set_value(&mut self, value: usize) {
        self.value = value;

        let percentage_of_max = self.value as f64 / self.max as f64;

        if percentage_of_max >= 1.0 {
            self.messenger.send("Error: You are over your quota!");
        } else if percentage_of_max >= 0.9 {
            self.messenger
                .send("Urgent warning: You've used up over 90% of your quota!");
        } else if percentage_of_max >= 0.75 {
            self.messenger
                .send("Warning: You've used up over 75% of your quota!");
        }
    }
}
```

**示例 15-20：跟踪值离最大值有多近、并在达到某些水平时发出警告的库**

　　这段代码的一个要点是：`Messenger` 特征有一个名为 `send` 的方法，它接受对 `self` 的不可变引用以及消息文本。该特征是模拟对象需要实现的接口，以便模拟能以与真实对象相同的方式被使用。另一个要点是：我们想测试 `LimitTracker` 上 `set_value` 方法的行为。我们可以改变传入的 `value` 参数，但 `set_value` 不返回任何可供断言的东西。我们希望能够断言：若创建一个带有实现了 `Messenger` 的东西、以及某个 `max` 值的 `LimitTracker`，在传入不同的 `value` 时，信使会被要求发送相应的消息。

　　我们需要一个模拟对象：调用 `send` 时不发邮件或短信，而只记录被告知要发送的消息。可以新建模拟对象实例，创建使用该模拟的 `LimitTracker`，调用 `LimitTracker` 的 `set_value`，再检查模拟对象是否有我们期望的消息。示例 15-21 展示了实现这种模拟的一次尝试，但借用检查器不允许。

**文件名：`src/lib.rs`**
```rust
#[cfg(test)]
mod tests {
    use super::*;

    struct MockMessenger {
        sent_messages: Vec<String>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger {
                sent_messages: vec![],
            }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        let mock_messenger = MockMessenger::new();
        let mut limit_tracker = LimitTracker::new(&mock_messenger, 100);

        limit_tracker.set_value(80);

        assert_eq!(mock_messenger.sent_messages.len(), 1);
    }
}
```

**示例 15-21：尝试实现借用检查器不允许的 `MockMessenger`**

　　这段测试代码定义了 `MockMessenger` 结构体，其字段 `sent_messages` 是 `String` 的 `Vec`，用于记录被告知要发送的消息。我们还定义关联函数 `new`，方便创建以空消息列表开始的新 `MockMessenger`。然后为 `MockMessenger` 实现 `Messenger` 特征，以便能把它交给 `LimitTracker`。在 `send` 方法的定义中，我们把作为参数传入的消息存入 `MockMessenger` 的 `sent_messages` 列表。

　　在测试中，我们测试当 `LimitTracker` 被要求把 `value` 设为超过 `max` 的 75% 时会发生什么。首先创建新的 `MockMessenger`，它以空消息列表开始。然后创建新的 `LimitTracker`，给它对新 `MockMessenger` 的引用以及 `max` 值 `100`。对 `LimitTracker` 调用 `set_value`，传入 `80`（超过 100 的 75%）。然后断言：`MockMessenger` 正在跟踪的消息列表现在应有一条消息。

　　然而，这个测试有一个问题，如下所示：

```console
$ cargo test
   Compiling limit-tracker v0.1.0 (file:///projects/limit-tracker)
error[E0596]: cannot borrow `self.sent_messages` as mutable, as it is behind a `&` reference
  --> src/lib.rs:58:13
   |
58 |             self.sent_messages.push(String::from(message));
   |             ^^^^^^^^^^^^^^^^^^ `self` is a `&` reference, so it cannot be borrowed as mutable
   |
help: consider changing this to be a mutable reference in the `impl` method and the `trait` definition
   |
 2 ~     fn send(&mut self, msg: &str);
 3 | }
...
56 |     impl Messenger for MockMessenger {
57 ~         fn send(&mut self, message: &str) {
   |

For more information about this error, try `rustc --explain E0596`.
error: could not compile `limit-tracker` (lib test) due to 1 previous error
```

　　我们无法修改 `MockMessenger` 来记录消息，因为 `send` 方法接受对 `self` 的不可变引用。我们也不能按错误文本的建议，在 `impl` 方法与特征定义中都改用 `&mut self`。我们不想仅为测试而改动 `Messenger` 特征。相反，需要找到让测试代码在现有设计下正确工作的办法。

　　这正是内部可变性大显身手之处！我们把 `sent_messages` 存在 `RefCell<T>` 里，这样 `send` 方法就能修改 `sent_messages` 以存储我们见过的消息。示例 15-22 展示了那样做的样子。

**文件名：`src/lib.rs`**

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::RefCell;

    struct MockMessenger {
        sent_messages: RefCell<Vec<String>>,
    }

    impl MockMessenger {
        fn new() -> MockMessenger {
            MockMessenger {
                sent_messages: RefCell::new(vec![]),
            }
        }
    }

    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            self.sent_messages.borrow_mut().push(String::from(message));
        }
    }

    #[test]
    fn it_sends_an_over_75_percent_warning_message() {
        // --snip--

        assert_eq!(mock_messenger.sent_messages.borrow().len(), 1);
    }
}
```

**示例 15-22**


　　`sent_messages` 字段现在是 `RefCell<Vec<String>>` 而不是 `Vec<String>`。在 `new` 函数中，我们在空向量外包一层新的 `RefCell<Vec<String>>` 实例。

　　对 `send` 方法的实现，第一个参数仍是对 `self` 的不可变借用，与特征定义一致。我们对 `self.sent_messages` 中的 `RefCell<Vec<String>>` 调用 `borrow_mut`，以获得指向 `RefCell<Vec<String>>` 内部值（即向量）的可变引用。然后就可以对向量的可变引用调用 `push`，记录测试期间发送的消息。

　　最后还要改断言：要查看内部向量有多少项，对 `RefCell<Vec<String>>` 调用 `borrow`，以获得对向量的不可变引用。

　　既然已经看过如何使用 `RefCell<T>`，下面深入看看它如何工作！

#### 在运行时跟踪借用

　　创建不可变与可变引用时，我们分别使用 `&` 与 `&mut` 语法。对于 `RefCell<T>`，我们使用属于其安全 API 的 `borrow` 与 `borrow_mut` 方法。`borrow` 返回智能指针类型 `Ref<T>`，`borrow_mut` 返回智能指针类型 `RefMut<T>`。这两种类型都实现了 `Deref`，因此可以像常规引用一样对待它们。

　　`RefCell<T>` 跟踪当前有多少个 `Ref<T>` 与 `RefMut<T>` 智能指针处于活动状态。每次调用 `borrow`，`RefCell<T>` 就增加活动的不可变借用计数。当 `Ref<T>` 值离开作用域时，不可变借用计数减 1。与编译期借用规则一样，`RefCell<T>` 在任意时刻允许我们有多个不可变借用，或一个可变借用。

　　若尝试违反这些规则，不会像使用引用那样得到编译错误，而是 `RefCell<T>` 的实现会在运行时 panic。示例 15-23 修改了示例 15-22 中 `send` 的实现。我们故意在同一作用域内创建两个活动的可变借用，以说明 `RefCell<T>` 会在运行时阻止我们这样做。

**文件名：`src/lib.rs`**

```rust
    impl Messenger for MockMessenger {
        fn send(&self, message: &str) {
            let mut one_borrow = self.sent_messages.borrow_mut();
            let mut two_borrow = self.sent_messages.borrow_mut();

            one_borrow.push(String::from(message));
            two_borrow.push(String::from(message));
        }
    }
```

**示例 15-23**


　　我们为 `borrow_mut` 返回的 `RefMut<T>` 智能指针创建变量 `one_borrow`。然后以同样方式在变量 `two_borrow` 中再创建一个可变借用。这使同一作用域内有两个可变引用，这是不允许的。运行库的测试时，示例 15-23 的代码会编译通过，但测试会失败：

```console
$ cargo test
   Compiling limit-tracker v0.1.0 (file:///projects/limit-tracker)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.91s
     Running unittests src/lib.rs (target/debug/deps/limit_tracker-e599811fa246dbde)

running 1 test
test tests::it_sends_an_over_75_percent_warning_message ... FAILED

failures:

---- tests::it_sends_an_over_75_percent_warning_message stdout ----

thread 'tests::it_sends_an_over_75_percent_warning_message' (6028024) panicked at src/lib.rs:60:53:
RefCell already borrowed
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    tests::it_sends_an_over_75_percent_warning_message

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

error: test failed, to rerun pass `--lib`
```

　　注意代码以消息 `already borrowed: BorrowMutError` panic。这就是 `RefCell<T>` 在运行时处理借用规则违反的方式。

　　像这里这样选择在运行时而不是编译期捕获借用错误，意味着你可能在开发过程更晚才发现代码中的错误：或许要到代码部署到生产环境之后。此外，由于在运行时而不是编译期跟踪借用，代码会有一点运行时性能代价。不过，使用 `RefCell<T>` 使得可以写出这样的模拟对象：在只允许不可变值的上下文中使用它时，它仍能修改自身以记录见过的消息。尽管有这些权衡，你仍可使用 `RefCell<T>`，以获得比常规引用更多的功能。

### 允许多个所有者拥有可变数据

　　使用 `RefCell<T>` 的常见方式是与 `Rc<T>` 组合。回想一下：`Rc<T>` 让你对某些数据有多个所有者，但只提供对该数据的不可变访问。若有一个持有 `RefCell<T>` 的 `Rc<T>`，就可以得到既有多个所有者、又可修改的值！

　　例如，回想示例 15-18 中的 cons list：我们用 `Rc<T>` 让多个列表共享另一个列表的所有权。因为 `Rc<T>` 只持有不可变值，一旦创建列表就不能再改其中任何值。我们加入 `RefCell<T>`，以获得修改列表中值的能力。示例 15-24 展示：通过在 `Cons` 定义中使用 `RefCell<T>`，我们可以修改所有列表中存储的值。

**文件名：`src/main.rs`**

```rust
#[derive(Debug)]
enum List {
    Cons(Rc<RefCell<i32>>, Rc<List>),
    Nil,
}

use crate::List::{Cons, Nil};
use std::cell::RefCell;
use std::rc::Rc;

fn main() {
    let value = Rc::new(RefCell::new(5));

    let a = Rc::new(Cons(Rc::clone(&value), Rc::new(Nil)));

    let b = Cons(Rc::new(RefCell::new(3)), Rc::clone(&a));
    let c = Cons(Rc::new(RefCell::new(4)), Rc::clone(&a));

    *value.borrow_mut() += 10;

    println!("a after = {a:?}");
    println!("b after = {b:?}");
    println!("c after = {c:?}");
}
```

**示例 15-24**


　　我们创建一个 `Rc<RefCell<i32>>` 实例，存在名为 `value` 的变量中，以便稍后直接访问。然后在 `a` 中创建一个 `List`，其 `Cons` 变体持有 `value`。需要克隆 `value`，这样 `a` 与 `value` 都拥有内部的 `5`，而不是把所有权从 `value` 转移给 `a`，或让 `a` 从 `value` 借用。

　　我们把列表 `a` 包在 `Rc<T>` 里，这样创建列表 `b` 与 `c` 时它们都能引用 `a`，这与示例 15-18 中的做法相同。

　　创建完 `a`、`b`、`c` 中的列表后，我们想给 `value` 中的值加 10。做法是对 `value` 调用 `borrow_mut`：它利用第 5 章[「`->` 运算符去哪了？」](/trpl/structs/03-method-syntax/#wheres-the---operator)中讨论的自动解引用特性，把 `Rc<T>` 解引用为内部的 `RefCell<T>` 值。`borrow_mut` 方法返回 `RefMut<T>` 智能指针，我们对它使用解引用运算符并修改内部值。

　　打印 `a`、`b`、`c` 时，可以看到它们都有修改后的值 `15`，而不是 `5`：

```console
$ cargo run
   Compiling cons-list v0.1.0 (file:///projects/cons-list)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.63s
     Running `target/debug/cons-list`
a after = Cons(RefCell { value: 15 }, Nil)
b after = Cons(RefCell { value: 3 }, Cons(RefCell { value: 15 }, Nil))
c after = Cons(RefCell { value: 4 }, Cons(RefCell { value: 15 }, Nil))
```

　　这种技巧相当巧妙！通过使用 `RefCell<T>`，我们有一个外表不可变的 `List` 值。但可以利用 `RefCell<T>` 上提供内部可变性访问的方法，在需要时修改数据。借用规则的运行时检查保护我们免受数据竞争，有时为了数据结构上的这种灵活性，值得用一点速度来交换。注意：`RefCell<T>` 不能用于多线程代码！`Mutex<T>` 是 `RefCell<T>` 的线程安全版本，我们会在第 16 章讨论 `Mutex<T>`。

[wheres-the---operator]: /trpl/structs/03-method-syntax/#wheres-the---operator
