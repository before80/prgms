+++
title = "10.2 用 Trait 定义共享行为"
date = 2026-08-05T08:44:00+08:00
weight = 43
type = "docs"
description = "用 trait、默认实现与 trait 约束定义共享行为"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 Trait 定义共享行为 {#trait}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch10-02-traits.html](https://doc.rust-lang.org/stable/book/ch10-02-traits.html)


## 用 Trait 定义共享行为

　　**特征（trait）** 定义了特定类型所具有、并可与其他类型共享的功能。我们可以用 trait 以抽象方式定义共享行为，并用 *trait 约束（trait bound）* 指明泛型类型可以是任何具有某种行为的类型。

> 注意：Trait 与其他语言中常称为*接口（interface）*的特性类似，但有一些差异。

### 定义 Trait

　　类型的行为由可在其上调用的方法组成。若能在多个类型上调用相同方法，这些类型就共享相同行为。Trait 定义是把方法签名组合在一起、以定义完成某项目的所需行为集合的方式。

　　例如，假设有多个保存各类文本的结构体：`NewsArticle` 保存在特定地点发布的新闻故事，`SocialPost` 最多 280 个字符，并带有表明是新帖、转发还是回复的元数据。

　　我们想做一个名为 `aggregator` 的媒体聚合库 crate，能显示可能存储在 `NewsArticle` 或 `SocialPost` 实例中的数据摘要。为此需要从每种类型获取摘要，并通过在实例上调用 `summarize` 方法来请求它。示例 10-12 展示了表达该行为的公共 `Summary` trait 定义。

**文件名：`src/lib.rs`**
```rust
pub trait Summary {
    fn summarize(&self) -> String;
}
```

**示例 10-12：由 `summarize` 方法所提供行为组成的 `Summary` trait**

　　我们用 `trait` 关键字后跟 trait 名来声明 trait，这里是 `Summary`。我们还把它声明为 `pub`，以便依赖本 crate 的其他 crate 也能使用该 trait，稍后会看到例子。在花括号内，我们声明描述实现该 trait 的类型之行为的方法签名，这里是 `fn summarize(&self) -> String`。

　　方法签名之后不用花括号提供实现，而是用分号。每个实现该 trait 的类型都必须为方法体提供自己的自定义行为。编译器会强制：任何具有 `Summary` trait 的类型都必须恰好以该签名定义方法 `summarize`。

　　一个 trait 的主体可以有多个方法：每个方法签名占一行，并以分号结尾。

### 在类型上实现 Trait {#implementing-a-trait-on-a-type}

　　定义好 `Summary` trait 的方法签名后，就可以在媒体聚合器的类型上实现它。示例 10-13 展示了在 `NewsArticle` 上实现 `Summary`：用标题、作者与地点构成 `summarize` 的返回值。对 `SocialPost`，我们把 `summarize` 定义为用户名后跟帖子全文，并假定内容已被限制在 280 字符以内。

**文件名：`src/lib.rs`**
```rust
pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }
}

pub struct SocialPost {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub repost: bool,
}

impl Summary for SocialPost {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }
}
```

**示例 10-13：在 `NewsArticle` 与 `SocialPost` 类型上实现 `Summary` trait**

　　在类型上实现 trait 与实现普通方法类似。区别是：在 `impl` 之后写要实现的 trait 名，再用 `for`，然后指定要实现该 trait 的类型名。在 `impl` 块内放入 trait 定义中的方法签名；签名后不用分号，而是用花括号填入我们希望该类型上这些方法所具有的具体行为。

　　库已在 `NewsArticle` 与 `SocialPost` 上实现 `Summary` 后，crate 的用户就可以像调用普通方法一样，在这些实例上调用 trait 方法。唯一区别是：用户必须同时把 trait 与类型引入作用域。下面是二进制 crate 如何使用我们的 `aggregator` 库 crate 的例子：

```rust
use aggregator::{SocialPost, Summary};

fn main() {
    let post = SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    };

    println!("1 new post: {}", post.summarize());
}
```

　　这段代码会打印 `1 new post: horse_ebooks: of course, as you probably already know, people`。

　　依赖 `aggregator` 的其他 crate 也可以通过 `use` 导入 `Summary` trait，以便在自己的类型上实现 `Summary`。有一条限制需要注意：只有当 trait 或类型中至少有一方定义在本 crate 时，才能在类型上实现 trait。例如，作为 `aggregator` crate 功能的一部分，我们可以在自定义类型如 `SocialPost` 上实现标准库 trait（如 `Display`），因为类型 `SocialPost` 对本 crate 是本地的。我们也可以在 `aggregator` 中为 `Vec<T>` 实现 `Summary`，因为 trait `Summary` 对本 crate 是本地的。

　　但不能为外部类型实现外部 trait。例如，不能在 `aggregator` 中为 `Vec<T>` 实现 `Display`，因为 `Display` 与 `Vec<T>` 都定义在标准库中，对本 crate 都不是本地的。这一限制属于称为*连贯性（coherence）*的性质，更具体地说是*孤儿规则（orphan rule）*——如此命名是因为“父类型”不在场。该规则确保别人的代码不会破坏你的代码，反之亦然。若没有该规则，两个 crate 可能为同一类型实现同一 trait，Rust 就不知道该用哪个实现。

### 使用默认实现

　　有时让 trait 中部分或全部方法具有默认行为很有用，而不是要求每个类型都实现所有方法。然后，在特定类型上实现该 trait 时，可以保留或覆盖每个方法的默认行为。

　　在示例 10-14 中，我们为 `Summary` trait 的 `summarize` 方法指定默认字符串，而不像示例 10-12 那样只定义方法签名。

**文件名：`src/lib.rs`**
```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
```

**示例 10-14：为 `summarize` 方法定义默认实现的 `Summary` trait**

　　要用默认实现来摘要 `NewsArticle` 实例，只需写空的 `impl` 块：`impl Summary for NewsArticle {}`。

　　尽管我们不再直接为 `NewsArticle` 定义 `summarize` 方法，但已提供默认实现并指明 `NewsArticle` 实现了 `Summary`。因此仍可在 `NewsArticle` 实例上调用 `summarize`，像这样：

```rust
    let article = NewsArticle {
        headline: String::from("Penguins win the Stanley Cup Championship!"),
        location: String::from("Pittsburgh, PA, USA"),
        author: String::from("Iceburgh"),
        content: String::from(
            "The Pittsburgh Penguins once again are the best \
             hockey team in the NHL.",
        ),
    };

    println!("New article available! {}", article.summarize());
```

　　这段代码会打印 `New article available! (Read more...)`。

　　创建默认实现并不要求我们改动示例 10-13 中 `SocialPost` 上 `Summary` 的实现。原因是：覆盖默认实现的语法，与实现没有默认实现的 trait 方法的语法相同。

　　默认实现可以调用同一 trait 中的其他方法，即便那些方法没有默认实现。这样，trait 可以提供大量有用功能，而只要求实现者指定其中一小部分。例如，我们可以定义 `Summary` 要求实现 `summarize_author`，再定义有默认实现的 `summarize`，由其调用 `summarize_author`：

```rust
pub trait Summary {
    fn summarize_author(&self) -> String;

    fn summarize(&self) -> String {
        format!("(Read more from {}...)", self.summarize_author())
    }
}
```

　　要使用这个版本的 `Summary`，在类型上实现该 trait 时只需定义 `summarize_author`：

```rust
impl Summary for SocialPost {
    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}
```

　　定义 `summarize_author` 之后，就可以在 `SocialPost` 实例上调用 `summarize`，默认实现会调用我们提供的 `summarize_author`。因为我们实现了 `summarize_author`，`Summary` trait 就给了我们 `summarize` 的行为，而无需再写更多代码。看起来像这样：

```rust
    let post = SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    };

    println!("1 new post: {}", post.summarize());
```

　　这段代码会打印 `1 new post: (Read more from @horse_ebooks...)`。

　　注意：无法从同一方法的覆盖实现中调用该方法的默认实现。

### 把 Trait 用作参数 {#traits-as-parameters}

　　既然知道如何定义与实现 trait，就可以探索如何用 trait 定义接受多种不同类型的函数。我们用示例 10-13 中在 `NewsArticle` 与 `SocialPost` 上实现的 `Summary` trait，定义一个对 `item` 参数调用 `summarize` 的 `notify` 函数，而 `item` 是某个实现了 `Summary` 的类型。为此使用 `impl Trait` 语法，像这样：

```rust
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}
```

　　`item` 参数不是具体类型，而是 `impl` 关键字加 trait 名。该参数接受任何实现了指定 trait 的类型。在 `notify` 函数体中，我们可以调用 `item` 上来自 `Summary` trait 的任何方法，例如 `summarize`。我们可以用任何 `NewsArticle` 或 `SocialPost` 实例调用 `notify`。用其他类型（如 `String` 或 `i32`）调用则无法编译，因为那些类型未实现 `Summary`。

#### Trait 约束语法

　　`impl Trait` 语法适用于简单情形，实际上是更长形式——*trait 约束*——的语法糖，如下所示：

```rust
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

　　这种较长形式与上一节的例子等价，但更冗长。我们在尖括号内、泛型类型参数声明之后用冒号写出 trait 约束。

　　简单情形下 `impl Trait` 更方便、代码更简洁；而完整的 trait 约束语法能表达更复杂的情况。例如，可以有两个都实现 `Summary` 的参数。用 `impl Trait` 写法如下：

```rust
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

　　若希望该函数允许 `item1` 与 `item2` 类型不同（只要都实现 `Summary`），用 `impl Trait` 合适。但若要强制两个参数类型相同，就必须用 trait 约束，像这样：

```rust
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

　　把泛型类型 `T` 同时指定为 `item1` 与 `item2` 的类型，就约束了函数：作为 `item1` 与 `item2` 传入的具体类型必须相同。

#### 用 `+` 语法指定多个 Trait 约束

　　我们也可以指定多个 trait 约束。假设希望 `notify` 除了在 `item` 上调用 `summarize`，还要使用显示格式化：在 `notify` 的定义中指明 `item` 必须同时实现 `Display` 与 `Summary`。可用 `+` 语法：

```rust
pub fn notify(item: &(impl Summary + Display)) {
```

　　`+` 语法对泛型类型上的 trait 约束同样有效：

```rust
pub fn notify<T: Summary + Display>(item: &T) {
```

　　指定两个 trait 约束后，`notify` 的函数体就可以调用 `summarize`，并用 `{}` 格式化 `item`。

#### 用 `where` 子句写出更清晰的 Trait 约束

　　Trait 约束过多也有缺点。每个泛型都有自己的约束，因此带多个泛型类型参数的函数可能在函数名与参数列表之间塞满约束信息，签名难读。为此，Rust 提供了在函数签名之后的 `where` 子句中指定 trait 约束的替代语法。于是，不必写成：

```rust
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

　　而可以用 `where` 子句，像这样：

```rust
fn some_function<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{
```

　　这个函数的签名更清爽：函数名、参数列表与返回类型靠得更近，类似没有大量 trait 约束的函数。

### 返回实现了 Trait 的类型

　　也可以在返回位置使用 `impl Trait` 语法，返回某个实现了某 trait 的类型的值，如下所示：

```rust
fn returns_summarizable() -> impl Summary {
    SocialPost {
        username: String::from("horse_ebooks"),
        content: String::from(
            "of course, as you probably already know, people",
        ),
        reply: false,
        repost: false,
    }
}
```

　　用 `impl Summary` 作为返回类型，表示 `returns_summarizable` 返回某个实现了 `Summary` 的类型，而无需命名具体类型。本例中它返回 `SocialPost`，但调用方不必知道这一点。

　　仅按所实现的 trait 指定返回类型，在闭包与迭代器的语境中尤其有用（第 13 章会讲）。闭包与迭代器会创建只有编译器知道、或写出来很长的类型。`impl Trait` 让你能简洁地指明函数返回某个实现了 `Iterator` 的类型，而无需写出很长的类型名。

　　不过，只有在返回单一类型时才能使用 `impl Trait`。例如，下面这段以 `impl Summary` 为返回类型、却可能返回 `NewsArticle` 或 `SocialPost` 的代码行不通：

```rust
fn returns_summarizable(switch: bool) -> impl Summary {
    if switch {
        NewsArticle {
            headline: String::from(
                "Penguins win the Stanley Cup Championship!",
            ),
            location: String::from("Pittsburgh, PA, USA"),
            author: String::from("Iceburgh"),
            content: String::from(
                "The Pittsburgh Penguins once again are the best \
                 hockey team in the NHL.",
            ),
        }
    } else {
        SocialPost {
            username: String::from("horse_ebooks"),
            content: String::from(
                "of course, as you probably already know, people",
            ),
            reply: false,
            repost: false,
        }
    }
}
```

　　由于编译器中 `impl Trait` 语法的实现限制，不允许返回 `NewsArticle` 或 `SocialPost` 二者之一。如何编写具有这种行为的函数，见第 18 章[「用 Trait 对象抽象共享行为」][trait-objects]。

### 用 Trait 约束有条件地实现方法

　　通过对使用泛型类型参数的 `impl` 块使用 trait 约束，我们可以仅为实现了指定 trait 的类型有条件地实现方法。例如，示例 10-15 中的类型 `Pair<T>` 始终实现 `new` 函数以返回新的 `Pair<T>` 实例（回想第 5 章[「方法语法」][methods]：`Self` 是 `impl` 块所针对类型的类型别名，这里是 `Pair<T>`）。但在下一个 `impl` 块中，只有当内部类型 `T` 既实现了支持比较的 `PartialOrd`，又实现了支持打印的 `Display` 时，`Pair<T>` 才实现 `cmp_display` 方法。

**文件名：`src/lib.rs`**
```rust
use std::fmt::Display;

struct Pair<T> {
    x: T,
    y: T,
}

impl<T> Pair<T> {
    fn new(x: T, y: T) -> Self {
        Self { x, y }
    }
}

impl<T: Display + PartialOrd> Pair<T> {
    fn cmp_display(&self) {
        if self.x >= self.y {
            println!("The largest member is x = {}", self.x);
        } else {
            println!("The largest member is y = {}", self.y);
        }
    }
}
```

**示例 10-15：根据 trait 约束有条件地在泛型类型上实现方法**

　　我们也可以为任何实现了另一 trait 的类型有条件地实现某个 trait。对满足 trait 约束的任何类型实现某 trait，称为*覆盖实现（blanket implementation）*，在 Rust 标准库中被广泛使用。例如，标准库为任何实现了 `Display` 的类型实现 `ToString` trait。标准库中的 `impl` 块类似这样：

```rust
impl<T: Display> ToString for T {
    // --snip--
}
```

　　因为有这条覆盖实现，我们可以在任何实现了 `Display` 的类型上调用 `ToString` 定义的 `to_string` 方法。例如，整数实现了 `Display`，因此可以这样把整数变成对应的 `String` 值：

```rust
let s = 3.to_string();
```

　　覆盖实现会出现在该 trait 文档的「实现者（Implementors）」一节。

　　Trait 与 trait 约束让我们能用泛型类型参数减少重复，同时又向编译器指明：我们希望泛型类型具有特定行为。编译器随后可用 trait 约束信息检查：与我们代码一起使用的所有具体类型都提供了正确行为。在动态类型语言中，若对未定义某方法的类型调用该方法，会在运行时出错；而 Rust 把这些错误前移到编译期，迫使我们在代码能运行之前就修复问题。此外，我们不必编写运行时检查行为的代码，因为已在编译期检查过。这样既提升性能，又不必放弃泛型的灵活性。

[trait-objects]: ../../oop/02-trait-objects/#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ../../structs/03-method-syntax/#method-syntax
