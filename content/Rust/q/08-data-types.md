+++
title = "08-data-types"
date = 2026-07-28T14:49:00+08:00
weight = 80
type = "docs"
description = "讲清 Rust 常见数据类型、类型边界与 Go 程序员最常踩的类型坑。"
isCJKLanguage = true
draft = false

+++

# 数据类型 (Data Types)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会刚写 Rust，就被 `i32`、`u64`、`usize`、`char`、`()` 这些类型名弄得眼花？
- 你是否想知道：Go 里很多地方“编译器帮你凑合”的类型转换，为什么到 Rust 里突然不让了？
- 你会不会被 `E0282`、`E0308`、`E0277` 这类类型错误挡住，却不知道该补哪一句类型标注？
- 你是否分不清 `String`、`&str`、`char`、字节、切片到底分别代表什么？
- 你会不会想当然地把 `int`、`byte`、`rune`、slice 的 Go 习惯直接搬到 Rust，结果越写越别扭？
- 你是否需要一份“哪些类型放栈上、哪些只是视图、哪些根本不能单独拿出来用”的速查地图？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| scalar type | — | 标量类型 | 单个值，不再由多个字段组成，如整数、浮点、`bool`、`char` | 基本类型 |
| compound type | — | 复合类型 | 由多个值组合成的类型，如元组、数组 | 结构体 / 数组 |
| integer | — | 整数 | 不带小数部分的数值类型 | `int` / `uint*` |
| signed | — | 有符号 | 既能表示正数也能表示负数 | `int*` |
| unsigned | — | 无符号 | 只能表示 0 和正数 | `uint*` / `byte` |
| literal | — | 字面量 | 直接写在代码里的值，如 `42`、`3.14`、`'a'` | 同概念 |
| type inference | — | 类型推断 | 编译器根据上下文猜出类型 | 类型推断 |
| type annotation | — | 类型标注 | 人工把类型写出来，如 `let x: u8 = 1;` | 显式类型 |
| `usize` | — | 平台字长无符号整数 | 专门给长度、索引、指针大小相关场景用 | `int`（但 Go 没单独索引类型） |
| `isize` | — | 平台字长有符号整数 | 与指针大小一致的有符号整数 | 无直接对应 |
| overflow | — | 溢出 | 运算结果超出类型可表示范围 | 溢出 |
| `wrapping_*` | — | 环绕运算 | 超界后按模回绕 | 手工位运算近亲 |
| `checked_*` | — | 检查型运算 | 超界时返回 `None`，不偷偷截断 | 手写边界检查 |
| `saturating_*` | — | 饱和运算 | 超界时卡在最大值或最小值 | 手写边界钳制 |
| **NaN** | Not a Number | 非数 | 浮点里的“不是一个正常数字”的特殊值 | `math.NaN()` |
| `char` | — | Unicode 标量值字符 | Rust 的 `char` 是一个 Unicode 标量值，占 4 字节，不等于字符串 | `rune` |
| Unicode scalar value | — | Unicode 标量值 | 合法的 Unicode 码点，排除代理区 | `rune` 的语言层近亲 |
| tuple | — | 元组 | 固定长度、可混合不同类型的一组值 | 多返回值打包近亲 |
| array | — | 数组 | 固定长度、元素同类型，长度写进类型里 | 数组 |
| slice | — | 切片视图 | 对一段连续数据的借用视图，如 `&[T]`、`&str` | slice |
| `DST` | Dynamically Sized Type | 动态大小类型 | 编译期不知道具体大小的类型，如 `str`、`[T]`、`dyn Trait` | 无直接对应 |
| `Sized` | — | 固定大小 trait | 编译期知道大小的类型会自动实现它 | 默认“普通类型” |
| cast | — | 强制转换 | 用 `as` 做底层数值或指针转换，可能丢信息 | 显式转换 |
| `From` / `Into` | — | 无损转换 trait | 表达“这种转换合理且通常不丢信息” | 手写转换函数 |
| `TryFrom` / `TryInto` | — | 可能失败的转换 trait | 转换可能越界、失败时返回错误 | `(T, error)` 风格转换 |
| unit type | — | 单元类型 | 只有一个值 `()` 的类型，表示“没有有意义的数据” | `struct{}` / `void` 近亲 |
| never type | — | 永不返回类型 | `!`，表示这段代码永远到不了返回点 | `panic` / 无限循环近亲 |
| type alias | — | 类型别名 | 给已有类型起新名字，不会变成新类型 | `type MyInt = int` |
| newtype | — | 新包装类型 | 用单字段结构体包一层，得到真正不同的新类型 | 定义新结构体 |
| **ZST** | Zero-Sized Type | 零大小类型 | 编译后不占空间的类型，如 `()`、空结构体 | `struct{}` |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q4](#q4), [Q5](#q5), [Q7](#q7), [Q9](#q9), [Q11](#q11), [Q12](#q12), [Q19](#q19) |
| `common` | [Q3](#q3), [Q6](#q6), [Q8](#q8), [Q10](#q10), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q20](#q20) |
| `occasional` | [Q16](#q16), [Q17](#q17) |
| `advanced` | [Q18](#q18) |

---

## Q1. Rust 最基础的数据类型到底有哪些？ {#q1}
**Tags:** `hot` `beginner` `scalar` `compound`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 最先要记住的是四类标量类型：整数、浮点、`bool`、`char`；以及两类基础复合类型：元组和数组。

**解答：**

Rust 里的**标量类型**（scalar type，标量类型：单个值，不再由多个字段组成）就是语言最基础的原子积木。

```rust
fn main() {
    let n: i32 = -42;
    let pi: f64 = 3.14159;
    let ok: bool = true;
    let ch: char = '中';

    println!("{n} {pi} {ok} {ch}");
}
```

除了标量，最早会遇到的还有两种**复合类型**（compound type，复合类型：由多个值组合而成）：

```rust
fn main() {
    let pair: (i32, f64) = (10, 2.5);
    let arr: [i32; 3] = [1, 2, 3];

    println!("{} {}", pair.0, arr[1]);
}
```

把它们按“是否同类型、长度是否固定”来记，最省脑力：

```rust
fn main() {
    let user_point = (3, 4); // 元组：允许不同类型，这里刚好相同
    let three_ids = [7, 8, 9]; // 数组：元素类型必须一致，长度固定

    println!("{user_point:?} {three_ids:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var n int32 = -42
	var pi float64 = 3.14159
	var ok bool = true
	var ch rune = '中'
	arr := [3]int{1, 2, 3}

	fmt.Println(n, pi, ok, ch, arr)
}
```

- **Go 怎么做**：也有整数、浮点、布尔、字符（通常用 `rune`）和数组。
- **Rust 为什么不同**：Rust 更早把“类型宽度”和“是否同构复合”写得很显式，方便编译期做更强的检查。
- **Go 程序员易踩的坑**：把 Rust 的 `char` 当成 Go 的 `string`，或者把元组当成“只是临时语法糖”；其实它们都是一等类型。

**记忆点：**

- 标量先背：整数、浮点、`bool`、`char`。
- 复合先背：元组 `(T1, T2, ...)`、数组 `[T; N]`。
- 后面学到的 `String`、切片、结构体、枚举，都是在这些基础上继续往上搭。

---

## Q2. 为什么有时候必须写类型标注，编译器自己猜不出来？ {#q2}
**Tags:** `hot` `beginner` `inference` `E0282`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 有类型推断，但它只在“能唯一确定”的前提下工作；像空容器、`parse()`、`collect()` 这类场景，常常需要你补一句类型标注。

**解答：**

**类型推断**（type inference，类型推断：编译器根据上下文猜出类型）很强，但不是心灵感应。对 `1`、`1.0` 这种简单字面量，它通常能猜：

```rust
fn takes_i64(x: i64) {
    println!("{x}");
}

fn main() {
    let x = 1;
    takes_i64(x); // 上下文告诉编译器：x 应该是 i64
}
```

但一旦上下文不够，比如空 `Vec`，编译器就会说“我真不知道里面该装什么”：

```rust
fn main() {
    let v = Vec::<i32>::new();
    println!("{}", v.len());
}
```

```rust
fn main() {
    let v = Vec::new();
    // error[E0282]: type annotations needed for `Vec<_>`
    println!("{}", v.len());
}
```

`parse()` 也是高频场景，因为 `"42"` 能被解析成很多整数或浮点类型：

```rust
fn main() {
    let port: u16 = "8080".parse().unwrap();
    let ratio = "3.5".parse::<f64>().unwrap();

    println!("{port} {ratio}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func main() {
	v := []int{}
	port, _ := strconv.Atoi("8080")
	fmt.Println(len(v), port)
}
```

- **Go 怎么做**：空 slice 通常能直接写成 `[]int{}`；字符串解析 API 也往往把目标类型写进函数名或参数里。
- **Rust 为什么不同**：同一个构造式常能落到很多目标类型，Rust 宁愿要求你多写一点，也不愿偷偷猜错。
- **Go 程序员易踩的坑**：看到 `E0282` 就觉得“编译器太笨”；其实是你的代码真的没告诉它足够信息。

**记忆点：**

- 编译器能唯一确定时，尽量让它推断。
- 空容器、`parse()`、`collect()` 猜不到时，第一反应就是补类型。
- 写法上常见三种：`let x: T = ...`、`Foo::<T>::new()`、`"42".parse::<T>()`。

---

## Q3. `i32`、`u32`、`i64`、`u8` 这些整数类型该怎么选？ {#q3}
**Tags:** `common` `beginner` `integer`
**适用版本:** Rust 1.0+

**一句话答案：**

一般业务整数默认用 `i32`，索引和长度用 `usize`，字节和二进制协议用 `u8`，需要明确位宽或跨平台格式时再选 `i64`、`u32` 之类。

**解答：**

整数先按两个维度理解：

1. `i` 开头是**有符号**（signed），能表示负数。
2. `u` 开头是**无符号**（unsigned），只能表示 0 和正数。

```rust
fn main() {
    let temp: i32 = -5;
    let count: u32 = 42;
    let byte: u8 = 255;

    println!("{temp} {count} {byte}");
}
```

如果你关心协议格式、磁盘文件、网络包，位宽必须写死；因为它就是数据格式的一部分：

```rust
fn main() {
    let magic: u32 = 0xFEED_BEEF;
    let file_size: u64 = 5_000_000_000;

    println!("{magic:#X} {file_size}");
}
```

日常选择可以用这张脑内小表：

```rust
fn main() {
    let default_math: i32 = 10; // 普通整数运算
    let index: usize = 2; // 长度、索引
    let flags: u8 = 0b1010_0001; // 位标志、字节流

    println!("{default_math} {index} {flags}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var temp int32 = -5
	var count uint32 = 42
	var b byte = 255

	fmt.Println(temp, count, b)
}
```

- **Go 怎么做**：很多地方习惯先用 `int`，必要时再补 `int32`、`uint64`。
- **Rust 为什么不同**：Rust 不想把“位宽”“是否有符号”藏起来，因为它们直接影响溢出、转换和内存布局。
- **Go 程序员易踩的坑**：把 Rust 的 `i32` 当成 Go 的 `int` 默认替身；其实很多索引相关 API 更想要的是 `usize`。

**记忆点：**

- 一般业务整数：`i32`。
- 长度与索引：`usize`。
- 字节流：`u8`。
- 协议 / 文件格式 / FFI 边界：显式固定位宽。

---

## Q4. `usize` / `isize` 为什么单独存在？什么时候必须用？ {#q4}
**Tags:** `hot` `beginner` `usize` `E0277`
**适用版本:** Rust 1.0+

**一句话答案：**

`usize` 和 `isize` 的位宽跟平台指针一致；标准库把索引、长度、切片范围这类“和内存地址天然相关”的场景统一交给 `usize`。

**解答：**

`usize` 不是“更大的 `u32`”，而是“能装下本机地址大小的无符号整数”。在 64 位机器上通常是 64 位，在 32 位机器上通常是 32 位。

```rust
fn main() {
    let arr = [10, 20, 30];
    let idx: usize = 1;

    println!("{}", arr[idx]);
}
```

长度 API 也统一返回 `usize`：

```rust
fn main() {
    let names = ["go", "rust", "zig"];
    let len: usize = names.len();

    println!("{len}");
}
```

如果你拿 `i32` 去索引，标准库会直接拒绝：

```rust
fn main() {
    let arr = [10, 20, 30];
    let idx: i32 = 1;
    println!("{}", arr[idx]);
    // error[E0277]: the type `[{integer}]` cannot be indexed by `i32`
}
```

真要从别的整数转成 `usize`，推荐先检查，再转换：

```rust
fn main() {
    let raw: i32 = 2;
    let idx = usize::try_from(raw).unwrap();
    let arr = [10, 20, 30];

    println!("{}", arr[idx]);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	arr := [3]int{10, 20, 30}
	idx := 1
	fmt.Println(arr[idx])
}
```

- **Go 怎么做**：索引通常直接用 `int`，语言层没有 `usize` 这种专门的索引类型。
- **Rust 为什么不同**：Rust 把“长度 / 下标 / 指针相关”明确收敛到 `usize`，减少跨平台位宽歧义。
- **Go 程序员易踩的坑**：习惯性把计数器写成 `i32` 或 `u32`，结果一碰切片索引就要转换。

**记忆点：**

- `len()`、`capacity()`、数组 / 切片索引，优先想 `usize`。
- `isize` 主要用于与指针差值同宽的有符号场景。
- 业务 ID、数据库主键不该因为“正好是无符号”就乱用 `usize`。

---

## Q5. Rust 里的整数溢出到底会怎样？ {#q5}
**Tags:** `hot` `beginner` `overflow`
**适用版本:** Rust 1.0+

**一句话答案：**

编译期能看出来的溢出会直接报错；运行期整数溢出在 debug 构建默认 panic，在 release 构建默认按二进制回绕，所以边界代码最好显式用 `checked_*`、`wrapping_*`、`saturating_*`。

**解答：**

先看运行期才知道值的例子。这里通过 `parse()` 把值拖到运行期，才能真实观察 debug / release 差异：

```rust
fn bump(x: u8) -> u8 {
    x + 1
}

fn main() {
    let x: u8 = "255".parse().unwrap();
    println!("{}", bump(x));
}
```

如果值在编译期就已知，编译器通常会在构建阶段就直接拦下；真正写业务代码时，更值得记的是“不要把边界语义留给构建模式决定”：

```rust
fn main() {
    let x: u8 = 255;
    let wrapped = x.wrapping_add(1);
    let checked = x.checked_add(1);

    println!("{wrapped} {checked:?}");
}
```

边界代码里更推荐把意图写死，不依赖构建模式：

```rust
fn main() {
    let a = 255u8.wrapping_add(1);
    let b = 255u8.checked_add(1);
    let c = 200u8.saturating_add(100);

    println!("{a} {b:?} {c}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var x uint8 = 255
	y := x + 1
	fmt.Println(y) // 0，固定按位宽回绕
}
```

- **Go 怎么做**：整数溢出按固定位宽回绕，没有 debug / release 语义差异。
- **Rust 为什么不同**：Rust 觉得“意外溢出”很常是 bug，所以在 debug 构建里更积极地帮你踩刹车。
- **Go 程序员易踩的坑**：默认以为 Rust 和 Go 一样永远静默回绕，结果测试环境里突然 panic。

**记忆点：**

- 编译期可知的溢出：直接报错。
- 运行期溢出：debug 默认 panic，release 默认回绕。
- 需要稳定语义时，优先 `checked_*` / `wrapping_*` / `saturating_*`。

---

## Q6. 浮点数为什么老被说“不适合算钱”？`NaN` 又是什么？ {#q6}
**Tags:** `common` `float` `NaN`
**适用版本:** Rust 1.0+

**一句话答案：**

`f32` / `f64` 是二进制浮点，很多十进制小数不能精确表示；`NaN` 是“不是一个正常数字”的特殊值，所以金额、计费、对账不要直接拿浮点做精确运算。

**解答：**

最经典的例子就是 `0.1 + 0.2 != 0.3`：

```rust
fn main() {
    let x = 0.1f64 + 0.2f64;
    println!("{x:.17}");
}
```

`NaN` 也很关键。它表示“这个结果没有正常数值意义”，比如 `0.0 / 0.0`：

```rust
fn main() {
    let x = 0.0f64 / 0.0;
    println!("{}", x.is_nan());
}
```

金额更推荐“分”为单位的整数，或专门的十进制 crate：

```rust
fn main() {
    let price_cents: i64 = 1999;
    let qty: i64 = 3;
    let total_cents = price_cents * qty;

    println!("{total_cents}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Printf("%.17f\n", 0.1+0.2)
	x := math.NaN()
	fmt.Println(math.IsNaN(x))
}
```

- **Go 怎么做**：同样是 IEEE 754 浮点，同样有精度误差和 `NaN`。
- **Rust 为什么不同**：Rust 不会替你掩盖浮点的不精确性，也不会让 `NaN` 悄悄变成某个合法整数。
- **Go 程序员易踩的坑**：因为 Go 里也常直接写 `float64`，于是把“演示用浮点”一路带进金额逻辑。

**记忆点：**

- 浮点适合科学计算、图形、近似值，不适合精确金额。
- `f64` 是默认浮点类型。
- 判断异常浮点时，用 `is_nan()`、`is_infinite()` 之类方法，不要硬比字符串或魔法值。

---

## Q7. `char` 到底是什么？为什么它不是“长度为 1 的字符串”？ {#q7}
**Tags:** `hot` `beginner` `char` `E0308`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 的 `char` 是一个 **Unicode 标量值**（Unicode scalar value，Unicode 标量值：合法的单个 Unicode 码点），占 4 字节；它像 Go 的 `rune`，不是 `String`，更不是 `&str`。

**解答：**

先看最小例子：

```rust
fn main() {
    let latin: char = 'A';
    let han: char = '中';

    println!("{latin} {han}");
}
```

`char` 可以安全表达一个 Unicode 标量值，所以它固定占 4 字节：

```rust
fn main() {
    println!("{}", std::mem::size_of::<char>());
    println!("{}", std::mem::size_of::<u8>());
}
```

它和字符串是不同类型，不能混用：

```rust
fn main() {
    let ch: char = "A";
    // error[E0308]: mismatched types
    println!("{ch}");
}
```

如果你想把 `char` 变成 `String`，要显式转换：

```rust
fn main() {
    let ch = 'A';
    let s = ch.to_string();

    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var r rune = '中'
	s := string(r)
	fmt.Println(r, s)
}
```

- **Go 怎么做**：单个 Unicode 码点通常用 `rune`，字符串用 `string`。
- **Rust 为什么不同**：Rust 把“一个 Unicode 标量值”和“UTF-8 字符串切片”分得更清楚，避免你把一个字符和一段文本混成一类。
- **Go 程序员易踩的坑**：看到单引号和双引号都像“字符文本”，于是把 `'A'` 和 `"A"` 当成可互换。

**记忆点：**

- `char` 像 Go 的 `rune`。
- `"A"` 是 `&str`，`'A'` 才是 `char`。
- `char` 固定 4 字节，不代表底层 UTF-8 只占 4 字节。

---

## Q8. 元组有什么用？它和数组、结构体分别差在哪？ {#q8}
**Tags:** `common` `tuple`
**适用版本:** Rust 1.0+

**一句话答案：**

元组适合“临时把几项不同类型的数据打成一包”；它长度固定、可异构、用 `.0`、`.1` 访问，但没有字段名，不适合长期表达业务结构。

**解答：**

元组最大的特点是“元素类型可以不一样”：

```rust
fn main() {
    let user = ("alice", 30, true);
    println!("{} {} {}", user.0, user.1, user.2);
}
```

它也很适合从函数里一次返回多个值：

```rust
fn split_point() -> (i32, i32) {
    (3, 4)
}

fn main() {
    let (x, y) = split_point();
    println!("{x} {y}");
}
```

如果这几个值有明确业务含义、会长期传来传去，就该升级成结构体，而不是继续用“第 0 个、第 1 个”硬记。

**Go 对比：**

```go
package main

import "fmt"

func splitPoint() (int, int) {
	return 3, 4
}

func main() {
	x, y := splitPoint()
	fmt.Println(x, y)
}
```

- **Go 怎么做**：更常直接用多返回值，而不是定义元组类型。
- **Rust 为什么不同**：Rust 没有 Go 那种语法级多返回值，所以元组承担了“临时打包多个返回值”的角色。
- **Go 程序员易踩的坑**：把元组当成结构体替代品，最后读代码的人根本记不住 `.0` 到底是什么。

**记忆点：**

- 元组：异构、固定长度、无字段名。
- 临时返回多个值很好用。
- 业务语义重时，尽快换结构体。

---

## Q9. 数组 `[T; N]` 和切片 `&[T]` 到底怎么分？ {#q9}
**Tags:** `hot` `beginner` `array` `slice`
**适用版本:** Rust 1.0+

**一句话答案：**

数组 `[T; N]` 是“拥有数据、长度写在类型里”的固定大小值；切片 `&[T]` 是“借来看一段连续元素”的视图，最适合当函数参数。

**解答：**

数组类型里直接写着长度，所以 `[i32; 3]` 和 `[i32; 4]` 是不同类型：

```rust
fn main() {
    let a: [i32; 3] = [1, 2, 3];
    let b: [i32; 3] = [0; 3];

    println!("{a:?} {b:?}");
}
```

切片更常见，因为它不关心“这段数据原本来自数组还是 `Vec`”，只关心“给我一段连续元素”：

```rust
fn sum(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    let arr = [1, 2, 3];
    println!("{}", sum(&arr));
}
```

数组长度不匹配时，编译器会当成类型错误：

```rust
fn main() {
    let a: [i32; 3] = [1, 2];
    // error[E0308]: mismatched types
    println!("{a:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func sum(xs []int) int {
	total := 0
	for _, x := range xs {
		total += x
	}
	return total
}

func main() {
	arr := [3]int{1, 2, 3}
	fmt.Println(sum(arr[:]))
}
```

- **Go 怎么做**：数组和 slice 也分开，但平时几乎总在用 slice。
- **Rust 为什么不同**：Rust 同样鼓励参数写切片，但数组长度属于类型的一部分，这一点比 Go 更“写在脸上”。
- **Go 程序员易踩的坑**：以为 `[T; N]` 就是 Rust 版 slice；其实它更接近 Go 真正的数组。

**记忆点：**

- `[T; N]` 拥有数据，长度是类型的一部分。
- `&[T]` 是借用视图，常做参数。
- 看到“想接受数组或 `Vec` 都行”，基本就是该写切片了。

---

## Q10. `bool` 为什么不能拿来当整数？ {#q10}
**Tags:** `common` `bool` `E0308`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 故意不把 `bool` 和整数自动互转；条件就是条件，数值就是数值，这样能少掉一大类“真假和数值混用”的歧义。

**解答：**

`bool` 只表示两种状态：`true` 和 `false`。

```rust
fn main() {
    let ok: bool = true;
    if ok {
        println!("ready");
    }
}
```

要转成整数可以，但必须显式写出来：

```rust
fn main() {
    let ok = true;
    let n = ok as u8;
    println!("{n}");
}
```

把整数直接塞进 `if` 条件里会被拒绝：

```rust
fn main() {
    let n = 1;
    if n {
        println!("hi");
    }
    // error[E0308]: mismatched types
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	ok := true
	if ok {
		fmt.Println("ready")
	}
}
```

- **Go 怎么做**：Go 也不允许 `if 1 {}`，这一点和 Rust 很像。
- **Rust 为什么不同**：Rust 进一步连 `bool + 1` 这种隐式数值化也不鼓励，要求你显式 `as`。
- **Go 程序员易踩的坑**：有 C / JavaScript 背景时，下意识把真假和 0/1 当一回事。

**记忆点：**

- 条件只能是 `bool`。
- 要 0/1 请显式 `as u8`。
- Rust 宁愿你多写一点，也不让“真假”和“数值”偷偷串线。

---

## Q11. `String` 和 `&str` 在数据类型层面到底差在哪？ {#q11}
**Tags:** `hot` `beginner` `string` `E0308`
**适用版本:** Rust 1.0+

**一句话答案：**

`String` 是拥有所有权、可增长的 UTF-8 文本；`&str` 是借用来的字符串切片视图。参数位置优先 `&str`，需要拥有或修改文本时再用 `String`。

**解答：**

最基本的分工是：`String` 拥有，`&str` 借用。

```rust
fn main() {
    let owned: String = String::from("hello");
    let borrowed: &str = owned.as_str();

    println!("{owned} {borrowed}");
}
```

函数参数优先写 `&str`，这样字面量和 `String` 借用都能传：

```rust
fn greet(name: &str) {
    println!("hi, {name}");
}

fn main() {
    let s = String::from("rust");
    greet(&s);
    greet("go");
}
```

字面量不是 `String`，不能直接塞给 `String` 类型变量：

```rust
fn main() {
    let s: String = "hello";
    // error[E0308]: mismatched types
    println!("{s}");
}
```

需要拥有所有权时，显式分配：

```rust
fn main() {
    let s1 = "hello".to_string();
    let s2 = String::from("world");

    println!("{s1} {s2}");
}
```

更完整的字符串与文本处理会在 [14-strings-and-text](../14-strings-and-text/) 展开，这里先把类型边界记牢。

**Go 对比：**

```go
package main

import "fmt"

func greet(name string) {
	fmt.Println("hi,", name)
}

func main() {
	s := "rust"
	greet(s)
}
```

- **Go 怎么做**：平时几乎都直接用 `string`，所有权与借用差别不会在类型上显式出现。
- **Rust 为什么不同**：Rust 想把“有没有拥有这段文本”直接写进类型系统里，这对性能和借用检查都很重要。
- **Go 程序员易踩的坑**：把 `String` 当成“Rust 里的字符串默认类型”；其实参数位置大多应该先想 `&str`。

**记忆点：**

- `String`：拥有、可增长、可能分配堆内存。
- `&str`：借用视图、常做参数。
- 字符串字面量 `"hello"` 的类型是 `&'static str`，不是 `String`。

---

## Q12. 为什么 Rust 不做隐式数值转换？ `as`、`From`、`TryFrom` 该怎么选？ {#q12}
**Tags:** `hot` `beginner` `cast` `E0308`
**适用版本:** Rust 1.0+

**一句话答案：**

Rust 故意不做隐式数值转换，因为很多转换会截断、溢出或改符号；能无损时优先 `From` / `Into`，可能失败时用 `TryFrom` / `TryInto`，底层强转才用 `as`。

**解答：**

不同整数类型不能直接混算，先看最常见的报错：

```rust
fn main() {
    let a: u8 = 10;
    let b: u16 = 20;
    let c = a + b;
    // error[E0308]: mismatched types
    println!("{c}");
}
```

无损扩大类型时，用 `From` / `Into` 更表达意图：

```rust
fn main() {
    let a: u8 = 10;
    let b: u16 = 20;
    let c = u16::from(a) + b;

    println!("{c}");
}
```

可能失败的缩窄转换，优先 `TryFrom`：

```rust
fn main() {
    let big: u16 = 300;
    let small = u8::try_from(big);

    println!("{small:?}");
}
```

`as` 能做底层强转，但可能静默截断：

```rust
fn main() {
    let big: u16 = 300;
    let small = big as u8;

    println!("{small}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var a uint8 = 10
	var b uint16 = 20
	c := uint16(a) + b
	fmt.Println(c)
}
```

- **Go 怎么做**：也要求显式转换，但日常主要靠 `T(x)` 这一种写法。
- **Rust 为什么不同**：Rust 把“无损转换”和“可能失败的转换”分成不同 trait，能让 API 语义更清楚。
- **Go 程序员易踩的坑**：上来就全用 `as`，结果把本来应该检查失败的边界静默吞掉了。

**记忆点：**

- 扩大且无损：`u16::from(x)`。
- 可能失败：`u8::try_from(x)`。
- 低层强转：`as`，但要知道它可能丢信息。

---

## Q13. `()` 是什么？为什么“没返回值”在 Rust 里其实也是一个类型？ {#q13}
**Tags:** `common` `unit`
**适用版本:** Rust 1.0+

**一句话答案：**

`()` 叫**单元类型**（unit type，单元类型：只有一个值 `()` 的类型），表示“这里没有有意义的数据”，但它本身依然是一个真类型、真值。

**解答：**

函数不写返回类型时，等价于返回 `()`：

```rust
fn log_ready() {
    println!("ready");
}

fn main() {
    log_ready();
}
```

你也可以把这个返回值显式接住：

```rust
fn log_ready() {
    println!("ready");
}

fn main() {
    let r: () = log_ready();
    println!("{r:?}");
}
```

`Result<(), E>` 也很常见，表示“只关心成功 / 失败，不关心成功时的数据内容”：

```rust
fn save() -> Result<(), &'static str> {
    Ok(())
}

fn main() {
    println!("{:?}", save());
}
```

**Go 对比：**

```go
package main

import "fmt"

func logReady() {
	fmt.Println("ready")
}

func main() {
	logReady()
}
```

- **Go 怎么做**：没有显式的 `void` 值可接住，函数“无返回值”就只是无返回值。
- **Rust 为什么不同**：Rust 把“一切都是表达式”推得更彻底，所以“没有有意义的数据”也被建模成一个正常类型。
- **Go 程序员易踩的坑**：以为 `()` 只是语法噪音，没意识到它经常出现在泛型、`Result<(), E>`、闭包返回值里。

**记忆点：**

- `()` = “没有有意义的数据”，但不是“没有类型”。
- 不写返回类型的函数，默认就是返回 `()`。
- 看到 `Result<(), E>` 时，读作“操作可能失败，但成功时不产出结果”。

---

## Q14. `!`（never type）又是什么？ {#q14}
**Tags:** `common` `never`
**适用版本:** Rust 1.0+（作为发散函数返回类型稳定可用）

**一句话答案：**

`!` 表示“永远到不了返回点”的类型，常见于 `panic!`、无限循环、直接退出程序之类的代码路径。

**解答：**

最容易理解的例子是死循环：

```rust
fn forever() -> ! {
    loop {
        std::hint::spin_loop();
    }
}

fn main() {
    let _f: fn() -> ! = forever;
}
```

`panic!` 也属于“不会正常返回”的路径，所以它能出现在本来应该返回别的类型的分支里：

```rust
fn must_be_positive(x: i32) -> u32 {
    if x < 0 {
        panic!("negative");
    }
    x as u32
}

fn main() {
    println!("{}", must_be_positive(3));
}
```

**Go 对比：**

```go
package main

import "fmt"

func mustBePositive(x int) uint32 {
	if x < 0 {
		panic("negative")
	}
	return uint32(x)
}

func main() {
	fmt.Println(mustBePositive(3))
}
```

- **Go 怎么做**：也有 `panic` 和无限循环，但没有把“永不返回”建成一个显式类型。
- **Rust 为什么不同**：Rust 的类型系统把这条信息也利用起来，帮助 `match`、`if` 等表达式在分支类型上达成一致。
- **Go 程序员易踩的坑**：把 `!` 看成“逻辑非号的变体”；它其实是一个类型，不是操作符。

**记忆点：**

- `!` = never type = 永不正常返回。
- 死循环、`panic!`、进程退出路径都可能涉及它。
- 平时不常手写，但读错误信息和标准库签名时会遇到。

---

## Q15. 类型别名 `type` 和 newtype 有什么本质区别？ {#q15}
**Tags:** `common` `alias` `newtype`
**适用版本:** Rust 1.0+

**一句话答案：**

类型别名只是“换个名字”，不会产生新类型；newtype 则是真正的新类型，能隔离语义、避免误传、单独实现 trait。

**解答：**

类型别名不会改变类型系统眼中的身份：

```rust
type UserId = u64;

fn takes_user_id(id: UserId) {
    println!("{id}");
}

fn main() {
    let id: u64 = 7;
    takes_user_id(id);
}
```

newtype 通常是一个单字段元组结构体，它和原类型已经不是一回事：

```rust
struct UserId(u64);

fn takes_user_id(id: UserId) {
    println!("{}", id.0);
}

fn main() {
    let id = UserId(7);
    takes_user_id(id);
}
```

newtype 最值钱的地方，是它能防止“两个底层都叫 `u64` 的概念”互相传错。

**Go 对比：**

```go
package main

import "fmt"

type UserID uint64

func takesUserID(id UserID) {
	fmt.Println(id)
}

func main() {
	var id UserID = 7
	takesUserID(id)
}
```

- **Go 怎么做**：`type UserID uint64` 会定义新类型；`type UserID = uint64` 才是别名。
- **Rust 为什么不同**：Rust 的别名和 newtype 分工也很清楚，只是 newtype 通常写成结构体包装。
- **Go 程序员易踩的坑**：把 Rust `type UserId = u64;` 误以为是 Go 的“新定义类型”；其实它只是换个名字。

**记忆点：**

- 别名：只改可读性，不改类型身份。
- newtype：真新类型，适合建立业务边界。
- 一看到“账号 ID”和“订单 ID”底层都同型但不能混，优先想 newtype。

---

## Q16. 为什么 `str`、`[T]` 这种类型不能直接单独当局部变量用？ {#q16}
**Tags:** `occasional` `DST` `E0277`
**适用版本:** Rust 1.0+

**一句话答案：**

因为 `str` 和 `[T]` 是 **DST**（Dynamically Sized Type，动态大小类型：编译期不知道具体大小），它们必须躲在某种指针或引用后面使用，比如 `&str`、`&[T]`、`Box<str>`。

**解答：**

`&str` 和 `&[T]` 很常见，但裸 `str`、裸 `[T]` 几乎不会直接出现为局部变量类型：

```rust
fn takes_text(s: &str) {
    println!("{s}");
}

fn takes_slice(xs: &[i32]) {
    println!("{}", xs.len());
}

fn main() {
    takes_text("hello");
    takes_slice(&[1, 2, 3]);
}
```

装箱后也可以，因为 `Box` 自己大小固定，盒子里再指向动态大小的数据：

```rust
fn main() {
    let text: Box<str> = "hello".into();
    println!("{text}");
}
```

裸 `str` 会直接触发“编译期大小未知”的错误：

```rust
fn main() {
    let s: str = *"hello";
    // error[E0277]: the size for values of type `str` cannot be known at compilation time
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func takesText(s string) {
	fmt.Println(s)
}

func main() {
	takesText("hello")
}
```

- **Go 怎么做**：`string` 和 slice 都是语言内建的一等值类型，使用者不需要显式面对“动态大小类型”这个概念。
- **Rust 为什么不同**：Rust 要明确区分“值本体大小编译期是否已知”，因为这会影响栈上布局、泛型默认约束和 ABI。
- **Go 程序员易踩的坑**：看到 `&str` 很常见，就以为 `str` 只是“少个 `&`”；其实两者地位完全不同。

**记忆点：**

- `str`、`[T]`、`dyn Trait` 都是 DST。
- DST 通常通过 `&`、`Box`、`Rc`、`Arc` 等指针间接使用。
- 参数位置最常见的是 `&str` 和 `&[T]`。

---

## Q17. 零大小类型（ZST）是什么，有什么实际意义？ {#q17}
**Tags:** `occasional` `ZST`
**适用版本:** Rust 1.0+

**一句话答案：**

**ZST**（Zero-Sized Type，零大小类型）是“有类型语义，但编译后不占空间”的类型；它常用于标记、泛型占位、表达“只关心存在性不关心数据内容”。

**解答：**

最典型的 ZST 就是 `()` 和空结构体：

```rust
struct Marker;

fn main() {
    println!("{}", std::mem::size_of::<Marker>());
    println!("{}", std::mem::size_of::<()>());
}
```

它们的价值在于“传递语义”，而不是存数据：

```rust
use std::collections::HashSet;

fn main() {
    let mut set = HashSet::new();
    set.insert("go");
    set.insert("rust");

    println!("{}", set.contains("rust"));
}
```

从实现角度看，`HashSet<T>` 就很像“把值类型设成 `()` 的 `HashMap<T, ()>` 思路”。

**Go 对比：**

```go
package main

import "fmt"

type Marker struct{}

func main() {
	set := map[string]struct{}{
		"go":   {},
		"rust": {},
	}
	_, ok := set["rust"]
	fmt.Println(Marker{}, ok)
}
```

- **Go 怎么做**：`struct{}` 也常被用作 set 的 value，占位但不存数据。
- **Rust 为什么不同**：Rust 更经常把 ZST 参与到泛型、trait、类型系统设计里，而不仅仅是节省空间的小技巧。
- **Go 程序员易踩的坑**：以为“零大小”就等于“没意义”；其实它往往恰恰在表达类型语义。

**记忆点：**

- ZST 可以有强语义，但几乎无运行时大小。
- 常见例子：`()`、空结构体、一些 marker type。
- 它们经常是“类型系统工具”，不是“业务数据载体”。

---

## Q18. `Sized` 和 DST 是什么关系？为什么泛型默认不接受 `str` 这种类型？ {#q18}
**Tags:** `advanced` `Sized` `DST`
**适用版本:** Rust 1.0+

**一句话答案：**

泛型参数默认都带着 `T: Sized`，也就是“编译期大小已知”；`str`、`[T]`、`dyn Trait` 这类 DST 不满足这个默认约束，所以要通过引用或 `T: ?Sized` 才能接住它们。

**解答：**

普通泛型函数默认只接收固定大小类型：

```rust
fn print_len<T: AsRef<str>>(s: T) {
    println!("{}", s.as_ref().len());
}

fn main() {
    print_len("hello");
    print_len(String::from("rust"));
}
```

如果你想显式接受“也许是 DST”的引用，需要写 `?Sized`：

```rust
use std::fmt::Display;

fn show<T: ?Sized + Display>(value: &T) {
    println!("{value}");
}

fn main() {
    show("hello");
}
```

直接把 DST 当作普通泛型实参，通常会撞上 `Sized` 约束：

```rust
fn need_sized<T>(_: T) {}

fn main() {
    let s: &str = "hello";
    need_sized::<str>(*s);
    // error[E0277]: the size for values of type `str` cannot be known at compilation time
}
```

**Go 对比：**

```go
package main

import "fmt"

func show[T fmt.Stringer](v T) {
	fmt.Println(v.String())
}

type Name string

func (n Name) String() string { return string(n) }

func main() {
	show(Name("rust"))
}
```

- **Go 怎么做**：Go 泛型不会把“值大小是否编译期已知”暴露成一条显式约束给你。
- **Rust 为什么不同**：Rust 的泛型要和内存布局、栈上传值、单态化代码生成严丝合缝地配合，所以 `Sized` 成了默认假设。
- **Go 程序员易踩的坑**：以为 `T` 就该“什么都能放”；在 Rust 里，泛型默认是“什么普通固定大小类型都能放”。

**记忆点：**

- 泛型默认：`T: Sized`。
- 想接受 DST，一般写成 `&T` 并加 `T: ?Sized`。
- `&str` 很常见，不代表裸 `str` 也是普通值类型。

---

## Q19. 为什么浮点数不宜当 `HashMap` 的 key？和 `NaN` 有什么关系？ {#q19}
**Tags:** `hot` `float` `HashMap` `NaN` `Eq` `Hash`
**适用版本:** Rust 1.0+

**一句话答案：**

`f32` / `f64` 不实现 `Eq` 与 `Hash`（主要因为 `NaN` 破坏“相等必可哈希、且相等可传递”的假设），所以根本不能当 `HashMap` 键；即便绕开，浮点近似相等也会让查找语义崩掉。金额与精确键请用整数或定点数（见 [Q6](#q6)）。

**解答：**

`HashMap<K, V>` 要求 `K: Eq + Hash`。浮点只有 **PartialEq**（可部分比较），因为 `NaN != NaN`，不满足 **Eq**（完全等价关系）所需的自反性。

直接写就编译不过：

```rust
use std::collections::HashMap;

fn main() {
    let mut bad: HashMap<f64, i32> = HashMap::new();
    // bad.insert(1.0, 1);
    // error[E0599]: the method `insert` exists for struct `HashMap<f64, i32>`, but its trait bounds were not satisfied
    //   = note: the following trait bounds were not satisfied:
    //           `f64: Eq`
    //           `f64: Hash`
    let _ = &bad;

    let mut m: HashMap<i64, i32> = HashMap::new();
    m.insert(1, 1); // 用整数键才行
    println!("{}", m[&1]);
}
```

`NaN` 本身也不能当“稳定身份”：

```rust
fn main() {
    let nan = f64::NAN;
    println!("{}", nan == nan); // false
    println!("{}", nan.is_nan()); // true
}
```

实务做法：把浮点量化成整数键（分、毫秒、定点数），或用有序结构 + 显式容差比较，而不是哈希查找：

```rust
use std::collections::HashMap;

fn main() {
    // 例如价格精确到“分”
    let mut prices: HashMap<i64, &str> = HashMap::new();
    prices.insert(1999, "sku-a"); // 19.99 元
    assert_eq!(prices.get(&1999), Some(&"sku-a"));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	m := map[float64]int{}
	m[1.0] = 1
	m[math.NaN()] = 2
	fmt.Println(m[1.0], math.IsNaN(math.NaN()), m[math.NaN()]) // 最后一个通常取不到
}
```

- **Go 怎么做**：`map[float64]T` 语法上允许，但 `NaN` 作键几乎查不回来，属于静默坑。
- **Rust 为什么不同**：类型系统直接禁止不可靠的键类型，把坑挡在编译期。
- **Go 程序员易踩的坑**：以为“Go 都能用 float 当 key，Rust 也应该行”；在 Rust 里请先换成整数键。

**记忆点：**

- `HashMap` 键要 `Eq + Hash`；`f64` 都没有。
- 根因是 `NaN`：自己不等于自己。
- 精确键用整数/定点数，浮点只做近似计算。

---

## Q20. `as` 截断和 `TryFrom` 到底差在哪？什么时候绝不能用 `as`？ {#q20}
**Tags:** `common` `cast` `TryFrom` `as`
**适用版本:** Rust 1.0+

**一句话答案：**

`as` 在整数缩窄时会**静默截断**（按位丢掉高位），编译期不报错；`TryFrom` / `TryInto` 在放不下时返回 `Err`。边界可能越界、来自外部输入、或失败必须处理时，用 `TryFrom`，不要用 `as`（总览见 [Q12](#q12)）。

**解答：**

同一数值，两种路径结果完全不同：

```rust
fn main() {
    let big: u16 = 300;
    let truncated = big as u8; // 300 = 0x012C → 低 8 位 0x2C = 44
    let checked = u8::try_from(big); // Err(TryFromIntError)
    println!("{truncated} {checked:?}");
}
```

有符号溢出同样危险——`as` 不帮你喊停：

```rust
fn main() {
    let n: i32 = -1;
    let as_u8 = n as u8; // 按补码位型转成 255，不是 Err
    let try_u8 = u8::try_from(n); // Err
    println!("{as_u8} {try_u8:?}");
}
```

「✅ 正确写法」——解析/协议/配置里对失败显式分支：

```rust
fn port_from_u32(n: u32) -> Result<u16, String> {
    u16::try_from(n).map_err(|_| format!("port out of range: {n}"))
}

fn main() {
    assert_eq!(port_from_u32(8080).unwrap(), 8080);
    assert!(port_from_u32(70000).is_err());
}
```

`as` 仍适合：你**明确知道**在范围内（刚做过边界检查）、或在做底层位宽变换且截断就是意图（掩码、校验和等）。扩大且无损时优先 `From`，别习惯性 `as`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	var big uint16 = 300
	small := uint8(big) // 同样静默变成 44
	fmt.Println(small)
}
```

- **Go 怎么做**：`T(x)` 转换也常静默截断，靠你自己检查。
- **Rust 为什么不同**：提供 `TryFrom` 把“可能失败”写进类型，强制处理 `Result`。
- **Go 程序员易踩的坑**：把 `as` 当成 Go 的 `uint8(x)` 随手写，漏掉边界错误。

**记忆点：**

- `as` 缩窄 ≈ 静默截断；`TryFrom` ≈ 可能 `Err`。
- 外部输入 / 端口 / 长度 → `TryFrom`。
- 已证明安全或故意要位截断 → 才考虑 `as`。

---
