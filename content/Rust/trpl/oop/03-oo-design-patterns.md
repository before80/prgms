+++
title = "18.3 实现面向对象设计模式"
date = 2026-08-05T08:44:00+08:00
weight = 89
type = "docs"
description = "用状态模式实现博客帖子工作流，并对比类型编码状态的惯用做法"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 实现面向对象设计模式


> 原文链接: [https://doc.rust-lang.org/stable/book/ch18-03-oo-design-patterns.html](https://doc.rust-lang.org/stable/book/ch18-03-oo-design-patterns.html)


## 实现面向对象设计模式

　　*状态模式*（state pattern）是一种面向对象设计模式。该模式的核心是：我们定义一个值在内部可以具有的一组状态。这些状态由一组*状态对象*表示，值的行为随其状态而变。我们将通过一个博客帖子结构体的例子逐步推进：该结构体有一个字段保存其状态，状态对象来自集合「草稿」「审阅」或「已发布」。

　　状态对象共享功能：在 Rust 中，我们当然使用结构体与 trait，而不是对象与继承。每个状态对象负责自己的行为，并负责管理何时应转变到另一状态。持有状态对象的值对状态的不同行为或何时在状态之间转换一无所知。

　　使用状态模式的优势是：当程序的业务需求变化时，我们不必改动持有状态的值的代码，也不必改动使用该值的代码。我们只需更新某个状态对象内部的代码以改变其规则，或也许添加更多状态对象。

　　首先，我们将以更传统的面向对象方式实现状态模式。然后，我们会使用一种在 Rust 中更自然一些的做法。让我们动手，用状态模式逐步实现博客帖子工作流。

　　最终功能如下：

1. 博客帖子从空草稿开始。
1. 草稿完成后，请求对帖子进行审阅。
1. 帖子获批后即发布。
1. 只有已发布的博客帖子才会返回可供打印的内容，这样未批准的帖子就不会被意外发布。

　　对帖子尝试的任何其他更改都应没有效果。例如，若我们在请求审阅之前就试图批准一份草稿博客帖子，该帖子应仍保持为未发布的草稿。

### 尝试传统面向对象风格

　　解决同一问题有无数种组织代码的方式，各自有不同取舍。本节的实现更偏传统面向对象风格：在 Rust 中可以这样写，但没有发挥 Rust 的一些优势。稍后我们会演示另一种仍使用面向对象设计模式、但对有面向对象经验的程序员可能看起来不那么熟悉的结构化方式。我们将比较这两种方案，以体验以不同于其他语言的方式设计 Rust 代码时的取舍。

　　示例 18-11 以代码形式展示了这一工作流：这是我们将在名为 `blog` 的库 crate 中实现的 API 的示例用法。目前还不能编译，因为我们尚未实现 `blog` crate。

**文件名：`src/main.rs`**
```rust
use blog::Post;

fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");
    assert_eq!("", post.content());

    post.request_review();
    assert_eq!("", post.content());

    post.approve();
    assert_eq!("I ate a salad for lunch today", post.content());
}
```

**示例 18-11：演示我们希望 `blog` crate 具备的期望行为的代码**

　　我们希望允许用户用 `Post::new` 创建新的草稿博客帖子。我们希望允许向博客帖子添加文本。若我们在批准之前立刻尝试获取帖子内容，不应得到任何文本，因为帖子仍是草稿。我们在代码中加入了 `assert_eq!` 以便演示。对此的出色单元测试会断言草稿博客帖子的 `content` 方法返回空字符串，但本例不写测试。

　　接下来，我们希望能请求对帖子进行审阅，并希望在等待审阅期间 `content` 仍返回空字符串。当帖子收到批准时，它应被发布，意味着调用 `content` 时会返回帖子的文本。

　　注意我们从该 crate 交互的唯一类型是 `Post` 类型。该类型将使用状态模式，并持有一个值，该值将是表示帖子可能处于的各种状态——草稿、审阅或已发布——的三个状态对象之一。从一种状态变到另一种将在 `Post` 类型内部管理。状态会响应我们库用户在 `Post` 实例上调用的方法而改变，但他们不必直接管理状态变化。此外，用户也不会在状态上犯错，例如在审阅之前就发布帖子。

#### 定义 `Post` 并创建新实例

　　开始实现这个库吧！我们知道需要一个公共的 `Post` 结构体来保存一些内容，因此从结构体定义以及用于创建 `Post` 实例的关联公共函数 `new` 开始，如示例 18-12 所示。我们还会做一个私有的 `State` trait，定义所有用于 `Post` 的状态对象必须具备的行为。

　　然后，`Post` 会在名为 `state` 的私有字段中、在 `Option<T>` 内持有 `Box<dyn State>` 的 trait 对象以保存状态对象。稍后你会看到为何需要 `Option<T>`。

**文件名：`src/lib.rs`**
```rust
pub struct Post {
    state: Option<Box<dyn State>>,
    content: String,
}

impl Post {
    pub fn new() -> Post {
        Post {
            state: Some(Box::new(Draft {})),
            content: String::new(),
        }
    }
}

trait State {}

struct Draft {}

impl State for Draft {}
```

**示例 18-12：`Post` 结构体与创建新 `Post` 实例的 `new` 函数、`State` trait 以及 `Draft` 结构体的定义**

　　`State` trait 定义了不同帖子状态共享的行为。状态对象是 `Draft`、`PendingReview` 与 `Published`，它们都将实现 `State` trait。目前该 trait 还没有任何方法；我们先只定义 `Draft` 状态，因为那是我们希望帖子起始所处的状态。

　　创建新 `Post` 时，我们把它的 `state` 字段设为持有一个 `Box` 的 `Some` 值。这个 `Box` 指向 `Draft` 结构体的新实例。这确保每当我们创建新的 `Post` 实例时，它都会从草稿开始。因为 `Post` 的 `state` 字段是私有的，没有办法在任何其他状态下创建 `Post`！在 `Post::new` 函数中，我们把 `content` 字段设为新的空 `String`。

#### 存储帖子内容的文本

　　我们在示例 18-11 中看到，希望能调用名为 `add_text` 的方法并传入 `&str`，然后把它添加为博客帖子的文本内容。我们把它实现为方法，而不是把 `content` 字段暴露为 `pub`，以便稍后可以实现控制如何读取 `content` 字段数据的方法。`add_text` 方法相当直接，因此我们把实现加到示例 18-13 的 `impl Post` 块中。

**文件名：`src/lib.rs`**
```rust
impl Post {
    // --snip--

    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }
}
```

**示例 18-13：实现 `add_text` 方法以向帖子的 `content` 添加文本**

　　`add_text` 方法接受对 `self` 的可变引用，因为我们在改变调用 `add_text` 的那个 `Post` 实例。然后我们对 `content` 中的 `String` 调用 `push_str`，并传入 `text` 参数以添加到已保存的 `content`。这一行为不依赖于帖子所处的状态，因此它不是状态模式的一部分。`add_text` 方法完全不与 `state` 字段交互，但它是我们希望支持的行为的一部分。

#### 确保草稿帖子的内容为空

　　即便我们已经调用 `add_text` 并向帖子添加了一些内容，我们仍希望 `content` 方法返回空字符串切片，因为帖子仍处于草稿状态，正如示例 18-11 中第一个 `assert_eq!` 所示。目前，我们用能满足这一要求的最简单做法实现 `content` 方法：总是返回空字符串切片。等我们实现改变帖子状态以便可以发布的能力后再改。到目前为止帖子只能处于草稿状态，因此帖子内容应始终为空。示例 18-14 展示了这一占位实现。

**文件名：`src/lib.rs`**
```rust
impl Post {
    // --snip--

    pub fn content(&self) -> &str {
        ""
    }
}
```

**示例 18-14：为 `Post` 上的 `content` 方法添加总是返回空字符串切片的占位实现**

　　有了这个新增的 `content` 方法，示例 18-11 中直到第一个 `assert_eq!` 的一切都能按预期工作。

#### 请求审阅，从而改变帖子状态

　　接下来，我们需要添加请求审阅帖子的功能，这应把它的状态从 `Draft` 变为 `PendingReview`。示例 18-15 展示了这段代码。

**文件名：`src/lib.rs`**
```rust
impl Post {
    // --snip--

    pub fn request_review(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.request_review())
        }
    }
}

trait State {
    fn request_review(self: Box<Self>) -> Box<dyn State>;
}

struct Draft {}

impl State for Draft {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        Box::new(PendingReview {})
    }
}

struct PendingReview {}

impl State for PendingReview {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }
}
```

**示例 18-15：在 `Post` 与 `State` trait 上实现 `request_review` 方法**

　　我们给 `Post` 一个名为 `request_review` 的公共方法，它接受对 `self` 的可变引用。然后我们对 `Post` 的当前状态调用内部的 `request_review` 方法，而这第二个 `request_review` 方法会消费当前状态并返回新状态。

　　我们把 `request_review` 方法加到 `State` trait；现在所有实现该 trait 的类型都需要实现 `request_review` 方法。注意该方法的第一个参数不是 `self`、`&self` 或 `&mut self`，而是 `self: Box<Self>`。这一语法意味着该方法只有在对持有该类型的 `Box` 调用时才有效。这一语法取得 `Box<Self>` 的所有权，使旧状态失效，以便 `Post` 的状态值可以转变成新状态。

　　要消费旧状态，`request_review` 方法需要取得状态值的所有权。这就是 `Post` 的 `state` 字段中的 `Option` 派上用场的地方：我们调用 `take` 方法从 `state` 字段取出 `Some` 值，并在原处留下 `None`，因为 Rust 不允许结构体中有未填充的字段。这让我们把 `state` 值移出 `Post` 而不是借用它。然后我们会把帖子的 `state` 值设为这次操作的结果。

　　我们需要暂时把 `state` 设为 `None`，而不是用类似 `self.state = self.state.request_review();` 的代码直接设置它，以便取得 `state` 值的所有权。这确保在我们把它转变成新状态之后，`Post` 不能再使用旧的 `state` 值。

　　`Draft` 上的 `request_review` 方法返回一个新的、装箱的 `PendingReview` 结构体实例，它表示帖子正在等待审阅时的状态。`PendingReview` 结构体也实现了 `request_review` 方法，但不做任何转变。相反，它返回自身，因为当我们在已处于 `PendingReview` 状态的帖子上请求审阅时，它应停留在 `PendingReview` 状态。

　　现在我们可以开始看到状态模式的优势：`Post` 上的 `request_review` 方法无论其 `state` 值如何都相同。每个状态负责自己的规则。

　　我们把 `Post` 上的 `content` 方法保持原样，返回空字符串切片。现在我们可以有处于 `PendingReview` 状态以及 `Draft` 状态的 `Post`，但我们希望在 `PendingReview` 状态下有相同行为。示例 18-11 现在可以工作到第二个 `assert_eq!` 调用！

#### 添加 `approve` 以改变 `content` 的行为

　　`approve` 方法将与 `request_review` 方法类似：它会把 `state` 设为当前状态在被批准时应具有的值，如示例 18-16 所示。

**文件名：`src/lib.rs`**
```rust
impl Post {
    // --snip--

    pub fn approve(&mut self) {
        if let Some(s) = self.state.take() {
            self.state = Some(s.approve())
        }
    }
}

trait State {
    fn request_review(self: Box<Self>) -> Box<dyn State>;
    fn approve(self: Box<Self>) -> Box<dyn State>;
}

struct Draft {}

impl State for Draft {
    // --snip--

    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }
}

struct PendingReview {}

impl State for PendingReview {
    // --snip--

    fn approve(self: Box<Self>) -> Box<dyn State> {
        Box::new(Published {})
    }
}

struct Published {}

impl State for Published {
    fn request_review(self: Box<Self>) -> Box<dyn State> {
        self
    }

    fn approve(self: Box<Self>) -> Box<dyn State> {
        self
    }
}
```

**示例 18-16：在 `Post` 与 `State` trait 上实现 `approve` 方法**

　　我们把 `approve` 方法加到 `State` trait，并添加一个实现 `State` 的新结构体——`Published` 状态。

　　与 `PendingReview` 上的 `request_review` 工作方式类似，若我们对 `Draft` 调用 `approve` 方法，它不会有效果，因为 `approve` 会返回 `self`。当我们在 `PendingReview` 上调用 `approve` 时，它返回一个新的、装箱的 `Published` 结构体实例。`Published` 结构体实现了 `State` trait，并且对 `request_review` 方法与 `approve` 方法都返回自身，因为在那些情况下帖子应停留在 `Published` 状态。

　　现在我们需要更新 `Post` 上的 `content` 方法。我们希望从 `content` 返回的值取决于 `Post` 的当前状态，因此我们将让 `Post` 委托给在其 `state` 上定义的 `content` 方法，如示例 18-17 所示。

**文件名：`src/lib.rs`**
```rust
impl Post {
    // --snip--

    pub fn content(&self) -> &str {
        self.state.as_ref().unwrap().content(self)
    }
    // --snip--

}
```

**示例 18-17：更新 `Post` 上的 `content` 方法以委托给 `State` 上的 `content` 方法**

　　因为目标是把所有这些规则都保持在实现 `State` 的结构体内部，我们对 `state` 中的值调用 `content` 方法，并把帖子实例（也就是 `self`）作为参数传入。然后返回对 `state` 值使用 `content` 方法所返回的值。

　　我们在 `Option` 上调用 `as_ref` 方法，因为我们想要的是对 `Option` 内值的引用，而不是该值的所有权。因为 `state` 是 `Option<Box<dyn State>>`，调用 `as_ref` 时会返回 `Option<&Box<dyn State>>`。若不调用 `as_ref`，我们会得到错误，因为不能把 `state` 移出函数参数中借用的 `&self`。

　　然后我们调用 `unwrap` 方法，我们知道它永远不会 panic，因为我们知道 `Post` 上的方法会确保那些方法结束时 `state` 总是包含 `Some` 值。这是我们在第 9 章[「当你比编译器掌握更多信息时」][more-info-than-rustc]一节中谈过的情形之一：我们知道 `None` 值绝不可能出现，即便编译器无法理解这一点。

　　此时，当我们在 `&Box<dyn State>` 上调用 `content` 时，解引用强制转换会作用于 `&` 与 `Box`，使得最终会在实现了 `State` trait 的类型上调用 `content` 方法。这意味着我们需要把 `content` 加到 `State` trait 定义中，并在那里放入根据所处状态返回何种内容的逻辑，如示例 18-18 所示。

**文件名：`src/lib.rs`**
```rust
trait State {
    // --snip--

    fn content<'a>(&self, post: &'a Post) -> &'a str {
        ""
    }
}

// --snip--

struct Published {}

impl State for Published {
    // --snip--

    fn content<'a>(&self, post: &'a Post) -> &'a str {
        &post.content
    }
}
```

**示例 18-18：向 `State` trait 添加 `content` 方法**

　　我们为 `content` 方法添加返回空字符串切片的默认实现。这意味着我们不必在 `Draft` 与 `PendingReview` 结构体上实现 `content`。`Published` 结构体会覆盖 `content` 方法并返回 `post.content` 中的值。虽然方便，但让 `State` 上的 `content` 方法决定 `Post` 的内容，正在模糊 `State` 的职责与 `Post` 的职责之间的界限。

　　注意我们需要在该方法上加生命周期注解，正如第 10 章所讨论的。我们把对 `post` 的引用作为参数，并返回对该 `post` 一部分的引用，因此返回引用的生命周期与 `post` 参数的生命周期相关。

　　我们完成了——示例 18-11 现在全部可以工作！我们用博客帖子工作流的规则实现了状态模式。与规则相关的逻辑住在状态对象中，而不是散落在整个 `Post` 里。

> ### 为何不用枚举？
>
> 你可能在想为何我们不用以不同可能帖子状态为变体的枚举。那当然也是可行方案；试一试并比较最终结果，看你更喜欢哪一种！使用枚举的一个缺点是：每一处检查枚举值的地方都需要 `match` 表达式或类似物来处理每个可能变体。这可能比这种 trait 对象方案更重复。

#### 评估状态模式

　　我们已经展示 Rust 有能力实现面向对象状态模式，以封装帖子在每种状态下应有的不同行为。`Post` 上的方法对各种行为一无所知。因为我们组织代码的方式，要了解已发布帖子可以有哪些不同行为，只需看一个地方：`Published` 结构体上对 `State` trait 的实现。

　　若我们创建不使用状态模式的替代实现，可能会改为在 `Post` 的方法中、甚至在检查帖子状态并在那些地方改变行为的 `main` 代码中使用 `match` 表达式。那就意味着我们要看好几处地方才能理解帖子处于已发布状态的全部含义。

　　有了状态模式，`Post` 的方法以及我们使用 `Post` 的地方都不需要 `match` 表达式；而要添加新状态，我们只需添加一个新结构体，并在那一处对该结构体实现 trait 方法。

　　使用状态模式的实现很容易扩展以添加更多功能。为体会维护使用状态模式的代码有多简单，试试这些建议中的几条：

- 添加 `reject` 方法，把帖子状态从 `PendingReview` 改回 `Draft`。
- 要求调用两次 `approve` 后状态才能变为 `Published`。
- 仅当帖子处于 `Draft` 状态时才允许用户添加文本内容。提示：让状态对象负责内容可能发生何种变化，但不负责修改 `Post`。

　　状态模式的一个缺点是：因为状态实现状态之间的转换，有些状态彼此耦合。若我们在 `PendingReview` 与 `Published` 之间再加一个状态，例如 `Scheduled`，就必须改动 `PendingReview` 中的代码，使其转为 `Scheduled`。若添加新状态时 `PendingReview` 不必改动，工作量会更少，但这意味着要切换到另一种设计模式。

　　另一个缺点是我们重复了一些逻辑。为消除部分重复，我们可能尝试为 `State` trait 上的 `request_review` 与 `approve` 方法做返回 `self` 的默认实现。不过这行不通：当把 `State` 用作 trait 对象时，trait 并不确切知道具体的 `self` 会是什么，因此返回类型在编译期未知。（这是前面提到的 dyn 兼容性规则之一。）

　　其他重复还包括 `Post` 上 `request_review` 与 `approve` 方法相似的实现。两个方法都对 `Post` 的 `state` 字段使用 `Option::take`，若 `state` 是 `Some`，它们就委托给被包装值上同名方法的实现，并把 `state` 字段的新值设为结果。若 `Post` 上有很多遵循这一模式的方法，我们可能考虑定义宏来消除重复（见第 20 章[「宏」][macros]一节）。

　　通过完全按面向对象语言所定义的方式实现状态模式，我们没有尽可能充分发挥 Rust 的优势。让我们看看可以对 `blog` crate 做哪些改动，以便把非法状态与转换变成编译期错误。

### 把状态与行为编码为类型 {#encoding-states-and-behavior-as-types}

　　我们将展示如何重新思考状态模式以获得另一套取舍。不是把状态与转换完全封装起来使外部代码对其一无所知，而是把状态编码到不同的类型中。于是 Rust 的类型检查系统会在我们试图在只允许已发布帖子的地方使用草稿帖子时，通过发出编译器错误来阻止。

　　看看示例 18-11 中 `main` 的第一部分：

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");
    assert_eq!("", post.content());

}
```

　　我们仍然支持用 `Post::new` 在草稿状态下创建新帖子，以及向帖子内容添加文本的能力。但不是在草稿帖子上有一个返回空字符串的 `content` 方法，而是让草稿帖子根本没有 `content` 方法。这样，若我们试图获取草稿帖子的内容，会得到告诉该方法不存在的编译器错误。结果是，我们不可能在生产中意外显示草稿帖子内容，因为那段代码甚至无法编译。示例 18-19 展示了 `Post` 结构体与 `DraftPost` 结构体的定义，以及各自的方法。

**文件名：`src/lib.rs`**
```rust
pub struct Post {
    content: String,
}

