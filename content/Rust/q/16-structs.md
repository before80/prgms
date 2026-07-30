+++
title = "16-structs"
date = 2026-07-28T14:49:00+08:00
weight = 160
type = "docs"
description = "面向 Go 程序员讲清结构体定义、方法、更新语法与所有权影响"
isCJKLanguage = true
draft = false

+++

# 结构体 (Structs)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把 Rust struct 当成“没有 GC 的 Go struct”，结果在 `..base`、方法接收者上连环报错？
- 你是否分不清 `self` / `&self` / `&mut self`，以及关联函数和方法的差别？
- 你会不会在字段默认私有、`derive`、newtype、带生命周期字段这些题上反复踩坑？
- 你是否想知道：什么时候该 Builder、什么时候该拥有 `String`、什么时候该借 `&str`？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| struct | — | 结构体 | 把相关字段聚合成一个类型 | `struct` |
| field | — | 字段 | 结构体里的命名成员 | 结构体字段 |
| `impl` | implementation | 实现块 | 给类型挂方法和关联函数的地方 | 方法集合（无独立语法） |
| receiver | — | 方法接收者 | 方法第一个参数：`self` / `&self` / `&mut self` | 值/指针接收者 |
| associated function | — | 关联函数 | `impl` 里没有 `self` 的函数，常用 `Type::new` | 包级构造函数近亲 |
| update syntax | — | 更新语法 | `User { active: false, ..base }` 从 base 补齐其余字段 | 无直接语法糖 |
| partial move | — | 部分移动 | 只移走结构体里部分非 `Copy` 字段 | Go 无对应 |
| newtype | — | 新类型包装 | 单字段元组结构体，用来区分语义 | 自定义命名类型近亲 |
| `ZST` | Zero-Sized Type | 零大小类型 | 编译期大小为 0 的类型（如单元结构体） | 无直接对应 |
| `RAII` | Resource Acquisition Is Initialization | 资源获取即初始化 | 资源跟着值的生命周期自动释放 | 常靠 `defer` |
| `GC` | Garbage Collector | 垃圾回收器 | 运行时回收不用对象 | Go 默认机制 |
| lifetime | — | 生命周期 | 引用有效存活区间的编译期标注 | 无显式对应 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q17](#q17) |
| `common` | [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q18](#q18), [Q19](#q19) |
| `occasional` | [Q12](#q12), [Q13](#q13), [Q14](#q14) |
| `advanced` | [Q15](#q15), [Q16](#q16) |

---

## Q1. Rust 结构体和 Go struct 最像的地方是什么？ {#q1}
**Tags:** `hot` `beginner` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

都是“把相关字段捆成一个类型”；差别在于 Rust 还把所有权、可见性和方法接收者一起编进这个类型里。

**解答：**

Go 的 struct 主要是字段聚合；Rust 的 struct 同样聚合字段，但字段类型一旦带上 `String`、`Vec` 等拥有型数据，赋值、传参、`..base` 更新都会触发 move 规则。先把三种形式认全：命名字段结构体、元组结构体、单元结构体（**ZST**，Zero-Sized Type，零大小类型）。

```rust
struct User {
    name: String,
    active: bool,
}

struct Point(i32, i32);

struct Marker;

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    let p = Point(1, 2);
    let _m = Marker;
    println!("{} {} {}", u.name, p.0, u.active);
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn build(name: String, active: bool) -> User {
    User { name, active } // 字段初始化简写：变量名与字段名相同
}

fn main() {
    let u = build(String::from("Ada"), true);
    println!("{} {}", u.name, u.active);
}
```

```rust
#[derive(Debug)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    println!("{u:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u := User{Name: "Ada", Active: true}
	fmt.Println(u.Name, u.Active)
}
```

- **Go 怎么做**：struct 字段聚合 + 方法，值复制很常见。
- **Rust 为什么不同**：类型还要回答“谁拥有堆数据、谁能改、谁能从外部构造”。
- **Go 程序员易踩的坑**：把带 `String` 的 struct 当成随手复制的小值。

---

## Q2. 为什么字段里有 `String` 就会牵出所有权问题？ {#q2}
**Tags:** `hot` `beginner` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` 拥有堆上的 UTF-8 字节；结构体拥有这个 `String`，所以结构体赋值/传参默认是 move，不是“便宜拷贝一份”。

**解答：**

Go 里 `string` 头复制很便宜，原变量通常还能用。Rust 里 `String` 不是 `Copy`：把整个 `User` 赋给别人，等于把 `name` 的所有权也交出去。只想临时看一眼时，借 `&User` 或 `&str`。

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = u1;
    println!("{} {}", u2.name, u2.active);
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = u1;
    println!("{}", u1.name);
    // error[E0382]: borrow of moved value: `u1`
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn show(u: &User) {
    println!("{} {}", u.name, u.active);
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    show(&u);
    println!("{}", u.name); // 仍可用：只是借出去看过
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u1 := User{Name: "Ada", Active: true}
	u2 := u1
	fmt.Println(u1.Name, u2.Name)
}
```

- **Go 怎么做**：赋值通常复制 struct 值（含 string 头）。
- **Rust 为什么不同**：非 `Copy` 字段让整个结构体默认走 move，避免双释放。
- **Go 程序员易踩的坑**：赋值后继续用旧变量，撞上 `E0382`。

---

## Q3. 结构体更新语法 `..base` 到底做了什么？ {#q3}
**Tags:** `hot` `beginner` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

`User { active: false, ..base }` 用你写明的字段覆盖，其余字段从 `base` 搬过来；非 `Copy` 字段会被 move，这叫 **partial move**（部分移动）。

**解答：**

`..base` 必须写在结构体字面量最后。它不是“浅拷贝一份再改”，而是：未写出的字段按所有权规则从 `base` 取走。`bool`/`i32` 等 `Copy` 字段取走后原值仍可读；`String` 取走后原字段失效，整个 `base` 也不能再按值使用。要两边都留着，就 `..base.clone()`（需 `#[derive(Clone)]`，写在该 struct 定义正上方）。

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        ..u1
    };
    println!("{} {}", u2.name, u2.active);
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        ..u1
    };
    println!("{}", u1.name);
    // error[E0382]: borrow of moved value: `u1.name`
    println!("{}", u2.active);
}
```

```rust
#[derive(Clone)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        ..u1.clone()
    };
    println!("{} {}", u1.name, u2.active);
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u1 := User{Name: "Ada", Active: true}
	u2 := u1
	u2.Active = false
	fmt.Println(u1.Name, u1.Active, u2.Active)
}
```

- **Go 怎么做**：先整份赋值，再改字段；两边都还在。
- **Rust 为什么不同**：更新语法默认搬所有权，避免悄悄复制堆数据。
- **Go 程序员易踩的坑**：写完 `..u1` 还以为 `u1.name` 能继续用。

---

## Q4. 方法接收者 `self` / `&self` / `&mut self` 怎么选？ {#q4}
**Tags:** `hot` `beginner` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

只读用 `&self`，要改字段用 `&mut self`，要消费/转换所有权才用 `self`。

**解答：**

这对应 Go 的值接收者 / 指针接收者，但 Rust 更严：`&self` 不能改；`self` 会把调用方手里的值吃掉。日常 API 默认 `&self` / `&mut self`；构建器收尾、`into_*` 转换再用 `self`。

```rust
struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn area(&self) -> u32 {
        self.w * self.h
    }

    fn grow(&mut self, dw: u32) {
        self.w += dw;
    }

    fn into_area(self) -> u32 {
        self.w * self.h
    }
}

