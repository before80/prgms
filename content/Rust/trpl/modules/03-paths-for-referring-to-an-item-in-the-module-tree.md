+++
title = "7.3 路径：引用模块树中的项"
date = 2026-08-05T08:44:00+08:00
weight = 30
type = "docs"
description = "用绝对路径与相对路径引用模块树中的项，并用 pub 控制可见性"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 路径：引用模块树中的项


> 原文链接: [https://doc.rust-lang.org/stable/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html](https://doc.rust-lang.org/stable/book/ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html)


## 路径：引用模块树中的项

　　要告诉 Rust 在模块树中哪里能找到某个项，我们使用路径，就像在文件系统里导航时使用路径一样。要调用一个函数，就需要知道它的路径。

　　路径可以有两种形式：

- *绝对路径*（absolute path）是从 crate 根开始的完整路径；对于外部 crate 中的代码，绝对路径以 crate 名开头，对于当前 crate 中的代码，则以字面量 `crate` 开头。
- *相对路径*（relative path）从当前模块开始，并使用 `self`、`super`，或当前模块中的一个标识符。

　　绝对路径和相对路径后面都跟着一个或多个由双冒号（`::`）分隔的标识符。

　　回到示例 7-1，假设我们想调用 `add_to_waitlist` 函数。这等价于问：`add_to_waitlist` 函数的路径是什么？示例 7-3 在示例 7-1 的基础上删去了部分模块和函数。

　　我们将展示从定义在 crate 根的新函数 `eat_at_restaurant` 中调用 `add_to_waitlist` 的两种方式。这些路径本身是正确的，但还有另一个问题会阻止这个例子按现状编译。我们稍后解释原因。

　　`eat_at_restaurant` 函数是我们库 crate 公共 API 的一部分，因此用 `pub` 关键字标记它。在[「用 `pub` 关键字公开路径」][pub]一节中，我们会更详细地讨论 `pub`。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    mod hosting {
        fn add_to_waitlist() {}
    }
}

pub fn eat_at_restaurant() {
    // Absolute path
    crate::front_of_house::hosting::add_to_waitlist();

    // Relative path
    front_of_house::hosting::add_to_waitlist();
}
```

**示例 7-3：使用绝对路径和相对路径调用 `add_to_waitlist` 函数**

　　在 `eat_at_restaurant` 中第一次调用 `add_to_waitlist` 时，我们使用绝对路径。`add_to_waitlist` 与 `eat_at_restaurant` 定义在同一个 crate 中，因此可以用 `crate` 关键字开始一条绝对路径。然后依次包含各个模块，直到到达 `add_to_waitlist`。你可以想象一个结构相同的文件系统：要运行 `add_to_waitlist` 程序，我们会指定路径 `/front_of_house/hosting/add_to_waitlist`；用 `crate` 名从 crate 根开始，就像在 shell 里用 `/` 从文件系统根开始。

　　第二次在 `eat_at_restaurant` 中调用 `add_to_waitlist` 时，我们使用相对路径。路径以 `front_of_house` 开头，它是与 `eat_at_restaurant` 定义在模块树同一层级的模块名。对应的文件系统等价物是使用路径 `front_of_house/hosting/add_to_waitlist`。以模块名开头意味着这是相对路径。

　　选择使用相对路径还是绝对路径，取决于你的项目，也取决于你更可能把项的定义代码与使用它的代码分开移动，还是一起移动。例如，若我们把 `front_of_house` 模块和 `eat_at_restaurant` 函数都移进名为 `customer_experience` 的模块，就需要更新指向 `add_to_waitlist` 的绝对路径，但相对路径仍然有效。然而，若我们单独把 `eat_at_restaurant` 函数移进名为 `dining` 的模块，指向 `add_to_waitlist` 调用的绝对路径会保持不变，相对路径则需要更新。我们大体上更倾向指定绝对路径，因为更常见的情况是我们希望独立地移动代码定义与项的调用位置。

　　让我们试着编译示例 7-3，看看它为什么还不能编译！得到的错误如示例 7-4 所示。

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0603]: module `hosting` is private
 --> src/lib.rs:9:28
  |
9 |     crate::front_of_house::hosting::add_to_waitlist();
  |                            ^^^^^^^  --------------- function `add_to_waitlist` is not publicly re-exported
  |                            |
  |                            private module
  |
note: the module `hosting` is defined here
 --> src/lib.rs:2:5
  |
2 |     mod hosting {
  |     ^^^^^^^^^^^

error[E0603]: module `hosting` is private
  --> src/lib.rs:12:21
   |
12 |     front_of_house::hosting::add_to_waitlist();
   |                     ^^^^^^^  --------------- function `add_to_waitlist` is not publicly re-exported
   |                     |
   |                     private module
   |
note: the module `hosting` is defined here
  --> src/lib.rs:2:5
   |
 2 |     mod hosting {
   |     ^^^^^^^^^^^

For more information about this error, try `rustc --explain E0603`.
error: could not compile `restaurant` (lib) due to 2 previous errors
```