pub struct DraftPost {
    content: String,
}

impl Post {
    pub fn new() -> DraftPost {
        DraftPost {
            content: String::new(),
        }
    }

    pub fn content(&self) -> &str {
        &self.content
    }
}

impl DraftPost {
    pub fn add_text(&mut self, text: &str) {
        self.content.push_str(text);
    }
}
```

**示例 18-19：带有 `content` 方法的 `Post` 与不带 `content` 方法的 `DraftPost`**

　　`Post` 与 `DraftPost` 结构体都有私有的 `content` 字段来存储博客帖子文本。这些结构体不再有 `state` 字段，因为我们正把状态的编码移到结构体的类型上。`Post` 结构体将表示已发布的帖子，并有返回 `content` 的 `content` 方法。

　　我们仍然有 `Post::new` 函数，但它不再返回 `Post` 实例，而是返回 `DraftPost` 实例。因为 `content` 是私有的，且没有任何函数返回 `Post`，目前不可能创建 `Post` 实例。

　　`DraftPost` 结构体有 `add_text` 方法，因此我们可以像以前一样向 `content` 添加文本，但注意 `DraftPost` 没有定义 `content` 方法！于是程序现在确保所有帖子都从草稿帖子开始，且草稿帖子的内容不可供显示。任何试图绕过这些约束的做法都会导致编译器错误。

　　那么，我们如何得到已发布的帖子？我们希望强制执行这样的规则：草稿帖子必须经过审阅与批准才能发布。处于待审阅状态的帖子仍不应显示任何内容。我们通过添加另一个结构体 `PendingReviewPost`、在 `DraftPost` 上定义返回 `PendingReviewPost` 的 `request_review` 方法，以及在 `PendingReviewPost` 上定义返回 `Post` 的 `approve` 方法，来实现这些约束，如示例 18-20 所示。

**文件名：`src/lib.rs`**
```rust
impl DraftPost {
    // --snip--

