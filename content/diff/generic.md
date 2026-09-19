+++
title = "泛型"
date = 2026-09-19T12:00:00+08:00
weight = 15
type = "docs"
description = "18 种语言的泛型对照：定义与约束、型变、实现模型、运行时类型与反射"
isCJKLanguage = true
draft = false
+++

# 泛型：18 种语言对照

泛型的写法只是表层，真正的分歧藏在这四个子主题里：**怎么写约束**（trait bound、concept、interface 类型集、协议约束、docblock 注解）、**子类型关系怎么传导**（协变、逆变、不变）、**代码最终怎么生成**（单态化、类型擦除、具体化）、**运行时还剩多少类型信息**（`typeof(T)`、`TypeId`、反射、完全擦掉）。这四件事互相牵制：选了单态化就换来性能但失去异构容器，选了擦除就换来代码体积但拿不到 `T`，选了具体化就保住了反射却背上 CLR/VM 的运行时元数据。本页先把 18 种语言放到同一张速览表里对齐，再逐个主题展开。按「语言本身是否提供类型参数」统计（口径：本文件 18 种语言全算），完全没有类型参数的 6 种是 C、Lua、R、Ruby、PHP、JavaScript，它们分别用 `void *` 加 `_Generic`、元表、S3/S4 分派、duck typing、docblock 加 PHPStan/Psalm、JSDoc `@template` 顶替；其余 12 种（Rust、Swift、Go、Python、Kotlin、Java、C++、Julia、C#、Dart、Zig、TypeScript）都有类型参数，但各有短板——Go 与 Zig 没有型变概念，Python 的类型参数只活在注解里，Java 的类型实参擦除后不剩，C# 的声明处型变只覆盖接口与委托。

## 泛型

**一页速览**

| 语言 | 泛型写法（有没有 / 关键字） | 实现模型 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | `fn f<T: Bound>(x: T)`、`where`、`const N: usize`、`impl Trait` | 单态化，零成本抽象，泛型本身无型变 | 编译时间与二进制膨胀；异构集合要 `dyn Trait` |
| Swift | `func f<T: P>(_: T)`、`where`、`some`、`any` | witness table + 特化，类型元数据保留 | `any` 装箱有开销；协议无声明处型变 |
| Go | `func F[T C](x T)`、约束接口、`~int \| string` | GC shape stenciling + 字典（部分单态化） | union 类型集只能作约束；泛型方法 1.27 才有 |
| Python | `class C[T]`（3.12+）、`TypeVar`、`Protocol` | 运行时类型对象 + 注解对象 | 运行时不强制；`T` 是 `TypeVar` 而非具体类型 |
| Kotlin | `class C<T>`、`<T : Any>`、`where`、`inline fun <reified T>` | JVM 上擦除，`reified` 靠 inline 撑 | `is T` 只能配 reified；星投影会丢类型 |
| Java | `class C<T extends Bound>`、`<? extends T>`、`<? super T>` | 类型擦除 + 桥方法 | 不能 `new T[]`；`instanceof List<String>` 不合法 |
| C++ | `template<class T>`、concepts、`requires`、可变参数模板 | 模板实例化即单态化 | 错误信息很长；分离编译要显式实例化 |
| C | 没有；用 `void *` + `_Generic` + 宏 | 无类型参数，只有运行时代码 | `void *` 丢类型；`_Generic` 只做编译期分派 |
| Julia | `struct S{T}`、`where`、抽象类型 | 每个具体类型组合都生成特化代码 | 参数化类型不变；`Vector{Int}` 不是 `Vector{Real}` |
| C# | `class C<T> where T : notnull, new()`、泛型数学 | CLR 具体化（reified），运行时保留 `T` | 约束顺序有讲究；`class` 约束下 `==` 是引用比较 |
| Dart | `class C<T extends Bound>`、F-bounds | reified，运行时保留类型实参 | 泛型按声明处协变，越界写入靠运行时检查 |
| R | 没有；S3/S4/R5/R6 泛型函数 | 运行时按 class 属性分派 | `UseMethod` 只看第一个参数；S3 不校验签名 |
| Zig | `fn f(comptime T: type, x: T)`、`anytype` | comptime 展开，等价于单态化 | 没有 trait；`anytype` 只能用在参数上 |
| Lua | 没有；动态类型 + 元表 | 无编译期泛型 | 类型信息跟着值走；错误在运行时才暴露 |
| TypeScript | `function f<T extends B>(x: T)`、条件类型、映射类型 | 完全编译期擦除，产物里没有类型 | 运行时拿不到 `T`；`as` 不做任何转换 |
| JavaScript | 没有；JSDoc `@template` | 无 | 注释不参与运行；约束只能手写检查 |
| PHP | 没有；docblock `@template` + PHPStan/Psalm | docblock 由外部静态分析器读 | 语言层面零检查；运行时无泛型 |
| Ruby | 没有；duck typing | 无 | 只能等运行时 `TypeError`；RBS/Sorbet 是外部工具 |

### 定义与约束

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的泛型是编译期单态化的类型参数，约束通过 `trait bound` 表达，属于静态检查、零成本抽象这一类。最该先记住的是：`T: Bound` 与 `where T: Bound` 完全等价，而 `const N: usize` 把「值」也提到了类型参数的位置上；`impl Trait` 则是把类型名字匿名化的语法糖。

```rust
use std::fmt::Display;

// 泛型参数 + trait bound
fn largest<T: PartialOrd + Copy>(list: &[T]) -> T {
    let mut max = list[0];
    for &x in list { if x > max { max = x; } }
    max
}
// where 子句：约束多或带关联类型时更清楚
fn show<T>(x: T) -> String where T: Display { format!("{x}") }
// const 泛型：长度进入类型系统
fn sum_arr<const N: usize>(a: [i32; N]) -> i32 { a.iter().sum() }
// impl Trait：返回位置匿名类型（这里类型名写不出来）
fn evens() -> impl Iterator<Item = i32> { (1..=6).filter(|x| x % 2 == 0) }

fn main() {
    println!("{}", largest(&[3, 7, 2]));              // 7
    println!("{}", show(1.5));                        // 1.5
    println!("{}", sum_arr([1, 2, 3]));               // 6
    println!("{:?}", evens().collect::<Vec<_>>());    // [2, 4, 6]
}
```

`const` 泛型让 `[i32; 3]` 与 `[i32; 4]` 成为两个不同的类型，`sum_arr` 会为每个长度各单态化一份，所以长度参数适合小整数。`impl Trait` 在返回位置只允许唯一的具体类型，写 `-> impl Iterator` 时调用方无法命名该类型，也就无法把它作为结构体字段——需要保存到字段就要换成 `Box<dyn Iterator<Item = i32>>`，代价是一次堆分配加动态分派。约束过宽是最常见的坑：只写 `T: Copy` 却在函数体里调用 `format!` 会直接编译失败，把 bound 改成 `T: Display` 或补上 `T: Display + Copy` 即可；trait 之间还可以用 `trait Sortable: Ord + Copy` 这样的 supertrait 一次性带上多个约束。

