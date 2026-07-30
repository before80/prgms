+++
title = "programDesign"
date = 2026-07-21T11:27:22+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++



## rustup命令

### rustup update





## cargo 命令





## 编译后不输出`warning`信息

**方案 1**：临时全局屏蔽所有警告（一次性运行，最常用）

​	通过环境变量 `RUSTFLAGS` 给 `rustc` 统一传参，**所有代码（自身 + 依赖）都生效**

```sh
# Linux / macOS
RUSTFLAGS="-A warnings" cargo run

# Windows powerShell
$env:RUSTFLAGS="-A warnings"; cargo run

# Windows CMD
set RUSTFLAGS=-A warnings && cargo run
```

**方案 2**：只屏蔽当前项目代码警告（不影响依赖）

​	用 `cargo rustc` 编译再运行，分开两步：

```rust
# 编译时给 rustc 传参数
cargo rustc -- -A warnings
# 运行产物
./target/debug/你的包名
```

**方案 3**：永久项目全局关闭（Cargo.toml）

​	写入项目配置，每次构建自动生效：



## drop函数

drop函数是存放在堆中的数据对应的变量才可以调用?还是存放在栈中的数据对应的变量也可以调用?



## 常量

常量中的数据是否可以存放在堆中?



## 关联函数

> 来自: [https://kaisery.github.io/trpl-zh-cn/ch02-00-guessing-game-tutorial.html](https://kaisery.github.io/trpl-zh-cn/ch02-00-guessing-game-tutorial.html)

​	关联函数是针对某个类型实现的函数.

```rust
let mut guess = String::new();
```

​	`::new` 那一行的 `::` 语法表明 `new` 是 `String` 类型的一个 **关联函数**.

## `::`标记

1. 官方标准叫法：**路径分隔符（path separator）**. Rust 官方文档、Rust Reference 统一称 `::` 为 **path separator**，作用是分割命名空间路径。

2. 通俗别名（社区常用）
   1. **双冒号运算符**（最口语，大家日常交流都这么叫）
   2. **作用域解析运算符**（借鉴 C++ 说法，Rust 社区广泛通用）
      1. 对应 C++ `::`，功能相似：访问类型 / 模块关联项

3. 两种核心使用场景（对应猜数字教程里的代码）

   1. 场景 1：访问关联函数 / 关联常量（类型`::`函数）

      ```rust
      String::new();
      rand::Rng;
      ```

      `String::new`：`::` 表示 `new` 是**关联函数**，归属 `String` 类型，不是实例方法（实例用 `.`）

   2. 场景 2：模块 /crate 路径分层分隔

      ```rust
      use std::cmp::Ordering;
      std::io::stdin();
      ```

      `std::cmp::Ordering`：多层路径，`::` 分割 crate → 模块 → 枚举。

4.  和 `.` 点运算符区分（极易混淆）

   | 符号 | 名称                      | 用途                                          |
   | ---- | ------------------------- | --------------------------------------------- |
   | `::` | 路径分隔符 / 作用域解析符 | 访问**类型 / 模块**上的关联函数、常量、子模块 |
   | `.`  | 点运算符（方法调用符）    | 访问**实例对象**的方法、成员                  |

   ```rust
   // :: 类型关联函数
   let s = String::new();
   // . 实例方法
   s.read_line(&mut buf);
   ```

> 注意
>
> ​	语法层面，`::` 不是独立二元运算符，属于**路径语法的标记**，而 `+`/`*` 这种才是标准二元运算符；但日常开发沟通中，大家都会统称它为「`双冒号运算符`」。

## 表达式和语句

> 来自: [https://kaisery.github.io/trpl-zh-cn/ch03-03-how-functions-work.html#%E8%AF%AD%E5%8F%A5%E5%92%8C%E8%A1%A8%E8%BE%BE%E5%BC%8F](https://kaisery.github.io/trpl-zh-cn/ch03-03-how-functions-work.html#%E8%AF%AD%E5%8F%A5%E5%92%8C%E8%A1%A8%E8%BE%BE%E5%BC%8F)

**语句**（*Statements*）是执行一些操作但不返回值的指令。

**表达式**（*Expressions*）计算并产生一个值。

## 分支块 {} 是表达式

​	Rust 块 `{}` 本身是表达式：

- 块最后一行**不带分号**：该行表达式的值就是整个块的值；

- 块最后一行**带分号**：块的值为 `()`；

  示例 1：分支返回数字

  ```rust
  let x = if true {
      100 // 无分号，块值 = 100
  } else {
      200
  };
  // x = 100
  ```

  示例 2：分支末尾加分号，返回单元

  ```rust
  let x = if true {
      100; // 带分号，块值 = ()
  } else {
      200;
  };
  // x 的类型是 ()
  ```

  

## if表达式

​	整个 `if / else if / else` 是**单一表达式**，它的返回值 = **第一个匹配成功分支块 `{}` 的最终表达式的值**。

1. 每个分支 `{}` 块的值 = 块内**最后一行无分号表达式**；
2. 所有分支必须返回**同一种类型**，否则编译报错；
3. 如果缺少 `else`，且存在条件为 false 的路径，类型为 `()`（单元）。



​	但, `if`也可以当做语句进行使用: 只需要**不把它赋值给变量**，表达式求值后的返回值直接丢弃：

```rust
fn main() {
    let n = 5;

    // 这里 if 是表达式，但当作语句使用，丢弃返回值
    if n < 10 {
        println!("small");
    } else {
        println!("big");
    }

    println!("done");
}
```

**底层逻辑**：

​	整个 `if-else` 先算出一个值（这里是 `()`，因为 `println!` 带分号），然后没人接收这个值，直接丢弃，视觉和行为上和 C/C++ 的 if 语句完全一致。

​	你也可以在末尾显式加分号，效果完全相同（多一条空语句，不影响逻辑）：

```rust
if n < 10 {
    println!("small");
} else {
    println!("big");
}; // 末尾分号，主动丢弃返回值
```



> **注意**
>
> ```rust
> fn main() {
>     let unit = if 2 > 1 {
>         999
>     };
>     println!("{:?}", unit);
> }
> ```
>
> ​	以上代码编译时会报错:
>
> ```
> error[E0317]: `if` may be missing an `else` clause
>  --> src\main.rs:2:16
>   |
> 2 |       let unit = if 2 > 1 {
>   |  ________________^
> 3 | |         999
>   | |         --- found here
> 4 | |     };
>   | |_____^ expected integer, found `()`
>   |
>   = note: `if` expressions without `else` evaluate to `()`
>   = help: consider adding an `else` block that evaluates to the expected type
> ```
>
> **报错核心原因：缺少 `else` 分支，类型不统一**
>
> 1. 先看代码逻辑
>
> ```rust
> let unit = if 2 > 1 {
>     999
> };
> ```
>
> - 条件 `2 > 1` 为 `true`，会执行 `if` 块，返回 `999`（类型 `i32`）
>
> - 但 Rust 编译器会**考虑所有可能分支**：万一条件为 `false`，代码没有任何返回值路径
> - Rust 规定：不带 `else` 的 `if` 表达式整体类型必须是 `()`，但你 `if` 分支返回 `i32`，两种类型冲突，直接编译报错
>
> 2. 编译器视角拆解
>
>    1. 当 `if` 有 `else`：两条路径都有明确返回值，要求两边类型一致
>
>    2. 当 `if` **没有 `else`**：
>
>       - 条件成立：执行块，产生块的值
>
>       - 条件不成立：直接跳过整个 `if`，表达式求值为单元 `()` → 这就要求：`if` 分支内部的块求值结果必须也是 `()`，否则两条路径类型不一致
>
> 该代码中：
>
> - true 路径：返回 `999`（`i32`）
>
> - false 路径：返回 `()`类型 `i32`和 `()` 不匹配，编译器拒绝编译。
>
> 3. 两种修复方案
>
> **方案 1**：补上 `else`，让两条分支都是 `i32`（推荐，真正取值）
>
> ```rust
> let unit = if 2 > 1 {
>     999
> } else {
>     0 // else 分支也要返回数字，统一 i32
> };
> println!("{:?}", unit) // 输出 999
> ```
>
> **方案 2**：`if` 分支末尾加分号，让块返回 `()`，匹配无 `else` 的单元类型
>
> ```rust
> let unit = if 2 > 1 {
>     999; // 末尾分号，块的值变为 ()
> };
> println!("{:?}", unit); // 输出 ()
> ```





### let if

​	参见以上注意.



### if let

​	`if let` 是 Rust 中的一种控制流语法，允许你只匹配一种关心的模式，而忽略其他所有情况。它可以看作 `match` 的“简化版”，非常适合只处理一个分支的场景。下面从语法、原理、对比、解构、组合条件、链式写法等方面详细展开。

---

1. 基本语法

```rust
if let 模式 = 表达式 {
    // 匹配成功时执行的代码
} else {
    // 匹配失败时执行的代码（可选）
}
```

- **模式**：任意可反驳的模式（如 `Some(x)`、`Ok(v)`、枚举变体、元组、结构体等）。
- **表达式**：返回需要匹配的值。
- `else` 分支可选，用于处理匹配失败的情况。

---

2. 与 `match` 的对比

`match` 要求穷尽所有模式，即使你只关心其中一种：

```rust
let some_option = Some(42);

// 使用 match
match some_option {
    Some(x) => println!("值为 {x}"),
    None => {}          // 必须处理 None，即使什么都不做
}
```

用 `if let` 可以大幅简化：

```rust
if let Some(x) = some_option {
    println!("值为 {x}");
}
// 不关心 None，无需写 else
```

如果还想处理其他情况，可以加上 `else`：

```rust
if let Some(x) = some_option {
    println!("值为 {x}");
} else {
    println!("没有值");
}
```

`if let` 背后本质就是 `match` 的语法糖，编译器会将其展开成 `match`，但代码更短、语义更清晰。

---

3. 常见应用场景

3.1 处理 `Option`

只关心 `Some` 里的值：
```rust
let config = Some("debug");
if let Some(mode) = config {
    println!("当前模式：{mode}");
}
```

3.2 处理 `Result`

只关心成功的值：
```rust
let result: Result<i32, &str> = Ok(10);
if let Ok(num) = result {
    println!("得到数字：{num}");
} else {
    println!("出错了");
}
```

3.3 自定义枚举

```rust
enum Message {
    Quit,
    Move { x: i32, y: i32 },
    Write(String),
}

let msg = Message::Move { x: 3, y: 5 };

if let Message::Move { x, y } = msg {
    println!("移动到 ({x}, {y})");
}
```

---

4. 带额外条件的 `if let`（if let 与 `&&` 组合）

你可以在模式匹配成功后，立即用 `&&` 附加一个布尔条件，实现更细粒度的控制：

```rust
let num = Some(8);

if let Some(n) = num && n > 5 {
    println!("{n} 大于 5");
}
// 等价于：
// if let Some(n) = num {
//     if n > 5 { ... }
// }
```

- 条件会短路求值：只有模式匹配成功，才会检查 `&&` 后的表达式。
- 可以使用多个 `&&`，但不能直接与 `||` 混合（优先级问题）。如果确实需要 `||`，可以写成 `if (let Some(n) = num && n > 5) || other_condition`，但这样代码可读性变差，一般更推荐用 `match` 或嵌套 `if`。

---

5. 链式 `else if let`

类似 `else if`，可以连续匹配不同模式：

```rust
let value: Result<i32, &str> = Err("文件未找到");

if let Ok(n) = value {
    println!("成功：{n}");
} else if let Err(e) = value {
    println!("错误：{e}");
}
```

这对于匹配多个枚举变体且每个分支简单时，比 `match` 更清晰。

---

6. 解构复杂模式

`if let` 支持所有可反驳的模式解构，包括元组、结构体、枚举内嵌数据等。

```rust
let point = (3, 7);
if let (x, y) = point {
    println!("坐标：({x}, {y})");
}

struct Person { name: String, age: u8 }
let person = Some(Person { name: "Alice".into(), age: 30 });
if let Some(Person { name, age }) = person {
    println!("{name} 今年 {age} 岁");
}
```

---

7. 与 `ref` / `ref mut` 配合

当你想绑定引用而不获取所有权时，可在模式中使用 `ref`：

```rust
let maybe_string = Some(String::from("hello"));
if let Some(ref s) = maybe_string {
    // s 是 &String 类型，maybe_string 仍然可用
    println!("{}", s);
}
// maybe_string 依然有效
```

类似地，`ref mut` 可以获取可变引用。

---

8. `while let`：循环版本

`if let` 只执行一次，`while let` 则是循环形式，只要模式匹配就不断执行：

```rust
let mut stack = vec![1, 2, 3];
while let Some(top) = stack.pop() {
    println!("弹出 {top}");
}
```

它会一直弹出元素，直到 `pop()` 返回 `None`。

---

9. 特别注意：非穷尽性

`if let` 是非穷尽的，它只关心一种模式，所以**编译器不会强制你处理其他分支**。当逻辑确实只需要处理一种情况时，这很方便；但如果未来枚举增加新变体，`if let` 不会在编译时提醒你更新代码，而 `match` 会。这是需要权衡的地方。

---

10. 总结

- **简洁**：用于只关心一种匹配分支，减少样板代码。
- **解构能力强**：支持元组、结构体、枚举变体等复杂模式。
- **可与 `&&` 条件组合**：进行二次过滤。
- **链式使用**：`else if let` 可连续匹配不同模式。
- **循环支持**：`while let` 实现条件循环。

当你发现 `match` 中大多数分支都为空或简单处理时，`if let` 通常就是更合适的选择。





## loop表达式

## match表达式



## break语句

## continue语句

## while语句

### while let

## for 语句

### for in





## 所有权规则

1. Rust 中的每一个`值`都有`一个所有者`（*owner*）。
2. `值`在任一时刻有且只有`一个所有者`。
3. 当`所有者`离开`作用域`，这个`值`将被丢弃。
