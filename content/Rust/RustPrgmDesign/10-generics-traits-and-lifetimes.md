+++
title = "10-泛型、Trait和生命周期"
date = 2026-07-28T14:49:00+08:00
weight = 100
type = "docs"
description = "泛型语法、trait 约束与生命周期注解及省略规则精要"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [TRPL 简体中文](https://kaisery.github.io/trpl-zh-cn/) 第10章

# 泛型、Trait 和生命周期

**泛型**：类型/行为的抽象占位符。**Trait**：共享行为。**生命周期**：引用有效性的泛型参数。

## 提取函数来减少重复

1. 找重复代码 → 2. 提取函数（明确输入输出）→ 3. 调用替换重复处 → 4. 再推广为泛型。

## 泛型数据类型

### 在函数定义中使用泛型

```rust
fn largest<T>(list: &[T]) -> &T { /* ... */ }
```

- 类型参数惯例：单字母大驼峰，如 `T`。
- 需 trait 约束才能比较：`T: PartialOrd`（见下节）。

### 结构体定义中的泛型

```rust
struct Point<T> { x: T, y: T }
struct Point2<T, U> { x: T, y: U }
```

### 枚举定义中的泛型

```rust
enum Option<T> { Some(T), None }
enum Result<T, E> { Ok(T), Err(E) }
```

### 方法定义中的泛型

```rust
impl<T> Point<T> {
    fn x(&self) -> &T { &self.x }
}
impl Point<f32> {  // 仅 f32 的专用 impl
    fn distance_from_origin(&self) -> f32 { /* ... */ }
}
```

- `impl` 后声明的泛型可与结构体泛型不同（如 `mixup` 方法）。

### 泛型代码的性能

- **单态化**（monomorphization）：编译期为每个具体类型生成代码 → **零运行时泛型开销**。

## Trait：定义共同行为

- 类似其他语言的接口；定义方法签名集合。

### 定义 trait

```rust
pub trait Summary {
    fn summarize(&self) -> String;
}
```

### 为类型实现 trait

```rust
impl Summary for NewsArticle {
    fn summarize(&self) -> String { /* ... */ }
}
```

- **孤儿规则**（相干性）：trait 或类型至少一方属于当前 crate，才能 impl。
- 调用 trait 方法前需 `use Summary` 引入作用域。

### 使用默认实现

```rust
pub trait Summary {
    fn summarize(&self) -> String {
        String::from("(Read more...)")
    }
}
impl Summary for NewsArticle {}  // 用默认
```

- 默认实现可调用同 trait 其他方法；**不能**在 override 里调同名默认实现。

### 使用 trait 作为参数

```rust
pub fn notify(item: &impl Summary) { }
pub fn notify<T: Summary>(item: &T) { }           // trait 约束语法糖
pub fn notify(item1: &impl Summary, item2: &impl Summary) { }  // 可不同类型
pub fn notify<T: Summary>(item1: &T, item2: &T) { }            // 必须同类型
```

#### 通过 `+` 语法指定多个 trait 约束

```rust
fn notify(item: &(impl Summary + Display)) { }
fn notify<T: Summary + Display>(item: &T) { }
```

#### 通过 `where` 简化 trait 约束

```rust
fn foo<T, U>(t: &T, u: &U) -> i32
where
    T: Display + Clone,
    U: Clone + Debug,
{ }
```

### 返回实现了 trait 的类型

```rust
fn returns_summarizable() -> impl Summary { SocialPost { /* ... */ } }
```

- 仅当**单一具体返回类型**；多类型返回需 trait object（第18章）。

### 使用 trait 约束有条件地实现方法

```rust
impl<T: PartialOrd + Display> Pair<T> {
    fn cmp_display(&self) { /* ... */ }
}
```

- **Blanket implementation**：`impl<T: Display> ToString for T { }` — 见 trait 文档 Implementers。

## 生命周期确保引用有效

- 每个引用有**生命周期**（有效作用域）；注解描述**多个引用间关系**，不改变实际寿命。

### 悬垂引用

- 引用不能比被引用数据活得更久；**借用检查器**比较作用域。

### 函数中的泛型生命周期

```rust
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}
```

- 返回引用生命周期 = 两个参数中**较短**者。
- 若总返回某一参数，可只标注该参数；**不能**返回函数内新建值的引用（悬垂）。

### 生命周期注解语法

```rust
&i32
&'a i32
&'a mut i32
```

- 写在 `&` 之后，与类型空格分隔；参数名以 `'` 开头，常用 `'a`。

### 在函数签名中

- 生命周期参数写在 `<>` 中与泛型并列：`fn foo<'a>(x: &'a str) -> &'a str`

### 在结构体定义中

```rust
struct ImportantExcerpt<'a> {
    part: &'a str,
}
```

- 实例不能比 `part` 引用活得更久。

### 生命周期省略（Lifetime Elision）

编译器三条规则（fn/impl）：

1. 每个引用参数得一个生命周期参数。
2. **仅一个**输入生命周期 → 赋给所有输出。
3. 方法有 `&self` / `&mut self` → 输出生命周期 = `self` 的。

- `first_word(&str) -> &str` 可省略；`longest(x, y)` 两输入 → 规则2不适用，须显式标注。

### 在方法定义中

- 结构体 lifetime 写在 `impl<'a>`；有 `&self` 时输出常随 `self`（规则3）。

### 静态生命周期

```rust
let s: &'static str = "I have a static lifetime.";
```

- 字面值存于二进制，全程有效；勿滥用 `'static` 掩盖生命周期错误。

### 泛型类型参数、trait 约束和生命周期

```rust
fn longest<'a, T>(x: &'a str, y: &'a str, ann: T) -> &'a str
where
    T: Display,
{ /* ... */ }
```
