+++
title = "5.1 定义并实例化结构体"
date = 2026-08-05T08:44:00+08:00
weight = 20
type = "docs"
description = "定义并实例化结构体：字段、更新语法、元组结构体与类单元结构体"
isCJKLanguage = true
draft = false
rust_version = "1.97.1"

+++

> 译文 · 基于 [The Rust Programming Language](https://doc.rust-lang.org/stable/book/)（rustc 1.97.1）

# 定义并实例化结构体


> 原文链接: [https://doc.rust-lang.org/stable/book/ch05-01-defining-structs.html](https://doc.rust-lang.org/stable/book/ch05-01-defining-structs.html)


## 定义并实例化结构体

　　结构体与[「元组类型」](../../common-programming-concepts/02-data-types/)一节讨论的元组相似，两者都能存放多个相关值。和元组一样，结构体的各个部分可以是不同类型。与元组不同的是，结构体会为每一块数据命名，因而值的含义更清晰。有了这些名字，结构体比元组更灵活：你不必依赖数据的顺序来指定或访问实例中的值。

　　要定义结构体，先写关键字 `struct` 并为整个结构体命名。结构体的名字应能说明被组合在一起的这些数据有何意义。然后在花括号内定义各块数据的名字和类型，这些称为*字段*（field）。例如，示例 5-1 展示了一个存储用户账户信息的结构体。

**文件名：`src/main.rs`**
```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}
```

**示例 5-1：`User` 结构体的定义**

　　定义结构体之后，要使用它，就通过为每个字段指定具体值来创建该结构体的*实例*（instance）。创建实例时写上结构体名，再跟上花括号，其中是 *`key: value`* 对：键是字段名，值是要存入这些字段的数据。字段不必按结构体声明时的顺序指定。换言之，结构体定义像是该类型的通用模板，实例则用具体数据填充模板以创建该类型的值。例如，可以像示例 5-2 那样声明某个特定用户。

**文件名：`src/main.rs`**
```rust
fn main() {
    let user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };
}
```

**示例 5-2：创建 `User` 结构体的实例**

　　要从结构体取得特定值，使用点号语法。例如，访问该用户的邮箱地址可用 `user1.email`。若实例可变，可以用点号语法给某个字段赋值来修改它。示例 5-3 展示如何更改可变 `User` 实例的 `email` 字段。

**文件名：`src/main.rs`**
```rust
fn main() {
    let mut user1 = User {
        active: true,
        username: String::from("someusername123"),
        email: String::from("someone@example.com"),
        sign_in_count: 1,
    };

    user1.email = String::from("anotheremail@example.com");
}
```

**示例 5-3：更改 `User` 实例的 `email` 字段**

　　注意：整个实例必须可变；Rust 不允许只把某些字段标为可变。和任何表达式一样，我们可以在函数体的最后一个表达式中构造结构体的新实例，从而隐式返回该实例。

　　示例 5-4 展示一个 `build_user` 函数：它返回 `User` 实例，`email` 和 `username` 来自参数，`active` 为 `true`，`sign_in_count` 为 `1`。

**文件名：`src/main.rs`**
```rust
fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username: username,
        email: email,
        sign_in_count: 1,
    }
}
```

**示例 5-4：接受邮箱和用户名并返回 `User` 实例的 `build_user` 函数**

　　用与结构体字段相同的名字给函数参数命名很合理，但反复写 `email`、`username` 字段名和变量名有点繁琐。字段更多时更烦人。幸运的是，有便捷的简写！

### 使用字段初始化简写

　　因为示例 5-4 中参数名与结构体字段名完全相同，我们可以用*字段初始化简写*（field init shorthand）语法重写 `build_user`，行为完全一样，却不必重复 `username` 和 `email`，如示例 5-5 所示。

**文件名：`src/main.rs`**
```rust
fn build_user(email: String, username: String) -> User {
    User {
        active: true,
        username,
        email,
        sign_in_count: 1,
    }
}
```

**示例 5-5：因 `username` 和 `email` 参数与结构体字段同名而使用字段初始化简写的 `build_user`**

　　这里我们在创建 `User` 结构体的新实例，其中有一个名为 `email` 的字段。我们希望把该字段的值设为 `build_user` 函数中 `email` 参数的值。因为 `email` 字段与 `email` 参数同名，只需写 `email`，而不必写 `email: email`。

### 用结构体更新语法创建实例 {#creating-instances-from-other-instances-with-struct-update-syntax}

　　经常有用的是：基于同一类型的另一实例的大部分值创建新实例，只改其中一些。这时可以用结构体更新语法。

　　首先，示例 5-6 展示不用更新语法、按常规方式在 `user2` 中创建新 `User` 实例：为 `email` 设置新值，其余使用示例 5-2 中创建的 `user1` 的值。

**文件名：`src/main.rs`**
```rust
fn main() {
    // --snip--

    let user2 = User {
        active: user1.active,
        username: user1.username,
        email: String::from("another@example.com"),
        sign_in_count: user1.sign_in_count,
    };
}
```

**示例 5-6：使用 `user1` 中除一个字段外的全部值创建新的 `User` 实例**

　　使用结构体更新语法可以用更少代码达到同样效果，如示例 5-7 所示。`..` 语法指定：其余未显式设置的字段应与给定实例中的对应字段值相同。

**文件名：`src/main.rs`**
```rust
fn main() {
    // --snip--

    let user2 = User {
        email: String::from("another@example.com"),
        ..user1
    };
}
```

**示例 5-7：用结构体更新语法为 `User` 实例设置新的 `email`，其余值来自 `user1`**

　　示例 5-7 的代码同样在 `user2` 中创建实例：`email` 不同，但 `username`、`active` 和 `sign_in_count` 与 `user1` 相同。`..user1` 必须放在最后，表示其余字段从 `user1` 对应字段取值；但我们可以按任意顺序为任意数量的字段指定值，不必遵循结构体定义中的字段顺序。

　　注意：结构体更新语法像赋值一样使用 `=`，因为它会移动数据，正如我们在[「变量与数据的交互方式：移动」](../../understanding-ownership/01-what-is-ownership/#variables-and-data-interacting-with-move)一节所见。在这个例子中，创建 `user2` 之后就不能再使用 `user1`，因为 `user1` 的 `username` 字段中的 `String` 被移动到了 `user2`。若我们给 `user2` 的 `email` 和 `username` 都提供了新的 `String` 值，从而只从 `user1` 使用了 `active` 和 `sign_in_count`，那么创建 `user2` 后 `user1` 仍然有效。`active` 和 `sign_in_count` 都实现了 `Copy` 特征，因此适用[「仅栈上的数据：Copy」](../../understanding-ownership/01-what-is-ownership/#stack-only-data-copy)一节讨论的行为。在这个例子中我们仍可使用 `user1.email`，因为它的值没有从 `user1` 中移出。

### 用元组结构体创建不同的类型 {#creating-different-types-with-tuple-structs}

　　Rust 还支持与元组相似的结构体，称为*元组结构体*（tuple struct）。元组结构体拥有结构体名所提供的额外含义，但字段没有名字，只有类型。当你想给整个元组起名并使其成为与其他元组不同的类型，而像常规结构体那样为每个字段命名又显得冗长或多余时，元组结构体很有用。

　　定义元组结构体时，以 `struct` 关键字和结构体名开头，后跟元组中的类型。例如，这里定义并使用两个名为 `Color` 和 `Point` 的元组结构体：

**文件名：`src/main.rs`**
```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);
}
```

　　注意：`black` 和 `origin` 是不同类型，因为它们是不同元组结构体的实例。你定义的每个结构体都是独立类型，即便结构体内字段类型相同。例如，接受 `Color` 类型参数的函数不能接受 `Point` 作为实参，尽管两者都由三个 `i32` 组成。除此之外，元组结构体实例与元组类似：可以解构为各个部分，也可以用 `.` 后跟索引访问单个值。与元组不同的是，解构元组结构体时必须写出结构体类型名。例如，应写作 `let Point(x, y, z) = origin;`，才能把 `origin` 点中的值解构到名为 `x`、`y` 和 `z` 的变量中。

### 定义类单元结构体

　　你也可以定义没有任何字段的结构体！它们称为*类单元结构体*（unit-like struct），因为行为类似我们在[「元组类型」](../../common-programming-concepts/02-data-types/)一节提到的单元类型 `()`。当你需要在某个类型上实现特征、却又不想在类型本身中存储任何数据时，类单元结构体很有用。特征会在第 10 章讨论。下面是声明并实例化名为 `AlwaysEqual` 的单元结构体的例子：

**文件名：`src/main.rs`**
```rust
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;
}
```

　　定义 `AlwaysEqual` 时，使用 `struct` 关键字、我们想要的名字，然后是分号。不需要花括号或圆括号！然后可以用类似方式在 `subject` 变量中得到 `AlwaysEqual` 的实例：使用我们定义的名字，同样不带花括号或圆括号。想象以后我们会为该类型实现某种行为，使每个 `AlwaysEqual` 实例都恒等于任何其他类型的每个实例——或许是为了测试时有一个已知结果。实现那种行为并不需要任何数据！第 10 章会看到如何定义特征并在任意类型（包括类单元结构体）上实现它们。

> ### 结构体数据的所有权
>
> 在示例 5-1 的 `User` 结构体定义中，我们使用了拥有所有权的 `String` 类型，而不是 `&str` 字符串切片类型。这是有意为之：我们希望该结构体的每个实例都拥有其全部数据，并且只要整个结构体有效，这些数据就一直有效。
>
> 结构体也可以存储由别处拥有的数据的引用，但这需要使用*生命周期*（lifetime）——第 10 章会讨论的 Rust 特性。生命周期确保结构体引用的数据在结构体有效期间始终有效。假设你试图在结构体中存储引用却不指定生命周期，如下面 *src/main.rs* 所示；这行不通：
>
> **文件名：`src/main.rs`**
>
> ```rust
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
> 
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```

>
> 编译器会抱怨需要生命周期标注：
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> 第 10 章会讨论如何修复这些错误以便在结构体中存储引用；眼下我们用像 `String` 这样的拥有所有权的类型，而不是像 `&str` 这样的引用，来避开这类错误。


[tuples]: ../../common-programming-concepts/02-data-types/
[move]: ../../understanding-ownership/01-what-is-ownership/#variables-and-data-interacting-with-move
[copy]: ../../understanding-ownership/01-what-is-ownership/#stack-only-data-copy