📘 [Rust · 泛型](https://doc.rust-lang.org/book/ch10-01-syntax.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的泛型是编译期静态检查加运行时元数据并存的一套机制：`<T: Protocol>` 与 `where` 子句表达约束，`some` 表示「编译期已知但对外匿名的一个具体类型」，`any` 表示运行时装箱的 existential。最该先知道的是 `some` 与 `any` 的语义完全不同，前者没有装箱开销，后者是一次类型擦除的容器。

```swift
import Foundation

// 泛型函数 + 协议约束
func largest<T: Comparable>(_ xs: [T]) -> T {
    var max = xs[0]
    for x in xs where x > max { max = x }
    return max
}
// where 子句约束多个参数
func pair<A, B>(_ a: A, _ b: B) -> String
    where A: CustomStringConvertible, B: CustomStringConvertible { "\(a)/\(b)" }
// some：不透明返回类型，具体类型由实现决定、对外隐藏
func evens() -> some Sequence<Int> { [2, 4, 6] }
// any：existential，运行时装箱，每个元素都带元数据
func total(_ s: any Sequence<Int>) -> Int { s.reduce(0, +) }

struct Stack<Element> {
    private var storage: [Element] = []
    mutating func push(_ e: Element) { storage.append(e) }
    var top: Element? { storage.last }
}
// 主要关联类型（Swift 5.7+）：Collection<Int> 直接写出元素类型
func countInts<C: Collection<Int>>(_ c: C) -> Int { c.count }

print(largest([3, 7, 2]))                    // 7
print(pair(1, "a"))                          // 1/a
print(Array(evens()))                        // [2, 4, 6]
print(total([1, 2, 3]))                      // 6
var st = Stack<Int>(); st.push(9)
print(st.top!)                               // 9
print(countInts([1, 2, 3]))                  // 3
let boxed: any Collection = [1, 2]
print(boxed.count)                           // 2
```

`some Sequence<Int>` 是「反向泛型」：由被调用方选定一个具体类型，调用方只能把它当 `Sequence<Int>` 用，因此可以零开销地内联与特化。`any Sequence<Int>` 则是把值装进 existential 容器，关联类型被擦掉但元数据保留，方法调用走 witness table 的间接调用；把 `any` 用在热路径上是常见的性能陷阱，而把 `some` 当成「泛型版接口」返回又会限制实现只能有一个具体类型。协议里用 `associatedtype` 声明关联类型时，泛型参数不能直接当类型用（不能写 `[P]`），这正是引入 `any P` 与主要关联类型的原因。

📘 [Swift · 泛型](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 1.18 起有了类型参数，约束写成接口（constraint interface），属于编译期静态检查，运行时靠反射兜底。最该先知道的是约束接口里的 union（`int | string`）只能当约束使用，不能用来声明变量，所以「类型集」是纯编译期概念。

```go
package main

import "fmt"

// 1.18+：类型参数写在方括号里，约束是一个接口
func Sum[T int | float64](xs []T) T {
	var total T
	for _, x := range xs { total += x }
	return total
}

// 约束接口可以复用：union 只允许出现在约束位置
type Number interface{ ~int | ~int64 | ~float64 } // ~ 表示"底层类型是"

// 约束也可以带方法，方法是类型集与调用能力同时具备
type Stringer interface {
	~string
	fmt.Stringer
}

// Go 1.27：具体类型的方法可以声明自己的类型参数
type Box[T any] struct{ v T }

func (b Box[T]) Map[R any](f func(T) R) Box[R] { return Box[R]{f(b.v)} }

func main() {
	fmt.Println(Sum([]int{1, 2, 3}))       // 6
	fmt.Println(Sum([]float64{1.5, 2.5}))  // 4
	fmt.Println(Box[int]{3}.Map(func(i int) string { return fmt.Sprint(i * 2) })) // {6}
	var s fmt.Stringer = nil
	_ = s
}
```

约束接口里的 `~T` 表示「底层类型是 `T`」的所有类型，这让 `type MyInt int` 这类定义类型也能满足约束；不写 `~` 时只有类型本身算数。`any` 是 `interface{}` 的别名，等价于无约束。最要紧的坑是类型集约束不能当普通类型用：`var n Number = 1` 会得到 `cannot use type Number outside a type constraint: interface contains type constraints`，因为类型集里根本没有可调用的方法集。Go 1.27 起具体类型的方法可以带类型参数，写法是 `func (b Box[T]) Map[R any](...)`，但接口方法仍然不能声明类型参数，泛型方法也不能用来满足接口方法。

📘 [Go spec · 类型参数声明](https://go.dev/ref/spec#Type_parameter_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的泛型是「运行时注解对象 + 静态类型检查器」的两层结构：3.12 引入 PEP 695 的 `class C[T]` 语法，把类型参数变成了语言层面的声明。最该先知道的是这些类型参数在运行时并不强制，`Stack[int]` 只是一个可下标的别名对象，装什么进去都不报错。

```python
from typing import Protocol, TypeVar, Callable

T = TypeVar("T")                       # 传统写法：TypeVar + 上界用 bound=
TNum = TypeVar("TNum", bound=int)      # 约束上界

# Protocol：结构化约束（鸭子类型的静态版）
class Sized(Protocol):
    def __len__(self) -> int: ...

# PEP 695（3.12+）：类型参数写在名字后面
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()

def first[T](xs: list[T]) -> T: return xs[0]

type Pair[T] = tuple[T, T]             # 3.12+ 泛型类型别名

print(first([1, 2, 3]))                # 1
s: Stack[int] = Stack()
s.push(1); s.push(2)
print(s.pop())                         # 2
print(Stack.__type_params__)           # (T,)
print(Stack[int])                      # __main__.Stack[int]
print(first(["a", "b"]))               # a
```

`TypeVar` 支持 `covariant=True`、`contravariant=True` 与 `infer_variance=True`，`ParamSpec` 用于装饰器转发参数，`TypeVarTuple` 用于变长元组；PEP 695 把泛型声明统一成 `class C[T]`、`def f[T]()`、`type Alias[T] = ...` 三处语法，但它创建的类型参数默认 `infer_variance=True`，型变由类型检查器推断，语法里不能再写 `out`/`in`。运行时唯一留下的痕迹是 `__type_params__` 属性，以及用 `Box[int](...)` 实例化时 CPython 设置的 `__orig_class__`（这不是语言保证，只是描述符实现细节）。常见陷阱是把 `list[T]` 当作运行时可判别的类型：`isinstance(x, list[int])` 会抛 `TypeError`，因为 `list[int]` 是 `types.GenericAlias`，不能用于 `isinstance`。

📘 [Python · typing 泛型](https://docs.python.org/3/library/typing.html#user-defined-generic-types)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的泛型在 JVM 上是擦除的，声明处型变（`out`/`in`）与 `where` 子句是它的特色，而 `inline fun <reified T>` 是唯一能在运行时拿到 `T` 的逃生舱。最该先知道的是空安全会影响约束写法：默认上界是 `Any?`，想排除 `null` 要显式写 `<T : Any>`。

```kotlin
// 声明处协变：Producer<Dog> 可以当 Producer<Animal> 用
interface Producer<out T> { fun produce(): T }
// 声明处逆变：Consumer<Animal> 可以当 Consumer<Dog> 用
interface Consumer<in T> { fun consume(item: T) }

// 多个上界用 where，且只能有一个类上界
fun <T> render(item: T): String where T : CharSequence, T : Comparable<T> = item.toString()

// reified：必须 inline，才能在运行时使用 T
inline fun <reified T> isOf(value: Any): Boolean = value is T
inline fun <reified T> typeName(): String = T::class.qualifiedName ?: "?"

class Stack<T : Any> {                       // 非空上界
    private val items = mutableListOf<T>()
    fun push(item: T) { items.add(item) }
    fun pop(): T = items.removeAt(items.size - 1)
}

fun main() {
    val p: Producer<Any> = object : Producer<String> { override fun produce() = "s" }
    println(p.produce())        // s
    println(isOf<String>("a"))  // true
    println(isOf<Int>("a"))     // false
    println(typeName<List<Int>>())  // kotlin.collections.List
    println(Stack<Int>().apply { push(1) }.pop())  // 1
}
```

`out`/`in` 是声明处型变，写一次就影响所有使用点；`MutableList<T>` 这类同时读写 `T` 的类型则天生不变，只能用使用处型变 `MutableList<out T>` 投影成只读视角。星投影 `List<*>` 等价于 `List<out Any?>`，能读不能写；把 `MutableList<*>` 当 `MutableList<Any?>` 用会编译失败。`reified` 的代价是函数会被内联到每个调用点，递归的 inline 函数写不出来，而且 `typeOf<T>()` 返回的是 `KType`，泛型实参会被擦成 `List` 这一类原始名字。

📘 [Kotlin · 泛型：in, out, where](https://kotlinlang.org/docs/generics.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的泛型是纯粹的编译期检查、运行期擦除：`class C<T extends Bound>` 里的 `T` 编译后变成 `Bound` 或 `Object`，约束用 `extends` 写（没有单独的 `where`）。最该先知道的是「上界」用 `extends` 表示，哪怕是接口也用 `extends`，而 `&` 可以写多个上界。

```java
import java.util.List;
import java.util.ArrayList;

// 上界用 extends，多个上界用 &（类必须在最前）
class Repo<T extends Number & Comparable<T>> {
    private final List<T> items = new ArrayList<>();
    void add(T t) { items.add(t); }
    // 静态方法不能使用类的类型参数，必须自己声明
    static <U> U first(List<U> xs) { return xs.get(0); }
    // 通配符：? extends 只读（Producer）
    static double sum(List<? extends Number> src) {
        double s = 0;
        for (Number n : src) s += n.doubleValue();
        return s;
    }
    // 通配符：? super 只写（Consumer）
    static void fill(List<? super Integer> dst) { dst.add(1); }
}

// Java 25+ 紧凑源文件：实例 main 不需要类外壳
void main() {
    Repo<Integer> r = new Repo<>();
    r.add(3);
    System.out.println(Repo.first(List.of(1, 2, 3)));      // 1
    System.out.println(Repo.sum(List.of(1, 2, 3)));        // 6.0
    List<Number> dst = new ArrayList<>();
    Repo.fill(dst);
    System.out.println(dst.size());                        // 1
    // src.add(1) 与 Integer x = dst.get(0) 都不合法，见下方说明

    // 类型参数推断：菱形运算符 + 目标类型
    List<String> empty = new ArrayList<>();
    System.out.println(empty.size());                      // 0
}
```

类型参数推断（Java 8 起大幅增强）让 `var list = new ArrayList<String>()`、`Repo.first(List.of(1))` 这类写法不必显式写实参；`<>` 菱形语法把实参交给目标类型推断。`T` 只能是引用类型，所以 `List<int>` 不合法，必须写 `List<Integer>` 并承担装箱。最常见的两个坑是：`T` 在运行时不存在，所以 `new T[10]`、`new T()`、`instanceof T`、`T.class` 全都不合法，要创建数组只能 `(T[]) new Object[n]` 并接受未检查警告；以及泛型可变参数 `T...` 会产生堆污染，必须用 `@SafeVarargs`（只能标注 `static`、`final`、`private` 方法）承诺不往数组里塞异类元素。

📘 [Java 教程 · 泛型](https://docs.oracle.com/javase/tutorial/java/generics/index.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的模板是编译期展开的代码生成器，`concepts` 与 `requires`（C++20）把原来靠 SFINAE 硬凑的约束变成了可读语法。最该先知道的是模板参数可以是类型、非类型（值）与模板本身三类，而且支持全特化与偏特化。

```cpp
#include <concepts>
#include <cstdio>
#include <string>
#include <vector>

// 类型参数 + concept 约束
template <std::integral T>
T twice(T v) { return v + v; }

// requires 子句表达复合要求
template <class T>
    requires requires(T a, T b) { a + b; }
auto add(T a, T b) { return a + b; }

// 非类型模板参数（C++20 起支持浮点与类类型）
template <std::size_t N>
struct Fixed { int data[N]; };

// 可变参数模板：递归展开的经典写法
template <class... Ts>
std::size_t countArgs(Ts... ) { return sizeof...(Ts); }

// 偏特化：只为指针类型换一套实现
template <class T> struct Describe { static const char* name() { return "value"; } };
template <class T> struct Describe<T*> { static const char* name() { return "pointer"; } };

int main() {
    std::printf("%d\n", twice(21));                       // 42
    std::printf("%d\n", add(1, 2));                       // 3
    std::printf("%zu\n", sizeof(Fixed<4>));               // 16
    std::printf("%zu\n", countArgs(1, 2.0, "x"));         // 3
    std::printf("%s\n", Describe<int>::name());           // value
    std::printf("%s\n", Describe<int*>::name());          // pointer
}
```

`concept` 是可复用的具名约束，`requires` 既能直接写内联要求也能引入具名 concept；被约束的模板在实参不满足时给出的错误信息比 SFINAE 时代清晰得多，这是 C++20 之后最实际的可读性收益。非类型模板参数让 `Fixed<4>` 与 `Fixed<8>` 成为不同类型。最常见的坑有三个：模板必须定义在头文件里（或在使用点可见），否则链接期报未定义符号，因为实例化发生在编译单元内部；想在 `.cpp` 里预实例化并让别处复用，要用显式实例化 `template struct Fixed<4>;` 配合 `extern template` 声明；可变参数模板的 `sizeof...` 只数个数，真正展开要用折叠表达式或递归，写错会得到成百上千行的实例化回溯。

📘 [cppreference · 模板](https://en.cppreference.com/w/cpp/language/templates)

{{% /tab %}}

{{% tab header="C" %}}

C 没有泛型，没有类型参数，也没有模板；语言提供的两个替代品是 `void *`（把类型信息交给调用者自己记）和 `_Generic`（C11 起的编译期类型分派宏）。最该先知道的是 `_Generic` 只在编译期选表达式，选完就没了，运行时什么也不剩。

```c
#include <stdio.h>
#include <stdlib.h>

/* _Generic：编译期按类型选表达式，等价于"宏版重载" */
#define type_name(x) _Generic((x),      \
    int: "int", long: "long",           \
    double: "double", char *: "char *", \
    default: "other")

/* 参数化宏：把类型名当参数传进去，文本展开出一堆同名函数 */
#define DECLARE_SUM(name, type) type name(type x, type y) { return x + y; }
DECLARE_SUM(sum_i, int)
DECLARE_SUM(sum_d, double)

/* void*：容器能装任何东西，但类型标签得自己带 */
typedef struct { void *data; size_t elem; size_t len; } AnyVec;

static int cmp_int(const void *a, const void *b) {
    return (*(const int *)a) - (*(const int *)b);
}

int main(void) {
    printf("%s %s %s\n", type_name(1), type_name(1.0), type_name("x"));
    /* int double char * */
    printf("%d %.1f\n", sum_i(1, 2), sum_d(1.5, 2.5));   /* 3 4.0 */
    int xs[5] = {3, 1, 4, 1, 5};
    qsort(xs, 5, sizeof xs[0], cmp_int);   /* 泛型算法靠函数指针补回类型 */
    AnyVec v = { xs, sizeof(int), 5 };
    printf("%zu %d\n", v.len, ((int *)v.data)[4]);        /* 5 5 */
    return 0;
}
```

`qsort` 是 C 里「泛型算法」的标准范式：数据用 `void *` 传，元素大小用参数传，比较逻辑用函数指针传——三样东西把编译期的类型信息全部拆成了运行时的数据。`_Generic` 的关联列表必须是完整类型，`const` 修饰与数组会退化成指针，所以 `type_name("x")` 匹配的是 `char *`；没列进列表的类型落到 `default`，这一点和 C++ 的函数重载不同，不会报错。宏方案的主要问题是每个实例都是一份独立的代码（体积变大），而且宏参数没有类型检查，`DECLARE_SUM(sum_s, char *)` 会静默生成一个指针相加的奇怪函数。

📘 [cppreference · `_Generic`](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 用参数化类型（parametric type）与抽象类型（abstract type）表达泛型，约束靠抽象类型和 `where` 子句，属于动态语言里少见的「运行时靠类型分派、编译期按具体类型特化」的组合。最该先知道的是参数化类型是不变的：`Vector{Int}` 不是 `Vector{Real}` 的子类型。

```julia
abstract type Animal end
struct Dog <: Animal end
struct Cat <: Animal end

# 参数化类型：字段类型由参数决定
struct Box{T}
    value::T
end

# where 子句约束类型参数
speak(x::T) where {T<:Animal} = "$(T) speaks"
# 抽象元素类型的容器：靠 Union 或抽象类型
struct Zoo{T<:Animal}
    animals::Vector{T}
end

# 抽象类型的容器可以放任意子类型
zoo = Animal[Dog(), Cat()]
println(length(zoo))              # 2
println(speak(Dog()))             # Dog speaks
b = Box(42)
println(typeof(b))                # Box{Int64}
println(b.value)                  # 42
println(Vector{Int} <: Vector{Real})   # false —— 参数化类型不变
println(Vector{Int} <: AbstractVector) # true  —— 抽象类型才有子类型关系
println(Box{Int} <: Box)               # true  —— UnionAll 是上界
```

参数化类型的不变性是有意的：如果 `Vector{Int}` 是 `Vector{Real}` 的子类型，那么往里面写 `Float64` 就会破坏 `Vector{Int}` 的内存布局。想写「接受任意元素类型」的函数，要写成 `f(v::Vector{T}) where {T<:Real}` 或 `f(v::AbstractVector{<:Real})`，而不是 `f(v::Vector{Real})`。抽象类型（`Real`、`Integer`、`Number`）构成类型树的上层，具体类型是叶子；`Union{Int,String}` 也是合法的类型，可以用在字段与分派里。`Vector{Real}` 是合法类型但通常不是你要的：它是「元素类型恰好为 `Real`（抽象类型）的向量」，能装任何 `Real` 子类型，代价是每个元素都装箱。

📘 [Julia · 类型](https://docs.julialang.org/en/v1/manual/types/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的泛型是 CLR 层面具体化（reified）的：类型实参保留到运行时，`typeof(T)`、`default(T)`、`new T()` 都能用。约束统一写成 `where T : 约束` 的子句，最该先知道的是约束的种类很多而且顺序有讲究。

```csharp
using System;
using System.Numerics;
using System.Collections.Generic;

// 基类 / 接口 / 构造 / 非空：约束用 where 写在类型参数后面
class Repo<T> where T : notnull, IComparable<T>, new()
{
    public T Create() => new T();          // new() 才能这样写
    public int Compare(T a, T b) => a.CompareTo(b);
}

static class Demo
{
    // 泛型数学：static abstract 成员（.NET 7 起）
    public static T Sum<T>(T[] xs) where T : IAdditionOperators<T, T, T>, IAdditiveIdentity<T, T>
    {
        T total = T.AdditiveIdentity;
        foreach (var x in xs) total += x;
        return total;
    }
    // 非托管约束：只有它才能对 T 用 sizeof
    public static int SizeOf<T>() where T : unmanaged => sizeof(T);
    // 泛型方法自己声明类型参数
    public static U Map<T, U>(T v, Func<T, U> f) => f(v);
    // 具体化的直接证据：typeof(T) 在运行时给出真实类型
    public static Type TypeOfT<T>() => typeof(T);
    public static T Zero<T>() where T : struct => default(T);
}

class Empty { }

class Program
{
    static void Main()
    {
        Console.WriteLine(Demo.Sum(new[] { 1, 2, 3 }));      // 6
        Console.WriteLine(Demo.Sum(new[] { 1.5, 2.5 }));     // 4
        Console.WriteLine(Demo.Map(3, x => x.ToString()));   // 3
        Console.WriteLine(Demo.TypeOfT<List<int>>());        // System.Collections.Generic.List`1[System.Int32]
        Console.WriteLine(Demo.Zero<int>());                 // 0
        Console.WriteLine(Demo.SizeOf<long>());              // 8
        Console.WriteLine(new Repo<string>().Compare("a", "b") < 0);   // True
        Console.WriteLine(new Repo<Empty>().Create() is Empty);        // True
    }
}
```

`where T : struct` 隐含 `new()`，所以两者不能同时写；`unmanaged` 隐含 `struct`；`notnull` 违反时只给警告而不是错误；`new()` 必须放在最后（只有 `allows ref struct` 这类反约束可以跟在它后面）。CLR 的具体化让 `typeof(T)` 与 `new T()` 都能工作，也让每个值类型实参各自生成一份代码——这正是泛型集合对 `int` 没有装箱开销的原因。C# 13 引入的 `allows ref struct` 是一条「反约束」，声明类型实参可以是 `ref struct`，此时该类型参数不能被装箱、不能当 `static` 字段；C# 14 的扩展成员（extension members）也能写在泛型参数上，例如 `extension<TDelegate>(TDelegate source) where TDelegate : System.Delegate`。常见坑是对 `where T : class` 的类型参数用 `==`：编译器只能选引用相等，即使实参重载了 `==` 也仍然比较引用，要值相等必须约束 `IEquatable<T>`。

📘 [MS Learn · 类型参数约束](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/constraints-on-type-parameters)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型是具体化（reified）的：类型实参在运行时保留，`x is List<String>` 能正常工作，`T` 也能用在 `is` 判断里。约束只有一种写法 `T extends Bound`，最该先知道的是上界默认是 `Object?`，要非空就写 `T extends Object`。

```dart
// 上界用 extends；默认上界是 Object?，写 Object 表示非空
class Cache<T extends Object> {
  final _store = <String, T>{};
  void set(String k, T v) => _store[k] = v;
  T? get(String k) => _store[k];
}

// F-bounds：上界引用自己（自引用类型参数）
abstract class Comparable2<T extends Comparable2<T>> {
  int compareTo(T other);
}

// 泛型方法自己声明类型参数
T first<T>(List<T> xs) => xs.first;
Map<K, V> group<K, V>(List<V> xs, K Function(V) key) =>
    {for (final x in xs) key(x): x};

void main() {
  final c = Cache<String>();
  c.set('a', 'x');
  print(c.get('a'));                 // x
  print(first([1, 2, 3]));           // 1
  print(group([1, 2, 3], (x) => x.isEven).length);  // 2
  final xs = <String>['a'];
  print(xs is List<String>);         // true —— reified，能看到类型实参
  print(xs is List<int>);            // false
  print(<Object>[] is List<String>); // false
}
```

Dart 的泛型是可具体化的，这一点与 Java 的擦除形成鲜明对照：Java 里 `list instanceof List<String>` 是编译错误，Dart 里 `xs is List<String>` 是合法且真的会做检查的表达式。代价是每个类型实参组合都会产生独立的运行时类型对象与检查代码，`List<int>` 与 `List<String>` 在 VM 上是不同的类型。F-bounds 用于表达「我能和自己同类型的对象比较」，写成 `T extends Comparable2<T>`，`class Foo extends Comparable2<Foo>` 才算合法。泛型的边界只在编译期决定能否调用成员，越界写入的检查依赖运行时，所以 `List<num>` 变量指向 `List<int>` 是合法的转换，但往里写 `1.5` 会在运行时抛错。

📘 [Dart · 泛型](https://dart.dev/language/generics)

{{% /tab %}}

{{% tab header="R" %}}

R 没有泛型，也没有类型参数；它的「泛型函数」指的是 S3/S4/R5/R6 这套按类分派的机制（generic function + method dispatch）。最该先知道的是 `UseMethod()` 只根据**第一个参数**的 class 属性去找方法，这既是它的全部威力也是它最大的限制。

```r
# S3 泛型函数：函数体只写 UseMethod，具体实现按第一个参数的 class 找
speak <- function(x, ...) UseMethod("speak")

speak.default <- function(x, ...) "unknown"
speak.dog <- function(x, ...) "woof"
speak.cat <- function(x, ...) "meow"

d <- structure(list(), class = "dog")
print(speak(d))                    # [1] "woof"

# NextMethod：沿 class 向量继续向下分派
speak.puppy <- function(x, ...) paste("small", NextMethod())
p <- structure(list(), class = c("puppy", "dog"))
print(speak(p))                    # [1] "small woof"

# 没有类型参数，用 do.call 把函数名当字符串来"参数化"
apply_fun <- function(fname, args) do.call(fname, args)
print(apply_fun("sum", list(1:3)))  # [1] 6
print(inherits(d, "dog"))           # [1] TRUE
```

S3 的 class 属性就是字符串向量，`UseMethod` 按顺序查找 `speak.puppy`、`speak.dog`、`speak.default`，所以继承关系靠字符串约定而不是编译器。S4 用 `setGeneric()` 与 `setMethod()` 声明签名，可以按多个参数分派；R5（引用类）与 R6 在 S4 之上提供了更现代的面向对象写法，`rlang` 包则提供了 `S3` 的 tidy 版分派与 `dispatch_args` 之类的工具。常见的坑是 S3 方法没有签名校验：`speak.dog` 少写一个参数不会报错，直到真正调用时才发现；另外 `NextMethod()` 不能接受参数名与形参冲突的写法，需要显式传 `...`。数学上的「泛型」在这里并不存在，`sum()`、`mean()` 这类函数本身就是 S3 泛型，能处理向量、矩阵、因子等多种输入。

📘 [R 语言定义 · 方法分派](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatch)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有泛型语法、没有 trait，也没有类型类；它用编译期参数（`comptime T: type`）与 `anytype` 让函数按需对类型展开，等价于单态化。最该先知道的是「约束」在 Zig 里就是 `comptime` 里的分支判断，不满足条件时用 `@compileError` 主动报错。

```zig
const std = @import("std");

// comptime 类型参数：T 是编译期已知的 type 值
fn twice(comptime T: type, x: T) T {
    return x + x;
}

// anytype：形参类型由调用点推断，必须在函数体内自证可用
fn show(x: anytype) void {
    const T = @TypeOf(x);
    switch (@typeInfo(T)) {
        .int, .comptime_int => std.debug.print("int {}\n", .{x}),
        .float, .comptime_float => std.debug.print("float {}\n", .{x}),
        else => std.debug.print("other {s}\n", .{@typeName(T)}),
    }
}

// 结构化"约束"：编译期检查字段是否存在，否则报错
fn firstField(x: anytype) @TypeOf(x[0]) {
    comptime {
        if (@typeInfo(@TypeOf(x)) != .array and @typeInfo(@TypeOf(x)) != .pointer)
            @compileError("need an array or slice, got " ++ @typeName(@TypeOf(x)));
    }
    return x[0];
}

pub fn main() void {
    std.debug.print("{}\n", .{twice(i32, 21)});   // 42
    show(1);                                     // int 1
    show(1.5);                                   // float 1.5
    std.debug.print("{}\n", .{firstField([_]i32{ 7, 8 })}); // 7
}
```

`comptime T: type` 与 `anytype` 的区别在于显式程度：前者要求调用点写清类型（可以只看签名就知道 T 是什么），后者完全由实参推断（`@TypeOf` 是唯一拿到类型的手段）。`@typeInfo` 是 Zig 的编译期反射入口，返回 `std.builtin.Type` 联合体，可以据此分派到不同分支；Zig 0.14 起该联合体的标签与字段改为小写风格（`.int`、`.float`、`.pointer`、`.@"struct"`），从 0.13 及更早版本迁移的代码需要同步改这些名字。因为一切都是 comptime 展开，写错约束的报错发生在编译期而不是运行期，但代价是每个类型组合都生成一份代码，而且 `anytype` 不能用在返回值位置，也不能作为结构体字段类型。

📘 [Zig · comptime](https://ziglang.org/documentation/master/#comptime)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有泛型，也没有类型参数：它是动态类型语言，变量只绑定值不绑定类型，容器的「元素类型」只能靠约定。最该先知道的是 Lua 的替代方案是元表（metatable）与元方法，把「行为」延迟到运行时按值决定。

```lua
-- 没有类型参数，表可以装任何东西
local function push(list, v) list[#list + 1] = v end
local function map(list, f)
  local out = {}
  for i, v in ipairs(list) do out[i] = f(v) end
  return out
end

local mixed = {}
push(mixed, 1); push(mixed, "a"); push(mixed, 2.5)
print(#mixed, mixed[2], math.type(mixed[1]))   -- 3	a	integer

local doubled = map({1, 2, 3}, function(x) return x * 2 end)
print(table.concat(doubled, ","))              -- 2,4,6

-- 元表：用 __index / __add 把"类型行为"绑到值上
local Vec = {}
Vec.__index = Vec
Vec.__add = function(a, b) return setmetatable({x = a.x + b.x}, Vec) end
Vec.__tostring = function(v) return "Vec(" .. v.x .. ")" end
local v = setmetatable({x = 1}, Vec) + setmetatable({x = 2}, Vec)
print(tostring(v))                             -- Vec(3)
print(type(v), getmetatable(v) == Vec)         -- table	true
```

Lua 的「泛型」体现在高阶函数与元表上：`map`/`filter`/`reduce` 这类函数对元素类型没有任何要求，因为 Lua 值自带类型标签（`type()` 返回 `"number"`、`"string"`、`"table"` 等），运算符会查元方法。想给自定义类型实现运算符重载，就在元表里放 `__add`、`__lt`、`__eq`、`__index`、`__call`，这样同一段泛型代码就能作用到用户类型上。代价是全部在运行时：写错类型的错误要到执行到那一行才暴露，也不存在编译期约束；想补充静态检查只能靠 LuaLS/LuaCATS 的注解注释，它们和 TypeScript 的 `as` 一样不产生运行时代码。Lua 5.5 把 `global` 变成了保留字、for 控制变量只读，这些语言层面的收紧与泛型无关，但会影响旧代码迁移。

📘 [Lua 5.5 · 元表与元方法](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的泛型完全活在编译期：类型参数、约束、条件类型、映射类型都会在生成 JavaScript 时被彻底擦掉，属于「静态检查、运行时零残留」。最该先知道的是类型系统本身是图灵完备的结构化系统，泛型不只是「占位符」，还能做类型层面的计算。

```typescript
// 泛型 + 约束 + 默认类型参数
function pick<T extends object, K extends keyof T = keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const out: Partial<T> = {};
  for (const k of keys) out[k] = obj[k];   // Partial<T> 写入合法
  return out as Pick<T, K>;
}

// 条件类型 + infer：在类型层面做模式匹配
type ElementOf<T> = T extends readonly (infer U)[] ? U : never;
type Flatten<T> = T extends Array<infer U> ? Flatten<U> : T;

// 映射类型 + 键重映射
type Getters<T> = { [K in keyof T as `get${Capitalize<string & K>}`]: () => T[K] };

// const 类型参数（TS 5.0）：字面量不被拓宽
function tuple<const T extends readonly unknown[]>(xs: T): T { return xs; }

const p = pick({ a: 1, b: "x" }, ["a"]);
console.log(p);                                   // { a: 1 }
const t = tuple([1, "a"]);                        // 类型是 readonly [1, "a"]
console.log(t);                                   // [1, 'a']
type E = ElementOf<string[]>;                     // string
type F = Flatten<number[][][]>;                   // number
type G = Getters<{ a: number }>;                  // { getA: () => number }
console.log(typeof pick);                         // function（泛型没留下任何痕迹）
```

`pick` 演示了三件常用手段：`K extends keyof T` 把键约束到 `T` 的键集合，默认参数 `= keyof T` 让调用点可省略，返回值用内置的 `Pick<T, K>` 组合。条件类型里的 `infer` 是类型层面的变量绑定，`Flatten` 用递归条件类型展开嵌套数组；映射类型配合 `as` 键重映射能批量改写属性名。TS 4.7 起可以在类型参数上写可选的型变标注 `in`/`out`（`interface Producer<out T>`），这不会改变运行时代码，但能让编译器更早发现型变冲突并加速类型检查；TS 5.0 的 `const` 类型参数让数组/对象字面量按只读元组推断，不再被拓宽成 `string[]`。最大的坑是忘记运行时没有类型：`as` 与类型参数都不做任何转换与检查，从 `any` 或网络数据构造出来的值只有手写类型守卫（`function isUser(x: unknown): x is User`）才能真正保证安全。

📘 [TS 手册 · 泛型](https://www.typescriptlang.org/docs/handbook/2/generics.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有泛型，也没有类型参数：它只有运行时值，类型信息附在值上而不是变量上。最该先知道的是「写泛型」在 JS 里只能靠 JSDoc 注释或 TypeScript 之类的超集，注释本身不参与执行、也不做任何检查。

```javascript
// JSDoc 的泛型注释：编辑器/tsc --checkJs 能读，运行时是纯注释
/**
 * @template T
 * @param {T[]} xs
 * @returns {T}
 */
function first(xs) { return xs[0]; }

/**
 * @template {{ id: number }} T
 * @param {T[]} xs
 * @returns {Map<number, T>}
 */
function indexById(xs) {
  const m = new Map();
  for (const x of xs) m.set(x.id, x);
  return m;
}

console.log(first([1, 2, 3]));                       // 1
console.log(first(["a"]));                           // a
console.log(indexById([{ id: 1 }, { id: 2 }]).get(2)); // { id: 2 }
console.log(typeof first, first.length);             // function 1
console.log(first.toString().includes("@template")); // false：注释不进函数体
```

JSDoc 的 `@template` 与 TypeScript 的类型参数一一对应，`tsc --checkJs` 或编辑器的 TS 语言服务会据此做检查，但生成的产物里连注释都可能被压掉。约束在 JSDoc 里写成 `@template {string} T` 或 `@template {{ id: number }} T`，属于结构性约束——只要值有 `id` 字段就满足。因为没有任何编译期机制，所有安全性都得靠运行时守卫：`Array.isArray`、`typeof`、`instanceof`、`Object.hasOwn` 以及手写的类型断言函数是唯一的保证手段。实践上推荐的做法是把泛型逻辑写成接收回调的高阶函数（`map`、`filter`、`reduce`），让「类型」体现为函数形状而不是类型参数，这样既符合 JS 的运行时模型，也能被 JSDoc 与 TS 正确推断。

📘 [MDN · JavaScript 数据类型](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Data_structures)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有泛型，语言层面既不支持类型参数也不支持泛型类；标准做法是把类型写在 docblock 的 `@template` 注解里，交给 PHPStan 或 Psalm 这类静态分析器检查。最该先知道的是这些注解对 PHP 运行时完全透明，运行时拿不到任何类型实参。

```php
<?php
declare(strict_types=1);

/**
 * @template T
 */
final class Stack
{
    /** @var list<T> */
    private array $items = [];

    /** @param T $item */
    public function push(mixed $item): void { $this->items[] = $item; }

    /** @return T */
    public function pop(): mixed { return array_pop($this->items); }
}

/**
 * @template T
 * @param list<T> $xs
 * @param callable(T): bool $keep
 * @return list<T>
 */
function filterList(array $xs, callable $keep): array {
    return array_values(array_filter($xs, $keep));
}

$s = new Stack();
$s->push(1);
echo $s->pop(), PHP_EOL;                       // 1
// PHPStan 会报错：Parameter #1 $item of method Stack<int>::push() expects int, string given
$s->push("oops");
echo implode(",", filterList([1, 2, 3, 4], fn(int $x): bool => $x % 2 === 0)), PHP_EOL; // 2,4
echo (new ReflectionClass(Stack::class))->getMethods()[0]->getName(), PHP_EOL; // pop
```

注解只是注释：`@template T` 让 PHPStan 把 `Stack` 当成 `Stack<T>` 处理，但 PHP 引擎看到的仍然是一个 `mixed` 参数的普通类。若把 `mixed` 换成具体类型（例如 `int $item`），就得到了「非泛型但类型安全」的写法——这也是 PHP 里最常见的选择：要么放弃复用性换取类型检查，要么保留 `mixed`/`object` 并接受注解带来的外部检查。PHP 8.0 起支持的 union 类型（`int|string`）、8.1 起的 `never`/`readonly` 属性、8.4 起的属性钩子（property hooks）都只是具体类型的组合或访问器逻辑，不能表达「对任意 `T` 成立」。需要注意 `@template` 的位置：只有写在类或函数的 docblock 顶部、并且由分析器识别时才生效，写错标签名（例如 `@T`）会被静默忽略。

📘 [PHP · 类型系统](https://www.php.net/manual/en/language.types.declarations.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有泛型，也没有类型参数：它是彻底的动态类型语言，约束靠 duck typing——不看你是什么类，只看你响应哪些方法。最该先知道的是「类型错误」在 Ruby 里是运行时异常，抛出点是真正调用到不存在的方法那一刻。

```ruby
# 没有类型参数：容器装什么都行，方法能不能响应由运行时决定
class Stack
  def initialize = @items = []
  def push(x) = @items.push(x)
  def pop = @items.pop
  def each(&blk) = @items.each(&blk)
  include Enumerable            # 混入 Enumerable 就白得 map/select/sum
end

s = Stack.new
s.push(1); s.push("a"); s.push(2.5)
puts s.pop                    # 2.5
puts s.map(&:class).inspect   # [Integer, String]

# 约束 = 检查方法是否存在，而不是检查类
def describe(x)
  if x.respond_to?(:each)
    "iterable(#{x.each.count})"
  else
    "scalar(#{x.class})"
  end
end
puts describe([1, 2, 3])      # iterable(3)
puts describe(42)             # scalar(Integer)

begin
  [1, "a"].sum                # 只有运行到这里才炸
rescue TypeError => e
  puts "#{e.class}: #{e.message}"   # TypeError: String can't be coerced into Integer
end
```

`respond_to?`、`is_a?`、`Enumerable` 混入构成了 Ruby 版的「泛型」：不声明元素类型，而是声明「我接受任何能 `each` 的东西」。这与 Go 的类型集约束在意图上相似，但一个在编译期、一个在运行时。静态化方案只能靠外部工具：Sorbet 的 `sig` 签名与 RBS 的 `.rbs` 文件能描述 `Array[Integer]` 这样的参数化类型，但它们都需要额外的类型检查器（`srb tc`、Steep）并且不改变运行时行为。常见坑是 `Array#sum` 之类的内置方法对元素类型有隐含要求，混入不兼容元素时不会在 `push` 时报错，而是在聚合时才抛 `TypeError`；另一个坑是 `respond_to?` 默认不含 `private` 方法，需要传 `true`。

📘 [Ruby · 模块与混入](https://docs.ruby-lang.org/en/master/Module.html)

{{% /tab %}}

{{< /tabpane >}}

### 型变

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有继承意义上的子类型，所以泛型参数本身谈不上协变或逆变；真正有型变的是**生命周期**，编译器自动为每个类型推导出协变、逆变或不变。最该先知道的是 `&'a T` 对 `'a` 协变、`&'a mut T` 对 `T` 不变，这条规则直接决定了你能不能把长生命周期的引用塞进短生命周期的地方。

```rust
// 协变：&'long T 可以用在期望 &'short T 的位置
fn use_short<'a>(s: &'a str) -> usize { s.len() }

// 不变：&mut 引用对内部类型不变，'a 被钉死
fn overwrite<'a>(slot: &mut &'a str, v: &'a str) { *slot = v; }

// 函数参数位置逆变：fn(&'short str) 可填入要求 fn(&'static str) 的槽
fn needs_static(f: fn(&'static str) -> usize) -> usize { f("abc") }
fn takes_any<'a>(s: &'a str) -> usize { s.len() }

fn main() {
    let s: &'static str = "static";
    println!("{}", use_short(s));             // 6  ✅ 协变
    println!("{}", needs_static(takes_any));  // 3  ✅ 参数位置逆变
    let slot: &'static str = "a";
    println!("{slot}");                       // a
    // let local = String::from("local");
    // overwrite(&mut slot, &local);          // 🛑 `local` does not live long enough
}
```

`PhantomData<T>` 是手动指定型变的开关：默认情况下 `PhantomData<T>` 让结构体表现得「拥有一个 `T`」，于是继承 `T` 的型变；想强制协变写 `PhantomData<fn() -> T>`，想逆变写 `PhantomData<fn(T)>`，想不变写 `PhantomData<*mut T>` 或 `PhantomData<Cell<T>>`。泛型参数 `T` 本身没有型变，是因为 Rust 里 `Vec<Derived>` 与 `Vec<Base>` 之间根本不存在子类型关系——没有继承就没有型变问题，取而代之的是 `Deref` 强制转换与 trait object 转换。最常见的坑出现在自引用结构与 unsafe 抽象里：把 `&'a mut T` 当成协变使用会让借用检查器拒绝合法代码或接受不安全代码，`std::cell::Cell`、`RefCell` 以及所有包含 `&mut` 的类型都是不变的，这就是为什么很多库要在文档里专门写一条「variance: invariant」。

📘 [Rust 参考 · 子类型与型变](https://doc.rust-lang.org/reference/subtyping.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 没有声明处型变标注，也没有 `out`/`in` 这样的关键字：泛型类型默认不变，浮动的兼容性靠**隐式转换**与协议 existential 提供。最该先知道的是 `Array<Dog>` 能赋给 `[Animal]` 是编译器专门为数组（以及 `Optional`、`Set`、`Dictionary` 的键值）开的口子，而不是通用的型变规则。

```swift
class Animal { func speak() -> String { "..." } }
class Dog: Animal { override func speak() -> String { "woof" } }

// 数组元素类型是协变的（编译器特例，Int → Any 这种装箱转换也成立）
func feed(_ xs: [Animal]) -> Int { xs.count }

// 函数类型：返回位置协变 —— (Animal) -> Dog 可当 (Animal) -> Animal 用
let makeDog: (Animal) -> Dog = { _ in Dog() }
let makeAnimal: (Animal) -> Animal = makeDog
// 函数类型：参数位置逆变 —— (Animal) -> Void 可当 (Dog) -> Void 用
let handleAny: (Animal) -> Void = { _ in }
let handleDog: (Dog) -> Void = handleAny

protocol Producer {
    associatedtype Output
    func produce() -> Output
}
struct DogProducer: Producer { func produce() -> Dog { Dog() } }

let dogs: [Dog] = [Dog(), Dog()]
print(feed(dogs))                       // 2  ✅ 数组协变
print(makeAnimal(Dog()).speak())        // woof
handleDog(Dog())
let p: any Producer = DogProducer()
print(type(of: p.produce()))            // Dog
```

自定义泛型类型不会自动获得这种转换：`struct Box<T> { var v: T }` 的 `Box<Dog>` 与 `Box<Animal>` 毫无关系，想表达协变只能自己定义协议并让容器实现它，或者提供 `map` 之类的转换方法。协议带 `associatedtype` 时它是自类型（Self-conforming），不能直接当独立类型使用，必须写成 `any Producer` 做存在类型装箱——装箱后关联类型 `Output` 被擦掉但具体类型元数据还在，所以 `type(of:)` 仍能报出 `Dog`。函数类型的返回位置协变、参数位置逆变是语言内置的子类型规则（`inout` 参数则是不变的，与 `@escaping` 也无关），它与 Array、Optional、Set、Dictionary 的元素协变一起，构成了 Swift 中仅有的几处自动型变；用错方向（把 `(Animal) -> Animal` 赋给 `(Dog) -> Dog`）编译器会直接拒绝，因为那需要参数协变。

📘 [Swift · 类型转换与存在类型](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/typecasting/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有型变：类型参数之间没有任何子类型关系，接口之间也只有「结构满足」而没有继承。最该先知道的是 `[]Dog` 不能当 `[]Animal` 用，哪怕 `Dog` 实现了 `Animal`，因为切片之间不存在转换。

```go
package main

import "fmt"

type Animal interface{ Speak() string }
type Dog struct{}

func (Dog) Speak() string { return "woof" }

func feed(xs []Animal) int { return len(xs) }

func main() {
	dogs := []Dog{{}, {}}
	// 🛑 编译错误：cannot use dogs (variable of type []Dog) as []Animal value
	// fmt.Println(feed(dogs))

	// ✅ 唯一的办法：逐个装箱成接口值
	xs := make([]Animal, len(dogs))
	for i, d := range dogs { xs[i] = d }
	fmt.Println(feed(xs)) // 2

	// 接口之间也没有子类型传递：值满足就行，不需要声明
	var a any = 1
	fmt.Println(a) // 1
}
```

Go 的接口采用了「隐式满足」：`Dog` 什么都不用声明就实现了 `Animal`，但这是**值的可赋值性**，不是类型之间的子类型关系，因此不会传导到 `[]Dog` 与 `[]Animal`。同理，泛型函数里的 `T` 与 `S` 之间也没有任何关系，`func f[T any](x T)` 不能接受「`T` 的某个子类型」这种说法。想把一组具体类型当成统一类型处理，得显式转换：要么像上面那样逐个装箱成接口切片，要么把容器本身写成泛型 `type List[T any] struct{...}` 再用 `List[Animal]`，但要注意 `List[Dog]` 与 `List[Animal]` 依然是两个无关的类型。这条规则看着严苛，好处是运行时没有任何协变检查开销，切片的内存布局永远是「元素类型连续排布」，不存在 Java 数组协变那种「写进去才发现类型不对」的问题。

📘 [Go spec · 可赋值性](https://go.dev/ref/spec#Assignability)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的型变完全属于类型检查器：`typing` 允许给 `TypeVar` 标注 `covariant=True` 或 `contravariant=True`，但解释器在运行时不做任何检查。最该先知道的是内置的 `list` 被声明为不变，因此 `list[Dog]` 在静态检查下不是 `list[Animal]`。

```python
from typing import TypeVar, Generic

T_co = TypeVar("T_co", covariant=True)            # 只出现在返回位置
T_contra = TypeVar("T_contra", contravariant=True)  # 只出现在参数位置
T = TypeVar("T")                                   # 不变

class Box(Generic[T]):
    def get(self) -> T: ...
class Producer(Generic[T_co]):
    def get(self) -> T_co: ...
class Consumer(Generic[T_contra]):
    def put(self, item: T_contra) -> None: ...

# 运行时不检查型变，也不检查类型实参
box: Box[int] = Box()
box2: Box[str] = box          # ⚠️ 静态检查器报错，运行时照样通过
print(type(box).__name__, box2 is box)   # Box True

def needs_ints(xs: list[int]) -> int: return len(xs)
print(needs_ints([1, 2]))      # 2
```

`list` 不变的原因是它既可读又可写：如果 `list[Dog]` 能当 `list[Animal]`，往里面 `append(Cat())` 就会破坏原来的元素类型。只读容器（`Sequence`、`Iterable`）在 typeshed 里被声明为协变，只写容器（`Consumer`）才可能逆变。PEP 695 的 `class Producer[T]:` 语法里不能再写型变标注（`class Producer[out T]:` 是语法错误），它创建的类型参数默认 `infer_variance=True`，由类型检查器按使用位置推断协变或逆变；要显式钉死型变，仍得回到 `TypeVar("T_co", covariant=True)` 加 `Generic[T_co]` 的老写法。最大的坑是误以为运行时会有检查：`box2: Box[str] = box` 这行代码在 CPython 里只是把同一个对象绑到另一个名字，`__orig_class__` 甚至可能还写着 `Box[int]`；要在运行时验证类型只能自己用 `isinstance` 检查元素，或者引入 `beartype`、`typeguard` 这类运行时类型检查库。

📘 [Python · typing 型变](https://docs.python.org/3/library/typing.html#variance-of-generic-types)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 把型变提到了声明处：`out T` 表示协变、`in T` 表示逆变，这比 Java 的通配符更省事。最该先知道的是 `MutableList<T>` 这类同时读写的类型必须不变，此时只能用使用处型变（类型投影）临时调整视角。

```kotlin
// 声明处协变：Producer<Dog> 就是 Producer<Animal> 的子类型
interface Producer<out T> { fun produce(): T }
// 声明处逆变：Consumer<Animal> 就是 Consumer<Dog> 的子类型
interface Consumer<in T> { fun consume(item: T) }

open class Animal
class Dog : Animal()

fun feedAll(animals: List<Animal>) = animals.size

fun main() {
    val dogs: List<Dog> = listOf(Dog())
    println(feedAll(dogs))                  // 1  ✅ List 是协变的

    // 使用处型变（类型投影）：把 MutableList 当只读视图传出去
    val src: MutableList<Dog> = mutableListOf(Dog())
    println(feedAll(src))                   // 1  ✅ MutableList<Dog> → List<Animal>

    // 星投影 List<*> 等价于 List<out Any?>：只能读，不能写
    val anys: List<Any?> = listOf(1, "a")
    println(anys.size)                      // 2

    // Nothing 是所有类型的子类型，可以安全地放进任何协变位置
    val empty: List<Nothing> = emptyList()
    println(feedAll(empty))                 // 0
}
```

`out`/`in` 一旦写在声明处就作用于所有使用点，编译器会检查类型参数是否只出现在允许的位置：`out T` 只能出现在返回值（与 `val` 属性）位置，`in T` 只能出现在参数位置，违反时报 `Type parameter T is declared as 'out' but occurs in 'in' position`。Kotlin 的 `List<out E>` 是标准库声明的协变只读接口，`MutableList<E>` 则是不变的，两者之间靠 `MutableList<Dog>` 到 `List<Dog>` 的隐式子类型关系衔接。星投影 `List<*>` 等价于 `List<out Any?>`：元素可以读成 `Any?`，但 `add` 这类写入方法全部不可用；如果写成 `MutableList<*>` 还要小心「能读不能写」的规则。`Nothing` 是所有类型的子类型，`List<Nothing>` 因此可以赋给任何 `List<T>`，这正是 `emptyList()` 的实现基础。

📘 [Kotlin · 型变](https://kotlinlang.org/docs/generics.html#variance)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的型变分两半：数组天生协变（历史遗留的缺陷），泛型则一律不变，用通配符在使用点调整。最该先知道的是 `? extends T` 只能读、`? super T` 只能写，也就是常说的 PECS（Producer Extends, Consumer Super）。

```java
import java.util.ArrayList;
import java.util.List;

void main() {
    // 数组协变：编译通过，运行时报错
    Object[] objects = new String[1];
    try {
        objects[0] = 42;                 // 🛑 ArrayStoreException
    } catch (ArrayStoreException e) {
        System.out.println("ArrayStoreException");   // ArrayStoreException
    }

    // 泛型不变：List<String> 不是 List<Object>
    List<String> strs = new ArrayList<>();
    // List<Object> objs = strs;         // 🛑 编译错误

    // ? extends：读取端（Producer）
    List<? extends Number> src = List.of(1, 2, 3);
    double sum = 0;
    for (Number n : src) sum += n.doubleValue();
    System.out.println(sum);             // 6.0
    // src.add(1);                       // 🛑 编译器不知道具体元素类型

    // ? super：写入端（Consumer）
    List<? super Integer> dst = new ArrayList<Number>();
    dst.add(1);
    System.out.println(dst.size());      // 1
    // Integer x = dst.get(0);           // 🛑 取出来只有 Object
}
```

数组协变是 Java 1.0 就有的设计，为了能写 `Object[] args` 接收任意数组；代价是每次数组写入都要插入运行时类型检查，这就是 `ArrayStoreException` 的来源。泛型在 2004 年加入时选择了不变加通配符的方案，理由是保留擦除后仍能保证类型安全。PECS 的直觉是：如果只需要从容器里读，用 `? extends T`；如果需要往容器里写，用 `? super T`。最常见的坑是 `List<? extends Number>` 里 `add` 不可用却想硬写，正确做法是加一个接收 `? super T` 的参数；另一个坑是 `List<?>` 既不能读成具体类型也不能写（除 `null`），它等价于 `List<? extends Object>`。`Arrays.asList` 返回的定长列表与 `List.of` 返回的不可变列表会让 `add` 抛 `UnsupportedOperationException`，那是实现限制而不是型变问题。

📘 [Java 教程 · 通配符](https://docs.oracle.com/javase/tutorial/java/generics/wildcards.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的类层次自带协变（`Derived*` 可以当 `Base*`），但模板实例之间没有任何型变：`std::vector<Derived>` 不是 `std::vector<Base>`。最该先知道的是函数指针类型也是不变的，想做签名转换得靠 `std::function` 这类类模板的可调用性检查。

```cpp
#include <cstdio>
#include <functional>
#include <vector>

struct Base { virtual ~Base() = default; virtual const char* name() const { return "Base"; } };
struct Derived : Base { const char* name() const override { return "Derived"; } };

static void takesBase(const Base& b) { std::printf("called with %s\n", b.name()); }

int main() {
    // 1. 类层次自带协变：只有指针/引用是子类型载体
    Derived d;
    Base* p = &d;
    std::printf("%s\n", p->name());            // Derived

    // 2. 模板实例之间没有型变
    std::vector<Derived> vd(2);
    // std::vector<Base> vb = vd;   // 🛑 no viable conversion from 'vector<Derived>'
    std::vector<Base*> vp;                     // 要异构就存指针或引用
    for (auto& x : vd) vp.push_back(&x);
    std::printf("%zu\n", vp.size());           // 2

    // 3. 函数指针类型不变
    // void (*bad)(const Derived&) = takesBase;   // 🛑 type mismatch at 1st parameter

    // 4. std::function 靠可调用性检查完成转换（此处参数逆变成立）
    std::function<void(const Base&)> fb = takesBase;
    std::function<void(const Derived&)> fd = fb;
    fd(d);                                     // called with Derived
    return 0;
}
```

模板不变性的物理原因是布局：`std::vector<Derived>` 与 `std::vector<Base>` 的元素大小与步长可能不同，能互相转换就会让 `operator[]` 算错地址；即使 `Derived` 与 `Base` 大小相同，切片（slicing）也会在赋值时丢掉派生部分。标准库容器因此只提供显式的转换途径，例如 `std::vector<Derived*>` 到 `std::vector<Base*>` 也要逐个元素复制，或者用 `std::span<Base*>`、`std::ranges` 的视图来避免拷贝。至于函数类型：C++ 的函数指针与成员函数指针**没有**子类型转换，`void(*)(const Base&)` 无法赋给 `void(*)(const Derived&)`；`std::function` 之所以可以，是因为它是类模板，其转换构造函数用 `is_invocable_r` 检查「用 `const Derived&` 调用 `takesBase` 是否合法」，本质是一次用户定义转换而不是语言级型变。

📘 [cppreference · 派生类到基类的转换](https://en.cppreference.com/w/cpp/language/derived_class)

{{% /tab %}}

{{% tab header="C" %}}

C 既没有泛型也没有子类型层次，因此不存在协变与逆变的概念；唯一近似的东西是 `void *` 可以接收任何对象指针，这是放弃类型检查而不是型变。最该先知道的是把 `int *` 转成 `void *` 再转回来是合法的隐式往返，但把 `int **` 转成 `void **` 不合法，指针的层级不会自动传导。

```c
#include <stdio.h>

struct Base { int kind; };
struct Derived { struct Base base; int extra; };   /* 手动模拟"继承" */

int main(void) {
    int a = 7;
    void *p = &a;                /* 任何对象指针 → void*：隐式、无检查 */
    printf("%d\n", *(int *)p);   /* 7 */

    /* 指针的指针不协变：int** 不能当 void** */
    int *pa = &a;
    /* void **pp = &pa; */       /* ⚠️ 违反严格别名规则，编译器会警告 */
    void *pp = &pa;              /* 只能升一层，再往下转要显式 */
    printf("%d\n", **(int **)pp);/* 7 */

    /* 结构体嵌套是唯一的"子类型"手段 */
    struct Derived d = { { 1 }, 2 };
    struct Base *b = &d.base;    /* 首成员地址相同，是刻意的约定 */
    printf("%d %d\n", b->kind, d.extra);  /* 1 2 */
    return 0;
}
```

C 的类型系统里没有「派生」关系，结构体嵌套加上「首成员地址与结构体地址相同」的保证是唯一能模拟出对象布局的办法，这也是 Linux 内核里常见的 container_of 模式的基础。`void *` 的转换规则是不对称的：任何对象指针都能隐式转成 `void *` 并原样转回；函数指针转 `void *` 则不属于标准保证的转换（POSIX 才要求支持），只是编译器普遍接受；而 `T **` 到 `void **` 之间有严格别名（strict aliasing）问题，标准并不保证安全，`-Wpedantic` 下会给出警告。数组在这里也没有型变：`int (*)[3]` 与 `int (*)[4]` 是不同类型，传给期望 `int *` 的平台数组参数时会发生退化，长度信息彻底丢失，这正是 C 里到处要传 `size_t len` 的原因。

📘 [cppreference · 指针转换](https://en.cppreference.com/w/c/language/pointer)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的参数化类型是**不变**的：`Vector{Int}` 不是 `Vector{Real}` 的子类型，这一点和 Java 泛型一致，但原因更物理——它关系到内存布局。最该先知道的是抽象类型（`Real`、`Integer`、`Number`）之间有子类型关系，而参数化类型只在自己内部判等。

```julia
abstract type Animal end
struct Dog <: Animal end
struct Cat <: Animal end

struct Box{T}; value::T; end             # 先定义，后面才能引用

# 参数化类型不变
println(Vector{Int} <: Vector{Real})     # false
println(Vector{Int} <: Vector{Int})      # true
println(Vector{Int} <: AbstractVector)   # true（抽象类型才有子类型关系）
println(Box{Int} <: Box)                 # true（Box 是 UnionAll，可看作上界）
println(Box{Int} <: Box{Real})           # false（参数化类型之间不协变）

# 想接受任意元素类型：用 where 或 <: 语法
summarize(v::AbstractVector{T}) where {T<:Real} = "reals($(length(v)))"
summarize(v::AbstractVector) = "any($(length(v)))"    # 兜底方法

println(summarize([1, 2, 3]))            # reals(3)
println(summarize(Any[1, "a"]))          # any(2)

# Union 类型可以出现在字段与分派里
const NumOrStr = Union{Int, String}
f(x::NumOrStr) = "union"
println(f(1), f("a"))                    # unionunion
println(Dog <: Animal, Cat <: Animal)    # truetrue
```

不变性的理由是：`Vector{Int}` 的元素按 8 字节紧排，`Vector{Real}` 里装的是指向装箱值的指针；如果前者是后者的子类型，一个接收 `Vector{Real}` 的函数就可能往里写 `1.5`，破坏 `Vector{Int}` 的内存约定。所以 Julia 要求你显式写出「元素类型是 `Real` 的某个子类型」，写成 `AbstractVector{T} where {T<:Real}`，或者用简洁语法 `AbstractVector{<:Real}`。抽象类型（`Any` 之下是 `Number`、`AbstractString` 等）是另一套机制，它们之间有真正的子类型图，`Int <: Real` 为真。想让一个容器装多种具体类型，要么用抽象元素类型 `Vector{Animal}`（元素装箱），要么用 `Union{Dog,Cat}` 的小联合（Julia 对小 `Union` 有专门的存储优化），要么用异构的 `Vector{Any}`。

📘 [Julia · 参数类型不变性](https://docs.julialang.org/en/v1/manual/types/#Parametric-Types)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的型变是「有限支持」：只有泛型**接口**与**委托**能声明 `out`/`in`，泛型类与泛型结构体一律不变。最该先知道的是数组也和 Java 一样协变，因此同样带着运行时检查的开销。

```csharp
using System;
using System.Collections.Generic;

// 接口声明处型变
interface IProducer<out T> { T Produce(); }        // 协变
interface IConsumer<in T> { void Consume(T item); } // 逆变

class DogProducer : IProducer<Dog> { public Dog Produce() => new Dog(); }
class AnimalConsumer : IConsumer<Animal> { public void Consume(Animal a) { } }

class Animal { public virtual string Speak() => "..."; }
class Dog : Animal { public override string Speak() => "woof"; }

class Program
{
    static int Feed(IEnumerable<Animal> xs) => System.Linq.Enumerable.Count(xs);

    static void Main()
    {
        // IEnumerable<out T> 协变：IEnumerable<Dog> → IEnumerable<Animal>
        IEnumerable<Dog> dogs = new List<Dog> { new Dog() };
        Console.WriteLine(Feed(dogs));                    // 1

        // Action<in T> 逆变
        Action<Animal> handleAny = a => { };
        Action<Dog> handleDog = handleAny;
        handleDog(new Dog());
        Console.WriteLine("ok");                          // ok

        // 数组协变：编译通过，写入时运行时检查
        object[] arr = new string[1];
        try { arr[0] = 42; }                              // 🛑 ArrayTypeMismatchException
        catch (ArrayTypeMismatchException) { Console.WriteLine("mismatch"); } // mismatch

        // 泛型类不变：List<Dog> 不是 List<Animal>
        // List<Animal> bad = new List<Dog>();            // 🛑 编译错误
        Console.WriteLine(new DogProducer() is IProducer<Animal>);  // True
    }
}
```

`IEnumerable<out T>`、`IReadOnlyList<out T>`、`Func<out TResult>` 是标准库里的协变类型，`Action<in T>`、`IComparer<in T>`、`IEqualityComparer<in T>` 是逆变类型，这张表决定了 LINQ 与集合接口能不能混用。协变的类型参数只能出现在输出位置（返回值、`get` 访问器），逆变只能出现在输入位置，编译器会检查；`out`/`in` 只是标注，实际转换由 CLR 的变体（variance）支持，运行时有专门的检查。数组协变与 Java 一样是历史包袱：`object[] arr = new string[1]` 合法，但 `arr[0] = 42` 会抛 `ArrayTypeMismatchException`，因为 CLR 在写入时做类型检查。最常见的坑是给自定义接口加了 `out T` 之后想再放一个 `void Add(T)` 方法，编译器会直接报「无效变体：类型参数 T 必须始终不变」；另一个坑是误以为 `List<T>` 能协变，实际上必须换成 `IEnumerable<T>` 或 `IReadOnlyList<T>` 才可以。

📘 [MS Learn · 泛型中的协变和逆变](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/concepts/covariance-contravariance/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型是**声明处协变**的：`List<Dog>` 天然就是 `List<Animal>` 的子类型，不需要任何标注。最该先知道的是这种协变是不健全的，所以 Dart 在涉及泛型类型参数的写入点插入运行时检查，并提供了 `covariant` 关键字来显式声明意图。

```dart
class Animal { String speak() => "..."; }
class Dog extends Animal { @override String speak() => "woof"; }
class Cat extends Animal { @override String speak() => "meow"; }

// Dart 泛型协变：List<Dog> 是 List<Animal> 的子类型
int feed(List<Animal> xs) => xs.length;

// covariant 关键字：显式声明参数中的类型参数可被"收紧"（把检查交给自己）
class Cage<T> {
  T? occupant;
  void put(covariant T animal) { occupant = animal; }
}

void main() {
  final dogs = <Dog>[Dog()];
  print(feed(dogs));                       // 1  ✅ 协变

  final cage = Cage<Animal>();
  cage.put(Dog());
  print(cage.occupant.runtimeType);        // Dog

  // 不健全之处：协变赋值合法，越界写入只能靠运行时检查兜底
  final List<Animal> animals = dogs;       // ✅ 协变：List<Dog> 是 List<Animal>
  try {
    animals.add(Cat());                    // 🛑 底层仍是 List<Dog>，不能放 Cat
  } on TypeError catch (e) {
    print(e.runtimeType);                  // TypeError
  }
  print(dogs.length);                      // 1
}
```

Dart 选择协变是为了让 `List<Dog>` 能直接传给接收 `List<Animal>` 的代码，代价是「写」不再静态安全：编译器允许把 `Cat` 加进一个实际是 `List<Dog>` 的 `List<Animal>` 视图，然后在运行时抛 `TypeError`。这就是所谓的 unsound 补丁——Dart 2 的空安全做到了健全，泛型则依赖运行时检查。`covariant` 关键字用在参数上，告诉分析器「这个参数位置允许把 `T` 收紧成子类型」，常用于 `operator ==`、`compareTo` 这类需要接受同类但声明为父类型的场景；配合 `extension type` 与 `F-bounds`，可以表达大部分常见的类型约束。因为类型实参是 reified 的，`T` 能在运行时用于 `is` 判断，这是 Dart 与 Java 擦除的最大差别。

📘 [Dart · 类型系统](https://dart.dev/language/type-system)

{{% /tab %}}

{{% tab header="R" %}}

R 没有泛型，所以也没有型变：`list` 与 `vector` 不携带元素类型，元素类型只在每个元素自己身上。最该先知道的是 R 里唯一的「类型关系」是 `class` 属性向量与 `inherits()` 判断，继承靠字符串约定而不是结构声明。

```r
# 没有类型参数：向量的类型由内容决定（强制层级），不是声明出来的
ints <- c(1L, 2L)
reals <- c(1, 2)
print(typeof(ints))                 # [1] "integer"
print(typeof(reals))                # [1] "double"

# 类型"关系"只看 class 属性
x <- structure(list(), class = c("dog", "animal"))
print(inherits(x, "animal"))        # [1] TRUE
print(inherits(x, "dog"))           # [1] TRUE
print(inherits(x, "cat"))           # [1] FALSE

# 向量化：一个函数对元素类型的要求在运行时按强制层级处理
mixed <- c(1L, 2.5)
print(typeof(mixed))                # [1] "double"（integer 被提升）

# 列表是不带元素类型的异构容器
box <- list(1, "a", TRUE)
print(vapply(box, typeof, ""))      # [1] "double" "character" "logical"
```

R 的「容器元素类型」是运行时推断出来的：`c()` 会把元素统一到强制层级（logical < integer < double < complex < character）中最高的一档，这种转换是隐式且不可逆的，`c(1L, 2.5)` 之后再也分不出哪个原本是 `integer`。`list()` 则是真正的异构容器，元素各自保留类型，代价是取值要 `[[` 而不是 `[`。面向对象方面，S3 的 `class` 属性是一个字符串向量，`inherits()` 按向量顺序判断，`NextMethod()` 沿这个向量继续分派；S4 用 `setClass()` 声明的类有真实的结构与继承关系，`is()`、`extends()` 可以查询，但它仍然不是「容器元素类型」意义上的泛型。实践中最容易踩的坑是把 `sapply` 的返回类型当稳定契约：输入类型不同，`sapply` 可能返回向量、矩阵或列表，这正是 `vapply` 要求显式给出 `FUN.VALUE` 模板的原因。

📘 [R 语言定义 · 对象与类](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Objects)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有型变概念：类型之间只有「相同」与「可强制转换」，不存在子类型关系，也就没有协变逆变可言。最该先知道的是 `*Derived` 能传给 `*Base` 是靠结构体的 `@fieldParentPtr` 与显式转换，而不是语言内建的继承。

```zig
const std = @import("std");

// 没有继承 → 没有子类型图 → 没有型变
const Animal = struct { kind: []const u8 };
const Dog = struct {
    animal: Animal,          // 组合而非继承
    name: []const u8,

    // 显式向上转换：从字段地址反推父结构地址
    pub fn asAnimal(self: *Dog) *Animal {
        return &self.animal;
    }
};

// 泛型参数之间也无关系：List(Dog) 与 List(Animal) 是两个类型
fn List(comptime T: type) type {
    return struct {
        items: []T,
        pub fn len(self: @This()) usize { return self.items.len; }
    };
}

pub fn main() void {
    var listDog = List(Dog){ .items = &.{} };
    const listAnimal = List(Animal){ .items = &.{} };
    std.debug.print("{} {}\n", .{ listDog.len(), listAnimal.len() });  // 0 0
    std.debug.print("{}\n", .{@TypeOf(listDog) == @TypeOf(listAnimal)}); // false

    var d = Dog{ .animal = .{ .kind = "dog" }, .name = "rex" };
    const a: *Animal = d.asAnimal();
    std.debug.print("{s}\n", .{a.kind});   // dog

    // 切片的强制转换只允许"加 const"，元素类型不会变
    const mut: []Dog = listDog.items;
    const ro: []const Dog = mut;           // ✅ 允许
    // const bad: []const Animal = mut;    // 🛑 元素类型不同，编译错误
    _ = ro;
}
```

Zig 的哲学是「没有隐藏控制流、没有隐藏类型转换」：既然没有继承，也就没有协变逆变这套规则，需要异构容器时用 tagged union 或 `std.mem.Allocator` 这类带函数指针的结构体自己实现动态分派。切片（`[]T`）之间唯一的自动转换是加 `const`（`[]T` → `[]const T`），元素类型相同才允许，这与 Rust 的 `&mut T` → `&T` 类似，都不涉及子类型。`@TypeOf(a) == @TypeOf(b)` 是编译期比较，能直接证明 `List(Dog)` 与 `List(Animal)` 是两个不同类型；要在运行时区分，只能像上面那样把类型名存进结构体字段。

📘 [Zig · 类型强制转换](https://ziglang.org/documentation/master/#Casting)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有泛型，因此没有型变；但 Lua 有一套更彻底的机制——元表，可以让「看起来是父类型」的对象在运行时表现成任何想要的样子。最该先知道的是 Lua 里没有类型之间的子类型关系，只有值的 `type()` 与元表里的 `__index` 链。

```lua
-- 没有子类型关系，只有元表链
local Animal = {}
Animal.__index = Animal
function Animal.new(name) return setmetatable({name = name}, Animal) end
function Animal:speak() return self.name .. " makes a sound" end

local Dog = setmetatable({}, { __index = Animal })   -- 用元表模拟"继承"
Dog.__index = Dog
function Dog.new(name) return setmetatable({name = name}, Dog) end
function Dog:speak() return self.name .. " woofs" end

local d = Dog.new("rex")
print(d:speak())                       -- rex woofs
print(getmetatable(d) == Dog)          -- true
print(rawget(d, "speak") == nil)       -- true（方法来自元表）
print(type(d))                         -- table（type 只看基础类型）

-- 容器元素类型完全不受约束
local anys = {1, "a", Animal.new("x"), function() end}
print(#anys)                           -- 4
for _, v in ipairs(anys) do io.write(type(v), " ") end
print()                                -- number string table function
```

Lua 的 `type()` 只返回八种基础类型（`nil`、`boolean`、`number`、`string`、`table`、`function`、`userdata`、`thread`），不区分「狗」和「动物」，因此没有型变可言；`__index` 链提供的是方法查找的回退路径，与类型系统无关。想要「元素类型一致」的保证，只能在构造时手写检查（比较元素类型或元表），或者用 `userdata` 加 C 侧的类型标记。`__index` 链的查找成本随链长线性增长，深层继承会把热路径拖慢；此外 `__add`、`__lt`、`__eq` 这类二元运算符的元方法**不必**放在两个操作数共同的元表里：Lua 先查第一个操作数的元表，找不到再查第二个，所以单侧定义也能触发（`__eq` 的额外前提是两个操作数同为 table 或同为 full userdata 且不是原始相等），这一点常被误当成「必须两侧都挂」。

📘 [Lua 5.5 · 元表](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 没有声明处型变关键字，但因为类型是结构化比较的，赋值兼容性看起来像协变，实际由编译器按成员位置推导型变。最该先知道的是 `strictFunctionTypes` 打开后函数类型参数的检查是逆变的，而方法参数的检查仍然是双变的。

```typescript
// 结构化类型：只要有 name 就算 Animal，不需要声明 implements
interface Animal { name: string }
interface Dog extends Animal { breed: string }

// 数组/只读容器：协变（可安全地只读）
function countAll(xs: readonly Animal[]): number { return xs.length }
const dogs: Dog[] = [{ name: "rex", breed: "lab" }];
console.log(countAll(dogs));                       // 1

// 可变数组的协变是不健全的，靠运行时自己小心
const animals: Animal[] = dogs;                    // ✅ 编译通过
// animals.push({ name: "x" }) 之后 dogs 里就混进了没有 breed 的元素

// 函数类型：strictFunctionTypes 下参数逆变、返回协变
type HandlesAnimal = (a: Animal) => Dog;
// const bad: HandlesAnimal = (a: Dog) => a;        // 🛑 参数收窄成 Dog，逆变不成立
type HandlesDog = (d: Dog) => Animal;
const handlesDog: HandlesDog = (a: Animal) => a;    // ✅ 参数放宽成 Animal，逆变成立

// 需要显式协变时用 out 标注（TS 4.7+），只影响检查不影响运行时
interface Producer<out T> { produce(): T }
interface Consumer<in T> { consume(item: T): void }
```

数组被设计为协变是出于可用性，代价和 Java 一样：`Animal[]` 与 `Dog[]` 指向同一块底层数组，往里推 `Animal` 就会让 `Dog[]` 名不副实，TypeScript 不插入任何运行时检查。`strictFunctionTypes` 只管「函数类型的位置」，对方法签名（`interface X { m(a: Animal): void }`）仍然按双变处理，这是为了兼容既有代码的刻意妥协。TS 4.7 的 `in`/`out` 标注是给编译器的提示：协变标注的类型参数只能出现在输出位置，逆变只能出现在输入位置，写错方向会立刻报错；标注还能让编译器跳过昂贵的结构比较，加快大型项目的类型检查。另一个常被忽略的点是 `readonly T[]` 才是真正安全的协变位置，能用只读就用只读。

📘 [TS 手册 · 类型兼容性](https://www.typescriptlang.org/docs/handbook/type-compatibility.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有泛型也没有静态类型，型变这个概念在运行时层面不存在；只在内存语义上「对象可以当作其原型链上任意类型的实例」这一点，看起来像协变。最该先知道的是 `Array` 完全不检查元素类型，所以既没有协变也不需要 `? extends`。

```javascript
// 没有元素类型，数组天然"容纳一切"
const dogs = [{ name: "rex", breed: "lab" }];
const animals = dogs;                  // 同一个引用，没有任何转换
animals.push({ name: "x" });           // 静默混入不完整的元素
console.log(dogs.length);              // 2
console.log(dogs[1].breed);            // undefined ⚠️

// 原型链是 JS 里唯一的"子类型"机制
class Animal { speak() { return "..."; } }
class Dog extends Animal { speak() { return "woof"; } }
const d = new Dog();
console.log(d instanceof Animal);      // true  ← 看起来像协变
console.log(d instanceof Dog);         // true

// 函数"逆变"靠运行时参数决定，语言不做检查
function feed(animal) { return animal.speak(); }
console.log(feed(d));                  // woof
try { feed({}); } catch (e) { console.log(e.constructor.name); }  // TypeError
```

JS 里唯一的类型关系是原型链（`instanceof`、`isPrototypeOf`），它是运行时的、可变的（`Object.setPrototypeOf` 能随时改），所以「协变」只是观察到的效果而不是规则。把数组赋给另一个变量完全共享底层存储，`animals.push()` 修改的就是 `dogs`，不会报错也不会拷贝；这正是 TypeScript 需要在类型层面提醒用户的原因。要得到真正的父子容器隔离，必须显式拷贝并校验每个元素（`structuredClone`、`map` 加类型守卫），运行时的 `instanceof` 只检查原型链，不检查结构的完整性——`feed({})` 直到调用 `animal.speak()` 才抛 `TypeError`。

📘 [MDN · 继承与原型链](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有泛型，也就没有型变；它有的是类继承带来的协变/逆变，作用在**方法签名**而不是类型参数上。最该先知道的是 PHP 7.4 起支持参数类型逆变、返回类型协变，这是语言层面唯一与型变相关的规则。

```php
<?php
declare(strict_types=1);

class Animal { public function speak(): string { return "..."; } }
class Dog extends Animal { public function speak(): string { return "woof"; } }

class Shelter {
    // 返回类型协变：子类可以返回更具体的类型
    public function adopt(): Animal { return new Animal(); }
    // 参数类型逆变：子类可以接受更宽的类型
    public function accept(Animal $a): void { echo $a->speak(), PHP_EOL; }
}

class DogShelter extends Shelter {
    public function adopt(): Dog { return new Dog(); }      // ✅ 返回协变
    public function accept(object $a): void { }             // ✅ 参数逆变（放宽）
}

$s = new DogShelter();
echo get_class($s->adopt()), PHP_EOL;        // Dog
$s->accept(new Dog());                       // 无输出

// union 类型也是"更宽"的一种表达（PHP 8.0+）
function feed(int|string $x): string { return (string) $x; }
echo feed(42), PHP_EOL;                      // 42

// 容器没有元素类型：数组装什么都行
$mixed = [1, "a", new Dog()];
echo count($mixed), PHP_EOL;                 // 3
```

PHP 的协变/逆变只作用于方法签名的继承检查：返回类型可以从 `Animal` 收窄成 `Dog`（协变），参数类型可以从 `Dog` 放宽成 `Animal` 或 `object`（逆变），违反时在编译/加载阶段就报致命错误。这与泛型型变无关，因为 PHP 根本没有类型参数——`array` 不携带元素类型，`iterable` 也不带，想表达「`list<T>`」只能写 docblock。PHP 8.0 引入的 union 类型与 8.1 引入的 `never`、交集类型（纯类型层面）把签名表达能力补齐了一部分，但仍然无法表达「对任意 `T` 成立」的约束。实践上常见的替代是运行时检查：在构造器里遍历元素并用 `instanceof` 或 `is_int` 断言，把类型不匹配变成 `InvalidArgumentException`，代价是每次构造都要扫一遍数组。

📘 [PHP · 协变与逆变](https://www.php.net/manual/en/language.oop5.variance.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有泛型，所以既没有声明处型变也没有使用处型变；但类继承带来的方法签名宽松规则、以及 `Module#include?` 形成的祖先链，在效果上与协变有些相似。最该先知道的是 Ruby 的类型关系完全在运行时，任何「容器元素类型」都不会被检查。

```ruby
class Animal
  def speak = "..."
end
class Dog < Animal
  def speak = "woof"
end

# 祖先链：唯一的"子类型"关系，运行时用 is_a? / === 查询
d = Dog.new
puts d.is_a?(Animal)          # true
puts Dog.ancestors.inspect    # [Dog, Animal, Object, Kernel, BasicObject]
puts Animal === d             # true（case/when 用的就是这个）

# 数组不带元素类型：协变、逆变都无从谈起
dogs = [Dog.new]
animals = dogs                # 同一个对象
animals << "not an animal"    # 静默通过
puts dogs.length              # 2
puts dogs.last.class          # String

# "约束"只能是运行时检查：检查失败就抛异常
def feed_all(list)
  list.each { |x| raise TypeError, "not animal" unless x.is_a?(Animal) }
  list.size
end
begin
  feed_all(dogs)              # dogs 里已经混进了 "not an animal"
rescue TypeError => e
  puts "#{e.class}: #{e.message}"   # TypeError: not animal
end
puts feed_all([Dog.new])      # 1（纯 Dog 的数组可以通过）
```

Ruby 的 `is_a?`、`kind_of?`、`instanceof?` 与 `Class#===` 都沿祖先链向上查，这是唯一的「向上转换」语义，不需要声明也不会有编译期错误。容器完全不参与：往 `Array` 里放什么都可以，`animals = dogs` 只是复制引用，之后的修改同时可见。想在 Ruby 里得到类型安全的泛型容器，只能靠外部静态检查——Sorbet 的 `T::Array[Animal]` 与 RBS 的 `Array[Animal]` 能表达参数化类型，`srb tc` 或 Steep 会在检查期报错，但运行时仍然不强制。另一个容易踩的点是 `Module#===` 与正则、Range 的 `===` 行为不同，在 `case` 语句里 `when Animal` 走的是 `Animal === x`，而 `when "a".."z"` 走的是 `Range#===`，混用时容易写出意料之外的分支。

📘 [Ruby · Module#=== 与祖先链](https://docs.ruby-lang.org/en/master/Module.html#method-i-3D-3D-3D)

{{% /tab %}}

{{< /tabpane >}}

### 实现模型

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 用单态化（monomorphization）：编译器为每个具体类型实参各生成一份机器码，泛型调用被静态解析成直接调用。最该先知道的是这条路带来零成本抽象，代价是编译时间与二进制体积随实例数量线性增长。

```rust
trait Speak { fn speak(&self) -> String; }

struct Dog;
struct Cat;
impl Speak for Dog { fn speak(&self) -> String { "woof".into() } }
impl Speak for Cat { fn speak(&self) -> String { "meow".into() } }

// 每个 T 各生成一份代码
fn speak_twice<T: Speak>(t: &T) -> String { format!("{} {}", t.speak(), t.speak()) }

// 泛型结构体的布局随 T 变化
struct Pair<T> { a: T, b: T }

fn main() {
    println!("{}", speak_twice(&Dog));   // woof woof
    println!("{}", speak_twice(&Cat));   // meow meow

    println!("{}", std::any::type_name::<Pair<u8>>());    // generic::Pair<u8>（含 crate 名）
    println!("{}", std::any::type_name::<Pair<u64>>());   // generic::Pair<u64>
    println!("u8:  {}", std::mem::size_of::<Pair<u8>>());  // u8:  2
    println!("u64: {}", std::mem::size_of::<Pair<u64>>()); // u64: 16

    // dyn Trait：只生成一份代码 + vtable 间接调用，换来异构容器
    let boxed: Vec<Box<dyn Speak>> = vec![Box::new(Dog), Box::new(Cat)];
    let all: Vec<String> = boxed.iter().map(|s| s.speak()).collect();
    println!("{all:?}");                                  // ["woof", "meow"]
    println!("{}", std::mem::size_of::<Box<dyn Speak>>()); // 16
}
```

`Pair<u8>` 占 2 字节、`Pair<u64>` 占 16 字节，这直接说明泛型参数进入了内存布局，编译器必须在编译期为每个组合生成独立代码。`Box<dyn Speak>` 则相反：它是胖指针（数据指针 + vtable 指针，在 64 位平台上 16 字节），所有 `dyn Speak` 共享同一份调用代码，代价是每次调用都要查 vtable，而且编译器无法内联。判断标准很简单：类型组合在编译期确定、且分布在热路径上，用泛型；需要在同一个 `Vec` 里装多种具体类型、或者想减少代码体积，用 `dyn`。单态化的两个实际代价是编译时间（一个函数被 20 个类型用到就编译 20 次）和指令缓存压力（每份实例都是独立代码），缓解手段是把泛型函数的非泛型部分抽到独立的非泛型函数里，只让薄薄的外壳保持泛型。

📘 [rustc 开发指南 · Monomorphization](https://rustc-dev-guide.rust-lang.org/backend/monomorph.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的默认实现模型是**泛型元数据 + witness table**：一份代码处理所有类型，运行时通过 witness table 找到具体类型的实现；同时编译器会对热点调用做特化（specialization）。最该先知道的是 `some` 与 `any` 恰好对应这两条路线。

```swift
import Foundation

protocol Speak { func speak() -> String }
struct Dog: Speak { func speak() -> String { "woof" } }
struct Cat: Speak { func speak() -> String { "meow" } }

// 泛型函数：默认一份代码 + witness table；编译器可为具体类型特化出专用版本
func speakTwice<T: Speak>(_ t: T) -> String { "\(t.speak()) \(t.speak())" }

// some = 不透明类型：调用方看不到具体类型，编译器可内联与特化
func makeDog() -> some Speak { Dog() }

// any = existential：装箱，运行时走 witness table 的间接调用
func speakAll(_ xs: [any Speak]) -> [String] { xs.map { $0.speak() } }

print(speakTwice(Dog()))                       // woof woof
print(makeDog().speak())                       // woof
print(speakAll([Dog(), Cat()]))                // ["woof", "meow"]

// 运行时可查询类型元数据：reified 的类型实参还在
let things: [Any] = [1, "a"]
print(things.map { String(describing: type(of: $0)) })   // ["Int", "String"]
```

Swift 的泛型默认不复制代码，而是把类型元数据与协议 witness table 作为隐藏参数传进去，因此 `speakTwice<T>` 的实现只有一份；编译器在能看到具体类型时会做特化（生成专用版本并内联），在优化级别较高的构建里这一步收益明显。`some Speak` 是反向的：具体类型由被调用方决定，调用方只知道它满足 `Speak`，所以编译器可以在跨模块时仍然把类型信息保存在元数据里，实现零开销抽象。`any Speak` 则是显式装箱：值被放进 existential 容器，方法调用通过 witness table 间接跳转，这就是常说的「`any` 比 `some` 慢」的原因。`Mirror` 与 `type(of:)` 都能在运行时拿到具体类型，说明 Swift 的类型元数据在 ABI 层面是保留的，与 Java 的擦除完全不同。

📘 [Swift · 不透明与存在类型](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/opaquetypes/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 1.18 起的实现策略是 **GC shape stenciling + 字典（dictionaries）**：既不是完整单态化，也不是完全擦除。最该先知道的是「GC shape」把类型分组——所有指针类型共享一份代码，而每个不同的非指针类型各生成一份。

```go
package main

import "fmt"

type Point struct{ X, Y int }
type Node struct{ N int }

//go:noinline
func Identity[T any](v T) T { return v }

func main() {
	fmt.Println(Identity(1))        // 1
	fmt.Println(Identity(int64(2))) // 2
	fmt.Println(Identity("s"))      // s
	fmt.Println(Identity(&Point{})) // &{0 0}
	fmt.Println(Identity(&Node{}))  // &{0}
}
```

用 `go build -gcflags='-l'`（关闭内联）编译后再 `go tool nm` 看符号，会看到每个非指针类型各有一个实例，而两个指针类型共用同一个实例：

| `go tool nm` 符号 | 含义 |
| --- | --- |
| `main.Identity[go.shape.*uint8]` | 唯一的指针形状实例，`*Point` 与 `*Node` 共用 |
| `main.Identity[go.shape.int]` | `int` 的专属实例 |
| `main.Identity[go.shape.int64]` | `int64` 的专属实例 |
| `main.Identity[go.shape.string]` | `string` 的专属实例 |
| `main..dict.Identity[int]` | `int` 的字典：类型元数据、`itab`、函数指针 |
| `main..dict.Identity[int64]` | `int64` 的字典 |
| `main..dict.Identity[string]` | `string` 的字典 |
| `main..dict.Identity[*main.Point]` | `*Point` 的字典（与 `*Node` 共用上面的形状代码） |
| `main..dict.Identity[*main.Node]` | `*Node` 的字典 |

`go.shape.*uint8` 这一份代码要同时服务 `*Point` 与 `*Node`，编译器无法在编译期把 `T` 换成具体类型，于是为每个具体类型各生成一个**字典**（符号里的 `main..dict.Identity[...]`），字典里装着类型元数据、`itab` 与需要的函数指针，运行时作为隐藏参数传入。这样做的收益是二进制体积不会随指针类型数量爆炸，代价是带字典的调用多一层间接寻址，而且指针形状里的字典访问无法被完全消除；非指针类型仍按类型各自 stencil，所以 `int`、`int64`、`string` 各有独立代码。想检查自己项目里的实例数量，用 `go tool nm` 过滤 `go.shape` 与 `..dict.` 是最直接的办法。

📘 [Go 设计文档 · GC shape stenciling](https://go.googlesource.com/proposal/+/master/design/generics-implementation-gcshape.md)

{{% /tab %}}

{{% tab header="Python" %}}

Python 没有「泛型代码生成」这一步：类型参数在运行时是普通对象（`TypeVar` 实例），泛型类与泛型函数都只是带注解的常规对象。最该先知道的是 `Stack[int]` 生成的是一个 `typing._GenericAlias`，可以放进注解、可以 `get_args`，但不能用于 `isinstance`。

```python
import typing
from typing import TypeVar

T = TypeVar("T")

class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None: self._items.append(item)
    def pop(self) -> T: return self._items.pop()

def first[T](xs: list[T]) -> T: return xs[0]

print(type(Stack[int]))            # <class 'typing._GenericAlias'>
print(typing.get_args(Stack[int])) # (<class 'int'>,)
print(Stack.__type_params__)       # (T,)
print(first.__type_params__)       # (T,)
print(Stack.__class_getitem__)     # <built-in method __class_getitem__ of type object ...>

s: Stack[int] = Stack()            # 实参只在注解里，对象本身不知道 int
s.push("not an int")               # 运行时照样通过
print(s.pop())                     # not an int
print(typing.get_origin(Stack[int]))   # <class '__main__.Stack'>（实参被剥离）
```

CPython 的 `_GenericAlias` 只做两件事：保存原对象与实参元组，并在被调用时把实参交给原对象构造。内建容器的 `list[int]`、`dict[str, int]` 走的是另一套 `types.GenericAlias`（由 `list.__class_getitem__` 产生），两者虽然不是同一个类，但同样不能用于 `isinstance` 与 `issubclass`：`isinstance(x, list[int])` 抛 `TypeError`，`issubclass(list[int], list)` 也会报错；唯一安全的用法是 `typing.get_origin()` 加 `typing.get_args()` 做结构分析，例如实现自己的序列化框架时按 `get_args` 递归处理。运行时真正可用的类型线索只有三种：值本身的 `type()`、`__annotations__`（Python 3.14 起是延迟求值的注解，用 `annotationlib.get_annotations` 取）以及实例上可能存在的 `__orig_class__`。性能上泛型没有任何开销，因为运行的是同一份字节码。

📘 [Python · types.GenericAlias](https://docs.python.org/3/library/stdtypes.html#types-generic-alias)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 在 JVM 上和其他 JVM 语言一样是类型擦除：`List<String>` 与 `List<Int>` 编译后都是 `List`，元素类型在字节码里不存在。最该先知道的是 `inline fun <reified T>` 是唯一例外——inline 把函数体复制到调用点，实参在编译期已知，于是 `T` 可以当类型用。

```kotlin
// 普通泛型：擦除，运行时拿不到 T
class Box<T>(val value: T)
fun <T> describe(box: Box<T>): String = "Box(${box.value})"

// reified + inline：唯一能在运行时使用 T 的写法
inline fun <reified T> Any.isInstanceOf(): Boolean = this is T
inline fun <reified T> typeName(): String = T::class.simpleName ?: "?"

// 擦除的直接证据：这两个函数签名冲突，无法共存
// fun f(x: List<String>) {}
// fun f(x: List<Int>) {}        // 🛑 Platform declaration clash

// 想保留类型实参，只能显式传入 KClass 或 TypeToken
class Token<T>(val type: Class<T>)

fun main() {
    println(describe(Box(1)))             // Box(1)
    println(describe(Box("a")))           // Box(a)
    println("x".isInstanceOf<String>())   // true
    println(1.isInstanceOf<String>())     // false
    println(typeName<List<String>>())     // List
    println(Token(String::class).type)    // class java.lang.String
}
```

擦除导致的第一类问题是重载冲突：`f(List<String>)` 与 `f(List<Int>)` 在 JVM 上签名相同（都是 `f(List)`），同一个类里不能并存，只能改名或用 `@JvmName` 标注。第二类问题是运行时判断：`x is T` 与 `T::class` 都要求 `T` 是 reified，而 reified 又要求函数是 inline，所以不能出现在接口方法、虚函数、构造器里，也不能被当作值传递（不能用 `::` 取引用）。第三类问题是协变擦除后的桥方法：Kotlin 编译器会生成 bridge 方法让 `List<String>` 与 `List<Int>` 共享实现，反编译时看到多出来的 `Object` 版本方法属于正常现象。需要完整类型信息时，标准做法是显式传入 `KClass<T>`、`java.lang.reflect.Type`（TypeToken 模式）或改用 `kotlin.reflect.typeOf`。

📘 [Kotlin · 内联函数与 reified 类型参数](https://kotlinlang.org/docs/inline-functions.html#reified-type-parameters)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的泛型是编译期擦除：`T` 编译后变成它的上界（默认 `Object`），字节码里没有类型实参。最该先知道的是为了让擦除后的子类仍然「看起来」重写了泛型方法，编译器会生成桥方法（bridge method）。

```java
import java.util.ArrayList;
import java.util.List;

class Node<T> implements Comparable<Node<T>> {
    final T value;
    Node(T value) { this.value = value; }
    @Override public int compareTo(Node<T> other) { return 0; }
}

class IntNode extends Node<Integer> {
    IntNode(Integer v) { super(v); }
    // 源码里只写了这一个方法
    @Override public int compareTo(Node<Integer> other) { return 1; }
}

void main() {
    List<String> a = new ArrayList<>();
    List<Integer> b = new ArrayList<>();
    // 擦除后的运行时类型完全相同
    System.out.println(a.getClass() == b.getClass());        // true
    System.out.println(a.getClass().getName());              // java.util.ArrayList

    // 桥方法：IntNode 上会出现编译器合成的 bridge=true 方法
    for (var m : IntNode.class.getDeclaredMethods()) {
        System.out.println(m.getName() + " " + m.getParameterTypes()[0].getSimpleName()
            + " bridge=" + m.isBridge());
    }
    System.out.println(new IntNode(1).compareTo(new Node<Integer>(2)));  // 1
}
```

反射打印会看到 `IntNode` 上有两个 `compareTo`：源码里写的 `compareTo(Node<Integer>)` 擦除后就是 `compareTo(Node)`（`bridge=false`，是真正的实现），编译器另外合成了一个参数类型为 `Object` 的 `compareTo(Object)`（`bridge=true`），它负责把 `Comparable<Node<Integer>>` 擦除后的签名 `compareTo(Object)` 转成 `compareTo(Node)` 再委派给真正的实现。桥方法的副作用是反射遍历方法时会看到「重复」的方法名，写注解处理器或序列化框架时必须过滤 `isBridge()`。擦除带来的四类硬限制是：不能 `new T[]`（只能 `(T[]) new Object[n]`）、不能 `new T()`（要传 `Class<T>` 或 `Supplier<T>`）、不能 `instanceof T`、不能定义泛型数组类型 `T[]` 字段以外的静态泛型成员。反过来，`Class<T>` 令牌、`TypeToken`（Guava）与 `getGenericSuperclass()` 是绕开擦除的标准手段——用法是让子类把实参写进父类签名，再由反射读出来。

📘 [JLS §4.6 · 类型擦除](https://docs.oracle.com/javase/specs/jls/se25/html/jls-4.html#jls-4.6)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 模板的实现模型是编译期实例化：模板本身不是代码，只有被具体实参实例化之后才生成代码，效果与 Rust 的单态化一致。最该先知道的是实例化发生在使用点，因此模板定义必须对使用点可见，否则链接期报未定义符号。

```cpp
#include <cstdio>
#include <string>
#include <vector>

template <class T>
T twice(T v) { return v + v; }        // 每个 T 实例化一份

template <class T>
struct Counter { static int count; };  // 每个 T 有独立的静态成员
template <class T> int Counter<T>::count = 0;

// 显式实例化定义：强制在本编译单元生成
template int twice<int>(int);
int main() {
    std::printf("%d %f\n", twice(21), twice(1.5));   // 42 3.000000
    std::printf("%zu\n", sizeof(Counter<int>));      // 1（空类占 1 字节）
    Counter<int>::count = 1;
    Counter<double>::count = 2;
    std::printf("%d %d\n", Counter<int>::count, Counter<double>::count); // 1 2
}
```

`Counter<int>::count` 与 `Counter<double>::count` 是两个完全独立的变量，这是模板实例化最直观的证据：模板不是「一个类」，而是「一张生成类的图纸」。工程上的核心问题是分离编译：如果把模板定义放在 `.cpp` 里而只在头文件里留声明，别的编译单元实例化时会找不到定义，链接期报 `undefined reference`；解决方案是显式实例化（`template class Counter<int>;`）配合 `extern template class Counter<int>;` 抑制其它编译单元的重复实例化，标准库容器就是这么处理的。常见坑还有模板错误信息的长度（一个类型不符会展开整条实例化链）、`std::vector<bool>` 这种特化带来的代理引用，以及可变参数模板 + 折叠表达式写错时的展开顺序问题。

📘 [cppreference · 模板实例化](https://en.cppreference.com/w/cpp/language/class_template#Explicit_instantiation)

{{% /tab %}}

{{% tab header="C" %}}

C 没有任何编译期的类型参数机制，「泛型」只能靠预处理器宏在文本层面复制代码，或者靠 `void *` 把类型信息推到运行时。最该先知道的是宏展开发生在预处理阶段，用 `clang -E` 可以直接看到「实例化」的产物。

```c
#include <stdio.h>

/* 参数化宏：文本展开即"实例化"，每个类型一份独立代码 */
#define DECLARE_SUM(name, type) type name(type x, type y) { return x + y; }
DECLARE_SUM(sum_i, int)
DECLARE_SUM(sum_d, double)

#define MAX(a, b) ((a) > (b) ? (a) : (b))   /* 无类型检查 */

int main(void) {
    printf("%d\n", sum_i(1, 2));          /* 3 */
    printf("%.1f\n", sum_d(1.5, 2.5));    /* 4.0 */
    printf("%d\n", MAX(1, 2));            /* 2 */
    printf("%s\n", MAX("a", "b"));        /* b（比较指针，标准未指定） */
    return 0;
}
```

用 `clang -E -P` 预处理后，`sum_i` 与 `sum_d` 会变成两个实实在在被写出来的函数定义（下面是预处理输出片段，只作对照、不能单独编译）：

```c
int sum_i(int x, int y) { return x + y; }
double sum_d(double x, double y) { return x + y; }
printf("%s\n", (("a") > ("b") ? ("a") : ("b")));
```

这就是 C 的「单态化」：没有类型系统参与，只有文本复制，所以 `MAX("a", "b")` 会静默地比较指针。另一条路线是运行时分派：`qsort`、`bsearch` 接受 `void *` 加元素大小加函数指针，一份代码服务所有类型，代价是每次比较都要间接调用，且类型错误没有任何编译期保护。两条路线在实际项目里经常混用：数据结构用宏或 `_Generic` 生成类型专属版本（如内核的 `list_head`、uthash），算法用 `void *` 保持通用。

📘 [cppreference · 预处理器](https://en.cppreference.com/w/c/preprocessor)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的泛型没有独立的编译步骤，但 JIT 会为**每个具体类型组合**生成特化代码，效果等价于单态化。最该先知道的是「泛型函数 + 具体实参 = 特化编译」这件事是自动的，用 `@code_typed` 与 `@code_native` 可以直接看到生成结果。

```julia
abstract type Shape end
struct Circle <: Shape; r::Float64; end
struct Square <: Shape; a::Float64; end

# 泛型函数：方法表按签名分派，JIT 按具体类型特化
area(s::Circle) = pi * s.r^2
area(s::Square) = s.a^2
area(s::T) where {T<:Shape} = error("unimplemented")

# 参数化类型 + UnionAll：容器布局随参数变化
struct Pair{T}; a::T; b::T; end

println(area(Circle(1.0)))            # 3.141592653589793
println(area(Square(2.0)))            # 4.0
println(sizeof(Pair{Int8}))           # 2
println(sizeof(Pair{Int64}))          # 16

# 查看特化产物：两个不同类型得到两份不同的优化后代码
println(Base.return_types(area, (Circle,)))   # (Float64,)
println(Base.return_types(area, (Square,)))   # (Float64,)
```

`@code_typed area(Circle(1.0))` 会显示编译器为 `Circle` 生成的类型推断结果与优化后的 IR，`@code_native` 则给出机器码——两者都随实参类型变化，这就是 Julia 被称为「为每个类型组合特化」的原因。特化的收益是数值代码可以消去装箱、内联到底；代价是「类型不稳定」的代码会让编译器生成大量分支与方法实例（所谓的 type instability 惩罚），以及首次调用时的编译延迟（time to first plot 问题）。`Pair{Int8}` 占 2 字节、`Pair{Int64}` 占 16 字节，说明参数直接决定了内存布局，这也是参数化类型不变的物理原因。实践中判断是否发生特化的工具是 `@code_warntype`（标红的变量表示类型推断失败）与 `Base.return_types`。

📘 [Julia · 方法](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的泛型由 CLR 直接支持，是**运行时具体化**的：类型实参作为元数据保留下来，`typeof(T)` 在运行时给出真实类型。最该先知道的是 CLR 对引用类型实参共享一份 JIT 代码（靠元数据区分），对值类型实参各自生成一份，这与 Java 的擦除形成鲜明对照。

```csharp
using System;
using System.Collections.Generic;

class Box<T> { public T Value; public Box(T v) => Value = v; }

class Program
{
    static void Main()
    {
        // 值类型：int 与 long 各有一份 JIT 代码，且无装箱
        var bi = new Box<int>(1);
        var bl = new Box<long>(2L);
        Console.WriteLine(bi.Value + bl.Value);              // 3
        Console.WriteLine(typeof(Box<int>) == typeof(Box<long>));  // False

        // 引用类型：string 与 object 共享同一份代码（Canonical instantiation）
        Console.WriteLine(typeof(Box<string>) == typeof(Box<object>));  // False（类型不同）
        Console.WriteLine(typeof(Box<string>).GetGenericArguments()[0]); // System.String

        // 运行时能拿到类型实参，反射也能
        var t = typeof(Box<>);
        Console.WriteLine(t.IsGenericTypeDefinition);        // True
        var closed = t.MakeGenericType(typeof(int));
        Console.WriteLine(closed == typeof(Box<int>));       // True

        // default(T) 与 new T() 可用，正因为 T 是具体化的
        Console.WriteLine(default(int));                     // 0
        Console.WriteLine(Activator.CreateInstance<int>());  // 0
    }
}
```

CLR 的具体化有两层含义：一是类型实参写进了类型的元数据，所以 `typeof(Box<int>)` 与 `typeof(Box<long>)` 是不同对象，反射能读能构造（`MakeGenericType`）；二是 JIT 的代码共享策略——引用类型实参（`string`、`object`、任何类）共享同一份机器码，因为指针表示相同，具体类型的差异靠元数据查表解决；值类型实参因为布局不同必须各自生成代码。这正是泛型集合对值类型没有装箱开销的原因，也是 C# 泛型比 Java 泛型在数值密集场景更快的关键。代价是运行时元数据体积增加，以及 `MakeGenericType` 走反射路径时无法内联；`default(T)` 对引用类型给 `null`、对值类型给零值，而 `new T()` 需要 `new()` 约束（`struct` 隐含满足）。

📘 [MS Learn · .NET 中的泛型](https://learn.microsoft.com/en-us/dotnet/standard/generics/)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型是具体化（reified）的：类型实参在运行时可见，AOT 与 JIT 都能据此做特化与内联。最该先知道的是「具体化」既是能力也是成本——每个类型实参组合都有自己的运行时类型表示，检查与类型对象的内存开销随组合数增长。

```dart
class Box<T> {
  final T value;
  const Box(this.value);

  // T 可以在运行时使用
  bool isT(Object? o) => o is T;
  String get typeName => T.toString();
}

// 上界是 num，所以可以对 T 调用 +；结果再断言回 T
T sum<T extends num>(List<T> xs) => xs.reduce((a, b) => (a + b) as T);

void main() {
  const b = Box<int>(1);
  print(b.typeName);                    // int
  print(b.isT(1));                      // true
  print(b.isT("a"));                    // false

  // 类型实参进入运行时类型，is 检查是真实的
  print(<int>[1] is List<num>);         // true  ← 泛型协变
  print(<num>[1] is List<int>);         // false
  print(<String>[] is List<Object>);    // true
  print(sum([1, 2, 3]));                // 6
  print(sum([1.5, 2.5]));               // 4.0

  // 具体化的代价：不同实参是不同的运行时类型
  print(identical(Box<int>, Box<int>)); // true（同一类型对象缓存）
  print(Box<int> == Box<double>);       // false
}
```

具体化让 Dart 能做 `o is T`、能用 `T.toString()`、能在 `catch` 里按泛型类型区分异常，也让 `List<int>` 与 `List<double>` 在运行时是不同类型，这对 Flutter 的热重载与反射式框架很有用。代价是每次泛型实例化都要在运行时构造并缓存类型对象，类型检查也要真的执行；在 AOT 编译的移动端，编译器会尽可能把检查静态化（尤其是带 `T extends num` 这类具体上界时），但完全擦除是不可能的。另一个实践要点是上界的选择会决定能否调用成员：`T extends num` 才能写 `total += x`，无上界时 `T` 等价于 `Object?`，只能调用 `Object` 的方法。

📘 [Dart · 泛型是具体化的](https://dart.dev/language/generics#generic-collections-and-the-types-they-contain)

{{% /tab %}}

{{% tab header="R" %}}

R 是解释执行的语言，没有编译期泛型，也没有为类型参数生成代码的步骤；它只有运行时的 S3/S4 分派。最该先知道的是「实现模型」在 R 里等于「按 class 属性查方法表」，成本主要是方法查找而不是代码生成。

```r
# 没有编译期实例化，只有运行时按 class 属性查表
speak <- function(x, ...) UseMethod("speak")
speak.default <- function(x, ...) "unknown"
speak.dog <- function(x, ...) "woof"

d <- structure(list(), class = "dog")
print(speak(d))                 # [1] "woof"

# 方法表在运行时查找：改一个函数就立刻改变行为
speak.dog <- function(x, ...) "WOOF"
print(speak(d))                 # [1] "WOOF"

# 用 microbenchmark 观察分派成本（伪代码，需先安装该包）
# microbenchmark::microbenchmark(speak(d), speak.default(d))

# 字节码编译：函数体会被编译成字节码，但泛型分派仍在运行时
f <- compiler::cmpfun(function(x) x + 1)
print(f(1))                     # [1] 2
print(compiler::enableJIT(-1))  # 查询当前 JIT 级别（R 3.4 起默认开启，返回整数）
```

R 的函数调用在解释器里按名查找：`UseMethod("speak")` 会查看第一个参数的 `class` 属性、尝试 `speak.dog`、`speak.default`，找不到就报错。这种方法查找每次调用都要跑一遍，所以把 S3 泛型用在最内层循环里会有明显开销；`compiler::cmpfun()` 与 JIT（R 3.4 起默认开启）能把函数体编译成字节码，但分派本身仍按名解析。`vapply` 比 `sapply` 快的原因之一就是它不需要在每次迭代后猜测返回类型，能提前确定结果向量的类型与长度，也避免了 `sapply` 可能的类型提升与列表回退。S4 的方法分派更严格也更慢，R5/R6 用引用语义与类定义换取更接近主流 OOP 的写法，但它们都不改变「没有编译期类型参数」这一事实。

📘 [R · 性能与编译](https://cran.r-project.org/doc/manuals/r-release/R-ints.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的「泛型」全部是 comptime 求值：函数返回类型、类型参数、字段布局都在编译期算出来，编译器为每个类型组合生成一份代码。最该先知道的是这等于手写的单态化，二进制体积与编译时间都会随实例数量增长，而 `@sizeOf` 与 `@typeName` 是观察实例的直接手段。

```zig
const std = @import("std");

// 返回类型的函数：编译期按参数生成一个 struct 类型
fn Vector(comptime T: type, comptime n: usize) type {
    return struct {
        data: [n]T,               // 长度进入类型，布局随 n 变化

        const Self = @This();
        pub fn len(self: *const Self) usize { return n; }
        pub fn get(self: *const Self, i: usize) T { return self.data[i]; }
    };
}

// 泛型算法：comptime 分派到不同实现，而不是运行时查表
fn doubleAll(v: anytype) @TypeOf(v) {
    var out = v;
    for (&out.data) |*x| x.* = x.* * 2;
    return out;
}

pub fn main() void {
    var v3 = Vector(i32, 3){ .data = .{ 1, 2, 3 } };
    var v4 = Vector(f64, 4){ .data = .{ 1, 2, 3, 4 } };
    const d3 = doubleAll(v3);
    std.debug.print("{} {} {}\n", .{ v3.len(), v3.get(0), d3.data[0] }); // 3 1 2
    std.debug.print("{} {}\n", .{ @sizeOf(@TypeOf(v3)), @sizeOf(@TypeOf(v4)) }); // 12 32
    std.debug.print("{s}\n", .{@typeName(@TypeOf(v3))});  // 类型名含 Vector(i32,3)
    _ = &v4;
}
```

`Vector(i32, 3)` 与 `Vector(f64, 4)` 在 `@typeName` 里是不同的类型名，`@sizeOf` 分别是 12 与 32 字节，这证明每个组合都生成了独立的类型与代码，与 Rust 单态化、C++ 模板实例化是同一类方案。comptime 的威力在于类型本身可以参与计算：`Vector(T, n)` 的返回类型是 comptime 表达式，`n` 直接进入内存布局，越界访问在编译期就能被查出（`v3.data[5]` 编译失败）。代价有三点：编译期代码必须有确定的值，任何依赖运行时数据的类型构造都无法表达；实例数量会线性推高编译时间与二进制体积；`comptime` 与运行时代码的边界需要显式标注（`comptime` 参数、`comptime` 块），写错会导致「无法在编译期求值」的报错。

📘 [Zig · comptime 与泛型](https://ziglang.org/documentation/master/#Generic-Data-Structures)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有编译期的泛型实现，它在加载 `chunk` 时编译成字节码，但字节码里只有通用指令，与「元素类型」无关。最该先知道的是 Lua 的所有多态都发生在运行时，靠值的类型标签与元方法，没有任何特化代码生成。

```lua
-- 只有一份通用代码，运行时按值的类型选择行为
local function add(a, b)
  return a + b            -- 数字相加、字符串拼接、或调用 __add
end

print(add(1, 2))          -- 3
print(add("a", "b"))      -- ab
print(add(1.5, 2))        -- 3.5

-- 元表提供"按类型"分派的唯一手段
local Vec = {}
Vec.__index = Vec
Vec.__add = function(x, y) return setmetatable({v = x.v + y.v}, Vec) end
Vec.__tostring = function(x) return "Vec(" .. x.v .. ")" end
local v = setmetatable({v = 1}, Vec) + setmetatable({v = 2}, Vec)
print(tostring(v))        -- Vec(3)

-- 字节码层面的证据：同一函数对不同类型的指令流相同
print(string.dump(function(a, b) return a + b end) ~= nil)   -- true
print(debug.getinfo(add, "S").what)                          -- "Lua"
print(type(add))                                             -- function
print(collectgarbage("count") > 0)                           -- true
```

Lua 的算术与比较运算符会先看操作数的原始类型（`number`、`string` 可自动转换），都不匹配时才查元表的 `__add`、`__concat`、`__lt` 等字段。所以「泛型」在 Lua 里等于「写一份通用代码，把差异交给运行时的类型标签和元表处理」。`string.dump` 可以把函数导出成字节码，对比不同参数调用的字节码长度能证明没有为类型生成特化版本。性能上这意味着一份代码服务所有类型，指令缓存友好，但每次运算都有类型检查开销；想加速只能靠把热循环改写成局部变量、用整数（Lua 5.3+ 的 integer 子类型）而不是浮点，以及避免在循环里触发元方法调用。

📘 [Lua 5.5 · 值与类型](https://www.lua.org/manual/5.5/manual.html#2.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的泛型在生成 JavaScript 时被完全擦除：类型参数、约束、条件类型、映射类型都不会产出任何代码。最该先知道的是「擦除」在这里比 Java 更彻底——连运行时类型对象都没有，产物里只剩下类型注解消失后的原始逻辑。

```typescript
// 泛型在产物中完全消失：下面这些写法生成的 JS 一模一样
function identity<T>(x: T): T { return x; }
function identityAny(x: any): any { return x; }

// 映射类型、条件类型只存在于类型世界
type Partial2<T> = { [K in keyof T]?: T[K] };
type Unwrap<T> = T extends Promise<infer U> ? U : T;

// 运行时唯一能用的手段：手写类型守卫
interface User { name: string; age: number }
function isUser(x: unknown): x is User {
  return typeof x === "object" && x !== null
    && typeof (x as User).name === "string"
    && typeof (x as User).age === "number";
}

console.log(identity(1));                       // 1
console.log(identity("a"));                     // a
console.log(isUser({ name: "a", age: 1 }));     // true
console.log(isUser({ name: "a" }));             // false
const u: Partial2<User> = { name: "a" };
console.log(JSON.stringify(u));                 // {"name":"a"}
type N = Unwrap<Promise<number>>;               // number（纯类型，产物里没有）
console.log(typeof identity, identity.length);  // function 1
```

因为擦除彻底，TypeScript 可以与任何 JavaScript 库互操作、产物体积极小、也不需要为泛型准备运行时支持；代价是运行时没有任何类型保证——从 `JSON.parse`、`localStorage`、网络请求拿到的数据都只是 `any`/`unknown`，把它断言成 `User` 不会做任何检查。TS 4.7 的 `in`/`out` 型变标注和 TS 5.0 的 `const` 类型参数同样只在编译期起作用，作用是让类型检查更精确更快。工程上要注意 `enum`、`namespace`、装饰器、参数属性这四类会生成运行时代码的构造，它们是擦除规则之外的特例；如果项目要求产物完全可预测，可以开启 `isolatedModules` 并优先使用 `const` 对象加字面量联合替代 `enum`。

📘 [TS 手册 · 泛型与类型擦除](https://www.typescriptlang.org/docs/handbook/2/generics.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 没有编译期泛型，也就没有实现模型可言：V8 之类的引擎做的是运行时内联缓存（inline cache）与隐藏类优化，与类型参数无关。最该先知道的是 JS 引擎的多态分派靠值的形状（shape）而不是声明，所以「泛型函数」的性能取决于调用点的类型是否单一。

```javascript
// 同一份代码服务所有类型，引擎按调用点的实际类型做内联缓存
function add(a, b) { return a + b; }

console.log(add(1, 2));          // 3
console.log(add("a", "b"));      // ab
console.log(add([1], [2]));      // 12（数组也是对象，+ 触发 toString）

// 单态调用点：只见过一种类型 → 最快
function doubleNums(xs) {
  const out = new Array(xs.length);
  for (let i = 0; i < xs.length; i++) out[i] = xs[i] * 2;
  return out;
}
console.log(doubleNums([1, 2, 3]));        // [2, 4, 6]

// 多态调用点：同一个函数被不同类型的实参反复调用 → 退化为字典查找
console.log(doubleNums([1.5, 2.5]));       // [3, 5]
console.log(doubleNums(["1", "2"]));       // [2, 4]（字符串被强制转换）

// 类型信息只在值上
console.log(typeof add, add.length);       // function 2
console.log(Object.keys(add));             // []（函数没有运行时类型参数）
```

因为没有类型参数，JS 引擎只能靠运行时的反馈优化：第一次调用记录实参的隐藏类，之后命中就直接走快速路径，一旦出现新的类型就退化为多态甚至超态（megamorphic）查表。这解释了为什么「泛型风格」的工具函数在数据形状统一时很快、混着数字与字符串调用时突然变慢。要在 JS 里得到类型保证只有两条路：把 JSDoc/TypeScript 放在构建期（`tsc --checkJs`、JSDoc 的 `@template`），或者在运行时手写守卫（`typeof`、`Array.isArray`、`Number.isFinite`）。压测与诊断用 `node --trace-opt`、`--trace-deopt` 观察函数是否被优化与反优化，比猜测类型参数更实际。

📘 [V8 · 内联缓存](https://v8.dev/blog/ignition-interpreter)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 没有泛型，也没有为泛型生成代码的步骤；它的执行模型是「编译成 opcode + 运行时类型检查」。最该先知道的是 docblock 里的 `@template` 完全不参与执行，只有 PHPStan/Psalm 这类外部工具会读它。

```php
<?php
declare(strict_types=1);

/**
 * @template T
 */
class Stack
{
    /** @var list<T> */
    private array $items = [];

    /** @param T $item */
    public function push(mixed $item): void { $this->items[] = $item; }

    /** @return int */
    public function count(): int { return count($this->items); }
}

$s = new Stack();
$s->push(1);
$s->push("mixed in");           // 运行时不会报错，PHPStan 会报错
echo $s->count(), PHP_EOL;      // 2

// 运行时可见的"实现"只有 opcode 与反射：没有类型实参
$r = new ReflectionClass(Stack::class);
echo $r->getName(), PHP_EOL;                                  // Stack
echo count($r->getMethods()), PHP_EOL;                        // 2（push 与 count）
echo $r->getMethod('push')->getParameters()[0]->getType(), PHP_EOL;  // mixed
echo $r->getProperty('items')->getType(), PHP_EOL;            // array（docblock 的 list<T> 反射不到）
echo function_exists('opcache_get_status') ? "opcache ext loaded" : "no opcache ext", PHP_EOL;

// 变通：为每种元素类型写一个薄子类
class TypedStack extends Stack { }
final class IntStack extends TypedStack { /** @param int $item */ public function push(mixed $item): void { parent::push($item); } }
(new IntStack())->push(2);
echo "ok", PHP_EOL;                                           // ok
```

PHP 的类型检查发生在运行时：`push(mixed $item)` 接受任何值，只有把参数类型改成具体类型（`int $item`）才会在调用点抛 `TypeError`。因此 PHP 里表达「泛型容器」的常见做法是「为每种元素类型写一个薄子类」或者直接用 `array` 加运行时断言；前者牺牲复用，后者牺牲静态保证。`@template` 注解的价值在于让 PHPStan 在分析期把 `Stack` 视作 `Stack<T>` 并检查调用一致性，但它对产物零影响。Opcache 缓存的是编译产物本身（opcode），与类型参数无关；运行时能用 `ReflectionClass`、`getType()` 读到的是具体类型（或 `mixed`），读不到任何实参。

📘 [PHP · 反射](https://www.php.net/manual/en/book.reflection.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 没有泛型，也没有编译期的类型参数；它的执行模型是解析成字节码（YARV）再解释执行，类型检查全部发生在运行时。最该先知道的是 Ruby 的「实现模型」里根本没有为类型生成代码这一步，同一段方法对任何类型都是同一份字节码。

```ruby
# 一份字节码服务所有类型
def add(a, b) = a + b

puts add(1, 2)            # 3
puts add("a", "b")        # ab
puts add(1.5, 2)          # 3.5

# 观察工具：RubyVM::InstructionSequence 能看到"泛型"消失后的指令
iseq = RubyVM::InstructionSequence.of(method(:add))
puts iseq.disasm.lines.first(3).join   # == disasm: #<ISeq:add@...>
puts iseq.to_a[13].size                # 字节码指令条数（与类型无关）

# 想特化只能自己写：按类分支
def double(x)
  case x
  when Integer then x * 2
  when String then x * 2          # 字符串的 * 是重复
  when Array then x.map { |e| e * 2 }
  end
end
puts double(3)             # 6
puts double("ab")          # abab
puts double([1, 2]).inspect # [2, 4]

# 运行时类型查询：只有值上的 class 与 respond_to?
puts 1.class, "a".class, [].class   # Integer String Array
```

Ruby 的方法体只有一份，`+` 的实现由接收者的类决定（`Integer#+`、`String#+`、`Array#+` 各不同），这就是动态分派：一份字节码 + 运行时的类查表。`RubyVM::InstructionSequence` 能反汇编出真实指令，可以看到泛型参数不会在指令里留下任何痕迹，因为语言里根本没有。要「特化」只能手写 `case`/`when` 分支，或者定义多个同名方法让它按参数类型分派——Ruby 不支持方法重载，所以只能靠 `case` 或关键字参数。外部工具方面，Sorbet 的 `sig { params(x: T).returns(T) }` 与 RBS 的 `.rbs` 文件能把类型契约从代码里分离出来交给静态检查器，但它们同样不生成任何特化代码。

📘 [Ruby · RubyVM::InstructionSequence](https://docs.ruby-lang.org/en/master/RubyVM/InstructionSequence.html)

{{% /tab %}}

{{< /tabpane >}}

### 运行时类型、反射与常见坑

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的泛型在编译后被单态化成具体类型，因此运行时可以用 `TypeId` 与 `dyn Any` 做类型判断，但拿不到「类型参数的字符串名」这种语言级保证。最该先知道的是 `TypeId::of::<T>()` 要求 `T: 'static`，而 `PhantomData<T>` 只影响型变与所有权，不占运行时空间。

```rust
use std::any::{Any, TypeId};
use std::marker::PhantomData;

fn name_of<T: 'static>() -> &'static str { std::any::type_name::<T>() }

// PhantomData<T>：标记"逻辑上拥有 T"，但零大小
struct Tag<T>(PhantomData<T>);

fn main() {
    println!("{}", TypeId::of::<i32>() == TypeId::of::<i32>());   // true
    println!("{}", TypeId::of::<i32>() == TypeId::of::<i64>());   // false
    println!("{}", name_of::<Vec<String>>());   // alloc::vec::Vec<alloc::string::String>

    // dyn Any：擦除后的运行时向下转型
    let boxed: Box<dyn Any> = Box::new(7i32);
    println!("{}", boxed.downcast_ref::<i32>().copied().unwrap_or(0));  // 7
    println!("{}", boxed.downcast_ref::<i64>().is_none());              // true

    let _t: Tag<u8> = Tag(PhantomData);
    println!("{}", std::mem::size_of::<Tag<u8>>());               // 0
    println!("{}", std::mem::size_of::<Option<Box<dyn Any>>>());  // 16
}
```

`type_name::<T>()` 返回的字符串仅供诊断，标准库明确说明它不是稳定接口（格式可能随版本变化），绝不能用它做逻辑判断；要判断类型请用 `TypeId`。`dyn Any` 的 `downcast_ref`/`downcast_mut`/`downcast` 是运行时的类型检查，失败返回 `None`/`Err` 而不是 panic，这也是插件系统与依赖注入的常见做法。`PhantomData<T>` 占 0 字节，它只参与编译器对所有权、型变与 drop check 的推理，所以 `Tag<u8>` 不占空间；把它写成 `PhantomData<fn() -> T>` 就能强行让结构体协变，这在 unsafe 封装里很常用。名称里的 `'_` 是生命周期占位符（`struct Ref<'a, T>(&'a T)` 写作 `Ref<'_, T>`），与泛型类型参数是两套东西，不能混用。

📘 [Rust std · `Any`](https://doc.rust-lang.org/std/any/trait.Any.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的类型元数据在运行时完整保留，所以 `T.self`、`type(of:)`、`Mirror` 都能工作；`any` 会把具体类型装进 existential 容器，元数据仍然可用。最该先知道的是 `T.self` 给出的是类型值（可以当参数传递），而 `Mirror` 给出的是**结构**反射（字段名与子值），两者用途不同。

```swift
import Foundation

// T.self：把类型本身当值传递
func typeName<T>(_ t: T.Type) -> String { String(describing: t) }

struct Probe<T> {
    func describe(_ v: T) -> String {
        let m = Mirror(reflecting: v)   // 结构反射：只看字段，不看类型语义
        return "T=\(T.self) children=\(m.children.count)"
    }
}
struct Point { let x: Int; let y: Int }
// 需要类型擦除时手写闭包即可（Dog 是上面未定义的示例类型，这里补上）
struct Dog { func speak() -> String { "woof" } }

print(typeName(Int.self))                          // Int
print(Probe<[Int]>().describe([1, 2, 3]))          // T=Array<Int> children=3
print(Probe<Point>().describe(Point(x: 1, y: 2)))  // T=Point children=2

// any：装箱后类型信息仍在，可以按具体类型分派
let things: [Any] = [1, "a", 2.5]
for t in things {
    switch t {
    case is Int: print("Int")           // Int
    case is String: print("String")     // String
    default: print("other")             // other
    }
}
// 完整类型擦除只能靠闭包手工完成（类型擦除器 / type eraser）
let erase: () -> String = { Dog().speak() }
print(erase())                                     // woof
```

`T.self` 与 `type(of:)` 的区别是静态与动态：`T.self` 在泛型上下文里给出类型参数本身，`type(of: x)` 给出运行时值的动态类型（对 `any` 容器里的值是具体类型）。`Mirror` 只能读字段名与子值，无法调用方法，也无法修改；它适合做调试打印与 Codable 风格的通用遍历，不适合做业务分派。`any` 会把关联类型擦掉，所以 `any Sequence<Int>` 仍然知道元素是 `Int`（主要关联类型还在元数据里），但 `any Collection` 就只剩 `count` 之类不依赖关联类型的成员。想要完全的类型擦除（例如在同一个数组里装不同具体类型的同协议对象，同时隐藏具体类型），标准做法是手写类型擦除器：用一个 `struct AnyProducer` 包一个闭包，把 `Output` 固定成具体类型。

📘 [Swift · `Mirror`](https://developer.apple.com/documentation/swift/mirror)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的泛型在编译期被 stencil 成有限几份代码，运行时可以用 `reflect` 观察具体类型；但类型参数 `T` 本身不是一个可以拿出来的值。最该先知道的是约束接口（类型集）不能用来声明变量，所以「拿到 `T` 的类型」只能通过反射一个真实的 `T` 值。

```go
package main

import (
	"fmt"
	"reflect"
)

type Number interface{ ~int | ~int64 | ~float64 }

type Box[T any] struct{ v T }

func (b Box[T]) TypeOf() reflect.Type { return reflect.TypeOf(b.v) }

func describe[T any](v T) string { return fmt.Sprintf("%T %v", v, v) }

func main() {
	fmt.Println(describe(1))        // int 1
	fmt.Println(describe("s"))      // string s
	fmt.Println(describe([]int{1})) // []int [1]

	fmt.Println(Box[int]{1}.TypeOf())      // int
	fmt.Println(Box[string]{"a"}.TypeOf()) // string

	var x any = 3.5
	fmt.Println(reflect.TypeOf(x).Kind())  // float64
	fmt.Println(reflect.TypeOf(x).Name())  // float64

	// 🛑 类型集约束不能声明变量：
	// var n Number = 1
	// cannot use type Number outside a type constraint:
	// interface contains type constraints
}
```

Go 里拿到运行时类型的唯一途径是反射一个真实值：`reflect.TypeOf(v)`、`any` 类型断言、`%T` 动词都要有一个值在手，`reflect.TypeOf[T]()` 这样的写法不存在。`reflect.TypeOf(b.v)` 之所以能工作，是因为 `b.v` 的类型已经是单态化后的具体类型；如果 `Box[T]` 里的字段从未被实例化，就没法凭空问出 `T`。类型集约束的限制是语言层面的硬规则：`Number interface{ ~int | ~float64 }` 只能出现在类型参数的位置（`func F[T Number](x T)`），写成 `var n Number = 1` 会得到 `cannot use type Number outside a type constraint: interface contains type constraints`，因为类型集没有可调用的方法集，用它声明变量没有任何可用的操作。常见坑还包括：`reflect` 的 `NumMethod` 看不到泛型方法（泛型方法必须先实例化才能获取），以及反射调用的性能远低于直接调用。

📘 [Go 包文档 · `reflect.TypeOf`](https://pkg.go.dev/reflect#TypeOf)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的「运行时类型」始终存在（值自带类型），但泛型类型参数只活在注解里；`typing.get_type_hints()` 与 Python 3.14 的 `annotationlib` 是读取注解的正规途径。最该先知道的是 3.14 起注解改为延迟求值（PEP 649/749），因此读取注解强烈建议用 `annotationlib.get_annotations` 而不是直接碰 `__annotations__`。

```python
import annotationlib
import typing
from typing import get_type_hints, TypeVar

T = TypeVar("T")

class Box[T]:
    def __init__(self, value: T) -> None:
        self.value: T = value
    def get(self) -> T: return self.value

def first[T](xs: list[T]) -> T: return xs[0]
def add(a: int, b: int) -> int: return a + b

print(get_type_hints(add))     # {'a': <class 'int'>, 'b': <class 'int'>, 'return': <class 'int'>}
print(get_type_hints(first))   # {'xs': list[T], 'return': T}（T 是 TypeVar，不是具体类型）
print(Box.__type_params__)     # (T,)
print(typing.get_args(Box[int]))  # (<class 'int'>,)
b = Box[int](1)
print(b.__orig_class__)        # __main__.Box[int]
print(annotationlib.get_annotations(Box.get, format=annotationlib.Format.STRING))
# {'return': 'T'}（STRING 格式不执行求值，直接给字符串）

# 泛型不强制：越界传值不会报错
print(first([1, "a"]))         # 1
print(Box("not an int").get()) # not an int

# isinstance 不能带参数化类型
try:
    isinstance(b, Box[int])
except TypeError as e:
    print("TypeError:", e)     # TypeError: Subscripted generics cannot be used with class and instance checks
```

`get_type_hints()` 会把字符串前向引用求值成对象，因此它能处理 `def f(x: "Box[int]")`，但遇到无法求值的名字仍会抛 `NameError`；3.14 的 `annotationlib` 提供了 `Format.FORWARDREF` 与 `Format.STRING` 两种更安全的读取方式，前者把未定义名字包成 `ForwardRef`，后者直接给字符串。`isinstance(x, Box[int])` 会抛 `TypeError`，因为 `Box[int]` 是 `typing._GenericAlias`；正确做法是 `isinstance(x, Box)` 再检查 `typing.get_args`。运行时要真正校验类型，只有两条路：逐个值做 `isinstance`/`type()` 检查，或引入 `beartype`、`typeguard`、`pydantic` 这类会在运行时代入注解并校验的库。最后一条实践建议是把泛型当成文档与静态检查工具，不要指望它在运行时拦住错误的调用。

📘 [Python · annotationlib](https://docs.python.org/3/library/annotationlib.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 在 JVM 上擦除，所以普通泛型的运行时类型只有一个办法：`inline` + `reified`。最该先知道的是 `typeOf<T>()` 也要 reified，它返回 `KType`（反射对象）而不是 `Class<T>`，想要 Java 的类对象还要再取 ` classifier`。

```kotlin
import kotlin.reflect.KType
import kotlin.reflect.typeOf

// reified：只有在 inline 函数里才能使用 T
inline fun <reified T> kindOf(value: Any): String = when {
    value is T -> "match"
    else -> "no match"
}
inline fun <reified T> ktype(): KType = typeOf<T>()

class Repo<T>(private val cls: Class<T>) {           // 显式传 Class<T>（Java 风格）
    fun newInstanceOrNull(): T? = cls.getDeclaredConstructor().newInstance()
}

class Empty

fun main() {
    println(kindOf<String>("a"))          // match
    println(kindOf<Int>("a"))             // no match
    println(ktype<List<Int>>())           // kotlin.collections.List<kotlin.Int>
    println(ktype<List<Int>>().arguments) // [kotlin.Int]

    val r = Repo(Empty::class.java)
    println(r.newInstanceOrNull()!!::class.simpleName)   // Empty

    // 擦除的直接后果：下面这行拿不到实参
    val list: List<String> = listOf("a", "b")
    println(list::class.simpleName)       // ArrayList（不是 List<String>）
    println(list is List<*>)              // true
    // println(list is List<String>)      // 🛑 编译错误：Cannot check for instance of erased type
}
```

`typeOf<List<Int>>()` 能给出带实参的 `KType`，这是 reified 的直接产物；而 `list::class` 只能给 `ArrayList`，因为 JVM 的类对象里没有实参。想保留完整类型信息有两条标准路线：显式传 `Class<T>`（只能表达非泛型实参）、或传 `kotlin.reflect.KType`/`TypeToken`（能表达 `List<String>` 这种嵌套实参，代价是需要额外的库或反射开销）。常见坑有三个：`is T` 只在 reified 时合法，普通泛型函数里写 `x is T` 直接编译失败；`inline` 函数不能持有非 public API（否则报 `Public-API inline function cannot access non-public-API`），也不能是虚函数或构造器；`typeOf<T>()` 在 Java 互操作场景下会返回 `KType`，需要再调 `.javaType` 才能给 Java 反射使用。

📘 [Kotlin · `typeOf`](https://kotlinlang.org/api/core/kotlin-stdlib/kotlin.reflect/type-of.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的泛型在运行时被擦除，所以反射拿不到 `T`；要保留类型信息必须让实参出现在可反射的位置。最该先知道的是 `getGenericSuperclass()` 能读到子类写在 `extends` 里的实参，`Class<T>` 令牌则是最简单的显式传递方式。

```java
import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;

// TypeToken 模式：把实参写进父类签名，反射时读出来
abstract class TypeRef<T> {
    final Type type;
    TypeRef() {
        Type sup = getClass().getGenericSuperclass();
        this.type = ((ParameterizedType) sup).getActualTypeArguments()[0];
    }
}

// Class<T> 令牌：只能表达非泛型实参
class Factory<T> {
    private final Class<T> type;
    Factory(Class<T> type) { this.type = type; }
    String name() { return type.getSimpleName(); }
}

void main() {
    List<String> a = new ArrayList<>();
    System.out.println(a.getClass() == new ArrayList<Integer>().getClass());  // true
    // a instanceof List<String>     // 🛑 编译错误：泛型不可具体化

    System.out.println(new TypeRef<List<String>>() {}.type);   // java.util.List<java.lang.String>
    System.out.println(new TypeRef<List<Integer>>() {}.type);  // java.util.List<java.lang.Integer>
    System.out.println(new Factory<>(String.class).name());     // String

    // 堆污染：泛型可变参数 + 未检查写入
    List<String>[] arr = (List<String>[]) new List<?>[1];       // 未检查警告
    List raw = arr;
    raw.add(1);                                                 // 运行时堆污染
    System.out.println(arr.length);                             // 1
}
```

`TypeRef` 能工作，是因为匿名子类把 `List<String>` 写进了 `extends TypeRef<List<String>>`，这段签名会作为泛型签名写进 class 文件，`getGenericSuperclass()` 才读得到；反过来 `new TypeRef<List<String>>() {}` 里的 `{}` 不能省，省了就没有子类、也读不到实参。`Class<T>` 令牌简单但没有嵌套信息，`List<String>.class` 这种写法不存在。堆污染（heap pollution）指往泛型容器里塞进类型不符的元素，典型触发点是泛型可变参数 `T...`（编译成 `Object[]` 后可以写入异类）与原始类型（raw type）混用，`@SafeVarargs` 只能作为「我不会污染」的声明而不能真正检查。实践中最容易踩的还有：`List<int[]>` 与 `List<Integer[]>` 都能编译但含义完全不同、`Arrays.asList(intArray)` 会得到 `List<int[]>` 而不是 `List<Integer>`。

📘 [Java 教程 · 泛型的限制](https://docs.oracle.com/javase/tutorial/java/generics/restrictions.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的运行时类型信息（RTTI）只对多态类型有效：`typeid` 在多态对象上给动态类型，在非多态对象上给静态类型；`type_traits` 则是纯编译期查询。最该先知道的是 `-fno-rtti` 会让 `typeid` 与 `dynamic_cast` 直接无法编译，很多二进制体积敏感的项目会关掉它。

```cpp
#include <cstdio>
#include <typeinfo>
#include <type_traits>
#include <vector>

struct Base { virtual ~Base() = default; };
struct Derived : Base {};

int main() {
    // 多态类型：typeid 给出动态类型
    Derived d;
    Base& b = d;
    std::printf("%s\n", typeid(b).name());              // 7Derived（clang 修饰名）
    std::printf("%d\n", typeid(b) == typeid(Derived));  // 1

    // 非多态类型：typeid 只给静态类型
    int x = 1;
    std::printf("%s\n", typeid(x).name());              // i
    std::printf("%d\n", typeid(int) == typeid(x));      // 1

    // 编译期反射：type_traits
    static_assert(std::is_integral_v<decltype(x)>);
    static_assert(!std::is_polymorphic_v<decltype(x)>);
    static_assert(std::is_polymorphic_v<Base>);
    std::printf("%d %zu\n", std::is_same_v<std::vector<int>, std::vector<int>>,
                sizeof(std::vector<int>));              // 1 24

    // 模板实例的类型名是修饰名，不可移植也不可读
    std::printf("%s\n", typeid(std::vector<int>).name());
    // libc++: NSt3__16vectorIiNS_9allocatorIiEEEE
    return 0;
}
```

`typeid(...).name()` 返回的是实现定义的修饰名（Itanium ABI 下的 `i`、`St6vector...`），既不可读也不可移植；想看可读名字要用 `abi::__cxa_demangle`（libstdc++/libc++ 的扩展）或 `boost::typeindex`。`typeid` 的另一个限制是它忽略顶层 `const`/`volatile`，`typeid(const int) == typeid(int)` 为真，所以不能靠它区分限定符。编译期查询才是 C++ 元编程的主角：`std::is_same_v`、`std::is_integral_v`、`std::is_polymorphic_v`、`std::is_trivially_copyable_v` 与 `concepts` 一起构成了「模板里的 if」。常见坑有：`dynamic_cast` 对引用失败时抛 `std::bad_cast`、对指针失败时返回 `nullptr`，两种写法要分别处理；`typeid(*p)` 对多态类型的空指针解引用会抛 `std::bad_typeid`，对非多态类型则是不求值的静态类型，不会抛错。

📘 [cppreference · `typeid`](https://en.cppreference.com/w/cpp/language/typeid)

{{% /tab %}}

{{% tab header="C" %}}

C 没有运行时类型信息，也没有反射：`void *` 只是一个地址，类型只存在于编译期的表达式里。最该先知道的是 `_Generic` 是唯一的「类型查询」手段，而它在预处理之后就被替换掉了，运行时什么也不剩。

```c
#include <stdio.h>
#include <stddef.h>

/* 编译期的类型选择：_Generic 在翻译期完成，运行时无残留 */
#define type_name(x) _Generic((x),                     \
    int: "int", long: "long",                          \
    double: "double", char *: "char *",                \
    const char *: "const char *", default: "unknown")

int main(void) {
    printf("%s\n", type_name(1));         /* int */
    printf("%s\n", type_name(1L));        /* long */
    printf("%s\n", type_name(1.0));       /* double */
    printf("%s\n", type_name("s"));       /* char * */
    printf("%s\n", type_name(1.0f));      /* unknown（float 不在列表里） */

    /* void* 不带类型标签：赋给它的那一刻类型就丢了 */
    int a = 7;
    void *p = &a;
    printf("%s\n", p ? "no type tag" : "null");   /* no type tag */
    printf("%d\n", *(int *)p);                    /* 7（靠调用者记得类型） */

    /* 唯一运行时可用的"类型"信息是大小与对齐 */
    printf("%zu %zu\n", sizeof(int), _Alignof(double));   /* 4 8 */
    return 0;
}
```

`_Generic` 的关联列表匹配的是**表达式的类型**，因此 `1.0f` 会落到 `default`（`float` 没列出），`"s"` 匹配 `char *` 而不是 `const char *`（字符串字面量的类型是 `char[N]`，会退化为 `char *`）。这种分派不产生任何运行时代码，指令里看不到分支。没有类型标签的后果是错误完全靠人保证：把 `int *` 存进 `void *` 再按 `double *` 读出来，编译器不会警告，程序会读到垃圾值；`sizeof` 与 `_Alignof` 只能告诉你大小与对齐，不能告诉你类型。需要运行时类型信息时，C 项目通常自己加一个枚举标签（tagged union / 判别式），例如 `struct Value { enum { I, D, S } tag; union { int i; double d; char *s; }; }`，这正是「判别联合」在 C 里的手写版本；调试信息（DWARF）里有类型信息，但那属于调试器与工具链，语言本身拿不到。

📘 [cppreference · `_Generic`](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的类型是一等公民：`typeof` 可以在任何值上调用，`isa`/`<:` 做判断，`typeintersect` 与 `typejoin` 在类型层面做集合运算。最该先知道的是类型参数在运行时可见（`typeof([1,2])` 给出 `Vector{Int64}`），这与 Java 的擦除完全相反。

```julia
abstract type Animal end
struct Dog <: Animal end
struct Cat <: Animal end

struct Box{T}; value::T; end

# 运行时看类型：完整实参都在
println(typeof([1, 2, 3]))          # Vector{Int64}
println(typeof(Box(1.5)))           # Box{Float64}
println(1 isa Number, 1.0 isa Int)  # truefalse
println(Int <: Real, Real <: Int)   # truefalse

# 类型层面的集合运算
println(typeintersect(Int, Real))   # Int64
println(typejoin(Int, Float64))     # Real
println(typeintersect(Int, String)) # Union{}
println(supertypes(Int))            # (Signed, Integer, Real, Number, Any)

# 从类型参数反查具体类型
f(x::Box{T}) where {T} = T
println(f(Box(1)))                  # Int64
println(f(Box("a")))                # String

# 泛型容器里每个元素都自带类型
xs = Any[1, "a", Dog()]
println(map(typeof, xs))            # DataType[Int64, String, Dog]
```

`where {T}` 把类型参数绑定成函数体内的一个**类型值**，可以当普通值使用（返回值、做 `isa` 判断、构造新类型 `Vector{T}()`），这是 Julia 泛型最灵活的地方，也是它参数化类型不变、但函数签名可以用 `<:` 表达「任意子类型」的原因。`typeintersect` 求两个类型集合的交，`typejoin` 求最小公共上界，`Union{}` 是空类型（不含任何值、是所有类型的子类型，因此 `Union{} <: Nothing`）——这些函数在方法分派与类型推断里都是核心工具。性能上的关键概念是「类型稳定性」：如果函数返回类型依赖运行时值，编译器无法特化，`@code_warntype` 会把这类变量标红。常见坑是用 `Vector{Any}` 装数值，每个元素都装箱，数值循环会慢一到两个数量级；正确做法是参数化容器类型或使用 `Union` 小联合。

📘 [Julia · 类型检查与转换](https://docs.julialang.org/en/v1/manual/types/#Type-Conversions-and-Promotion)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的泛型在 CLR 上具体化，所以 `typeof(T)`、`default(T)`、`new T()` 全都能用，反射也能拿到完整实参。最该先知道的是这些能力都有约束前提：`new T()` 需要 `new()`，`sizeof(T)` 需要 `unmanaged`，`is T` 则不需要任何约束。

```csharp
using System;
using System.Collections.Generic;

class Factory<T> where T : new()
{
    public T Create() => new T();                    // 需要 new() 约束
    public Type RuntimeType() => typeof(T);          // 无需任何约束
    public T Fallback() => default(T);               // 无需任何约束
}

static class Probe
{
    public static bool IsOf<T>(object o) => o is T;  // 无需约束
    public static int SizeOf<T>() where T : unmanaged => sizeof(T);
}

class Empty { }

class Program
{
    static void Main()
    {
        var f = new Factory<Empty>();
        Console.WriteLine(f.RuntimeType());                 // Empty
        Console.WriteLine(f.Create() is Empty);             // True
        Console.WriteLine(f.Fallback() == null);            // True（引用类型给 null）
        Console.WriteLine(Probe.IsOf<string>("a"));         // True
        Console.WriteLine(Probe.SizeOf<long>());            // 8

        // 反射读实参：具体化让这一步成为可能
        Type t = typeof(Dictionary<string, List<int>>);
        foreach (var arg in t.GetGenericArguments())
            Console.WriteLine(arg);   // System.String / System.Collections.Generic.List`1[System.Int32]

        // 从类型参数构造：泛型定义 + 实参
        var open = typeof(List<>);
        Console.WriteLine(open.MakeGenericType(typeof(int)) == typeof(List<int>));  // True

        // 常见坑：class 约束下的 == 是引用比较
        Console.WriteLine(RefEq<string>("ab", new string(new[] { 'a', 'b' })));   // False
    }

    static bool RefEq<T>(T a, T b) where T : class => a == b;
}
```

`default(T)` 对值类型给零值、对引用类型给 `null`，所以 `T` 加了 `notnull` 之后 `default(T)` 仍然可能在语义上不合法（例如 `string`），.NET 会用 `MaybeNull`/`NotNull` 之类的特性来标注，但这属于分析器范畴。运行时反射能读出 `Dictionary<string, List<int>>` 的完整实参树，`MakeGenericType` 还能从开放泛型构造封闭类型——这两点都是 Java 做不到的。常见坑有四类：`class` 约束下 `==` 永远是引用比较，值相等要用 `EqualityComparer<T>.Default` 或约束 `IEquatable<T>`；`is T` 对 `T` 是需要运行时的类型检查（但比 `GetType() == typeof(T)` 更宽松，子类型也算）；`typeof(T)` 在泛型类里对每个实例化都不同，不能缓存成静态只读字段（那会变成每个 `T` 一份，通常正是想要的）；AOT/裁剪（NativeAOT、IL trimming）下反射构造泛型可能被裁掉，需要 `DynamicDependency` 或 `rd.xml` 声明。

📘 [MS Learn · `typeof`](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/type-testing-and-cast)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型具体化，所以在运行时 `T` 可以直接用于 `is` 判断，`Type` 对象也能通过 `T.toString()` 或 `runtimeType` 拿到。最该先知道的是 `T` 只有在「泛型类型参数处于作用域内」时才可用，静态成员与顶层函数里的 `T` 无处可来。

```dart
class Box<T> {
  final T value;
  const Box(this.value);

  bool holds(Object? o) => o is T;          // T 可以直接用于 is
  String get name => T.toString();          // 也能取到类型名
}

T? castOrNull<T>(Object? o) => o is T ? o : null;   // 泛型函数里 T 同样可用

void main() {
  const b = Box<int>(1);
  print(b.holds(1));                  // true
  print(b.holds("a"));                // false
  print(b.name);                      // int

  print(castOrNull<String>("a"));     // a
  print(castOrNull<String>(1));       // null

  // 运行时类型对象：类型实参是真实存在的
  print(<int>[].runtimeType);         // List<int>
  print(<int>[] is List<int>);        // true
  print(<int>[] is List<num>);        // true（协变）
  print(<num>[] is List<int>);        // false
  print(const <int>[] is List<Object>); // true

  // 类型擦除在 Dart 里不成立：这与 Java 刚好相反
  print(<String>[] is List<String>);  // true（Java 里这行根本编译不过）

  // 坑：null 与泛型的交互
  print(castOrNull<int>(null));       // null
  print(<int?>[null] is List<int?>);  // true
}
```

`o is T` 会真的执行运行时类型检查，`T.toString()` 给出可读的类型名（`int`、`List<int>`），`runtimeType` 返回完整的 `Type` 对象。这与 Java 的 `instanceof List<String>` 不可写形成鲜明对照，也是 Dart 能在运行时做泛型序列化、泛型反序列化与依赖注入的根基。需要注意三点：泛型类型参数是可空的（`T` 默认相当于 `T extends Object?`），写 `T extends Object` 才能保证非空；`is T` 与 `as T` 都只在 `T` 处于作用域时可用，静态方法与顶层函数必须自己声明 `<T>`；具体化带来运行时开销，AOT 编译器会尽量把已知具体类型的检查优化掉，但在泛型参数完全未知的代码里每次 `is` 都是真实检查。

📘 [Dart · 运行时类型检查](https://dart.dev/language/type-system#runtime-checks)

{{% /tab %}}

{{% tab header="R" %}}

R 的运行时类型信息分两层：`typeof()` 给出底层存储类型，`class()` 给出 S3/S4 的类属性；泛型的「类型参数」在 R 里根本不存在。最该先知道的是 `typeof` 与 `class` 经常不一致：`typeof(1)` 是 `double` 而 `class(1)` 是 `numeric`，`typeof(factor(1))` 是 `integer` 而 `class(factor(1))` 是 `factor`。

```r
x <- factor(c("a", "b"))
print(typeof(x))            # [1] "integer"   ← 底层存储
print(class(x))             # [1] "factor"    ← 语义类型
print(is.factor(x))         # [1] TRUE
print(inherits(x, "factor"))# [1] TRUE

# S3/S4 分派靠 class 属性
print(methods("print"))     # 列出大量 print.* 方法
print(getS3method("print", "factor"))   # 拿到具体实现

# 想要更现代的工具可以引入 rlang：类型谓词与参数匹配
# rlang::is_s3(x)、rlang::is_s4(x)、rlang::arg_match("dog", c("dog", "cat"))

# 没有泛型类型参数：容器的"元素类型"靠运行时内容决定
lst <- list(1L, 2.5, "a")
print(vapply(lst, typeof, ""))    # [1] "integer" "double" "character"
print(sapply(lst, class))         # [1] "integer" "numeric" "character"
```

`class()` 返回的字符串向量就是 S3 的「类型层次」，`inherits()`、`NextMethod()`、`UseMethod()` 都基于它工作；`typeof()` 则完全不看类属性，只看底层存储。这解释了为什么 `class(1L)` 是 `"integer"` 而 `class(1)` 是 `"numeric"`（`double` 的 class 是 `numeric`），也解释了为什么对因子直接做算术会得到整数编码而不是报错。S4 用 `is()`、`extends()`、`slotNames()` 提供更严格的查询，`R5`/`R6` 用引用语义的类；`rlang` 的 `is_s3()`、`is_s4()`、`arg_match()` 让这些检查更易读。实践上最容易踩的坑是把 `class()` 的返回值当稳定契约：数据框的 `class` 可能是 `c("tbl_df", "tbl", "data.frame")` 这样的多层向量，只判断 `"data.frame"` 会漏掉 `tbl` 的特有行为，应该用 `inherits(x, "data.frame")`。

📘 [R · `class` 与 `typeof`](https://stat.ethz.ch/R-manual/R-devel/library/base/html/class.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的反射发生在编译期：`@TypeOf` 取类型，`@typeInfo` 取类型的结构描述，然后由 `comptime` 分支决定生成什么代码。最该先知道的是运行时没有任何类型信息，`@typeInfo` 的结果在编译完成后就消失了，想留下线索必须自己把类型名或标签存进数据里。

```zig
const std = @import("std");

fn describe(x: anytype) void {
    const T = @TypeOf(x);
    switch (@typeInfo(T)) {
        .int, .comptime_int => std.debug.print("int {d}\n", .{x}),
        .float, .comptime_float => std.debug.print("float {d}\n", .{x}),
        .pointer => |p| std.debug.print("pointer to {s}\n", .{@typeName(p.child)}),
        .@"struct" => |s| std.debug.print("struct with {d} fields\n", .{s.fields.len}),
        .optional => std.debug.print("optional\n", .{}),
        else => std.debug.print("other {s}\n", .{@typeName(T)}),
    }
}

// comptime 反射：遍历结构体字段，生成通用打印
fn dumpFields(x: anytype) void {
    inline for (@typeInfo(@TypeOf(x)).@"struct".fields) |f| {
        std.debug.print("{s}={}\n", .{ f.name, @field(x, f.name) });
    }
}

pub fn main() void {
    describe(1);                       // int 1
    describe(1.5);                     // float 1.5
    var byte: u8 = 1;
    describe(&byte);                   // pointer to u8
    describe(.{ .a = 1, .b = 2 });     // struct with 2 fields
    std.debug.print("{s}\n", .{@typeName(@TypeOf(true))});   // bool
    dumpFields(.{ .x = 1, .y = 2 });   // x=1 / y=2
    var opt: ?u8 = null;
    describe(opt);                     // optional
}
```

`@typeInfo(T)` 返回的是 `std.builtin.Type` 联合体，可以匹配 `.int`、`.float`、`.pointer`、`.@"struct"`、`.optional`、`.@"enum"` 等标签并按标签取相关字段；Zig 0.14 起这些标签与字段名统一改成小写风格，从 0.13 迁移的代码需要同步改名。`inline for` 让循环在编译期展开，因此 `dumpFields` 能为任意结构体生成针对性的打印代码——这是 Zig 版的「反射」，但完全是编译期的，产物里没有元数据表。运行时想识别类型只有两条路：把类型当作显式的枚举标签存进数据（tagged union），或者把 `@typeName(T)` 的字符串存下来做诊断。常见坑是 `@typeInfo` 只接受类型而不是值（要用 `@TypeOf(x)` 包一层）、以及 `comptime` 分支里不能做任何 I/O 或运行时判断。

📘 [Zig · `@typeInfo`](https://ziglang.org/documentation/master/#typeInfo)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有编译期泛型，运行时也没有「类型参数」；它有的是每个值自带的类型标签与 `type()`、`math.type()` 这类查询。最该先知道的是 `type()` 只区分八种基础类型，用户类型的区分要自己用元表或字段标记。

```lua
-- 基础类型查询
print(type(1), math.type(1))        -- number	integer
print(type(1.0), math.type(1.0))    -- number	float
print(type("a"), type({}), type(print))  -- string	table	function
print(type(nil), type(true))        -- nil	boolean

-- 区分"用户类型"：靠元表或字段标签
local Dog = {}; Dog.__index = Dog
local Cat = {}; Cat.__index = Cat
local function new(cls) return setmetatable({}, cls) end

local function kindof(v)
  if type(v) ~= "table" then return type(v) end
  local mt = getmetatable(v)
  if mt == Dog then return "Dog" end
  if mt == Cat then return "Cat" end
  return "table"
end

print(kindof(new(Dog)))             -- Dog
print(kindof(new(Cat)))             -- Cat
print(kindof({}))                   -- table

-- 泛型代码只能靠运行时检查兜底
local function sum(xs)
  assert(type(xs) == "table", "sum: table expected, got " .. type(xs))
  local t = 0
  for _, v in ipairs(xs) do
    assert(type(v) == "number", "sum: number expected, got " .. type(v))
    t = t + v
  end
  return t
end
print(pcall(sum, {1, 2, 3}))        -- true	6
print(pcall(sum, {1, "a"}))         -- false	sum: number expected, got string
```

`type()` 永远返回基础类型字符串，`math.type()` 才能区分 `integer` 与 `float`（Lua 5.3 起 number 有这两个子类型）。用户类型只能靠元表身份（`getmetatable(v) == Dog`）或约定字段（`v.__kind`）来识别，`io.type()`、`debug.getinfo()` 是标准库为特定对象提供的专用查询。因为泛型不存在，通用函数的类型约束只能靠 `assert` 在入口处检查，失败时用 `error` 抛出带 `level` 的错误信息；`pcall`/`xpcall` 捕获后可以继续处理。常见坑有：`#` 长度运算符只对序列有意义，含 `nil` 洞的表长度未定义；`ipairs` 遇到 `nil` 就停，遍历可能提前结束，要用 `pairs` 或 `next` 明确表达意图。

📘 [Lua 5.5 · `type`](https://www.lua.org/manual/5.5/manual.html#pdf-type)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的类型在运行时完全不存在，反射只能靠值本身与手写守卫；类型参数 `T` 在产物里是一个被删掉的名字。最该先知道的是判别联合（discriminated union）加类型守卫是唯一能得到可靠运行时分支的模式。

```typescript
// 1. 判别联合：用字面量字段区分，运行时真的能读到
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "rect"; w: number; h: number };

function area(s: Shape): number {
  switch (s.kind) {                 // 判别字段是运行时存在的值
    case "circle": return Math.PI * s.r ** 2;
    case "rect": return s.w * s.h;
  }
}

// 2. 类型守卫：把运行时检查的结果反馈给类型系统
function isShape(x: unknown): x is Shape {
  if (typeof x !== "object" || x === null) return false;
  const k = (x as { kind?: unknown }).kind;
  return k === "circle" || k === "rect";
}

// 3. 运行时拿不到类型参数
function first<T>(xs: T[]): T | undefined { return xs[0]; }

console.log(area({ kind: "rect", w: 2, h: 3 }));   // 6
console.log(isShape({ kind: "circle", r: 1 }));    // true
console.log(isShape({ kind: "square" }));          // false
console.log(first([1, 2, 3]));                     // 1
console.log(typeof first, first.length);           // function 1
// console.log(first<string>([1]) is string)       // 类型参数不参与运行时

// 4. 反射可用信息只有构造器名与原型链
class Box<T> { constructor(public value: T) {} }
const b = new Box(1);
console.log(b.constructor.name);                   // Box
console.log(Object.getPrototypeOf(b).constructor.name); // Box
console.log(b instanceof Box);                     // true
```

类型守卫的返回值写成 `x is Shape` 时，编译器会在 `if` 分支内把 `x` 收窄成 `Shape`，这是把运行时检查「接回」静态类型系统的标准做法。`asserts x is T`（断言函数）与 `satisfies` 运算符是另外两个相关工具：前者让函数抛错时也能收窄，后者只检查赋值兼容而不改变推断出的类型。运行时能拿到的信息只有 `constructor.name`、`instanceof`、`typeof`、`Object.keys` 与 `Symbol.toStringTag`；`constructor.name` 在代码压缩后会变，生产环境不要依赖它做逻辑，应该用显式的判别字段。最后一个常见坑是 `as` 与泛型一起用时会「假装」类型正确：`JSON.parse(text) as User` 不做任何校验，正确的做法是先 `as unknown` 再用守卫逐字段验证，或者用 `zod`、`valibot` 这类 schema 库在运行时真正解析。

📘 [TS 手册 · 类型收窄](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的类型信息完全跟着值走，所以「反射」就是查值的构造器、原型链与 `typeof`；泛型类型参数不存在，也就无从反射。最该先知道的是 `typeof` 有一批历史遗留的奇怪结果，跨 realm（iframe、worker）时 `instanceof` 会失效。

```javascript
// typeof 的完整结果集：只有 8 种
const samples = [undefined, null, true, 1, 1n, "a", Symbol("s"), {}, function () {}];
console.log(samples.map((v) => typeof v));
// [ 'undefined', 'object', 'boolean', 'number', 'bigint', 'string', 'symbol', 'object', 'function' ]
console.log(typeof null);                       // object ⚠️ 历史遗留
console.log(Array.isArray([]));                 // true（typeof [] 也是 object）

// 构造器与原型链
class Box { constructor(v) { this.value = v; } }
const b = new Box(1);
console.log(b.constructor.name);                // Box
console.log(b instanceof Box);                  // true
console.log(Object.getPrototypeOf(b) === Box.prototype); // true

// Object.prototype.toString：跨 realm 也可靠
console.log(Object.prototype.toString.call([]));       // [object Array]
console.log(Object.prototype.toString.call(new Map())); // [object Map]
console.log(Object.prototype.toString.call(null));      // [object Null]

// 判别字段：运行时区分联合类型的唯一可靠手段
function area(shape) {
  switch (shape.kind) {
    case "circle": return Math.PI * shape.r ** 2;
    case "rect": return shape.w * shape.h;
    default: throw new Error("unknown shape");
  }
}
console.log(area({ kind: "rect", w: 2, h: 3 }));  // 6
```

`typeof null === "object"` 是 1995 年的实现遗留，无法修复；`typeof` 对数组、`Date`、`Map`、正则都返回 `"object"`，因此判断具体内建类型要用 `Array.isArray`、`Object.prototype.toString.call` 或 `instanceof`。`instanceof` 沿原型链查找，跨 realm（不同 iframe、`node:vm` 上下文）时同一个类的原型对象不同，`[] instanceof Array` 会变成 `false`，此时 `Array.isArray` 才是正确工具。`constructor.name` 在打包压缩后会被改名（`Box` 变成 `t`），所以不能作为业务逻辑的依据。要在 JS 里得到接近泛型的类型安全，只有三条路：构建期用 JSDoc/TypeScript 检查、运行时用 schema 校验库（`zod`、`ajv`）、以及在数据结构里显式存判别字段——最后一条最朴素也最可靠。

📘 [MDN · `typeof`](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Operators/typeof)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 有完整的运行时类型信息（`gettype`、`get_debug_type`、反射），但没有泛型类型参数；`gettype` 与 `get_debug_type` 的区别正是最该先知道的一点。反射读到的参数类型永远是具体类型或 `mixed`，读不到任何实参。

```php
<?php
declare(strict_types=1);

class Box {}

$vals = [null, true, 1, 1.5, "a", [1], new Box(), fopen('php://memory', 'r')];
foreach ($vals as $v) {
    // gettype 给旧式名字，get_debug_type 给现代名字（PHP 8.0+）
    echo gettype($v), " / ", get_debug_type($v), PHP_EOL;
}
// NULL / null
// boolean / bool
// integer / int
// double / float
// string / string
// array / array
// object / Box
// resource / resource (stream)

// 反射：泛型实参不存在，只能看到声明时的类型
/** @param list<int> $xs */
function total(array $xs): int { return array_sum($xs); }
$r = new ReflectionFunction('total');
echo $r->getParameters()[0]->getType()->getName(), PHP_EOL;   // array
echo $r->getReturnType()->getName(), PHP_EOL;                 // int

// 运行时检查：instanceof 与 is_* 系列
echo (new Box()) instanceof Box ? "yes" : "no", PHP_EOL;      // yes
echo is_int(1) && is_array([1]) ? "ok" : "no", PHP_EOL;       // ok
echo count(get_declared_classes()) > 0 ? "loaded" : "none", PHP_EOL;  // loaded
```

`gettype()` 返回 `integer`、`double`、`NULL` 这样的历史名字（PHP 4 时代），`get_debug_type()` 返回 `int`、`float`、`null` 并会给出对象的实际类名和资源的类型，写调试信息与错误消息应该用后者。`instanceof` 沿继承链与接口判断，`is_int`、`is_string` 这类函数用于标量。反射能给出的是声明的具体类型，`@param list<int>` 这类 docblock 只有在 PHPStan/Psalm 读取时才存在，`ReflectionParameter::getType()` 对它一无所知。标准库还提供了更细的查询工具：`get_resource_type()`（PHP 4.0.2 起）、`get_mangled_object_vars()`（PHP 7.4 起）、`enum_exists()`（PHP 8.1 起）；调试输出用 `var_dump()` 与 `var_export()` 能看出完整类型与结构，而 `print_r()` 会省略类型信息。想校验来自外部的数据，标准做法是显式判断每一个字段（`is_int($data['age'])`）或引入 `symfony/validator`、`respect/validation` 做声明式校验，而不是依赖 docblock。

📘 [PHP · `get_debug_type`](https://www.php.net/manual/en/function.get-debug-type.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的运行时类型信息非常丰富：`class`、`is_a?`、`respond_to?`、`ObjectSpace`、`method(:x).parameters` 都能查，但泛型类型参数不存在。最该先知道的是判断能力时要看 `respond_to?`（行为）而不是只看 `class`（血缘），这才是 duck typing 的运行时版本。

```ruby
# 三种查询层级：class（血缘）、is_a?（含祖先）、respond_to?（能力）
class Animal; def speak = "..." end
class Dog < Animal; def speak = "woof" end

d = Dog.new
puts d.class                # Dog
puts d.is_a?(Animal)        # true（沿祖先链）
puts d.instance_of?(Animal) # false（只判当前类）
puts d.respond_to?(:speak)  # true
puts d.method(:speak).arity # 0
puts d.methods.include?(:speak)  # true

# 单例类与匿名类让"类型"可以在运行时改变
s = "x"
def s.shout = upcase + "!"
puts s.shout                # X!
puts s.singleton_class.ancestors.first # #<Class:#<String:0x...>>

obj = Object.new
def obj.speak = "hi"
puts obj.respond_to?(:speak) # true
puts obj.is_a?(Animal)       # false（能力 ≠ 血缘）

# 没有泛型：容器的元素类型靠遍历检查
list = [1, "a", Dog.new]
puts list.map(&:class).inspect        # [Integer, String, Dog]
puts list.all? { |x| x.respond_to?(:to_s) }  # true
```

`is_a?`（别名 `kind_of?`）沿 `ancestors` 链查找，`instance_of?` 只比较当前类；`respond_to?` 检查方法是否可调用，默认不包含 `private` 方法，要传 `true` 才会算进去。`Method#parameters` 与 `Method#arity` 能在运行时读出参数形状（必选、可选、关键字、块），这是 Ruby 做 DSL 与依赖注入的常用手段。`singleton_class` 与匿名类让单个对象可以在运行时获得新方法，所以「类型」在 Ruby 里不是固定标签，而是随时可变的能力集合。常见坑有三个：`ObjectSpace` 遍历会产生大量对象引用、影响 GC 与性能；`method_missing` 配合 `respond_to_missing?` 才算完整实现，只写前者会让 `respond_to?` 返回错误结果；`is_a?` 与 `instance_of?` 的差别在代理对象（`SimpleDelegator`、`BasicObject`）上尤其明显，代理的 `is_a?` 需要显式转发。

📘 [Ruby · `Object#is_a?`](https://docs.ruby-lang.org/en/master/Object.html#method-i-is_a-3F)

{{% /tab %}}

{{< /tabpane >}}
