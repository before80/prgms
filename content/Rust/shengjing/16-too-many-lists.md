+++
title = "16-手把手带你实现链表"
date = 2026-07-28T14:49:00+08:00
weight = 160
type = "docs"
description = "《Rust语言圣经》「手把手带你实现链表」精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「手把手带你实现链表」

# 手把手带你实现链表

> 其它语言：学语法？写个链表吧。Rust：精通了？写个链表证明一下。

译自 [Learning Rust With Entirely Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)。**日常开发请用 `Vec` / `VecDeque` / 标准库 `LinkedList`，本章为教学深坑。**

项目：`cargo new --lib lists`，每版链表单独模块文件，跟着编译器报错迭代。

## 我们到底需不需要链表

**99% 场景用 `Vec`；剩余 1% 里 99% 用 `VecDeque`。**

链表合理场景：频繁分割/合并、无锁并发、内核/嵌入式、纯函数式语言受限、**教学**。

常见误区反驳：

| 说法 | 反驳要点 |
|------|----------|
| O(1) 插入删除 | 调用频率是否在热点？`Vec` push/pop 也是 O(1) 且更快 |
| 不能承受 realloc | 非热点无所谓；可 `with_capacity` / `size_hint` |
| 更省内存 | 每节点多 1–2 指针；小元素大量节点反而浪费 |
| 函数式习惯 head/tail | Rust 有 `Iterator`、切片、不可变无需链表 |
| 并发结构 | 确实合适，但仅当无更好方案 |

## 不太优秀的单向链表：栈

**目标**：LIFO 栈；第一版「能编译但设计差」。

### 数据布局

函数式定义 `List = Empty | Elem(a, List)` → Rust 递归 enum **无限大小**。

- **陷阱 E0072**：递归 variant 需 indirection → `Box<List>`
- 坏布局：最后一节点堆上像 junk；首节点可能在栈上
- 好布局：`List { head: Link }` + `Node { elem, next }`，`Link = Option<Box<Node>>`，统一堆分配

### 基本操作

- `push`：`mem::replace(&mut head, None)` 取旧 head 挂到新节点 `next`
- `pop`：`replace` head → match `Some(node)` 提升 `node.next` 为新 head
- **陷阱**：直接 `self.head = node.next` 会 partial move；用 `replace` 避免

### 最后实现

- 手写 `Drop`：循环 `replace` 逐节点释放，避免递归 drop 栈溢出
- 单元测试 + 初步 `Peek`

**本版关键词**：`Box`、DST、枚举 niche 优化、`mem::replace`、手动 Drop。

## 还可以的单向链表

**目标**：类型优化 + 完整迭代器族 + Peek。

### 优化类型定义

- `type Link = Option<Box<Node>>` 替代自定义 `enum Link`（语义相同，更 idiomatic）
- 加泛型 `List<T>`

### 定义 Peek 函数

- `peek` / `peek_mut`：返回 `Option<&T>` / `Option<&mut T>`，不消费节点
- 借用规则：`&mut self` 期间不能 push/pop

### IntoIter 和 Iter

| 迭代器 | 所有权 | 实现要点 |
|--------|--------|----------|
| `IntoIter` | 消费 List | 字段 `head: Link`，每次 pop 式前进 |
| `Iter` | 共享引用 | 存 `Option<&Node>`，`*next` 不可变遍历 |

- `IntoIterator` for `List` / `&List`
- **陷阱**：`Iter` 生命周期需 `'a` 绑定到 List

### IterMut 以及完整代码

- `IterMut`：`Option<&mut Node>`，同一时刻仅一个可变遍历
- 完整 impl：`FromIterator`、Debug、PartialEq（测试用）
- **陷阱**：IterMut 与 push/pop 互斥（可变借用冲突）

## 持久化单向链表

**目标**：函数式不可变栈 — `prepend`/`tail` 返回新 List，共享尾部节点。

### 数据布局和基本操作

- 多 List 共享节点 → 不能用独占 `Box` → **`Rc<Node>`**
- `Link<T> = Option<Rc<Node<T>>>`
- `prepend`：`Rc::new(Node { next: self.head.clone() })` — `clone` 是 **Rc 计数+1**，非深拷贝
- `tail`：克隆 `next` 指针构造新 List（共享后缀）
- **不可变**：无 `&mut self` 的 push/pop

### Drop、Arc 及完整代码

- **陷阱**：`Drop` 不能简单递归 drop 共享 Rc 节点 → 用 `Rc::try_unwrap`，仅最后一个 owner 才释放
- 循环 + `mem::replace` 配合 `try_unwrap`
- 多线程持久化需 `Arc`（本章用 `Rc`）

## 不咋样的双端队列

**目标**：Deque（头尾 push/pop）；安全但极其啰嗦。

### 数据布局和基本操作

- 双向：`Node { prev, next }`，`List { head, tail }`
- **`Rc<RefCell<Node>>`**：共享 + 内部可变
- **陷阱**：RefCell 运行时 borrow 检查；push/pop 逻辑量翻倍
- 不变量：非空时 head/tail 互相可达；每内部节点被 prev/next 正确指向

### Peek

- `peek_front` / `peek_back`：通过 `RefCell` 借 `elem`
- **陷阱**：持有 peek 借用时不能 mutate 结构

### 基本操作的对称镜像

- `push_front` / `push_back` / `pop_front` / `pop_back` 四向对称
- 空 deque 边界：head/tail 同时为 None 或同时指向唯一节点

### 迭代器

