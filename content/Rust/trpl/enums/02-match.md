+++
title = "6.2 match 控制流结构"
date = 2026-08-05T08:44:00+08:00
weight = 25
type = "docs"
description = "match 控制流结构：穷尽模式匹配与绑定值"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# match 控制流结构 {#match}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch06-02-match.html](https://doc.rust-lang.org/stable/book/ch06-02-match.html)


## `match` 控制流结构 {#the-match-control-flow-construct}

　　Rust 有一个非常强大的控制流结构，叫做 `match`：它让你把一个值与一系列模式相比较，并按匹配到的模式执行相应代码。模式可以是字面量、变量名、通配符，以及许多其他形式；[第 19 章][ch19-00-patterns]会介绍各类模式及其用法。`match` 之所以强大，既因为模式表达力强，也因为编译器会检查是否已覆盖所有可能情况。

　　可以把 `match` 表达式想象成一台硬币分拣机：硬币沿轨道滑下，轨道上有大小不一的孔，每枚硬币落入它遇到的第一个能容下自己的孔。同样，值会依次经过 `match` 中的每个模式，在第一个「合适」的模式处落入关联的代码块并在执行中被使用。

　　说到硬币，我们用它们作为使用 `match` 的例子！可以编写一个函数，接收一枚未知的美国硬币，像计数机一样判断它是哪种硬币，并返回其面值（以美分为单位），如示例 6-3 所示。

```rust
enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter,
}

fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

**示例 6-3：一个枚举以及以该枚举变体为模式的 `match` 表达式**

　　下面分解 `value_in_cents` 函数中的 `match`。首先是 `match` 关键字，后跟一个表达式，此处即值 `coin`。这看起来很像与 `if` 一起使用的条件表达式，但有一个重大区别：使用 `if` 时，条件需要求值为布尔值，而这里可以是任意类型。本例中 `coin` 的类型是我们在第一行定义的 `Coin` 枚举。

　　接下来是 `match` 分支（arm）。一个分支有两部分：一个模式和一些代码。这里的第一个分支有一个模式，其值是 `Coin::Penny`，然后是分隔模式与要运行代码的 `=>` 运算符。此处的代码只是值 `1`。每个分支用逗号与下一个分支分隔。

　　当 `match` 表达式执行时，它会按顺序把结果值与每个分支的模式相比较。若某个模式匹配该值，就执行与该模式关联的代码。若该模式不匹配，执行继续到下一个分支，很像硬币分拣机。我们可以有任意多个分支：在示例 6-3 中，我们的 `match` 有四个分支。

　　与每个分支关联的代码是一个表达式，匹配分支中该表达式的结果值就是整个 `match` 表达式的返回值。

　　若 match 分支的代码很短——像示例 6-3 中每个分支只返回一个值那样——我们通常不用花括号。若想在 match 分支中运行多行代码，则必须使用花括号，此时分支后的逗号可选。例如，下面的代码每次以 `Coin::Penny` 调用该方法时都会打印 “Lucky penny!”，但仍然返回代码块的最后一个值 `1`：

```rust
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => {
            println!("Lucky penny!");
            1
        }
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter => 25,
    }
}
```

### 绑定值的模式

　　match 分支另一个有用的特性是：它们可以绑定到匹配模式的值的各个部分。这就是我们如何从枚举变体中提取值。

　　举例来说，让我们把其中一个枚举变体改成在内部保存数据。从 1999 年到 2008 年，美国铸造的 25 美分硬币一面有 50 个州各自不同的设计。其他硬币没有州设计，因此只有 25 美分硬币有这个额外值。可以把这一信息加入我们的 `enum`：把 `Quarter` 变体改为在内部保存一个 `UsState` 值，如示例 6-4 所示。

```rust
#[derive(Debug)] // so we can inspect the state in a minute
enum UsState {
    Alabama,
    Alaska,
    // --snip--
}

