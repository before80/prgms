+++
title = "19-常见集合"
date = 2026-07-28T14:49:00+08:00
weight = 190
type = "docs"
description = "围绕 `Vec`、`HashMap`、`HashSet` 与 `collect()`，讲清 Rust 常见集合与 Go 直觉差异"
isCJKLanguage = true
draft = false

+++

# 常见集合 (Collections)

> 面向 **Rust 1.97.1** (stable, 2026-07)。本篇假设你熟悉 Go，凡有可比性处均给出 🐹 Go 对比。
>
> 热度: `hot` 高频 | `common` 常见 | `occasional` 偶尔 | `advanced` 进阶少见

**本篇能解决什么：**

- 你会不会在 `HashMap::get` 后立刻 `insert` 撞上 `E0502`？
- 你是否分不清 `iter` / `iter_mut` / `into_iter`、以及 `entry` / `collect` / `drain`？
- 你会不会把 Go 的 slice/map 扩容与并发直觉直接带进 Rust？
- 你是否想知道：`Vec`/`HashMap`/`BTreeMap`/`VecDeque`/`LinkedList`/`BinaryHeap` 各自什么时候该选？

**术语速查表：**

| 术语 / 缩略词 | 全称 / 读法 | 中文 | 一句话解释 | Go 里的近亲 |
|---|---|---|---|---|
| `Vec<T>` | vector | 动态数组 | 连续可增长数组 | `[]T` / slice |
| `HashMap<K,V>` | — | 哈希表 | 无序键值映射 | `map[K]V` |
| `HashSet<T>` | — | 哈希集合 | 无序去重集合 | `map[T]struct{}` |
| `BTreeMap` | — | B 树映射 | 有序键值映射 | 无标准库直接对应 |
| `VecDeque` | double-ended queue | 双端队列 | 两端高效进出 | 常用切片/容器模拟 |
| `BinaryHeap` | — | 二叉堆 | 优先队列；默认最大堆 | `container/heap` |
| capacity | — | 容量 | 已分配能装多少，未必等于长度 | `cap` |
| `entry` API | — | 入口 API | 一次查找完成“有则改/无则插” | 先查再写 |
| `collect` | — | 收集 | 把迭代器收成集合 | 手写 append |
| rehash | — | 重哈希 | 哈希表扩容后重新放置元素 | map 增长 |
| amortized | — | 摊销 | 单次偶发贵、平均仍便宜 | `append` 摊销 |
| `GC` | Garbage Collector | 垃圾回收器 | 运行时回收 | Go 默认机制 |

> 说明：本表覆盖本篇出现的所有专业名词与缩略词；正文首次出现时仍会就地解释一次。

**热度索引：**