- `Iter` / `IntoIter`：沿 next 或 prev 走
- RefCell 使迭代器实现比单向链表痛苦得多

### 最终代码

- 能用的安全 deque，但代码量、运行时 RefCell 开销、API 易误用
- **结论**：教学价值 > 实用价值

## 不错的 unsafe 队列

**目标**：FIFO 队列；`Box` + 裸指针，性能接近理想。

### 数据布局

- 队列 = 头进尾出；单 `tail` 指针不够 → **`head` + `tail`**
- 初版：`Link = Option<Box<Node>>`，tail 指向最后节点
- **陷阱**：单链表只存 tail 则 push/pop 一端 O(n)

### 基本操作

- `push`：尾插；更新 `tail`
- `pop`：头删；空时 head/tail 置 None
- 维护 tail 指向**最后一个**节点（非 None 的 next）

### Miri

- `cargo +nightly miri test`：检测 UB 的 interpreter
- unsafe 链表**必须**配合 Miri/测试

### 栈借用

- Rust 别名规则：`*mut` 可变与共享引用互斥
- Stacked Borrows 模型：每次 borrow 压栈，冲突则 UB
- `UnsafeCell` 绕过编译期借用，运行时自己保证

### 测试栈借用

- 专门测试：数组、不可变引用、内部可变性、Box 的 aliasing 边界

### 数据布局 2

- 进一步裸：`NonNull<Node>` 替代 `Box` 链，减少 Option 开销
- tail 存 `Option<NonNull<Node>>`

### 额外的操作

- `IntoIter`、`Peek`、`Drop` 的 unsafe 实现
- `Drop`：walk 链表 raw 释放

### 最终代码

- 可用的 unsafe 单向队列；Send 需手动 impl（若满足条件）

## 生产级的双向 unsafe 队列

**目标**：接近 `std::collections::LinkedList` 质量的双向 deque + cursor。

### 数据布局

两种方案：

| 方案 | 结构 | 优缺点 |
|------|------|--------|
| 传统 | head/tail 指针 + 双向节点 | 边界情况多 |
| 哨兵/虚拟节点 | 环状 dummy node | 消除空列表特例，实现复杂 |

节点：`prev`/`next` 裸指针或 `NonNull`；List 持有 head/tail 或 sentinel。

### 型变与子类型

- 泛型容器含 `'a` 引用时：**型变**（variance）影响子类型关系
- **`PhantomData<T>`**：告诉编译器逻辑上「拥有」T，影响 Send/Sync/variance，不占空间

### 基础结构

- push/pop 四向 + 指针修复（6+ 指针写操作）
- **陷阱**：任一指针写错 → 内存泄漏或 double free

### 恐慌与安全

- **Drop 与 panic 安全**：操作中 panic 不能泄漏节点或破坏链表
- 模式：`mem::replace` / 先建后连 / scope guard 思维
- `ManuallyDrop` 控制 drop 时机

### 无聊的组合

- 枚举所有 head/tail/空/单节点 组合，逐一实现/测试
- 组合爆炸是 bidirectional unsafe 的主要成本

### 其它特征

- `Debug`、`PartialEq`、`FromIterator`、`Extend`
- 编译期测试：Send/Sync 自动 trait 或 negative impl

### 测试

- 单元 + 属性测试 + Miri
- 覆盖 push/pop/peek/iter/drop 组合

### Send,Sync和编译测试

- 裸指针默认 !Send；含 `PhantomData<*const T>` 等标记影响
- `compile_fail` 测试验证不应 Send 的类型

### 实现游标

- `CursorMut`：在 deque 内 O(1) 插入/删除当前节点
- `split` / `splice` 等高级 API
- 游标持有 `&mut List` + 当前 `NonNull`

### 测试游标

- 游标越界、空 deque、头尾、splice 后不变量

### 最终代码

- 生产级 unsafe deque：性能强、代码量大、维护成本高
- **仅当标准库/生态不满足且团队有 unsafe 能力时使用**

## 使用高级技巧实现链表

### 双单向链表

- 两个 `Stack<T>`：`left` + `right`，分别向两端增长
- 避免 RefCell/Rc 双向噩梦；用已有 ok-stack 组合
- 牺牲：非真双向节点，某些操作语义不同

### 栈上的链表

- 固定容量 + 数组/索引模拟 `next` 指针（arena 风格）
- 无堆分配；适合嵌入式/实时
- **陷阱**：容量固定；索引生命周期管理

---

## 版本演进总览

```text
bad-stack      Box + replace + Drop
ok-stack       Option<Box> + 泛型 + Iter/IterMut/IntoIter
persistent     Rc + prepend/tail + try_unwrap Drop
deque          Rc<RefCell> 双向（安全但丑）
unsafe-queue   Box/NonNull + head/tail + Miri
prod-deque     双向裸指针 + PhantomData + cursor + panic-safe
advanced       双 Stack 组合 / 栈上 arena
```

## 贯穿知识点

| 主题 | 出现章节 |
|------|----------|
| `Box` / `Rc` / `Arc` / 裸指针 / `NonNull` | 全系列递进 |
| `mem::replace` / 手动 Drop | bad → unsafe |
| 迭代器三件套 | ok-stack |
| 内部可变性 RefCell | deque |
| unsafe / Miri / stacked borrows | unsafe-queue |
| PhantomData / variance / Send Sync | prod-deque |
| panic safety | prod-deque |

**源码路径**：`shengJing/_src/src/too-many-lists/` 各子目录对应上表模块名。
