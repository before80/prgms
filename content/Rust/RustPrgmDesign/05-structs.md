+++
title = "05-使用结构体组织相关联的数据"
date = 2026-07-28T14:49:00+08:00
weight = 50
type = "docs"
description = "结构体定义、更新语法、impl 方法与关联函数的精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第5章

# 使用结构体组织相关联的数据

**结构体**（struct）：自定义类型，把多个相关值命名组合在一起（类似 OOP 的数据属性）。

## 结构体的定义和实例化

```rust
struct User {
    active: bool,
    username: String,
    email: String,
    sign_in_count: u64,
}

let user1 = User {
    email: String::from("someone@example.com"),
    username: String::from("someusername123"),
    active: true,
    sign_in_count: 1,
};

let email = user1.email;           // 点号访问
user1.active = false;              // 整个实例须 mut；不能单独 mut 字段
```

- 字段顺序与实例化顺序无关。
- 函数末尾构造 struct 可隐式返回。

### 使用字段初始化简写语法

参数名与字段名相同时：

```rust
fn build_user(email: String, username: String) -> User {
    User {
        email,      // 等价 email: email
        username,
        active: true,
        sign_in_count: 1,
    }
}
```

### 使用结构体更新语法创建实例

```rust
let user2 = User {
    email: String::from("another@example.com"),
    ..user1          // 其余字段从 user1 复制/移动，须放最后
};
```

- 类似赋值：`String` 字段会 **移动**；`Copy` 字段（如 `bool`、`u64`）复制后 `user1` 仍可用。

### 使用元组结构体创建不同的类型

```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

let black = Color(0, 0, 0);
let origin = Point(0, 0, 0);
// Color 与 Point 是不同类型
```

- 有类型名、无字段名；可解构 `let Point(x, y, z) = origin;` 或 `.0` 索引。

### 定义类单元结构体

```rust
struct AlwaysEqual;

let subject = AlwaysEqual;
```

- 无字段；常用于实现 trait 而无数据（第10章）。

> **结构体数据的所有权**：字段通常用 `String` 等 owned 类型；存引用 `&str` 需 **生命周期** 标注（第10章）。

## 结构体示例程序

用 `Rectangle` 算面积：独立变量 → 元组 → 结构体。

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

fn area(rectangle: &Rectangle) -> u32 {
    rectangle.width * rectangle.height
}
```

- 传 `&Rectangle` 借用，不移动所有权；字段访问不移动字段。

### 通过派生 trait 增加功能

```rust
#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

println!("rect1 is {rect1:?}");    // Debug
println!("rect1 is {rect1:#?}");  // 美化 Debug

let scale = 2;
let width = dbg!(30 * scale);     // 打印文件/行号/值，返回表达式值
dbg!(&rect1);
```

- `{}` 需要 `Display`；结构体默认无，用 `Debug` + `#[derive(Debug)]`。
- `dbg!` 输出到 **stderr**。

## 方法

**方法**：定义在 struct/enum/trait 上，第一个参数是 `self`。

### 方法语法

```rust
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

let rect1 = Rectangle { width: 30, height: 50 };
println!("{}", rect1.area());
```

- `impl` 块：关联类型与函数。
- `&self` = `self: &Self`：不可变借用；`&mut self` 可变；`self` 取得所有权（少见）。
- 方法与字段可同名：`rect1.width()` 是方法，`rect1.width` 是字段。

> Rust 无 `->`：方法调用时自动添加 `&` / `&mut` / `*` 匹配签名。

### 带有更多参数的方法

```rust
impl Rectangle {
    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
```

### 关联函数

- `impl` 内 **不以 `self` 为首参** 的函数 = **关联函数**（如 `String::from`）。
- 常用作构造函数：

```rust
impl Rectangle {
    fn square(size: u32) -> Self {
        Self { width: size, height: size }
    }
}

let sq = Rectangle::square(3);  // Type::function 语法
```

### 多个 `impl` 块

同一类型允许多个 `impl` 块（泛型/trait 场景常用）。

## 总结

- Struct：命名字段组合数据；简写 / 更新语法 / 元组 struct / 单元 struct
- 调试：`#[derive(Debug)]`、`{:?}`、`dbg!`
- `impl`：方法（`&self`）与关联函数（`Type::new()`）