fn main() {
    let mut r = Rect { w: 3, h: 4 };
    println!("{}", r.area());
    r.grow(1);
    println!("{}", r.into_area());
}
```

```rust
struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn into_area(self) -> u32 {
        self.w * self.h
    }
}

fn main() {
    let r = Rect { w: 3, h: 4 };
    let a = r.into_area();
    println!("{}", r.w);
    // error[E0382]: borrow of moved value: `r`
    println!("{a}");
}
```

```rust
struct Counter {
    n: i32,
}

impl Counter {
    fn bump(&mut self) {
        self.n += 1;
    }
}

fn main() {
    let mut c = Counter { n: 0 };
    c.bump();
    println!("{}", c.n);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Rect struct{ W, H uint }

func (r Rect) Area() uint { return r.W * r.H }

func (r *Rect) Grow(dw uint) { r.W += dw }

func main() {
	r := Rect{W: 3, H: 4}
	fmt.Println(r.Area())
	r.Grow(1)
	fmt.Println(r.W)
}
```

- **Go 怎么做**：值/指针接收者都能写，编译器较少阻止“用完还用”。
- **Rust 为什么不同**：接收者签名直接编码借用或消费。
- **Go 程序员易踩的坑**：把该 `&self` 的查询写成 `self`，调用后原值没了。

---

## Q5. 关联函数和方法差在哪？ {#q5}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

关联函数没有 `self`，用 `Type::name(...)` 调用；方法有接收者，用 `value.name(...)` 调用。

**解答：**

最常见的关联函数是构造器 `new`。`Self` 是当前类型别名，写在 `impl Type` 里等于写 `Type`。Go 没有完全同构的语法，通常是包级 `NewXxx` 或返回指针的工厂函数。

```rust
struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn new(w: u32, h: u32) -> Self {
        Self { w, h }
    }

    fn area(&self) -> u32 {
        self.w * self.h
    }
}

