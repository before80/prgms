+++
title = "07-Rust高级进阶"
date = 2026-07-28T14:49:00+08:00
weight = 70
type = "docs"
description = "《Rust语言圣经》Rust高级进阶各专题精要速成"
isCJKLanguage = true
draft = false

+++

> 精要笔记 · 基于 [Rust语言圣经](https://beatai.org/rust-course/)「Rust 高级进阶」

# Rust 高级进阶

基础已会，本章一带而过细节，聚焦规则与最短示例。

## 生命周期

生命周期标注引用有效范围；编译器用消除规则推断，搞不定时手动标。

### 深入生命周期

#### 不太聪明的生命周期检查

```rust
impl Foo {
    fn mutate_and_share(&mut self) -> &Self { &*self }
    fn share(&self) {}
}
// loan = foo.mutate_and_share(); foo.share(); // E0502
```

- 消除规则 3：`&mut self` 与返回值 `&Self` 同生命周期 `'a`，loan 用到 `println!` 前可变借用仍有效
- **口诀**：编译器按签名推断，不按「方法内已结束借用」；改结构或缩短返回值生命周期

`match map.get_mut()` 分支内再 `insert` 也会 E0499（match 整块视为同一借用域）→ 用 `if let` / 提前 `drop` 借用。

#### 无界生命周期

```rust
fn f<'a, T>(x: *const T) -> &'a T { unsafe { &*x } } // 'a 凭空产生
```

- 避免：输出生命周期被消除时必有对应输入生命周期

#### 生命周期约束 HRTB

```rust
struct DoubleRef<'a, 'b: 'a, T> { r: &'a T, s: &'b T } // 'b 至少与 'a 同寿
struct Ref<'a, T: 'a> { r: &'a T }                     // T 活得比 'a 久
```

HRTB（高阶）：`for<'a> Fn(&'a str)` — 对**任意** `'a` 的引用都成立。

#### 闭包函数的消除规则

- 闭包环境 + 输入参数 → 编译器推断捕获引用生命周期
- `move` 闭包：捕获变为 owned，常配合 `'static`

#### NLL (Non-Lexical Lifetime)

- 借用**最后使用点**结束，非词法作用域末尾
- 再借用（reborrow）：`&mut *x` 子借用结束后可变借用可继续

#### 生命周期消除规则补充

1. 每个引用参数各得独立生命周期
2. 仅一个输入生命周期 → 赋给所有输出
3. `&self` / `&mut self` 方法：输出生命周期 = `self` 的生命周期

#### 一个复杂的例子

多引用返回时按规则 2/3 推断；冲突则显式 `'a, 'b: 'a`。

### &'static 和 T: 'static

#### `&'static`

- 字面量、`&'static str`、全局静态数据；**不是**「活整个程序」的唯一含义

#### `T: 'static`

- `T` 不含非 `'static` 的引用；owned 类型通常满足
- `spawn` 要求 `F: 'static`：闭包不能捕获栈上短生命周期引用

#### static 到底针对谁？

- `'static` 约束的是**类型/绑定**，不是「必须全局存储」

## 函数式编程: 闭包、迭代器

### 闭包 Closure

```rust
let x = 1;
let sum = |y| x + y;
assert_eq!(3, sum(2));
```

- 匿名、可赋值/传参、**捕获**环境

#### 使用闭包来简化代码

`|intensity| { ... }` 替代重复函数调用；改一处即可。

#### 闭包的类型推导

```rust
let ex = |x| x + 1; // 第一次调用前类型未固定
```

#### 结构体中的闭包

```rust
struct C<T> { c: T }
// T: Fn(i32) -> i32 等
```

#### 捕获作用域中的值

##### 闭包对内存的影响

- 捕获引用 → 栈上指针；`move` → 按值捕获（可能堆分配）

##### 三种 Fn 特征

| 特征 | 调用 | 捕获 |
|------|------|------|
| `Fn` | `&self` | 不可变 |
| `FnMut` | `&mut self` | 可变 |
| `FnOnce` | 消费 self | 移动 |

```rust
fn call_fn(f: impl Fn()) { f(); f(); }
fn call_once(f: impl FnOnce()) { f(); }
```

- `thread::spawn` 要 `FnOnce + Send + 'static`

#### 闭包作为函数返回值

返回 `impl Fn()` 或 `Box<dyn Fn()>`；注意捕获变量生命周期。

#### 闭包的生命周期

返回引用时生命周期与捕获绑定；常改返回 owned 或 `'static`。

### 迭代器 Iterator

#### For 循环与迭代器

```rust
for v in arr { }      // 语法糖：IntoIterator
for i in 1..10 { }
```

- 数组非迭代器，但实现了 `IntoIterator`

#### 惰性初始化

```rust
let it = v.iter(); // 未消费前不遍历
for x in it { }
```

#### next 方法

```rust
trait Iterator {
    type Item;
    fn next(&mut self) -> Option<Self::Item>;
}
```

#### IntoIterator 特征

`iter()` / `iter_mut()` / `into_iter()` 三种借用形式

#### 消费者与适配器

- **消费者**：`collect` `sum` `count` `fold` `for_each`
- **适配器**：`map` `filter` `take` `skip` `enumerate` `zip` `chain`
- **口诀**：适配器惰性，消费者触发执行

```rust
v.iter().filter(|x| x % 2 == 0).map(|x| x * 2).sum::<i32>()
```

#### 实现 Iterator 特征

```rust
struct Counter { n: u32 }
impl Iterator for Counter {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        if self.n < 5 { self.n += 1; Some(self.n) } else { None }
    }
}
```

#### 迭代器的性能

- 零成本抽象；链式调用常编译为单循环
- 比索引循环有时更快（边界检查消除）

## 深入类型

### 类型转换

#### `as`转换

```rust
let a = 3i32 as i16; // 数值间，可能截断
let p = s.as_ptr();  // 指针相关
```

- **弱转换**：编译器允许但可能丢精度

#### TryInto 转换

```rust
use std::convert::TryInto;
let n: u32 = "42".try_into().unwrap();
```

- 失败返回 `Err`，比 `as` 安全

#### 通用类型转换

`From` / `Into`（自动实现）、`TryFrom` / `TryInto`：

```rust
impl From<i32> for MyType { fn from(v: i32) -> Self { ... } }
let m: MyType = 5i32.into();
```

### newtype 和 类型别名

#### newtype

```rust
struct Meters(u32);
struct Kilometers(u32);
// 防混用；可单独 impl trait
```

#### 类型别名(Type Alias)

```rust
type Kilometers = i32;
```

- 别名**不**创建新类型，仅可读性

#### !永不返回类型

```rust
fn die() -> ! { panic!() }
```

-  diverging，可赋给任意类型（类型推断用）

### Sized 和不定长类型 DST

#### 动态大小类型 DST

`str` `[T]` `dyn Trait` — 编译期大小未知，只能通过指针（`&str` `&[T]` `&dyn Trait`）

#### Sized 特征

- 默认 `T: Sized`；`?Sized` 允许 DST：`fn foo<T: ?Sized>(t: &T)`

#### `Box<str>`

`Box<str>` 堆上固定 fat pointer；`String` → `s.into_boxed_str()`

### 枚举和整数

```rust
enum E { A = 1, B = 2 }
let e: E = unsafe { std::mem::transmute(3u8) }; // 危险
```

- 推荐 `TryFrom` / `num_enum` / match；`transmute` 仅底层互操作

## 智能指针

### Box\<T\> 堆对象分配

```rust
let b = Box::new(5);
let list = Cons(1, Box::new(Cons(2, Box::new(Nil))));
```

- 堆分配；转移所有权只拷贝指针
- 场景：大对象、递归类型、`dyn Trait` 特征对象
- `Box::leak(b)` → `&'static mut T`（有意泄漏）

### Deref 解引用

```rust
trait Deref {
    type Target;
    fn deref(&self) -> &Self::Target;
}
```

- `*` 显式解引用；`&T` → `&U` 强制解引用（赋值/传参）
- 连续解引用：编译器多次 `deref`（最多一层到 method 自动解引用）

### Drop 释放资源

```rust
struct HasDrop;
impl Drop for HasDrop { fn drop(&mut self) { println!("drop"); } }
```

- 离开作用域自动 `drop`；`std::mem::drop(x)` 手动提前释放
- **Copy 与 Drop 互斥**

### Rc 与 Arc 实现 1vN 所有权机制

```rust
use std::rc::Rc;
let a = Rc::new(5);
let b = Rc::clone(&a); // 引用计数 +1
```

- `Rc<T>`：单线程共享所有权
- `Arc<T>`：多线程 + `Send`/`Sync`；`Arc::clone` 原子计数
- **Rc 不能跨线程** → 用 Arc

### Cell 与 RefCell 内部可变性

```rust
use std::cell::{Cell, RefCell};
let c = Cell::new(1); c.set(2); let v = c.get(); // Copy 类型
let r = RefCell::new(String::from("hi"));
let s = r.borrow_mut(); // 运行时 borrow 检查，违反则 panic
```

- **内部可变性**：`&self` 上改数据
- `RefCell` + `Rc`：多所有者可变；`try_borrow` 避免 panic
- `Cell::from_mut(&mut T)` 临时拆分可变借用

## 循环引用与自引用

### Weak 与循环引用

```rust
use std::rc::{Rc, Weak};
struct Node { next: Option<Rc<Node>>, owner: Option<Weak<Node>> }
```

- `Rc` 强引用循环 → 泄漏；`Weak::upgrade()` → `Option<Rc>`
- `Arc` + `Weak` 多线程同理

### 结构体中的自引用

```rust
// 错：self 移动后内部指针失效
struct SelfRef { s: String, p: *const u8 }
```

- 方案：`Pin` 固定地址、`ouroboros` 宏、间接存储索引、Arena
- **Pin**：`Pin<P<T>>` 保证 `T` 不被移动（`!Unpin` 类型）

## 多线程并发编程

### 并发和并行

- **并发**：任务交替推进；**并行**：同时执行
- 单核可并发不可并行；多核可并行

### 使用多线程

```rust
let h = thread::spawn(|| { /* ... */ });
h.join().unwrap();
```

- `move ||` 捕获所有权进新线程
- `thread::scope`：栈上线程，借用外部数据
- CPU 密集：线程数 ≈ 核心数；IO 密集：线程/ async 更多

### 线程同步：消息传递

```rust
let (tx, rx) = mpsc::channel();
tx.send(1).unwrap();
for v in rx { }
```

- 多生产者 `clone(tx)`；`try_recv` 非阻塞
- 同步 channel 满则阻塞发送；异步见 tokio mpsc

### 线程同步：锁、Condvar 和信号量

```rust
let m = Mutex::new(0);
let mut g = m.lock().unwrap();
```

- `RwLock`：读多写少；写锁排斥读写
- **死锁**：两锁交叉获取 → 固定加锁顺序
- `Condvar::wait` / `wait_timeout`：等条件
- `Semaphore`：限制并发数

### 线程同步：Atomic 原子操作与内存顺序

```rust
use std::sync::atomic::{AtomicUsize, Ordering};
static N: AtomicUsize = AtomicUsize::new(0);
N.fetch_add(1, Ordering::SeqCst);
```

- `Relaxed` / `Acquire` / `Release` / `AcqRel` / `SeqCst`
- 简单计数用 Atomic；复杂不变量仍用 Mutex

### 基于 Send 和 Sync 的线程安全

- **`Send`**：所有权可跨线程转移
- **`Sync`**：`&T` 可跨线程共享
- `Rc` 非 Send/Sync；`Arc<Mutex<T>>` 常见组合
- 裸指针默认非 Send/Sync，unsafe 可手动 impl（需自证安全）

## 全局变量

```rust
static mut COUNTER: u32 = 0; // unsafe 读写
static HELLO: &str = "hi";    // 编译期

use std::sync::OnceLock;
static CONFIG: OnceLock<String> = OnceLock::new();
CONFIG.get_or_init(|| load_config());
```

- `lazy_static` / `once_cell` / `OnceLock`：运行期初始化一次
- **优先** `const` / `OnceLock`；避免 `static mut`

## 错误处理

```rust
result.map(|v| v + 1).and_then(|v| ok(v)).or_else(|e| err(e));
```

- 组合器：`map` `and_then` `or_else` `unwrap_or_else`
- 自定义 `Error` trait + `thiserror` / `anyhow`
- `?` 自动 `From` 转换；库用具体错误，应用可用 `anyhow::Result`

## Unsafe Rust

### 五种兵器

1. **解引用裸指针** `*const T` / `*mut T`（需 unsafe deref）
2. **调用 unsafe fn**
3. **unsafe trait / impl**
4. **访问 `static mut`**
5. **FFI** `extern "C"`

```rust
let raw = &5 as *const i32;
unsafe { println!("{}", *raw); }
```

- unsafe 块：编译器不检查内存安全，**程序员**保证
- 安全抽象：对外 safe API，内部 unsafe 封装

### 内联汇编

```rust
unsafe {
    std::arch::asm!("nop");
}
```

- `asm!` 宏；寄存器约束、clobber；平台相关，慎用

## Macro 宏编程

### 宏和函数的区别

- **元编程**：编译期生成代码（`derive` `println!`）
- **可变参数**：`println!("a {} b", x)`
- **为任意类型 impl trait**（函数做不到）
- 缺点：难读、难调试

### 声明式宏 `macro_rules!`

```rust
macro_rules! my_vec {
    ( $( $x:expr ),* ) => {
        { let mut v = Vec::new(); $( v.push($x); )* v }
    };
}
```

- 模式匹配 Rust **源码**片段；`$()` 重复、`*` `+` 量词
- `#[macro_export]` 导出；卫生宏（hygiene）减少捕获冲突

### 用过程宏为属性标记生成代码

- `#[derive(Debug, Clone)]` — 派生宏
- 类属性宏：`#[route(GET, "/")]` 自定义
- 类函数宏：`sql!(SELECT * FROM t)` 类似函数调用

## async/await 异步编程

### async 编程入门

```rust
async fn foo() -> u32 { 42 }
let f = foo();           // impl Future，未执行
let n = foo().await;     // 驱动至完成
```

- **Future 惰性**：drop 则永不运行
- **零成本**：无内置运行时；用 tokio/async-std
- IO 密集 → async；CPU 密集 → 线程 / `spawn_blocking`

### 底层探秘: Future 执行与任务调度

```rust
enum Poll<T> { Ready(T), Pending }
trait Future {
    type Output;
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

- Executor 循环 poll；`Pending` 时 Waker 注册，就绪后 wake

### 定海神针 Pin 和 Unpin

- 自引用 Future 不能移动 → `Pin<Box<dyn Future>>`
- `Unpin`：可安全移动；大多数类型自动 Unpin

### async/await 和 Stream 流处理

```rust
async fn bar() {
    let mut stream = tokio_stream::iter(vec![1, 2, 3]);
    while let Some(v) = stream.next().await { }
}
```

- `async move`：捕获 move 进 Future
- `.await` 点可能 yield 到 executor 其它任务

### 同时运行多个 Future

```rust
tokio::join!(f1(), f2());           // 并发等全部
tokio::try_join!(f1(), f2())?;      // 任一 Err 则返回
tokio::select! {
    r = f1() => { }
    r = f2() => { }
}
```

### 一些疑难问题的解决办法

- async 块内 `?`：块返回 `Result` 即可
- `async fn` 默认 `Send`（跨线程 executor）；非 Send 捕获 → 用 `tokio::task::spawn_local`
- 递归 async：改循环或 `Box::pin` + 手动 Future
- trait 中 async：`async-trait` crate 或返回 `impl Future`

### 实践应用：Async Web 服务器

```rust
#[tokio::main]
async fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").await.unwrap();
    loop {
        let (stream, _) = listener.accept().await.unwrap();
        tokio::spawn(async move { handle_connection(stream).await; });
    }
}
```

- 单线程 async 可并发大量连接；详见第 08/09 章实战
