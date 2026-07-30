+++
title = "12-references-and-borrowing"
date = 2026-07-28T14:49:00+08:00
weight = 120
type = "docs"
description = "面向熟悉 Go 的读者讲清引用、可变借用、冲突与 NLL"
isCJKLanguage = true
draft = false

+++

# 引用与借用 (References and Borrowing)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会把 `&T` / `&mut T` 当成 Go 的普通指针，结果一改就撞上 `error[E0502]` / `error[E0499]`？
- 你是否想知道：为什么 `HashMap::get` 之后不能立刻 `insert`，Go 里却很自然？
- 你是否分不清 **NLL**（Non-Lexical Lifetimes，非词法生命周期）到底放宽了什么、没放宽什么？
- 你是否写过 `for x in &v { v.push(...) }`，却不懂编译器在防什么真实内存错误？
- 你是否需要一套「先缩作用域 / 再换 API / 最后才 clone 或内部可变」的日常判断流程？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| reference | — | 引用 | 指向某值的借用指针，不拥有该值 | `*T` / 切片头，近似 |
| borrow | — | 借用 | 临时只读或可写访问，但不接管所有权 | 传指针 / 传切片头 |
| shared borrow | `&T` | 共享借用 | 可同时存在多个的只读借用 | 多个只读指针，近似 |
| mutable borrow | `&mut T` | 可变借用 | 同一时刻只能有一个的独占可写借用 | 无编译期对应 |
| borrow checker | — | 借用检查器 | 编译期检查引用别名与生命周期的规则引擎 | Go 无 |
| **NLL** | Non-Lexical Lifetimes | 非词法生命周期 | 借用活到最后一次使用，而不必活到 `}` | Go 无 |
| reborrow | — | 再借用 | 从已有借用上临时再借一层，内层结束后外层恢复 | Go 无直接对应 |
| lifetime | — | 生命周期 | 引用允许存在的时间范围（类型系统里的标注） | Go 无 |
| dangling reference | — | 悬垂引用 | 指向已释放内存的引用 | 悬空指针 |
| **Deref** | — | 解引用强制转换 | 如 `&String` 自动当 `&str` 用 | Go 无同名机制 |
| interior mutability | — | 内部可变性 | 通过共享引用仍能改内部数据（运行时检查） | 无直接对应 |
| `Cell<T>` | — | 按值内部可变 | 共享下整值替换 / `Copy` 读写，不借出引用 | 无 |
| `RefCell<T>` | — | 运行时借用检查 | 共享下借出 `&T`/`&mut T`，违规则 panic | 无 |
| `'static` | — | 静态生命周期 | 能活到程序结束的引用生命周期 | 包级变量，近似 |
| `T: 'static` | — | 静态约束 | 类型内部不含短生命周期借用 | 拥有数据的值，近似 |
| owner | — | 所有者 | 负责最终释放该值的绑定 | 无（Go 靠 GC） |
| **GC** | Garbage Collector | 垃圾回收器 | 运行时回收不用对象 | Go 默认机制 |
| **RAII** | Resource Acquisition Is Initialization | 资源获取即初始化 | 资源随作用域结束自动释放 | `defer` 手动模拟 |
| **UB** | Undefined Behavior | 未定义行为 | 语言不保证结果的非法操作 | 数据竞争等 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q21](#q21) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q22](#q22) |
| `occasional` | [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `advanced` | [Q19](#q19), [Q20](#q20) |

---

## Q1. `&T` 和 `&mut T` 的底层规则到底是什么？ {#q1}
**Tags:** `hot` `beginner` `borrowing`
**适用版本:** Rust 1.0+（1.97.1 行为一致）

**一句话答案：**

对同一数据，同一时刻要么任意多个共享借用 `&T`，要么唯一一个可变借用 `&mut T`——二者不可并存；借用不转移所有权（ownership，所有权，见 [11-ownership](../11-ownership/#q1)）。

**解答：**

`&x` 创建对 `x` 的**共享借用**（shared borrow，类型 `&T`，只读）；`&mut x` 创建**可变借用**（mutable borrow，类型 `&mut T`，独占可写）。两者都不吃掉所有者，用完后原变量仍可用。

硬规则只有一条：

- 可有任意多个 `&T`，**或**
- 只能有一个 `&mut T`

不能同时既有人读又有人改。这在单线程也成立——防的是逻辑别名错误，不只是数据竞争。

```rust
fn main() {
    let mut x = 1;
    let a = &x;
    let b = &x; // 多个共享借用 OK
    println!("{a} {b}");
    // a、b 用完后，可变借用才登场
    let m = &mut x;
    *m += 1;
    println!("{m}");
}
```

共享借用存活期间不能再拿可变借用：

```rust
fn main() {
    let mut s = String::from("hi");
    let r = &s;
    // s.push('!');
    // error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
    println!("{r}");
}
```

函数参数用借用时，调用方继续拥有值：

```rust
fn bump(x: &mut i32) {
    *x += 1;
}

fn show(s: &str) {
    println!("{s}");
}

fn main() {
    let mut n = 1;
    bump(&mut n);
    let s = String::from("hello");
    show(&s);
    println!("{n} {s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func bump(x *int) {
	*x = *x + 1
}

func main() {
	n := 1
	bump(&n)
	fmt.Println(n) // 两边都能继续用指针语义
}
```

- **Go 怎么做**：传 `*T` 很常见，别名安全靠约定和 race detector。
- **Rust 为什么不同**：把「能否同时读写同一值」提前到编译期的借用检查器（borrow checker）。
- **Go 程序员易踩的坑**：把 `&mut` 当成普通指针；它是带独占承诺的借用，不是“随便传的地址”。

**记忆点：**

- `&T` = 只读访客证（可多张）；`&mut T` = 独占施工证（同时只能一张）。
- 借用 ≠ move：所有者还在。
- `E0502` = 共享与可变冲突；`E0499` = 两个可变冲突。

---

## Q2. 为什么不能同时拿两个可变借用？ {#q2}
**Tags:** `hot` `beginner` `mut-borrow`
**适用版本:** Rust 1.0+；NLL 改善诊断但独占规则不变

**一句话答案：**

`&mut` 承诺「我是此刻唯一写入者」；两个同时存活的可变借用会破坏该承诺，编译器报 `error[E0499]`。

**解答：**

经典踩坑：想同时改 `v[0]` 和 `v[1]`。`&mut v[i]` 在类型系统里是先对**整个** `v` 做可变借用再索引——借用检查器不做「下标不同就不重叠」的值级证明。

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &mut v[0];
    let second = &mut v[1];
    // error[E0499]: cannot borrow `v` as mutable more than once at a time
    *first += 10;
    *second += 10;
}
```

顺序使用：上一个 `&mut` 用完后再借下一个——在 **NLL**（Non-Lexical Lifetimes，非词法生命周期，详见 [Q5](#q5)）下自然合法：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &mut v[0];
    *first += 10; // first 最后一次使用，借用结束
    let second = &mut v[1];
    *second += 10;
    assert_eq!(v, [11, 12, 3]);
}
```

需要**同时**持有两段不重叠的可变切片时，用标准库 API（内部用 unsafe 证明不重叠，对外安全）：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let (left, right) = v.split_at_mut(2);
    left[0] += 10;
    right[0] += 10;
    // 1.86+：一次拿多个互不重叠的 &mut
    if let Ok([x, z]) = v.get_disjoint_mut([0, 2]) {
        *x += 1;
        *z += 1;
    }
    assert_eq!(v, [12, 2, 14, 4]);
}
```

更多见 [Q14](#q14)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	p0, p1 := &v[0], &v[1] // Go 允许同时持有
	*p0 += 10
	*p1 += 10
	fmt.Println(v)
}
```

- **Go 怎么做**：切片元素地址可同时持有；安全靠程序员约定。
- **Rust 为什么不同**：默认拒绝「整容器上的双重可变别名」，除非你用证明过不重叠的 API。
- **Go 程序员易踩的坑**：以为「下标不同」编译器会自动放行——不会。

**记忆点：**

- 两个活着的 `&mut` 同一数据 → `E0499`。
- 先用完再借下一个；或 `split_at_mut` / `get_disjoint_mut`。
- 不要自己写原始指针“拆别名”，优先标准库。

---

## Q3. 为什么“先借后改”会报 `E0502`？ {#q3}
**Tags:** `hot` `beginner` `E0502`
**适用版本:** Rust 1.0+

**一句话答案：**

共享借用还活着时再要可变借用，就是 `error[E0502]`；先结束只读借用（或先拷贝出需要的值），再改。

**解答：**

「先借后改」指：手里还拿着 `&T`，又对同一所有者调用需要 `&mut` 的操作。

```rust
fn main() {
    let mut s = String::from("hi");
    let r = &s;
    s.push_str("!");
    // error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
    println!("{r}");
}
```

修法一：读完再用（NLL 下借用止于最后一次使用）：

```rust
fn main() {
    let mut s = String::from("hi");
    let r = &s;
    println!("{r}"); // r 用完，共享借用结束
    s.push_str("!");
    println!("{s}");
}
```

修法二：先把需要的数据拷成拥有值，再改容器：

```rust
fn main() {
    let mut s = String::from("hello");
    let first = s.chars().next(); // Option<char>，不再挂着对 s 的借用
    s.push('!');
    println!("{first:?} {s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := []byte("hi")
	r := &s[0]
	s = append(s, '!') // 可能换底层数组；r 可能悬空——Go 编译器不拦
	fmt.Println(*r, string(s))
}
```

- **Go 怎么做**：编译器通常不拦「边持指针边扩容」。
- **Rust 为什么不同**：`E0502` 正是在编译期挡住「引用还活着却让底层失效」的路径。
- **Go 程序员易踩的坑**：看到 `E0502` 以为编译器“太严”；它常在防真实的悬垂。

**记忆点：**

- `E0502` = 不可变借用还在，又要可变。
- 先结束读，或先 `copy`/`clone`/`copied()` 再改。
- 与 [Q4](#q4)、[Q9](#q9) 是同一类问题。

---

## Q4. 为什么 `HashMap::get` 之后不能立刻 `insert`？ {#q4}
**Tags:** `hot` `intermediate` `hashmap`
**适用版本:** 全版本；NLL 有时仍不够（引用还被后续使用）

**一句话答案：**

`get` 返回的引用生命周期绑在整个 `map` 上；`insert` 需要 `&mut map` 且可能 rehash，使旧引用失效——故与存活的共享借用冲突（`E0502`）。

**解答：**

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<String, i32> = HashMap::from([("key".into(), 1)]);
    let v = map.get("key").unwrap(); // v: &i32，借用挂在 map 上
    map.insert("key2".into(), 2);
    // error[E0502]: cannot borrow `map` as mutable because it is also borrowed as immutable
    println!("{v}");
}
```

常见修法：

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<String, i32> = HashMap::from([("key".into(), 1)]);

    // 1) 先变成拥有 / Copy 值，借用立刻结束
    let v = map.get("key").copied(); // 非 Copy 值用 cloned()
    map.insert("key2".into(), 2);
    println!("{v:?}");

    // 2) 读完再写（NLL：借用止于最后一次使用）
    println!("{:?}", map.get("key"));
    map.insert("key3".into(), 3);

    // 3) entry API：一次查找完成“不存在则插入 / 存在则修改”
    *map.entry("key".into()).or_insert(0) += 1;
    println!("{map:?}");
}
```

若只是「没有则插入」，优先 `entry`，避免手搓 get+insert 两阶段：

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.entry("a").or_insert(1);
    map.entry("a").and_modify(|n| *n += 1).or_insert(0);
    assert_eq!(map["a"], 2);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{"key": 1}
	v := m["key"] // 得到的是值拷贝（对 int）
	m["key2"] = 2
	fmt.Println(v, m)
}
```

- **Go 怎么做**：`m[k]` 对小类型常是值拷贝；对指针/切片仍可能共享，靠约定。
- **Rust 为什么不同**：`get` 默认借出 `&V`，与可能触发 rehash 的 `insert` 冲突。
- **Go 程序员易踩的坑**：把 `get` 想成“取出一份副本”；对非 `Copy` 值它往往是借用。

**记忆点：**

- `get` 后还要用引用 → 别立刻 `insert`。
- `copied()` / `cloned()` / 先读后写 / `entry`。
- 根因与 [Q3](#q3)、[Q9](#q9) 相同：借用期间不能让容器失效。

---

## Q5. NLL（非词法生命周期）到底帮了什么忙？ {#q5}
**Tags:** `hot` `intermediate` `nll`
**适用版本:** NLL 自 1.31（2018 edition）引入，1.36 起所有 edition 默认；1.97.1 无需开关

**一句话答案：**

**NLL**（Non-Lexical Lifetimes，非词法生命周期）让借用活到**最后一次使用**，而不必拖到外层 `}`；它不放宽别名规则，只是更精确地结束借用。

**解答：**

旧词法模型：借用活到作用域花括号结束。NLL：分析控制流，用完即可结束。

```rust
fn main() {
    let mut x = 1;
    let r = &x;
    println!("{r}"); // 最后使用 r
    x += 1; // NLL 下 OK；旧模型可能报错
    println!("{x}");
}
```

NLL **不**允许真正的别名可变。下面仍然失败——因为 `r` 在可变操作之后还被使用：

```rust
fn main() {
    let mut x = 1;
    let r = &x;
    x += 1;
    // error[E0502]: cannot borrow `x` as mutable because it is also borrowed as immutable
    println!("{r}");
}
```

对「读完再写」的日常代码，NLL 省掉许多多余的 `{}`：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let n = v.len(); // 临时借用，用完即结束
    v.push(n);
    assert_eq!(v, [1, 2, 3, 3]);
}
```