fn main() {
    let r = Rect::new(3, 4);
    assert_eq!(r.area(), 12);
}
```

```rust
struct Rect {
    w: u32,
    h: u32,
}

impl Rect {
    fn square(side: u32) -> Self {
        Self { w: side, h: side }
    }
}

fn main() {
    let r = Rect::square(5);
    println!("{} {}", r.w, r.h);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Rect struct{ W, H uint }

func NewRect(w, h uint) Rect { return Rect{W: w, H: h} }

func (r Rect) Area() uint { return r.W * r.H }

func main() {
	r := NewRect(3, 4)
	fmt.Println(r.Area())
}
```

- **Go 怎么做**：工厂函数 + 方法分开写。
- **Rust 为什么不同**：两者都进同一个 `impl`，但调用语法不同。
- **Go 程序员易踩的坑**：对关联函数写 `r.new(...)`，或对方法写 `Rect::area(r)` 却忘了接收者形式。

---

## Q6. 什么时候该 `derive(Debug)`？ {#q6}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

几乎所有要 `println!("{x:?}")`、测日志、看断言失败信息的类型，都应在定义上方加 `#[derive(Debug)]`。

**解答：**

写在 `struct` / `enum` 定义正上方：`#[derive(Debug)]`。字段类型也必须实现 `Debug`，否则 derive 失败。Go 常用 `%+v`；Rust 没有默认万能打印，需要 `Debug`。

```rust
#[derive(Debug)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    println!("{u:?}");
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    println!("{u:?}");
    // error[E0277]: `User` doesn't implement `Debug`
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u := User{Name: "Ada", Active: true}
	fmt.Printf("%+v\n", u)
}
```

- **Go 怎么做**：`fmt` 对结构体开箱即用。
- **Rust 为什么不同**：调试打印是显式 trait，避免默认可打印敏感字段时无约束。
- **Go 程序员易踩的坑**：一上来就 `{u:?}`，却忘了 `derive(Debug)`。

---

## Q7. 什么时候该 `derive(Clone)`，什么时候不该？ {#q7}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

需要显式复制（例如 `..base.clone()`、放入多处拥有者）时 derive；持有不可克隆资源（文件句柄、锁、唯一 ID）时不要盲目 derive。

**解答：**

`Clone` 是显式深/浅复制约定（对 `String` 是再分配一份堆数据）。写在类型定义上方：`#[derive(Clone)]`。若字段不能 `Clone`，要么手写 `Clone`，要么改设计。不要用 `Clone` 掩盖本该借用的 API。

```rust
#[derive(Clone, Debug)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = u1.clone();
    println!("{u1:?} {u2:?}");
}
```

```rust
#[derive(Clone)]
struct User {
    name: String,
    active: bool,
}

fn main() {
    let u1 = User {
        name: String::from("Ada"),
        active: true,
    };
    let u2 = User {
        active: false,
        ..u1.clone()
    };
    println!("{} {}", u1.name, u2.active);
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u1 := User{Name: "Ada", Active: true}
	u2 := u1 // 值拷贝
	fmt.Println(u1, u2)
}
```

- **Go 怎么做**：赋值常常已经拷贝了值头。
- **Rust 为什么不同**：复制要显式，避免隐藏的堆分配。
- **Go 程序员易踩的坑**：到处 `.clone()` 消错，却不改接收者/借用设计。

---

## Q8. 元组结构体有什么用？ {#q8}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

给“有类型、但字段名不重要”的值起名，例如坐标点、像素颜色；也常作 newtype 的载体。

**解答：**

用 `.0`、`.1` 访问。比裸元组更可读，又能挂方法。字段很多、语义复杂时仍应用命名字段结构体。

```rust
struct Point(i32, i32);

impl Point {
    fn dist2(&self) -> i32 {
        self.0 * self.0 + self.1 * self.1
    }
}

fn main() {
    let p = Point(3, 4);
    println!("{} {}", p.0, p.dist2());
}
```

```rust
struct Color(u8, u8, u8);

fn main() {
    let c = Color(255, 128, 0);
    println!("rgb({},{},{})", c.0, c.1, c.2);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Point struct{ X, Y int }

func main() {
	p := Point{X: 3, Y: 4}
	fmt.Println(p.X, p.Y)
}
```

- **Go 怎么做**：几乎总是命名字段。
- **Rust 为什么不同**：元组结构体在“轻量命名类型”场景更短。
- **Go 程序员易踩的坑**：把元组结构体当匿名 tuple，忘记它已是独立类型、不能和 `(i32,i32)` 混用。

---

## Q9. newtype 模式为什么常见？ {#q9}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

用单字段元组结构体包一层，让 `UserId` 和 `i64`、`Meters` 和 `f64` 在类型上不能混用，并单独实现行为。

**解答：**

写在业务模块的 `types.rs` 或同文件类型区：`struct UserId(u64);`。需要时再 `impl UserId { ... }`。这比 Go 的 `type UserId int64` 更强：Rust 不会自动当成底层类型用。

```rust
struct UserId(u64);

impl UserId {
    fn get(self) -> u64 {
        self.0
    }
}

fn main() {
    let id = UserId(42);
    println!("{}", id.get());
}
```

```rust
struct Meters(f64);
struct Seconds(f64);

fn speed(dist: Meters, time: Seconds) -> f64 {
    dist.0 / time.0
}

fn main() {
    let d = Meters(100.0);
    let t = Seconds(9.58);
    println!("{}", speed(d, t));
}
```

**Go 对比：**

```go
package main

import "fmt"

type UserId int64

func main() {
	var id UserId = 42
	fmt.Println(int64(id))
}
```

- **Go 怎么做**：定义类型别名式命名类型，转换仍很常见。
- **Rust 为什么不同**：newtype 是真正的新类型，默认不与底层类型互通。
- **Go 程序员易踩的坑**：期望 `UserId` 能直接当 `u64` 做算术。

---

## Q10. 字段默认私有意味着什么？ {#q10}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

即使 `pub struct`，字段默认仍私有；模块外不能直接写字面量构造，也不能读私有字段，除非字段标 `pub` 或你提供构造器/访问器。

**解答：**

在定义字段处写 `pub name: String` 才导出字段。更常见做法：结构体 `pub`，字段私有，在同模块 `impl` 里提供 `pub fn new(...)`。这比 Go 的首字母大小写导出更细：类型公开 ≠ 字段公开。

```rust
mod account {
    pub struct User {
        pub name: String,
        active: bool,
    }

    impl User {
        pub fn new(name: String, active: bool) -> Self {
            Self { name, active }
        }

        pub fn active(&self) -> bool {
            self.active
        }
    }
}

fn main() {
    let u = account::User::new(String::from("Ada"), true);
    println!("{} {}", u.name, u.active());
}
```

```rust
mod account {
    pub struct User {
        pub name: String,
        active: bool,
    }
}

fn main() {
    let _u = account::User {
        name: String::from("Ada"),
        active: true,
    };
    // error[E0451]: field `active` of struct `User` is private
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	active bool // 包外不可见
}

func main() {
	u := User{Name: "Ada"}
	fmt.Println(u.Name)
}
```

- **Go 怎么做**：靠标识符首字母控制导出。
- **Rust 为什么不同**：`pub` 可标在类型和每个字段上，粒度更细。
- **Go 程序员易踩的坑**：以为 `pub struct` 就能在外部用字段字面量随便拼。

---

## Q11. 为什么结构体参数常优先借用而不是按值拿走？ {#q11}
**Tags:** `common` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

按值会 move（或大结构体按位复制）；只读用 `&T`，要改用 `&mut T`，只有转移所有权时才接 `T`。

**解答：**

这和 [Q4](#q4) 同一套直觉。小 `Copy` 结构体按值传也可以；带堆数据或较大时，借用更省事，也让调用方继续拥有原值。

```rust
struct User {
    name: String,
    active: bool,
}

fn label(u: &User) -> String {
    format!("{}:{}", u.name, u.active)
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    println!("{}", label(&u));
    println!("{}", u.name);
}
```

```rust
struct User {
    name: String,
    active: bool,
}

fn consume(u: User) -> String {
    u.name
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        active: true,
    };
    let name = consume(u);
    println!("{name}");
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func Label(u User) string {
	return fmt.Sprintf("%s:%v", u.Name, u.Active)
}

func main() {
	u := User{Name: "Ada", Active: true}
	fmt.Println(Label(u), u.Name)
}
```

- **Go 怎么做**：值传递很常见，大结构体才改指针。
- **Rust 为什么不同**：非 `Copy` 按值等于移交所有权。
- **Go 程序员易踩的坑**：API 到处接 `User`，调用方被迫不断 clone。

---

## Q12. 带生命周期的结构体什么时候值得写？ {#q12}
**Tags:** `occasional` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

结构体需要“借用别人的数据且不拥有它”时才写生命周期参数；能改成拥有 `String`/`Vec` 往往更简单。

**解答：**

写法：`struct View<'a> { text: &'a str }`，`'a` 写在类型名后、字段引用上。含义是：`View` 不能比它借用的 `str` 活得更久。Go 靠 GC 持有底层数据；Rust 要你在类型上写清借用关系。初学优先拥有型字段。

```rust
struct View<'a> {
    text: &'a str,
}

fn main() {
    let s = String::from("hello");
    let v = View { text: &s };
    println!("{}", v.text);
}
```

```rust
struct View<'a> {
    text: &'a str,
}

fn main() {
    let v;
    {
        let s = String::from("hello");
        v = View { text: &s };
    }
    println!("{}", v.text);
    // error[E0597]: `s` does not live long enough
}
```

**Go 对比：**

```go
package main

import "fmt"

type View struct{ Text string }

func main() {
	s := "hello"
	v := View{Text: s}
	fmt.Println(v.Text)
}
```

- **Go 怎么做**：字符串数据由运行时管理，结构体里存 string 很轻松。
- **Rust 为什么不同**：借用字段必须声明“我依赖谁还活着”。
- **Go 程序员易踩的坑**：一上来就在 struct 里塞满 `&str`，被生命周期淹没。

---

## Q13. 为什么自引用结构体不好做？ {#q13}
**Tags:** `occasional` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

字段不能安全地既拥有一块数据、又同时持有指向自己内部的引用；搬家/move 会让内部指针失效。

**解答：**

Go 里指针指自己很常见。Rust 里普通引用结构体在 move 后地址可能变，编译器拒绝这种自引用。常见替代：把数据放一起、用索引代替内部指针，或拆成“拥有缓冲 + 临时借用视图”两个类型。需要真正自引用时才考虑 `Pin` 等进阶工具（本篇不展开）。

```rust
struct Owns {
    data: String,
}

fn main() {
    let o = Owns {
        data: String::from("hello"),
    };
    let view: &str = &o.data;
    println!("{view}");
}
```

```rust
// 签名示意，非完整程序：下面这种“结构体字段引用自己另一字段”的模式
struct Bad {
    data: String,
    // view: &str, // 想指向 data —— 生命周期与 move 语义都会卡住
}
```

**Go 对比：**

```go
package main

import "fmt"

type Node struct {
	Val  int
	Self *Node
}

func main() {
	n := &Node{Val: 1}
	n.Self = n
	fmt.Println(n.Self.Val)
}
```

- **Go 怎么做**：结构体里存指向自己的指针很自然。
- **Rust 为什么不同**：默认 move 可能改变地址，内部引用会悬空。
- **Go 程序员易踩的坑**：把链表/图直接按 Go 指针思维平移过来。

---

## Q14. Builder 模式在 Rust 里为什么常见？ {#q14}
**Tags:** `occasional` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

字段多、可选配置多、又想保持字段私有/一次构造完整时，用 Builder 逐步设置，最后 `build()` 产出拥有型值。

**解答：**

通常在同一文件或 `foo/builder.rs` 里写 `FooBuilder`，方法接 `&mut self` 或 `self`（链式），`build(self) -> Foo`。这比一长串构造参数清晰，也比外部随意改私有字段安全。

```rust
struct Config {
    host: String,
    port: u16,
}

struct ConfigBuilder {
    host: String,
    port: u16,
}

impl ConfigBuilder {
    fn new() -> Self {
        Self {
            host: String::from("127.0.0.1"),
            port: 8080,
        }
    }

    fn host(mut self, host: impl Into<String>) -> Self {
        self.host = host.into();
        self
    }

    fn port(mut self, port: u16) -> Self {
        self.port = port;
        self
    }

    fn build(self) -> Config {
        Config {
            host: self.host,
            port: self.port,
        }
    }
}

fn main() {
    let c = ConfigBuilder::new().host("localhost").port(3000).build();
    println!("{}:{}", c.host, c.port);
}
```

```rust
struct Config {
    host: String,
    port: u16,
}

impl Config {
    fn new(host: String, port: u16) -> Self {
        Self { host, port }
    }
}

fn main() {
    let c = Config::new(String::from("localhost"), 3000);
    println!("{}:{}", c.host, c.port);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Config struct {
	Host string
	Port uint16
}

func main() {
	c := Config{Host: "localhost", Port: 3000}
	fmt.Println(c.Host, c.Port)
}
```

- **Go 怎么做**：常用结构体字面量 + functional options。
- **Rust 为什么不同**：字段私有 + 所有权让 Builder/`new` 更常见。
- **Go 程序员易踩的坑**：对外暴露所有字段，失去不变量保护。

---

## Q15. Go 的匿名字段直觉在 Rust 里能直接迁移吗？ {#q15}
**Tags:** `advanced` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

不能直接迁移：Rust 没有 Go 那种匿名字段提升；要组合就显式嵌套字段，要复用行为就用 trait 或手动委托方法。

**解答：**

Go 的嵌入会把内嵌类型的方法“提升”到外层。Rust 写 `struct Dog { pet: Pet }` 后，调用的是 `dog.pet.speak()`，除非你手写转发方法或实现相同 trait。这更啰嗦，但类型关系更清晰。

```rust
struct Pet {
    name: String,
}

impl Pet {
    fn greet(&self) -> String {
        format!("hi {}", self.name)
    }
}

struct Dog {
    pet: Pet,
    breed: String,
}

impl Dog {
    fn greet(&self) -> String {
        self.pet.greet()
    }
}

fn main() {
    let d = Dog {
        pet: Pet {
            name: String::from("Rex"),
        },
        breed: String::from("corgi"),
    };
    println!("{} {}", d.greet(), d.breed);
}
```

```rust
struct Pet {
    name: String,
}

struct Dog {
    pet: Pet,
}

fn main() {
    let d = Dog {
        pet: Pet {
            name: String::from("Rex"),
        },
    };
    println!("{}", d.pet.name);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Pet struct{ Name string }

func (p Pet) Greet() string { return "hi " + p.Name }

type Dog struct {
	Pet
	Breed string
}

func main() {
	d := Dog{Pet: Pet{Name: "Rex"}, Breed: "corgi"}
	fmt.Println(d.Greet(), d.Name, d.Breed)
}
```

- **Go 怎么做**：匿名字段自动提升字段/方法。
- **Rust 为什么不同**：偏好显式字段访问与 trait，避免隐式提升。
- **Go 程序员易踩的坑**：以为嵌套 struct 会自动拥有内层方法。

---

## Q16. 本章最实用的结构体设计准则是什么？ {#q16}
**Tags:** `advanced` `struct`
**适用版本:** Rust 1.0+

**一句话答案：**

字段默认私有 + 构造器约束不变量；能借用就别拿走；需要复制再 `Clone`；更新语法想保留原值就 `clone`；别一上来自引用和复杂生命周期。

**解答：**

落地检查清单：

1. 字段类型先选拥有型（`String`/`Vec`），确认 API 稳定后再考虑借用字段。
2. 方法接收者默认 `&self`/`&mut self`。
3. `..base` 后假设非 `Copy` 字段已 move。
4. 导出类型时优先 `new`/Builder，而不是把所有字段 `pub`。
5. `Debug` 常开；`Clone`/`Copy` 按语义开，不按“好写”开。

```rust
#[derive(Debug, Clone)]
struct User {
    name: String,
    active: bool,
}

impl User {
    fn new(name: impl Into<String>) -> Self {
        Self {
            name: name.into(),
            active: true,
        }
    }

    fn deactivate(&mut self) {
        self.active = false;
    }
}

fn main() {
    let mut u = User::new("Ada");
    u.deactivate();
    let u2 = User {
        active: true,
        ..u.clone()
    };
    println!("{u:?} {u2:?}");
}
```

```rust
struct User {
    name: String,
}

fn show(u: &User) {
    println!("{}", u.name);
}

fn main() {
    let u = User {
        name: String::from("Ada"),
    };
    show(&u);
    show(&u);
}
```

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	u := User{Name: "Ada", Active: true}
	u.Active = false
	fmt.Println(u)
}
```

- **Go 怎么做**：字面量 + 导出字段往往就够用。
- **Rust 为什么不同**：所有权与可见性迫使你更早定 API 边界。
- **Go 程序员易踩的坑**：用“先全 pub、再到处 clone”硬扛编译器。

---

## Q17. 为什么能同时改两个字段，却常不能「借字段 A 再改字段 B」？ {#q17}
**Tags:** `hot` `struct` `borrow` `split-borrow`
**适用版本:** Rust 1.0+

**一句话答案：**

对**结构体字段**的直接访问，编译器可以做**拆分借用**（各字段互不重叠就能同时借）；但方法接收者是整个 `self`，经 `&self`/`&mut self` 返回的字段引用会把**整棵结构体**借住，于是再改另一个字段就冲突。

**解答：**

直接改两个字段没问题——两次都是短命的独占访问，不重叠：

```rust
struct Pair {
    a: i32,
    b: i32,
}

fn bump_both(p: &mut Pair) {
    p.a += 1;
    p.b += 1;
}

fn main() {
    let mut p = Pair { a: 1, b: 2 };
    bump_both(&mut p);
    println!("{} {}", p.a, p.b);
}
```

字段级拆分借用也合法：

```rust
struct Pair {
    a: i32,
    b: i32,
}

fn main() {
    let mut p = Pair { a: 1, b: 2 };
    let ra = &mut p.a;
    let rb = &mut p.b; // OK：不同字段
    *ra += 10;
    *rb += 20;
    println!("{} {}", p.a, p.b);
}
```

一换成「方法借出字段」，借用范围变成整个 `self`：

```rust
struct Pair {
    a: i32,
    b: i32,
}

impl Pair {
    fn a_ref(&self) -> &i32 {
        &self.a
    }
}

fn main() {
    let mut p = Pair { a: 1, b: 2 };
    let ra = p.a_ref();
    // p.b += 1;
    // error[E0502]: cannot borrow `p` as mutable because it is also borrowed as immutable
    println!("{ra}");
    p.b += 1; // 等 ra 用完再改就行
}
```

排错：能写 `p.a` / `p.b` 就别绕一层返回 `&self` 字段的 getter；真要长期同时持有多字段，用局部拆分借用，或把数据拆成更小的类型。

**Go 对比：**

```go
package main

import "fmt"

type Pair struct{ A, B int }

func (p *Pair) ARef() *int { return &p.A }

func main() {
	p := &Pair{A: 1, B: 2}
	a := p.ARef()
	p.B++ // Go 允许；别名与数据竞争要靠人看
	fmt.Println(*a, p.B)
}
```

- **Go 怎么做**：指针别名默认允许，靠纪律与 race detector。
- **Rust 为什么不同**：借用检查按「借了谁」算；方法签名常把范围放大到整个结构体。
- **Go 程序员易踩的坑**：到处写 `fn name(&self) -> &str`，再在同作用域改别的字段，撞 `E0502`。

**记忆点：**

- 字段直接访问 → 可拆分借用。
- `&self` 方法借出字段 → 锁住整个 `self`。
- 冲突时：缩短借用、改直接字段访问，或拆类型。

---

## Q18. `#[derive(Default)]` 和手写 `Default` 怎么选？ {#q18}
**Tags:** `common` `struct` `default` `derive`
**适用版本:** Rust 1.0+

**一句话答案：**

字段**全都**实现了 `Default`、且「全零/全默认」语义正确时用 `derive`；任一字段没有 `Default`、或默认值不是类型默认（例如 `active: true`），就手写 `impl Default`。

**解答：**

derive 要求每个字段都 `Default`，生成「字段各自 default 再拼起来」：

```rust
#[derive(Debug, Default)]
struct Config {
    retries: u32,     // 0
    verbose: bool,    // false
}

fn main() {
    let c = Config::default();
    println!("{c:?}");
}
```

需要自定义默认时手写：

```rust
#[derive(Debug)]
struct User {
    name: String,
    active: bool,
}

impl Default for User {
    fn default() -> Self {
        Self {
            name: String::from("anonymous"),
            active: true, // 不是 bool 的 Default(false)
        }
    }
}

fn main() {
    let u = User::default();
    println!("{u:?}");
}
```

字段含无 `Default` 的类型时，derive 直接失败（示意）：

```text
error[E0277]: the trait bound `MyId: Default` is not satisfied
// #[derive(Default)]
// struct Wrap { id: MyId }
```

也可只给部分场景提供 `User::new(...)`，不必强行 `Default`；`Default` 适合「空配置 / 占位 / `..Default::default()` 更新语法」。

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name   string
	Active bool
}