    pub fn request_review(self) -> PendingReviewPost {
        PendingReviewPost {
            content: self.content,
        }
    }
}

pub struct PendingReviewPost {
    content: String,
}

impl PendingReviewPost {
    pub fn approve(self) -> Post {
        Post {
            content: self.content,
        }
    }
}
```

**示例 18-20：通过对 `DraftPost` 调用 `request_review` 创建的 `PendingReviewPost`，以及把 `PendingReviewPost` 变为已发布 `Post` 的 `approve` 方法**

　　`request_review` 与 `approve` 方法取得 `self` 的所有权，从而消费 `DraftPost` 与 `PendingReviewPost` 实例，并分别把它们转变成 `PendingReviewPost` 与已发布的 `Post`。这样，在我们对它们调用 `request_review` 之后就不会再有残留的 `DraftPost` 实例，依此类推。`PendingReviewPost` 结构体上也没有定义 `content` 方法，因此试图读取其内容会像对 `DraftPost` 一样导致编译器错误。因为获得定义了 `content` 方法的已发布 `Post` 实例的唯一方式是对 `PendingReviewPost` 调用 `approve` 方法，而获得 `PendingReviewPost` 的唯一方式是对 `DraftPost` 调用 `request_review` 方法，我们现在已经把博客帖子工作流编码进了类型系统。

　　但我们也必须对 `main` 做一些小改动。`request_review` 与 `approve` 方法返回新实例而不是修改它们所调用的结构体，因此我们需要添加更多 `let post =` 遮蔽赋值来保存返回的实例。我们也不能再断言草稿与待审阅帖子的内容为空字符串，也不再需要：试图使用那些状态下帖子内容的代码已无法编译。`main` 中更新后的代码如示例 18-21 所示。

**文件名：`src/main.rs`**
```rust
use blog::Post;