遇到 Stack Overflow 旧答案说「必须加大括号」时，先在当前版本试一下——许多已不再需要；仍失败时再主动缩作用域（见 [Q8](#q8)）。

**Go 对比：**

- **Go 怎么做**：没有借用检查器，也就没有 NLL 这种“精确结束借用”的概念。
- **Rust 为什么不同**：NLL 是借用检查器的精度升级，不是新语法开关。
- **Go 程序员易踩的坑**：看到旧文说“必须 `{}`”，在 1.97 里盲加括号；先确认引用是否还在后面被使用。

**记忆点：**

- NLL = 活到最后一次使用，不是活到 `}`。
- 不改变「共享 / 可变互斥」铁律。
- 旧答案里的大括号，很多已过时。

---

## Q6. 函数参数为什么常写成 `&str` 而不是 `&String`？ {#q6}
**Tags:** `common` `beginner` `deref` `api`
**适用版本:** Rust 1.0+

**一句话答案：**

`&str` 更通用：`String`、字符串字面量、子切片都能传入（借助 **Deref** 强制转换）；`&String` 只接受 `String` 的借用。

**解答：**

**Deref**（解引用强制转换）让 `&String` 在需要 `&str` 的地方自动转换。API 写成 `&str`，调用方最省事：

```rust
fn takes(s: &str) {
    println!("{s}");
}

fn main() {
    let owned = String::from("hi");
    takes(&owned); // &String -> &str
    takes("literal"); // &'static str
    takes(&owned[0..1]); // 子切片
}
```

若写成 `&String`，字面量就不能直接传：

```rust
fn only_string(s: &String) {
    println!("{s}");
}

fn main() {
    let owned = String::from("hi");
    only_string(&owned);
    // only_string("literal");
    // error[E0308]: mismatched types
    //   expected `&String`, found `&str`
}
```

切片同理：参数优先 `&[T]` 而不是 `&Vec<T>`。

```rust
fn sum(xs: &[i32]) -> i32 {
    xs.iter().sum()
}

fn main() {
    let v = vec![1, 2, 3];
    let a = [4, 5];
    println!("{} {}", sum(&v), sum(&a));
}
```

**Go 对比：**

```go
package main

import "fmt"

func takes(s string) { // Go 的 string 本身是只读头
	fmt.Println(s)
}

func main() {
	takes("literal")
	takes(string([]byte("hi")))
}
```

- **Go 怎么做**：`string` / `[]T` 本身就是“视图头”，API 很少再套一层“指向 string 的指针”才接受。
- **Rust 为什么不同**：`String` 是拥有者，`str` 是 DST（Dynamically Sized Type，动态大小类型）切片；参数用 `&str` 对齐“只读视图”。
- **Go 程序员易踩的坑**：把 `String` 当成 Go 的 `string`，参数写成 `&String` 反而把 API 写窄了。

**记忆点：**

- 只读字符串参数 → `&str`；只读序列 → `&[T]`。
- 需要拥有 / 修改再收 `String` / `&mut String`。
- Deref 是便利，不是所有权转移。

---

## Q7. reborrow（再借用）是什么？ {#q7}
**Tags:** `common` `intermediate` `reborrow`
**适用版本:** 全版本

**一句话答案：**

**reborrow**（再借用）是从已有 `&mut T` 上临时再借出 `&mut T` 或 `&T`；内层结束后外层可变借用恢复，而不是把外层引用 move 走。

**解答：**

传给函数时经常发生隐式 reborrow，因此可以多次把同一个 `&mut` 交给不同调用（非同时重叠）：

```rust
fn helper(x: &mut i32) {
    *x += 1;
}

fn main() {
    let mut n = 0;
    let r = &mut n;
    helper(r); // 隐式 reborrow
    helper(r); // 再次 OK
    *r += 1;
    assert_eq!(n, 3);
}
```

显式写法是 `&mut *r`：从 `r` 指向的数据上再借一次，而不是移动 `r` 本身：

```rust
fn main() {
    let mut n = 0;
    let r = &mut n;
    let r2 = &mut *r; // 显式 reborrow：r 暂时“冻结”
    *r2 += 1; // r2 最后使用，内层结束
    *r += 1; // 外层恢复
    assert_eq!(n, 2);
}
```

对比：`let r2 = r;` 对 `&mut T` 是 move，之后 `r` 不能再用：

```rust
fn main() {
    let mut n = 0;
    let r = &mut n;
    let r2 = r; // move，不是 reborrow
    *r2 += 1;
    // println!("{r}");
    // error[E0382]: borrow of moved value: `r`
    assert_eq!(n, 1);
}
```

也可把 `&mut T` **降级**再借为 `&T`（共享期间不能通过原 `&mut` 写入，见 [Q11](#q11)）。

**Go 对比：**

- **Go 怎么做**：指针赋值是复制指针值，没有“可变借用被 move / reborrow”之分。
- **Rust 为什么不同**：`&mut T` 不是 `Copy`，必须区分 move 与临时再借，才能维持独占。
- **Go 程序员易踩的坑**：对 `&mut` 做 `let y = x` 后还想用 `x`——应写成 `&mut *x` 或继续隐式传参。

**记忆点：**

- 函数参数上的 `&mut` 传参多半是 reborrow。
- 显式：`&mut *r`；移动：`let r2 = r`。
- 内层活着时外层冻结；内层结束外层恢复。

---

## Q8. 什么时候该把借用缩进更小的作用域？ {#q8}
**Tags:** `common` `beginner` `scope`
**适用版本:** 全版本；多数情况 NLL 已够，仍失败时再手动缩

**一句话答案：**

当引用在控制流上“看起来还活着”、但你逻辑上已用完，或编译器推断不够聪明时，用 `{ ... }` 或尽早结束使用，强制缩短借用。

**解答：**

NLL 之后，许多“读完再写”已不需要大括号。仍建议主动缩作用域的典型场景：借用变量名在后面还存在、但中间夹了可变操作；或匹配/分支里借用跨度难读。

```rust
fn main() {
    let mut map = std::collections::HashMap::from([("a", 1)]);
    {
        let v = map.get("a").copied();
        println!("{v:?}");
    } // 即使不用 copied，花括号也能帮人读清“读阶段结束”
    map.insert("b", 2);
    println!("{map:?}");
}
```

对比：同一名字一直活到函数尾，中间又改所有者——更容易踩 `E0502`：

```rust
fn main() {
    let mut s = String::from("x");
    let r = s.as_str();
    // s.push('y');
    // error[E0502]: cannot borrow `s` as mutable because it is also borrowed as immutable
    println!("{r}");
}
```

修法：缩小读阶段，或拷贝出需要的数据：

```rust
fn main() {
    let mut s = String::from("x");
    let snapshot = s.clone(); // 或先 println 完再改
    s.push('y');
    println!("{snapshot} {s}");
}
```

**Go 对比：**

- **Go 怎么做**：没有借用作用域概念；最多靠短生命周期变量提高可读性。
- **Rust 为什么不同**：作用域与使用点共同决定借用何时结束。
- **Go 程序员易踩的坑**：变量名“还在”就以为借用一定还在——看最后一次使用，必要时再加 `{}`。

**记忆点：**

- 先靠 NLL；不够再 `{ }` 或提前 `drop` 逻辑结束使用。
- 缩作用域是可读性工具，也是拆冲突工具。
- 与 [Q5](#q5)、[Q19](#q19) 配套。

---

## Q9. 为什么借用期间不能让容器扩容？ {#q9}
**Tags:** `common` `intermediate` `vec` `reallocation`
**适用版本:** 全版本

**一句话答案：**

扩容（如 `Vec::push` 触发重分配）可能搬迁堆缓冲区，使仍存活的元素引用变成悬垂引用；借用规则在编译期直接禁止这条路径。

**解答：**

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let first = &v[0];
    v.push(4);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{first}");
}
```

安全模式：先算完要追加的数据，结束借用，再改容器；或只用索引（在固定 `len` 范围内）：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let extra: Vec<i32> = v.iter().map(|x| x * 10).collect();
    v.extend(extra);
    for i in 0..v.len() {
        v[i] += 1; // 索引访问，不长期持有 &元素
    }
    println!("{v:?}");
}
```

`HashMap::insert` 可能 rehash，同理——见 [Q4](#q4)。内存布局细节见 [15-memory-and-allocation](../15-memory-and-allocation/#q9)。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	p := &v[0]
	v = append(v, 4) // 可能换底层数组
	fmt.Println(*p, v) // 可能读到垃圾或旧数组——编译器不拦
}
```

- **Go 怎么做**：`append` 是否换底层靠运行时；持有元素指针时扩容是经典坑。
- **Rust 为什么不同**：直接不让你在借用元素时扩容。
- **Go 程序员易踩的坑**：把 Rust 的拒绝当成繁琐；它防的正是 Go 里要小心的悬空。

**记忆点：**

- 持有 `&v[i]` / `map.get` 结果时 → 别 `push`/`insert`。
- 先收集、再修改；或改用索引 / `entry`。
- 扩容 = 可能搬迁 = 旧引用作废。

---

## Q10. 可变借用为什么不是 `Copy`？ {#q10}
**Tags:** `common` `intermediate` `copy` `mut`
**适用版本:** 全版本

**一句话答案：**

`&T` 是 `Copy`（多份只读别名合法）；`&mut T` 若可 Copy 就会凭空复制出第二张独占施工证，破坏唯一可变规则，因此赋值是 move。

**解答：**

共享借用可以复制：

```rust
fn main() {
    let x = 1;
    let a = &x;
    let b = a; // &i32: Copy
    println!("{a} {b}");
}
```

可变借用赋值会移走：

```rust
fn main() {
    let mut x = 1;
    let a = &mut x;
    let b = a; // move
    *b += 1;
    // println!("{a}");
    // error[E0382]: borrow of moved value: `a`
    assert_eq!(x, 2);
}
```

需要“临时再给别人用一下”时用 reborrow（[Q7](#q7)），不要幻想 `&mut` 能像 `&` 一样随便复制。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	x := 1
	a := &x
	b := a // 复制指针值，两个都能解引用写
	*b = 2
	fmt.Println(*a, x)
}
```

- **Go 怎么做**：指针赋值总是复制地址。
- **Rust 为什么不同**：用“`&mut` 不可 Copy”维持独占不变式。
- **Go 程序员易踩的坑**：对 `&mut` 做赋值后继续用旧名。

**记忆点：**

- `&T: Copy`；`&mut T` 不是。
- 赋 `&mut` = move；临时共享用 reborrow。
- 与 [11-ownership](../11-ownership/#q3) 的 Copy 规则一致。

---

## Q11. 共享借用和可变借用谁更“强”？ {#q11}
**Tags:** `common` `intermediate` `reborrow`
**适用版本:** 全版本

**一句话答案：**

可变借用更“强”：可从 `&mut T` 再借出 `&T`（降级）；反过来不能从 `&T` 变出 `&mut T`。共享借用存活时，原 `&mut` 不能写入。

**解答：**

降级再借用：

```rust
fn main() {
    let mut x = 1;
    let m = &mut x;
    let s: &i32 = &*m; // 或 let s: &i32 = m;
    println!("{s}");
    *m += 1; // NLL：s 用完后恢复写入
    assert_eq!(x, 2);
}
```

共享还活着时不能写：

```rust
fn main() {
    let mut x = 1;
    let m = &mut x;
    let s: &i32 = m;
    // let _w = &mut x;
    // error[E0502]: cannot borrow `x` as mutable because it is also borrowed as immutable
    println!("{s}");
}
```

“强”不等于“随时可写”——独占期间你可以降级只读，但只读结束前不能再通过可变路径写入。

**Go 对比：**

- **Go 怎么做**：`*T` 没有共享/可变两套类型；写不写靠约定。
- **Rust 为什么不同**：用类型区分权限，并可单向降级。
- **Go 程序员易踩的坑**：以为有了 `&mut` 就随时能写，忽略中间临时的 `&`。

**记忆点：**

- `&mut` → `&` 可以；`&` → `&mut` 不行。
- 降级共享存活 ⇒ 外层写入暂停。
- 权限可以收窄，不能凭空放大。

---

## Q12. 什么是悬垂引用，Rust 怎么阻止它？ {#q12}
**Tags:** `common` `beginner` `lifetime` `dangling`
**适用版本:** 全版本

**一句话答案：**

**悬垂引用**（dangling reference）指向已释放的内存；Rust 用生命周期检查禁止返回局部变量的引用等操作（常见 `error[E0515]`）。

**解答：**

返回局部 `String` 的引用会在函数返回后失效：

```rust
fn bad<'a>() -> &'a str {
    let s = String::from("x");
    &s
    // error[E0515]: cannot return reference to local variable `s`
}

fn main() {
    let _ = bad();
}
```

三种合法方向：

```rust
fn owned() -> String {
    String::from("x")
}

fn stat() -> &'static str {
    "literal"
}

fn derived(s: &str) -> &str {
    s.trim()
}

fn main() {
    println!("{}", owned());
    println!("{}", stat());
    let text = String::from("  hi  ");
    println!("{}", derived(&text));
}
```

返回引用必须来自输入参数或 `'static` 数据，详见 [27-lifetimes](../27-lifetimes/#q1)。

**Go 对比：**

```go
package main

import "fmt"

func bad() *int {
	x := 1
	return &x // Go 允许；编译器把 x 逃逸到堆，靠 GC
}

func main() {
	fmt.Println(*bad())
}
```

- **Go 怎么做**：逃逸分析 + GC，返回局部地址往往合法。
- **Rust 为什么不同**：没有 GC 兜底，必须证明引用不超过所有者。
- **Go 程序员易踩的坑**：把 Go 的“返回 &局部”习惯搬到 Rust。

**记忆点：**

- 悬垂 = 指向已死数据。
- `E0515` = 想返回局部引用。
- 返回：拥有值 / `'static` / 来自参数的借用。

---

## Q13. 为什么结构体里放引用会突然需要生命周期？ {#q13}
**Tags:** `common` `intermediate` `lifetime` `struct`
**适用版本:** 全版本

**一句话答案：**

结构体字段若是引用，类型必须声明「这个引用能活多久」，否则编译器无法在使用处检查它是否短于所有者——于是出现 `<'a>`。

**解答：**

不含引用的结构体不需要生命周期参数；一旦字段是借用，就要标注：

```rust
struct Excerpt<'a> {
    part: &'a str,
}

fn main() {
    let novel = String::from("Call me Ishmael.");
    let first = novel.split('.').next().unwrap();
    let e = Excerpt { part: first };
    println!("{}", e.part);
    // Excerpt 不能比 novel 活得更久
}
```

缺少标注时，定义阶段就会被拒绝：

```rust
// 签名示意，非完整程序
// struct Excerpt {
//     part: &str,
// }
// error[E0106]: missing lifetime specifier
```

更完整的省略规则与多生命周期见 [27-lifetimes](../27-lifetimes/#q1)。初学建议：能存 `String` 就别存 `&str`，少很多标注。

```rust
struct OwnedExcerpt {
    part: String, // 拥有数据，无需 'a
}

fn main() {
    let e = OwnedExcerpt {
        part: String::from("Call me Ishmael."),
    };
    println!("{}", e.part);
}
```

**Go 对比：**

```go
package main

import "fmt"

type Excerpt struct {
	Part string // Go 的 string 头可复制；底层由 GC 管理
}

func main() {
	e := Excerpt{Part: "Call me Ishmael."}
	fmt.Println(e.Part)
}
```

- **Go 怎么做**：结构体里放 `string`/指针很常见，存活靠 GC。
- **Rust 为什么不同**：引用字段把“别活得比所有者久”写进类型。
- **Go 程序员易踩的坑**：一在结构体里放 `&str` 就被生命周期吓到——可先改存 `String`。

**记忆点：**

- 字段是引用 ⇒ 结构体要 `<'a>`。
- `Excerpt` 不能超过其借用的数据。
- 能拥有就拥有，生命周期标注可推迟到 [27-lifetimes](../27-lifetimes/#q1)。

---

## Q14. `split_at_mut` 为什么是标准解？ {#q14}
**Tags:** `common` `intermediate` `slice`
**适用版本:** Rust 1.0+；`get_disjoint_mut` 需 1.86+

**一句话答案：**

借用检查器不能证明「两个下标不重叠」，但标准库用 unsafe 在实现里证明后，对外提供安全的 `split_at_mut`——这是同时拿两段 `&mut` 的标准做法。

**解答：**

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let (left, right) = v.split_at_mut(2);
    left[0] = 10;
    right[0] = 30;
    assert_eq!(v, [10, 2, 30, 4]);
}
```

对比手写双重索引可变借用会 `E0499`（见 [Q2](#q2)）。多个任意下标可用 `get_disjoint_mut`：

```rust
fn main() {
    let mut v = vec![10, 20, 30, 40];
    let Ok([a, c]) = v.get_disjoint_mut([0, 2]) else {
        panic!("overlapping or OOB");
    };
    *a += 1;
    *c += 1;
    assert_eq!(v, [11, 20, 31, 40]);
}
```

同类还有 `split_first_mut`、`split_last_mut` 等。优先这些 API，而不是自己写 `*mut`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3, 4}
	left, right := v[:2], v[2:] // 共享底层；两边都能写
	left[0] = 10
	right[0] = 30
	fmt.Println(v)
}
```

- **Go 怎么做**：子切片天然共享底层数组，可同时写不同区间（重叠时也危险）。
- **Rust 为什么不同**：默认禁止双重 `&mut`；`split_at_mut` 把“不重叠”证明封装进标准库。
- **Go 程序员易踩的坑**：想当然 `&mut v[i]` 两次——请改用拆分 API。

**记忆点：**

- 同时两段可变切片 → `split_at_mut`。
- 任意不重叠下标 → `get_disjoint_mut`（1.86+）。
- 不要为这点小事自己写 unsafe。

---

## Q15. `Cell` / `RefCell` 什么时候能绕开编译期借用限制？ {#q15}
**Tags:** `common` `intermediate` `interior-mutability`
**适用版本:** 全版本；仅单线程。跨线程用 `Mutex` / `RwLock`

**一句话答案：**

需要「外面是共享借用，里面还能改」时用**内部可变性**（interior mutability）：`Cell` 做整值替换；`RefCell` 把借用检查推迟到运行时（违规 panic，不是编译错误）。

**解答：**

```rust
use std::cell::{Cell, RefCell};

fn main() {
    // Cell：不借出 &T/&mut T，只 get/set，因此无“借用冲突”，永不因借用 panic
    let c = Cell::new(1);
    c.set(c.get() + 1);
    assert_eq!(c.get(), 2);

    // RefCell：可借出 & / &mut，规则改到运行时
    let x = RefCell::new(1);
    *x.borrow_mut() += 1;
    assert_eq!(*x.borrow(), 2);
}
```

`RefCell` 在共享引用背后修改——适合「结构体方法是 `&self`，但要改内部缓存」等场景；同时两个 `borrow_mut` 会 **panic**：

```rust
use std::cell::RefCell;

fn main() {
    let x = RefCell::new(1);
    let mut a = x.borrow_mut();
    // let mut b = x.borrow_mut(); // 运行时 panic：already borrowed
    *a += 1;
    drop(a);
    assert_eq!(*x.borrow(), 2);
}
```

不要把 `RefCell` 当第一选择：能改成 `&mut self`、拆作用域、换 API，就别上运行时检查。

**Go 对比：**

- **Go 怎么做**：结构体指针方法里改字段很随意；没有编译期借用位。
- **Rust 为什么不同**：默认 `&self` 不能改字段；内部可变性是显式退出“编译期借用”。
- **Go 程序员易踩的坑**：到处 `RefCell` 把 panic 留到运行时——先问能否 `&mut self`。

**记忆点：**

- `Cell`：Copy/替换；`RefCell`：运行时 `&`/`&mut`。
- 单线程；多线程 →锁。
- 能编译期解决就别用内部可变。

---

## Q16. 方法接收者 `&self` / `&mut self` 怎么选？ {#q16}
**Tags:** `occasional` `beginner` `methods`
**适用版本:** 全版本

**一句话答案：**

只读用 `&self`；要改字段用 `&mut self`；要吃掉并拆开用 `self`。调用 `&mut self` 时，接收者变量需是 `mut`。

**解答：**

```rust
struct Counter(u32);

impl Counter {
    fn value(&self) -> u32 {
        self.0
    }
    fn inc(&mut self) {
        self.0 += 1;
    }
    fn into_inner(self) -> u32 {
        self.0
    }
}

fn main() {
    let mut c = Counter(0);
    c.inc(); // 需要 c: mut
    println!("{}", c.value());
    let n = c.into_inner(); // 消费所有权
    // c.value();
    // error[E0382]: borrow of moved value: `c`
    println!("{n}");
}
```

若 `c` 未声明 `mut`，调用 `inc` 会报：

```rust
struct Counter(u32);
impl Counter {
    fn inc(&mut self) {
        self.0 += 1;
    }
}

fn main() {
    let c = Counter(0);
    // c.inc();
    // error[E0596]: cannot borrow `c` as mutable, as it is not declared as mutable
    let _ = c;
}
```

命名惯例：`into_xxx` 消费 `self`，`as_xxx` 借用，`to_xxx` 常复制出新值。

**Go 对比：**

```go
package main

import "fmt"

type Counter struct{ n uint }

func (c Counter) Value() uint  { return c.n }      // 值接收者
func (c *Counter) Inc()        { c.n++ }           // 指针接收者
func (c Counter) IntoInner() uint { return c.n }

func main() {
	c := Counter{}
	c.Inc()
	fmt.Println(c.Value())
}
```

- **Go 怎么做**：值 / 指针接收者；调用方常自动取址。
- **Rust 为什么不同**：`&mut self` 要求绑定可变，且消费 `self` 后不能再用。
- **Go 程序员易踩的坑**：忘了 `let mut`，或 `into_` 之后还当借用用。

**记忆点：**

- 读 `&self`；改 `&mut self`；移交 `self`。
- `&mut self` ⇒ 变量要 `mut`。
- `into_` 吃掉自己。

---

## Q17. 为什么 `for x in &v` 里不能 `push`？ {#q17}
**Tags:** `occasional` `beginner` `iterator`
**适用版本:** 全版本

**一句话答案：**

`for x in &v` 在整个循环期间持有对 `v` 的共享借用；`push` 需要 `&mut v` 且可能重分配——故 `E0502`，防的是迭代器内部指针悬垂。

**解答：**

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for x in &v {
        v.push(*x);
        // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    }
}
```

常见修法：

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    // 1) 就地改：retain / iter_mut
    v.retain(|&x| x != 2);
    for x in v.iter_mut() {
        *x *= 10;
    }

    // 2) 先收集再改
    let doubled: Vec<i32> = v.iter().map(|&x| x * 2).collect();
    v.extend(doubled);

    // 3) 用索引（len 预先固定）
    let n = v.len();
    for i in 0..n {
        v[i] += 1;
    }
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	for _, x := range v {
		v = append(v, x) // 合法但危险：range 用的是开始时的快照/底层
	}
	fmt.Println(v)
}
```

- **Go 怎么做**：`range` 中 `append` 常能编译，语义却容易让人困惑。
- **Rust 为什么不同**：直接禁止边迭代边扩容同一 `Vec`。
- **Go 程序员易踩的坑**：把 Go 里“能跑”的写法搬过来。

**记忆点：**

- `&v` 的 for = 整段循环都在借用。
- 先收集 / `iter_mut` / 索引，别边借边 `push`。
- 与 [Q9](#q9) 同一根因。

---

## Q18. `'static` 引用和 `T: 'static` 有什么区别？ {#q18}
**Tags:** `occasional` `intermediate` `static`
**适用版本:** 全版本

**一句话答案：**

`&'static T` 是「这个**引用**能活到程序结束」；`T: 'static` 是「这个**类型**不含短生命周期借用」（拥有数据的 `String`、`i32`、`Vec<u8>` 都满足）。

**解答：**

`&'static T`：引用本身必须指向永不失效的数据（字面量、`static` 项、`Box::leak` 等）：

```rust
fn need_static(s: &'static str) {
    println!("{s}");
}

fn main() {
    need_static("literal");
    let s = String::from("x");
    // need_static(&s);
    // error[E0597]: `s` does not live long enough
}
```

`T: 'static`：约束的是值里有没有“短借”。`String` 拥有堆数据，满足 `T: 'static`，但它不是 `&'static String`：

```rust
fn take_static_type<T: 'static>(_: T) {}

fn main() {
    take_static_type(String::from("owned")); // OK：拥有数据
    take_static_type(42_i32);
    let local = String::from("x");
    // take_static_type(&local);
    // error[E0597]: `local` does not live long enough
    // —— 这里 T = &String，借用绑在 local 上，不满足 'static
}
```

线程 `spawn` 要求闭包 `T: 'static`，因此传拥有的 `String` 可以，传借用 `&s` 通常不行——要的是“别把短命借用带进别的线程”，不是要求参数必须是 `&'static`。

**Go 对比：**

- **Go 怎么做**：没有 `'static` 约束；逃逸与 GC 处理跨 goroutine 的指针存活。
- **Rust 为什么不同**：用 `T: 'static` 在类型层禁止短借出逃。
- **Go 程序员易踩的坑**：看见 `'static` 就以为必须用全局/字面量；`String` 往往就够。

**记忆点：**

- `&'static T` = 引用活到进程结束。
- `T: 'static` = 类型内无短生命周期借用（拥有值通常 OK）。
- `String: 'static`，但 `&String` 一般不是 `&'static String`。

---

## Q19. 借用报错时最先该改哪一行？ {#q19}
**Tags:** `advanced` `diagnostics`
**适用版本:** 1.97.1

**一句话答案：**

先看编译器标的**第一条冲突借用**和 note 里的“first borrowed here / mutable borrow later”，优先结束较早的那次借用，而不是盲目 `clone` 报错行。

**解答：**

典型 `E0502` 诊断会指出两处：先发生的共享借用，和后来的可变借用。先改“让第一次借用更早结束”的那一行（缩短使用、提前拷贝、调整顺序）：

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([("k", 1)]);
    let v = map.get("k").copied(); // 优先改这里：别让 &i32 活过 insert
    map.insert("k2", 2);
    println!("{v:?}");
}
```

对照错误形态选策略：

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    // E0499：两个 &mut —— 改成顺序用或 split_at_mut
    {
        let a = &mut v[0];
        *a += 1;
    }
    let b = &mut v[1];
    *b += 1;

    // E0502：& 与 &mut —— 先结束读
    let n = v.len();
    v.push(n);

    // E0515：返回局部引用 —— 改返回类型为拥有值（见 [Q12](#q12)）
    println!("{v:?}");
}
```

操作顺序建议：① 看清两处借用 ② 缩短第一次借用 / 换序 ③ 换 API（`entry`、`split_at_mut`）④ 最后才 `clone` / `RefCell`。

**Go 对比：**

- **Go 怎么做**：没有这类编译期冲突诊断；问题常拖到运行时。
- **Rust 为什么不同**：错误信息里已经标出“谁先借、谁后改”。
- **Go 程序员易踩的坑**：只改最后一行 `insert`/`push`，却不结束前面的 `get`/迭代借用。

**记忆点：**

- 先读 note 里的两处借用点。
- 优先结束较早的借用。
- `clone` 是权宜，不是第一步。

---

## Q20. 这一章最实用的判断流程是什么？ {#q20}
**Tags:** `advanced` `summary` `borrowing`
**适用版本:** 1.97.1

**一句话答案：**

只读 → `&` / `&str`；要改 → 唯一 `&mut`；冲突时按「缩作用域 → 换 API → 拷贝值 → 内部可变」升级，不要一上来 `clone` 或 `RefCell`。

**解答：**

日常决策树：

```rust
fn read(s: &str) {
    println!("{s}");
}

fn bump(v: &mut Vec<i32>) {
    v.push(1);
}

fn main() {
    let mut v = vec![1, 2];
    read("hi"); // 1) 能只读就 & / &str
    bump(&mut v); // 2) 要改就单一 &mut
    let n = v.len(); // 3) 冲突：先结束借用
    v.push(n as i32);
}
```

拆冲突清单（与旧章实战清单一致）：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];

    // 缩作用域 / 顺序使用（NLL）
    {
        let x = &v[0];
        println!("{x}");
    }
    v.push(5);

    // 分区可变
    let (a, b) = v.split_at_mut(2);
    a[0] += 1;
    b[0] += 1;

    // 先读出拥有/Copy 值再改
    let first = v.first().copied();
    v.push(first.unwrap_or(0));
    println!("{v:?}");
}
```

错误码速记：`E0499` 双重 mut；`E0502` mut 与共享冲突；`E0515` 返回局部引用；`E0597` 活得不够久。

**Go 对比：**

- **Go 怎么做**：传指针 + 约定；没有这套编译期流程。
- **Rust 为什么不同**：流程的每一步都在维持“别名与存活”不变式。
- **Go 程序员易踩的坑**：把每个借用错误都当成新语言特性，而不是同一棵决策树。

**记忆点：**

- 能借只读就别可变；能一个 `&mut` 就别两个。
- 冲突：缩域 → API → 拷贝 → `Cell`/`RefCell`。
- 背错误码，对上 [Q19](#q19) 的改法。

---

## Q21. 报错 `temporary value dropped while borrowed` 是什么意思？ {#q21}
**Tags:** `hot` `borrowing` `temporary` `E0716`
**适用版本:** Rust 1.0+

**一句话答案：**

你把引用绑到了**临时值**上，而临时值在当前语句结束就会 drop；引用却还想活到后面——于是 `error[E0716]`。修法：先用 `let` 把拥有值存住，再借。

**解答：**

经典踩法：把临时 `String` 上的借用塞进要活得更久的容器：

```rust
fn main() {
    let mut v: Vec<&str> = Vec::new();
    // v.push(String::from("hi").as_str());
    // error[E0716]: temporary value dropped while borrowed
    //   creates a temporary value which is freed while still in use
    let owned = String::from("hi");
    v.push(owned.as_str());
    println!("{:?}", v);
}
```

方法链里也会中招：临时值只活到语句末尾，中间产生的借用不能“逃”到下一句去喂给长期容器：

```rust
fn main() {
    let mut parts: Vec<&str> = Vec::new();
    // parts.push(String::from("  rust  ").trim());
    // error[E0716]: temporary value dropped while borrowed
    let owned = String::from("  rust  ");
    parts.push(owned.trim());
    assert_eq!(parts[0], "rust");
}
```

需要拥有修剪后的文本时，转成 `String`，让所有权离开临时上下文：

```rust
fn main() {
    let cleaned = String::from("  rust  ").trim().to_string();
    println!("{cleaned}");
}
```

本质：借用必须挂在某个**活得够久的所有者**上；表达式中间的临时值不是合格的长期房东。

**Go 对比：**

```go
package main

import (
	"fmt"
	"strings"
)

func main() {
	r := strings.TrimSpace("  rust  ")
	fmt.Println(r) // string 值拷贝头；底层数据由 GC 管
}
```

- **Go 怎么做**：返回的 `string` 自带可用的数据视图，GC 保证安全。
- **Rust 为什么不同**：`&str` 不拥有缓冲，临时 `String` 一 drop，引用就悬垂。
- **Go 程序员易踩的坑**：链式 `String::from(...).as_str()` 当普通表达式随便存。

**记忆点：**

- `E0716` = 临时值死得太早。
- 先 `let owned = ...;` 再 `&owned` / `.as_str()`。
- 要带走文本 → `.to_string()` / `String::from`，别只留引用。

---

## Q22. 为什么“先索引借出来，再 `push`”编译不过？ {#q22}
**Tags:** `common` `borrowing` `Vec` `push` `E0502`
**适用版本:** Rust 1.0+

**一句话答案：**

`&v[i]` 在元素引用存活期间持有对整个 `Vec` 的共享借用；`push` 需要 `&mut Vec` 且可能重分配——二者冲突，报 `E0502`。先结束借用（拷贝/克隆出值，或缩作用域），再改容器。

**解答：**

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    let x = &v[0];
    // v.push(4);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{x}");
    v.push(4); // x 已不再使用，NLL 下这里 OK
}
```

若后面还要用索引借出的引用，必须先把值拿出来（`Copy` 直接拷，非 `Copy` 用 `clone`）：

```rust
fn main() {
    let mut v = vec![String::from("a"), String::from("b")];
    let first = v[0].clone(); // 结束对 v 的借用
    v.push(String::from("c"));
    println!("{first} {v:?}");
}
```

只读长度再 push 可以，因为临时借用立刻结束（对照 [Q9](#q9)、[Q3](#q3)）：

```rust
fn main() {
    let mut v = vec![10, 20];
    let n = v.len(); // 临时借用结束
    v.push(n);
    assert_eq!(v, vec![10, 20, 2]);
}
```

根因不是“下标语法特殊”，而是：**活着的元素引用 ≈ 禁止容器再搬家**；`push` 可能搬家。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	x := &v[0]
	v = append(v, 4) // 可能换底层数组；x 可能悬空——Go 编译器不拦
	fmt.Println(*x, v)
}
```

- **Go 怎么做**：允许，但扩容后旧指针可能失效，靠你小心。
- **Rust 为什么不同**：同一类 bug 在编译期直接拒绝。
- **Go 程序员易踩的坑**：觉得“我只是读了 `v[0]`”，不理解借用还绑着整容器。

**记忆点：**

- 持有 `&v[i]` 时别 `push`/`insert`。
- 先 `copied`/`cloned`/缩作用域，再改。
- 防的是扩容后悬垂引用。

---