**示例 7-4：构建示例 7-3 中的代码时的编译器错误**

　　错误信息说模块 `hosting` 是私有的。换句话说，我们指向 `hosting` 模块和 `add_to_waitlist` 函数的路径是正确的，但 Rust 不允许我们使用它们，因为无法访问这些私有部分。在 Rust 中，所有项（函数、方法、结构体、枚举、模块和常量）默认对其父模块是私有的。若想让函数或结构体这类项变成私有的，就把它放进模块里。

　　父模块中的项不能使用子模块内的私有项，但子模块中的项可以使用其祖先模块中的项。这是因为子模块会包装并隐藏自己的实现细节，但子模块能看见自己被定义时所处的上下文。继续用我们的比喻：可以把私有性规则想成餐馆的后台办公室——那里发生的事对顾客是私密的，但办公室经理可以看到并处理他们经营的餐馆里的一切。

　　Rust 选择让模块系统以这种方式工作，是为了默认隐藏内部实现细节。这样，你就知道哪些内部代码可以改动而不破坏外部代码。不过，Rust 也允许你用 `pub` 关键字把项设为公有，从而把子模块内部的一部分代码暴露给外部的祖先模块。

### 用 `pub` 关键字公开路径 {#exposing-paths-with-the-pub-keyword}

　　回到示例 7-4 中告诉我们 `hosting` 模块是私有的那个错误。我们希望父模块中的 `eat_at_restaurant` 函数能访问子模块中的 `add_to_waitlist` 函数，因此给 `hosting` 模块加上 `pub` 关键字，如示例 7-5 所示。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        fn add_to_waitlist() {}
    }
}

