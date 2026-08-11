+++
title = "附录A 关键字"
date = 2026-08-05T08:44:00+08:00
weight = 105
type = "docs"
description = "Rust 当前使用与预留关键字，以及原始标识符"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# A - 关键字 {#a}


> 原文链接: [https://doc.rust-lang.org/stable/book/appendix-01-keywords.html](https://doc.rust-lang.org/stable/book/appendix-01-keywords.html)


## 附录 A：关键字

　　下列列表包含 Rust 语言当前或未来保留使用的关键字。因此它们不能用作标识符（除非使用[「原始标识符」][raw-identifiers]一节中讨论的原始标识符）。*标识符*指函数、变量、参数、结构体字段、模块、crate、常量、宏、静态值、属性、类型、特征（trait）或生命周期的名字。

[raw-identifiers]: #raw-identifiers

### 当前使用的关键字

　　以下是当前正在使用的关键字及其功能说明。

- **`as`**：进行原始类型转换、消歧义某个包含项的具体特征，或在 `use` 语句中重命名项。
- **`async`**：返回一个 `Future`，而不是阻塞当前线程。
- **`await`**：挂起执行，直到某个 `Future` 的结果就绪。
- **`break`**：立即退出循环。
- **`const`**：定义常量项或常量原始指针。
- **`continue`**：继续下一次循环迭代。
- **`crate`**：在模块路径中，指代 crate 根。
- **`dyn`**：对特征对象进行动态分发。
- **`else`**：`if` 与 `if let` 控制流结构的回退分支。
- **`enum`**：定义枚举。
- **`extern`**：链接外部函数或变量。
- **`false`**：布尔假字面量。
- **`fn`**：定义函数或函数指针类型。
- **`for`**：遍历迭代器中的项、实现特征，或指定高阶生命周期。
- **`if`**：根据条件表达式的结果进行分支。
- **`impl`**：实现固有方法或特征功能。
- **`in`**：`for` 循环语法的一部分。
- **`let`**：绑定变量。
- **`loop`**：无条件循环。
- **`match`**：将值与模式进行匹配。
- **`mod`**：定义模块。
- **`move`**：使闭包获取其所有捕获的所有权。
- **`mut`**：在引用、原始指针或模式绑定中表示可变性。
- **`pub`**：在结构体字段、`impl` 块或模块中表示公开可见性。
- **`ref`**：按引用绑定。
- **`return`**：从函数返回。
- **`Self`**：我们所定义或实现的类型的类型别名。
- **`self`**：方法的主体（接收者）或当前模块。
- **`static`**：全局变量，或贯穿整个程序执行的生命周期。
- **`struct`**：定义结构体。
- **`super`**：当前模块的父模块。
- **`trait`**：定义特征。
- **`true`**：布尔真字面量。
- **`type`**：定义类型别名或关联类型。
- **`union`**：定义[联合体（union）][union]；仅在联合体声明中用作关键字。
- **`unsafe`**：标记不安全代码、函数、特征或实现。
- **`use`**：将符号引入作用域。
- **`where`**：表示约束类型的子句。
- **`while`**：根据表达式结果进行条件循环。

[union]: https://doc.rust-lang.org/stable/reference/items/unions.html

### 为将来保留的关键字

　　下列关键字目前尚无功能，但被 Rust 保留以备将来使用：

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### 原始标识符 {#raw-identifiers}

　　*原始标识符*（raw identifiers）是一种语法，让你可以在通常不允许使用关键字的地方使用关键字。做法是在关键字前加上前缀 `r#`。

　　例如，`match` 是关键字。若你尝试编译下面这个以 `match` 为名的函数：

<span class="filename">文件名：src/main.rs</span>

```rust
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

　　你会得到这样的错误：

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

　　错误表明不能把关键字 `match` 用作函数标识符。若要把 `match` 当作函数名，需要使用原始标识符语法，像这样：

<span class="filename">文件名：src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

　　这段代码可以无错误地编译。注意函数定义处以及在 `main` 中调用处，函数名都带有 `r#` 前缀。

　　原始标识符让你可以把任意词语用作标识符，哪怕它恰好是保留关键字。这让我们在选择标识符名称时更自由，也便于与那些不把这些词当作关键字的语言所写的程序集成。此外，原始标识符还允许你使用与当前 crate 不同 Rust edition 编写的库。例如，`try` 在 2015 edition 中不是关键字，但在 2018、2021 和 2024 edition 中是。若你依赖一个用 2015 edition 编写、且带有 `try` 函数的库，在较新的 edition 下调用该函数就需要使用原始标识符语法，此处即 `r#try`。关于 edition 的更多信息见[附录 E][appendix-e]。

[appendix-e]: ../05-e-editions/
