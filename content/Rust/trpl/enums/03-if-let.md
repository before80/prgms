+++
title = "6.3 用 if let 与 let...else 简化控制流"
date = 2026-08-05T08:44:00+08:00
weight = 26
type = "docs"
description = "用 if let 与 let...else 以更简洁的方式处理单一模式"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 用 if let 与 let...else 简化控制流 {#if-let-let-else}


> 原文链接: [https://doc.rust-lang.org/stable/book/ch06-03-if-let.html](https://doc.rust-lang.org/stable/book/ch06-03-if-let.html)


## 用 `if let` 与 `let...else` 简化控制流

　　`if let` 语法让你把 `if` 和 `let` 结合起来，以更简洁的方式处理匹配某一模式的值，同时忽略其余情况。考虑示例 6-6 中的程序：它对 `config_max` 变量中的 `Option<u8>` 值做 match，但只想在值为 `Some` 变体时执行代码。

```rust
    let config_max = Some(3u8);
    match config_max {
        Some(max) => println!("The maximum is configured to be {max}"),
        _ => (),
    }
```

**示例 6-6：只关心值是 `Some` 时执行代码的 `match`**

　　若值是 `Some`，我们通过在模式中把值绑定到变量 `max` 来打印 `Some` 变体中的值。对于 `None` 值我们不想做任何事。为满足 `match` 表达式，在只处理一个变体之后还必须加上 `_ => ()`，这是烦人的样板代码。

　　取而代之，可以用 `if let` 写得更短。下面的代码与示例 6-6 中的 `match` 行为相同：

```rust
    let config_max = Some(3u8);
    if let Some(max) = config_max {
        println!("The maximum is configured to be {max}");
    }
```

　　`if let` 语法接受一个模式和一个由等号分隔的表达式。它的工作方式与 `match` 相同：表达式交给 `match`，模式则是其第一个分支。此处模式是 `Some(max)`，`max` 绑定到 `Some` 内部的值。然后可以在 `if let` 块的主体中使用 `max`，方式与在对应的 `match` 分支中使用 `max` 相同。只有当值匹配该模式时，`if let` 块中的代码才会运行。

　　使用 `if let` 意味着少写一些代码、缩进更少、样板也更少。不过，你也失去了 `match` 强制的穷尽性检查——那种检查能确保你没有漏掉任何情况。在 `match` 与 `if let` 之间如何取舍，取决于具体场景，以及你是否愿意为简洁而牺牲穷尽性检查。

　　换言之，可以把 `if let` 看作一种语法糖：相当于一个在值匹配某一模式时运行代码、然后忽略所有其他值的 `match`。

　　我们可以给 `if let` 加上 `else`。与 `else` 关联的代码块，等同于与该 `if let` 和 `else` 等价的 `match` 表达式中 `_` 情况关联的代码块。回想示例 6-4 中的 `Coin` 枚举定义，其中 `Quarter` 变体还保存了 `UsState` 值。若我们想统计见到的所有非 25 美分硬币，同时报出 25 美分硬币的州名，可以用 `match` 表达式这样做：

```rust
    let mut count = 0;
    match coin {
        Coin::Quarter(state) => println!("State quarter from {state:?}!"),
        _ => count += 1,
    }
```

　　或者也可以用 `if let` 和 `else` 表达式，像这样：

```rust
    let mut count = 0;
    if let Coin::Quarter(state) = coin {
        println!("State quarter from {state:?}!");
    } else {
        count += 1;
    }
```

## 用 `let...else` 留在「成功路径」上

　　常见模式是：当值存在时执行某些计算，否则返回默认值。继续用带有 `UsState` 值的硬币例子：若我们想根据 25 美分硬币上州的历史长短说点有趣的话，可以在 `UsState` 上引入一个方法来检查州的年龄，像这样：

```rust
impl UsState {
    fn existed_in(&self, year: u16) -> bool {
        match self {
            UsState::Alabama => year >= 1819,
            UsState::Alaska => year >= 1959,
            // -- snip --
        }
    }
}
```

　　然后，我们可以像示例 6-7 那样，用 `if let` 匹配硬币类型，并在条件体中引入 `state` 变量。

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    if let Coin::Quarter(state) = coin {
        if state.existed_in(1900) {
            Some(format!("{state:?} is pretty old, for America!"))
        } else {
            Some(format!("{state:?} is relatively new."))
        }
    } else {
        None
    }
}
```

**示例 6-7：用嵌套在 `if let` 内的条件检查某州在 1900 年是否已存在**

　　这样能完成任务，却把主要逻辑都放进了 `if let` 语句的主体里；若要做的事更复杂，可能很难看清顶层各分支究竟如何关联。我们也可以利用表达式会产生值这一点，要么从 `if let` 产生 `state`，要么提前返回，如示例 6-8 所示。（用 `match` 也能做类似的事。）

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    let state = if let Coin::Quarter(state) = coin {
        state
    } else {
        return None;
    };

    if state.existed_in(1900) {
        Some(format!("{state:?} is pretty old, for America!"))
    } else {
        Some(format!("{state:?} is relatively new."))
    }
}
```

**示例 6-8：用 `if let` 产生值或提前返回**

　　不过这种写法同样繁琐：`if let` 的一个分支产生值，另一个分支则直接 `return`。

　　为了更优雅地表达这种常见模式，Rust 提供了 `let...else`。`let...else` 语法左侧是模式、右侧是表达式，与 `if let` 非常相似，但它没有 `if` 分支，只有 `else` 分支。若模式匹配，它会把模式中的值绑定到外层作用域；若模式*不*匹配，程序会进入 `else` 分支，而该分支必须从函数返回。

　　在示例 6-9 中，可以看到用 `let...else` 替代 `if let` 后示例 6-8 的样子。

```rust
fn describe_state_quarter(coin: Coin) -> Option<String> {
    let Coin::Quarter(state) = coin else {
        return None;
    };

    if state.existed_in(1900) {
        Some(format!("{state:?} is pretty old, for America!"))
    } else {
        Some(format!("{state:?} is relatively new."))
    }
}
```

**示例 6-9：用 `let...else` 理顺函数中的控制流**

　　注意：这样一来，函数主体可以沿着主流程编写，而不像 `if let` 那样把控制流拆成两个截然不同的分支。

　　若遇到用 `match` 表达起来过于啰嗦的程序逻辑，请记住：`if let` 和 `let...else` 也在你的 Rust 工具箱里。

## 总结

　　我们现在已经介绍了如何用枚举创建可以是一组枚举值之一的自定义类型。我们展示了标准库的 `Option<T>` 类型如何帮助你利用类型系统防止错误。当枚举值内部有数据时，可以用 `match` 或 `if let` 提取并使用这些值，取决于你需要处理多少种情况。

　　你的 Rust 程序现在可以用结构体和枚举表达领域中的概念。创建在 API 中使用的自定义类型能确保类型安全：编译器会保证你的函数只接收每个函数所期望类型的值。

　　为了向用户提供组织良好、易于使用、且恰好只暴露用户所需内容的 API，接下来我们转向 Rust 的模块。