func main() {
	var u User // 零值："" / false
	fmt.Println(u)
}
```

- **Go 怎么做**：`var u T` 就是零值默认。
- **Rust 为什么不同**：没有隐式零值构造；要默认就实现 / derive `Default`。
- **Go 程序员易踩的坑**：以为 `User { .. }` 能省略字段；Rust 必须写全或 `..Default::default()`。

**记忆点：**

- 全字段默认且语义对 → `derive(Default)`。
- 自定义默认值 → 手写 `impl Default`。
- 没有合理默认 → 只提供 `new`，别硬 derive。

---

## Q19. 字段简写 `User { name }` 是什么？ {#q19}
**Tags:** `common` `struct` `syntax` `shorthand`
**适用版本:** Rust 1.0+

**一句话答案：**

当**局部变量名与字段名相同**时，`User { name }` 等价于 `User { name: name }`，是初始化（和解构）时的语法糖。

**解答：**

```rust
struct User {
    name: String,
    age: u32,
}

fn new_user(name: String, age: u32) -> User {
    User { name, age } // 同 User { name: name, age: age }
}

fn main() {
    let u = new_user(String::from("Ada"), 36);
    println!("{} {}", u.name, u.age);
}
```

解构同样能简写：

```rust
struct User {
    name: String,
    age: u32,
}

fn main() {
    let u = User {
        name: String::from("Ada"),
        age: 36,
    };
    let User { name, age } = u;
    println!("{name} {age}");
}
```

名字对不上就必须写完整：`User { name: n, age: a }`。它只省重复标识符，不改变所有权——`String` 字段照样 move。

**Go 对比：**

```go
package main

import "fmt"

type User struct {
	Name string
	Age  int
}

func main() {
	name := "Ada"
	age := 36
	u := User{Name: name, Age: age} // 必须 Name: name，没有同名简写
	fmt.Println(u)
}
```

- **Go 怎么做**：复合字面量用 `Field: value`；键值与变量同名也要写两边。
- **Rust 为什么不同**：提供字段初始化简写，少打一遍名字。
- **Go 程序员易踩的坑**：写成 `User { name: }` 或漏字段；简写要求标识符完全同名。

**记忆点：**

- 变量名 = 字段名 → `Type { field }`。
- 不等价于「可选字段」；没写的字段仍要补齐（或 `..`）。
- 解构侧同样可用简写。

---
