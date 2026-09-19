+++
title = "内存安全"
date = 2026-09-19T12:00:00+08:00
weight = 19
type = "docs"
description = "18 种语言的内存安全对照：内存模型与所有权、安全边界、安全保证与逃逸通道、常见问题与检测工具"
isCJKLanguage = true
draft = false
+++

# 内存安全：18 种语言对照

内存安全不是"有没有垃圾回收"这么简单的问题，它由三层东西叠起来：**内存怎么分配和释放**（手动、引用计数、追踪式 GC、编译期所有权）、**哪些操作一旦写错就不再是"错误"而是"未定义行为"**（越界、悬垂、数据竞争）、以及**语言把保证做到哪一步、又留了哪些官方的逃逸通道**（`unsafe`、FFI、反射、C 扩展）。本页按这四层组织：先看**内存模型与所有权**，再看**安全边界**里各语言对 UB 的定义差异，然后是**安全保证与逃逸通道**，最后是**常见问题与检测工具**。各语言最根本的分歧在于：C 与 C++ 把内存完全交给程序员，Rust 用编译期所有权把大部分检查提前到编译期，Zig 把安全检查做成可切换的构建模式，而 Java、C#、Go、Swift、Dart、JavaScript 把保证放在运行时，Python、Ruby、PHP、Lua、R、Julia 则依靠"错误的操作抛异常"这一层薄薄的运行时约定。

## 内存安全

**一页速览**

| 语言 | 内存管理机制 | 安全保证层级 | 逃逸通道与关键陷阱 |
| --- | --- | --- | --- |
| Rust | 编译期所有权 + 借用检查，无 GC | 编译期（safe Rust 保证内存与线程安全） | `unsafe` 块把责任交回程序员；Miri 可查 UB |
| Swift | ARC 引用计数，编译器插入 retain/release | 编译期类型检查 + 运行时检查 + ARC | `unowned` 目标先死即崩溃；循环引用必须用 `weak` 打断 |
| Go | 并发三色标记清除 GC + 逃逸分析 | 运行时（safe Go 内存安全） | 数据竞争不等于内存不安全，但只有 `-race` 查得到；`unsafe.Pointer` 一用就没保证 |
| Python | 引用计数 + 循环 GC | 运行时（C 层错误可崩进程） | `ctypes` 与 C 扩展越界；free-threading 只是可选构建 |
| Kotlin | JVM 分代 GC，按可达性回收 | 运行时（JVM 没有 UB 概念） | JNI 边界、`Unsafe`、反射 `setAccessible` |
| Java | JVM 分代 GC + G1/ZGC/Shenandoah | 运行时（除 JNI 与 `Unsafe` 外无 UB） | JNI、`sun.misc.Unsafe`、反射绕过 `private` |
| C++ | 手动 `new`/`delete` + RAII 与智能指针 | 无（UB 清单很长，靠工具与约定） | 越界、有符号溢出、严格别名、use-after-free、数据竞争 |
| C | 手动 `malloc`/`free` | 无（UB 清单与 C++ 同源） | 同一份 UB 清单；违反 `restrict` 也是 UB |
| Julia | 内置追踪式 GC，可用 `@allocated` 观测 | 运行时（默认开边界检查） | `@inbounds` 与 `unsafe_load` 关掉全部检查 |
| C# | .NET 分代 GC + Server GC | 运行时（托管代码没有 UB） | `unsafe` + `fixed` + `stackalloc`；`UnsafeAccessor` 直取私有字段 |
| Dart | 分代 GC，每个 isolate 一个独立堆 | 运行时（`dart:ffi` 之外无 UB） | FFI 越界即原生内存错误，Dart 不检查 |
| R | 引用计数 + 追踪 GC，修改时复制 | 运行时（下标越界不报错） | `.C`/`.Call`/Rcpp 的原生代码没有任何保护 |
| Zig | 显式 `Allocator`，无 GC | Debug/ReleaseSafe 检查，ReleaseFast 不检查 | 切到 ReleaseFast 后越界与溢出都成了真 UB |
| Lua | 增量 / 分代 GC，全自动 | 运行时（C API 边界除外） | LuaJIT FFI 与 C API 完全无保护 |
| TypeScript | 运行时同 JavaScript（V8 分代 GC） | 编译期类型不产生任何运行时检查 | `as` 断言、`any`、装饰器全部被擦除 |
| JavaScript | V8 分代 GC（Orinoco） | 运行时（没有内存级 UB） | Wasm 与 N-API 插件都在引擎保护之外 |
| PHP | 引用计数 + 循环收集器 | 运行时（FFI 与 C 扩展除外） | FFI（7.4 起）与扩展开发直接操作原生内存 |
| Ruby | 标记-清除 GC（增量 + 分代改进） | 运行时（C 扩展与 Fiddle 除外） | `Fiddle`、C 扩展；GVL 不等于 Ruby 层线程安全 |

本表合计 18 个条目，统计口径为「语言顺序与全站固定的 18 种语言一一对应」；「安全保证层级」一列统计的是**默认构建、safe/托管代码路径下**生效的保证，不计官方明确标注为 `unsafe`、实验性或可选构建的通道（例如 Rust 的 `unsafe`、Zig 的 ReleaseFast、Python 的 free-threading、Ruby 的 Ractor）。

### 内存模型与所有权

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 是唯一把内存所有权写进类型系统的语言：值有唯一的拥有者，赋值默认是 move 而不是拷贝，借用由生命周期在编译期核对，运行时不带 GC 也不带引用计数。它属于编译期静态保证这一类，最该先知道的是"默认 move + 借用检查"这两条规则，其余智能指针都是在这两条规则上做出来的受控例外。

```rust
use std::cell::RefCell;
use std::rc::Rc;

fn take(s: String) -> usize { s.len() } // 取得所有权，函数结束时释放

fn main() {
    let s = String::from("hi");
    let n = take(s);
    // println!("{s}");                 // 🛑 编译错误：s 已被 move
    println!("{n}");                     // 2

    let rc = Rc::new(RefCell::new(1));   // Rc + RefCell：共享 + 内部可变性
    let rc2 = Rc::clone(&rc);
    *rc2.borrow_mut() += 41;
    println!("{} {}", rc.borrow(), Rc::strong_count(&rc)); // 42 2

    let boxed = Box::new([0u8; 4]);      // Box：独占的堆分配
    println!("{}", boxed.len());         // 4
}
```

`Box<T>` 是唯一拥有堆数据的指针，离开作用域就释放；`Rc<T>` 与 `Arc<T>` 是共享所有权的引用计数（单线程 / 多线程），`RefCell<T>` 与 `Mutex<T>` 提供内部可变性（单线程 / 多线程）。组合规则是固定的：单线程共享可变用 `Rc<RefCell<T>>`，多线程共享可变用 `Arc<Mutex<T>>`，二者都不能裸着用，因为 `Rc` 不是 `Send`、`RefCell` 不是 `Sync`。最容易踩的坑是借用冲突在编译期就报错而不是运行时，`borrow_mut()` 与 `borrow()` 同时存活会 panic，所以内部可变性要尽量缩到最小的一段作用域里。

布局与驻留方面，Rust 结构体默认是 `#[repr(Rust)]`，字段顺序由编译器重排以节省空间，需要稳定 ABI 时写 `#[repr(C)]`，`size_of`/`align_of` 能读到实际尺寸与对齐。`String` 是 UTF-8 的堆缓冲加长度与容量，`&str` 是带长度的胖指针，字符串字面量放在只读数据段并不做运行期驻留。