enum Coin {
    Penny,
    Nickel,
    Dime,
    Quarter(UsState),
}
```

**示例 6-4：`Quarter` 变体还保存 `UsState` 值的 `Coin` 枚举**

　　想象有位朋友想收集全部 50 个州的 25 美分硬币。我们按硬币类型整理零钱时，也会报出每个 25 美分硬币关联的州名，这样若朋友还没有那一枚，就可以加入收藏。

　　在这段代码的 match 表达式中，我们在匹配变体 `Coin::Quarter` 的模式里加入名为 `state` 的变量。当匹配到 `Coin::Quarter` 时，`state` 变量会绑定到该 25 美分硬币的州值。然后可以在该分支的代码中使用 `state`，像这样：

```rust
fn value_in_cents(coin: Coin) -> u8 {
    match coin {
        Coin::Penny => 1,
        Coin::Nickel => 5,
        Coin::Dime => 10,
        Coin::Quarter(state) => {
            println!("State quarter from {state:?}!");
            25
        }
    }
}
```

　　若调用 `value_in_cents(Coin::Quarter(UsState::Alaska))`，`coin` 将是 `Coin::Quarter(UsState::Alaska)`。当我们把该值与各个 match 分支比较时，直到 `Coin::Quarter(state)` 之前都不会匹配。此时，`state` 的绑定将是值 `UsState::Alaska`。然后可以在 `println!` 表达式中使用该绑定，从而从 `Coin` 枚举的 `Quarter` 变体中取出内部的州值。

### 匹配 `Option<T>`


　　上一节中，我们希望在使用 `Option<T>` 时从 `Some` 情况中取出内部的 `T` 值；也可以像对待 `Coin` 枚举那样，用 `match` 处理 `Option<T>`！我们比较的不再是硬币，而是 `Option<T>` 的变体，但 `match` 表达式的工作方式保持不变。

　　假设我们想编写一个函数：接受 `Option<i32>`，若内部有值则加 1；若没有值，函数应返回 `None`，且不尝试执行任何操作。

　　多亏有 `match`，这个函数写起来很容易，会像示例 6-5 这样。

```rust
    fn plus_one(x: Option<i32>) -> Option<i32> {
        match x {
            None => None,
            Some(i) => Some(i + 1),
        }
    }

    let five = Some(5);
    let six = plus_one(five);
    let none = plus_one(None);
```

**示例 6-5：对 `Option<i32>` 使用 `match` 表达式的 `plus_one` 函数**


　　更仔细地看看 `plus_one` 的第一次执行。当我们调用 `plus_one(five)` 时，`plus_one` 函数体中的变量 `x` 将具有值 `Some(5)`。然后我们把它与每个 match 分支比较：

```rust
            None => None,
```

　　`Some(5)` 值不匹配模式 `None`，因此继续到下一个分支：

```rust
            Some(i) => Some(i + 1),
```

　　`Some(5)` 匹配 `Some(i)` 吗？匹配！我们有相同的变体。`i` 绑定到 `Some` 中包含的值，因此 `i` 取值为 `5`。然后执行该 match 分支中的代码：把 `i` 的值加 1，并创建一个内部总计为 `6` 的新 `Some` 值。

　　现在考虑示例 6-5 中对 `plus_one` 的第二次调用，此时 `x` 是 `None`。我们进入 `match` 并与第一个分支比较：

```rust
            None => None,
```

　　匹配了！没有可加的值，因此程序停下来，返回 `=>` 右侧的 `None` 值。因为第一个分支已匹配，不再比较其他分支。

　　把 `match` 与枚举结合在许多情况下都很有用。你会在 Rust 代码中经常看到这种模式：对枚举做 `match`，把变量绑定到内部数据，然后据此执行代码。一开始可能有点别扭，但习惯之后你会希望所有语言都有它。它一直是用户最喜爱的特性之一。

### 匹配必须穷尽

　　关于 `match` 还有一点需要讨论：各分支的模式必须覆盖所有可能性。考虑我们这个有 bug、无法编译的 `plus_one` 函数版本：

```rust
    fn plus_one(x: Option<i32>) -> Option<i32> {
        match x {
            Some(i) => Some(i + 1),
        }
    }