| 热度 | 题目 |
|------|------|
| `hot` | [Q1](#q1), [Q2](#q2), [Q3](#q3), [Q4](#q4), [Q5](#q5), [Q21](#q21), [Q23](#q23), [Q24](#q24), [Q25](#q25) |
| `common` | [Q6](#q6), [Q7](#q7), [Q8](#q8), [Q9](#q9), [Q10](#q10), [Q11](#q11), [Q12](#q12), [Q13](#q13), [Q14](#q14), [Q15](#q15), [Q22](#q22) |
| `occasional` | [Q16](#q16), [Q17](#q17), [Q18](#q18) |
| `advanced` | [Q19](#q19), [Q20](#q20) |

---

## Q1. `Vec<T>` 为什么是默认集合？ {#q1}
**Tags:** `hot` `beginner` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

连续内存、缓存友好、API 全面，绝大多数“一列同质元素”的场景 `Vec` 都是第一选择。

**解答：**

对应 Go 的切片后端数组。`Vec` 拥有堆缓冲；`len` 是元素数，`capacity` 是已分配槽位。常用 `vec![]`、`push`、`pop`、索引、`iter`。

```rust
fn main() {
    let mut v = Vec::new();
    v.push(1);
    v.push(2);
    println!("len={} cap={} {:?}", v.len(), v.capacity(), v);
}
```

```rust
fn main() {
    let v = vec![10, 20, 30];
    println!("{} {}", v[0], v.len());
}
```

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    assert_eq!(v.pop(), Some(3));
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2}
	v = append(v, 3)
	fmt.Println(len(v), cap(v), v)
}
```

- **Go 怎么做**：切片 + `append`。
- **Rust 为什么不同**：`Vec` 是明确的拥有型类型，和切片 `&[T]` 分开。
- **Go 程序员易踩的坑**：把 `Vec` 和 `&[T]` 混为一谈。

---

## Q2. `HashMap` 的 key/value 所有权是谁的？ {#q2}
**Tags:** `hot` `beginner` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`insert` 之后，map 拥有键和值；`get` 只借给你 `&V`，不会交出所有权。

**解答：**

`use std::collections::HashMap;`。键常要 `String`（拥有）以便 map 长期持有；查找可用 `&str`，因为 `String` 实现了 `Borrow<str>`。想取出拥有值用 `remove`。

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    map.insert(String::from("a"), 1);
    println!("{:?}", map.get("a"));
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    let k = String::from("a");
    map.insert(k, 1);
    // println!("{k}");
    // error[E0382]: borrow of moved value: `k`
    println!("{:?}", map.get("a"));
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    let v = map.remove("a");
    println!("{v:?} {}", map.len());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{"a": 1}
	fmt.Println(m["a"])
}
```

- **Go 怎么做**：map 存键值；取出来的是值拷贝（对内建类型）。
- **Rust 为什么不同**：`get` 返回引用，所有权仍在 map。
- **Go 程序员易踩的坑**：以为 `get` 拿到了拥有值，或 insert 后还用原来的 `String` 键。

---

## Q3. 为什么从 `HashMap::get` 拿到引用后不能立刻 `insert`？ {#q3}
**Tags:** `hot` `beginner` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`get` 返回的 `&V` 借用了整个 map；`insert` 可能扩容/**rehash**（重哈希），需要 `&mut self`，与未结束的不可变借冲突，报 `E0502`。

**解答：**

修法：

1. 先结束借用：把需要的值 `copied()`/`cloned()`/`to_owned()` 出来再改 map；
2. 或用 `entry` API 一次完成“查+插”（见 [Q4](#q4)）；
3. 或缩小作用域，让引用在 `insert` 前结束。

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    let cur = map.get("a").copied();
    map.insert(String::from("b"), 2);
    println!("{:?} {:?}", cur, map.get("b"));
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    let v = map.get("a");
    map.insert(String::from("b"), 2);
    // error[E0502]: cannot borrow `map` as mutable because it is also borrowed as immutable
    println!("{:?}", v);
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([(String::from("a"), 1)]);
    {
        let v = map.get("a");
        println!("{v:?}");
    } // 借用在此结束
    map.insert(String::from("b"), 2);
    println!("{}", map.len());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{"a": 1}
	v := m["a"]
	m["b"] = 2
	fmt.Println(v, m["b"])
}
```

- **Go 怎么做**：读出的 `int` 是拷贝，随后写 map 无妨。
- **Rust 为什么不同**：引用期间禁止可能使引用失效的可变操作。
- **Go 程序员易踩的坑**：`let v = map.get(...); map.insert(...); println!("{v:?}")`。

---

## Q4. `entry()` API 为什么这么常用？ {#q4}
**Tags:** `hot` `beginner` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

一次哈希查找完成“有则改、无则插”，避免 get/insert 两趟查找，也常避开借用冲突。

**解答：**

`map.entry(key).or_insert(default)` 返回 `&mut V`。计数、分组、缓存初始化极常用。键会按 entry 需要 move 进 map（已存在则键可能丢弃，注意 `String` 键的开销，可用 `entry` 前先考虑借用型查找策略）。

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::new();
    for w in ["go", "rust", "go"] {
        *map.entry(w).or_insert(0) += 1;
    }
    println!("{}", map["go"]);
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<String, Vec<i32>> = HashMap::new();
    map.entry(String::from("a")).or_default().push(1);
    map.entry(String::from("a")).or_default().push(2);
    println!("{:?}", map["a"]);
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut map = HashMap::from([("x", 1)]);
    map.entry("x").and_modify(|v| *v += 10).or_insert(0);
    println!("{}", map["x"]);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{}
	for _, w := range []string{"go", "rust", "go"} {
		m[w]++
	}
	fmt.Println(m["go"])
}
```

- **Go 怎么做**：直接 `m[w]++`（零值可读可写）。
- **Rust 为什么不同**：没有“读零值自动可写”的 map 语义，用 `entry` 表达意图。
- **Go 程序员易踩的坑**：先 `get` 再 `insert` 写两遍逻辑还借着用。

---

## Q5. `collect()` 到底是怎么把迭代器收成集合的？ {#q5}
**Tags:** `hot` `beginner` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`collect` 消费迭代器，按目标类型（实现了 `FromIterator`）组装成 `Vec`/`HashMap`/`String` 等；常需标注目标类型。

**解答：**

写法：`let v: Vec<_> = iter.collect();` 或 `iter.collect::<Vec<_>>()`（turbofish）。元素类型要匹配；收集 `(K,V)` 可得 `HashMap`。

```rust
fn main() {
    let v: Vec<i32> = (1..=3).map(|x| x * 2).collect();
    println!("{v:?}");
}
```

```rust
use std::collections::HashMap;

fn main() {
    let m: HashMap<_, _> = [("a", 1), ("b", 2)].into_iter().collect();
    println!("{}", m["a"]);
}
```

```rust
fn main() {
    let s: String = ['r', 'u', 's', 't'].into_iter().collect();
    println!("{s}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	in := []int{1, 2, 3}
	out := make([]int, 0, len(in))
	for _, x := range in {
		out = append(out, x*2)
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：手写循环 `append`。
- **Rust 为什么不同**：迭代器适配器 + `collect` 声明目标容器。
- **Go 程序员易踩的坑**：不标类型，看 `E0282` 不知道要写成 `Vec<_>`。

---

## Q6. `iter` / `iter_mut` / `into_iter` 对集合分别意味着什么？ {#q6}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`iter` 借不可变元素；`iter_mut` 借可变元素；`into_iter` 拿走集合所有权并产出拥有元素。

**解答：**

对 `Vec<T>`：`iter()` → `&T`；`iter_mut()` → `&mut T`；`into_iter()` → `T`，之后原 `Vec` 不能再用。`for x in &v` 约等于 `iter`；`for x in v` 约等于 `into_iter`。

```rust
fn main() {
    let v = vec![1, 2, 3];
    for x in v.iter() {
        println!("{x}");
    }
    println!("{}", v.len());
}
```

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for x in v.iter_mut() {
        *x *= 2;
    }
    println!("{v:?}");
}
```

```rust
fn main() {
    let v = vec![1, 2, 3];
    let sum: i32 = v.into_iter().sum();
    println!("{sum}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	for _, x := range v {
		fmt.Println(x)
	}
	fmt.Println(len(v))
}
```

- **Go 怎么做**：`range` 默认拷贝元素值（对 int）。
- **Rust 为什么不同**：三种迭代显式区分借用/消费。
- **Go 程序员易踩的坑**：`for x in v` 把 `Vec` 吃掉还想再用。

---

## Q7. 为什么迭代集合时不能顺手修改结构？ {#q7}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

迭代持有对集合的借用；同时 `push`/`insert`/`remove` 要可变借用并可能搬家，编译器拒绝。

**解答：**

先收集要删/要加的键或索引，迭代结束后再改；或用 `retain`/`extract_if`（按版本）等专门 API。Go 里改 map 虽“能跑”也有坑；Rust 直接禁止大多数危险重叠。

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    v.retain(|x| *x % 2 == 0);
    println!("{v:?}");
}
```

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    for x in &v {
        v.push(*x);
        // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
        println!("{x}");
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3, 4}
	out := v[:0]
	for _, x := range v {
		if x%2 == 0 {
			out = append(out, x)
		}
	}
	fmt.Println(out)
}
```

- **Go 怎么做**：常新建切片或小心原地过滤。
- **Rust 为什么不同**：借用规则禁止“边遍历边扩容”。
- **Go 程序员易踩的坑**：在 `for x in &v` 里 `v.push`。

---

## Q8. `Vec` 的 `push` 为什么是摊销 O(1)？ {#q8}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

多数 `push` 只写入已有 capacity；偶发扩容会分配更大缓冲并搬迁，平均下来仍是 **amortized**（摊销）O(1)。

**解答：**

与 Go `append` 类似。扩容后旧引用/指针失效——Rust 用借用检查在编译期拦住“拿着元素引用还 push”。

```rust
fn main() {
    let mut v = Vec::with_capacity(2);
    v.push(1);
    v.push(2);
    println!("len={} cap={}", v.len(), v.capacity());
    v.push(3); // 可能触发扩容
    println!("len={} cap={}", v.len(), v.capacity());
}
```

```rust
fn main() {
    let mut v = vec![1];
    let first = &v[0];
    v.push(2);
    // error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
    println!("{first}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]int, 0, 2)
	v = append(v, 1, 2, 3)
	fmt.Println(len(v), cap(v))
}
```

- **Go 怎么做**：`append` 摊销增长，程序员自己小心悬空指针。
- **Rust 为什么不同**：扩容与借用冲突由编译器检查。
- **Go 程序员易踩的坑**：持有 `&v[0]` 时继续 `push`。

---

## Q9. 什么时候该预分配 capacity？ {#q9}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

大致知道最终长度时用 `Vec::with_capacity(n)` / `HashMap::with_capacity(n)`，减少反复扩容与搬迁。

**解答：**

写在创建容器处：`let mut v = Vec::with_capacity(items.len());`。不知道大小就别猜一个过大数字。`collect` 有时能利用 size hint 预留。

```rust
fn main() {
    let n = 100;
    let mut v = Vec::with_capacity(n);
    for i in 0..n {
        v.push(i);
    }
    println!("{} {}", v.len(), v.capacity());
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut m = HashMap::with_capacity(8);
    m.insert("a", 1);
    println!("{}", m.capacity() >= 1);
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := make([]int, 0, 100)
	for i := 0; i < 100; i++ {
		v = append(v, i)
	}
	fmt.Println(len(v), cap(v))
}
```

- **Go 怎么做**：`make([]T, 0, n)`。
- **Rust 为什么不同**：同样是预留，只是 API 名不同。
- **Go 程序员易踩的坑**：`Vec::with_capacity` 后以为 `len` 已经是 n。

---

## Q10. `HashSet` 和 `HashMap<K, ()>` 有什么关系？ {#q10}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`HashSet<T>` 本质上就是只关心键、值类型为单元值 `()` 的集合抽象；用来去重和成员测试。

**解答：**

`use std::collections::HashSet;`。`insert` 返回是否为新元素；`contains` 判断成员。实现上可理解为 `HashMap<T, ()>` 的封装。

```rust
use std::collections::HashSet;

fn main() {
    let mut s = HashSet::new();
    assert!(s.insert("a"));
    assert!(!s.insert("a"));
    println!("{}", s.contains("a"));
}
```

```rust
use std::collections::HashSet;

fn main() {
    let a: HashSet<_> = [1, 2, 3].into_iter().collect();
    let b: HashSet<_> = [3, 4].into_iter().collect();
    println!("{:?}", a.intersection(&b).collect::<Vec<_>>());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	s := map[string]struct{}{}
	s["a"] = struct{}{}
	_, ok := s["a"]
	fmt.Println(ok)
}
```

- **Go 怎么做**：`map[T]struct{}` 模拟集合。
- **Rust 为什么不同**：标准库直接给 `HashSet`。
- **Go 程序员易踩的坑**：还手写 `HashMap<K, ()>` 却不用集合 API。

---

## Q11. 为什么 `BTreeMap` 有时比 `HashMap` 更合适？ {#q11}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

需要有序遍历、范围查询、或键没有好哈希但实现了 `Ord` 时，用 `BTreeMap`。

**解答：**

`use std::collections::BTreeMap;`。按键排序迭代；`range` 取区间。一般查找 `HashMap` 平均更快；要顺序选 BTree。

```rust
use std::collections::BTreeMap;

fn main() {
    let mut m = BTreeMap::new();
    m.insert(2, "b");
    m.insert(1, "a");
    for (k, v) in &m {
        println!("{k}:{v}");
    }
}
```

```rust
use std::collections::BTreeMap;

fn main() {
    let mut m = BTreeMap::from([(1, "a"), (2, "b"), (3, "c")]);
    let part: Vec<_> = m.range(2..).map(|(k, v)| (*k, *v)).collect();
    println!("{part:?}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	m := map[int]string{2: "b", 1: "a"}
	ks := make([]int, 0, len(m))
	for k := range m {
		ks = append(ks, k)
	}
	sort.Ints(ks)
	for _, k := range ks {
		fmt.Println(k, m[k])
	}
}
```

- **Go 怎么做**：map 无序，要顺序就取出键排序。
- **Rust 为什么不同**：`BTreeMap` 内建有序。
- **Go 程序员易踩的坑**：以为 `HashMap` 迭代顺序稳定。

---

## Q12. `VecDeque` 适合什么场景？ {#q12}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

需要队列语义、两端都能高效 `push`/`pop` 时用 `VecDeque`；只在尾部操作时 `Vec` 通常更简单。

**解答：**

`use std::collections::VecDeque;`。`push_back`/`pop_front` 做 FIFO。中间任意删除仍可能贵。

```rust
use std::collections::VecDeque;

fn main() {
    let mut q = VecDeque::new();
    q.push_back(1);
    q.push_back(2);
    println!("{:?}", q.pop_front());
    println!("{:?}", q.pop_front());
}
```

```rust
use std::collections::VecDeque;

fn main() {
    let mut q = VecDeque::from(vec![1, 2, 3]);
    q.push_front(0);
    println!("{q:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	q := []int{1, 2}
	q = append(q, 3)
	front := q[0]
	q = q[1:]
	fmt.Println(front, q)
}
```

- **Go 怎么做**：用切片头尾操作模拟队列（注意底层数组泄漏）。
- **Rust 为什么不同**：`VecDeque` 专为双端设计。
- **Go 程序员易踩的坑**：用 `Vec::remove(0)` 当队列导致 O(n)。

---

## Q13. 为什么标准库 `LinkedList` 很少推荐？ {#q13}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

缓存不友好、很多操作并不比 `Vec` 快，还更难用；真需要链表语义时再考虑，默认仍选 `Vec`/`VecDeque`。

**解答：**

文档也偏向“大多数情况用 `Vec`”。Rust 的所有权使某些经典链表写法更别扭。不要因为 Go 里偶尔手写 list 就默认搬 `LinkedList`。

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    v.insert(0, 0); // 对小数据常常够用
    println!("{v:?}");
}
```

```rust
use std::collections::LinkedList;

fn main() {
    let mut list = LinkedList::new();
    list.push_back(1);
    list.push_back(2);
    println!("{:?}", list.pop_front());
}
```

**Go 对比：**

```go
package main

import (
	"container/list"
	"fmt"
)

func main() {
	l := list.New()
	l.PushBack(1)
	fmt.Println(l.Front().Value)
}
```

- **Go 怎么做**：有 `container/list`，也不总是首选。
- **Rust 为什么不同**：更强调连续内存性能。
- **Go 程序员易踩的坑**：中级教程一上来就实现链表当练习，当成默认容器。

---

## Q14. `drain` / `retain` / `remove` 的所有权差别是什么？ {#q14}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`remove`/`pop` 取出拥有元素；`drain` 借走一段并产出拥有元素迭代器；`retain` 原地过滤，被丢掉的元素直接 drop。

**解答：**

`drain` 期间集合被可变借用，迭代器用完才完全释放该借用。`retain` 适合“留下谁”。按键删 map 用 `remove`。

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    let taken: Vec<_> = v.drain(1..3).collect();
    println!("{v:?} {taken:?}");
}
```

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4];
    v.retain(|x| *x % 2 == 0);
    println!("{v:?}");
}
```

```rust
use std::collections::HashMap;

fn main() {
    let mut m = HashMap::from([("a", 1), ("b", 2)]);
    println!("{:?}", m.remove("a"));
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3, 4}
	taken := append([]int{}, v[1:3]...)
	v = append(v[:1], v[3:]...)
	fmt.Println(v, taken)
}
```

- **Go 怎么做**：切片拼装。
- **Rust 为什么不同**：API 明确表达拿走还是丢弃。
- **Go 程序员易踩的坑**：`drain` 还没消费完就再借用原 `Vec`。

---

## Q15. 排序时 `sort` 和 `sort_unstable` 怎么选？ {#q15}
**Tags:** `common` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

不需要稳定性时优先 `sort_unstable`（通常更快）；相等元素要保留原相对顺序时用 `sort`。

**解答：**

都在 `&mut [T]` 上，元素需 `Ord`。自定义比较用 `sort_by` / `sort_unstable_by`。稳定性：相等键的相对次序是否保持。

```rust
fn main() {
    let mut v = vec![3, 1, 4, 1, 5];
    v.sort_unstable();
    println!("{v:?}");
}
```

```rust
fn main() {
    let mut v = vec![(2, "b"), (1, "a"), (2, "c")];
    v.sort_by_key(|p| p.0); // 稳定排序
    println!("{v:?}");
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"sort"
)

func main() {
	v := []int{3, 1, 4, 1, 5}
	sort.Ints(v)
	fmt.Println(v)
}
```

- **Go 怎么做**：`sort` 包；稳定性看具体函数。
- **Rust 为什么不同**：稳定/不稳定 API 名字分开。
- **Go 程序员易踩的坑**：不需要稳定却坚持 `sort`，无谓多耗。

---

## Q16. 为什么 `HashMap` 迭代顺序不能依赖？ {#q16}
**Tags:** `occasional` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

哈希表按桶遍历，顺序未定义，且可能受随机种子影响；要稳定顺序用 `BTreeMap` 或先取出键排序。

**解答：**

这和 Go 从 1 起随机化 map 迭代类似：防止依赖顺序的隐患。测试里不要断言 `HashMap` 的遍历次序。

```rust
use std::collections::{BTreeMap, HashMap};

fn main() {
    let h = HashMap::from([("b", 2), ("a", 1)]);
    let b: BTreeMap<_, _> = h.into_iter().collect();
    let keys: Vec<_> = b.keys().copied().collect();
    println!("{keys:?}");
}
```

```rust
use std::collections::HashMap;

fn main() {
    let m = HashMap::from([(1, "a"), (2, "b")]);
    println!("{}", m.len()); // 可依赖：长度；不可依赖：迭代次序
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{"a": 1, "b": 2}
	for k := range m {
		fmt.Println(k) // 顺序不保证
	}
}
```

- **Go 怎么做**：map 迭代故意不稳定。
- **Rust 为什么不同**：同样不保证 `HashMap` 顺序。
- **Go 程序员易踩的坑**：快照测试写死 HashMap Debug 顺序。

---

## Q17. Go 的 map 和 Rust `HashMap` 最大的工程差异是什么？ {#q17}
**Tags:** `occasional` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

Go map 引用语义 + 零值可读可写；Rust `HashMap` 拥有键值，读写借用分离，缺键用 `Option`/`entry`，并发要显式同步。

**解答：**

Go：`m[k]++` 很爽；多 goroutine 写要自己加锁。Rust：借用检查管单线程别踩引用；多线程用 `Mutex<HashMap<...>>` 等。缺键不是零值，是 `None`。

```rust
use std::collections::HashMap;

fn main() {
    let mut m = HashMap::new();
    *m.entry("n").or_insert(0) += 1;
    println!("{}", m.get("missing").copied().unwrap_or(0));
}
```

```rust
use std::collections::HashMap;

fn main() {
    let m = HashMap::from([("a", 1)]);
    match m.get("a") {
        Some(v) => println!("{v}"),
        None => println!("nope"),
    }
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{}
	m["n"]++
	fmt.Println(m["missing"]) // 0
}
```

- **Go 怎么做**：零值让读缺失键很方便。
- **Rust 为什么不同**：用 `Option` 区分“没有”和“有零值”。
- **Go 程序员易踩的坑**：`m["k"]` 式思维导致该用 `entry`/`get` 时乱 `unwrap`。

---

## Q18. 如何把一堆 `Result<T, E>` 收成 `Result<Vec<T>, E>`？ {#q18}
**Tags:** `occasional` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

对迭代器直接 `collect()`：因为 `Result<Vec<T>, E>` 实现了从 `Result<T, E>` 迭代器收集——遇第一个 `Err` 就失败。

**解答：**

```rust
let collected: Result<Vec<_>, _> = results.into_iter().collect();
```

也可 `?` 写在循环里。要“收集所有错误”需另用策略（crate 或手写），标准 `collect` 是 fail-fast。

```rust
fn main() {
    let rs = vec![Ok(1), Ok(2), Ok(3)];
    let v: Result<Vec<i32>, &str> = rs.into_iter().collect();
    println!("{:?}", v.unwrap());
}
```

```rust
fn main() {
    let rs = vec![Ok(1), Err("boom"), Ok(3)];
    let v: Result<Vec<i32>, &str> = rs.into_iter().collect();
    println!("{:?}", v.err());
}
```

```rust
fn parse_all(xs: &[&str]) -> Result<Vec<i32>, std::num::ParseIntError> {
    xs.iter().map(|s| s.parse::<i32>()).collect()
}

fn main() {
    println!("{:?}", parse_all(&["1", "2"]));
}
```

**Go 对比：**

```go
package main

import (
	"fmt"
	"strconv"
)

func parseAll(xs []string) ([]int, error) {
	out := make([]int, 0, len(xs))
	for _, s := range xs {
		n, err := strconv.Atoi(s)
		if err != nil {
			return nil, err
		}
		out = append(out, n)
	}
	return out, nil
}

func main() {
	fmt.Println(parseAll([]string{"1", "2"}))
}
```

- **Go 怎么做**：循环里遇错返回。
- **Rust 为什么不同**：`collect` 对 `Result` 有特化。
- **Go 程序员易踩的坑**：手写一堆 match，不知道一行 `collect` 就行。

---

## Q19. 哪些集合操作最容易诱发无意义 clone？ {#q19}
**Tags:** `advanced` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

为绕开借用而 `clone` 整个 `Vec`/`String`/`HashMap`，或把 `String` 键反复 `clone` 进 `entry`；先问能否借用、`entry`、索引、缩短作用域。

**解答：**

常见浪费：`map.get(&k).cloned()` 其实只需 `copied` 的 `Copy` 值；`for x in v.clone()`；为 `insert` 先 `k.clone()` 再 `get`。优先 `&str` 查找、`entry`、结构体里存 `Rc`/`Arc` 等共享（确有共享需求时）。

```rust
use std::collections::HashMap;

fn main() {
    let mut m = HashMap::new();
    let k = String::from("a");
    m.insert(k, 1); // move 进去，不必 clone
    println!("{:?}", m.get("a")); // 用 &str 查找
}
```

```rust
fn main() {
    let v = vec![String::from("a"), String::from("b")];
    for s in &v {
        println!("{s}");
    }
    println!("{}", v.len());
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	m := map[string]int{}
	k := "a"
	m[k] = 1
	fmt.Println(m["a"])
}
```

- **Go 怎么做**：string 赋值便宜，较少纠结 clone。
- **Rust 为什么不同**：`clone` 可能分配，要显式。
- **Go 程序员易踩的坑**：编译器一报错就 `.clone()` 灭火。

---

## Q20. 本章最值得背的集合 API 选择表是什么？ {#q20}
**Tags:** `advanced` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

序列用 `Vec`；队列两端用 `VecDeque`；无序字典 `HashMap`；有序字典 `BTreeMap`；去重 `HashSet`；查+插用 `entry`；组装用 `collect`。

**解答：**

| 需求 | 优先选择 |
|------|----------|
| 动态数组 | `Vec` |
| FIFO/双端 | `VecDeque` |
| 哈希键值 | `HashMap` |
| 有序键值/范围 | `BTreeMap` |
| 去重集合 | `HashSet` |
| 有则改无则插 | `entry` |
| 迭代组装 | `collect` |
| get 后还要改 | 先拷贝值或 `entry`，避免 `E0502` |

```rust
use std::collections::{HashMap, HashSet, VecDeque};

fn main() {
    let v = vec![1, 2, 3];
    let mut q = VecDeque::from(v);
    q.push_back(4);
    let mut set = HashSet::from([1, 2]);
    set.insert(3);
    let mut map = HashMap::from([("a", 1)]);
    *map.entry("a").or_insert(0) += 1;
    println!("{:?} {:?} {:?}", q, set, map);
}
```

```rust
fn main() {
    let squares: Vec<_> = (1..=4).map(|x| x * x).collect();
    println!("{squares:?}");
}
```

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{1, 2, 3}
	m := map[string]int{"a": 1}
	s := map[int]struct{}{1: {}, 2: {}}
	fmt.Println(v, m, s)
}
```

- **Go 怎么做**：切片 + map 覆盖大多数需求。
- **Rust 为什么不同**：标准库把场景拆成更多专用类型。
- **Go 程序员易踩的坑**：只会 `Vec`+`HashMap`，在有序/双端场景硬拧。

---

## Q21. `entry().or_insert` 的标准写法是什么？和 `or_insert_with` / `or_default` 怎么选？ {#q21}
**Tags:** `hot` `HashMap` `entry` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

计数/累加的标准 idiom 是 `*map.entry(k).or_insert(0) += 1`；默认值构造很贵时用 `or_insert_with(|| ...)`；值类型实现了 `Default` 时用 `or_default()`。一次查找完成“有则改、无则插”（入门见 [Q4](#q4)）。

**解答：**

词频统计是最常见模板：

```rust
use std::collections::HashMap;

fn main() {
    let mut freq: HashMap<&str, usize> = HashMap::new();
    for w in ["go", "rust", "go", "rust", "go"] {
        *freq.entry(w).or_insert(0) += 1;
    }
    assert_eq!(freq["go"], 3);
}
```

`or_insert(v)` 每次调用都先构造 `v`（即使键已存在也会构造后再丢弃）；昂贵默认值改用闭包：

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<&str, Vec<i32>> = HashMap::new();
    map.entry("a").or_insert_with(|| Vec::with_capacity(64)).push(1);
    map.entry("a").or_insert_with(|| panic!("should not build")).push(2);
    assert_eq!(map["a"], vec![1, 2]);
}
```

`Default` 类型用 `or_default()` 更短；需要“读改写”分支时配 `and_modify`：

```rust
use std::collections::HashMap;

fn main() {
    let mut map: HashMap<&str, String> = HashMap::new();
    map.entry("msg").or_default().push_str("hi");
    map.entry("msg")
        .and_modify(|s| s.push('!'))
        .or_insert_with(|| String::from("x"));
    assert_eq!(map["msg"], "hi!");
}
```

避免先 `get` 再 `insert` 的两趟查找，也常顺带避开 `E0502`（见 [Q3](#q3)）。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	freq := map[string]int{}
	for _, w := range []string{"go", "rust", "go"} {
		freq[w]++ // 零值可直接写
	}
	fmt.Println(freq["go"])
}
```

- **Go 怎么做**：map 读缺失键得零值，可直接 `++`。
- **Rust 为什么不同**：没有“读出零值就能写回”的语义，用 `entry` 表达同一意图。
- **Go 程序员易踩的坑**：手写 get/insert 两步，又撞借用又多一次哈希。

**记忆点：**

- 计数：`*entry(k).or_insert(0) += 1`。
- 贵默认：`or_insert_with`；有 `Default`：`or_default`。
- 能 `entry` 就别 get+insert。

---

## Q22. `remove`、`swap_remove`、`retain` 该怎么选？ {#q22}
**Tags:** `common` `Vec` `remove` `retain` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

要按索引删且**保持相对顺序**用 `remove`（O(n)）；不在乎顺序、要 O(1) 用 `swap_remove`；按谓词留下一批用 `retain`。`HashMap` 按键删除用 `remove`（对照 [Q14](#q14) 的所有权视角）。

**解答：**

`remove(i)` 把后面元素前移，保序：

```rust
fn main() {
    let mut v = vec!["a", "b", "c", "d"];
    let taken = v.remove(1); // 拿走 "b"，后面左移
    assert_eq!(taken, "b");
    assert_eq!(v, ["a", "c", "d"]);
}
```

`swap_remove(i)` 用最后一个填洞，快但不保序：

```rust
fn main() {
    let mut v = vec!["a", "b", "c", "d"];
    let taken = v.swap_remove(1); // "b" 被拿走，"d" 填到下标 1
    assert_eq!(taken, "b");
    assert_eq!(v, ["a", "d", "c"]);
}
```

`retain` 原地过滤，被踢出的元素直接 drop，不逐个返回：

```rust
fn main() {
    let mut v = vec![1, 2, 3, 4, 5];
    v.retain(|x| x % 2 == 1);
    assert_eq!(v, [1, 3, 5]);
}
```

选型：游戏实体袋、无序缓冲区 → `swap_remove`；展示列表、时间线 → `remove`/`retain`；删 map 条目 → `map.remove(&key)`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []string{"a", "b", "c", "d"}
	// 保序删除
	v = append(v[:1], v[2:]...)
	fmt.Println(v)
	// 无序删除：用末尾覆盖
	u := []string{"a", "b", "c", "d"}
	u[1] = u[len(u)-1]
	u = u[:len(u)-1]
	fmt.Println(u)
}
```

- **Go 怎么做**：切片拼装或末尾覆盖，没有同名标准方法。
- **Rust 为什么不同**：`Vec` 把保序/不保序删法做成明确 API，避免无意选错复杂度。
- **Go 程序员易踩的坑**：循环里反复 `remove(0)` 当成队列（O(n²)）；队列场景看 `VecDeque`。

**记忆点：**

- 保序 → `remove`；要快不保序 → `swap_remove`。
- 批量按条件留 → `retain`。
- Map 按键删 → `HashMap::remove`。

---

## Q23. `v[i]` 越界会 panic，和 `get` / `get_mut` 怎么选？ {#q23}
**Tags:** `hot` `beginner` `Vec` `indexing` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

`v[i]`（`Index`）在越界时**直接 panic**；`get` / `get_mut` 返回 `Option`，越界是 `None`。下标来自外部输入或不确定时用 `get`；你能证明下标合法（刚用 `len` 算过、算法不变量）时用 `v[i]` 更短。

**解答：**

合法下标时索引很干净：

```rust
fn main() {
    let v = vec![10, 20, 30];
    assert_eq!(v[1], 20);
    assert_eq!(v.get(1), Some(&20));
    assert_eq!(v.get(99), None);
}
```

需要改元素且可能越界时用 `get_mut`：

```rust
fn main() {
    let mut v = vec![1, 2, 3];
    if let Some(x) = v.get_mut(1) {
        *x *= 10;
    }
    assert_eq!(v, [1, 20, 3]);
    assert_eq!(v.get_mut(9), None);
}
```

「❌ 错误写法」——对不可信下标用 `v[i]`：

```rust
fn main() {
    let v = vec![1, 2, 3];
    let i = 99usize;
    let _ = v[i];
    // thread 'main' panicked at ... index out of bounds: the len is 3 but the index is 99
}
```

`HashMap` 的 `map[k]` 在缺键时也会 panic（走 `Index`）；日常查找用 `get`，缺键插入用 `entry`（见 [Q4](#q4) / [Q21](#q21)）。切片 `&[T]` 同样有 `get`/`get_mut`。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	v := []int{10, 20, 30}
	fmt.Println(v[1])
	// v[99] 同样 panic
	if 99 < len(v) {
		fmt.Println(v[99])
	}
}
```

- **Go 怎么做**：索引越界也是运行时 panic；常用先比 `len`。
- **Rust 为什么不同**：额外提供 `Option` 路径，把“可能没有”编码进类型。
- **Go 程序员易踩的坑**：所有查找都写 `v[i]` / `m[k]`，把可恢复的缺失变成崩溃。

**记忆点：**

- 确定合法 → `v[i]`；不确定 → `get`/`get_mut`。
- `HashMap` 查找优先 `get`，别依赖 `map[k]`。
- 越界索引 = panic，不是 `Option`。

---

## Q24. `extend`、`append`、`reserve` + `push` 该怎么选？ {#q24}
**Tags:** `hot` `Vec` `extend` `append` `collections`
**适用版本:** Rust 1.0+

**一句话答案：**

从任意迭代器批量灌入用 `extend`；把另一个 `Vec` 的全部元素**搬走拼到自己尾部**用 `append`（对方变空）；已知最终大小、逐个构造元素时用 `reserve`/`with_capacity` 再 `push`，减少扩容。

**解答：**

`extend` 吃任何 `IntoIterator`：

```rust
fn main() {
    let mut v = vec![1, 2];
    v.extend([3, 4]);
    v.extend(5..=6);
    assert_eq!(v, [1, 2, 3, 4, 5, 6]);
}
```

`append` 专门吞另一个 `Vec`，移动元素、对方 `clear` 成空但保留 capacity：

```rust
fn main() {
    let mut a = vec![1, 2];
    let mut b = vec![3, 4];
    a.append(&mut b);
    assert_eq!(a, [1, 2, 3, 4]);
    assert!(b.is_empty());
}
```

预分配后再 `push`（见 [Q9](#q9)）：

```rust
fn main() {
    let n = 100;
    let mut v = Vec::with_capacity(n);
    // 等价：let mut v = Vec::new(); v.reserve(n);
    for i in 0..n {
        v.push(i);
    }
    assert_eq!(v.len(), n);
    assert!(v.capacity() >= n);
}
```

选型口令：有现成迭代器 / 数组 / 范围 → `extend`；有另一个要掏空的 `Vec` → `append`；循环里一个个算出来 → `reserve` + `push`。`extend` 一个 `Vec` 也可以（`a.extend(b)` 会消费 `b`），但 `append(&mut b)` 在“保留对方空壳再复用”时更贴切。

**Go 对比：**

```go
package main

import "fmt"

func main() {
	a := []int{1, 2}
	b := []int{3, 4}
	a = append(a, b...)
	fmt.Println(a, b) // b 仍在；Go 没有“append 掏空对方”的标准语义
}
```

- **Go 怎么做**：统一 `append`，预分配用 `make([]T, 0, n)`。
- **Rust 为什么不同**：把“迭代器灌入 / 掏空另一 Vec / 预留再 push”拆成更准确的 API。
- **Go 程序员易踩的坑**：只会循环 `push`，在已知长度时反复扩容；或把 `append` 和 Go 的 `append` 一一等同。

**记忆点：**

- 迭代器批量 → `extend`。
- 掏空另一个 `Vec` → `append`。
- 已知容量逐个加 → `reserve`/`with_capacity` + `push`。

---

## Q25. 优先队列用 `BinaryHeap` 吗？怎么做最小堆？（对标 `container/heap`） {#q25}
**Tags:** `hot` `BinaryHeap` `priority-queue` `Reverse`
**适用版本:** Rust 1.0+（`std::collections::BinaryHeap`；`Reverse` 在 `std::cmp`）

**一句话答案：**
标准库优先队列就是 **`BinaryHeap<T>`**（二叉堆）：默认是**最大堆**（`peek`/`pop` 最大）。要最小堆，用 **`BinaryHeap<Reverse<T>>`**，或自定义 `Ord`。对标 Go 的 `container/heap`。

**解答：**
最大堆：

```rust
use std::collections::BinaryHeap;

fn main() {
    let mut heap = BinaryHeap::new();
    heap.push(1);
    heap.push(5);
    heap.push(3);
    assert_eq!(heap.pop(), Some(5));
    assert_eq!(heap.peek(), Some(&3));
}
```

最小堆（推荐写法）：

```rust
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn main() {
    let mut heap = BinaryHeap::new();
    heap.push(Reverse(1));
    heap.push(Reverse(5));
    heap.push(Reverse(3));
    assert_eq!(heap.pop(), Some(Reverse(1)));
    assert_eq!(heap.peek().map(|r| r.0), Some(3));
}
```

任务调度常见形状：

```rust
use std::cmp::Reverse;
use std::collections::BinaryHeap;

#[derive(Eq, PartialEq, Ord, PartialOrd, Debug)]
struct Job {
    priority: i32, // 越大越优先 → 直接进最大堆
    id: u32,
}

fn main() {
    let mut q = BinaryHeap::new();
    q.push(Job { priority: 1, id: 10 });
    q.push(Job { priority: 9, id: 2 });
    assert_eq!(q.pop().unwrap().id, 2);

    // 若 priority 越小越先：包一层 Reverse，或把字段顺序/符号设计进 Ord
    let mut min_ids = BinaryHeap::new();
    min_ids.push(Reverse(7));
    min_ids.push(Reverse(2));
    assert_eq!(min_ids.pop().unwrap().0, 2);
}
```

注意：`BinaryHeap` **不是**稳定排序；相等优先级的弹出顺序不保证。需要「同优先级 FIFO」时，在元素里再加单调序号参与排序。

**Go 对比：**

```go
package main

import (
	"container/heap"
	"fmt"
)

type IntHeap []int

func (h IntHeap) Len() int            { return len(h) }
func (h IntHeap) Less(i, j int) bool  { return h[i] < h[j] } // 最小堆
func (h IntHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *IntHeap) Push(x any)         { *h = append(*h, x.(int)) }
func (h *IntHeap) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func main() {
	h := &IntHeap{3, 1, 5}
	heap.Init(h)
	heap.Push(h, 2)
	fmt.Println(heap.Pop(h)) // 1
}
```

- **Go 怎么做**：实现 `heap.Interface`，`Less` 决定最小/最大。
- **Rust 为什么不同**：给现成 `BinaryHeap`；默认最大堆，最小堆用 `Reverse`。
- **Go 程序员易踩的坑**：以为默认最小堆——Rust 默认是最大堆。

**记忆点：**

- 优先队列 → `BinaryHeap`。
- 最大堆直接用；最小堆 → `Reverse`。
- 稳定同优先级要自己加序号。

---