📘 [Rust · 所有权](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的堆对象由 ARC 在编译期插入 `retain`/`release` 调用管理，引用计数降到零就立即析构，没有单独的 GC 线程；结构体、枚举、元组是值语义，类实例是引用语义。它属于编译期插入代码加运行时检查的混合模型，最该先知道的是"类是引用、结构体是值"以及循环引用必须手动打破。

```swift
final class Node {
    let id: Int
    var next: Node?
    weak var owner: Node?            // weak 不增加引用计数，避免循环引用
    init(_ id: Int) { self.id = id; print("init \(id)") }
    deinit { print("deinit \(id)") }
}

func demo() {
    let a = Node(1)                  // init 1
    let b = Node(2)                  // init 2
    a.next = b                       // strong：b 的 RC 变成 2
    b.owner = a                      // weak：a 的 RC 仍是 1
    print("scope end")               // scope end
}
demo()                               // a 先释放 → deinit 1；a.next 随之释放 b → deinit 2

struct Point { var x: Int; var y: Int }   // 值语义
var p = Point(x: 1, y: 2)
var q = p
q.x = 9
print(p.x, q.x)                      // 1 9
```

`weak` 必须声明为 `Optional` 并且在目标释放后自动变 `nil`，`unowned` 则是"我保证它活着"的非拥有引用，目标先死再访问就是崩溃。Objective-C 时代需要手动 `retain`/`release`，或者用 `__weak`/`__unsafe_unretained`，Swift 把这套东西统一成了 `weak`/`unowned`，并把 ARC 的插入交给编译器。判断该用哪个的经验规则是：父指向子是强引用，子回指父用 `weak`；能保证"子不晚于父死亡"的场合才用 `unowned`。

布局上结构体的字段顺序与填充由编译器决定，`MemoryLayout<T>.size`、`.stride`、`.alignment` 是查询入口。字符串是值类型且有短字符串优化：不超过 15 个 UTF-8 字节的内容直接内联在变量里，不进堆，所以大量小字符串不会带来分配开销。

📘 [Swift · 自动引用计数](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/automaticreferencecounting/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的堆由并发的三色标记清除 GC 管理，编译器通过逃逸分析决定变量放栈还是放堆，`struct` 是值语义而 `slice`、`map`、`chan`、`func` 是引用语义的描述符。它属于运行时保证这一类，最该先知道的是"切片是一个包含指针、长度、容量的描述符"，这决定了切片赋值后底层数组仍然共享。

```go
package main

import "fmt"

type Point struct{ X, Y int } // 值语义：赋值即拷贝

func modify(p Point) { p.X = 100 } // 改的是副本

func main() {
	p := Point{1, 2}
	modify(p)
	fmt.Println(p.X) // 1   值语义

	s := make([]int, 3, 10) // slice 是「指针 + len + cap」的描述符
	t := s                  // 拷贝描述符，底层数组共享
	t[0] = 9
	fmt.Println(s[0], len(s), cap(s)) // 9 3 10

	u := append(s, 4) // cap 够，复用底层数组
	u[0] = 7
	fmt.Println(s[0], u[0]) // 7 7  ⚠️ 仍共享

	m := map[string]int{"a": 1} // map 是引用类型
	n := m
	n["a"] = 2
	fmt.Println(m["a"]) // 2
}
```

GC 用 `GOGC`（默认 100，表示堆增长到上次存活量的两倍时触发）和 `GOMEMLIMIT` 调，后者是软上限，用来防止容器里 OOM。逃逸分析可以直接观察：`go build -gcflags='-m'` 会打印 `escapes to heap` 之类的判断，理解它就能避免不必要的堆分配。最常见的陷阱是 `append` 的复用语义——两个切片共享底层数组时改一个会影响另一个，需要真正独立就 `slices.Clone` 或者三索引切片 `s[:n:n]`。数组、结构体是值语义，切片、map、channel 是引用语义，指针和接口也都是可以带类型的引用。

布局与驻留方面，结构体字段按各自对齐要求排列，`unsafe.Alignof`/`Offsetof`/`Sizeof` 能读到具体数值，空结构体大小为 0。字符串是不可变的“指针 + 长度”，字面量位于只读数据段，Go 不做运行期字符串驻留，所以两个内容相同的字符串并不保证共享底层内存。

📘 [Go · 切片：用法的陷阱](https://go.dev/blog/slices-intro)

{{% /tab %}}

{{% tab header="Python" %}}

CPython 的对象生命周期由引用计数主导，引用计数归零立即回收，另有一个循环 GC 专门处理容器之间的环；变量名只是指向对象的绑定，不存在值语义的容器。它属于运行时保证这一类，最该先知道的是"引用计数 + 循环 GC 是两套机制"，环里的对象只有等循环 GC 跑起来才会被回收。

```python
import gc
import sys

a = []
print(sys.getrefcount(a))          # 2   变量 a 本身 + getrefcount 的参数

class Node:
    def __init__(self):
        self.other = None
    def __del__(self):
        print("collected")

gc.collect()                       # 先清一次，让计数从稳定状态开始
cycle = Node()
cycle.other = cycle                # 循环引用：引用计数永远不归零
del cycle                          # 只减一次计数，对象仍被自己引用
print(gc.collect())                # collected / 1   ← 只有循环 GC 能回收它
print(gc.isenabled(), gc.get_threshold())   # True (2000, 10, 10)
```

`sys.getrefcount` 的参数本身会临时加一次计数，所以看到的值总比"真实引用数"多 1，调它的时候要记住这一点。`gc` 模块管的是环，`gc.collect()` 的返回值是这一轮回收到的不可达对象数；`gc.freeze()` 在 fork 之前冻结已有对象，能显著减少写时复制。3.13 起提供了实验性的 free-threading 构建（`--disable-gil`，用 `sys._is_gil_enabled()` 判断运行时状态，用 `sysconfig.get_config_var("Py_GIL_DISABLED")` 判断构建），3.14 按 PEP 779 把它提升为官方支持的**可选**构建，默认构建仍然带 GIL；free-threading 下引用计数变成偏向式/每线程计数，对象通常活得更久、内存占用也更高。

布局与驻留方面，`sys.getsizeof` 给的是对象自身开销（不含它引用的对象），`__slots__` 去掉实例 `__dict__` 能显著省内存。CPython 会把看起来像标识符的短字符串字面量在编译期驻留，`sys.intern()` 可以显式把运行期字符串放进驻留表，之后相同内容的字符串是同一个对象。

📘 [Python · gc 模块](https://docs.python.org/3/library/gc.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 编译到 JVM（或 Native、JS），对象由 JVM 的分代 GC 按可达性回收，语言本身不提供所有权、借用或生命周期标注。它属于运行时保证这一类，最该先知道的是"引用语义 + 可达性回收"，以及 `data class` 的 `equals` 是值比较而 `===` 才是身份比较。

```kotlin
class Node { var next: Node? = null }

data class Point(val x: Int, val y: Int)

@JvmInline
value class Meters(val v: Double)   // 值类：多数场景不装箱

fun main() {
    val a = Node()
    val b = Node()
    a.next = b
    b.next = a                       // ⚠️ 循环引用：可达性分析照样回收
    println(a === b)                 // false   === 是身份比较

    val p = Point(1, 2)
    println(p == Point(1, 2))        // true    data class 按值比较
    println(p === Point(1, 2))       // false   仍是不同对象

    val m: Meters = Meters(1.0)      // 非空值类：通常是未装箱的 Double
    val nullable: Meters? = Meters(2.0)   // 可空值类必须装箱
    println("$m $nullable")          // Meters(v=1.0) Meters(v=2.0)
    println(Runtime.getRuntime().maxMemory() > 0)   // true
}
```

`value class`（旧写法 `inline class`）用来给 `Double`、`String` 这类单字段包装类型去掉装箱开销，但一旦放进集合、变成可空类型或者用到泛型，装箱还是会回来。`data class` 生成的 `equals`/`hashCode` 只看主构造参数，这点和 Java 的 `record` 类似。Kotlin/Native 用的是另一套 GC（基于追踪，旧版还有过对象子图所有权模型，新版已统一为追踪式），所以同一段代码在 JVM 与 Native 上的内存行为并不完全一致。

布局仍然由 JVM 决定：对象有对象头、字段按 8 字节对齐，`@JvmField` 与 `@JvmInline` 会影响实际布局，用 JOL 可以精确查看。字符串字面量放在 class 常量池里天然驻留，`"a" + "b"` 在编译期折叠，运行期要显式驻留就调 `intern()`。

📘 [Kotlin · 值类](https://kotlinlang.org/docs/inline-classes.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的对象全部分配在堆上，由分代 GC 按可达性回收，局部变量放栈上但只能是基本类型与引用；语言规范里根本没有"未定义行为"这个概念。它属于运行时保证这一类，最该先知道的是"分代假设"以及 G1、ZGC、Shenandoah 这几个收集器的定位差别。

```java
public class Mem {
    static final class Node { Node next; }

    record Point(int x, int y) {}          // 值语义的载体，但实例仍是引用

    public static void main(String[] args) {
        Node a = new Node(), b = new Node();
        a.next = b; b.next = a;            // ⚠️ 循环引用：可达性分析照样回收
        a = null; b = null;
        System.gc();
        System.out.println(Runtime.getRuntime().maxMemory() > 0);   // true

        Point p = new Point(1, 2);
        int[] xs = {1, 2, 3};
        System.out.println(p.x() + p.y());  // 3
        System.out.println(xs.length);      // 3   数组自带长度与边界检查
    }
}
```

堆按代划分：年轻代放朝生夕死的对象（Eden + 两个 Survivor），老年代放活得久的对象，绝大多数对象在年轻代就死掉，所以 `Minor GC` 便宜、`Full GC` 昂贵。G1 面向大堆、按 Region 增量回收并可以设停顿目标；ZGC 与 Shenandoah 是并发收集器，目标是把停顿压到毫秒级，代价是更多的并发开销与屏障。`System.gc()` 只是建议，`-Xlog:gc` 才能看到真实回收日志。逃逸分析后 JIT 可以把未逃逸的对象拆散到栈上（标量替换），这是"对象一定在堆上"的唯一例外，但它是 JVM 的实现优化，不是语言保证。

布局方面对象由“对象头 + 字段”组成并按 8 字节对齐，开启压缩指针后引用宽度是 4 字节。字符串字面量在 class 常量池里驻留，`new String("abc")` 会另建一个不驻留的对象，`intern()` 是显式驻留入口，判断“是不是同一个字符串”应该用 `equals` 而不是 `==`。

📘 [Java · 内存管理](https://docs.oracle.com/en/java/javase/25/gctuning/index.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 把内存完全交给程序员：`new`/`delete` 手动配对，RAII 把释放绑在对象析构上，`unique_ptr`、`shared_ptr`、`weak_ptr` 是标准库给 RAII 提供的三个智能指针。它属于"没有安全保证"这一类，最该先知道的是"栈对象自动析构、堆对象要有人负责"这条分工。

```cpp
#include <bit>
#include <cstdio>
#include <iostream>
#include <memory>

struct Widget {
    int id;
    explicit Widget(int i) : id(i) { std::cout << "ctor " << id << "\n"; }
    ~Widget() { std::cout << "dtor " << id << "\n"; }
};

int main() {
    {
        std::unique_ptr<Widget> up = std::make_unique<Widget>(1); // ctor 1
        std::cout << up->id << "\n";       // 1
        // std::unique_ptr<Widget> copy = up;      // 🛑 独占所有权，不能拷贝
        std::unique_ptr<Widget> moved = std::move(up);
        std::cout << (up == nullptr) << "\n";      // 1
    }                                      // dtor 1（离开作用域自动释放）

    std::shared_ptr<Widget> sp = std::make_shared<Widget>(2);  // ctor 2
    std::weak_ptr<Widget> wp = sp;         // weak 不增加计数，用来打破循环引用
    std::cout << sp.use_count() << "\n";   // 1
    sp.reset();                            // dtor 2
    std::cout << wp.expired() << "\n";     // 1
}
```

`unique_ptr` 是零开销的独占所有权，可以只移动不能拷贝；`shared_ptr` 用控制块里的原子计数共享所有权，代价是原子操作与一份额外控制块；`weak_ptr` 只观察不拥有，用 `lock()` 原子地提升为 `shared_ptr`，专门用来断开互相持有的环。`make_unique`/`make_shared` 比裸 `new` 更安全，因为异常安全与（对 `shared_ptr` 而言）控制块合并都在里面处理掉了。数组要用 `std::vector`、`std::string`、`std::array` 这类 RAII 容器，裸 `new[]` 只在这些容器内部出现。

布局与字符串方面，`alignof`/`alignas` 控制对齐，`offsetof` 读偏移，`std::string` 普遍实现短字符串优化（阈值由实现决定，常见是 15 或 22 字节）所以小字符串不分配堆内存。字符串字面量是否合并（相同内容是否同一地址）是实现定义的，不能依赖。

📘 [cppreference · 智能指针](https://en.cppreference.com/w/cpp/memory)

{{% /tab %}}

{{% tab header="C" %}}

C 只有 `malloc`/`calloc`/`realloc`/`free` 这一组手动分配接口，没有析构函数也没有所有权概念，堆上的每个字节都由程序员负责。它属于"完全没有安全保证"这一类，最该先知道的是"分配大小按字节算、释放后指针不会自动置空"。

```c
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Node { int v; struct Node *next; };

int main(void) {
    int *p = malloc(sizeof(int) * 4);      /* 手动分配，字节数自己算 */
    if (!p) return 1;
    p[0] = 1; p[3] = 4;
    printf("%d %zu\n", p[3], sizeof(p));   /* 4 8   sizeof(指针) 不是 sizeof(数组) */
    free(p);                               /* 必须手动释放 */

    struct Node *n = calloc(1, sizeof *n); /* calloc 清零；sizeof *n 免写类型 */
    printf("%d %p\n", n->v, (void *)n->next);  /* 0 0x0 */
    free(n);

    char *leak = malloc(8);                /* ⚠️ 忘记 free：Valgrind 会报 definitely lost */
    (void)leak;
    return 0;
}
```

`calloc` 会把内存清零而 `malloc` 不会，`realloc` 可能搬动内存所以旧的指针立刻失效，`free(NULL)` 是合法的空操作但 `free` 同一块内存两次是未定义行为。指针失去指向之后不会自动变成 `NULL`，所以"置空"这个动作必须自己写，这也是 use-after-free 最常见的来源。C23 仍然没有改变这套模型，`nullptr`、`constexpr`、`typeof` 这些新增特性只是让代码更清楚，不会替你检查内存。

布局方面 `_Alignof`、`alignas`（C23 起 `alignof` 是关键字）与 `offsetof` 是标准工具，`malloc` 保证返回适合任何基本类型的对齐。字符串字面量是否被合并是实现定义的，`char *p = "abc";` 指向只读内存，改它就是未定义行为；C 也没有字符串驻留机制。

📘 [cppreference · C 内存管理](https://en.cppreference.com/w/c/memory)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的堆对象由一个内置的追踪式 GC 管理，数值类型与不可变结构体默认内联在栈或数组里，只有真正需要引用的东西才上堆；`@allocated` 与 `@time` 是观察分配的入口。它属于运行时保证这一类，最该先知道的是"类型不稳定会导致大量装箱分配"。

```julia
function churn(n)
    acc = 0
    for i in 1:n
        acc += sum([i, i])          # 每次迭代都在堆上分配一个 Vector
    end
    return acc
end

println(churn(3))                   # 6
println(@allocated(churn(3)) > 0)   # true   这次调用分配的字节数大于 0

Base.GC.gc()                        # 手动触发一次完整回收
println(Base.gc_num().pause >= 0)   # true   当前进程累计的 GC 暂停次数

# ⚠️ 顶层全局变量类型不稳定：x 的类型是 Any，循环里读写都要装箱
x = 1
f() = x + 1
println(f())                        # 2
println(typeof(x))                  # Int64（值本身有类型，但绑定的类型是 Any）
```

GC 是分代式的标记清除，`--heap-size-hint` 可以在内存接近上限时更早、更积极地回收，适合容器环境。真正影响性能的是类型稳定性：函数内部如果某个变量在不同分支上会是不同类型（`Union{Int,Float64}` 甚至 `Any`），编译器就无法生成专用代码，结果就是每次迭代都装箱、分配，GC 压力成倍上升；`@code_warntype` 用红色高亮不稳定点。全局变量默认是 `Any` 且非 `const`，在热点循环里读写全局变量是最经典的性能陷阱，改用 `const` 或者把值当参数传进去即可。

布局方面 `sizeof`、`fieldoffset`、`isbitstype` 决定一个值会不会被内联进数组（`isbitstype` 为真的类型没有指针、连续存放，是性能关键）。`String` 是不可变字节序列，`Symbol` 是驻留的，所以拿 `Symbol` 做键比用 `String` 比较更快。

📘 [Julia · 内存与 GC](https://docs.julialang.org/en/v1/devdocs/gc/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的引用类型由 .NET 分代 GC 按可达性回收，`struct`、`Span<T>`、`stackalloc` 走栈或内联存储，`unsafe` 上下文里的指针由程序员负责。它属于运行时保证这一类，最该先知道的是"引用类型与值类型的分配位置不同"，以及 `IDisposable` 管的是非托管资源而不是内存。

```csharp
using System;

class Node { public Node? Next; }

struct Point { public int X, Y; }     // 值语义，通常是栈分配或被内联

sealed class Resource : IDisposable {
    public void Dispose() => Console.WriteLine("disposed");   // 确定性清理
}

class Program {
    static void Main() {
        var a = new Node();
        var b = new Node();
        a.Next = b; b.Next = a;                     // 循环引用：可达性分析照样回收
        Console.WriteLine(GC.GetGeneration(a));     // 0   第 0 代
        Console.WriteLine(GCSettings.IsServerGC);   // False（控制台默认工作站 GC）

        var p = new Point { X = 1, Y = 2 };
        var q = p; q.X = 9;                         // struct 赋值是拷贝
        Console.WriteLine($"{p.X} {q.X}");          // 1 9

        using (var r = new Resource()) { }           // disposed
        GC.Collect();                                // 只是建议，不保证立刻回收
        Console.WriteLine(GC.GetTotalMemory(false) > 0);   // True
    }
}
```

GC 分三代：第 0 代最小最频繁，第 1 代是缓冲区，第 2 代放长寿对象并配合大对象堆（LOH，85 KB 以上的对象直接进 LOH，默认不压缩）。Server GC 为每个 CPU 核分配独立堆和收集线程，适合吞吐型服务端，用 `<ServerGarbageCollection>true</ServerGarbageCollection>` 或 `DOTNET_gcServer=1` 打开。`struct` 只有在逃逸到需要引用的位置（装箱、字段、`async` 状态机）时才会被搬到堆上，所以"值类型一定在栈上"是不准确的。`IDisposable` 与 `using` 处理的是文件句柄、原生内存这些 GC 管不到的东西，写终结器时要用 `Dispose(bool)` 模式避免重复释放。

布局方面 `Marshal.SizeOf` 与 `Unsafe.SizeOf<T>()` 给出尺寸，`[StructLayout(LayoutKind.Sequential)]`/`Explicit` 控制与原生互操作时的排布。字符串驻留由驻留池负责，字面量自动进池，运行期用 `string.Intern` 显式驻留，`ReferenceEquals` 才能用来判断“是不是同一个字符串对象”。

📘 [MS Learn · .NET 垃圾回收](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的对象由分代 GC 管理，而且是**每个 isolate 一个独立的堆**，两个 isolate 之间不共享任何可变对象，只能靠消息传递。它属于运行时保证这一类，最该先知道的是"isolate 之间零共享"这条设计，它把数据竞争从语言层面删掉了。

```dart
class Node {
  Node? next;
}

void main() {
  final a = Node(), b = Node();
  a.next = b;
  b.next = a;                              // ⚠️ 循环引用：可达性分析照样回收
  print(a.next != null);                   // true

  final list = [1, 2, 3];                  // List 是引用类型
  final copy = List.of(list);              // 显式拷贝，否则共享同一个对象
  copy[0] = 9;
  print('$list $copy');                    // [1, 2, 3] [9, 2, 3]

  final w = WeakReference<Node>(a);        // 弱引用：不阻止回收
  print(w.target != null);                 // true

  final ints = Int32List(3);               // 类型化数据：连续内存，无装箱
  ints[0] = 7;
  print(ints[0]);                          // 7
  print(identityHashCode(a) != 0);         // true
}
```

新生代用 Scavenger 半空间复制，老生代用标记-清除加标记-整理，GC 在分配达到阈值时启动；因为每个 isolate 都有独立堆，收集可以在不暂停其他 isolate 的情况下并行进行。`WeakReference` 与 `Finalizer` 是弱引用通道；`NativeFinalizer` 用来给 `dart:ffi` 分配的原生内存挂终结器，这是把原生资源接进 GC 的唯一正路。需要共享大量数据时用 `TransferableTypedData` 做零拷贝转移而不是拷贝，`Isolate.run` 是 2.19 之后最简单的入口。

布局上 Dart 对象的具体排布不是语言契约，需要知道原生侧尺寸时用 `dart:ffi` 的 `sizeOf<T>()`；编译时常量字符串会被规范化，所以 `identical("a", "a")` 为真，而运行期拼出来的字符串不参与规范化。Dart 3.3 起的 `extension type` 是纯编译期的静态包装：它在运行期被完全擦除，`List<E>` 与 `List<R>` 在运行期是同一个类型，所以它带来类型安全却不增加任何内存开销。

📘 [Dart · isolate 与并发](https://dart.dev/language/isolates)

{{% /tab %}}

{{% tab header="R" %}}

R 的向量在语义上是值：赋值不复制，但任何一次修改都会触发"修改时复制"（copy-on-modify），背后由引用计数加追踪式 GC 撑着。它属于运行时保证这一类，最该先知道的是"看起来是引用语义的环境（environment）才是真正的引用类型，其余都是值"。

```r
u <- 1:3
v <- u
v[1] <- 99L                       # 触发 copy-on-modify：u 不变
print(u)                          # [1] 1 2 3
print(v)                          # [1] 99  2  3

tracemem(v)                       # 打印 v 的内存地址
w <- v                            # w 与 v 共享同一份数据
w[2] <- 0L                        # tracemem[0x... -> 0x...]：这里发生了复制
untracemem(w)

e <- new.env(parent = emptyenv()) # environment 是引用语义：改的就是同一份
e$big <- 1:1e6                    # 闭包环境把大对象钉在内存里
f <- function() length(e$big)
print(f())                        # [1] 1e+06
print(rownames(gc()))             # [1] "Ncells" "Vcells"（使用量/触发阈值/上限）

gcinfo(TRUE)                      # 之后每次 GC 都会打印统计（返回值是上一次的标记）
rm(e); invisible(gc())            # 大对象这时才可能被回收
gcinfo(FALSE)
```

`gc()` 返回一个矩阵，行是 Ncells（cons 单元）与 Vcells（向量单元），列给出 `used`、`gc trigger` 与最大使用量（设置过上限时还多一列 `limit`），是判断"内存是不是被谁钉住了"的第一手材料；`gcinfo(TRUE)` 只是打开"每次 GC 打印统计"的开关（它返回上一次的标记值，不是计数），要看具体哪一行在分配得靠 `Rprofmem()`、`profmem` 与 `lobstr`。R 的 GC 是标记-清除，写屏障把老年代指向新生代的引用记录下来。函数环境是引用语义，这既是闭包能工作的原因，也是内存泄漏的来源：一个环境被闭包捕获后，环境中所有对象都会活着，直到闭包本身被回收。

布局与驻留在 R 里同样重要：向量是连续内存，属性（`attributes`）与 ALTREP 会影响真实占用，`lobstr::obj_size` 比 `object.size` 更接近实际。字符串由全局字符串池缓存，内容相同的字符串共享同一个 CHARSXP，所以大量重复字符串不会成倍占用内存。

📘 [R · gc 与内存管理](https://stat.ethz.ch/R-manual/R-devel/library/base/html/gc.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有 GC、没有所有权检查，也没有 `new` 关键字，所有堆分配都必须显式传一个 `std.mem.Allocator`，由调用点决定内存从哪来、什么时候还。它属于"安全模式可选"这一类，最该先知道的是"分配器是参数不是全局状态"，以及 `defer`/`errdefer` 是配平释放的主要工具。

```zig
const std = @import("std");

pub fn main() !void {
    var gpa_state = std.heap.DebugAllocator(.{}){};   // 0.15 起 DebugAllocator 是正式名
    defer _ = gpa_state.deinit();                      // 退出时报告泄漏
    const gpa = gpa_state.allocator();

    const buf = try gpa.alloc(u8, 8);                  // 显式传分配器
    defer gpa.free(buf);                               // 显式释放

    var list: std.ArrayList(u32) = .empty;             // 0.15 的 ArrayList 是非托管版本
    defer list.deinit(gpa);                            // 方法签名里带着 gpa
    try list.append(gpa, 1);
    try list.append(gpa, 2);
    std.debug.print("{d}\n", .{list.items.len});       // 2

    var arena = std.heap.ArenaAllocator.init(gpa);
    defer arena.deinit();                              // 一次性全部释放
    const hello = try arena.allocator().dupe(u8, "hi");
    std.debug.print("{s}\n", .{hello});                // hi

    _ = allocThenFail(gpa) catch {};
}

fn allocThenFail(gpa: std.mem.Allocator) !void {
    const p = try gpa.create(u32);
    errdefer gpa.destroy(p);        // 只在错误返回路径上执行
    p.* = 1;
    return error.Boom;
}
```

Zig 0.15 把 `std.ArrayList` 改成了非托管版本：结构体里不再保存 allocator，`append`、`deinit`、`clone` 这些方法都要把分配器当第一个参数传进去，`std.ArrayListUnmanaged` 这个名字已经并入，老的托管版本搬到了（已废弃的）`std.array_list.Managed`。`ArenaAllocator` 适合"整个阶段一起释放"的场景，`std.heap.DebugAllocator`（旧名 `GeneralPurposeAllocator`）会做泄漏检测与释放后使用检测，代价是慢；官方推荐的组合是 Debug 与 ReleaseSafe 用它、ReleaseFast 与 ReleaseSmall 换 `std.heap.smp_allocator`。⚠️ Zig 没有库层面的"默认分配器"：`std.heap.page_allocator` 只是兜底，任何分配都要由调用方显式传入 allocator，所以这条组合是约定而不是自动切换的开关。

布局由 `@sizeOf`、`@alignOf`、`@offsetOf` 查询，普通 `struct` 的字段顺序可以重排，需要稳定内存布局时用 `extern struct`（C ABI）或 `packed struct`（无填充）。字符串就是 `[]const u8`，字面量在只读数据段，Zig 不做驻留，相等要显式比较内容。

📘 [Zig · 分配器](https://ziglang.org/documentation/master/#Choosing-an-Allocator)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的所有值都由一个增量或分代模式的 GC 全自动管理，表、函数、协程、userdata 都是对象，变量只是引用。它属于运行时保证这一类，最该先知道的是"默认是增量模式、需要时再切到分代模式"，以及弱表是唯一能表达"不阻止回收"的手段。

```lua
-- 增量 / 分代两种模式；默认是增量模式
print(collectgarbage("count") > 0)      -- true    当前占用（KB）
collectgarbage("collect")                -- 手动跑一次完整回收
print(collectgarbage("isrunning"))       -- true
print(collectgarbage("generational"))    -- incremental   切到分代，返回切换前的模式
print(collectgarbage("incremental"))     -- generational  切回增量，返回切换前的模式

local weak = setmetatable({}, { __mode = "v" })   -- 弱值表：值可被回收
local obj = { name = "temp" }
weak[1] = obj
obj = nil
collectgarbage("collect")
print(weak[1])                           -- nil     已被回收

local res = setmetatable({}, { __gc = function() print("finalized") end })
res = nil
collectgarbage("collect")                -- finalized
```

增量模式每次只做一小步标记-清除，用 pause、step multiplier、step size 三个参数调节；分代模式频繁做只遍历新对象的 minor 收集，必要时才升级为 major 收集，用 minor multiplier、minor-major multiplier 与 major-minor multiplier 三个乘数控制节奏。弱表通过 `__mode` 声明，`"k"` 是弱键表（键可被回收，常用于缓存）、`"v"` 是弱值表、`"kv"` 两者都弱。`__gc` 元方法必须在把表设成元表**之前**就写好，否则不会生效；终结器里让对象重新可达会"复活"它，这类代码极难推理，能用弱表就别用终结器。5.5 起 `global` 变成保留字（必须显式声明全局变量），for 的控制变量也变成只读，语言的这类收紧减少了意外共享状态。

布局与驻留方面，表的内部由数组部分与哈希部分组成，连续整数键走数组、其余走哈希，构造时预分配尺寸能明显减少重哈希。长度不超过 40 字节的短字符串会被自动驻留，相等判断因此退化成指针比较；更长的字符串不驻留，比较要逐字节来。

📘 [Lua 5.5 · 垃圾回收](https://www.lua.org/manual/5.5/manual.html#2.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 对运行时内存行为没有任何影响：编译产物就是 JavaScript，由 V8 的分代 GC 管理，唯一的区别是类型信息全部在编译期被擦除。它属于编译期静态检查这一类，最该先知道的是"类型只在编译期存在"，`as` 不产生任何代码、也不做任何检查。

```typescript
// TypeScript 不改变运行时：内存模型与 JavaScript 完全一致
class Node {
  next: Node | null = null;
}

const a = new Node();
const b = new Node();
a.next = b;
b.next = a;                            // ⚠️ 循环引用：标记清除照样回收
console.log(Object.keys(a).length);     // 1

const weak = new WeakRef(b);            // 弱引用
console.log(weak.deref() === b);        // true

// 类型只在编译期：断言不会生成任何检查代码
const list: number[] = [1, 2, 3];
const asString = list as unknown as string;
console.log((asString as unknown as number[]).length);   // 3

// 运行时能拿到的是擦除后的构造函数名
console.log(a.constructor.name);        // Node
console.log(typeof (a as { x: number }).x);   // undefined（属性不存在也不会报错）
```

`readonly`、`private`、`as const`、装饰器元数据全都止步于编译期，把编译产物加载到浏览器里之后没有任何东西保护它们。真正需要"运行时类型"就要自己写类型守卫（`typeof`、`Array.isArray`、`instanceof`）或者上 `zod` 这类校验库。结构子类型（structural typing）带来的另一个错觉是"两个形状相同的类型可以互换"，但类私有字段（`#x`）是唯一带运行时语义的可见性标记，它在编译产物里是真的私有槽位。

布局与驻留完全由 JavaScript 引擎决定，TypeScript 的类型与 `readonly` 不影响任何内存排布。V8 用隐藏类（hidden class）与内联缓存优化属性访问，所以“一开始就把所有字段写进构造函数”比运行期陆续增删属性更快，`--allow-natives-syntax` 下的 `%DebugPrint` 能看到隐藏类。

📘 [TypeScript · 类型擦除与 everyday types](https://www.typescriptlang.org/docs/handbook/2/everyday-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的对象全部由 V8 的分代 GC 管理，没有手动释放、没有指针、也没有内存级未定义行为，越界读数组只会给你 `undefined`。它属于运行时保证这一类，最该先知道的是"引用可达性决定回收"，循环引用从来不是问题，而闭包与全局缓存才是真正的泄漏源。

```javascript
// V8 分代 GC（Orinoco）：新生代 Scavenger + 老生代 mark-sweep / mark-compact
class Node {}
let a = new Node();
let b = new Node();
a.next = b;
b.prev = a;                            // ⚠️ 循环引用：按可达性回收，不是引用计数
console.log(Object.keys(a).length);    // 1

const ref = new WeakRef(b);            // 弱引用：不阻止回收
console.log(ref.deref() === b);        // true

const reg = new FinalizationRegistry((held) => console.log("freed", held));
reg.register(b, "node-b");             // 回收后异步回调，时机不确定
console.log(reg instanceof FinalizationRegistry);   // true

a = null; b = null;                    // 解除强引用
console.log(process.memoryUsage().heapTotal > 0);   // true
console.log(typeof globalThis.gc);     // undefined（要 node --expose-gc 才有）
```

V8 的堆分新生代与老生代，新生代用 Scavenger 做半空间复制，经历两次回收还存活的对象晋升到老生代，老生代用标记-清除加标记-整理，并且大量步骤与主线程并发/并行执行（Orinoco 项目）。`WeakMap`、`WeakSet`、`WeakRef`、`FinalizationRegistry` 是四条弱引用通道，其中 `WeakMap` 最适合给对象挂旁路数据（DOM 节点缓存、私有状态），因为键一死数据就自动消失。最经典的泄漏是"闭包持有 DOM 节点"和"全局缓存只增不减"，另外 `setInterval` 忘了 `clearInterval` 也会让整条引用链活着。

布局与驻留方面，V8 给每个形状相同的对象分配同一个隐藏类，属性增删会让隐藏类迁移、内联缓存失效，这是“对象形状保持一致”这一优化建议的来源。数组分为 packed 与 holey 两种内部表示，出现空洞会让访问退化；字符串是不可变的且有内部化机制，字面量天然共享。

📘 [MDN · WeakRef 与内存管理](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Memory_management)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的变量由引用计数管理，计数归零立即释放，另有一个循环收集器定期清理数组与对象之间的环；数组在语义上是值（写时复制），对象是引用。它属于运行时保证这一类，最该先知道的是"unset 只是减一次引用，环要靠 `gc_collect_cycles`"。

```php
<?php
// PHP 用引用计数 + 循环收集器；unset 只是减引用，不一定立即回收
$obj = new stdClass();
$obj->self = $obj;                 // 自引用：纯引用计数永远回收不了
unset($obj);                       // 计数不为零，对象还挂在环里

$status = gc_status();
echo ($status['runs'] >= 0) ? "ok\n" : "no\n";   // ok
echo gc_collect_cycles(), "\n";    // 1   ← 循环收集器回收了 1 个环
echo memory_get_usage() > 0 ? "mem>0\n" : "mem=0\n";   // mem>0

$a = [1, 2, 3];                    // 数组是值语义（写时复制）
$b = $a;
$b[0] = 9;
echo $a[0], $b[0], "\n";           // 19

$o1 = new stdClass();
$o2 = $o1;                         // 对象是引用语义
$o2->v = 7;
echo $o1->v, "\n";                 // 7
```

`memory_get_usage()` 给的是当前 PHP 分配器统计到的字节数，`memory_get_peak_usage()` 给峰值，配合 `memory_limit` 判断是不是快撞墙。循环收集器由 `zend.enable_gc` 控制（默认开启），触发条件是"可能的根"达到阈值（默认 10000），长驻进程（Swoole、RoadRunner、队列 worker）里手动调 `gc_collect_cycles()` 是常规操作。`unset` 只断开一个绑定，如果变量还被别处引用就什么都不会发生；对象之间的循环引用、闭包捕获 `$this`、静态属性持有大数组都是长驻进程里最典型的内存增长来源。

布局与驻留方面，每个值是一个 16 字节的 `zval`，字符串是带引用计数、长度与哈希缓存的 `zend_string`，所以对同一字符串反复取 `strlen` 或做键查找都很快。字面量与 OPcache 里的常量字符串会被驻留（interned string），长驻进程里因此不会重复分配。

📘 [PHP · 垃圾回收](https://www.php.net/manual/en/features.gc.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

MRI 用标记-清除 GC，配合增量式与分代式改进来压低停顿，所有对象都在堆上、变量都是引用，值语义要靠对象冻结或显式拷贝来模拟。它属于运行时保证这一类，最该先知道的是"标记清除能正确回收循环引用"，以及 `GC.stat` 是看堆状态的第一入口。

```ruby
# MRI 用标记-清除（增量 + 分代式改进）GC；对象都在堆上，变量都是引用
class Node
  attr_accessor :peer
end

a = Node.new
b = Node.new
a.peer = b
b.peer = a                        # ⚠️ 循环引用：标记清除照样回收
puts GC.stat[:count] >= 0         # true   GC 运行次数
puts ObjectSpace.count_objects[:TOTAL] > 0   # true

GC.compact                        # 整理堆，压缩对象（2.7 起）
puts GC.stat[:heap_allocated_pages] > 0      # true

a = b = nil
GC.start                          # 手动触发一次完整 GC
puts GC.stat[:heap_live_slots] >= 0          # true
puts GC.stat.keys.include?(:heap_allocated_pages)   # true
```

`GC.stat` 里最该看的是 `heap_live_slots`（存活对象数）、`heap_allocated_pages`（已分配的堆页）、`heap_free_slots` 与 `count`（GC 次数），`ObjectSpace.count_objects` 按类型给出对象分布，`GC.compact` 会搬动对象以消除碎片（搬动后 C 扩展里缓存的裸指针就得靠 pinning 保护）。`ObjectSpace.each_object`、`define_finalizer` 是另外两个观测与清理通道，但终结器同样会拖慢 GC。Ruby 4.0 的 GC 还把不同 size pool 的堆页改成独立增长，只在大对象页上加速清扫，长驻进程的常驻内存因此更容易压住。`ObjectSpace._id2ref` 在 4.0 起被废弃。

布局与驻留方面，MRI 的每个对象占一个 RVALUE 槽（64 位下 40 字节），不超过 23 字节的字符串会直接内联在槽里而不额外分配。`Symbol` 是驻留的（4.0 起符号表换成无锁哈希集），`-"str"` 生成冻结去重的字符串，适合当哈希键；`ObjectSpace.memsize_of` 只在 `objspace` 扩展里提供。

📘 [Ruby · GC](https://docs.ruby-lang.org/en/master/GC.html)

{{% /tab %}}

{{< /tabpane >}}

### 安全边界

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 把"内存安全"定义成一条明确的界线：safe Rust 里不会出现悬垂引用、越界读写或数据竞争，而 `unsafe` 块里的操作一旦违反契约，就和其他系统语言一样是未定义行为。它属于编译期保证这一类，最该先知道的是"`unsafe` 不是关掉检查，而是把检查责任转给写代码的人"。

```rust
fn main() {
    let v = vec![1, 2, 3];
    // println!("{}", v[3]);              // 🛑 panic: index out of bounds
    println!("{:?}", v.get(3));           // None

    let p: *const i32 = &v[0];
    let ok = unsafe { *p };               // 指针有效：这里没有 UB
    println!("{ok}");                     // 1
    // let bad = unsafe { *p.add(3) };    // 🛑 UB：越界读，Miri 会报

    let rc = std::rc::Rc::new(1);
    // std::thread::spawn(move || println!("{rc}"));  // 🛑 Rc 不是 Send
    println!("{rc}");                     // 1
}
```

越界在 safe Rust 里是 panic（`get` 这类 API 则返回 `Option`），不是 UB；`unsafe` 里的悬垂引用、别名违反（同时存在 `&mut` 与 `&`）、越界裸指针访问、数据竞争、把未初始化内存当成已初始化读，全都会落到 `unsafe` 的契约上。悬垂与生命周期在 safe Rust 里被编译器挡死（`fn dangle() -> &String { let s = String::new(); &s }` 直接编译不过），泄漏则是显式允许的：`Box::leak`、`std::mem::forget`、`Rc` 互环都会泄漏但不是 UB，Miri 会把"程序结束时仍不可达且未释放"的内存报成泄漏。数据竞争由 `Send`/`Sync` 在编译期排除——`Rc`、`RefCell`、裸指针不是 `Send`/`Sync`，共享可变状态必须走 `Arc<Mutex<T>>` 或原子类型。

📘 [Rust Reference · 未定义行为](https://doc.rust-lang.org/reference/behavior-considered-undefined.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的安全保证来自编译期类型检查、运行时前置条件（数组边界、整数溢出、强制解包）以及 ARC，一旦离开这三层进入 `UnsafePointer` 系列就退化成 C 的规则。它属于运行时保证这一类，最该先知道的是"安全的数组下标始终带检查（只有 `-Ounchecked` 才整体去掉），而 `Unsafe*` 指针的下标在 `-O` 下就只剩裸指针加法"。

```swift
let arr = [1, 2, 3]
// print(arr[3])                     // 🛑 Fatal error: Index out of range
print(arr.indices.contains(3))        // false
print(arr[0])                         // 1

arr.withUnsafeBufferPointer { buf in
    print(buf[2])                     // 3
    // print(buf[3])                  // 🛑 -O 下不检查，读到的是垃圾值
}

final class Owner { var pet: Pet? }
final class Pet { unowned var owner: Owner? }   // unowned：不增加引用计数
var o: Owner? = Owner()
let pet = Pet()
pet.owner = o!
o = nil
// print(pet.owner!)                  // 🛑 崩溃：unowned 目标已释放
print("done")                         // done
```

数组下标在 Debug 构建里越界会 `Fatal error: Index out of range`，但 `UnsafeBufferPointer` 的下标在 `-O` 下就是裸指针加法，实测能读出垃圾值而不崩溃；整数溢出默认 trap，只有 `&+`/`&*` 才回绕；强制解包 `!` 与 `try!` 失败即崩溃。悬垂问题集中在 `unowned` 与非托管指针上：`unowned` 目标先死再访问必然崩溃，`Unmanaged.passUnretained` 不增加引用计数、对象随时可能被 ARC 释放。泄漏最主要的形式是闭包捕获 `self` 造成的循环引用——在闭包里写 `[weak self]` 或者 `[unowned self]` 是标准做法；`URLSession`、`Timer`、通知中心都会强引用闭包，是线上最常见的泄漏点。Swift 6 语言模式（opt-in，SwiftPM 里 `swift-tools-version: 6.0` 起默认启用）下严格并发检查全开，跨隔离域传递的值必须满足 `Sendable`，`actor` 用串行执行消灭数据竞争，编译器把不安全的传递直接标成错误。

📘 [Swift · 内存安全](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的官方立场是清楚的两句话：Go 提供内存安全保证（没有越界、没有 use-after-free、没有指针算术），但**数据竞争是未定义行为**，需要靠 `-race` 或同步原语自己防。它属于运行时保证这一类，最该先知道的是"内存安全 ≠ 数据竞争安全"这个区分。

```go
package main

import (
	"fmt"
	"sync"
)

func main() {
	s := []int{1, 2, 3}
	// fmt.Println(s[3])              // 🛑 panic: index out of range [3] with length 3
	fmt.Println(len(s), cap(s)) // 3 3

	big := make([]byte, 1<<20)
	small := big[:10]                    // ⚠️ 仍持有整个 1 MiB 底层数组
	fmt.Println(cap(small) > len(small)) // true
	safe := big[:10:10]                  // 三索引切片：限制容量
	fmt.Println(cap(safe))               // 10

	var mu sync.Mutex
	var wg sync.WaitGroup
	counter := 0
	for i := 0; i < 100; i++ {
		wg.Add(1)
		go func() { defer wg.Done(); mu.Lock(); counter++; mu.Unlock() }()
	}
	wg.Wait()
	fmt.Println(counter) // 100   去掉 mu 就是数据竞争，-race 会报
}
```

数组与切片的越界访问、`nil` map 写入、类型断言失败都会 panic 而不是损坏内存，所以 Go 的内存安全是运行时兜底的。数据竞争则是另一回事：两个 goroutine 无同步地读写同一变量属于未定义行为，可能读到撕裂的值、也可能因为编译器重排而永久看不到更新，这不会 panic，只能靠 `go test -race`、`sync.Mutex`、`sync/atomic`、channel 或 `errgroup` 来防。泄漏在 Go 里主要是两类：**goroutine 泄漏**（往没人接收的 channel 发送、`time.Ticker` 忘了 `Stop`、`context` 没取消）与**切片持有大数组**（`big[:10]` 那种，用三索引切片或者 `slices.Clone` 解决）。悬垂不会发生，但"逻辑上不再需要却仍被引用"会让整个对象图活着。

📘 [Go · 数据竞争与内存模型](https://go.dev/ref/mem)

{{% /tab %}}

{{% tab header="Python" %}}

Python 在 Python 层没有内存级未定义行为，错误一律表现为异常；但 `ctypes`、`cffi`、C 扩展、`memoryview` 直接落到原生内存上，越界与悬垂立刻变成段错误。它属于运行时保证这一类，最该先知道的是"Python 的保证只覆盖 Python 层，C 层一进去就没有"。

```python
import sysconfig
import ctypes
import sys

xs = [1, 2, 3]
print(xs[-1])                      # 3    负索引从尾部数
try:
    xs[3]
except IndexError as e:
    print("IndexError:", e)        # IndexError: list index out of range

buf = ctypes.create_string_buffer(4)
print(ctypes.sizeof(buf))          # 4
# ctypes.memmove(buf, b"0123456789", 10)   # 🛑 越界写：C 层不检查，可能崩

print(sysconfig.get_config_var("Py_GIL_DISABLED"))   # 0  本机是默认（带 GIL）构建
print(sys._is_gil_enabled())                          # True
print(sys.version.split()[0])                         # 3.14.7
```

越界在列表、字符串、字节串上都是 `IndexError`，切片越界则是截断而不报错（`xs[1:99]` 合法），这是最容易被忽略的一处宽松。悬垂问题以"循环引用 + `__del__`"的形式出现：有 `__del__` 的环在旧版本里会进 `gc.garbage` 永不回收，正确做法是避免在 `__del__` 里引用外部对象，或者改用 `weakref` 与上下文管理器。泄漏基本都来自长驻进程里的全局缓存、`lru_cache`、事件回调注册后不解绑、`sys.modules` 里被反复 import 的模块，用 `tracemalloc` 对比两次快照定位最快。并发方面，默认构建靠 GIL 保证字节码级原子性，但 `i += 1` 这种复合操作仍会丢失更新，需要 `threading.Lock`；3.13 起可选的 free-threading 构建（3.14 起为官方支持的可选构建）去掉了 GIL，内置容器用内部锁保护并发修改，但"并发修改是否安全"官方明确说是实现描述而不是保证，应该显式加锁；同一迭代器被多线程共用会重复或漏掉元素。

📘 [Python · C 扩展与 free threading](https://docs.python.org/3/howto/free-threading-python.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 运行在 JVM 上，所以继承了"没有未定义行为"这条底线：越界抛 `IndexOutOfBoundsException`、空指针抛 `NullPointerException`、溢出静默回绕。它属于运行时保证这一类，最该先知道的是"Kotlin 用可空类型把 NPE 赶到了编译期，但协程与共享可变状态仍需自己保证"。

```kotlin
import java.util.concurrent.atomic.AtomicInteger

class Flag {
    @Volatile var visible = false          // JMM：写操作对其他线程可见
}

fun main() {
    val xs = listOf(1, 2, 3)
    println(xs.getOrNull(3))               // null   可失败访问
    // println(xs[3])                      // 🛑 IndexOutOfBoundsException

    val arr = intArrayOf(1, 2, 3)          // 数组带边界检查
    println(arr.size)                      // 3

    val counter = AtomicInteger()
    val ts = List(10) { Thread { repeat(1000) { counter.incrementAndGet() } } }
    ts.forEach { it.start() }
    ts.forEach { it.join() }
    println(counter.get())                 // 10000

    val f = Flag()
    f.visible = true
    println(f.visible)                     // true
}
```

`@Volatile` 只保证可见性与禁止重排，不保证 `x++` 这类复合操作原子，`AtomicInteger`、`LongAdder`、`ConcurrentHashMap` 才提供原子语义；JVM 的 happens-before 由 `synchronized`、`volatile`、`java.util.concurrent` 里的锁与原子类共同建立。协程方面，同一个 `CoroutineScope` 里并发修改普通集合会出问题，跨线程切换用 `Dispatchers.Default` 时尤其危险，正确做法是让状态留在单个协程里、用 `Mutex`/`AtomicReference`/`StateFlow` 做同步，`@Volatile` 对挂起函数里的状态毫无帮助。泄漏问题集中在协程作用域：`GlobalScope.launch` 会一直活着，Android 上把 `Activity` 的引用塞进长生命周期协程是最常见的泄漏；结构化并发（`coroutineScope`、`viewModelScope`）就是为了让作用域跟着生命周期结束。

📘 [Kotlin · 共享可变状态与并发](https://kotlinlang.org/docs/shared-mutable-state-and-concurrency.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 语言规范里没有"未定义行为"这一档，越界是 `ArrayIndexOutOfBoundsException`、空引用是 NPE、整数溢出是回绕，全部有确定语义；唯一没有保证的是 JNI 与 `sun.misc.Unsafe` 触碰到的原生内存。它属于运行时保证这一类，最该先知道的是"JMM 定义的 happens-before 是判断线程安全唯一的尺子"。

```java
import java.util.concurrent.atomic.AtomicInteger;

public class Boundary {
    static volatile boolean flag = false;   // volatile：建立 happens-before

    public static void main(String[] args) throws Exception {
        int[] xs = {1, 2, 3};
        // System.out.println(xs[3]);      // 🛑 ArrayIndexOutOfBoundsException

        AtomicInteger c = new AtomicInteger();
        Thread[] ts = new Thread[10];
        for (int i = 0; i < ts.length; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < 1000; k++) c.incrementAndGet(); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        System.out.println(c.get());        // 10000

        flag = true;
        System.out.println(flag);           // true
        // JNI / sun.misc.Unsafe / java.lang.foreign 之后就没有语言保证了
        System.out.println(xs.length);      // 3
    }
}
```

可见性问题由 JMM 定义：`volatile` 写与读之间、`synchronized` 的解锁与加锁之间、`Thread.start`/`join` 之间都存在 happens-before，没有这些关系就没有任何顺序保证，测试机上跑对了不代表线上对。`java.util.concurrent` 里的 `ConcurrentHashMap`、`CopyOnWriteArrayList`、`LongAdder`、`BlockingQueue` 是常规答案，`Collections.synchronizedXxx` 只是给每个方法加锁，迭代时仍要手动同步。泄漏的三大经典来源是 `static` 集合只增不减、`ThreadLocal` 里的大对象（线程池复用时尤其危险，必须 `remove()`）、以及被应用服务器或自定义 `ClassLoader` 加载后无法卸载的类。悬垂不会出现，但"引用保持对象存活"会造成逻辑泄漏：缓存里存了 `Class`、`ClassLoader`、大 `byte[]`，对象图就一直不释放。Java 25 落地的 JEP 513（Flexible Constructor Bodies）把构造期这条边界又往安全的一侧推了一步：构造函数体允许在 `super(...)`/`this(...)` 之前先执行语句，但这段序言（prologue）里不能使用正在构造的实例，只能给本类中尚无初始化器的字段赋值；于是参数校验可以 fail-fast，子类字段也能在父类构造器把它暴露给其他代码之前先初始化好，避免"父类构造器调用可覆写方法时读到子类未初始化字段"这一类经典问题。

📘 [JLS · Java 内存模型](https://docs.oracle.com/javase/specs/jls/se25/html/jls-17.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的未定义行为清单很长，而且编译器有权假设它永远不会发生，因此优化会把"看起来能跑"的代码变成完全不同的东西。它属于没有安全保证这一类，最该先知道的是"UB 不是错误结果，而是编译器不再对程序负任何责任"。

```cpp
#include <bit>
#include <cstdio>
#include <vector>

int main() {
    int a[3] = {1, 2, 3};
    // std::printf("%d\n", a[3]);         // 🛑 越界读：UB（ASan 能抓到）
    std::printf("%zu\n", std::size(a));   // 3

    int x = 2147483647;
    // x + 1;                              // 🛑 有符号溢出：UB
    unsigned u = 4294967295u;
    std::printf("%u\n", u + 1);            // 0    无符号回绕是良定义

    int bits = 0x3f800000;
    float f = std::bit_cast<float>(bits);  // 位重解释：标准做法
    std::printf("%.1f\n", f);              // 1.0

    static int *dangling = nullptr;
    { int local = 7; dangling = &local; }
    // std::printf("%d\n", *dangling);     // 🛑 use-after-free：UB
    std::printf("%d\n", dangling == nullptr);   // 0
}
```

UB 清单里的常见项包括：数组越界、空指针解引用、有符号整数溢出、严格别名违反（用 `float*` 读 `int` 对象）、读未初始化值、use-after-free、double free、数据竞争（C++11 起）、无效的类型转换、违反 `restrict` 对应物的契约、以及对象生命周期之外访问。越界与悬垂在标准库里靠容器与智能指针规避，`std::span`、`std::string_view` 带长度但不检查，`std::vector::operator[]` 不检查而 `at()` 检查。泄漏的正解是 RAII：`std::unique_ptr`/`shared_ptr` 加容器；`shared_ptr` 互环要用 `weak_ptr` 断开否则必然泄漏，`std::weak_ptr::lock` 是安全的提升方式。并发安全由 C++ 内存模型兜底：`std::atomic` 配 `memory_order_relaxed`/`acquire`/`release`/`acq_rel`/`seq_cst` 表达顺序，`std::mutex`、`std::scoped_lock`、`std::jthread` 是常规工具，任何无同步的共享写都是数据竞争即 UB。

📘 [cppreference · 未定义行为](https://en.cppreference.com/w/cpp/language/ub)

{{% /tab %}}

{{% tab header="C" %}}

C 标准里的未定义行为比 C++ 还宽：很多在其他语言里"实现相关"的东西在 C 里直接是 UB，编译器可以据此做任意假设。它属于没有安全保证这一类，最该先知道的是"C 的运行时没有一层安全网，`-fsanitize` 是开发期唯一的补救"。

```c
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int a[3] = {1, 2, 3};
    /* printf("%d\n", a[3]);       🛑 越界读：UB，完全没有边界检查 */
    printf("%zu\n", sizeof a / sizeof a[0]);   /* 3 */

    int x = INT_MAX;
    /* x + 1;                       🛑 有符号溢出：UB */
    unsigned u = UINT_MAX;
    printf("%u\n", u + 1);          /* 0    无符号回绕是良定义 */

    int *p = malloc(sizeof(int));
    *p = 1;
    free(p);
    /* printf("%d\n", *p);          🛑 use-after-free：UB */
    /* free(p);                     🛑 double free：UB */

    int uninit;
    /* printf("%d\n", uninit);      🛑 读未初始化：UB */
    (void)x; (void)uninit;
    /* 违反 restrict、无效的函数指针转换、数据竞争（C11 起）同样是 UB */
    return 0;
}
```

越界访问在 C 里没有任何检查：数组退化成指针后长度信息就丢了，越界读可能拿到别的变量、越界写可能改掉返回地址，`gets`、`strcpy`、`sprintf` 是历史上的重灾区，替代品是 `fgets`、`strncpy`/`snprintf` 以及 `memcpy_s` 一类的边界检查版本。悬垂的典型形式是返回局部数组的指针、`free` 之后继续用、`realloc` 之后仍用旧指针；生命周期完全靠纪律与工具（ASan、Valgrind）而不是类型系统。泄漏就是 `malloc` 与 `free` 配平失败，环形数据结构、错误路径提前 `return`、`realloc` 失败后丢掉原指针是三个高发点。并发方面，C11 引入 `_Atomic` 与 `<stdatomic.h>`、`<threads.h>`，在那之前只能靠平台原语；任何无同步的共享写都是数据竞争，在 C11 的内存模型下也是 UB。

📘 [cppreference · C 未定义行为](https://en.cppreference.com/w/c/language/behavior)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 默认开边界检查、默认做类型检查，错误以异常形式抛出，所以安全边界的默认位置和 Python 接近；但 `@inbounds` 与 `unsafe_load`/`unsafe_store!` 会把这一层全部拿掉。它属于运行时保证这一类，最该先知道的是"`@inbounds` 是性能工具，同时也是 UB 开关"。

```julia
v = [1, 2, 3]
println(v[2])              # 2
# v[4]                     # 🛑 BoundsError

s = 0
@inbounds for i in 1:3     # 关掉这一段的边界检查
    global s += v[i]
end
println(s)                 # 6

p = pointer(v)             # 指向底层数组
println(unsafe_load(p, 2)) # 2
# unsafe_load(p, 99)       # 🛑 UB：没有边界检查，读到什么都有可能

println(Base.JLOptions().check_bounds)   # 1  默认开；--check-bounds=no 时是 0
```

`@inbounds` 与 `@boundscheck` 的约定是"调用者保证下标合法"，循环写错一位时不会抛 `BoundsError` 而是读出垃圾值、写坏相邻内存；`unsafe_load`/`unsafe_store!`/`unsafe_wrap` 直接操作裸指针，`ccall` 进入 C 之后所有保证同样消失，`GC.@preserve` 用来保证被 C 持有的对象在调用期间不被搬动或回收。泄漏方面 Julia 的 GC 不会漏收可达对象，真正的问题是"看起来该被回收却始终可达"：闭包捕获的大数组、`const` 全局字典、任务（`Task`）挂在调度器上不结束、`Channel` 没有关闭。并发方面 `Threads.@threads`、`Threads.@spawn`、`@async` 都不能自动保证安全，共享数组的并发写是真正的数据竞争（会读到撕裂值），要么按索引切分让每个线程写自己的区间，要么用 `Threads.Atomic`、`ReentrantLock`、`Channel` 做同步；`--check-bounds=yes` 是排查边界问题的编译选项。

📘 [Julia · 边界检查与 @inbounds](https://docs.julialang.org/en/v1/devdocs/boundscheck/)

{{% /tab %}}

{{% tab header="C#" %}}

托管代码里 C# 没有未定义行为：越界抛 `IndexOutOfRangeException`、溢出默认回绕而 `checked` 抛 `OverflowException`、空引用抛 `NullReferenceException`；一旦进入 `unsafe` 上下文就退化成指针语义。它属于运行时保证这一类，最该先知道的是"`unsafe` 与 `stackalloc` 是两处需要自己负责的地方"。

```csharp
using System;

class Boundary {
    static unsafe void Main() {
        int[] xs = { 1, 2, 3 };
        // Console.WriteLine(xs[3]);          // 🛑 IndexOutOfRangeException

        int x = int.MaxValue;
        Console.WriteLine(unchecked(x + 1));   // -2147483648  默认 unchecked 回绕
        try { Console.WriteLine(checked(x + 1)); }
        catch (OverflowException) { Console.WriteLine("overflow"); }   // overflow

        fixed (int* p = xs) {                  // unsafe 上下文 + fixed 固定托管对象
            Console.WriteLine(p[2]);           // 3
            // Console.WriteLine(p[3]);        // 🛑 托管对象之外，没有任何检查
        }

        Span<byte> buf = stackalloc byte[4];   // 栈上分配，生命周期受限于作用域
        buf[0] = 42;
        Console.WriteLine(buf[0]);             // 42
    }
}
```

`unsafe` 块里的指针算术、`fixed` 固定后的托管数组、`stackalloc` 分配的栈内存都不带边界检查，`Span<T>` 与 `Memory<T>` 则把长度带在身上，`buf[4]` 会抛 `IndexOutOfRangeException`，所以 2.1 之后的新代码应该优先用 `Span<T>` 而不是裸指针。悬垂在托管世界不会发生，但 `stackalloc` 的缓冲区离开作用域即失效，把它当返回值传出去是典型的 bug；`fixed` 的作用域之外指针也必须弃用。泄漏主要来自事件订阅（`event += handler` 后不解绑会让发布者一直持有订阅者）、`static` 缓存、以及 `IDisposable` 忘记 `Dispose` 导致原生句柄耗尽。并发方面 `volatile` 只给可见性，`Interlocked`、`lock`、`System.Collections.Concurrent`、`Channel<T>` 才是原子与顺序的正解。

📘 [MS Learn · unsafe 代码与指针](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/unsafe-code)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 在语言层没有未定义行为：越界抛 `RangeError`、类型不符抛 `TypeError`、空值访问在空安全下编译期就被挡掉；离开 `dart:ffi` 才是原生内存的地盘。它属于运行时保证这一类，最该先知道的是"isolate 之间零共享内存，所以 Dart 里没有传统意义的数据竞争"。

```dart
import 'dart:isolate';

void main() async {
  final xs = [1, 2, 3];
  print(xs.elementAtOrNull(3));    // null
  try { xs[3]; } catch (e) { print(e.runtimeType); }   // RangeError

  // isolate 之间没有共享可变内存：数据靠消息传递
  final port = ReceivePort();
  await Isolate.spawn(worker, port.sendPort);
  print(await port.first);         // 42

  final typed = Int32List(3);      // 连续内存的类型化数组，越界同样抛 RangeError
  typed[0] = 7;
  print(typed[0]);                 // 7

  final w = WeakReference<List<int>>(xs);   // 弱引用
  print(w.target != null);         // true
}

void worker(SendPort p) => p.send(42);
```

越界访问对 `List`、`Uint8List`、`Int32List` 一律抛 `RangeError`，`elementAtOrNull`/`tryParse` 这类 API 返回 `null` 而不抛；`!` 空断言失败抛 `TypeError`，`late` 变量未初始化就读会抛 `LateInitializationError`。悬垂不会在 Dart 对象上发生（有 GC），但 `dart:ffi` 里 `calloc` 出来的内存必须自己 `free`，用 `Arena` 做区域分配或者 `NativeFinalizer` 挂终结器是官方推荐的两条路。泄漏在 Flutter/Dart 里主要是 `Stream` 订阅忘记 `cancel`、`StreamController` 没 `close`、`Timer`/`Timer.periodic` 没取消，`leak_tracker` 就是专门为这个场景做的。并发模型上，每个 isolate 有独立堆与独立事件循环，共享状态只能靠消息传递或者 `TransferableTypedData`；`Isolate.run` 起一个短任务是最简单的并行手段。

📘 [Dart · dart:ffi](https://dart.dev/interop/c-interop)

{{% /tab %}}

{{% tab header="R" %}}

R 在语言层没有未定义行为，但它的"安全边界"很特别：越界取下标不报错而是给 `NA`、向量长度不匹配时自动回收、类型不兼容时静默强制转换，错误因此更难被发现。它属于运行时保证这一类，最该先知道的是"R 的宽松本身就是最大的边界风险"。

```r
x <- 1:3
x[5] <- 9              # 向量自动延长，中间填 NA
print(x)               # [1]  1  2  3 NA  9
print(x[10])           # [1] NA   越界取下标给 NA，不报错
print(x[-1])           # [1] 2 3 NA 9   负下标是「排除」

print(c(1, 2, 3, 4) + c(1, 2))   # [1] 2 4 4 6   短的向量循环回收（recycling）
print(c(1, 2, 3) + c(1, 2))      # [1] 2 4 4     长度不整除时给警告

# 边界之外：.C / .Call / Rcpp 调用的原生代码没有任何保护
# 写错参数类型或长度不会抛错，而是读到垃圾内存，最坏直接让 R 进程崩溃
print(is.na(x[10]))              # [1] TRUE
```

越界取下标给 `NA`、负下标表示排除、`[[` 与 `[` 的返回类型不同（前者取元素、后者取子集），这些规则让"我以为取到了"成为最常见的错误来源；赋值时自动延长向量尤其危险，因为打错一个索引会静默把向量撑大。悬垂在 R 里不存在（有 GC），但环境的引用语义会造成"对象被闭包钉住"，以及 `data.table` 的按引用修改在函数间传递时改变调用者的数据。泄漏的两种形式是"环境被闭包捕获后长期存活"和"外部指针对象（externalptr）从未被 `finalizer` 释放"，`gc()`、`Rprofmem()`、`lobstr::obj_size`、`pryr::object_size`、`tracemem()` 是排查工具。并发方面 R 的解释器是单线程的，并行只能靠 `parallel`、`future`、`foreach` 起多个进程（fork 或 socket 集群），共享内存要靠 `sharedMemory` 或 `Rdsm` 这类扩展；`future` 的 `multisession` 是跨平台最稳的选择。

📘 [R · 内存与对象大小](https://cran.r-project.org/doc/manuals/r-release/R-ints.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的安全边界是构建模式决定的：Debug 与 ReleaseSafe 会检查整数溢出、越界、`null` 解引用、非法类型转换，ReleaseFast 与 ReleaseSmall 把这些检查全部关掉，同一份源码在两种模式下语义不同。它属于"安全模式可选"这一类，最该先知道的是"发布模式一改，越界就从 panic 变成真 UB"。

```zig
const std = @import("std");

pub fn main() !void {
    var a = [_]u8{ 1, 2, 3 };
    std.debug.print("{d}\n", .{a[2]});          // 3
    // std.debug.print("{d}\n", .{a[3]});       // 🛑 Debug/ReleaseSafe：panic
                                                //    ReleaseFast/ReleaseSmall：不检查，是真 UB

    const overflowing: u8 = 255;
    // _ = overflowing + 1;                     // 🛑 安全模式 panic：integer overflow
    const wrapped = overflowing +% 1;            // 回绕运算符：任何模式都合法
    std.debug.print("{d}\n", .{wrapped});        // 0

    var list: std.ArrayList(u8) = .empty;        // 0.15：非托管，allocator 显式传
    defer list.deinit(std.heap.page_allocator);
    try list.append(std.heap.page_allocator, 9);
    std.debug.print("{d}\n", .{list.items[0]});  // 9
}
```

安全的两种含义在 Zig 里分得很清：`undefined` 参与任何可能触发非法行为的运算都属于 Illegal Behavior，解引用 `undefined` 指针、越界、整数溢出在安全模式下 panic，在快速模式下是 UB；`@ptrCast`、`@alignCast`、`@intFromPtr` 这类转换永远不做检查，`-fsanitize-c` 与 UBSan 模式是额外的补偿。悬垂在 Zig 里肯定会遇到，因为释放是显式的：`defer`/`errdefer` 是配平的主要手段，`std.heap.DebugAllocator` 会在释放后把内存标记成不可用并报告 use-after-free 与双重释放。泄漏同样靠 `DebugAllocator.deinit()` 的输出与 `std.testing.allocator`（测试结束时自动检查泄漏）来抓，社区工具多是在 DebugAllocator 的报告之上做可视化封装。并发方面 Zig 没有内置的并发安全保证：`std.Thread`/`std.Thread.Mutex`/`std.atomic` 都是原语，数据竞争的责任完全在写代码的人；0.15 起 `async`/`await` 关键字已从语言中移除，异步 I/O 由标准库的 `std.Io` 接口承担。

📘 [Zig · 未定义行为与安全模式](https://ziglang.org/documentation/master/#Undefined-Behavior)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 语言层没有未定义行为：越界读表给 `nil`、类型不对抛错误、算术溢出回绕，所以它是"宽松但确定"的。它属于运行时保证这一类，最该先知道的是"Lua 的所有保护在 C API 边界上就终止了"。

```lua
local t = {1, 2, 3}
print(t[3])            -- 3
print(t[4])            -- nil    越界读给 nil，不报错
t[4] = 9               -- 越界写直接扩表
print(#t)              -- 4

-- for 的控制变量是只读（const）的：下面一行是编译错误
-- for i = 1, 3 do i = i + 1 end    -- 🛑 不能给只读的控制变量赋值

print(math.maxinteger + 1 == math.mininteger)   -- true   整数回绕
print(tonumber(nil))                             -- nil
-- C API 完全没有保护：栈索引越界、类型断言用错、userdata 生命周期管错
-- 都会读到无效内存，LUA_USE_APICHECK 只提供开发期的断言
```

表的越界读给 `nil`、越界写自动扩展，这既是 Lua 用起来舒服的原因，也是"打错字段名静默产生 `nil`"这类 bug 的来源；`#t` 返回的是一个边界而不是长度，表里有空洞时结果不确定。悬垂不会发生在 Lua 对象上（GC 负责），但 `userdata` 与 C API 里用 `lua_touserdata` 拿到的裸指针由扩展负责，C 侧缓存 Lua 对象指针而不加引用会让 GC 提前回收它。泄漏在 Lua 里主要是"强引用链"：模块级表当缓存、`package.loaded` 里的模块、闭包捕获的大表、注册表（registry）里塞了对象却从不清理。并发方面 Lua 没有共享内存线程，`coroutine` 是协作式调度、同一时刻只有一个协程在跑，所以不存在数据竞争；LuaJIT 的 FFI 与 C 扩展如果自己起了线程并访问 Lua 状态，就完全越出了 Lua 的保证范围。

📘 [Lua 5.5 · 错误处理与 C API](https://www.lua.org/manual/5.5/manual.html#4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的运行时就是 JavaScript，所以没有内存级未定义行为；它额外带来的是编译期检查，而编译器的检查只对"它看得见的类型"有效。它属于编译期静态检查这一类，最该先知道的是"`any`、`as`、非空断言 `!` 是三个合法的逃逸口，运行时不会有任何兜底"。

```typescript
const xs: number[] = [1, 2, 3];
console.log(xs[3]);                    // undefined  越界给 undefined，不抛错
console.log(xs.length);                // 3

// 类型只在编译期：任何断言都能骗过编译器
const n = "abc" as unknown as number;
console.log(typeof n);                 // string

// 运行时收窄必须自己写
function toNumber(v: unknown): number {
  if (typeof v === "number") return v + 1;
  return 0;
}
console.log(toNumber("x" as unknown)); // 0

// 索引签名默认不检查键是否存在
const dict: Record<string, number> = {};
console.log(dict["missing"]);          // undefined
```

越界访问在编译期取决于是否开启 `noUncheckedIndexedAccess`：不开启时 `xs[3]` 的类型是 `number`（谎报），开启后才是 `number | undefined`，这是 TypeScript 里最值得打开的一个开关。`as` 与 `!` 只是对编译器的承诺，`as unknown as T` 可以把任何类型变成任何类型，运行时不产生一行代码。悬垂不会发生（有 GC），但 `WeakRef`/`WeakMap` 与闭包捕获的 DOM 节点会造成"该释放却没释放"；`FinalizationRegistry` 能挂回收回调，回调时机同样不保证。并发模型与 JavaScript 相同：单线程事件循环，共享内存只有 `SharedArrayBuffer` + `Atomics`，`worker_threads` 之间默认拷贝数据，用共享内存就必须用原子操作，否则就是数据竞争。

📘 [TypeScript · noUncheckedIndexedAccess](https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有内存级未定义行为：越界读数组给 `undefined`、访问不存在的属性给 `undefined`、类型错误在需要时抛 `TypeError`。它属于运行时保证这一类，最该先知道的是"引擎保护你免受内存错误，但保护不了引用悬挂与资源泄漏"。

```javascript
const xs = [1, 2, 3];
console.log(xs[3]);              // undefined   越界不报错
console.log(xs.length);          // 3
xs[10] = 1;                      // 稀疏数组：长度直接变成 11
console.log(xs.length);          // 11

const o = {};
console.log(o.missing);          // undefined   JS 没有内存级 UB

// 唯一真正并行的共享内存：SharedArrayBuffer + Atomics
const sab = new SharedArrayBuffer(4);
const ia = new Int32Array(sab);
Atomics.store(ia, 0, 7);
console.log(Atomics.load(ia, 0));   // 7
console.log(typeof Atomics.add);    // function
```

越界读给 `undefined` 而不抛错，意味着拼错的属性名、错位的数组索引都会静默传播 `undefined`，需要在边界处用 `Object.hasOwn`、`Array.isArray`、可选链加默认值把它变成显式错误。悬垂在 JS 里表现为"闭包或订阅持有已废弃的对象"：`WeakRef` 能观察回收但不能阻止，`FinalizationRegistry` 的回调时机不保证，所以清理逻辑不能只依赖终结器。泄漏的三个高发点是闭包持有大对象或 DOM 节点、事件监听/`setInterval` 未解绑、模块级缓存只增不减（`Map` 当缓存时用 `WeakMap` 或者自己设上限）。并发方面 JS 是单线程事件循环，"数据竞争"只可能发生在 `SharedArrayBuffer` 上——`Atomics` 提供原子读写与 `wait`/`notify`，普通读写就是竞争；`worker_threads` 之间传对象是结构化克隆（拷贝），传 `ArrayBuffer` 可以转移所有权，这两条路径都不共享内存。

📘 [MDN · SharedArrayBuffer 与 Atomics](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Atomics)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 在语言层没有未定义行为：越界访问数组给警告加 `null`、字符串偏移越界给警告加空串、整数溢出变浮点，错误都比 C 温和；FFI 与 C 扩展一进去规则就换成 C 的规则。它属于运行时保证这一类，最该先知道的是"`isset`/`array_key_exists` 是判断键存在与否的正确姿势"。

```php
<?php
$xs = [1, 2, 3];
var_dump($xs[2]);                 // int(3)
// var_dump($xs[3]);              // ⚠️ Warning: Undefined array key 3 → NULL
var_dump(isset($xs[3]));          // bool(false)
var_dump(array_key_exists(2, $xs));   // bool(true)

$s = "abc";
var_dump($s[1]);                  // string(1) "b"
var_dump($s[5]);                  // ⚠️ Warning: Uninitialized string offset 5 → string(0) ""

echo PHP_INT_MAX + 1, "\n";       // 9.2233720368548E+18   溢出变 float
echo gettype(PHP_INT_MAX + 1), "\n";   // double

// FFI 直接进原生内存：越界与悬垂都没有保护
$ffi = FFI::cdef("int strlen(const char *s);", null);   // null：当前进程
echo $ffi->strlen("hello"), "\n";                        // 5
```

`isset` 对值是 `null` 的键返回 `false`，想区分"键不存在"与"键存在但是 `null`"必须用 `array_key_exists`；字符串偏移越界给警告而不是异常，`$s[5]` 返回空串，负索引要从 PHP 7.1 起才支持。悬垂在 PHP 层不会出现（有 GC），但 `FFI` 与扩展里的指针由扩展作者负责，`FFI::free` 之后继续用、`FFI::addr` 拿到的地址被 GC 搬走都是真问题。泄漏的核心是循环引用与长驻进程：对象互环、闭包捕获 `$this`、静态属性持有大数组，靠 `gc_collect_cycles()` 与 `gc_status()` 观测。并发方面 PHP 的常规模型是"每个请求一个进程"，进程之间不共享内存，因此没有数据竞争；`pcntl_fork`、`parallel` 扩展、Swoole/RoadRunner 这类常驻方案才需要考虑共享状态，此时仍要靠锁、`atomic` 或消息队列而不是共享变量。

📘 [PHP · FFI](https://www.php.net/manual/en/book.ffi.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 在语言层没有未定义行为：数组越界给 `nil`、类型错误抛异常、整数任意精度不会溢出；`Fiddle`、C 扩展、`ObjectSpace` 这些通道一用就离开保护范围。它属于运行时保证这一类，最该先知道的是"GVL 只保证单条字节码的原子性，不保证你的多步逻辑安全"。

```ruby
xs = [1, 2, 3]
p xs[2]              # 3
p xs[3]              # nil      越界读给 nil
p xs[-1]             # 3        负索引从尾部数
p xs.fetch(3, :dflt) # :dflt    fetch 越界可抛可给默认值

# Ruby 层没有内存级 UB，但 C 扩展与 Fiddle 直接操作裸指针
require "fiddle"
libc = Fiddle.dlopen(nil)
strlen = Fiddle::Function.new(libc["strlen"], [Fiddle::TYPE_VOIDP], Fiddle::TYPE_LONG)
p strlen.call("hello")   # 5
# 传一个无效指针进去就是段错误，Ruby 保护不了

p Thread.list.size >= 1  # true    GVL：同一时刻只有一个线程跑 Ruby 代码
```

越界读给 `nil` 是 Ruby 最著名的宽松点，`fetch` 与 `dig` 才是"我要求这个键必须存在"的写法；`nil` 会一路传播到需要数值的地方才炸，错误现场离根因很远。悬垂不会发生在 Ruby 对象上，但 C 扩展里缓存的 `VALUE` 不加引用会被 GC 回收，`Data`/`TypedData` 的 `free` 回调里访问已释放的 Ruby 对象也是崩溃来源。泄漏的主力是常量与全局变量（`CONST = []` 之后一直 `<<`）、类级缓存、单例上的哈希、以及 `ObjectSpace.define_finalizer` 里意外捕获的对象。并发方面 MRI 有 GVL，同一时刻只有一个线程执行 Ruby 字节码，所以 `+=` 这类复合操作仍会丢更新，需要 `Mutex`；要真正并行必须用 `Ractor`（4.0 起新增 `Ractor::Port` 做收发，`Ractor.yield` 与 `Ractor#take` 已移除，且它仍是实验特性）或者多进程；`Fiber` 是协作式调度，不提供任何并发安全。

📘 [Ruby · Ractor](https://docs.ruby-lang.org/en/master/Ractor.html)

{{% /tab %}}

{{< /tabpane >}}

### 安全保证与逃逸通道

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的保证是编译期保证，而且边界写得很死：safe Rust 保证内存安全与数据竞争自由，`unsafe` 只关掉**五件事**的检查（解引用裸指针、调用 `unsafe fn`、访问 `union` 字段、访问可变 `static`、实现 `unsafe trait`），其余规则照旧生效。它属于编译期保证这一类，最该先知道的是"`unsafe` 是契约声明，不是'关掉借用检查'"。

```rust
#![deny(unsafe_op_in_unsafe_fn)]

/// 安全 API：内部不做任何边界之外的假设
fn first_or_zero(v: &[i32]) -> i32 {
    *v.first().unwrap_or(&0)
}

/// # Safety
/// `ptr` 必须指向一个对齐且已初始化的 `i32`。
unsafe fn deref_raw(ptr: *const i32) -> i32 {
    unsafe { *ptr }                       // unsafe fn 内也要显式 unsafe 块
}

/// 安全抽象：把 unsafe 关在内部，对外只暴露不会 UB 的接口
struct MyVec<T> {
    data: *mut T,
    len: usize,
}

impl<T> MyVec<T> {
    fn get(&self, i: usize) -> Option<&T> {
        if i < self.len { Some(unsafe { &*self.data.add(i) }) } else { None }
    }
}

fn main() {
    let v = vec![5, 6];
    println!("{}", first_or_zero(&v));    // 5
    let x = 7;
    let got = unsafe { deref_raw(&x) };
    println!("{got}");                    // 7
    let mv: MyVec<i32> = MyVec { data: std::ptr::null_mut(), len: 0 };
    println!("{:?}", mv.get(0));          // None
    println!("{}", std::mem::size_of::<Option<&i32>>()); // 8
}
```

`unsafe fn` 表示调用者要承担责任，`unsafe trait` 表示实现者要承担责任，`unsafe impl` 则表示"我确认这个类型满足 `Send`/`Sync` 的语义要求"。`#[deny(unsafe_op_in_unsafe_fn)]` 强制在 `unsafe fn` 内部再写显式的 `unsafe` 块，好处是让"哪一行真的危险"一眼可见；这条 lint 在 2024 edition 里的默认级别是 warn（提示 `unsafe fn` 里哪些操作需要显式的 `unsafe` 块），写成 `deny` 才会升级为编译错误。安全抽象原则是被反复强调的工程纪律：`unsafe` 代码必须被封装在一个对外安全、内部自洽的 API 后面，并且用 `# Safety` 文档写清契约；标准库里的 `Vec`、`String`、`Mutex` 都是这个模式的范例。审计上通常配合 `cargo-geiger` 统计依赖树里的 unsafe 密度、`cargo-audit` 查已知漏洞、Miri 在测试里跑 UB 检测。

📘 [Rust 指南 · Unsafe 代码准则](https://rust-lang.github.io/unsafe-code-guidelines/)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的保证是编译期类型安全加运行时检查再加 ARC 的组合，官方称之为"默认内存安全"；`UnsafePointer` 系列与 `Unmanaged` 是官方留出的显式逃逸通道，名字里就写着 `Unsafe`。它属于运行时保证这一类，最该先知道的是"指针 API 只在闭包作用域内有效"。

```swift
final class Box { var v = 1 }

let bytes: [UInt8] = [0x41, 0x42, 0x43]
bytes.withUnsafeBytes { raw in
    let p = raw.baseAddress!.assumingMemoryBound(to: UInt8.self)
    print(p[1])                       // 66
}                                     // 闭包返回后这个指针立刻失效

var value = 42
withUnsafeMutablePointer(to: &value) { p in
    p.pointee += 1                    // 绕过值语义直接改内存
}
print(value)                          // 43

let unmanaged = Unmanaged.passRetained(Box())   // 引用计数 +1，脱离 ARC
print(unmanaged.takeUnretainedValue().v)        // 1
unmanaged.release()                             // 必须手动配平，否则泄漏

print(MemoryLayout<Box>.size)         // 8   类实例的引用宽度
```

`withUnsafeBytes`/`withUnsafeBufferPointer` 的作用域契约是核心规则：闭包一返回，指针就不再有效，把它存起来跨作用域使用就是悬垂。`Unmanaged.passRetained`/`passUnretained`/`takeRetainedValue`/`takeUnretainedValue` 用来在 ARC 之外传递对象引用，`passUnretained` 不增加计数，对象随时可能被释放，用错方向就是崩溃或泄漏。`withUnsafeBytes` 还有一个容易忽略的细节：它给的是原始字节，`assumingMemoryBound` 要求内存里真的存着目标类型，类型不符就是别名违规。Swift 6 语言模式下严格并发检查全开（该语言模式是 opt-in 的，需要显式选择），跨隔离域必须 `Sendable`，`@unchecked Sendable` 是并发这条线上的逃逸口——写它等于承诺自己会加锁。

📘 [Swift · 不安全指针与 Unmanaged](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的保证是运行时保证：safe Go 不会有内存错误，越界与空指针都变成 panic；`unsafe.Pointer`、`cgo` 与 `//go:linkname` 是官方留出的三条逃逸通道。它属于运行时保证这一类，最该先知道的是"`unsafe` 包的名字就是免责声明"。

```go
package main

import (
	"fmt"
	"unsafe"
)

type sliceHeader struct {
	Data uintptr
	Len  int
	Cap  int
}

func main() {
	s := []int32{1, 2, 3}
	h := (*sliceHeader)(unsafe.Pointer(&s)) // unsafe：直接看切片头
	fmt.Println(h.Len, h.Cap)               // 3 3

	p := unsafe.Slice((*byte)(unsafe.Pointer(&s[0])), 12)
	fmt.Println(len(p)) // 12   自己声明长度，越界就没有保护了

	var x int64 = 0x0102030405060708
	b := unsafe.Slice((*byte)(unsafe.Pointer(&x)), 8)
	fmt.Println(b[0]) // 8   小端机器的最低字节

	fmt.Printf("%T\n", unsafe.Pointer(nil)) // unsafe.Pointer
	fmt.Println(unsafe.Sizeof(x))           // 8
}
```

`unsafe.Pointer` 的合法转换规则在 `unsafe` 包文档里写得很细：`*T` 与 `unsafe.Pointer` 可以互转，`uintptr` 只能作为中间值立刻转回指针，绝不能把 `uintptr` 存起来当指针用，因为 GC 不认为它是引用、对象可能被搬走或回收。`cgo` 是第二条通道：C 代码里分配的内存不受 Go GC 管理，`C.CString` 必须配 `C.free`，Go 指针传给 C 之后 C 不能长期保存（cgo 指针传递规则），调用 `C` 的开销也比普通调用大得多。`//go:linkname` 是第三条通道，它直接绑定到运行时或标准库的内部符号，用在生产代码里等于把自己钉死在某个 Go 版本上，官方明确不提供兼容保证。

📘 [Go · unsafe 包](https://pkg.go.dev/unsafe)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的保证是运行时保证，而且只覆盖 Python 层；`ctypes`、`cffi`、C 扩展模块、`array`/`memoryview` 的 buffer protocol 是四条通往原生内存的路。它属于运行时保证这一类，最该先知道的是"buffer protocol 是零拷贝共享内存，也是 Python 最容易与 C 撞车的地方"。

```python
import ctypes

class Point:
    __slots__ = ("x",)             # 关掉 __dict__，省内存
    def __init__(self):
        self.x = 1

p = Point()
print(p.x)                         # 1

class Raw(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int)]

r = Raw(7)
ctypes.memmove(ctypes.byref(r), ctypes.byref(ctypes.c_int(9)), ctypes.sizeof(ctypes.c_int))
print(r.x)                         # 9   ctypes 直接改 C 层内存

class Guarded:
    __slots__ = ("_v",)
    @property
    def v(self):
        return self._v

g = Guarded()
g._v = 1
object.__setattr__(g, "_v", 99)    # 反射绕过一切可见性
print(g.v)                         # 99

mv = memoryview(bytearray(b"abcd"))  # buffer protocol：零拷贝共享内存
mv[0] = ord("Z")
print(bytes(mv))                   # b'Zbcd'
```

`ctypes` 适合一次性调用 C 函数，`cffi` 的 ABI 模式同样简单而 API 模式能生成编译期检查的绑定，性能敏感的场景应该写真正的 C 扩展（`PyCapsule` 管理生命周期、`Py_LIMITED_API` 保持 ABI 稳定）。buffer protocol 的问题在于"导出后仍然可变"：`memoryview` 导出期间对原对象做 `resize` 会抛 `BufferError`，但 C 侧拿着指针时 Python 并不知道，所以导出期间的对象必须靠引用保持存活。反射这条逃逸线在 Python 里格外彻底：`object.__setattr__`、`type.__setattr__`、`__dict__` 直接改写、`inspect` 拿 `f_locals` 都能越过 `property`、`__slots__`、描述符的一切约定；序列化库（`pickle`、`dataclasses` 的 `__init__` 绕过）也是同一类通道。审计手段是 `ctypes` 用法审查、`-X dev` 打开开发模式警告、以及对 C 扩展固定 `Py_LIMITED_API` 版本。

📘 [Python · ctypes](https://docs.python.org/3/library/ctypes.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 本身没有 `unsafe` 关键字，它的保证来自 JVM：字节码验证器保证类型正确、数组访问有边界检查、对象引用不会是野指针。它属于运行时保证这一类，最该先知道的是"逃逸全部发生在 JVM 之外或 JVM 的未受检 API 上"。

```kotlin
import java.lang.reflect.Field

class Secret(private val hidden: String = "s3cr3t") {
    fun reveal() = hidden
}

fun main() {
    val s = Secret()
    println(s.reveal())                       // s3cr3t

    // 反射是逃逸通道：setAccessible 绕过 private
    val f: Field = Secret::class.java.getDeclaredField("hidden")
    f.isAccessible = true                     // Kotlin 里是属性写法
    f.set(s, "hacked")
    println(s.reveal())                       // hacked

    // external 函数走 JNI：类型与生命周期由 native 侧负责
    println(System.getProperty("java.version"))   // 26（LTS 为 25）
    println(Runtime.getRuntime().availableProcessors() > 0)   // true
}
```

JNI 是 Kotlin/JVM 最主要的原生通道：`external fun` 声明的方法由 C/C++ 侧实现，参数与返回值要进行 `JNIEnv` 转换，`jobject` 的局部引用在 native 方法返回后失效、全局引用必须手动 `DeleteGlobalRef`，任何一处写错都是崩溃或泄漏。JVM 自身的逃逸口是 `sun.misc.Unsafe`（堆外内存、绕过构造器分配、`compareAndSwap`）以及新的 `java.lang.foreign`（`MemorySegment` 带边界检查，是 `Unsafe` 的推荐替代），`VarHandle` 提供受支持的原子与有序访问。反射在 JDK 9 之后受模块系统约束，需要 `--add-opens` 才能深入别的模块，这本身就是一条审计线索：需要 `--add-opens` 的代码就是在越过封装。

📘 [Kotlin · 与 Java 互操作](https://kotlinlang.org/docs/java-interop.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的保证是运行时保证：类加载时的字节码验证、数组边界检查、类型安全、GC 加在一起，让 Java 代码在语言层几乎不可能造成内存破坏。它属于运行时保证这一类，最该先知道的是"三条逃逸通道是 `Unsafe`、JNI 和反射（含 `VarHandle`）"。

```java
import java.lang.invoke.MethodHandles;
import java.lang.invoke.VarHandle;
import java.lang.reflect.Field;

public class Escape {
    private int secret = 1;

    public static void main(String[] args) throws Exception {
        Escape e = new Escape();
        Field f = Escape.class.getDeclaredField("secret");
        f.setAccessible(true);          // 反射绕过可见性（模块下需 --add-opens）
        f.setInt(e, 42);
        System.out.println(e.secret);   // 42

        VarHandle vh = MethodHandles.lookup().findVarHandle(Escape.class, "secret", int.class);
        vh.set(e, 7);
        System.out.println(vh.get(e));          // 7
        System.out.println(vh.getAndAdd(e, 1)); // 7
        System.out.println(e.secret);           // 8

        // JNI：native 方法里的越界与悬垂 JVM 完全看不到
        System.out.println(System.getProperty("java.vm.name").length() > 0);   // true
    }
}
```

反射的用途是框架（序列化、依赖注入、ORM）在读不到源码的情况下操作对象，代价是绕过 `private`、绕过泛型擦除、绕过 `final`（`Field.setAccessible` 加 `modifiers` 改写），所以 JDK 9 之后用模块系统的 `opens` 把它约束成显式授权。`VarHandle` 是 JDK 9 起对 `Unsafe` 的受支持替代，提供 `get`/`set`/`compareAndSet`/`getAndAdd` 以及 `getAcquire`/`setRelease` 等有序访问，是写无锁数据结构时应该用的东西。JNI 与 `java.lang.foreign`（`Linker`、`MemorySegment`、`Arena`）是原生内存通道，后者的 `Arena` 明确规定了内存的存活范围，比 JNI 手动管理更不容易漏。审计上通常用 `jdeps` 看模块依赖、用 JFR 看原生内存、以及对 `--add-opens`/`--enable-native-access` 这类启动参数做代码审查。

📘 [Java · java.lang.foreign（FFM API）](https://docs.oracle.com/en/java/javase/25/core/foreign-function-and-memory-api.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 没有"安全"与"不安全"的语法分界，整个语言都建立在"程序员不触发 UB"这个契约上，标准库与操作系统 API 只是相对可靠的约定。它属于约定保证这一类，最该先知道的是"没有 `unsafe` 关键字，意味着没有地方可以声明'我知道我在干什么'"。

```cpp
#include <bit>
#include <cstdio>
#include <cstdlib>
#include <new>
#include <type_traits>

struct Header { int tag; };

int main() {
    // 字节级观察是允许的：任何对象都可以当作 unsigned char 数组来读
    Header h{1};
    auto *raw = reinterpret_cast<unsigned char *>(&h);
    std::printf("%02x\n", raw[0]);                 // 01（小端）

    // 用非类型正确的指针访问对象是 UB；placement new 才是构造对象的正路
    void *slot = std::malloc(sizeof(Header));
    Header *hp = new (slot) Header{7};
    std::printf("%d\n", hp->tag);                  // 7
    hp->~Header();
    std::free(slot);

    std::printf("%d\n", std::is_trivially_copyable_v<Header>);   // 1
    std::printf("%d\n", std::has_unique_object_representations_v<Header>);   // 1

    // FFI 边界：dlopen/dlsym 拿到的函数指针类型全靠约定
    std::printf("%zu\n", sizeof(void (*)()));      // 8
}
```

`reinterpret_cast` 与 `static_cast` 的差别、`const_cast` 去掉 `const` 后写入只读对象、通过错误类型访问对象（严格别名）、把 `void*` 转成不匹配的指针，这些都是编译器无法检查而标准明文禁止的操作。与操作系统的边界靠显式契约维持：POSIX 函数指针 `strlen` 返回 `size_t`，写错签名就是 UB；回调函数必须用 `extern "C"` 并获得正确的调用约定；`dlopen`/`dlsym` 拿到的地址转成函数指针在标准里是实现定义行为。工程上的应对是把 C API 包成 RAII 的 C++ 类（`std::unique_ptr` 配自定义 deleter、`std::span` 带长度），再用 `-fsanitize=address,undefined` 与 `clang-tidy` 覆盖这些边界。

📘 [cppreference · C++ 与 C 互操作](https://en.cppreference.com/w/cpp/language/language_linkage)

{{% /tab %}}

{{% tab header="C" %}}

C 没有任何安全标注，整个语言默认就是"不安全"：所有保证都来自库的约定与程序员的纪律。它属于没有安全保证这一类，最该先知道的是"`restrict`、`volatile`、`_Atomic` 是三个不同方向的契约，谁也不能替代谁"。

```c
#include <stdio.h>
#include <stdlib.h>

/* C 没有任何安全标注：整个语言默认就是「不安全」，责任全在程序员 */
static void copy10(int *restrict dst, const int *restrict src) {
    for (int i = 0; i < 10; i++) dst[i] = src[i];   /* 违反 restrict 是 UB */
}

int main(void) {
    int *a = malloc(10 * sizeof *a);
    int *b = malloc(10 * sizeof *b);
    if (!a || !b) return 1;
    for (int i = 0; i < 10; i++) b[i] = i;
    copy10(a, b);                 /* 两块内存不重叠：契约满足 */
    printf("%d\n", a[9]);         /* 9 */

    volatile int guard = 1;       /* volatile 只禁止优化掉访问，不是同步原语 */
    printf("%d\n", guard);        /* 1 */
    free(a); free(b);
    return 0;
}
```

`restrict` 是"我保证这块内存只通过这个指针访问"的承诺，编译器据此做向量化与重排，一旦两块内存重叠结果就是未定义行为；`volatile` 是"每次都真的读写这个地址"的承诺，用于内存映射 I/O 与信号处理，它**不**提供原子性、**不**建立线程间的顺序；`_Atomic`（C11）才是并发语义的正确工具，配 `memory_order` 表达顺序。调用操作系统的边界（`read`/`write`、`mmap`、`ioctl`、`dlopen`）全部靠头文件里的原型维持，写错长度或类型不会有任何运行时检查。审计手段是编译期警告全开（`-Wall -Wextra -Wconversion -Wcast-align`）、`clang-tidy`、`cppcheck`、静态分析器，加上 ASan/UBSan/TSan 与 Valgrind 做动态覆盖。

📘 [cppreference · restrict 与 volatile](https://en.cppreference.com/w/c/language/restrict)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的保证是运行时保证：默认开边界检查、默认做类型检查、`MethodError` 之类的错误都很明确；`@inbounds`、`unsafe_load`、`ccall` 是三条官方的逃逸通道。它属于运行时保证这一类，最该先知道的是"`ccall` 的参数类型与 ABI 都要自己写对，写错不会报错而是崩溃"。

```julia
# Julia 的默认保证是「边界检查 + 类型检查」，逃逸通道全部带 unsafe/@inbounds 名字
v = [10, 20, 30]
println(v[3])                       # 30

# ccall：直接调 C 函数，参数类型与 ABI 全靠自己保证
t = ccall(:time, Clong, (Ptr{Cvoid},), C_NULL)
println(t isa Int)                  # true

# 字符串指针只在 GC 不移动该对象期间有效
s = "hello"
GC.@preserve s begin
    p = pointer(s)
    println(unsafe_load(p, 1))      # 104   'h' 的 ASCII 码
end

println(Base.JLOptions().check_bounds)   # 1  默认开边界检查
sum_inbounds(x) = @inbounds x[1] + x[3]
println(sum_inbounds(v))            # 40
# @inbounds 之后越界不再抛 BoundsError，而是真正的 UB
# bad(x) = @inbounds x[9]           # 调用它读到的是垃圾值，不是异常
```

`ccall` 的写法是 `ccall((:函数名, "库名"), 返回类型, (参数类型...), 参数...)`，返回类型必须与 C 的 ABI 匹配，`Cint`/`Clong`/`Csize_t` 这些别名要按平台用，传 `String` 给 `const char*` 需要 `Base.unsafe_convert` 或 `GC.@preserve` 保证对象不被搬动。`unsafe_load`/`unsafe_store!`/`unsafe_wrap`/`unsafe_pointer_to_objref` 都不做检查，`@inbounds` 只跳过边界检查而保留其余语义。反射在 Julia 里同样彻底：`fieldnames`、`getfield`、`setfield!`、`eval`、`@eval` 可以获取与修改任何字段（`setfield!` 对不可变结构体例外），`Base.@assume_effects` 与 `@inline` 是性能声明而不是安全声明。审计手段是 `--check-bounds=yes` 强制开检查、`--track-allocation=user` 与 `@allocated` 观察分配、`JET.jl` 做静态类型与错误分析、`Cthulhu.jl` 看编译结果里的 `@inbounds` 是否被真的消除。

📘 [Julia · ccall 与原生代码](https://docs.julialang.org/en/v1/manual/calling-c-and-fortran-code/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的保证是运行时保证：IL 验证器保证类型安全、数组访问有边界检查、GC 管住生命周期；`unsafe` 上下文是官方留出的、带语法标记的逃逸通道。它属于运行时保证这一类，最该先知道的是"`unsafe` 之外还有一条更隐蔽的通道叫 `UnsafeAccessor`"。

```csharp
using System;
using System.Reflection;
using System.Runtime.CompilerServices;

class Secret {
    private int hidden = 1;
    public int Reveal() => hidden;
}

class Escape {
    [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "hidden")]
    extern static ref int HiddenField(Secret s);      // C# 12+：无需反射、无装箱

    static void Main() {
        var s = new Secret();
        Console.WriteLine(s.Reveal());                // 1

        HiddenField(s) = 99;                          // 直接拿到私有字段的 ref
        Console.WriteLine(s.Reveal());                // 99

        var f = typeof(Secret).GetField("hidden", BindingFlags.NonPublic | BindingFlags.Instance)!;
        Console.WriteLine(f.GetValue(s));             // 99   反射同样能读

        Console.WriteLine(f.IsPrivate);               // True

        int[] arr = { 1, 2, 3 };
        unsafe { fixed (int* p = arr) { Console.WriteLine(p[2]); } }   // 3
    }
}
```

`unsafe` 上下文里能写指针、`stackalloc`、`fixed`，其中 `fixed` 用来把托管对象钉住不让 GC 搬动，`stackalloc` 在栈上分配缓冲区（超过一定大小会改走堆，配 `Span<T>` 使用），`checked`/`unchecked` 控制溢出行为。`UnsafeAccessor` 是 C# 12 引入的、比反射更彻底的通道：它在编译期生成对私有字段/方法的直接访问代码，没有反射的运行时开销，也没有 `setAccessible` 那样的授权检查，所以它在性能敏感的框架里被广泛使用，同时让"私有"彻底变成约定。序列化库（`System.Text.Json`、Newtonsoft.Json）与 ORM 走的是同一类通道：直接写字段、跳过构造函数、绕过只读属性。审计上应该盯住 `unsafe`、`UnsafeAccessor`、`Marshal`、`DllImport`/`LibraryImport` 与 `--enable-native-access`，还要盯住 `stackalloc` 的大小是否来自外部输入。

📘 [MS Learn · UnsafeAccessorAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.unsafeaccessorattribute)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的保证是运行时保证：空安全在编译期挡住空值、`List` 与类型化数组越界抛 `RangeError`、GC 管住对象生命周期；`dart:ffi` 是官方留出的唯一原生内存通道。它属于运行时保证这一类，最该先知道的是"Arena 与 NativeFinalizer 是把原生内存接回 Dart 生命周期的两件工具"。

```dart
import 'dart:ffi';
import 'package:ffi/ffi.dart';

typedef StrlenNative = IntPtr Function(Pointer<Utf8>);
typedef StrlenDart = int Function(Pointer<Utf8>);

void main() {
  final libc = DynamicLibrary.process();          // 进程内的 C 符号
  final strlen = libc.lookupFunction<StrlenNative, StrlenDart>('strlen');

  final arena = Arena();                          // 区域分配：作用域结束统一释放
  final p = 'hello'.toNativeUtf8(allocator: arena);
  print(strlen(p));                               // 5
  // arena 离开作用域时一次性释放全部内存

  final raw = calloc<Uint8>(4);                   // 独立分配：必须自己 free
  raw[0] = 65;
  print(raw[0]);                                  // 65
  // raw[4] = 1;                                  // 🛑 越界写：原生内存，Dart 不检查
  calloc.free(raw);

  print(libc.providesSymbol('strlen'));           // true
}
```

`Arena` 是 `package:ffi` 里官方推荐的默认选择：把一批临时原生内存挂在同一个区域上，退出作用域时统一释放，避免逐块 `free` 遗漏；需要独立生命周期时用 `calloc`/`malloc` 加 `free`，并用 `NativeFinalizer` 在 GC 回收 Dart 对象时自动释放对应的原生内存。`Pointer<T>` 的 `[]` 下标不做边界检查，`asTypedList` 得到的 `TypedData` 视图一旦超出原始分配就是越界；`DynamicLibrary.process()` 只能看已经加载进进程的符号，`DynamicLibrary.open` 才是主动加载动态库。WebAssembly 是另一条通道：`dart:js_interop` + Wasm 让 Dart 与 JS 共享线性内存，越界访问由 Wasm 引擎 trap 兜住，这一层比 FFI 安全一些。

📘 [Dart · 与 C 互操作](https://dart.dev/interop/c-interop)

{{% /tab %}}

{{% tab header="R" %}}

R 的保证是运行时保证，而且它的"检查"很宽松：越界给 `NA`、类型不匹配做强制转换、原生代码完全没有保护。它属于运行时保证这一类，最该先知道的是"`.C`、`.Call`、`.External` 三条原生通道的抽象层级依次升高"。

```r
# 原生边界：.C / .Call / .External 三条通道
# .C 只传基本类型指针，最容易写错；.Call 传 SEXP，官方推荐；
# .External 允许 R 侧懒求值参数，只有 base 包和少数高级包在用
cat("channels:", paste(c(".C", ".Call", ".External"), collapse = ", "), "\n")
# channels: .C, .Call, .External

# 反射式逃逸：环境是引用语义，可以绕过一切可见性约定
e <- new.env(parent = emptyenv())
assign("hidden", 42, envir = e)
f <- function() get("hidden", envir = e)
print(f())                    # [1] 42
assign("hidden", 99, envir = e)
print(f())                    # [1] 99
lockBinding("hidden", e)
print(bindingIsLocked("hidden", e))   # [1] TRUE
unlockBinding("hidden", e)
print(bindingIsLocked("hidden", e))   # [1] FALSE

# Rcpp：C++ 侧用 Rcpp::export 暴露函数，边界检查仍要自己写
# R CMD SHLIB 编译出的 .so 一旦越界，R 进程直接崩溃
```

`.C` 的接口只允许基本类型指针，参数长度由调用者保证，写错长度就是原生内存错误；`.Call` 用 `SEXP` 传递 R 对象，配合 `Rf_protect`/`Rf_unprotect` 管理 GC 保护，是 CRAN 上绝大多数包的做法；`.External` 允许把参数当作 promise 懒求值，只有 `base` 与少数包在用。`Rcpp` 用 `Rcpp::export` 生成胶水代码，把 `NumericVector`、`IntegerVector` 这类带长度信息的视图交给 C++，比裸指针安全得多，但 `.at()` 与 `[]` 的差别（前者检查、后者不检查）仍然是手工责任。反射式的逃逸在 R 里主要通过 `environment`、`assign`、`unlockBinding`、`assignInNamespace` 实现，`assignInNamespace` 甚至能改别的包里的私有对象，调试很方便、上线很危险；`tracemem`、`Rprofmem`、`lobstr` 是审计内存行为的主要工具。

📘 [R · 与 C 的接口](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Interface-functions-.C-.Call-and-.External)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的保证是"安全模式可选"：Debug 与 ReleaseSafe 带检查，ReleaseFast 与 ReleaseSmall 不带，所以它的安全等级是构建选项而不是语言属性。它属于"安全模式可选"这一类，最该先知道的是"`@cImport` 与 `export` 让 Zig 能无缝进出 C，也把 C 的所有风险原样带进来"。

```zig
const std = @import("std");
const c = @cImport({                       // 直接翻译 C 头文件，边界由你负责
    @cInclude("string.h");
});

export fn addOne(x: c_int) c_int {         // export：按 C ABI 暴露给外部
    return x + 1;
}

pub fn main() !void {
    var buf: [16]u8 = undefined;
    const s = "hello";
    _ = c.strcpy(&buf, s);                  // C 函数不会检查缓冲区大小
    std.debug.print("{s}\n", .{buf[0..5]}); // hello

    const aligned: u32 = 0x01020304;
    const bytes: []const u8 = @ptrCast(&aligned);   // 0.15 起允许：单指针 → 切片
    std.debug.print("{d}\n", .{bytes[0]});          // 4（小端的最低字节）

    var mmio: u32 = 0;
    const vp: *volatile u32 = &mmio;        // volatile：禁止编译器消除/合并访问
    vp.* = 1;
    std.debug.print("{d}\n", .{mmio});      // 1
}
```

`@cImport`/`@cInclude` 在编译期把 C 头翻译成 Zig 声明，`@cDefine`/`@cUndef` 控制宏，`export` 与 `extern` 分别对应"我提供符号"和"我引用符号"，`callconv(.c)` 明确调用约定。`@ptrCast` 与 `@alignCast` 是零成本转换：前者改指针类型，后者承诺对齐（对齐不足在安全模式下 panic，快速模式下是 UB）；`@volatileCast` 与 `*volatile T` 处理内存映射 I/O；`@bitCast` 做位重解释。Zig 0.15 起 `@ptrCast` 还支持把单项指针直接转成切片，官方计划把这类"可能越界"的转换拆到新的 `@memCast` 里，用意就是让危险操作更容易被搜索到。审计手段是 Debug/ReleaseSafe 构建加 `std.testing.allocator`、`-fsanitize-c` 生成 C 兼容的 UBSan 信息、以及 `--verbose-air` 查看编译中间表示确认哪些检查被保留或消除。

📘 [Zig · C 互操作与 @cImport](https://ziglang.org/documentation/master/#C)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的保证是运行时保证：类型错误抛错误、越界读给 `nil`、GC 管住对象；C API 与 LuaJIT FFI 是没有保护的逃逸通道。它属于运行时保证这一类，最该先知道的是"C API 的契约（栈平衡、索引合法、生命周期）全部由扩展作者承担"。

```lua
-- 纯 Lua 侧没有 unsafe：所有逃逸都发生在 C API 边界
print(debug.getinfo(1, "S").what)        -- main   debug 库本身也是一条逃逸通道
print(debug.getlocal(1, 1))              -- nil    没有第 1 个局部变量

local t = setmetatable({}, { __index = function(_, k) return "gen:" .. k end })
print(t.anything)                        -- gen:anything   元表能拦截一切访问

print(_VERSION)                          -- Lua 5.5
-- C API 的契约示例（伪代码）：
--   lua_pushvalue(L, 99)  → 索引越界，读到无效栈位置
--   luaL_checkstring(L, 1) 之前不检查类型，后面全是错
--   lua_touserdata 拿到的指针在 __gc 之后就是悬垂
-- LuaJIT 的 FFI 比 C API 更直接：声明 C 类型后直接调用，越界即崩溃
--   ffi.cdef[[ int puts(const char *s); ]]
--   ffi.C.puts("hi")
```

C API 的核心契约有三条：栈必须配平（压了几个值就要弹回几个）、索引必须有效（正索引从 1 数、负索引从栈顶数、伪索引指向注册表与环境）、对象的生命周期必须由引用管理（`luaL_ref`/`luaL_unref` 拿到的引用要显式释放，`lua_pcall` 之外的长跳转要防止栈失衡）。元表本身是一条设计层面的逃逸通道：`__index`、`__newindex`、`__gc`、`__close` 可以拦截几乎所有操作，`debug` 库还能读写局部变量、修改上值、替换元表，所以"加载不受信任的 Lua 代码"和"执行任意代码"基本等价。LuaJIT FFI 的威力更大也更危险，`ffi.new`/`ffi.cast`/`ffi.string` 的错误立刻变成段错误，而且 LuaJIT 的 JIT 会把这些操作编译成真实的内存访问。

📘 [Lua 5.5 · C API](https://www.lua.org/manual/5.5/manual.html#4.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的保证只在编译期：类型检查、可见性、`readonly`、泛型约束全部止步于 `.ts`，产物里什么也没有。它属于编译期静态检查这一类，最该先知道的是"WebAssembly 与原生插件是运行时那两条逃逸通道"。

```typescript
// TypeScript 的安全边界与 JS 完全相同；额外的逃逸通道是 Wasm 与原生插件
const bytes = new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0]);   // 最小 wasm 模块头
console.log(WebAssembly.validate(bytes));                       // true

// 只有编译期存在的保证：断言、泛型、readonly 全部会被擦除
interface User { readonly name: string }
const u = { name: "a" } as User;
(u as { name: string }).name = "b";                             // ⚠️ readonly 只是编译期
console.log(u.name);                                            // b

// 编译期检查看不见的东西：来自 JSON、环境变量、原生插件的数据
const raw: unknown = JSON.parse('{"n": 1}');
console.log((raw as { n: number }).n + 1);                      // 2
console.log((raw as { n: string }).n.length);                   // ⚠️ 运行时才炸

console.log(typeof process.versions.napi);                      // string
```

编译期的逃逸口有三个值得单独记住：`any`（关掉这一整片区域的检查）、`as`（对编译器的单方面承诺）、`!`（非空断言），其中 `as unknown as T` 能让任意两个类型互相转换。运行时那两条通道是 WebAssembly（线性内存的越界访问会被引擎 trap，比 FFI 安全，但 `WebAssembly.Memory` 共享给 JS 后就没有类型保护了）与 N-API/node-addon-api 原生插件（原生侧的错误 Node 无法捕获，直接崩进程）。序列化与反序列化是"编译期看不见的数据"进入系统的主要入口，正确做法是在边界上用校验库把 `unknown` 收窄成具体类型，而不是一路 `as` 下去。

📘 [TypeScript · 类型系统与运行时](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的保证是运行时保证：没有内存级 UB、所有属性访问都由引擎检查、GC 管住生命周期。它属于运行时保证这一类，最该先知道的是"引擎的保护圈外面还有 Wasm 与原生插件"。

```javascript
// JS 没有内存级 UB；逃逸通道都在引擎边界之外
const mod = new WebAssembly.Module(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0]));
console.log(WebAssembly.Module.exports(mod).length);   // 0  最小模块没有导出

const mem = new WebAssembly.Memory({ initial: 1 });
mem.grow(1);
console.log(mem.buffer.byteLength);            // 131072

// Wasm 线性内存越界会被引擎 trap，不会静默损坏内存
console.log(typeof process.versions.napi);     // string
console.log(Object.keys(process.versions).length > 0);   // true
console.log(typeof WebAssembly.instantiate);   // function
```

Wasm 的越界访问在实例内部会 trap（`RuntimeError: memory access out of bounds`），但一旦把 `WebAssembly.Memory` 的 `ArrayBuffer` 交给 JS，JS 侧的 `Uint8Array` 视图就只是普通视图，超出真实长度的访问又会回到 `undefined` 的宽松语义。N-API/node-addon-api 插件、`process.binding` 这类内部 API、以及 `--experimental-*` 开关都是把保护圈打开的口子，其中原生插件里分配的内存不受 V8 GC 管理，必须用 `napi_create_external_buffer` 配终结器或者让 JS 侧持有 `ArrayBuffer`。`new Function`、`eval`、`vm` 模块与不受信任的 `import()` 是代码层面的逃逸：它们能把任意字符串变成可执行代码，CSP 与 `vm.SourceTextModule` 是常见的约束手段。

📘 [MDN · WebAssembly 内存](https://developer.mozilla.org/en-US/docs/WebAssembly/JavaScript_interface/Memory)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的保证是运行时保证：类型声明（含 `strict_types`）、`TypeError`、GC 一起把内存破坏挡在语言层之外；FFI 扩展与 C 扩展开发是官方的逃逸通道。它属于运行时保证这一类，最该先知道的是"FFI 自 PHP 7.4 起可用，它给的指针不受 GC 管理"。

```php
<?php
// PHP 的安全保证是运行时检查；逃逸通道是 FFI 与 C 扩展
if (extension_loaded('ffi')) {
    $ffi = FFI::cdef("size_t strlen(const char *s);", null);   // null：当前进程
    echo $ffi->strlen("hello"), "\n";                          // 5
} else {
    echo "ffi disabled\n";
}

// 反射绕过 private（PHP 8.1 起 setAccessible 不再必要）
class Cfg {
    public function __construct(private string $secret = "a") {}
    public function get(): string { return $this->secret; }
}
$c = new Cfg();
echo $c->get(), "\n";                       // a
$r = new ReflectionProperty(Cfg::class, 'secret');
$r->setValue($c, "b");                      // ⚠️ 私有可见性只是约定
echo $c->get(), "\n";                       // b

echo FFI::sizeof(FFI::new("int")), "\n";    // 4   FFI 侧的类型尺寸
```

`FFI::cdef` 解析一段 C 声明并绑定到动态库，`FFI::new`/`FFI::cast`/`FFI::addr` 负责分配与转换，`FFI::memcpy`/`FFI::memset` 做批量操作；`FFI` 分配的内存不由 PHP GC 管理，PHP 8 起 `FFI\CData` 对象被回收时会释放自己持有的那块内存，但从 `FFI::addr` 拿到的地址传给别人之后就不能再依赖这个时机。C 扩展开发是更彻底的一条路：`zend_module_entry` 注册函数、`ZEND_BEGIN_ARG_INFO` 声明参数、`zend_parse_parameters` 校验类型，任何一处漏检查都会让用户在 PHP 层触发原生错误；`valgrind --tool=memcheck php -d extension=your.so` 是标准验证流程。反射与序列化（`unserialize` 能绕过构造函数与 `readonly`、`__wakeup` 之前就能写入属性）是 PHP 里"私有"失效的主要途径，官方文档明确说 `unserialize` 不可用于不受信任的输入。

📘 [PHP · FFI 扩展](https://www.php.net/manual/en/book.ffi.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的保证是运行时保证：类型错误抛异常、越界给 `nil`、GC 管住对象；`Fiddle`、`ffi` gem 与 C 扩展是三条原生通道。它属于运行时保证这一类，最该先知道的是"扩展里缓存的 `VALUE` 不加引用就会被 GC 回收"。

```ruby
require "fiddle"

# Fiddle 是标准库里的 libffi 绑定：直接调 C 函数
libc = Fiddle.dlopen(nil)
strlen = Fiddle::Function.new(libc["strlen"], [Fiddle::TYPE_VOIDP], Fiddle::TYPE_LONG)
puts strlen.call("hello")            # 5

# Fiddle::Importer（require "fiddle/import"）只是语法糖：符号解析失败、
# 参数类型写错，后果都由扩展作者承担

# 反射同样能绕过可见性
class Secret
  private
  def hidden = "s3cr3t"
end
s = Secret.new
puts s.send(:hidden)                 # s3cr3t
puts Secret.private_instance_methods(false).include?(:hidden)   # true
```

`Fiddle::Function` 的签名表（`TYPE_VOIDP`、`TYPE_LONG`、`TYPE_INT` 等）是唯一的类型声明，写错就是读到错误的位模式；`Fiddle::Pointer` 的 `[]`/`[]=`/`to_s` 不做边界检查，`free` 由调用者负责。C 扩展里最核心的纪律是 GC 保护：调用可能触发 GC 的 API 之前必须用 `rb_gc_register_address` 或者把对象放在栈上保护，`TypedData` 的 `dfree` 回调里不能再访问被释放的对象，`rb_thread_call_without_gvl` 期间不能碰 Ruby 对象。`rb_thread_fd_close` 在 Ruby 4.0 起被废弃且变成空操作，需要暴露文件描述符时要用 `RUBY_IO_MODE_EXTERNAL` 配 `rb_io_close`，否则直接关闭 fd 会让挂起的 IO 操作进入未定义行为。反射上有 `send`、`instance_variable_get/set`、`define_method`、`TracePoint`、`ObjectSpace`，`ObjectSpace._id2ref` 在 4.0 起被废弃正是为了收紧这条通道。

📘 [Ruby · C 扩展](https://docs.ruby-lang.org/en/master/extension_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 常见问题与检测工具

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的内存问题分两类：safe 代码里几乎只剩内存增长与 `Rc` 环造成的逻辑泄漏，`unsafe` 代码里才会出现真正的 UB，所以工具链也分成"日常 lint"与"UB 检测"两层。它属于编译期保证这一类，最该先知道的是"Miri 与 sanitizer 都只在 nightly 上可用"。

```rust
// cargo clippy                                  静态 lint（stable 即可）
// warning: length comparison to zero
//   --> src/main.rs:3:8
//   3 |     if v.len() == 0 {
//     |        ^^^^^^^^^^^^ help: using `is_empty` is clearer and more explicit
//
// cargo test                                    普通单元测试
// cargo test -- --nocapture                     显示测试里的 stdout
//
// rustup +nightly component add miri            先装组件（nightly only）
// cargo +nightly miri test                      在解释器里跑测试，检测 UB 与数据竞争
// error: Undefined Behavior: memory access failed: attempting to access 4 bytes,
//        but got alloc291+0xc which is at or beyond the end of the allocation of size 12 bytes
//  --> src/main.rs:4:24
//   = help: see https://doc.rust-lang.org/nightly/reference/behavior-considered-undefined.html
//
// RUSTFLAGS="-Zsanitizer=address" cargo +nightly test --target aarch64-apple-darwin
// RUSTFLAGS="-Zsanitizer=thread"  cargo +nightly test --target aarch64-apple-darwin
// cargo geiger                                  统计依赖树里 unsafe 的密度（第三方）
// cargo audit                                   核对已披露漏洞（第三方）
// MIRIFLAGS="-Zmiri-many-seeds=0..16" cargo +nightly miri test   多探索几种线程交错
```

Miri 是一个 MIR 解释器，能抓到越界、use-after-free、未初始化读取、对齐错误、无效枚举判别值、数据竞争、别名违规（Stacked Borrows / Tree Borrows，二者都是实验性的），并在程序结束时报告泄漏。它的限制也很明确：它只解释 Rust 代码，遇到 FFI 会直接报 `unsupported operation: can't call foreign function`，所以绕过 FFI 的那部分代码检测不到；它只跑一种（或若干种）执行路径，跑不出 UB 不等于代码 sound；它也不保证与未来编译器版本的定义一致。sanitizer 走的是另一条路线：ASan 查越界与 use-after-free、TSan 查数据竞争、MSan 查未初始化读取，它们能覆盖 FFI 与真实硬件行为，代价是需要 nightly 的 `-Zsanitizer` 且必须指定 `--target`。日常排查内存增长用的是 `dhat`（堆剖析）、`heaptrack`、`valgrind --tool=massif`，CPU 侧用 `perf`、Instruments 或 `cargo flamegraph`。

📘 [Miri · README](https://github.com/rust-lang/miri#readme)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的日常问题集中在 ARC 的循环引用与 `Unsafe*` 指针的越界，工具上分三块：编译器自带的 sanitizer、Xcode/Instruments 的可视化排查、以及运行时的 `-Ounchecked` 对照实验。它属于运行时保证这一类，最该先知道的是"`swiftc -sanitize=address` 是查指针越界最快的办法"。

```swift
// swiftc -sanitize=address -g app.swift -o app && ./app
// =================================================================
// ==53749==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6030000022a0
// WRITE of size 8 at 0x6030000022a0 thread T0
//     #0 0x000104c90a40 in main app.swift:4
// 0x6030000022a0 is located 0 bytes after 16-byte region [0x603000002290,0x6030000022a0)
//
// swiftc -sanitize=thread -g app.swift -o app && ./app        TSan：数据竞争
// swiftc -sanitize=undefined -g app.swift -o app && ./app     UBSan：溢出与非法转换
// swiftc -O -g app.swift -o app && ./app                      优化构建：Unsafe 下标不再检查
// swiftc -Ounchecked app.swift -o app                         去掉全部运行时安全检查
// swift build -Xswiftc -sanitize=address                       SwiftPM 项目里加 sanitizer
//
// xcrun xctrace list templates                                Instruments 模板列表
// xcrun xctrace record --template 'Leaks' --launch ./app      泄漏检测
// xcrun xctrace record --template 'Allocations' --launch ./app 分配与引用计数
//
// swift test --enable-code-coverage                           覆盖率（顺带看未走到的路径）
```

`Leaks` 模板直接给循环引用的对象图，`Allocations` 模板看分配量与引用计数变化，`Zombies` 模板查 use-after-free；命令行下 `xcrun xctrace` 是这些模板的入口。ARC 类问题的另一个高效手段是在类的 `deinit` 里打日志，看看该析构的对象到底有没有析构——`deinit` 不打印，基本就是循环引用。`-Ounchecked` 会移除数组边界、整数溢出、强制解包等所有前置条件检查，它的用途不是"发布更快的版本"而是"验证这段代码是不是依赖了运行时检查"，一旦在它下面跑出诡异结果就说明前面某处已经越界。Linux 上还可以用 `swift run -Xswiftc -sanitize=address` 配合 `perf` 与火焰图。

📘 [Swift · 诊断与 sanitizer](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/memorysafety/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的问题几乎全部集中在数据竞争、goroutine 泄漏与内存增长三处，工具链也就围绕这三件事：`-race` 查竞争、pprof 查内存与 CPU、`go vet` 与 `runtime/metrics` 查静态与运行状态。它属于运行时保证这一类，最该先知道的是"race detector 只报它真的观察到的竞争，覆盖率靠测试负载"。

```go
// go vet ./...                                  静态检查（unsafe、格式串、锁拷贝等）
// （无输出即为干净）
//
// go build -gcflags='-m' ./...                  逃逸分析
// ./escape.go:7:25: &P{...} escapes to heap     这个对象跑到堆上了
// ./escape.go:8:6:  can inline sum
//
// go test -race ./...                           数据竞争检测
// ==================
// WARNING: DATA RACE
// Read at 0x00c000196188 by goroutine 11:
//   racetest.TestRace.func1()
//       /tmp/verify/ms/racetest/race_test.go:13
// Previous write at 0x00c000196188 by goroutine 9:
//   racetest.TestRace.func1()
//       /tmp/verify/ms/racetest/race_test.go:13
//
// go test -bench=. -benchmem ./...              基准与分配统计（B/op、allocs/op）
// go tool pprof -http=:8080 http://localhost:6060/debug/pprof/heap  堆剖析
// GODEBUG=gctrace=1 ./app                      每次 GC 打印一行统计
// GODEBUG=inittrace=1,allocfreetrace=1 ./app   初始化与逐次分配跟踪（后者极慢）
// go run runtime/metrics 示例                   读 /gc/heap/live:bytes 等稳定指标
```

`-race` 用的是 ThreadSanitizer 的 Go 版，官方给出的典型开销是内存占用增加 5 到 10 倍、执行时间增加 2 到 20 倍，所以只在测试与预发环境开；它报的是"观测到的竞争"，没报不等于没有，压力测试与并发用例覆盖度直接决定效果。goroutine 泄漏的排查入口是 `runtime.NumGoroutine()` 与 `pprof` 的 goroutine 视图（`debug=2` 能看到每个 goroutine 的栈），`time.Ticker` 忘记 `Stop`、向无缓冲 channel 发送且没人接收、`context` 没取消是三个高发点。内存增长用 `pprof` 的 heap 剖析加 `-base` 对比两个时间点的快照，`GOGC` 调大降低 GC 频率、`GOMEMLIMIT` 设软上限防止容器 OOM；`runtime/metrics` 是官方推荐的稳定指标入口，比自己去读 `runtime.MemStats` 更靠谱。

📘 [Go · 数据竞争检测器](https://go.dev/doc/articles/race_detector)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的内存问题基本等于"对象为什么没被释放"与"谁在一直分配"，标准库给的 `tracemalloc`、`gc`、`faulthandler` 已经能覆盖大部分场景。它属于运行时保证这一类，最该先知道的是"tracemalloc 的两份快照对比"是最省事的手法。

```python
import gc
import tracemalloc
import faulthandler

faulthandler.enable()              # 段错误时打印 Python 栈
tracemalloc.start()                # 开始跟踪分配

snap1 = tracemalloc.take_snapshot()
data = [bytearray(1000) for _ in range(100)]
snap2 = tracemalloc.take_snapshot()
top = snap2.compare_to(snap1, "lineno")[0]
print(top.size_diff > 0)           # True   净增长字节数
print(len(gc.get_objects()) > 0)   # True   当前被 GC 跟踪的对象数
print(tracemalloc.get_traced_memory()[0] > 0)   # True   当前跟踪到的字节数
tracemalloc.stop()
```

```python
python3 -X dev app.py                 开发模式：把 ResourceWarning 等默认关掉的东西打开
python3 -W error app.py               把警告升级成异常（pytest 用 -W error）
python3 -X tracemalloc=10 app.py      启动就开 tracemalloc 并保留 10 帧回溯
python3 -m pdb app.py                 交互式调试
py-spy dump --pid 1234                不重启进程看 Python 栈（第三方，采样式）
py-spy top --pid 1234                 实时 CPU 火焰视图
objgraph.show_most_common_types()     按类型统计对象数（第三方）
pympler.asizeof(obj)                  递归算对象真实占用（第三方）
memory_profiler：python3 -m memory_profiler app.py   逐行内存增长（第三方）
```

`tracemalloc` 的用法是"先 `take_snapshot()`，做一段操作，再 `take_snapshot()`，用 `compare_to` 按 `lineno`/`traceback` 排序"，这样能直接定位到增长的那一行；`gc.get_objects()` 配合 `gc.get_referrers` 可以顺着引用链找到"谁在持有它"。循环引用与 `__del__` 的组合要特别注意：有终结器的环在旧版本里会进 `gc.garbage` 永不回收，官方建议不要在 `__del__` 里依赖其他对象。C 层问题（段错误、越界）用 `faulthandler` 打印 Python 栈、用 `gdb --args python3 app.py` 看 C 栈、用 `valgrind --tool=memcheck` 跑 C 扩展，`-X dev` 与 `-W error` 则负责把"资源没关"升级成可见告警。

📘 [Python · tracemalloc](https://docs.python.org/3/library/tracemalloc.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的内存分析就是 JVM 的内存分析：堆转储看对象图、JFR 看事件流、async-profiler 看火焰图，另外还要盯住协程与 Android 生命周期带来的逻辑泄漏。它属于运行时保证这一类，最该先知道的是"Kotlin 侧没有专属工具，全部沿用 JVM 那套"。

```kotlin
// kotlinc -J-Xmx256m -include-runtime -d app.jar app.kt && java -jar app.jar
//
// java -Xlog:gc*:file=gc.log:time,uptime -jar app.jar       GC 日志（JDK 9+ 统一日志）
// jcmd <pid> GC.heap_info                                    当前堆各代使用量
// jcmd <pid> GC.class_histogram                              按类统计实例数与占用
// jcmd <pid> JFR.start duration=60s filename=rec.jfr && jfr print rec.jfr
// jmap -dump:live,format=b,file=heap.hprof <pid>             堆转储
// java -XX:+HeapDumpOnOutOfMemoryError -jar app.jar          OOM 时自动转储
//
// java -agentpath:/path/libasyncProfiler.so=start,event=cpu,file=cpu.html -jar app.jar
// java -jar jol-cli.jar internals java.lang.String           对象布局（JOL，第三方）
//
// Android：./gradlew :app:assembleDebug 后在 Profiler 里看 Memory / CPU
// LeakCanary 自动检测 Activity/Fragment 泄漏（第三方，Android 专用）
```

`jcmd` 是 JDK 自带的诊断入口，`GC.heap_info`、`GC.class_histogram`、`VM.native_memory`、`JFR.start` 都在里面；`JFR`（Java Flight Recorder）开销很低，适合常开，记录 GC、分配采样、锁竞争、线程等事件，`jfr print` 与 JDK Mission Control 都能读。堆转储用 Eclipse MAT 或 VisualVM 分析，MAT 的 dominator tree 与 leak suspects 报告是找"谁持有不释放"最快的路径。Kotlin 特有的排查点是协程：`GlobalScope`、没有取消的 `Job`、`runBlocking` 里嵌套长任务都会让对象活着，`kotlinx.coroutines` 的 `CoroutineExceptionHandler` 只能处理异常不能处理泄漏，结构化的 `coroutineScope`/`viewModelScope` 才是正解。CPU 与内存的火焰图统一用 async-profiler 生成，它同时支持事件类型 `cpu`、`alloc`、`lock`，是 JVM 上最省事的剖析器。

📘 [Java · JDK 诊断工具](https://docs.oracle.com/en/java/javase/25/troubleshoot/)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的诊断工具箱非常成熟：`jcmd`、JFR、JOL、JMH、MAT 覆盖"看现场、看事件、看布局、看性能、看对象图"五个方向。它属于运行时保证这一类，最该先知道的是"JOL 看布局、JFR 看事件，这两个配合基本能定位绝大多数内存问题"。

```java
// java -Xlog:gc*:file=gc.log:time,uptime:filecount=5,filesize=20M -jar app.jar
// （示例输出）[0.123s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 12M->3M(256M) 4.321ms
//
// jcmd <pid> GC.heap_info
// jcmd <pid> GC.class_histogram | head -20
// jcmd <pid> VM.native_memory summary                        （需 -XX:NativeMemoryTracking=summary）
// jcmd <pid> Thread.print -l                                 线程栈（含锁信息）
// jcmd <pid> JFR.start name=prof filename=app.jfr duration=120s
// jcmd <pid> JFR.dump  name=prof filename=app.jfr
// jfr view gc app.jfr                                        汇总视图
//
// jmap -dump:live,format=b,file=heap.hprof <pid>             堆转储，交给 MAT 分析
// java -XX:StartFlightRecording=filename=app.jfr,duration=60s -jar app.jar
// java -agentpath:libasyncProfiler.so=start,event=alloc,file=alloc.html -jar app.jar
//
// JOL：java -jar jol-cli.jar internals java.util.HashMap
// JMH：用 @Benchmark 写基准，避免手写计时被 JIT 骗
```

`-Xlog:gc` 是 JDK 9 起统一的日志框架，能同时输出 GC、类加载、JIT 编译等；G1 的日志里要看"Evacuation Pause"的停顿与"Mixed"回收是否跟上，ZGC/Shenandoah 则主要关注分配速率与并发周期是否跟得上。JOL（Java Object Layout）回答"这个对象到底占多少字节、字段怎么排、有没有被 `@Contended` 填充"，是排查"对象比想象中大"的利器。JMH 解决的是"手写 `System.nanoTime()` 会被 JIT 死代码消除、常量折叠、预热不足骗到"的问题。堆泄漏的定位流程是"`jcmd GC.class_histogram` 看哪个类实例数异常，再 `jmap` 转储、用 MAT 的 dominator tree 找到持有者"，`static` 集合、`ThreadLocal`、`ClassLoader` 是前三名嫌疑对象。CPU 与分配热点统一用 async-profiler 或 JFR 的采样视图。

📘 [Java · JFR 与诊断](https://docs.oracle.com/en/java/javase/25/troubleshoot/diagnostic-tools.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的检测工具链是这本对照里最完整也最必须的：Valgrind 家族管动态分析、sanitizer 管插桩检测、静态分析管编译期，再加上调试器与性能剖析。它属于没有安全保证这一类，最该先知道的是"sanitizer 比 Valgrind 快一个数量级，应该常驻 CI"。

```cpp
// 动态分析（Valgrind）
// valgrind --tool=memcheck --leak-check=full --track-origins=yes ./app
// ==1234== 16 bytes in 1 blocks are definitely lost in loss record 1 of 1
// valgrind --tool=massif ./app       堆剖析，配 ms_print 看峰值来源
// valgrind --tool=helgrind ./app     数据竞争与锁序问题
// valgrind --tool=callgrind ./app    指令级调用计数，配 kcachegrind 看图
//
// 插桩 sanitizer（编译期加，运行时快得多）
// clang++ -fsanitize=address -g app.cpp && ./a.out
// ==52009==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000100
// WRITE of size 4 at 0x602000000100 thread T0
// clang++ -fsanitize=undefined -fno-sanitize-recover=all app.cpp && ./a.out
// app.cpp:5:22: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
// clang++ -fsanitize=thread app.cpp && ./a.out
// WARNING: ThreadSanitizer: data race
// clang++ -fsanitize=memory app.cpp && ./a.out        未初始化读取（需全部代码插桩）
//
// 编译期与运行期加固
// clang++ -Wall -Wextra -Wconversion -fstack-protector-strong -D_FORTIFY_SOURCE=3 app.cpp
// clang-tidy app.cpp -- -std=c++23
// cppcheck --enable=all --inconclusive app.cpp
// gdb ./app  然后 break / run / bt / p obj / watch var
// perf record -g ./app && perf report         Linux CPU 火焰图（配 FlameGraph 脚本）
```

`memcheck` 抓越界、use-after-free、未初始化读取与泄漏，代价是 10 到 50 倍减速；`helgrind` 与 `drd` 抓数据竞争；`massif` 看堆峰值归因；`callgrind` 看指令级热点。sanitizer 的优势是速度（ASan 约 2 倍减速），所以可以放进 CI 跑全量测试；`-fsanitize=memory`（MSan）需要整条依赖链都插桩，实际使用门槛较高。`_FORTIFY_SOURCE` 与 `-fstack-protector-strong` 是运行期加固，主要防栈溢出与格式化串；`clang-tidy` 与 `cppcheck` 负责在没有测试覆盖的地方找问题。跨平台的热点分析用 `perf`（Linux）、Instruments（macOS）、VTune（Intel）、以及基于 `perf`/`DTrace` 采样生成的火焰图。

📘 [clang · Sanitizer 文档](https://clang.llvm.org/docs/index.html)

{{% /tab %}}

{{% tab header="C" %}}

C 的工具链与 C++ 完全共用：Valgrind 与 sanitizer 是主力，静态分析与编译器加固是补充。它属于没有安全保证这一类，最该先知道的是"`-fsanitize=address` 加 `-g` 能直接给出越界那一行的调用栈"。

```c
// 编译期把警告拉满
// clang -std=c23 -Wall -Wextra -Wconversion -Wcast-align -Wshadow -Wvla \
//       -fstack-protector-strong -D_FORTIFY_SOURCE=3 -g app.c -o app
// (void)x;                      /* 未使用变量在警告列表里也要处理干净 */
//
// 插桩 sanitizer
// clang -fsanitize=address -g app.c -o app && ./app
// ==52009==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000100
// WRITE of size 4 at 0x602000000100 thread T0
//     #0 0x000104a785e4 in main app.c:4
// 0x602000000100 is located 0 bytes after 16-byte region [0x6020000000f0,0x602000000100)
// clang -fsanitize=undefined -fno-sanitize-recover=all -g app.c -o app && ./app
// app.c:5:22: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
// clang -fsanitize=thread -g app.c -o app && ./app
// WARNING: ThreadSanitizer: data race
//   Write of size 4 at 0x000100ba0000 by thread T1:
//
// 动态分析
// valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all ./app
// valgrind --tool=helgrind ./app             数据竞争
// valgrind --tool=massif ./app               堆峰值
// gdb ./app     break / run / bt / x/16xb p / watch *p
// clang-tidy app.c -- -std=c23
// cppcheck --enable=all app.c
```

`ASan` 抓堆越界、栈越界、use-after-free、double free，`UBSan` 抓有符号溢出、移位越界、空指针解引用、对齐错误、无效的 `bool` 值，`MSan` 抓未初始化读取，`TSan` 抓数据竞争。Valgrind 不需要重编译但慢得多，好处是能查"编译时没带 `-g`"的二进制与部分库；`memcheck` 的 `definitely lost` 与 `indirectly lost` 是真正的泄漏，`still reachable` 通常可以忽略。`gdb` 的 `watch` 断点在追踪"谁改坏了这个变量"时特别有效，`x/16xb` 能直接看内存。生产环境的热点与内存增长用 `perf`、`heaptrack`、`Instruments`、`VTune` 处理，火焰图是统一的可视化形式。

📘 [clang · AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的排查重点是"哪里在分配"与"类型是否稳定"，工具是 `@allocated`、`@time`、`--track-allocation`、`Profile` 加 `JET.jl` 静态分析。它属于运行时保证这一类，最该先知道的是"`--track-allocation=user` 会写出逐行分配数，是最直接的一手材料"。

```julia
function churn(n)
    acc = 0
    for i in 1:n
        acc += sum([i, i])          # 每次迭代都在堆上分配
    end
    return acc
end

println(@allocated(churn(3)) > 0)   # true   这次调用分配的字节数
@time churn(1000)                   # （示例）0.000123 seconds (3.00 k allocations: 156.375 KiB)
                                    # 括号里的 allocations 就是总分配次数
@timev churn(1000)                  # 详细版：GC 时间、分配次数、字节数
println(Base.gc_bytes() > 0)        # true   累计 GC 字节数
println(Base.gc_num().pause >= 0)   # true   GC 暂停次数
println(@elapsed churn(1000) > 0)   # true   墙钟时间
```

```julia
julia --track-allocation=user script.jl     运行后生成 *.mem 文件，逐行给出分配字节数
julia --check-bounds=yes script.jl          强制打开边界检查（排查 @inbounds 引起的错误）
julia --heap-size-hint=2G script.jl         堆接近上限时更积极地回收
julia --project -e 'using Pkg; Pkg.test()'  跑测试
julia -e 'using Profile; Profile.@profile f(); Profile.print()'   采样剖析
julia -e 'using Profile; using PProf; @pprof f()'                 生成火焰图（PProf.jl）
julia -e 'using JET; @report_opt f(1)'                            静态分析类型不稳定（JET.jl）
```

`@time` 输出里 `allocations` 与 `KiB` 两列是判断热点的第一步，`@allocated` 给出单次调用的精确字节数，`--track-allocation=user` 在源文件同目录生成 `<源文件名>.mem`（例如 `script.jl.mem`），文件内每行对应源码一行的分配字节数，看哪一行数字最大就改哪一行。类型不稳定用 `@code_warntype`（红色标注 `Any`/`Union`）或者 `JET.jl` 的 `@report_opt`、`@report_call` 静态定位，效果比盲目加 `@inbounds` 好得多。CPU 侧用 `Profile` 标准库采样再 `Profile.print()`，图形化用 `PProf.jl` 出火焰图、`ProfileCanvas` 在 Jupyter 里出交互视图。`--check-bounds=yes` 是把 `@inbounds` 的保护重新打开用于排查的开关，`--heap-size-hint` 则是容器环境里防止内存涨过头的实用选项。

📘 [Julia · 性能剖析](https://docs.julialang.org/en/v1/manual/profile/)

{{% /tab %}}

{{% tab header="C#" %}}

.NET 的诊断工具是一整套 `dotnet-*` 全局工具，配合 Visual Studio 的诊断窗口与 Roslyn 分析器，覆盖计数器、跟踪、转储、GC 转储与基准五个方向。它属于运行时保证这一类，最该先知道的是"`dotnet-counters` 看趋势、`dotnet-gcdump` 看托管堆，这两个是第一步"。

```csharp
// dotnet tool install --global dotnet-counters
// dotnet tool install --global dotnet-trace
// dotnet tool install --global dotnet-dump
// dotnet tool install --global dotnet-gcdump
//
// dotnet-counters monitor -n MyApp --counters System.Runtime
// （示例输出）
// [System.Runtime]
//     % Time in GC (since last GC)                        0.12
//     Allocation Rate (B / 1 sec)                     1,234,567
//     GC Heap Size (MB)                                    42
//     Gen 0 GC Count                                       17
//
// dotnet-counters ps                          列出可附加的进程
// dotnet-trace collect -n MyApp --duration 00:00:30    采样跟踪，输出 .nettrace
// dotnet-trace convert --format speedscope trace.nettrace  转成火焰图可读格式
// dotnet-dump collect -p <pid>                全内存转储（SOS 分析）
// dotnet-gcdump collect -p <pid>              只抓托管堆，体积小得多
// dotnet-dump analyze core_dump               进入 SOS：dumpheap -stat / gcroot <addr>
//
// 代码侧：
// GC.GetTotalMemory(false)                    当前托管堆字节数
// GC.Collect(); GC.WaitForPendingFinalizers(); 强制回收（仅调试用）
// BenchmarkDotNet 基准：dotnet run -c Release
```

`dotnet-counters` 用 `System.Runtime` 计数器看分配速率、GC 堆大小、各代回收次数，`% Time in GC` 长期偏高说明分配压力过大。`dotnet-gcdump` 只在 GC 时抓取托管堆的图，文件比完整转储小很多，适合在生产上抓两次对比；`dotnet-dump` 是完整转储，配合 SOS 里的 `dumpheap -stat`（按类型统计）与 `gcroot`（顺着根找持有者）定位泄漏。Roslyn 分析器（`<AnalysisMode>All</AnalysisMode>`、`<TreatWarningsAsErrors>`、`EnableNETAnalyzers`）负责在编译期发现 `IDisposable` 未释放、`async void`、闭包捕获等问题；Visual Studio 的 Diagnostic Tools 与 BenchmarkDotNet 分别管交互式排查与严谨基准。另外要盯住 `IDisposable`/`IAsyncDisposable` 与原生句柄：托管内存不涨但句柄数涨，问题通常在 `SafeHandle` 之外。

📘 [MS Learn · .NET 诊断工具](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的内存排查靠 DevTools 的 Memory 视图加 `--observe`/`--enable-vm-service`，泄漏检测则有官方维护的 `leak_tracker` 包。它属于运行时保证这一类，最该先知道的是"`--observe` 打开 Observatory/DevTools 是标准入口"。

```dart
// dart run --observe bin/main.dart            打开 VM service（打印 DevTools 地址）
// dart run --enable-vm-service=8181 bin/main.dart
// dart compile exe bin/main.dart -o app        AOT 编译后在 DevTools 里附加
// flutter run --profile                        然后按提示打开 DevTools
//
// DevTools · Memory 视图的操作顺序：
//   1. 打一次堆快照（Snapshot）
//   2. 反复做可疑操作（例如进出页面 10 次）
//   3. 再打一次快照，选 Diff 比较新增对象
//   4. 按 class 排序，看谁的数量随操作次数线性增长
//
// dart pub global activate devtools && devtools        启动 DevTools
// dart test --coverage=coverage && dart pub global run coverage:format_coverage
//
// leak_tracker（第三方，官方 Flutter 团队维护）：
//   LeakTracking.wrapWithMemoryAvailability(); 检查某个对象是否真的被释放
//   expectNotLeaked(obj);                       测试里断言没有泄漏
```

DevTools 的 Memory 视图给两类信息：堆快照（对象数量、按类占用、支配树、引用链）与分配剖析（哪个函数的分配量最大）。排查"每次操作都涨一点"的泄漏，Diff 两份快照是最有效的路径，再顺着引用链找到持有者；Flutter 场景里最常见的持有者是 `State`、`BuildContext`、`StreamSubscription`、`AnimationController` 与静态单例。`leak_tracker` 把"对象应该在某个时机被释放"变成可以在单元测试里断言的检查，适合放进 CI。CPU 与帧率问题用 DevTools 的 Performance 视图和 `--profile` 构建，`flutter run --profile` 下才有真实性能数据；`dart:developer` 的 `Timeline` API 可以给自定义事件打标记。

📘 [Dart · DevTools](https://docs.flutter.dev/tools/devtools/memory)

{{% /tab %}}

{{% tab header="R" %}}

R 的内存排查工具是 `gc()`、`gcinfo(TRUE)`、`Rprofmem()`、`tracemem()` 加 `lobstr`、`pryr`、`profmem` 这几个包，配合 `valgrind` 检查原生代码。它属于运行时保证这一类，最该先知道的是"`lobstr::obj_size` 看真实占用、`Rprofmem` 看谁在分配"。

```r
# 基础观测
print(rownames(gc()))              # [1] "Ncells" "Vcells"
print(gc())                        # 行=Ncells/Vcells；列=used / gc trigger / max used（设限时含 limit）
gcinfo(TRUE)                       # 打开「每次 GC 打印统计」（返回上一次的标记值）
x <- vector("list", 10000)
gcinfo(FALSE)                      # 关闭 GC 消息
print(rownames(gc()))              # [1] "Ncells" "Vcells"

# 谁在分配
Rprofmem("mem.out")                # 记录每一次分配
y <- vector("list", 1000)
Rprofmem(NULL)
print(readLines("mem.out")[1:2])   # 每行一次分配，可能以 "new page:" 开头

# 谁被复制了（copy-on-modify）
v <- 1:5
tracemem(v)                        # 打印地址
w <- v                             # w 与 v 共享同一份数据
w[1] <- 0L                         # tracemem[0x... -> 0x...] 说明发生了复制
untracemem(w)

# 启动期参数（环境变量）
# R_MAX_VSIZE=8Gb                  向量堆上限
# R_GC_MEM_GROW=0..3               堆增长策略，越大越激进
# --min-vsize / --max-vsize        初始与最大向量堆
# 第三方（需要安装）
# lobstr::obj_size(x)              递归计算真实占用
# pryr::object_size(x)             同上，更老牌
# profmem::profmem({ x <- 1:1e6 }) 记录带调用栈的分配
# valgrind --tool=memcheck R -d valgrind -f script.R   检查 C 层
```

`gc()` 的各列分别是"当前使用量、下一次触发阈值、最大使用量（设置过上限时还多一列当前上限）"，`Vcells` 与 `Ncells` 分开计，向量数据看 `Vcells`；`gcinfo(TRUE)` 打开的是"每次 GC 打印一行统计"的开关，它本身不返回计数。`Rprofmem()` 输出的是"每一次分配发生在哪一行"，配合 `profmem` 包能拿到调用栈，是找"哪一行把内存吃光"的最直接手段。`tracemem()` 解决的是另一类问题：R 的 `copy-on-modify` 语义下，一次不小心的赋值会让大对象复制一份，`tracemem` 会在复制时打印地址变化，`lobstr::obj_addr` 也能看地址。数据框类的大对象建议用 `data.table`（按引用修改）或者 `arrow`/`duckdb`（数据留在磁盘/原生内存里），`Rcpp`/`RcppArmadillo` 的 C 层问题用 `valgrind --tool=memcheck R -d valgrind` 与 `gctorture()` 排查。

📘 [R · gc 与内存统计](https://stat.ethz.ch/R-manual/R-devel/library/base/html/gc.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的检测手段与它的设计一脉相承：分配器自己就是工具，加上 Debug 构建的运行时安全检查与 `--verbose-air` 看中间表示。它属于"安全模式可选"这一类，最该先知道的是"`std.testing.allocator` 会在测试结束时报告泄漏"。

```zig
const std = @import("std");

test "leak detection via testing allocator" {
    const gpa = std.testing.allocator;      // 结束时自动检查泄漏
    const p = try gpa.alloc(u8, 16);
    defer gpa.free(p);                      // 注释掉这一行 → 报 leak
    try std.testing.expect(p.len == 16);    // 通过
}

test "debug allocator reports leaks at deinit" {
    var gpa_state = std.heap.DebugAllocator(.{}){};
    defer _ = gpa_state.deinit();           // 有泄漏时返回 .leak 并在 stderr 打印
    const gpa = gpa_state.allocator();
    const p = try gpa.create(u32);
    defer gpa.destroy(p);
    p.* = 1;
    try std.testing.expect(p.* == 1);       // 通过
}

// 命令行：
// zig test src/main.zig                     跑测试，泄漏与断言都会报出来
// zig build test                            同上（走 build.zig）
// zig build-exe -ODebug   src/main.zig      运行时安全检查全开（默认构建模式）
// zig build-exe -OReleaseSafe src/main.zig  优化 + 安全检查
// zig build-exe -OReleaseFast src/main.zig  优化 + 安全检查全关（越界即 UB）
// zig build-exe --verbose-air src/main.zig  打印 Zig AIR，确认哪些检查被消除
// zig build-exe -fsanitize-c src/main.zig   不安全构建下开启 C 未定义行为检测
// zig build-exe -fsanitize-thread src/main.zig   Thread Sanitizer（构建选项）
// valgrind --tool=memcheck ./app            检查 C 侧与生成代码
```

`std.heap.DebugAllocator`（0.15 之前的名字是 `GeneralPurposeAllocator`）在 Debug 与 ReleaseSafe 下启用，会检测泄漏、双重释放、释放后使用与越界，并在 `deinit()` 时输出摘要；`std.testing.allocator` 是它的测试专用包装，任何忘记 `free`/`deinit` 的路径都会让测试失败，这是 Zig 项目里最有效的纪律工具。安全模式的四种构建模式差别是硬性的：Debug 与 ReleaseSafe 会 panic 于整数溢出、越界、`null` 解引用、非法类型转换，ReleaseFast 与 ReleaseSmall 不做这些检查（按官方推荐这时把 allocator 换成 `std.heap.smp_allocator`），所以"用 ReleaseSafe 发版"是很多项目的默认选择。`--verbose-air` 与 `--verbose-llvm-ir` 用来看编译器实际生成了什么，是确认 `@inbounds` 式的假设有没有生效（或者有没有被误消除）的手段。

📘 [Zig · 构建模式与安全](https://ziglang.org/documentation/master/#Build-Mode)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的排查工具很精简：`collectgarbage` 看内存、`debug` 库看栈与局部变量、`luacheck` 做静态检查，LuaJIT 还有 `-jv` 与 `-jdump`。它属于运行时保证这一类，最该先知道的是"`collectgarbage("count")` 是最直接的内存读数"。

```lua
-- 内存读数与手动回收
print(collectgarbage("count"))        -- 例如 24.53（单位 KB）
local t = {}
for i = 1, 1000 do t[i] = string.rep("x", 100) end
print(collectgarbage("count"))        -- 明显变大
t = nil
collectgarbage("collect")             -- 手动跑一次完整回收
print(collectgarbage("count"))        -- 回落到接近初始值

-- debug 库看运行时信息
local function f(a, b) return debug.getinfo(1, "nSl") end
print(f(1, 2).currentline ~= nil)     -- true
print(debug.traceback("here", 1))     -- here\nstack traceback:...

-- 命令行工具
-- luacheck script.lua                静态检查：未定义全局、未使用变量、行宽
-- luac -l script.lua                 列出字节码（看常量表与闭包）
-- lua -e 'print(collectgarbage("count"))'
-- luajit -jv script.lua              跟踪 JIT 编译过程（哪些函数被编译、为什么没编译）
-- luajit -jdump script.lua           输出生成的机器码
-- valgrind --tool=memcheck lua script.lua   检查 C 侧与扩展
-- lua -e 'collectgarbage("generational")' 切换 GC 模式
```

Lua 的内存问题基本是"强引用链太长"：模块级表当缓存、闭包捕获大表、`package.loaded` 里的模块、注册表里只增不减的条目。因为 Lua 的 GC 是自动且无法被精确控制何时回收，观测的常规手法是"打印 `collectgarbage("count")`，执行可疑操作，再打印一次"，两次的差值就是这段操作的净增长；`collectgarbage("step")` 可以在对延迟敏感的场合手动推进回收。`debug` 库是双刃剑：`debug.getlocal`、`debug.setupvalue`、`debug.sethook` 能让代码访问任何局部变量与上值（upvalue），非常适合调试，也彻底破坏了可见性，生产环境里通常用 `debug = nil` 或 sandbox 把它屏蔽。LuaJIT 侧要额外注意 `-jv` 的输出里"NYI: 不支持的操作导致回退到解释器"这一类信息，它往往同时解释了 CPU 热点与分配激增。

📘 [Lua 5.5 · collectgarbage](https://www.lua.org/manual/5.5/manual.html#pdf-collectgarbage)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的检测 = JavaScript 的运行时工具加编译期静态检查，前者用 Chrome DevTools 与 Node 的诊断能力，后者用 `tsc --noEmit` 与 ESLint 的类型规则。它属于编译期静态检查这一类，最该先知道的是"类型检查再严也抓不到内存泄漏，堆快照才是"。

```typescript
// 编译期
// npx tsc --noEmit                          只做类型检查，不产出文件
// npx tsc --noEmit --strict --noUncheckedIndexedAccess   把最严的开关全打开
// npx eslint . --ext .ts                    类型感知的 lint（@typescript-eslint）
// npx tsc --generateTrace trace             生成编译性能跟踪
//
// 运行时（Node）
// node --inspect-brk dist/main.js           打开 Inspector，Chrome 里 chrome://inspect
// node --trace-gc dist/main.js              打印每次 GC（实测输出形如）：
//   [53606:0xaf740c000]       10 ms: Scavenge 4.4 (6.3) -> 4.3 (7.3) MB, 0.21 / 0.00 ms
// node --cpu-prof --heap-prof dist/main.js  直接产出 .cpuprofile / .heapprofile
// node --max-old-space-size=512 dist/main.js
// process.memoryUsage()                     代码里读 heapUsed/heapTotal/rss
//
// 浏览器：DevTools → Memory → Heap snapshot → 操作 → 再拍一张 → Comparison 视图
// clinic.js：clinic doctor / clinic flame / clinic heap  一体化诊断（第三方）
```

Node 侧的排查顺序通常是"`process.memoryUsage()` 或 `--trace-gc` 确认是不是真的在涨"，"`--heap-prof` 或 `--inspect` 抓堆快照定位到具体类型"，"Comparison 视图看两次快照之间哪些对象数量增加"。浏览器侧同一套思路，DevTools 的 Memory 面板提供 Heap snapshot、Allocation instrumentation on timeline、Allocation sampling 三种视图，其中 timeline 视图最适合找"每次操作都涨一点"的泄漏。`clinic.js` 把 CPU、事件循环延迟、内存、火焰图整合成一次运行，适合服务端排查。编译期这边真正与内存/资源相关的是 `noUncheckedIndexedAccess`（把越界的 `undefined` 变成静态可见）、`strict`、以及 ESLint 的 `@typescript-eslint/no-floating-promises`（未处理的 Promise 会让闭包与资源一直挂着），但它们仍然抓不到引用链问题。编译器自身也在换代：TypeScript 7 的编译器是 Go 重写的原生实现（microsoft/typescript-go），官方给出的口径是编辑器加载约 8 倍、完整构建约 10 倍提升，构建期内存占用下降一成到两成多（7.0 公告的多仓库实测为减少 6% 到 26%），类型检查语义与现有 `tsc` 保持一致，所以上面这套排查流程不变，只是跑得更快。

📘 [Node.js · 诊断与内存](https://nodejs.org/en/learn/diagnostics/memory)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的检测工具就是引擎自己的诊断能力：DevTools 的 Memory 面板、Node 的 Inspector 与 `--trace-gc`、以及 `process.memoryUsage()`。它属于运行时保证这一类，最该先知道的是"`--trace-gc` 看趋势、堆快照看对象，两者配合就能定位绝大多数泄漏"。

```javascript
// V8 分代 GC 的痕迹：新生代 Scavenge 频繁但便宜，老生代 Mark-Compact 才昂贵
// node --trace-gc app.js
// [53606:0xaf740c000]       10 ms: Scavenge 4.4 (6.3) -> 4.3 (7.3) MB, pooled: 0 MB, 0.21 / 0.00 ms
// [53606:0xaf740c000]       11 ms: Scavenge 6.6 (11.6) -> 6.6 (11.6) MB, pooled: 0 MB, 0.08 / 0.00 ms

const arr = [];
for (let i = 0; i < 5; i++) arr.push(new Array(100000).fill(i));
console.log(process.memoryUsage().heapUsed > 0);   // true
console.log(process.memoryUsage().heapTotal > 0);  // true

// node --expose-gc app.js 之后可以手动回收，仅用于排查
if (globalThis.gc) { globalThis.gc(); console.log("gc forced"); }

// node --inspect-brk app.js       Chrome 打开 chrome://inspect 附加
// node --cpu-prof --heap-prof app.js
// node --max-old-space-size=512 app.js
console.log(typeof globalThis.gc);   // undefined（没加 --expose-gc 时）
```

`--trace-gc` 的输出里，`Scavenge` 是新生代回收、`Mark-Compact` 是老生代回收，如果老生代回收后堆大小仍持续上升，就说明对象真的被长期持有；`--max-old-space-size` 只限制老生代，`--max-semi-space-size` 调新生代大小。堆快照的比较是定位泄漏的标准流程：DevTools Memory 面板拍两张快照后在 Comparison 里按 `Delta` 排序，再用 Retainers 面板看"谁在持有它"。浏览器里还要注意游离 DOM（从 DOM 树摘下但仍被 JS 引用）与 Detached HTMLElement 的数量，DevTools 会在快照里直接标出来。除了内存，Node 侧的事件循环延迟用 `perf_hooks.monitorEventLoopDelay()` 或 `clinic doctor` 观察，CPU 热点用 `--cpu-prof` 或 `clinic flame` 生成火焰图。

📘 [Chrome DevTools · 内存面板](https://developer.chrome.com/docs/devtools/memory)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的排查工具是 `memory_get_usage` 家族加 `gc_status`、Xdebug、以及 Valgrind 与 OPcache 的统计。它属于运行时保证这一类，最该先知道的是"长驻进程里 `memory_get_usage(true)` 与 `false` 的两个数字含义不同"。

```php
<?php
echo memory_get_usage(), "\n";          // 1234567     PHP 层实际使用的字节数
echo memory_get_usage(true), "\n";      // 2097152     向系统申请的内存块大小
echo memory_get_peak_usage(), "\n";     // 2345678     本请求峰值

$obj = new stdClass();
$obj->self = $obj;                      // 自引用
unset($obj);
echo gc_collect_cycles(), "\n";         // 1          循环收集器回收的环数
print_r(gc_status());                   // runs / collected / threshold / roots
echo gc_mem_caches(), "\n";             // 0          释放 Zend 内存缓存，返回释放的字节数

$before = memory_get_usage();
$data = array_fill(0, 1000, str_repeat("x", 100));
echo (memory_get_usage() - $before > 0) ? "grew\n" : "same\n";   // grew
unset($data);
echo gc_mem_caches() >= 0 ? "ok\n" : "no\n";                     // ok
```

```php
php -d memory_limit=256M -d zend.enable_gc=1 -d opcache.enable_cli=1 script.php
php -i | grep -E "opcache|memory_limit"          当前配置
php -d xdebug.mode=develop,trace script.php      Xdebug 开发模式 + 函数跟踪
php -d xdebug.mode=profile script.php            生成 cachegrind 文件，用 KCachegrind 看
php -r 'var_dump(gc_status());'
valgrind --tool=memcheck php -d extension=your.so script.php    检查扩展的 C 层
valgrind --tool=massif php script.php                           堆峰值来源
opcache_get_status()['opcache_statistics']        OPcache 命中率与缓存使用量（常驻进程）
```

`memory_get_usage()` 不含 `false` 时给的是 PHP 分配器统计到的用量，`true` 时给的是向系统申请的内存块大小，两者差值就是分配器内部的碎片与预留；`memory_get_peak_usage()` 是判断"这个请求会不会撞 `memory_limit`"的依据。`gc_status()` 里的 `roots` 是当前待检查的循环根数量、`runs` 是收集器运行次数，长驻进程（Swoole、RoadRunner、队列 worker）应该定期 `gc_collect_cycles()` 并监控 `memory_get_usage()` 是否只增不减。`gc_mem_caches()` 释放 Zend 内存管理器缓存的空闲块，能立刻降低 RSS，是长驻进程里常用的手段。扩展层面的问题（段错误、越界）只能靠 Valgrind 与 `gdb`：`valgrind --tool=memcheck php -d extension=...` 是最标准的一条命令，Xdebug 只覆盖 PHP 层。

📘 [PHP · 内存与 GC 函数](https://www.php.net/manual/en/function.memory-get-usage.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的观测入口是 `GC.stat` 与 `ObjectSpace`，热点分析靠 `stackprof`，内存增长分析靠 `memory_profiler`，JIT 侧有 `--yjit-stats`。它属于运行时保证这一类，最该先知道的是"`GC.stat[:heap_live_slots]` 是判断是否真在泄漏的第一指标"。

```ruby
before = GC.stat[:heap_live_slots]
objs = Array.new(10_000) { |i| +"s#{i}" }        # 造 1 万个字符串
after = GC.stat[:heap_live_slots]
puts after > before                               # true   存活槽位增长
puts ObjectSpace.count_objects[:TOTAL] > 0        # true   当前对象总数

GC.start
puts GC.stat[:count] >= 0                         # true   GC 运行次数
puts GC.stat.keys.include?(:heap_allocated_pages) # true   堆页数

objs = nil
GC.start
puts GC.stat[:heap_live_slots] < after            # true   释放后回落

require "objspace"
puts ObjectSpace.count_objects_size[:TOTAL] > 0   # true   各类对象的字节数
puts GC.stat[:heap_free_slots] >= 0               # true   空闲槽位
```

```ruby
ruby --yjit-stats script.rb        退出时打印 YJIT 统计
***YJIT: Printing YJIT statistics on exit***
method call fallback reasons:
    (all relevant counters are zero)
./configure --enable-yjit=stats && ruby --yjit-stats script.rb   ratio_in_yjit 需要 configure 时开启
ruby --zjit script.rb               ZJIT（4.0 起实验性方法级 JIT，需 Rust 1.85+ 构建）
RUBY_GC_HEAP_INIT_SLOTS=100000 ruby script.rb     调初始堆槽位数
RUBY_GC_HEAP_GROWTH_FACTOR=1.1 ruby script.rb     调堆增长因子
RUBY_GC_HEAP_OLDOBJECT_LIMIT_FACTOR=1.5 ruby script.rb
ruby -robjspace -e 'p ObjectSpace.count_objects'
# 第三方：
# gem install memory_profiler && ruby -r memory_profiler -e 'MemoryProfiler.report { ... }.pretty_print'
# gem install stackprof && stackprof --mode wall tmp/stackprof.dump
# gem install heapy && heapy dump
```

`GC.stat` 里最值得盯的是 `heap_live_slots`（存活对象数）、`heap_allocated_pages`、`heap_free_slots`、`count`（GC 次数）与 `time`（GC 累计耗时）：稳态下 `heap_live_slots` 应该在一个区间内波动而不是单调上升，单调上升基本就是泄漏。定位用 `ObjectSpace.each_object` 按类型统计、`memory_profiler` 给出"每个 gem / 每一行分配了多少对象与字节"、`stackprof` 给 CPU 与墙钟采样。Ruby 4.0 的 GC 改动（不同 size pool 独立增长、大对象页清扫更快、`id2ref` 表按需创建、`Random`/`StringScanner` 等对象加写屏障）都直接影响长驻进程的常驻内存，升级版本后应重新对比 `GC.stat` 的基线。`--yjit-stats` 与 `RubyVM::YJIT.runtime_stats` 用于确认 JIT 是否真的生效，4.0 起 `ratio_in_yjit` 需要在 `configure` 时加 `--enable-yjit=stats` 才有数据。

📘 [Ruby · GC.stat](https://docs.ruby-lang.org/en/master/GC.html#method-i-stat)

{{% /tab %}}

{{< /tabpane >}}