fn main() {
    let mut post = Post::new();

    post.add_text("I ate a salad for lunch today");

    let post = post.request_review();

    let post = post.approve();

    assert_eq!("I ate a salad for lunch today", post.content());
}
```

**示例 18-21：修改 `main` 以使用博客帖子工作流的新实现**

　　我们对 `main` 所做的、为重新赋值 `post` 而需要的改动意味着，这一实现不再完全遵循面向对象状态模式：状态之间的转变不再完全封装在 `Post` 的实现内部。不过，我们的收获是：由于类型系统以及编译期发生的类型检查，非法状态现在不可能出现！这确保某些缺陷——例如显示未发布帖子的内容——会在进入生产之前就被发现。

　　试着对示例 18-21 之后的 `blog` crate 做本节开头建议的那些任务，看看你对这一版代码设计有何想法。注意其中有些任务在这种设计中可能已经完成了。

　　我们已经看到，即便 Rust 有能力实现面向对象设计模式，像把状态编码进类型系统这样的其他模式在 Rust 中同样可用。这些模式有不同取舍。尽管你可能非常熟悉面向对象模式，重新思考问题以发挥 Rust 特性的优势可以带来好处，例如在编译期防止某些缺陷。由于所有权等面向对象语言所没有的特性，面向对象模式在 Rust 中并不总是最佳方案。

## 小结

　　无论读完本章后你是否认为 Rust 是一门面向对象语言，你现在都知道可以用 trait 对象在 Rust 中获得一些面向对象特性。动态分发可以给你的代码一些灵活性，代价是一点运行时性能。你可以用这种灵活性实现有助于代码可维护性的面向对象模式。Rust 还有所有权等面向对象语言所没有的其他特性。由于这些特性，面向对象模式并不总是发挥 Rust 优势的最佳方式，但它是可用的选项。

　　接下来，我们将看看模式（pattern）——Rust 另一项带来大量灵活性的特性。我们在全书中已简要看过它们，但尚未见识其全部能力。出发吧！

[more-info-than-rustc]: ../../error-handling/03-to-panic-or-not-to-panic/#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ../../advanced-features/05-macros/#macros