// -- snip --
```

**示例 7-5：将 `hosting` 模块声明为 `pub`，以便从 `eat_at_restaurant` 中使用它**

　　不幸的是，示例 7-5 中的代码仍然会产生编译器错误，如示例 7-6 所示。

```console
$ cargo build
   Compiling restaurant v0.1.0 (file:///projects/restaurant)
error[E0603]: function `add_to_waitlist` is private
  --> src/lib.rs:10:37
   |
10 |     crate::front_of_house::hosting::add_to_waitlist();
   |                                     ^^^^^^^^^^^^^^^ private function
   |
note: the function `add_to_waitlist` is defined here
  --> src/lib.rs:3:9
   |
 3 |         fn add_to_waitlist() {}
   |         ^^^^^^^^^^^^^^^^^^^^

error[E0603]: function `add_to_waitlist` is private
  --> src/lib.rs:13:30
   |
13 |     front_of_house::hosting::add_to_waitlist();
   |                              ^^^^^^^^^^^^^^^ private function
   |
note: the function `add_to_waitlist` is defined here
  --> src/lib.rs:3:9
   |
 3 |         fn add_to_waitlist() {}
   |         ^^^^^^^^^^^^^^^^^^^^

For more information about this error, try `rustc --explain E0603`.
error: could not compile `restaurant` (lib) due to 2 previous errors
```

**示例 7-6：构建示例 7-5 中的代码时的编译器错误**

　　发生了什么？在 `mod hosting` 前面加上 `pub` 关键字使该模块变为公有。有了这一改动，只要我们能访问 `front_of_house`，就能访问 `hosting`。但 `hosting` 的*内容*仍然是私有的；让模块公有并不会让其内容也公有。模块上的 `pub` 关键字只允许祖先模块中的代码引用该模块，而不能访问其内部代码。因为模块是容器，仅仅让模块公有能做的事并不多；我们还需要更进一步，选择让模块内的一个或多个项也变为公有。

　　示例 7-6 中的错误说 `add_to_waitlist` 函数是私有的。私有性规则同样适用于结构体、枚举、函数和方法，以及模块。

　　让我们也给 `add_to_waitlist` 函数加上 `pub`，在其定义前添加该关键字，如示例 7-7 所示。

**文件名：`src/lib.rs`**
```rust
mod front_of_house {
    pub mod hosting {
        pub fn add_to_waitlist() {}
    }
}

// -- snip --
```

**示例 7-7：给 `mod hosting` 和 `fn add_to_waitlist` 加上 `pub` 关键字后，就可以从 `eat_at_restaurant` 调用该函数。**

　　现在代码可以编译了！为了弄清加上 `pub` 之后，为何这些路径在 `eat_at_restaurant` 中相对于私有性规则可用，我们来看看绝对路径和相对路径。

　　在绝对路径中，我们从 `crate`（crate 模块树的根）开始。`front_of_house` 模块定义在 crate 根中。虽然 `front_of_house` 不是公有的，但因为 `eat_at_restaurant` 与 `front_of_house` 定义在同一模块中（也就是说，两者是同级模块），所以我们可以从 `eat_at_restaurant` 引用 `front_of_house`。接下来是标了 `pub` 的 `hosting` 模块。我们能访问 `hosting` 的父模块，因此也能访问 `hosting`。最后，`add_to_waitlist` 函数标了 `pub`，且我们能访问其父模块，所以这次函数调用可以成功！

　　在相对路径中，逻辑与绝对路径相同，只是第一步不同：路径不是从 crate 根开始，而是从 `front_of_house` 开始。`front_of_house` 与 `eat_at_restaurant` 定义在同一模块中，因此从定义 `eat_at_restaurant` 的模块出发的相对路径有效。然后，因为 `hosting` 和 `add_to_waitlist` 都标了 `pub`，路径的其余部分也有效，这次函数调用合法！

　　若你打算共享自己的库 crate，好让其他项目使用你的代码，那么公共 API 就是你与 crate 用户之间的契约，决定了他们如何与你的代码交互。围绕如何管理公共 API 的变更、以便他人更容易依赖你的 crate，有许多需要考虑的事项。这些超出了本书范围；若你对此感兴趣，请参阅 [Rust API Guidelines][api-guidelines]。

> #### 同时包含二进制与库的包的最佳实践
>
> 我们提到过，一个包可以同时包含 *src/main.rs* 二进制 crate 根和 *src/lib.rs* 库 crate 根，且默认两者都使用包名。通常，采用这种「既有库又有二进制」模式的包，二进制 crate 里只会放刚好够启动可执行文件的代码，并调用库 crate 中定义的代码。这样其他项目就能受益于该包提供的大部分功能，因为库 crate 的代码可以被共享。
>
> 模块树应定义在 *src/lib.rs* 中。然后，二进制 crate 中任何公有项都可以通过以包名开头的路径来使用。二进制 crate 会像完全外部的 crate 那样成为库 crate 的用户：它只能使用公共 API。这有助于你设计良好的 API——你既是作者，也是客户！
>
> 在[第 12 章][ch12]中，我们会用一个同时包含二进制 crate 和库 crate 的命令行程序来演示这种组织方式。

### 以 `super` 开始相对路径

　　我们可以构造从父模块（而不是当前模块或 crate 根）开始的相对路径，方法是在路径开头使用 `super`。这类似文件系统路径以 `..` 开头，表示进入父目录。使用 `super` 可以引用我们知道位于父模块中的项；当某个模块与父模块关系紧密、但父模块将来可能被挪到模块树别处时，这能让重组模块树更容易。

　　看看示例 7-8 中的代码，它模拟厨师修正错误订单并亲自把菜送到顾客面前的情形。定义在 `back_of_house` 模块中的函数 `fix_incorrect_order`，通过以 `super` 开头的路径调用定义在父模块中的 `deliver_order`。

**文件名：`src/lib.rs`**
```rust
fn deliver_order() {}

mod back_of_house {
    fn fix_incorrect_order() {
        cook_order();
        super::deliver_order();
    }

    fn cook_order() {}
}
```

**示例 7-8：使用以 `super` 开头的相对路径调用函数**

　　`fix_incorrect_order` 函数在 `back_of_house` 模块中，因此我们可以用 `super` 进入 `back_of_house` 的父模块，此例中就是根模块 `crate`。从那里查找 `deliver_order` 并找到它。成功！我们认为 `back_of_house` 模块与 `deliver_order` 函数很可能保持这种相对关系，若我们决定重组 crate 的模块树，它们也会一起移动。因此我们使用了 `super`，这样将来这段代码被挪到不同模块时，需要更新的地方会更少。

### 使结构体和枚举公有

　　我们也可以用 `pub` 把结构体和枚举标为公有，但对它们使用 `pub` 时还有一些额外细节。若在结构体定义前使用 `pub`，结构体本身会变成公有，但其字段仍然是私有的。我们可以逐个决定每个字段是否公有。在示例 7-9 中，我们定义了一个公有的 `back_of_house::Breakfast` 结构体，其中 `toast` 字段公有，`seasonal_fruit` 字段私有。这模拟了餐馆里顾客可以选择配餐面包种类，但厨师根据当季与库存决定配什么水果的情形。可用的水果变化很快，因此顾客不能选择水果，甚至看不到会得到什么水果。

**文件名：`src/lib.rs`**
```rust
mod back_of_house {
    pub struct Breakfast {
        pub toast: String,
        seasonal_fruit: String,
    }

    impl Breakfast {
        pub fn summer(toast: &str) -> Breakfast {
            Breakfast {
                toast: String::from(toast),
                seasonal_fruit: String::from("peaches"),
            }
        }
    }
}

pub fn eat_at_restaurant() {
    // Order a breakfast in the summer with Rye toast.
    let mut meal = back_of_house::Breakfast::summer("Rye");
    // Change our mind about what bread we'd like.
    meal.toast = String::from("Wheat");
    println!("I'd like {} toast please", meal.toast);

    // The next line won't compile if we uncomment it; we're not allowed
    // to see or modify the seasonal fruit that comes with the meal.
    // meal.seasonal_fruit = String::from("blueberries");
}
```

**示例 7-9：部分字段公有、部分字段私有的结构体**

　　因为 `back_of_house::Breakfast` 结构体中的 `toast` 字段是公有的，在 `eat_at_restaurant` 里我们可以用点号读写 `toast` 字段。注意我们不能在 `eat_at_restaurant` 中使用 `seasonal_fruit` 字段，因为它是私有的。试着取消注释修改 `seasonal_fruit` 字段值的那一行，看看会得到什么错误！

　　另外注意，因为 `back_of_house::Breakfast` 有一个私有字段，该结构体需要提供一个公有的关联函数来构造 `Breakfast` 实例（这里我们把它命名为 `summer`）。若 `Breakfast` 没有这样的函数，我们就无法在 `eat_at_restaurant` 中创建 `Breakfast` 实例，因为无法在那里设置私有字段 `seasonal_fruit` 的值。

　　相比之下，若我们把枚举设为公有，它的所有变体就都是公有的。我们只需在 `enum` 关键字前加 `pub`，如示例 7-10 所示。

**文件名：`src/lib.rs`**
```rust
mod back_of_house {
    pub enum Appetizer {
        Soup,
        Salad,
    }
}

pub fn eat_at_restaurant() {
    let order1 = back_of_house::Appetizer::Soup;
    let order2 = back_of_house::Appetizer::Salad;
}
```

**示例 7-10：把枚举标为公有会使其所有变体都变为公有。**

　　因为我们把 `Appetizer` 枚举设为了公有，就可以在 `eat_at_restaurant` 中使用 `Soup` 和 `Salad` 变体。

　　除非变体是公有的，否则枚举用处不大；若每次都要给所有枚举变体加 `pub` 会很烦人，因此枚举变体的默认就是公有。结构体即使字段不公有也常常很有用，因此结构体字段遵循「默认全部私有，除非标注 `pub`」的一般规则。

　　还有一种涉及 `pub` 的情形我们尚未讲到，那就是模块系统的最后一个特性：`use` 关键字。我们会先单独讲 `use`，然后再展示如何把 `pub` 与 `use` 结合起来。

[pub]: #exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: /trpl/an-io-project/
