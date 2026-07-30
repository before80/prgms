+++
title = "25-generics"
date = 2026-07-28T14:49:00+08:00
weight = 250
type = "docs"
description = "面向 Go 用户重写 Rust 泛型：边界、单态化、`impl Trait` 与 const 泛型"
isCJKLanguage = true
draft = false

+++

泛型 (Generics)

面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go；只有真的能形成代码对照时才给 Go 代码，否则只做概念对比。

**本篇能解决什么：**
- 你是否知道 Rust 泛型不是“先写着，实例化时再看能不能用”的模板系统？
- 你是否总在 `T` 上直接点方法，然后遇到 “no method found for type parameter” 这类报错？
- 你是否分不清 `T: Trait`、`where`、`impl Trait`、`dyn Trait` 各自的职责？
- 你是否想搞懂 const 泛型、默认类型参数、`?Sized` 这些常见扩展写法？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| generic | — | 泛型 | 把类型当参数传给函数、结构体或枚举 | Go 泛型 |
| bound | — | 约束 | 指定类型参数必须实现哪些 trait | interface 约束 |
| monomorphization | — | 单态化 | 编译器为具体类型生成专门代码 | Go 也会做专门化，但语义曝光更少 |
| `impl Trait` | — | trait 占位写法 | 用更短的语法表达“某个实现了此 trait 的类型” | 只有局部相似，没有完全对应物 |
| const generic | — | 常量泛型 | 把常量值也当作泛型参数 | Go 无直接对应物 |
| `DST` | Dynamically Sized Type | 动态大小类型 | 编译期不知道大小的类型，如 `str`、`[T]` | slice/string header 背后对象有点像 |

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q17](#q17), [Q18](#q18), [Q19](#q19) |
| `common` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q16](#q16) |

## Q1. Rust 泛型最基本写法是什么，能放在哪些位置？ {#q1}
**Tags:** `common` `generics` `syntax`
**适用版本:** Rust 1.0+

**一句话答案：** 泛型参数可以出现在函数、结构体、枚举、`impl` 和方法上，本质上都是“先声明类型参数，再在签名里使用它”。

**详细解答：** 先记住一个最小规则：尖括号里声明，后面正文里使用。Rust 不会因为你写了 `T` 就默认允许一切操作；没有额外约束时，`T` 只是“某个未知类型”。

```rust
fn first<T>(items: &[T]) -> Option<&T> {
    items.first()
}

fn main() {
    let nums = vec![10, 20, 30];
    assert_eq!(first(&nums), Some(&10));
}
```

```rust
struct Pair<T> {
    left: T,
    right: T,
}

enum Either<L, R> {
    Left(L),
    Right(R),
}

fn main() {
    let p = Pair { left: 1, right: 2 };
    let e: Either<&str, i32> = Either::Right(42);
    assert_eq!(p.left + p.right, 3);
    assert!(matches!(e, Either::Right(42)));
}
```

**🐹 Go 对比：**
- Go 里你也会在函数或类型后面写类型参数，但 Rust 还会把它大量用于 `impl`、trait bound 和关联类型组合里。
- Rust 的重点不是“语法像不像”，而是“没承诺的能力就不能用”。

**记忆点：** `T` 只是占位符，不是“万能类型”。

## Q2. 为什么没有 trait bound 的 `T` 几乎什么都不能做？ {#q2}
**Tags:** `common` `bounds` `diagnostics`
**适用版本:** Rust 1.0+

**一句话答案：** 因为编译器只知道 `T` 是某个未知类型；你没承诺它支持比较、打印、相加或调用特定方法，编译器就不能放行。

**详细解答：** 这和 Go 的约束思路类似，但 Rust 更严格地落实到每个操作上。你想比较，就写 `PartialOrd`；想打印，就写 `Debug` 或 `Display`；想加法，就写 `Add`。

```rust
fn largest<T: PartialOrd>(items: &[T]) -> &T {
    let mut max = &items[0];
    for item in items {
        if item > max {
            max = item;
        }
    }
    max
}

fn main() {
    let nums = vec![3, 9, 4];
    assert_eq!(largest(&nums), &9);
}
```

```rust
fn print_len<T>(value: T) {
    // value.len();
    // error[E0599]: no method named `len` found for type parameter `T`
    let _ = value;
}

fn main() {
    print_len(String::from("hello"));
}
```

**🐹 Go 对比：**
```go
package main

import "fmt"

type HasLen interface {
	~string | ~[]byte
}

func printLen[T HasLen](v T) {
	fmt.Println(len(v))
}

func main() {
	printLen("hello")
}
```

**记忆点：** Rust 的泛型不是“鸭子类型”；能力必须写进签名。

## Q3. 内联 bound 和 `where` 子句该怎么选？ {#q3}
**Tags:** `common` `where` `readability`
**适用版本:** Rust 1.0+

**一句话答案：** 约束少时内联写法够用，约束一多、关联类型一出现，`where` 往往更清楚。

**详细解答：** 两者表达能力相同，区别主要在可读性。尤其是你要同时约束迭代器本身和它的 `Item` 时，`where` 比较不拥挤。

```rust
use std::fmt::Debug;

fn dump_inline<T: Debug>(value: T) {
    println!("{value:?}");
}

fn main() {
    dump_inline(vec![1, 2, 3]);
}
```

```rust
fn collect_twice<I>(iter: I) -> Vec<I::Item>
where
    I: Iterator,
    I::Item: Clone,
{
    iter.collect()
}

fn main() {
    let values = vec![1, 2, 3];
    let copied = collect_twice(values.into_iter());
    assert_eq!(copied, vec![1, 2, 3]);
}
```

**🐹 Go 对比：** 这更像 Go 里把复杂约束单独提出来命名；目标都是减少签名噪音。

**记忆点：** 读起来更清楚就用 `where`，不是更“高级”才用。

## Q4. `::<>` 这个 turbofish 什么时候必须写？ {#q4}
**Tags:** `common` `turbofish` `type-inference`
**适用版本:** Rust 1.0+

**一句话答案：** 当类型推断不够时，就要用 turbofish 或变量类型标注把目标类型说清楚。

**详细解答：** 最常见的两类场景是 `collect()` 和 `parse()`。因为候选目标类型不止一个，编译器不会替你猜。

```rust
fn main() {
    let values = (1..=3).collect::<Vec<i32>>();
    let n = "42".parse::<i32>().unwrap();

    assert_eq!(values, vec![1, 2, 3]);
    assert_eq!(n + 1, 43);
}
```

```rust
fn main() {
    let values: Vec<i32> = (1..=3).collect();
    let more = (4..=6).collect::<Vec<_>>();

    assert_eq!(values.len() + more.len(), 6);
}
```

**🐹 Go 对比：** Go 通常更依赖上下文推断，Rust 遇到歧义时会更早要求你显式写出来。

**记忆点：** `collect`、`parse`、某些关联函数，是 turbofish 的高频出现场景。

## Q5. `impl Trait` 在参数位置和返回位置有什么区别？ {#q5}
**Tags:** `common` `impl-Trait`
**适用版本:** 参数位置和返回位置 `impl Trait` 均为 Rust 1.26+

**一句话答案：** 参数位置的 `impl Trait` 基本等价于“匿名泛型参数”，返回位置的 `impl Trait` 则表示“由实现方隐藏一个具体类型”。

**详细解答：** 这两处写法长得一样，语义重点却不同。参数位置是“调用方给我一个实现了某 trait 的值”；返回位置是“我给你一个实现了某 trait 的值，但不告诉你具体类型名”。

```rust
fn print_it(value: impl ToString) {
    println!("{}", value.to_string());
}

fn main() {
    print_it(123);
    print_it("hello");
}
```

```rust
fn make_counter() -> impl Iterator<Item = i32> {
    0..3
}

fn main() {
    let collected: Vec<_> = make_counter().collect();
    assert_eq!(collected, vec![0, 1, 2]);
}
```

**🐹 Go 对比：**
- 参数位置有点像“接受某个满足接口的值”。
- 返回位置没有直接等价物；Go 若想隐藏具体类型，常直接返回 interface 值，而 Rust 这里仍是静态分发。

**记忆点：** 返回 `impl Trait` 不是 `dyn Trait`，它仍然是编译期确定的单一具体类型。

## Q6. 什么时候该用泛型，什么时候该用 `dyn Trait`？ {#q6}
**Tags:** `common` `static-vs-dynamic`
**适用版本:** Rust 1.0+

**一句话答案：** 追求零开销和内联时优先用泛型；需要异构集合、运行时替换实现、减少代码膨胀时考虑 `dyn Trait`。

**详细解答：** 泛型通常走 **单态化**（monomorphization，编译器为每种具体类型生成专门代码），而 `dyn Trait` 走虚表动态分发。两者都重要，关键是场景不同。

```rust
use std::fmt::Display;

fn show_all<T: Display>(items: &[T]) {
    for item in items {
        println!("{item}");
    }
}

fn main() {
    show_all(&[1, 2, 3]);
}
```

```rust
trait Draw {
    fn draw(&self) -> &'static str;
}

struct Circle;
struct Square;

impl Draw for Circle {
    fn draw(&self) -> &'static str {
        "circle"
    }
}

impl Draw for Square {
    fn draw(&self) -> &'static str {
        "square"
    }
}

fn main() {
    let shapes: Vec<Box<dyn Draw>> = vec![Box::new(Circle), Box::new(Square)];
    let labels: Vec<_> = shapes.iter().map(|s| s.draw()).collect();
    assert_eq!(labels, vec!["circle", "square"]);
}
```

**🐹 Go 对比：** Go interface 值更接近 `dyn Trait`；而 Rust 泛型默认是静态分发，不是 interface 值那一套。

**记忆点：** “能不能放进同一个 `Vec` 里装不同实现” 是判断要不要 `dyn` 的一个好问题。

## Q7. 结构体的泛型参数和方法自己的泛型参数能同时存在吗？ {#q7}
**Tags:** `common` `impl` `methods`
**适用版本:** Rust 1.0+

**一句话答案：** 可以，`impl<T>` 是类型自己的参数，方法还能再引入新的 `U`、`F` 等独立参数。

**详细解答：** 这和“容器自身装什么”和“某个方法额外需要什么能力”是两层概念。很多初学者会把它们混成一层。

```rust
#[derive(Debug, PartialEq)]
struct Pair<T> {
    left: T,
    right: T,
}

impl<T> Pair<T> {
    fn swap(self) -> Pair<T> {
        Pair {
            left: self.right,
            right: self.left,
        }
    }
}

fn main() {
    let pair = Pair { left: 1, right: 2 }.swap();
    assert_eq!(pair, Pair { left: 2, right: 1 });
}
```

```rust
#[derive(Debug, PartialEq)]
struct Pair<T> {
    left: T,
    right: T,
}

impl<T> Pair<T> {
    fn map<U, F>(self, f: F) -> Pair<U>
    where
        F: Fn(T) -> U,
    {
        Pair {
            left: f(self.left),
            right: f(self.right),
        }
    }
}

fn main() {
    let pair = Pair { left: 1, right: 2 }.map(|n| n.to_string());
    assert_eq!(
        pair,
        Pair {
            left: String::from("1"),
            right: String::from("2")
        }
    );
}
```

**🐹 Go 对比：** Go 的泛型方法限制更多；Rust 在 `impl` 和方法层级上会更灵活。

**记忆点：** `impl<T>` 不会自动替你引入方法级的 `U`。

## Q8. 如何约束关联类型，比如 `Iterator::Item`？ {#q8}
**Tags:** `common` `associated-types`
**适用版本:** Rust 1.0+

**一句话答案：** 先约束外层类型实现某个 trait，再通过 `Trait::Assoc` 或 `Trait<Assoc = ...>` 继续约束它的关联类型。

**详细解答：** 关联类型让“一个实现只对应一个答案”这件事更明确。迭代器是最常见例子。

```rust
use std::fmt::Debug;

fn debug_iter<I>(iter: I)
where
    I: Iterator,
    I::Item: Debug,
{
    for item in iter {
        println!("{item:?}");
    }
}

fn main() {
    debug_iter(vec![1, 2, 3].into_iter());
}
```

```rust
fn sum_iter<I>(iter: I) -> i32
where
    I: Iterator<Item = i32>,
{
    iter.sum()
}

fn main() {
    let total = sum_iter(vec![1, 2, 3].into_iter());
    assert_eq!(total, 6);
}
```

**🐹 Go 对比：** Go 没有“关联类型”这个机制；这类关系常靠额外类型参数显式展开。

**记忆点：** `I: Iterator<Item = T>` 是读迭代器签名时必须熟悉的基本句式。

## Q9. 默认类型参数有什么用？ {#q9}
**Tags:** `common` `default-type-params`
**适用版本:** Rust 1.0+

**一句话答案：** 默认类型参数让常见用法更短，同时保留“高级用户可以手动换掉实现”的扩展口。

**详细解答：** 标准库里最经典的例子是 `HashMap<K, V, S = RandomState>`。多数人不会手动换哈希器，所以默认值能把常规写法压短。

```rust
use std::marker::PhantomData;

#[derive(Debug)]
struct Cache<K, V, S = u64> {
    _k: PhantomData<K>,
    _v: PhantomData<V>,
    state: S,
}

fn main() {
    let cache: Cache<String, i32> = Cache {
        _k: PhantomData,
        _v: PhantomData,
        state: 0,
    };
    assert_eq!(cache.state, 0);
}
```

```rust
use std::marker::PhantomData;

#[derive(Debug)]
struct Cache<K, V, S = u64> {
    _k: PhantomData<K>,
    _v: PhantomData<V>,
    state: S,
}

fn main() {
    let cache = Cache::<String, i32, &'static str> {
        _k: PhantomData,
        _v: PhantomData,
        state: "custom",
    };
    assert_eq!(cache.state, "custom");
}
```

**🐹 Go 对比：** Go 目前没有默认类型参数；Rust 在库设计上因此更容易兼顾“常用简单”和“进阶可定制”。

**记忆点：** 默认类型参数主要是 API 设计工具，不是语法炫技。

## Q10. const 泛型到底解决了什么问题？ {#q10}
**Tags:** `common` `const-generics`
**适用版本:** 基础 const 泛型自 Rust 1.51+

**一句话答案：** const 泛型允许你把“数组长度、容量上限、块大小”这类编译期常量写进类型系统。

**详细解答：** 最直接的收益是不同长度的数组终于能通过一个统一 API 处理，而不是为每种长度单独写类型。

```rust
struct Window<const N: usize> {
    data: [i32; N],
}

fn main() {
    let window = Window::<3> { data: [1, 2, 3] };
    assert_eq!(window.data.iter().sum::<i32>(), 6);
}
```

```rust
fn sum<const N: usize>(data: [i32; N]) -> i32 {
    data.iter().sum()
}

fn main() {
    assert_eq!(sum([1, 2, 3, 4]), 10);
    assert_eq!(sum([8, 9]), 17);
}
```

**🐹 Go 对比：** Go 泛型不支持把常量值当作类型参数；这类需求通常只能退回运行时检查。

**记忆点：** `const N: usize` 是数组与固定容量数据结构的常用入口。

## Q11. 为什么有时必须写 `PhantomData<T>`？ {#q11}
**Tags:** `common` `PhantomData`
**适用版本:** Rust 1.0+

**一句话答案：** 当类型参数没有真实字段承载时，`PhantomData<T>` 用来把“我逻辑上与 `T` 有关”明确告诉编译器。

**详细解答：** 它不存储数据，但会影响未使用类型参数检查、drop 检查以及变型（variance）推导。面向应用代码，先记住“逻辑上依赖但物理上不存储时要用它”就够了。

```rust
use std::marker::PhantomData;

#[derive(Debug)]
struct Id<T> {
    raw: u64,
    _marker: PhantomData<T>,
}

struct User;

fn main() {
    let user_id = Id::<User> {
        raw: 7,
        _marker: PhantomData,
    };
    assert_eq!(user_id.raw, 7);
}
```

```rust
use std::marker::PhantomData;

struct Borrowed<'a, T> {
    ptr: *const T,
    _marker: PhantomData<&'a T>,
}

fn main() {
    let value = 10;
    let borrowed = Borrowed {
        ptr: &value,
        _marker: PhantomData,
    };
    assert_eq!(borrowed.ptr, &value as *const i32);
}
```

**🐹 Go 对比：** Go 基本不需要这类“零大小类型标记”工具；这是 Rust 在类型系统层面表达所有权/借用关系的典型做法。

**记忆点：** 不存字段不等于“不需要告诉编译器这个关系存在”。

## Q12. `T: ?Sized` 是什么场景才需要写？ {#q12}
**Tags:** `common` `DST` `sized`
**适用版本:** Rust 1.0+

**一句话答案：** 因为泛型默认隐含 `T: Sized`，只有你真的想接受 `str`、`[T]` 或 trait 对象这类动态大小类型时，才需要放宽成 `T: ?Sized`。

**详细解答：** 大多数时候你根本不用写它；但做“接受任意引用目标”的通用 API 时很常见，比如 `&str` 和 `&String` 都想收的时候。

```rust
fn show_len<T: ?Sized + AsRef<str>>(value: &T) {
    println!("{}", value.as_ref().len());
}

fn main() {
    let owned = String::from("hello");
    show_len(&owned);
    show_len("world");
}
```

```rust
fn first_byte<T: ?Sized + AsRef<[u8]>>(value: &T) -> u8 {
    value.as_ref()[0]
}

fn main() {
    let data = vec![1, 2, 3];
    assert_eq!(first_byte(&data), 1);
    assert_eq!(first_byte(&[9, 8][..]), 9);
}
```

**🐹 Go 对比：** Go 不需要显式表达 “Sized / ?Sized” 这层约束；Rust 之所以需要，是因为它把内存布局也纳入了类型系统。

**记忆点：** 看到 `?Sized`，先想到“这个 API 想接收动态大小类型的引用”。

## Q13. Rust 泛型和 Go 1.18+ generics 差在哪？（单态化 vs 字典派发直觉） {#q13}
**Tags:** `common` `monomorphization` `go-generics`
**适用版本:** Rust 1.0+；Go generics 自 Go 1.18+

**一句话答案：** Rust 泛型默认走 **单态化**（monomorphization，为每种具体类型生成专用机器码）；Go 泛型更接近“一份共享代码 + 运行时按类型信息派发”的字典式实现直觉。

**详细解答：** 调用 `fn f<T: Display>(x: T)` 时，Rust 会为 `i32`、`String` 等各自生成一份内联友好的专用版本。收益是零虚表开销、容易内联；代价是代码体积可能膨胀（见 [Q14](#q14)）。需要运行时异构时，Rust 才显式改用 `dyn Trait`。

```rust
use std::fmt::Display;

fn show<T: Display>(value: T) {
    println!("{value}");
}

fn main() {
    show(42);
    show("hello");
}
```

```rust
use std::fmt::Display;

fn show_dyn(value: &dyn Display) {
    println!("{value}");
}

fn main() {
    show_dyn(&42);
    show_dyn(&"hello");
}
```

第一段是静态分发：编译期就定死调用目标。第二段是动态分发：通过虚表在运行时选方法。Go 的 `func F[T fmt.Stringer](v T)` 在语义上像“带约束的类型参数”，但实现策略和 Rust 默认单态化并不相同；不要把 Go 那套运行时派发直觉硬套到 Rust 泛型上。

**🐹 Go 对比：**
```go
package main

import "fmt"

func Show[T fmt.Stringer](v T) {
	fmt.Println(v.String())
}

type Name string

func (n Name) String() string { return string(n) }

func main() {
	Show(Name("Ada"))
}
```

Go 里 interface 值本来就是字典派发；泛型则是另一条路径。Rust 把“静态泛型”和“动态 `dyn`”拆成两套显式选择。

**记忆点：** Rust 泛型默认“每种类型一份机器码”；要字典派发请写 `dyn Trait`。

## Q14. 单态化会不会把二进制撑很大？怎么缓解？ {#q14}
**Tags:** `common` `codegen` `binary-size`
**适用版本:** Rust 1.0+

**一句话答案：** 会，尤其是热路径上为很多具体类型各生成一份大函数时；缓解办法是收敛实例化种类、把胖逻辑收到非泛型/`dyn` 边界里，并在需要时做链接期裁剪。

**详细解答：** 单态化本身不是 bug，而是“用体积换速度”的默认策略。真正危险的是：同一个大泛型函数被 `u8`/`u16`/`u32`/`String`/`PathBuf`……各实例化一遍。常见缓解：

1. **减少 `T` 种类**：能统一成 `&str` / `&[u8]` 就别为每个拥有型各开一份。
2. **内层去泛型**：对外保留薄泛型壳，对内落到共享的非泛型实现或 `dyn Trait`。
3. **按需 `dyn`**：插件、异构集合、实例化爆炸处改动态分发（见 [Q6](#q6)）。
4. **发布裁剪**：release 下 `LTO`、`strip`、避免无谓 `Debug` 格式化膨胀。

```rust
use std::fmt::Display;

fn format_many<T: Display>(items: &[T]) -> String {
    format_dyn(&items.iter().map(|x| x as &dyn Display).collect::<Vec<_>>())
}

fn format_dyn(items: &[&dyn Display]) -> String {
    items
        .iter()
        .map(|x| x.to_string())
        .collect::<Vec<_>>()
        .join(",")
}

fn main() {
    assert_eq!(format_many(&[1, 2, 3]), "1,2,3");
    assert_eq!(format_many(&["a", "b"]), "a,b");
}
```

上面故意把“真正拼字符串”的逻辑收到 `format_dyn`：外层仍可泛型调用，但重活不必为每种 `T` 各复制一份。

**🐹 Go 对比：** Go 泛型通常不会像 Rust 这样把“每种 `T` 一份专用机器码”推到你脸上；你更常遇到的是 interface 装箱与逃逸，而不是单态化体积爆炸。Rust 要你主动在速度和体积之间选型。

**记忆点：** 泛型壳要薄，重逻辑尽量共享；体积炸了先查“实例化了多少种 `T`”。

## Q15. `T: Clone + Debug` 多约束写在尖括号还是 where？ {#q15}
**Tags:** `common` `where` `bounds`
**适用版本:** Rust 1.0+

**一句话答案：** 一两个简单 bound 写在尖括号里最清晰；约束变多、要碰关联类型，或签名已经很长时，挪到 `where`（和 [Q3](#q3) 同一原则）。

**详细解答：** `T: Clone + Debug` 这种短组合，内联完全合适。一旦出现 `I::Item: Clone`、多个类型参数互相约束、或函数参数列表本身已经很长，`where` 更易读。两者语义等价，选可读性。

```rust
use std::fmt::Debug;

fn dump_pair<T: Clone + Debug>(value: T) {
    let copy = value.clone();
    println!("{copy:?}");
}

fn main() {
    dump_pair(vec![1, 2, 3]);
}
```

```rust
use std::fmt::Debug;

fn dump_mapped<I, F, U>(iter: I, f: F) -> Vec<U>
where
    I: IntoIterator,
    I::Item: Clone + Debug,
    F: Fn(I::Item) -> U,
    U: Debug,
{
    let mut out = Vec::new();
    for item in iter {
        println!("see {item:?}");
        out.push(f(item.clone()));
    }
    out
}

fn main() {
    let doubled = dump_mapped(vec![1, 2], |n| n * 2);
    assert_eq!(doubled, vec![2, 4]);
}
```

**🐹 Go 对比：** Go 常把复杂约束提成命名 interface / 类型集合；Rust 的 `where` 扮演类似“把约束从签名中线挪开”的角色。

**记忆点：** 短 bound 内联，长约束 / 关联类型上 `where`。

## Q16. 为什么有的 API 要 `T: 'static`？ {#q16}
**Tags:** `common` `static` `bounds`
**适用版本:** Rust 1.0+

**一句话答案：** 因为调用方可能把 `T` 存得比当前栈帧更久（线程、`'static` 回调、全局注册表）；`T: 'static` 保证值内部不含更短的借用。

**详细解答：** 这里的 `'static` 不是“必须是字面量”，而是“不携带短命引用”。`String`、`i32`、`Vec<u8>` 都满足；`&str` 指向局部 `String` 时通常不满足。线程、异步任务、类型擦除后的长期存储最常要求它。

```rust
fn stash_owned<T: 'static>(value: T) -> T {
    value
}

fn main() {
    let owned = stash_owned(String::from("ok"));
    assert_eq!(owned, "ok");
}
```

```rust
use std::thread;

fn run_detached<T>(value: T) -> thread::JoinHandle<T>
where
    T: Send + 'static,
{
    thread::spawn(move || value)
}

fn main() {
    let handle = run_detached(String::from("hello"));
    assert_eq!(handle.join().unwrap(), "hello");
}
```

若你手里只有短借用，常见出路是：改成拥有型（`to_owned` / `Arc`）、缩短存储寿命（`thread::scope`）、或不要把引用塞进 `'static` 槽位。

**🐹 Go 对比：** Go 可以把局部变量地址丢进 goroutine，靠逃逸分析和 GC 兜底；Rust 用 `T: 'static`（或作用域线程）在类型层先问清“这份数据能不能活到任务结束”。

**记忆点：** 看到 `T: 'static`，先翻译成“别把短借用偷偷存久”。

## Q17. `if` / `match` 分支返回不同类型怎么办？ {#q17}
**Tags:** `hot` `type-unification` `match` `enum`
**适用版本:** Rust 1.0+

**一句话答案：** 每个分支必须收敛成**同一个类型**；做不到就引入枚举、转成共同类型，或改用 `Box<dyn Trait>` / 泛型回调，而不是指望编译器“两边各返回各的”。

**详细解答：** `if`/`match` 作为表达式时，所有臂的类型要一致（或能强制到同一类型）。`String` 和 `i32`、`Vec<u8>` 和 `&[u8]` 不能直接并成一个返回值。常见出路：

1. **统一成已有类型**：两边都 `.to_string()`，或都变成 `Option`/`Result` 的同一成功类型。
2. **自建枚举**：语义不同就用 `enum` 显式建模。
3. **动态分发**：异构实现收进 `Box<dyn Trait>`（见 [Q6](#q6)）。

```rust
fn label(flag: bool) -> String {
    if flag {
        String::from("yes")
    } else {
        String::from("no")
    }
}

fn main() {
    assert_eq!(label(true), "yes");
}
```

```rust
enum Outcome {
    Text(String),
    Code(i32),
}

fn classify(ok: bool) -> Outcome {
    if ok {
        Outcome::Text(String::from("ok"))
    } else {
        Outcome::Code(1)
    }
}

fn main() {
    assert!(matches!(classify(false), Outcome::Code(1)));
}
```

「❌ 错误直觉」——以为分支可以像动态语言一样各返回各的类型：编译器会报类型不匹配，而不是运行时再选。

**🐹 Go 对比：** Go 的 `if` 多是语句；多返回值类型在签名里就定死了。真要“有时字符串有时整数”，Go 也常退回 `interface{}` / 自定义类型，和 Rust 的 `enum`/`dyn` 选型同类。

**记忆点：** 分支要先统一类型；统一不了就 `enum` 或 `dyn`。

## Q18. 报 `type annotations needed` 时，类型标注该写在哪？ {#q18}
**Tags:** `hot` `type-inference` `turbofish` `annotations`
**适用版本:** Rust 1.0+

**一句话答案：** 优先标在**结果落点**：`let` 绑定、`collect`/`parse` 的 turbofish，或函数返回类型；标在“信息最够用、改动最小”的那一处，而不是到处撒注解。

**详细解答：** 这条报错表示局部上下文推不出唯一类型。高频落点：

1. **`let x: T = ...`**：后面还要用、或要约束容器元素类型时最直观。
2. **turbofish**：`collect::<Vec<_>>()`、`parse::<i32>()`（见 [Q4](#q4)）。
3. **函数签名**：参数/返回类型写清后，函数体里往往不再需要局部标注。
4. **`as` / `From`/`Into`**：数值或转换目标歧义时，明确目标类型。

```rust
fn main() {
    let values: Vec<i32> = (1..=3).collect();
    let n = "42".parse::<i32>().unwrap();
    assert_eq!(values.len() + n as usize, 45);
}
```

```rust
fn sum_parsed(lines: &[&str]) -> i32 {
    lines.iter().map(|s| s.parse::<i32>().unwrap()).sum()
}

fn main() {
    assert_eq!(sum_parsed(&["1", "2", "3"]), 6);
}
```

先补一处最关键的注解再 `cargo check`；若仍歧义，再往调用链上游补签名。不要在每个中间变量上重复写同一类型。

**🐹 Go 对比：** Go 也有推断，但歧义时常靠左侧短变量声明或显式转换；Rust 对 `collect`/`parse` 这类“多目标类型”API 更早要求你点名。

**记忆点：** 标注写在结果落点；`collect`/`parse` 优先 turbofish。

## Q19. 为什么返回 `impl Trait` 不能有时是 A、有时是 B？ {#q19}
**Tags:** `hot` `impl-Trait` `opaque-type`
**适用版本:** 返回位置 `impl Trait` 自 Rust 1.26+

**一句话答案：** 返回位置的 `impl Trait` 表示**一个**编译期确定的具体（不透明）类型；两个分支若是不同具体类型，即使都实现了同一 trait，也不能写成“有时 A 有时 B”。

**详细解答：** `fn f() -> impl Iterator<Item = i32>` 的意思是：实现方选定**唯一**具体类型（例如 `Range` 或 `Map<...>`），对外只承诺 trait 能力。`if` 一边返回 `0..3`、一边返回 `vec![1,2].into_iter()`，具体类型不同，编译失败。这和 [Q5](#q5)、[Q17](#q17) 是同一条类型统一规则。

出路：

1. **统一迭代器适配**：两边都 `.map(...)` 成同形，或先 `collect` 再统一。
2. **枚举包装**：自定义 enum，再手写 `Iterator`（或用标准库/`either` 一类工具；引入外部 crate 时用命令安装，不要在文档里假装已依赖）。
3. **`Box<dyn Trait>`**：接受动态分发，换运行时异构。

```rust
fn counter(flag: bool) -> impl Iterator<Item = i32> {
    // 两边必须是同一具体类型；这里都走 Range
    if flag {
        0..3
    } else {
        10..13
    }
}

fn main() {
    assert_eq!(counter(true).sum::<i32>(), 3);
    assert_eq!(counter(false).sum::<i32>(), 33);
}
```

```rust
fn counter_dyn(flag: bool) -> Box<dyn Iterator<Item = i32>> {
    if flag {
        Box::new(0..3)
    } else {
        Box::new(vec![7, 8, 9].into_iter())
    }
}

fn main() {
    assert_eq!(counter_dyn(false).sum::<i32>(), 24);
}
```

需要“真正不同的具体类型 + 静态分发”时，通常改 API：拆成两个函数，或返回枚举。

**🐹 Go 对比：** Go 返回 interface 时，两边可以是不同具体类型（动态派发）。Rust 的 `impl Trait` 更接近“隐藏的单一具体类型”，不是 Go interface 那种异构盒子；要异构请用 `dyn Trait`。

**记忆点：** `impl Trait` = 单一隐藏具体类型；异构请用 `enum` 或 `dyn`。