```

　　我们没有处理 `None` 情况，因此这段代码会造成 bug。幸运的是，这是 Rust 知道如何捕获的 bug。若试图编译这段代码，会得到如下错误：

```console
$ cargo run
   Compiling enums v0.1.0 (file:///projects/enums)
error[E0004]: non-exhaustive patterns: `None` not covered
 --> src/main.rs:3:15
  |
3 |         match x {
  |               ^ pattern `None` not covered
  |
note: `Option<i32>` defined here
 --> /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/option.rs:597:0
 ::: /rustc/2d8144b7880597b6e6d3dfd63a9a9efae3f533d3/library/core/src/option.rs:601:4
  |
  = note: not covered
  = note: the matched value is of type `Option<i32>`
help: ensure that all possible cases are being handled by adding a match arm with a wildcard pattern or an explicit pattern as shown
  |
4 ~             Some(i) => Some(i + 1),
5 ~             None => todo!(),
  |

For more information about this error, try `rustc --explain E0004`.
error: could not compile `enums` (bin "enums") due to 1 previous error
```

　　Rust 知道我们没有覆盖每一种可能情况，甚至知道我们忘了哪个模式！Rust 中的匹配是*穷尽的*（exhaustive）：必须穷尽每一种最后的可能性，代码才有效。尤其是对于 `Option<T>`，当 Rust 阻止我们忘记显式处理 `None` 情况时，它就保护我们免于在可能为 null 时假定我们有值，从而使前面讨论的十亿美元错误变得不可能。

### 通配模式与 `_` 占位符

　　使用枚举时，我们也可以对少数特定值采取特殊行动，而对所有其他值采取一个默认行动。想象我们在实现一个游戏：若骰子掷出 3，玩家不移动，而是得到一顶新奇的帽子；若掷出 7，玩家丢掉一顶新奇的帽子；对其余所有值，玩家在游戏板上移动相应格数。下面的 `match` 实现了该逻辑，骰子结果被硬编码而非随机，其余逻辑用没有函数体的函数表示，因为真正实现它们超出了本例范围：

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        other => move_player(other),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
    fn move_player(num_spaces: u8) {}
```

　　前两个分支的模式是字面量 `3` 和 `7`。覆盖其余所有可能值的最后一个分支，模式是我们选择命名为 `other` 的变量。为 `other` 分支运行的代码会把该变量传给 `move_player` 函数。

　　这段代码可以编译，即便我们没有列出 `u8` 可能有的全部值，因为最后一个模式会匹配所有未特别列出的值。这个通配模式满足了 `match` 必须穷尽的要求。注意：我们必须把通配分支放在最后，因为模式按顺序求值。若把通配分支放在前面，其他分支永远不会运行，因此若在通配之后再加分支，Rust 会警告我们！

　　Rust 还有一种模式，用于我们想要通配却不想*使用*通配模式中的值时：`_` 是特殊模式，匹配任意值且不绑定到该值。这告诉 Rust 我们不会使用该值，因此 Rust 不会警告未使用的变量。

　　让我们改改游戏规则：现在，若掷出的不是 3 或 7，必须再掷一次。我们不再需要使用通配值，因此可以把代码改为使用 `_` 而不是名为 `other` 的变量：

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        _ => reroll(),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
    fn reroll() {}
```

　　这个例子也满足穷尽性要求，因为我们在最后一个分支中显式忽略了所有其他值；我们没有遗漏任何情况。

　　最后再改一次游戏规则：若掷出的不是 3 或 7，本回合什么也不发生。可以用单元值（我们在[「元组类型」][tuples]一节提到的空元组类型）作为与 `_` 分支关联的代码来表达这一点：

```rust
    let dice_roll = 9;
    match dice_roll {
        3 => add_fancy_hat(),
        7 => remove_fancy_hat(),
        _ => (),
    }

    fn add_fancy_hat() {}
    fn remove_fancy_hat() {}
```

　　这里我们明确告诉 Rust：对于不匹配先前分支中任何模式的其他值，我们不会使用它们，也不想在这种情况下运行任何代码。

　　关于模式与匹配还有更多内容，我们会在[第 19 章][ch19-00-patterns]介绍。眼下我们转向 `if let` 语法，它在 `match` 表达式略显啰嗦的情况下可能有用。

[tuples]: ../../common-programming-concepts/02-data-types/
[ch19-00-patterns]: ../../patterns/
