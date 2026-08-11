+++
title = "3.3 生命周期"
date = 2026-08-06T17:08:00+08:00
weight = 13
type = "docs"
description = "生命周期的含义与作用范围"
isCJKLanguage = true
draft = false
rust_edition = "2024"

+++

> 译文 · 基于 [The Rustonomicon](https://doc.rust-lang.org/nomicon/)

# 生命周期


> 原文链接: [https://doc.rust-lang.org/nomicon/lifetimes.html](https://doc.rust-lang.org/nomicon/lifetimes.html)


　　Rust 通过*生命周期（lifetime）* 强制这些规则。生命周期是引用必须有效的命名代码区域。这些区域可能相当复杂，对应程序中的执行路径。路径中甚至可能有「洞」——只要在使用前重新初始化，引用就可能失效。含引用（或假装含引用）的类型也可标生命周期，以便 Rust 防止它们被失效。

　　在多数例子中，生命周期与作用域重合，因为例子简单。更复杂的不重合情况见下文。

　　在函数体内，Rust 一般不允许显式命名涉及的生命周期。因为局部上下文通常不必谈生命周期；Rust 有全部信息，可尽可能最优推断。许多你否则须写的匿名作用域与临时量常被引入以使代码正常工作。

　　然而一旦跨函数边界，就须谈生命周期。生命周期用撇号表示：`'a`、`'static`。为入门，我们假装允许给作用域标生命周期，并把本章开头的例子脱糖（desugar）。

　　原先，我们的例子对作用域与生命周期用了*大量*语法糖——甚至高果糖玉米糖浆——因为全写出来*极其*嘈杂。所有 Rust 代码都依赖对「显然」之事的积极推断与省略。

　　一块特别有趣的糖是：每个 `let` 语句隐式引入作用域。大多时候无关紧要。但对彼此引用的变量则重要。为简单例子，完全脱糖这段 Rust：

```rust
let x = 0;
let y = &x;
let z = &y;
```

　　借用检查器总是试图最小化生命周期范围，故可能脱糖为：

```rust,ignore
// 注意：`'a: {` 与 `&'b x` 不是合法语法！
'a: {
    let x: i32 = 0;
    'b: {
        // 使用的生命周期是 'b，因为够用了。
        let y: &'b i32 = &'b x;
        'c: {
            // 'c 同理
            let z: &'c &'b i32 = &'c y; // 「指向 i32 引用的引用」（已标生命周期）
        }
    }
}
```

　　哇。这……糟透了。让我们感谢 Rust 让这更简单。

　　实际上把引用传到外层作用域会使 Rust 推断更大生命周期：

```rust
let x = 0;
let z;
let y = &x;
z = y;
```

```rust,ignore
'a: {
    let x: i32 = 0;
    'b: {
        let z: &'b i32;
        'c: {
            // 此处须用 'b，因为对 x 的引用
            // 被传到作用域 'b。
            let y: &'b i32 = &'b x;
            z = y;
        }
    }
}
```

## 示例：比被引用对象活得更久的引用

　　好，看前面一些例子：

```rust,compile_fail
fn as_str(data: &u32) -> &str {
    let s = format!("{}", data);
    &s
}
```

　　脱糖为：

```rust,ignore
fn as_str<'a>(data: &'a u32) -> &'a str {
    'b: {
        let s = format!("{}", data);
        return &'a s;
    }
}
```

　　`as_str` 的签名取*某*生命周期的 `u32` 引用，并承诺可产生能活*同样久*的 `str` 引用。已可见该签名可能麻烦：基本上暗示我们须在 `u32` 引用来源的作用域或*更早*某处找到 `str`。要求颇高。

　　然后我们计算字符串 `s` 并返回其引用。因函数契约说引用须比 `'a` 活得更久，我们为引用推断 `'a`。不幸的是 `s` 定义在 `'b` 作用域，故健全的唯一可能是 `'b` 包含 `'a`——显然不成立，因为 `'a` 须包含函数调用本身。我们因而创造了比被引用对象活得更久的引用，这正是引用规则禁止的第一件事。编译器理所当然地报错。

　　为更清楚，可展开：

```rust,ignore
fn as_str<'a>(data: &'a u32) -> &'a str {
    'b: {
        let s = format!("{}", data);
        return &'a s
    }
}

fn main() {
    'c: {
        let x: u32 = 0;
        'd: {
            // 引入匿名作用域，因为借用不必
            // 持续 x 有效的整个作用域。as_str 的返回
            // 须在本调用前某处找到 str。显然不会发生。
            println!("{}", as_str::<'d>(&'d x));
        }
    }
}
```

　　糟了！

　　正确写法当然是：

```rust
fn to_string(data: &u32) -> String {
    format!("{}", data)
}
```

　　须在函数内产生 owned 值再返回！唯一能返回 `&'a str` 的方式是它在 `&'a u32` 的字段里，显然不是。

　　（其实也可返回字符串字面量，作为全局可视为在栈底；但这*稍微*限制实现。）

## 示例：别名可变引用

　　另一个例子：

```rust,compile_fail
let mut data = vec![1, 2, 3];
let x = &data[0];
data.push(4);
println!("{}", x);
```

```rust,ignore
'a: {
    let mut data: Vec<i32> = vec![1, 2, 3];
    'b: {
        // 'b 只要借用到 `println!` 所需那么大
        let x: &'b i32 = Index::index::<'b>(&'b data, 0);
        'c: {
            // 临时作用域，因为 &mut 不必
            // 再持续更久。
            Vec::push(&'c mut data, 4);
        }
        println!("{}", x);
    }
}
```

　　此处问题更微妙也更有趣。我们希望 Rust 拒绝此程序，理由：在试图对 `data` 取 `push` 所需的 `&mut` 时，我们仍持有指向 `data` 某后代的活跃共享引用 `x`。这会创造别名的可变引用，违反引用的*第二条*规则。

　　然而 Rust *完全不是*这样推理程序有问题。Rust 不理解 `x` 是指向 `data` 子路径的引用，也不理解 `Vec`。它*看到*的是 `x` 须活 `'b` 才能打印。`Index::index` 的签名随后要求对 `data` 的引用须存活 `'b`。当我们试图 `push`，它看到我们试图做 `&'c mut data`。Rust 知道 `'c` 包含在 `'b` 内，拒绝程序，因为 `&'b data` 仍须有效！

　　此处可见生命周期系统比我们要维护的引用语义粗粒度得多。大多时候*完全没问题*，因为避免我们整天向编译器解释程序。然而若干对 Rust *真正*语义完全正确的程序会因生命周期推断过粗而被拒。

## 生命周期覆盖的范围

　　引用（有时称*借用*）从创建处活跃到最后一次使用。被借值只需比仍活跃的借用活得更久。看起来简单，有几处微妙之处。

　　下列片段能编译，因为打印 `x` 后不再需要它，悬垂或别名都无所谓（尽管变量 `x` *技术上*存在到作用域末尾）。

```rust
let mut data = vec![1, 2, 3];
let x = &data[0];
println!("{}", x);
// 可以，x 不再需要
data.push(4);
```

　　但若值有析构函数，析构在作用域末运行。运行析构算一次使用——显然是最后一次。故下列*不能*编译。

```rust,compile_fail
#[derive(Debug)]
struct X<'a>(&'a i32);

impl Drop for X<'_> {
    fn drop(&mut self) {}
}

let mut data = vec![1, 2, 3];
let x = X(&data[0]);
println!("{:?}", x);
data.push(4);
// 此处运行析构，故编译失败。
```

　　一种说服编译器 `x` 不再有效的方式是在 `data.push(4)` 前 `drop(x)`。

　　此外，借用可能有多个可能的最后使用点，例如条件各分支。

```rust
# fn some_condition() -> bool { true }
let mut data = vec![1, 2, 3];
let x = &data[0];

if some_condition() {
    println!("{}", x); // 本分支中 `x` 的最后使用
    data.push(4);      // 故可在此 push
} else {
    // 本分支未使用 `x`，故有效上的最后使用是
    // 例子顶部的 x 创建。
    data.push(5);
}
```

　　生命周期可有暂停。或可视作两次独立借用绑定到同一局部变量。循环周围常见（在循环末写变量新值、在下次迭代顶最后一次使用）。

```rust
let mut data = vec![1, 2, 3];
// 此 mut 允许改变引用指向
let mut x = &data[0];

println!("{}", x); // 此次借用的最后使用
data.push(4);
x = &data[3]; // 在此开始新借用
println!("{}", x);
```

　　历史上 Rust 把借用保持到作用域结束，故这些例子在旧编译器上可能失败。仍有边角情况 Rust 未能正确缩短借用的活跃部分、看起来应能编译却失败。会随时间解决。
