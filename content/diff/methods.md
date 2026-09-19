+++
title = "methods"
date = 2026-09-19T12:00:00+08:00
weight = 13
type = "docs"
description = "18 种语言的方法对照：定义与接收者、方法与函数的关系、方法解析与派发、构造析构与运算符重载等特殊方法"
isCJKLanguage = true
draft = false
+++

# 方法：18 种语言对照

函数是大家都有的东西，方法却不是：它是一段代码加上一个"接收者"。本页按四个主题组织这条线索。**定义与接收者**回答"接收者写在哪里"——Rust 放进 `impl` 块、Go 写在函数名前的括号里、Python 把它变成第一个显式参数、C 干脆没有。**方法与函数的关系**回答"方法能不能变回普通函数"——Go 的方法表达式、Rust 的 UFCS、C++ 的成员函数指针，以及各语言的扩展方法。**方法解析与派发**回答"调用哪一份实现、什么时候决定"——是编译期静态绑定还是查 vtable，是单分派还是多分派。**特殊方法**回答"构造、析构、运算符怎么用方法表达"。最根本的分歧只有两条：接收者是值还是引用、名字到实现的绑定发生在编译期还是运行时；其余所有差异几乎都能从这两条推出来。

## 方法

**一页速览**

| 语言 | 接收者写法 | 一句话说明 / 关键差异 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | `impl T { fn m(&self) }` | 方法只能定义在与类型同 crate 的 `impl` 块中；`self`/`&self`/`&mut self` 显式表达所有权 | 没有构造函数与重载；`self` 的三种形态决定能否移动、能否改 |
| Swift | `func m()`，值类型要 `mutating` | 值类型方法默认不能改自身，`mutating` 才改；`extension` 可给任意类型加方法 | 值类型方法静态派发，类方法默认走 vtable（`final` 可静态化）；协议扩展的方法不参与动态派发 |
| Go | `func (c *Counter) Inc()` | 接收者写在函数名之前，可在任意文件给本包类型加方法 | 方法集规则：值接收者的方法进 `T` 与 `*T`，指针接收者的只进 `*T` |
| Python | `def m(self, x)` | 接收者就是第一个普通参数，由描述符协议自动绑定 | 忘记 `self` 或写成 `@staticmethod` 后仍传参，运行时才报错 |
| Kotlin | `fun m()`，类内成员函数 | 类内函数即方法；扩展函数是顶层静态函数，编译期解析 | 成员函数默认 `final` 不能重写；扩展函数不能被重写、也看不到私有成员 |
| Java | `this`，类内方法 | 类内所有非 `static` 方法都带隐式 `this`；默认全部虚方法 | 默认虚 + 动态派发，构造函数里调可重写方法是经典陷阱 |
| C++ | `void m() const`，类内 | 成员函数带隐式 `this`；`virtual` 才动态派发，默认静态 | 值语义与切片：按值传基类会切掉派生部分，虚派发失效 |
| C | 没有方法 | 用「结构体 + 首参传指针」加名字前缀（`counter_init`）模拟 | 没有 `this`、没有重载、没有访问控制，全靠命名约定与自律 |
| Julia | `f(x::T) = 表达式` | 方法就是给函数加一个签名，函数名是全局的 | 多分派按全部实参选择，参数类型交集处会歧义（ambiguity） |
| C# | `this`，类内方法 | 类内非 `static` 方法带隐式 `this`；默认非虚，`virtual` 才可重写 | 扩展方法不能在扩展块里访问私有成员；C# 14 的扩展块与旧 `this` 参数可混用 |
| Dart | `this`，类内方法 | 类内方法默认虚，接口靠隐式 interface 实现 | 扩展方法（2.7+）编译期解析，不能访问私有成员；`extension type`（3.3+）是零成本包装 |
| R | `f(x, ...) UseMethod("f")` | S3/S4 泛型函数按第一个参数（S4 按全部）选方法 | S3 的 `UseMethod` 只按第一个参数分派，签名不一致会静默错配 |
| Zig | 没有方法 | 只有结构体与自由函数，首参写成 `self: *T`，`x.f(y)` 是语法糖 | 没有 `impl`、没有重载、没有 `this`；所有派发在编译期解析 |
| Lua | `function obj:m()`，冒号 | `obj:m(a)` 等价 `obj.m(obj, a)`，冒号只是把 `obj` 塞成第一个参数 | 点号与冒号混用是头号错误；`self` 不是关键字，只是约定名 |
| TypeScript | `this`，类内方法 | 类成员方法带 `this`；类型系统是结构化的 | `this` 类型只在编译期约束；扩展靠声明合并，运行时仍是 JS 原型 |
| JavaScript | `this`，类内方法 | 没有类方法的概念，只有「函数值 + 调用点的 `this`」 | 方法摘下来当变量传就丢 `this`；箭头函数没有自己的 `this` |
| PHP | `$this`，类内方法 | 类内非 `static` 方法带隐式 `$this`；8.4 起属性可有 `get`/`set` 钩子 | 没有运算符重载；魔术方法拼写错就静默不生效 |
| Ruby | `def m` / `def self.m` | 实例方法定义在类里，类方法与单例方法走 `def self.` | `method_missing` 必须与 `respond_to_missing?` 成对，否则 `respond_to?` 说谎 |

### 定义与接收者

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的方法必须写在 `impl` 块里，接收者显式声明为 `self`、`&self` 或 `&mut self` 三者之一；这是编译期就固定的静态选择，决定方法拿到的是所有权、共享借用还是独占借用。没有接收者的项叫关联函数（associated function），通过 `Type::name()` 调用，它是 Rust 表达构造函数与工厂的常规手段。Rust 也没有构造函数语法、没有重载、没有继承，方法之间的关系只能靠 trait 表达。

```rust
// /tmp/verify/methods.rs（rustc 1.98.1 实测）
struct Circle { r: f64 }

impl Circle {
    fn new(r: f64) -> Self { Circle { r } }              // 关联函数：没有 self，充当构造函数
    fn area(&self) -> f64 { 3.141592653589793 * self.r * self.r }  // &self：只读借用
    fn grow(&mut self, d: f64) { self.r += d; }           // &mut self：独占借用才能改
    fn into_r(self) -> f64 { self.r }                     // self：取得所有权，调用后 c 不可再用
}

fn main() {
    let mut c = Circle::new(1.0);       // 关联函数用 :: 调
    println!("{}", c.area());           // 3.141592653589793
    c.grow(1.0);                        // 需要 mut 绑定
    println!("{}", c.area());           // 12.566370614359172
    let r = c.into_r();                 // 消费 c；此后再用 c 就是编译错误
    println!("{}", r);                  // 2
}
```

`impl` 块可以拆成多个，也可以为泛型写带约束的实现；`&self` 的方法能用 `&mut self` 的接收者调用，反之不行，这条规则同样适用于 `impl Trait for T` 的形式。最该记住的是：接收者的三种形态不是风格问题而是所有权问题——`self` 会消耗调用者，`&mut self` 要求调用者本身可变，`&self` 最宽松。想要一个"构造函数"，就写返回 `Self` 的关联函数（社区惯例是 `new`，没有语言强制）。trait 也能定义方法并提供默认实现，`impl Trait for T` 时只覆盖需要定制的部分。

📘 [Rust · 方法语法](https://doc.rust-lang.org/book/ch05-03-method-syntax.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的实例方法写在类型内部，接收者是隐式的 `self`；值类型（`struct`、`enum`）的方法默认不能修改自身存储，必须标 `mutating` 才获得写权限，这是写时复制（copy-on-write）语义的直接后果。类型方法用 `static`（不可重写）或 `class`（类中可重写）声明，它们不带实例接收者，调用时以 `Type.method()` 的形式出现。`extension` 可以把方法加到任何已有类型上，包括来自标准库或框架的类型。

```swift
// /tmp/verify/methods.swift（swiftc 6.4 实测）
struct Counter {                             // 值类型
    var count = 0
    mutating func inc() { count += 1 }        // mutating：允许改自身字段
    func show() -> Int { count }              // 默认方法：对 self 只读
    static func make() -> Counter { Counter() }   // 类型方法：静态派发
}
class Base {
    func who() -> String { "Base" }            // 类方法默认可重写、动态派发
    class func kind() -> String { "Base" }      // class 方法：子类可 override
    final func sealed() -> String { "sealed" }   // final：禁止重写
}
class Sub: Base {
    override func who() -> String { "Sub" }
    override class func kind() -> String { "Sub" }
}
extension Counter {                          // 给已有类型补方法
    func doubled() -> Int { count * 2 }
}
var c = Counter.make()
c.inc()
print(c.show(), c.doubled())      // 1 2
print(Base().who(), Sub().who())  // Base Sub
print(Base.kind(), Sub.kind())    // Base Sub
print(Sub().sealed())             // sealed
```

`mutating` 只能用在 `struct`/`enum` 上，`class` 的方法本来就能改自身状态，标了反而是错误。值类型的方法在语义上把 `self` 当作 `inout` 参数；正因为如此，`let` 绑定的结构体实例不能调用任何 `mutating` 方法。类型方法里 `static` 与 `class` 的区别只有一个：`class` 允许子类用 `override class func` 替换实现，`static` 不允许。`extension` 里可以加方法、计算属性、构造器与协议一致性，但不能加存储属性——存储布局在类型定义时就定死了。另外，`final` 类里的所有方法都自动是静态派发，这既是性能手段也是语义声明。

📘 [Swift · 方法](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/methods/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的方法就是"带接收者参数的函数"，接收者写在 `func` 关键字与函数名之间，看起来像多出来的一组参数。接收者可以写成值类型 `(c Counter)` 或指针类型 `(c *Counter)`，这个选择不影响调用语法（`c.Inc()` 会自动取址或解引用），但严格决定了方法集与"能不能改到原对象"。方法定义必须与类型在同一个包内，但不受文件限制。

```go
// /tmp/verify/go/main.go（go 1.27.1 实测）
package main

import "fmt"

type Counter struct{ n int }

func (c Counter) Get() int { return c.n }   // 值接收者：操作副本
func (c *Counter) Inc()    { c.n++ }        // 指针接收者：改原对象
func (c Counter) String() string { return fmt.Sprintf("Counter(%d)", c.n) }

type Stringer interface{ String() string }

func New(n int) *Counter { return &Counter{n: n} }   // 没有构造函数，用 New 工厂

func main() {
	c := New(1)
	c.Inc()                    // 自动写成 (&c).Inc()
	fmt.Println(c.Get(), c.n)  // 2 2
	f := c.Get                 // 方法值：绑定接收者副本
	c.n = 99
	fmt.Println(f())           // 2  仍是绑定那一刻的副本
	g := (*Counter).Get        // 方法表达式：接收者提升为第一个显式参数
	fmt.Println(g(c))          // 99
	var s Stringer = c
	fmt.Println(s.String())    // Counter(99)
	var s2 Stringer = &Counter{5}
	fmt.Println(s2.String())   // Counter(5)
}
```

方法集规则是 Go 最容易出错的地方：类型 `T` 的方法集只包含值接收者方法，`*T` 的方法集包含值接收者与指针接收者方法；因此 `Counter` 能满足 `Stringer`，而 `*Counter` 能满足任何接口。接口变量赋值时编译器会检查方法集，把 `*T` 塞进要求指针方法的接口没问题，反过来就会编译失败。工程上的惯例是：一个类型的方法要么全用值接收者、要么全用指针接收者，混用会让方法集变得难以推理。Go 没有扩展方法（不能在别的包里给已有类型加方法），替代方案是自由函数（`strings.TrimSpace(s)`）、嵌入（embedding）或自定义类型包装。

📘 [Go spec · 方法声明](https://go.dev/ref/spec#Method_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的方法就是定义在类体里的普通函数，接收者 `self` 是第一个普通参数，由描述符协议（descriptor protocol）在属性查找时自动绑定；`@staticmethod` 取消绑定、`@classmethod` 把第一个参数换成类本身、`@property` 把方法伪装成属性访问。这套机制完全是运行时的：方法在实例字典与类字典里查找，找不到就调 `__getattr__`。类里写的就是"成员函数"，没有关键字区分实例方法与静态方法，靠装饰器表达。

```python
# /tmp/verify/methods.py（python3 3.14.7 实测）
import math

class Point:
    count = 0

    def __init__(self, x, y):          # 显式 self；只负责初始化，不负责分配
        self.x, self.y = x, y
        Point.count += 1

    @staticmethod
    def origin():                       # 静态方法：不自动传任何东西
        return Point(0, 0)

    @classmethod
    def from_pair(cls, p):               # 类方法：第一个参数是类，子类调用时拿到子类
        return cls(p[0], p[1])

    @property
    def r(self):                          # 属性：读的时候像字段，实际是方法
        return math.hypot(self.x, self.y)

    def __repr__(self):                    # 没有它就只会打印 <__main__.Point object at 0x...>
        return f"Point({self.x}, {self.y})"

class Point3(Point):
    def __repr__(self):                     # 子类覆盖表示
        return f"Point3({self.x}, {self.y})"

print(Point(3, 4).r)                       # 5.0
print(Point.origin())                      # Point(0, 0)
print(Point.from_pair([1, 2]))             # Point(1, 2)
print(Point3.from_pair([1, 2]))            # Point3(1, 2)  cls 是子类
print(Point.count)                          # 4  三个 Point + 一个 Point3
```

`@classmethod` 与 `@staticmethod` 的关键差别在于 `cls` 参数带来的多态：工厂方法写成 `cls(...)` 时，子类调用返回子类实例，写成硬编码类名就不是。`@property` 只能读，配套写法是 `@r.setter`，它让"先当字段用、以后改成计算属性"变成不破坏调用方的重构。常见陷阱有三个：`self` 只是约定名（写成 `this` 也能跑，但没人这么写）；把方法存进变量后它仍是绑定方法（`p.r` 已求值，`Point.r` 是函数对象）；`@staticmethod` 里忘记写参数列表而调用时传了参数，会得到 TypeError 而不是自动忽略。猴子补丁（给类对象赋新属性）能加方法，但作用在类上是全局的，只影响之后的新查找。

📘 [Python · 类与方法](https://docs.python.org/3/tutorial/classes.html#a-word-about-names-and-objects)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的成员函数写在类体里，接收者是隐式的 `this`；类内函数默认是 `final`，要允许子类重写必须显式标 `open`。扩展函数（extension function）语法上像方法，实际上编译成"把接收者当作第一个参数的静态函数"，因此它不能访问私有成员、也不能被重写——这是 Kotlin 与 C#/Swift 扩展机制最本质的分歧点。伴生对象（`companion object`）承担静态成员的职责。

```kotlin
class Counter(private var n: Int) {          // 主构造函数
    fun get(): Int = n                        // 成员函数：带隐式 this，默认 final
    fun inc() { n++ }
    companion object {                        // 伴生对象：放"静态"成员
        fun make(n: Int): Counter = Counter(n)
        const val KIND = "Counter"
    }
}

open class Base {
    open fun who(): String = "Base"           // open 才允许重写
    fun sealed(): String = "sealed"           // 默认 final
}
class Sub : Base() {
    override fun who(): String = "Sub"        // 必须写 override
}

fun Counter.twice(): Int = get() * 2          // 扩展函数：编译期静态解析
fun String.shout(): String = uppercase() + "!"

fun main() {
    val c = Counter.make(1)
    c.inc()
    println("${c.get()} ${c.twice()}")        // 2 4
    println(Sub().who())                      // Sub
    println("abc".shout())                    // ABC!
    // 扩展函数在编译期绑定：变量静态类型是 Base 就调 Base 的扩展
}
```

扩展函数在编译期按变量的**静态类型**解析，不参与虚派发：如果一个 `Base` 变量实际指向 `Sub`，调用的仍是 `Base` 版本的扩展函数；成员函数与扩展函数同名时，成员函数永远优先。这一点与 C# 的扩展方法一致，但 Kotlin 的扩展属性进一步放大了风险——扩展属性不能有幕后字段（backing field），因为编译器无法往别人的类里塞存储。`companion object` 里的成员用 `Counter.make(...)` 调用，与 C#/Java 的静态方法在调用点上没有差别，但它本质上是单例对象的成员。需要多态工厂就用 `open` 函数或 `@JvmStatic` 暴露给 Java。

📘 [Kotlin · 扩展](https://kotlinlang.org/docs/extensions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的实例方法写在类体里，接收者是隐式的 `this`，不需要也不能显式声明；`static` 方法没有接收者，属于类。所有非 `private`、非 `static`、非 `final` 的方法默认都是虚方法，子类用 `@Override` 重写。Java 没有扩展方法，也没有运算符重载，给已有类型加行为的常规做法是静态工具类（`Objects`、`Collections`、`Stream`）或包装类。Java 25 起构造函数体可以在 `super(...)`/`this(...)` 之前写语句（JEP 513），这是构造语义上的一次实质放宽。

```java
// 版本基线：Java 26（LTS 25）
class Counter {
    private int n;
    Counter(int n) { this.n = n; }            // 显式 this 区分字段与参数
    int get() { return n; }                    // 实例方法：默认虚
    void inc() { n++; }
    static Counter make(int n) { return new Counter(n); }   // 静态工厂
    @Override public String toString() { return "Counter(" + n + ")"; }
}

final class Positive extends Counter {
    Positive(int n) {
        if (n < 0) throw new IllegalArgumentException("negative");   // JEP 513：super 之前可写语句
        super(n);
    }
}

class Base {
    Base() { show(); }                         // ⚠️ 构造器里调可重写方法
    void show() { System.out.println("Base"); }
}
class Derived extends Base {
    private final String tag = "Derived";
    @Override void show() { System.out.println("show " + tag); }   // 会先打印 show null
}

public class Main {
    public static void main(String[] args) {
        Counter c = Counter.make(1);
        c.inc();
        System.out.println(c + " " + c.get());  // Counter(2) 2
        new Positive(1);                        // ✅ 合法
        new Derived();                          // show null ← 经典陷阱
    }
}
```

`this` 在实例方法里总是有效，但在 `static` 方法里不可用，这是初学者最常见的编译错误来源。真正的语义陷阱在继承：Java 默认虚派发意味着构造函数里调用可重写方法时，子类重写版本会在子类字段初始化之前运行，于是读到默认值。JEP 513 允许在 `super(...)` 之前写验证语句，但那段代码处于 early construction context——不能引用 `this`、不能读实例字段、不能调用实例方法，只能给本类中"没有初始化器"的字段赋值。构造函数调用自身不能出现在 `try` 块内（JVM 限制）。方法重载在 Java 里很常见，但要记住它按编译期静态类型选择，且返回类型不参与重载判定。

📘 [JEP 513 · Flexible Constructor Bodies](https://openjdk.org/jeps/513)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的成员函数写在类定义内（或类外配合 `::` 限定），带隐式的 `this` 指针；函数名后的 `const` 限定接收者只读，这是 C++ 独有的接收者修饰手段。成员函数默认静态绑定，只有声明为 `virtual` 才进入 vtable 做动态派发。C++ 支持多重继承、运算符重载、构造与析构函数，一把梭全在语言里，也因此规则最多。

```cpp
// 版本基线：C++23（g++/clang++ -std=c++23）
#include <iostream>
#include <string>

struct Counter {
    int n = 0;
    Counter() = default;
    explicit Counter(int v) : n(v) {}          // 成员初始化列表
    int get() const { return n; }               // const 成员函数：不能改字段
    void inc() { ++n; }
    virtual ~Counter() = default;               // 虚析构：多态删除必需
    virtual std::string who() const { return "Counter"; }
    static Counter make(int v) { return Counter(v); }   // 静态成员函数
};

struct Named : Counter {
    std::string name = "named";
    Named(int v, std::string s) : Counter(v), name(std::move(s)) {}   // 初始化列表按声明序
    std::string who() const override { return "Named:" + name; }
};

void byValue(Counter c) { std::cout << c.who() << '\n'; }      // 切片：动态类型丢失
void byRef(const Counter& c) { std::cout << c.who() << '\n'; }   // 保持多态

int main() {
    auto c = Counter::make(1);      // 静态成员函数用类名调
    c.inc();
    std::cout << c.get() << '\n';    // 2
    Named n{2, "a"};
    byValue(n);                      // Counter ← 切片陷阱
    byRef(n);                        // Named:a
    Counter* p = &n;
    std::cout << p->who() << '\n';    // Named:a（vtable 派发）
}
```

最需要记住的是"按值传递会切片"：`void f(Counter c)` 接收基类副本，派生部分与 vtable 指针一起被切掉，函数里只能调到基类版本；要保留多态必须传引用或指针。成员初始化列表的顺序由成员声明顺序决定，与列表书写顺序无关，写反了会产生"用未初始化值初始化"的 UB。`virtual` 有代价（对象多一个指针、调用不可内联），所以 C++ 的默认选择是静态派发，这与 Java/C# 的默认相反。`const` 成员函数参与重载：同一个名字可以同时有 `int f()` 与 `int f() const`，编译器按接收者的 const 性选择。构造/析构、运算符重载（`operator+`、`operator[]`、`operator()`）全是普通成员函数，C++ 没有单独的语法类别。

📘 [cppreference · 成员函数](https://en.cppreference.com/w/cpp/language/member_functions)

{{% /tab %}}

{{% tab header="C" %}}

C 没有方法：没有类、没有隐式接收者、没有访问控制，也没有 `this`。表达"对象上的操作"只能靠约定——把结构体指针作为第一个参数显式传进去，并在函数名上带类型前缀；想要运行期多态，就在结构体里放函数指针，手工搭出一张 vtable。C23 依然没有给语言加类语义。

```c
/* /tmp/verify/spec.c（Apple clang 21, -std=c23 实测） */
#include <stdio.h>

typedef struct { int n; } Counter;

static void counter_init(Counter *self, int n) { self->n = n; }  /* 构造靠 init 函数 */
static void counter_inc(Counter *self) { self->n += 1; }         /* 显式 self 参数 */
static int  counter_get(const Counter *self) { return self->n; } /* const 版只读 */

/* 手工 vtable：每个实例一个函数指针槽，模拟虚方法 */
typedef struct Shape Shape;
struct Shape {
    const char *name;
    double (*area)(const Shape *);          /* 约定第一个参数是"接收者" */
};
static double circle_area(const Shape *s) { (void)s; return 3.5; }
static double square_area(const Shape *s) { (void)s; return 4.0; }

int main(void) {
    Counter c;
    counter_init(&c, 1);
    counter_inc(&c);
    printf("%d\n", counter_get(&c));         /* 2 */

    Shape a = { "circle", circle_area };
    Shape b = { "square", square_area };
    Shape *list[2] = { &a, &b };
    for (int i = 0; i < 2; i++)
        printf("%s %.1f\n", list[i]->name, list[i]->area(list[i]));  /* circle 3.5 / square 4.0 */
    return 0;
}
```

`counter_init` 这类 `init` 函数就是构造函数的替代品，但它不会自动被调用，忘记调用就会用到未初始化的结构体；`free` 之后指针也不会自动置空，这些在 C++/Rust 里由语言保证的东西在 C 里全靠纪律。函数指针表的做法是 GLib、CPython（`PyTypeObject`）等库的通用模式：结构体里放一组函数指针，调用方通过 `obj->methods->foo(obj, ...)` 派发。需要注意函数指针表必须由创建者填好，而且它只是数据，编译器无法检查你是否漏填某个槽位。C 也没有重载：同一个名字只能有一个函数，想区分类型只能换名字（`int_add`、`float_add`），或者用 C11 的 `_Generic` 做编译期分派。命名前缀（`counter_`、`str_`）实际上取代了命名空间与方法归属。

📘 [cppreference · C 结构体](https://en.cppreference.com/w/c/language/struct)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 里没有"属于某个类型的函数"这种概念：函数是全局的对象，方法（method）只是给同一个函数名增加一个参数类型签名。`f(x::T) = ...` 定义的不是新函数而是 `f` 的一个方法，调用时按所有实参的运行时类型选择最具体的方法，这就是多分派（multiple dispatch）。方法定义属于运行时行为——类型一旦被更具体的方法覆盖，之后所有调用都会走新方法。

```julia
# 版本基线：Julia 1.13
abstract type Shape end
struct Circle <: Shape; r::Float64; end
struct Square <: Shape; a::Float64; end

area(s::Circle) = pi * s.r^2                 # 给全局函数 area 加方法
area(s::Square) = s.a^2
area(s::Shape)  = error("未实现")             # 抽象类型上的兜底方法

struct Named{T<:Shape}; inner::T; name::String; end
area(n::Named) = area(n.inner)                # 可以复用底层类型的方法

println(area(Circle(1.0)))     # 3.141592653589793
println(area(Square(2.0)))     # 4.0
println(area(Named(Square(3.0), "s")))  # 9.0

println(methods(area))         # 列出 area 的全部方法
println(which(area, (Circle,)))  # 具体选了哪个方法

# 类型构造器本身就是方法：Circle(1.0) 调的是 Circle 的构造方法
f(x::Int, y::Int) = x + y
println(hasmethod(f, Tuple{Int,Int}))   # true
println(hasmethod(f, Tuple{Float64,Float64}))  # false
```

`methods(f)`、`hasmethod`、`which` 这套自省 API 是 Julia 特有资产：方法的集合是运行时可查的数据。歧义（ambiguity）是多分派必须付的代价——如果有 `f(x::Int, y::Any)` 与 `f(x::Any, y::Int)` 两个方法，调用 `f(1, 1)` 时两者都不比对方更具体，Julia 会抛 `MethodError` 并提示 ambiguous，必须在类型交集处补一个 `f(x::Int, y::Int)`。`abstract type` 上的方法提供默认行为，与 OO 的"接口默认实现"思路一致但机制不同：它同样只是一个方法。Julia 没有 `this`，也没有 `obj.method()` 的特殊绑定——`obj.f(args)` 只是 `f(obj, args)` 的语法（点号调用会自动把 obj 作为第一个参数）。

📘 [Julia · 方法](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的实例方法写在类体里，接收者是隐式的 `this`；方法默认**非虚**，允许重写必须显式写 `virtual`（或 `abstract`/`override`），这与 Java 的默认相反。C# 14 引入了 `extension` 块，把扩展方法升级为扩展成员：同一个块里可以声明方法、属性、运算符和静态扩展成员，接收者在 `extension(接收者类型 名字)` 里声明一次，块内所有成员共享。旧式 `this` 参数写法仍然有效，两种形式生成的 IL 完全一致。

```csharp
// 版本基线：C# 14 / .NET 10
public static class NumericSequences
{
    // C# 14 的 extension 块：一次性声明接收者，块内方法/属性/运算符都在其作用域
    extension(IEnumerable<int> sequence)
    {
        public IEnumerable<int> AddValue(int operand)     // 实例扩展方法
        {
            foreach (var item in sequence) yield return item + operand;
        }

        public int Median                                  // 扩展属性（C# 14 新增）
        {
            get
            {
                var sorted = sequence.OrderBy(n => n).ToList();
                int mid = sorted.Count / 2;
                return sorted.Count % 2 == 0
                    ? (sorted[mid - 1] + sorted[mid]) / 2
                    : sorted[mid];
            }
        }

        public static IEnumerable<int> Identity => Enumerable.Empty<int>();   // 静态扩展成员
        public static IEnumerable<int> operator +(IEnumerable<int> left, IEnumerable<int> right)
            => left.Concat(right);                          // 扩展运算符
    }
}

public static class LegacyExtensions
{
    public static IEnumerable<int> AddValue(this IEnumerable<int> sequence, int operand)  // 旧写法
        => sequence.Select(x => x + operand);
}

class Base
{
    public virtual string Who() => "Base";        // 必须 virtual 才能重写
    public string Sealed() => "sealed";           // 默认非虚
}
class Sub : Base
{
    public override string Who() => "Sub";        // override 必需
}
```

`extension` 块不引入新的作用域，同一个类里所有成员（含多个扩展块）的签名必须唯一；生成的签名里带着接收者信息——静态扩展成员把接收者类型编进方法名，实例扩展成员则把它作为第一个参数。扩展成员在编译期解析、本质是静态方法调用，所以不能访问私有成员、不能参与虚派发；把接收者变量换成基类静态类型就选不到更具体的扩展。C# 14 的扩展块支持泛型接收者（`extension<T>(IEnumerable<T> source)`），类型参数用在接收者上就写在 `extension` 后，只用在成员上就写在成员上，两处不能重复。扩展索引器是 C# 15 的特性，C# 14 里不能写在扩展块中。重载在 C# 里很常见，`override` 必须与基类签名完全匹配（协变返回类型自 C# 9 起允许）。

📘 [MS Learn · extension 声明](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/extension)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的实例方法写在类体里，接收者是隐式的 `this`；类成员默认可重写，每个类同时隐含一个接口（implement 时只取签名），所以 Dart 的多态是"隐式接口 + 动态派发"。扩展能力分两层：`extension` 声明（Dart 2.7+）提供编译期静态解析的扩展方法与扩展 getter，`extension type`（Dart 3.3+）提供零成本的类型包装，二者用途不同但都遵循"不改变原类型"的原则。

```dart
// 版本基线：Dart 3.13
class Counter {
  int _n;                                  // 私有字段只在库内可见
  Counter(int n) : _n = n;                 // 构造：参数 n 在初始化列表里赋给私有字段 _n
  int get n => _n;                         // getter
  set n(int v) => _n = v;                  // setter：都是特殊方法
  void inc() => _n++;                      // 实例方法：默认可被 override
  static Counter make(int n) => Counter(n); // 静态方法
  @override String toString() => 'Counter($_n)';   // 隐藏接口里的方法
}

class Named extends Counter {
  final String name;
  Named(super.n, this.name);               // super 参数转发（2.17+）
  @override void inc() { super.inc(); super.inc(); }   // 重写 + super
}

extension CounterX on Counter {            // 扩展：编译期静态解析，不能碰私有成员
  int get twice => n * 2;                  // 扩展 getter
  void add(int k) => n = n + k;            // 扩展里能用公开 setter
}

extension type Meters(double value) {      // extension type（3.3+）：零成本包装
  double get inFeet => value * 3.28084;    // 编译期存在、运行时就是 double
}

void main() {
  final c = Named(1, 'a')..inc();          // 级联：返回接收者
  print('$c ${c.twice}');                  // Counter(3) 6
  print(Meters(1).inFeet);                 // 3.28084
  Counter plain = c;
  print(plain.toString());                 // Counter(3)（动态派发到 Named 继承的 toString）
}
```

`extension` 与 `extension type` 的差别值得单独记住：`extension` 给已有类型加成员，解析在编译期完成并且只对静态类型生效，所以 `Counter` 类型上没声明过 `twice` 的变量调不到它；`extension type` 则是在编译期把包装类型当作新类型、运行时擦除为被包装类型（representation type），适合给"裸 `double`"加上单位语义而不付运行时开销，它还能实现接口、声明成员。`super` 参数转发让子类构造器不必手写全部参数，但只能在构造器参数列表里用。Dart 的字段访问会被编译成 getter/setter 调用，所以 `n = v` 与 `set n` 是同一件事；`@override` 只是给编译器与读者的标注，漏写不会导致编译失败（但会丢警告）。没有运算符重载之外的"魔术方法"体系——`operator +` 这类声明是 Dart 里唯一可重载的运算符入口。

📘 [Dart · 扩展方法](https://dart.dev/language/extension-methods)

{{% /tab %}}

{{% tab header="R" %}}

R 有四套并存的方法系统。S3 最常用也最松散：定义一个泛型函数 `f`，函数体里调 `UseMethod("f")`，R 再按第一个参数的 `class` 属性去找 `f.类名`。S4 用 `setGeneric`/`setMethod` 做正式的多参数分派，带签名检查。R5（Reference Classes）与 R6 是"引用语义的对象系统"，方法挂在对象上而不是全局泛型函数上。R 的方法解析完全是运行时的，方法查找靠命名约定与注册表。

```r
# 版本基线：R 4.6
area <- function(x, ...) UseMethod("area")     # S3 泛型：只按第一个参数分派
area.default <- function(x, ...) stop("没有 area 方法")
area.circle <- function(x, ...) pi * x$r^2     # 方法名 = 泛型名 + 类名
area.square <- function(x, ...) x$a^2

circle <- function(r) structure(list(r = r), class = "circle")   # 用 class 属性打标
square <- function(a) structure(list(a = a), class = "square")

cat(area(circle(1)), "\n")        # 3.141593
cat(area(square(2)), "\n")        # 4
print(methods("area"))             # 列出 area.default / area.circle / area.square

# S4：正式的多参数分派与签名检查
setClass("Point", representation(x = "numeric", y = "numeric"))
setGeneric("shift", function(object, dx) standardGeneric("shift"))
setMethod("shift", signature(object = "Point", dx = "numeric"),
          function(object, dx) new("Point", x = object@x + dx, y = object@y))
p <- shift(new("Point", x = 1, y = 2), 3)
cat(p@x, "\n")                     # 4
cat(isGeneric("shift"), "\n")      # TRUE
```

S3 分派只看第一个参数，`area.default` 是不匹配时的兜底，忘了写它就会报"no applicable method"；方法名必须是 `泛型名.类名`，中间的点不能省。类属性是向量，`UseMethod` 会沿 `class(x)` 的顺序逐个找，因此多重继承在 S3 里表现为"类向量"。S4 的方法选择用签名（signature）描述，支持多参数联合分派，还提供 `isGeneric`、`selectMethod`、`showMethods` 等自省函数，代价是建类与注册泛型更啰嗦。R5/R6 是另一条路线：对象里存环境，方法通过 `$` 访问，更接近 Java 的对象模型，`R6` 包的 `private`/`public` 分节是常见选择。R 的 `Ops` 组泛型（`+.circle`）就是运算符重载，`groupGeneric` 声明它会一次性覆盖 `+`、`-`、`*`、`/` 等一组成员。

📘 [R · S3 方法](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatch)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有方法：没有类、没有 `impl`、没有隐式接收者，只有结构体（或 `union`、`enum`）与自由函数。给结构体写操作的方式是把 `self` 显式写成第一个参数写在结构体命名空间（`const T = struct { ... }` 内部的 `pub fn`）里，调用时 `x.f(y)` 会被编译器展开成 `T.f(x, y)`——点号调用只是语法糖。Zig 也没有重载，所有函数名必须唯一，派发全部在编译期完成。

```zig
// 版本基线：Zig 0.15
const std = @import("std");

const Counter = struct {
    n: i32 = 0,

    pub fn init(n: i32) Counter {          // 没有构造函数语法，惯例用 init
        return .{ .n = n };
    }
    pub fn inc(self: *Counter) void {      // 首参是 self 指针
        self.n += 1;
    }
    pub fn get(self: Counter) i32 {        // 值 self：拿到副本
        return self.n;
    }
    pub fn add(a: Counter, b: Counter) Counter {   // 静态风格的"类型方法"
        return .{ .n = a.n + b.n };
    }
    pub fn format(self: Counter, writer: *std.Io.Writer) std.Io.Writer.Error!void {
        try writer.print("Counter({d})", .{self.n});
    }
};

pub fn main() !void {
    var c = Counter.init(1);
    c.inc();                               // 等价于 Counter.inc(&c)
    std.debug.print("{d}\n", .{c.get()});   // 2
    std.debug.print("{d}\n", .{Counter.add(c, Counter.init(3)).n});  // 5
    std.debug.print("{f}\n", .{c});         // Counter(2)（{f} 调用自定义 format 方法）
    std.debug.print("{d}\n", .{Counter.get(c)});   // 2  也可以完全写成函数调用
}
```

真正要建立的心智模型是"名字空间 + 首参"：`Counter` 是一个类型也是一个名字空间，`pub fn` 只是把函数挂在这个名字空间下，`c.inc()` 与 `Counter.inc(&c)` 生成的机器码相同。因此没有虚表、没有运行期派发，想要多态只能用编译期的 `comptime`、泛型参数或 `anytype`，运行期多态要靠 tagged union 加 `switch` 手工实现。`{f}` 这样的格式说明符会让 `std.fmt` 调用该类型的 `format` 方法（Zig 0.15 起方法名与签名固定为 `fn format(self, writer: *std.Io.Writer)`，`{}` 遇到带 `format` 方法的类型会直接报 ambiguous 编译错误），这是 Zig 里"特殊方法"的唯一形态。Zig 0.15 的 `std.ArrayList` 已是非托管版本（不再存 allocator），把它当字段时要把 allocator 一起传进去，这是从旧版本迁移时最容易踩的坑。没有继承也就没有"重写"，同名函数在不同类型上互不影响。

📘 [Zig · 语言参考（结构体与命名空间）](https://ziglang.org/documentation/master/#struct)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有类与方法，只有表（table）、函数和一点语法糖。`function obj:m(a)` 等价于 `function obj.m(self, a)`，冒号只是自动补一个名为 `self` 的首参；`obj:m(a)` 是 `obj.m(obj, a)` 的缩写。类、继承、方法解析全靠元表（metatable）的 `__index` 链手工搭。Lua 5.5 把 `global` 列为保留字，写类的时候不要拿它当变量名。

```lua
-- 版本基线：Lua 5.5
local Counter = {}
Counter.__index = Counter                      -- 实例查不到就去 Counter 里找

function Counter.new(n)                        -- 构造函数：惯例叫 new
  local self = setmetatable({}, Counter)        -- 单表继承的经典写法
  self.n = n or 0
  return self
end

function Counter:inc()                         -- 冒号：self 是第一个参数
  self.n = self.n + 1
  return self
end

function Counter:get() return self.n end
function Counter.__tostring(self) return "Counter(" .. self.n .. ")" end   -- 元方法
function Counter.__add(a, b) return Counter.new(a.n + b.n) end             -- 运算符重载

local c = Counter.new(1):inc()                 -- 链式调用
print(tostring(c), c:get())                    -- Counter(2) 2
print(tostring(c + Counter.new(3)))            -- Counter(5)

-- 冒号与点号混用是头号错误：Counter:inc(c) 会把类表当成 self
local ok, err = pcall(function() return Counter:inc(c) end)
print(ok, err)                                 -- false  attempt to perform arithmetic on a nil value (field 'n')

-- 子类：把父类放进 __index 链
local Named = setmetatable({}, { __index = Counter })
Named.__index = Named
function Named.new(n, name)
  local self = Counter.new(n)
  self.name = name
  return setmetatable(self, Named)
end
function Named:label() return self.name .. "=" .. self:get() end
print(Named.new(1, "a"):inc():label())          -- a=2
```

`Counter:inc(c)` 这种写法把类表 `Counter` 当成了 `self`（等价于 `Counter.inc(Counter, c)`），于是 `self.n` 是 nil，做加法时报 nil 运算错误；反过来写成 `c.inc()` 又会以 nil 为 `self`。这类错误只在运行时暴露，规模大了很难追。运算符重载全部通过元方法完成：`__add`、`__sub`、`__mul`、`__div`、`__mod`、`__pow`、`__unm`、`__concat`、`__len`、`__eq`、`__lt`、`__le`、`__index`、`__newindex`、`__call`、`__tostring`、`__gc`、`__close`，名字必须精确匹配，写错不会报错、只会静默不生效。`__index` 既可以是表（查表）也可以是函数（动态计算），这就是 Lua 实现"继承"与"默认值"的同一把钥匙。方法只是表里的函数值，因此**谁都能替换**，写库时要意识到调用方可以随时改掉你的方法。

📘 [Lua 5.5 · 元表与元方法](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的方法与 JavaScript 完全同构：类成员写在类体里，通过原型在运行时查找，`this` 由调用点决定。TypeScript 追加的只是**类型层面**的检查，包括显式的 `this` 参数、`implements` 检查、`override` 关键字、访问修饰符。扩展能力靠声明合并（declaration merging）给已有接口或模块补签名，但编译器不会因此生成任何代码。

```typescript
// 版本基线：TypeScript 7（Go 重写的原生编译器）
class Counter {
  #n: number;                                  // 私有字段：真正的运行时隔离
  constructor(n: number) { this.#n = n; }
  inc(this: Counter): this {                    // 显式 this 参数：绑定检查在编译期
    this.#n++;
    return this;
  }
  get n(): number { return this.#n; }
  static make(n: number): Counter { return new Counter(n); }
  toString(): string { return `Counter(${this.#n})`; }
}

class Named extends Counter {
  constructor(public name: string, n: number) {   // 参数属性：自动声明并赋值字段
    super(n);
  }
  override toString(): string { return `${this.name}:${super.toString()}`; }
}

const c = Named.make(1);                       // 静态方法也能继承
console.log(String(c.inc()));                  // Counter(2) ← Named 没重写 inc

const loose = c.inc;                           // 摘下来后 this 类型不匹配
try { loose(); } catch (e) { console.log('🛑', (e as Error).constructor.name); }  // 🛑 TypeError

interface Counter {                            // 声明合并：给类补类型签名
  twice(): number;
}
Counter.prototype.twice = function (this: Counter) { return this.n * 2; };  // 补实现
console.log(c.twice());                        // 4

declare module './m' {                         // 模块增强：给第三方模块补类型
  interface Options { extra?: boolean }
}
```

类型层面的方法解析是**结构化**的：只要对象有 `inc(): this` 这样的成员，它就满足相应接口，不需要显式 `implements`，也不需要继承关系。这与 Java 的标称类型正好相反，好处是跨库组合容易，代价是"看着能调、实际调不到"——`declare module` 补的签名如果没有对应的运行时实现，编译通过但运行时报 `undefined`。`this` 参数（`inc(this: Counter)`）是 TypeScript 特有的编译期约束：把方法摘下来赋给变量时，调用点不再满足 `this` 约束，编译器会直接报错——这是它比 JavaScript 更安全的地方。改内建原型（`Array.prototype.xxx = ...`）在类型与运行时都能生效，但会污染所有代码并可能与未来标准冲突，工程上应避免。

📘 [TypeScript · 类](https://www.typescriptlang.org/docs/handbook/2/classes.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 里没有"方法"这个独立概念，只有函数值与调用时确定的 `this`：`obj.m()` 会以 `obj` 为 `this` 调用函数，`const f = obj.m; f()` 则以 `undefined`（严格模式/模块）为 `this`。`class` 语法把构造函数、原型方法与静态方法放在一处书写，方法解析沿原型链进行。箭头函数没有自己的 `this`，它捕获定义处的词法 `this`，因此常被当作"自动绑定"的手段。

```javascript
// /tmp/verify/methods.js（node 24.20.0 实测；文档按 Node 26 写）
class Counter {
  #n = 0;
  constructor(n) { this.#n = n; }              // constructor 是特殊方法，不能当函数调
  inc() { this.#n++; return this; }             // 原型方法：默认动态派发
  get n() { return this.#n; }                   // getter
  static make(n) { return new Counter(n); }      // 静态方法挂在构造函数上
  toString() { return `Counter(${this.#n})`; }   // 字符串化钩子
}
const c = Counter.make(1);
c.inc();
console.log(String(c), c.n);                    // Counter(2) 2

const loose = c.inc;                            // 摘下来就丢了 this
try { loose(); } catch (e) { console.log('🛑 ' + e.constructor.name); }  // 🛑 TypeError
c.inc.bind(c)();                                 // bind 固定 this
console.log(c.n);                                // 3

class Sub extends Counter {
  inc() { super.inc(); return this; }             // super 沿原型链找父类方法
  toString() { return 'Sub' + super.toString(); }
}
console.log(String(Sub.make(0).inc().inc()));     // Counter(2)：make 里硬编码 new Counter，返回的不是 Sub
console.log(Object.getPrototypeOf(Sub.prototype) === Counter.prototype);  // true

Counter.prototype.double = function () { return this.n * 2; };   // 原型扩展
console.log(c.double());                          // 6
```

`this` 不是"对象自己"，而是"调用表达式左边那个东西"：同一函数可以用不同 `this` 调用，也可以用 `call`/`apply`/`bind` 强行指定。三种常见补救是 `bind`、类字段箭头函数（`inc = () => { ... }`，每个实例一份函数）、以及把逻辑写成普通函数再用参数传对象。原型链是所有方法解析的唯一路径，`super` 使用定义时绑定的原型（不是调用者的），所以在子类里写 `super.toString()` 一定能拿到父类版本，即使实例上又覆盖了一次。给原型加方法（monkey patching）在运行时可行且立即对所有实例生效，但修改内建原型（`Array.prototype`、`Object.prototype`）会污染所有代码、破坏 `for...in`、也可能与未来标准方法撞名，不要做。`class` 体内的方法默认不可枚举，这一点与手工写 `Counter.prototype.inc =` 不同。

📘 [MDN · 方法与 this](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Functions/Method_definitions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的实例方法写在类体里，接收者是隐式的 `$this`；`static` 方法没有 `$this`。对象语义是引用语义（对象靠句柄传递，赋值不会复制），方法解析在运行时按类层次进行，父类方法用 `parent::` 显式调用。PHP 没有运算符重载，但 8.4 起属性可以有 `get`/`set` 钩子（property hooks），把 getter/setter 的样板代码直接内联到属性声明里。

```php
// 版本基线：PHP 8.5
class Counter
{
    public int $count = 0;

    public function __construct(private int $n) {}      // 构造器属性提升
    public function inc(): static { $this->n++; return $this; }   // static 返回类型 = 后期静态绑定
    public function get(): int { return $this->n; }
    public static function make(int $n): static { return new static($n); }
    public function __toString(): string { return "Counter({$this->n})"; }
}

final class Positive extends Counter
{
    public function __construct(int $n)
    {
        if ($n < 0) throw new InvalidArgumentException('negative');
        parent::__construct($n);                        // 父类构造要显式调
    }
}

// PHP 8.4 的属性钩子：虚拟属性，没有存储空间
class Rectangle
{
    public int $area {
        get => $this->h * $this->w;                     // 短写法 get
    }
    public function __construct(public int $h, public int $w) {}
}

$c = Positive::make(1)->inc();
echo $c, ' ', $c->get(), PHP_EOL;                        // Counter(2) 2
$r = new Rectangle(4, 5);
echo $r->area, PHP_EOL;                                  // 20
// $r->area = 30;                                        // 🛑 Error：虚拟属性没定义 set
```

`$this` 只存在于实例方法中，在 `static` 方法里使用会直接报致命错误；类内调用同名方法时 `$this->m()` 是动态派发，`self::m()` 是静态解析到当前类，`static::m()` 是后期静态绑定（late static binding）——三者语义不同，工厂方法里通常要用 `new static(...)` 才能让子类返回子类实例。属性钩子是 8.4 的新工具：`get` 只有一个表达式时可以写 `get => 表达式;`，`set` 可以省略参数名而用隐含的 `$value`；只要钩子里引用了属性本身（`$this->area`）就是"有后备存储"的 backed property，完全没引用则是虚拟属性，此时缺哪个钩子哪个操作就不存在。钩子与 `readonly` 属性不兼容，需要限制写权限请改用非对称可见性（`public private(set)`）。魔术方法（`__get`、`__set`、`__call`、`__callStatic`、`__toString`、`__invoke`、`__destruct`）依然是"特殊方法"的主力，名字拼错不会报错，只会静默不生效。

📘 [PHP · 属性钩子](https://www.php.net/manual/en/language.oop5.property-hooks.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 里一切都是对象，方法定义在类或模块里，接收者默认是 `self`；`def self.name` 定义类方法（本质是单例方法）。方法查找沿祖先链（ancestors）向上，找不到就调 `method_missing`，这是 Ruby 元编程的核心钩子。运算符就是方法（`+`、`[]`、`<<`、`==` 都能定义），`Method` 与 `UnboundMethod` 对象让方法本身可以当值传来传去。

```ruby
# /tmp/verify/methods.rb（ruby 4.0.6 实测）
class Counter
  attr_reader :n
  def initialize(n) = @n = n            # 构造钩子；new 负责分配，initialize 负责初始化
  def inc                               # 实例方法：接收者是 self
    @n += 1
    self
  end
  def self.make(n) = new(n)             # 类方法：def self.
  def to_s = "Counter(#{@n})"            # 隐式转换钩子
  def +(other) = Counter.new(@n + other.n)   # 运算符就是方法
  def method_missing(name, *args)       # 找不到方法时兜底
    return "缺失 #{name}" if name.to_s.start_with?("ghost_")
    super
  end
  def respond_to_missing?(name, _priv = false) = name.to_s.start_with?("ghost_") || super
end

c = Counter.make(1).inc
puts c                                   # Counter(2)
puts(c + Counter.new(3))                 # Counter(5)
puts c.ghost_x                           # 缺失 ghost_x
puts c.respond_to?(:ghost_x)             # true
m = c.method(:inc)                       # Method 对象：绑定接收者
puts m.call.n                            # 3
um = Counter.instance_method(:inc)       # UnboundMethod：必须 bind 到实例
puts um.bind(Counter.new(9)).call.n      # 10
```

`method_missing` 是最后一道防线而不是"动态方法"的正规写法，用它做代理或 DSL 时可以，但必须同时定义 `respond_to_missing?`，否则 `respond_to?`、`method`、内省工具都会给出错误答案；能用 `define_method` 动态定义就不要依赖它，因为性能和可调试性都更差。`Method` 是绑定到具体接收者的可调用对象，`UnboundMethod` 只有在 `bind` 之后才能调用，两者是 Ruby 相对 Go 方法值/C++ 成员函数指针更完整的方案。祖先链的修改有三把钥匙：`include`（模块插到类之后）、`prepend`（模块插到类之前，因此模块版本先执行且能用 `super` 调原实现）、`refine`（只在 `using` 的词法作用域内生效，作用域外的方法完全不变）。`refine` 是对猴子补丁的正式替代方案，代价是生效范围有限、跨文件调试更绕。

📘 [Ruby · 类与方法](https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 方法与函数的关系

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的方法只是"第一个参数是 `self` 的关联函数"，两者可以互相调用：`Type::method(&x)` 是 UFCS（universal function call syntax）写法，而 `<Type as Trait>::method(&x)` 是完全限定语法（fully qualified syntax），用于同名方法消歧。Rust 不支持函数重载，但支持为同一类型实现多个 trait 的同名方法；方法值（`let f = Type::method;`）拿到的是可调用的函数项。

```rust
// /tmp/verify/methods.rs（rustc 1.98.1 实测）
trait Area { fn area(&self) -> f64; }
trait Perimeter { fn area(&self) -> f64; }   // 故意与 Area 同名

struct Circle { r: f64 }
impl Circle { fn area(&self) -> f64 { 1.0 } }        // 固有方法也叫 area

impl Area for Circle { fn area(&self) -> f64 { self.r * self.r } }
impl Perimeter for Circle { fn area(&self) -> f64 { 2.0 * self.r } }

fn main() {
    let c = Circle { r: 2.0 };
    println!("{}", c.area());                 // 1.0  固有方法优先
    println!("{}", Circle::area(&c));          // 1.0  UFCS：显式指定固有方法
    println!("{}", <Circle as Area>::area(&c));      // 4.0  完全限定语法选中 Area
    println!("{}", <Circle as Perimeter>::area(&c)); // 4.0  另一个 trait 的实现
    let f: fn(&Circle) -> f64 = Circle::area;   // 方法当函数值传
    println!("{}", f(&c));                      // 1.0
}
```

当固有方法与 trait 方法同名时，`x.area()` 选固有方法，trait 版本必须用完全限定语法才能调到——这是 Rust 里"消歧"的标准手段，泛型代码里尤其常见（`T::default()` 与 `<T as Default>::default()`）。Rust 没有重载，同名不同签名的需求由 trait 承担；反过来，trait 扩展方法是 Rust 给已有类型加行为的主要途径，只要 trait 与类型在同一 crate（或 trait 来自标准库/依赖），`impl MyTrait for Vec<T>` 就能让 `v.my_method()` 生效。扩展方法无法访问类型的私有字段，与 Kotlin/C# 的扩展机制一样受限于可见性。注意 trait 必须在作用域内（`use` 进来）才能调用其方法，否则报"method not found"。

📘 [Rust · 完全限定语法](https://doc.rust-lang.org/reference/expressions/call-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的方法可以像函数一样取出：`let f = instance.method` 得到绑定接收者的闭包，`let g = Type.method` 得到只接收显式参数的函数引用；类型方法同理。Swift 给已有类型加行为不需要额外机制，`extension` 就是语言级的扩展方法入口，还可以用 `extension T: Protocol` 一次性补齐协议一致性，这在标准库里随处可见。

```swift
// /tmp/verify/methods.swift（swiftc 6.4 实测）
struct Counter {
    var n = 0
    func get() -> Int { n }
    func plus(_ k: Int) -> Counter { Counter(n: n + k) }   // 无重载，靠默认参数/泛型
    static func make() -> Counter { Counter() }
}
extension Counter {                                        // 扩展：加方法
    func doubled() -> Int { n * 2 }
    var asString: String { "Counter(\(n))" }                // 扩展计算属性
}
protocol Describable { func describe() -> String }
extension Counter: Describable {                            // 用一种扩展补协议一致性
    func describe() -> String { "n=\(n)" }
}
let c = Counter(n: 2)
let bound = c.doubled          // 方法值：绑定接收者
let unbound = Counter.doubled   // 类型上的函数引用：柯里化成 (Counter) -> () -> Int
print(bound(), unbound(c)())    // 4 4
print(c.describe(), c.asString) // n=2 Counter(2)
```

`instance.method` 与 `Type.method` 的区别类似 Go 的方法值与方法表达式，但 Swift 的 `Type.method` 是柯里化的：`let g = Counter.doubled` 的类型是 `(Counter) -> () -> Int`，要先 `g(c)` 取出闭包再调用（结构体与类都是这样，实例方法本身不把接收者当普通参数）；`instance.method` 则把接收者固定进去。区别在于 Swift 值类型的方法取出后会捕获当时的副本（值语义），类实例的方法取出则捕获引用，之后状态变化仍然可见。`extension` 里可以重载已有方法签名，也可以给协议加默认实现（`extension Protocol { func f() {...} }`），但**协议扩展的方法不参与动态派发**，它们按静态类型选择实现——这是 Swift 最著名的性能与语义陷阱之一，需要覆盖行为时应该把方法写进协议要求里而不是只写在协议扩展里。`mutating` 方法在扩展中同样需要标 `mutating`，且扩展里依然不能添加存储属性。

📘 [Swift · 扩展](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/extensions/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 把"方法与函数的关系"讲得最直白：方法表达式 `T.Method` 就是普通函数（接收者变成第一个参数），方法值 `x.Method` 是绑定了接收者的闭包。Go 没有扩展方法、没有重载、没有继承，给已有类型加行为只能换一个类型或写自由函数。接口是唯一的抽象机制，方法与函数之间的转换不需要任何额外语法。

```go
// /tmp/verify/go/main.go（go 1.27.1 实测）
package main

import "fmt"

type Counter struct{ n int }

func (c Counter) Get() int   { return c.n }      // 值方法
func (c *Counter) Inc()      { c.n++ }           // 指针方法
func (c Counter) Add(k int) Counter { return Counter{c.n + k} }

type Adder interface{ Add(int) Counter }         // 接口用方法签名描述能力

func main() {
	c := Counter{n: 1}
	mv := c.Get          // 方法值：接收者已绑定（值接收者 → 绑定副本）
	me := Counter.Get    // 方法表达式：接收者变成第一个参数
	mp := (*Counter).Inc // 指针方法表达式
	fmt.Println(mv(), me(c))              // 1 1
	mp(&c)
	fmt.Println(c.Get())                  // 2
	c.Inc()
	fmt.Println(c.Get())                  // 3
	// 接口到函数的桥接：把方法值存进 map、slice 或函数字段
	table := map[string]func(){ "inc": c.Inc }   // 指针接收者的方法值绑定的是 &c
	table["inc"]()
	fmt.Println(c.Get())                  // 4（原对象被改到了）
	table2 := map[string]func(){ "inc": (&c).Inc }
	table2["inc"]()
	fmt.Println(c.Get())                  // 5
	var a Adder = c
	fmt.Println(a.Add(10).Get())          // 15（a 仍是 c 的副本）
}
```

`map[string]func(){ "inc": c.Inc }` 这个例子点出了 Go 方法值最容易搞混的地方：指针接收者的方法值绑定的是 `&c`（调用会改到原对象），而值接收者的方法值绑定的是求值那一刻的副本（之后原对象怎么变都看不见）。Go 没有重载，替代手段是可变参数（`...T`）、接口或不同名字的函数；Go 也没有扩展方法，`strings.TrimSpace`、`sort.Slice` 这类自由函数就是它的"扩展"形态，或者定义新类型（`type MySlice []int`）再在其上加方法——新类型与底层类型之间需要显式转换，这既是限制也是隔离。`Adder` 接口可以接收 `Counter` 值，因为值类型提供了 `Add`；如果把 `Add` 改成指针接收者，`var a Adder = c` 就不能编译，必须写 `&c`。

📘 [Go spec · 方法值与方法表达式](https://go.dev/ref/spec#Method_values)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的方法就是函数加一个绑定过程：`obj.m` 触发描述符协议返回 bound method，`Cls.m` 返回普通函数对象，`Cls.__dict__["m"]` 拿到函数本身。因此方法可以当一等对象传来传去，也可以挂到别的类上。Python 没有重载（同名定义只有最后一个生效，签名检查靠类型注解与运行时的 `functools.singledispatch`），重写是普通的名字遮蔽，扩展则靠猴子补丁或混入类。

```python
# /tmp/verify/methods.py（python3 3.14.7 实测）
class Counter:
    def __init__(self, n): self.n = n
    def inc(self): self.n += 1; return self
    def __repr__(self): return f"Counter({self.n})"

c = Counter(0)
bound = c.inc          # 绑定方法对象：已记住 self
print(bound, bound())  # <bound method Counter.inc of Counter(1)> Counter(1)（参数先求值，bound() 已把 n 改成 1）
print(Counter.inc)     # <function Counter.inc at ...> 未绑定，需要显式传 self
print(Counter.inc(c))  # Counter(2)
print(c.inc.__self__ is c, c.inc.__func__ is Counter.inc)   # True True

def shout(self): return f"{self!r}!"
Counter.shout = shout          # 猴子补丁：给类加方法，立即对所有实例生效
print(c.shout())               # Counter(2)!
c.only_here = lambda: "实例字段"    # 这不会绑定 self，纯粹是实例属性
print(c.only_here())           # 实例字段

class Mixin:                   # 混入类：靠 MRO 插入方法
    def twice(self): return self.n * 2
class Combined(Counter, Mixin): pass
print(Combined(3).twice())     # 6
```

`c.shout()` 能工作是因为查找发生在类上，而 `c.only_here()` 能工作是因为实例字典优先——这两者走的是不同路径，理解这一点才能看懂后面 MRO 与 `__getattr__` 的行为。`__self__` 与 `__func__` 让绑定关系可拆解，`MethodType(f, obj)` 可以手工绑定。Python 不支持方法重载：连续定义同名方法只有最后一个存在，需要按类型分派就用 `functools.singledispatch`（按第一个参数类型分派）或 `functools.singledispatchmethod`（在类里按第一个非 self 参数分派）。混入类必须放在继承列表靠前的位置才能覆盖基类实现，因为 MRO 从左到右、从子到父。给类打补丁会同时影响已经存在的实例（因为它们只在类字典里查），这既是威力也是风险；`types.MethodType` 可以给单个实例绑定方法而不污染类。

📘 [Python · 方法对象](https://docs.python.org/3/tutorial/classes.html#method-objects)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的成员函数是一等公民的一部分：`::method` 得到可调用引用（callable reference），`instance::method` 绑定接收者，`Type::method` 留出接收者参数。Kotlin 支持函数重载（按参数列表区分），支持 `override`，支持扩展函数与扩展属性——但扩展在编译期静态解析，本质是静态方法调用。Kotlin 没有方法值的隐式转换，需要显式写 `::` 或 lambda。

```kotlin
class Counter(private var n: Int) {
    fun get(): Int = n
    fun add(k: Int): Counter { n += k; return this }     // 重载：同名不同参数列表
    fun add(k: Int, times: Int): Counter { repeat(times) { n += k }; return this }
    fun describe(): String = "Counter($n)"
}
// 扩展函数：编译成静态函数，接收者是第一个参数
fun Counter.triple(): Int = get() * 3
// 扩展属性：不能有幕后字段
val Counter.label: String get() = "L${get()}"

fun apply(f: (Counter) -> Int, c: Counter) = f(c)

fun main() {
    val c = Counter(1)
    val bound = c::get                 // 绑定接收者的可调用引用
    val unbound = Counter::get          // 未绑定：接收者变成参数
    val addOnce: (Counter, Int) -> Counter = Counter::add        // 重载引用：靠期望类型消歧
    val addMany: (Counter, Int, Int) -> Counter = Counter::add
    println("${bound()} ${unbound(c)}")  // 1 1
    println(addOnce(c, 2).describe())    // Counter(3)
    println(addMany(c, 2, 3).describe()) // Counter(9)
    println(apply(Counter::get, c))      // 9
    println("${c.triple()} ${c.label}")   // 27 L9
    val asFunction: (Counter) -> Int = Counter::get
    println(asFunction(c))              // 9
}
```

可调用引用与扩展函数配合时有个容易忽略的点：`Counter::get` 的类型是 `(Counter) -> Int`，而 `c::get` 是 `() -> Int`；扩展函数也能取引用（`Counter::triple`），此时它就是一个普通函数而非方法。重载与可调用引用一起用时，`Counter::add` 这种写法需要编译器从期望类型推断出选哪一个，否则报"overload resolution ambiguity"。Kotlin 的扩展函数不能覆盖成员函数（成员优先）、也不能被 `override`，扩展本身不是多态入口，需要多态就定义接口与实现类。扩展属性使用最广的场景是给第三方类型加"计算视图"（`val String.lastChar`），注意它每次访问都会执行 getter 代码，没有缓存。

📘 [Kotlin · 函数引用](https://kotlinlang.org/docs/reflection.html#function-references)

{{% /tab %}}

{{% tab header="Java" %}}

Java 没有函数指针，方法不能脱离类存在，但方法引用（`Type::method`、`instance::method`）让方法可以当作函数式接口的实现传递；`Method` 反射对象提供运行时的调用入口，代价是失去静态检查与内联能力。Java 支持方法重载与重写，但扩展方法不存在——给已有类型加行为要写静态工具类，或者用接口的默认方法（只有自己能改的接口才行）。

```java
// 版本基线：Java 26（LTS 25）
import java.util.function.*;
import java.lang.reflect.Method;

class Counter {
    private int n;
    Counter(int n) { this.n = n; }
    int get() { return n; }
    Counter add(int k) { n += k; return this; }        // 重载 1
    Counter add(int k, int times) { for (int i = 0; i < times; i++) n += k; return this; }  // 重载 2
    @Override public String toString() { return "Counter(" + n + ")"; }
    static Counter make(int n) { return new Counter(n); }
}

class Base { String who() { return "Base"; } }
class Sub extends Base { @Override String who() { return "Sub"; } }

public class Main {
    public static void main(String[] args) throws Exception {
        Counter c = Counter.make(1);
        Function<Counter, Integer> f = Counter::get;          // 未绑定引用：接收者变成参数
        IntSupplier bound = c::get;                            // 绑定引用
        BiFunction<Counter, Integer, Counter> add = Counter::add;  // 重载按目标类型消歧
        System.out.println(f.apply(c) + " " + bound.getAsInt());   // 1 1
        System.out.println(add.apply(c, 5));                        // Counter(6)
        Function<Base, String> g = Base::who;                        // 未绑定引用只吃掉接收者这一个参数
        System.out.println(g.apply(new Sub()));                      // Sub（虚派发生效）

        Method m = Counter.class.getDeclaredMethod("get");           // 反射：运行时查找
        System.out.println(m.invoke(c));                             // 6

        // 扩展方法的替代：静态工具类 或 接口默认方法
        System.out.println(Util.twice(c));                           // 12
    }
}
class Util { static int twice(Counter c) { return c.get() * 2; } }
```

方法引用与 lambda 都是函数式接口的实例，`Counter::get` 在目标类型为 `Function<Counter,Integer>` 时是未绑定形式（接收者当参数），在目标类型为 `IntSupplier` 时绑定形式——同一个语法随上下文变化，这是 Java 方法引用最常见的困惑来源。重载选择在编译期完成，`Counter::add` 依赖目标类型消歧，赋给不明确的目标类型会编译失败。反射调用能绕过访问控制（`setAccessible(true)`），但从 Java 9 模块系统起对 JDK 内部类会受限，且 `invoke` 有装箱与调用开销；能静态引用就不要用反射。接口默认方法（`default`）是 Java 8 引入的"受控扩展"：接口作者可以不破坏实现类地新增方法，但实现类一旦自己有同名方法就优先，而且多个接口默认方法冲突时必须显式 `Interface.super.m()`。

📘 [JLS · 方法调用表达式](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.12)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的成员函数指针（pointer to member function）是"方法与函数关系"最复杂的形态：`&T::m` 的类型是 `Ret (T::*)(Args)`，必须配合对象才能调用（`(obj.*pm)(...)` 或 `(ptr->*pm)(...)`）。C++ 允许成员函数重载，`static_cast` 到目标签名可以消歧；成员函数也可以取地址得到类似函数指针的东西，但 `this` 是隐式参数，所以类型不同。C++ 没有扩展方法，替代方案是自由函数重载运算符、ADL 查找、或者继承。

```cpp
// 版本基线：C++23
#include <iostream>
#include <string>
#include <functional>
#include <vector>

struct Counter {
    int n = 0;
    int get() const { return n; }
    int add(int k) { n += k; return n; }        // 重载 1
    int add(int k, int times) { for (int i = 0; i < times; ++i) n += k; return n; }  // 重载 2
    static int twice(int x) { return x * 2; }    // 静态成员函数：类型是普通函数指针
};

// 自由函数扩展 + ADL：不修改 Counter 也能加行为
namespace ext { std::string label(const Counter& c) { return "L" + std::to_string(c.get()); } }

int main() {
    Counter c{1};
    int (Counter::*pm)(int) = &Counter::add;               // 成员函数指针（重载按签名选）
    int (Counter::*pg)() const = &Counter::get;
    std::cout << (c.*pm)(5) << ' ' << (c.*pg)() << '\n';    // 6 6
    int (*pf)(int) = &Counter::twice;                        // 静态成员：普通函数指针
    std::cout << pf(4) << '\n';                              // 8

    auto bound = std::bind(pm, &c, std::placeholders::_1);   // 绑定接收者
    std::cout << bound(1) << '\n';                             // 7
    auto lam = [&c, pm](int k) { return (c.*pm)(k); };           // lambda 捕获对象与成员指针
    std::cout << lam(0) << '\n';                                // 7

    std::vector<Counter> v{{1}, {2}};
    for (auto& x : v) std::cout << (x.*pg)() << ' ';            // 1 2
    std::cout << '\n' << ext::label(c) << '\n';                  // L7
}
```

成员函数指针必须区分"成员"与"静态"：静态成员函数的地址是普通函数指针，可以直接赋给 `int(*)(int)`；非静态成员函数需要对象参与，`.*` 与 `->*` 两个运算符是专门为它准备的，优先级低、需要括号。虚成员函数指针调用依然走 vtable，因此多态不丢。`std::bind` 与 lambda 都能固定接收者，实践中 lambda 更清晰也更容易被内联。C++ 没有扩展方法，替代路径是：给类型加成员（要能改源码）、写自由函数（`ext::label(c)`，靠 ADL 或命名空间组织）、或写运算符重载让语法自然。`std::function` 会带来类型擦除开销（堆分配 + 间接调用），性能敏感处应使用模板参数或函数指针。

📘 [cppreference · 成员函数指针](https://en.cppreference.com/w/cpp/language/pointer#Pointers_to_member_functions)

{{% /tab %}}

{{% tab header="C" %}}

C 里函数就是函数，没有方法也没有成员函数指针（严格说成员函数指针是 C++ 概念）。要在 C 里表达"按名字找实现"，只能靠函数指针数组或 `switch`；要扩展一个结构体的行为，就在同一个编译单元里加 `prefix_` 开头的函数，或者把函数指针放进结构体让调用方替换。C 不支持重载，同名函数只能有一个。

```c
/* /tmp/verify/spec.c（Apple clang 21, -std=c23 实测） */
#include <stdio.h>
#include <string.h>

typedef struct { int n; } Counter;

static int counter_get(const Counter *self) { return self->n; }
static int counter_add(Counter *self, int k) { self->n += k; return self->n; }

/* 用函数指针表模拟"扩展方法/虚方法" */
typedef struct CounterOps CounterOps;
struct CounterOps {
    int  (*get)(const Counter *);
    int  (*add)(Counter *, int);
};
static const CounterOps OPS = { counter_get, counter_add };

/* C11 _Generic：编译期按类型选函数，是重载的最近似替代 */
#define show(x) _Generic((x), int: show_int, double: show_double, char *: show_str)(x)
static void show_int(int v) { printf("int %d\n", v); }
static void show_double(double v) { printf("double %g\n", v); }
static void show_str(char *v) { printf("str %s\n", v); }

/* 函数指针可以当参数传，等价于"把方法交出去" */
static void each(Counter *c, int (*f)(Counter *, int)) { f(c, 1); }

int main(void) {
    Counter c = { .n = 1 };
    printf("%d\n", OPS.add(&c, 5));         /* 6 */
    printf("%d\n", OPS.get(&c));            /* 6 */
    each(&c, counter_add);
    printf("%d\n", c.n);                    /* 7 */
    show(1); show(1.5); show("x");          /* int 1 / double 1.5 / str x */
    return 0;
}
```

函数指针是 C 表达"行为可替换"的唯一手段：结构体里放 `ops` 表（GLib 的 `GObjectClass`、CPython 的 `PyTypeObject` 都是这个模式）、把函数指针当回调参数、或者用宏在编译期选实现。`_Generic`（C11）能在编译期按表达式类型选择函数，但它只是宏展开，不支持多参数联合分派，也不支持用户自定义类型以外的匹配规则（写宏要覆盖所有情形，否则展开失败）。C 没有名字修饰与命名空间，所以库必须用前缀避免冲突（`counter_get`、`gtk_widget_show`），这也是"方法归属"在 C 里的实际呈现。结构体里的函数指针会占空间且需要初始化，漏填就是空指针调用；用 `const` 表并把表定义成 `static` 可以避免每个实例都存一份。

📘 [cppreference · 函数指针](https://en.cppreference.com/w/c/language/pointer#Pointers_to_functions)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 里"方法"与"函数"的关系是全局的：`f` 是一个泛型函数对象，`methods(f)` 列出它的全部方法，`f(x) = ...` 只是追加一个方法。因此给已有函数添加方法（哪怕函数来自别的包）是常态而不是 hack，`Base.push!` 之类的函数可以被任意包扩展——只要参数类型属于你的包（"类型盗版"是社区禁忌）。Julia 没有重载这个概念，因为它就是多方法本身。

```julia
# 版本基线：Julia 1.13
struct Counter; n::Int; end                      # struct 自动生成默认构造器 Counter(n::Int)
Base.get(c::Counter) = c.n                       # 扩展 Base 的函数必须写限定名（或先 import）
add(c::Counter, k::Int) = Counter(c.n + k)       # 普通两参函数
add(c::Counter, k::Int, times::Int) = Counter(c.n + k * times)   # 另一签名 = "重载"

Base.show(io::IO, c::Counter) = print(io, "Counter(", c.n, ")")   # 扩展 Base.show
Base.:+(a::Counter, b::Counter) = Counter(a.n + b.n)             # 扩展运算符
Base.:(==)(a::Counter, b::Counter) = a.n == b.n                  # 扩展 ==（还要自定义 hash）

println(Counter(1))                  # Counter(1)
println(get(Counter(1)))             # 1
println(add(Counter(1), 5))          # Counter(6)
println(add(Counter(1), 5, 3))       # Counter(16)
println(Counter(1) + Counter(2))     # Counter(3)
println(length(methods(add)))        # 2
println(Counter(1) == Counter(1))    # true

f = get                               # 函数本身是一等值
println(f(Counter(9)))                # 9
println(add)                          # add (generic function with 2 methods)
```

"函数名是全局的、方法属于函数"带来了几个直接后果：给 `Base.show` 加方法就能让 `println` 打印自定义类型，给 `Base.:+` 加方法就能让 `+` 支持新类型，这些都是普通的方法定义而非特殊语法；同名函数只能有一个泛型函数对象，两个包各自定义 `f` 却不相遇（会各自有独立的方法表，调用时按导入的是哪一个）；要"扩展"别人的函数必须先 `import Base: show` 或写 `Base.show`。`Base.:(==)` 是运算符方法名的写法，括号是必需的（否则 `==` 会被解析成比较表达式）。自定义 `==` 时要一起定义 `hash`，否则放进 `Dict`/`Set` 会违反哈希契约。注意 `methods(add)` 只统计当前可见的方法，预编译别的包可能带进更多方法。

📘 [Julia · 方法](https://docs.julialang.org/en/v1/manual/methods/#Method-definitions)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的方法可以变成委托：`MethodName` 直接转成 `Action`/`Func`，实例方法转成委托会固定接收者；`Delegate.CreateDelegate` 与反射的 `MethodInfo.Invoke` 提供运行时入口。C# 支持重载与重写；扩展能力在 C# 14 之前只有 `this` 参数形式的扩展方法，C# 14 增加了 `extension` 块，让扩展属性、扩展运算符、静态扩展成员成为可能，但本质仍是静态方法调用。

```csharp
// 版本基线：C# 14 / .NET 10
using System.Reflection;

public class Counter
{
    public int N { get; private set; }
    public Counter(int n) => N = n;
    public int Get() => N;
    public Counter Add(int k) { N += k; return this; }               // 重载 1
    public Counter Add(int k, int times) { N += k * times; return this; }  // 重载 2
    public override string ToString() => $"Counter({N})";
}

public static class Ext
{
    extension(Counter c)                       // C# 14 扩展块
    {
        public int Twice => c.Get() * 2;        // 扩展属性
        public string Label => $"L{c.Get()}";    // 另一个扩展属性
    }
    public static Counter Make(int n) => new(n);   // 普通静态方法代替工厂
}

public class Program
{
    public static void Main()
    {
        var c = new Counter(1);
        c.Add(5, 2);
        System.Console.WriteLine(c);                 // Counter(11)
        System.Console.WriteLine($"{c.Twice} {c.Label}");   // 22 L11

        Func<int> bound = c.Get;                       // 实例方法转委托：接收者已固定
        Func<Counter, int> unbound = Counter_Get;       // 未绑定形式只能手写静态包装
        System.Console.WriteLine($"{bound()} {unbound(c)}");  // 11 11

        MethodInfo mi = typeof(Counter).GetMethod("Get")!;    // 反射
        System.Console.WriteLine(mi.Invoke(c, null));           // 11
    }
    private static int Counter_Get(Counter c) => c.Get();       // 未绑定形式只能手写
}
```

C# 里实例方法可以直接赋给签名匹配的委托（编译器生成 `ldftn` 加 `newobj`），但**没有** `Type.Method` 这种天然的"未绑定接收者"语法，要拿未绑定形式必须手写静态包装或用表达式树。`Delegate.CreateDelegate` 能在运行时绑定，配合反射可以做插件式调用，代价是失去内联与静态检查。重载解析在编译期完成，方法组（method group）转委托时如果重载有歧义会编译失败。扩展成员在编译期解析、按接收者的静态类型选择，因此 `Counter` 变量调不到为 `object` 定义的扩展；扩展块里声明的成员签名在同一个类内必须唯一。C# 14 之前只有 `this` 参数形式的扩展方法，两种写法生成的 IL 相同，可以混用。

📘 [MS Learn · 扩展方法](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/extension-methods)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的方法与函数关系简单：方法就是带接收者的函数，`Type.method`/`instance.method` 可以取到方法 tear-off（自动转成闭包），不需要显式 `::`。Dart 支持重载吗？不支持——同名方法只能有一个，替代方案是可选参数、命名参数与泛型。重写用 `@override`，扩展方法（2.7+）与扩展类型（3.3+）提供了不改源码加行为的能力。

```dart
// 版本基线：Dart 3.13
class Counter {
  int n;
  Counter(this.n);
  int get() => n;
  Counter add(int k, [int times = 1]) => Counter(n + k * times);  // 可选位置参数代替重载
  @override String toString() => 'Counter($n)';
}
extension CounterX on Counter {
  int get twice => get() * 2;              // 扩展 getter
  Counter labelled() => Counter(get() + 1000);
}
extension type Meters(double value) {      // extension type：编译期包装，运行时就是 double
  double get feet => value * 3.28084;
}

int Function(Counter) pick() => Counter.get;   // 方法 tear-off：未绑定
void main() {
  final c = Counter(1);
  final int Function() bound = c.get;            // 绑定 tear-off
  final int Function(Counter) unbound = Counter.get;
  print('${bound()} ${unbound(c)}');              // 1 1
  print(c.add(2, 3));                              // Counter(7)（add 返回新对象，不改 c）
  print('${c.twice} ${c.labelled()}');             // 2 Counter(1001)（c 仍是最初的 Counter(1)）
  print(Meters(1).feet);                           // 3.28084
  final num raw = Meters(1) as num;                 // extension type 运行时就是 double
  print(raw + 1);                                   // 2.0
  print(pick()(c));                                 // 1
}
```

Dart 的方法 tear-off 由编译器生成闭包，`c.get` 等价于 `() => c.get()`，`Counter.get` 等价于 `(Counter c) => c.get()`——这正是 Go 的方法值与方法表达式。Dart 不支持重载，`add(int)` 与 `add(int, int)` 不能共存，必须用可选参数（`[int times = 1]`）或命名参数（`{int times = 1}`）；可选参数带来"同一个方法承担多种调用形态"的表达力，但也让默认值成为签名的一部分。`extension type`（3.3+）在编译期充当新类型，运行时擦除为被包装类型（representation type），所以 `as num` 能成功；它适合给裸类型加单位或约束语义且零运行时开销。`extension`（2.7+）给已有类型加成员，静态解析、不能访问私有成员、且对 `dynamic` 类型无效。

📘 [Dart · extension type](https://dart.dev/language/extension-types)

{{% /tab %}}

{{% tab header="R" %}}

R 的函数是一等对象，泛型函数靠 `UseMethod`/`standardGeneric` 做运行时派发，所以"给函数加方法"就是注册一个新函数。S3 用命名约定（`f.class`）注册，S4 用 `setMethod` 显式注册；函数本身可以赋值、传参、用 `body()` 与 `formals()` 检查，`do.call` 可以把参数列表喂给任何函数。R 没有重载语法，`...` 与默认参数是常规替代。

```r
# 版本基线：R 4.6
add <- function(x, ...) UseMethod("add")          # 泛型函数
add.default <- function(x, ...) x                  # 兜底方法
add.Counter <- function(x, k = 1, ...) structure(list(n = x$n + k), class = "Counter")
as.Counter <- function(n) structure(list(n = n), class = "Counter")

c <- add(as.Counter(1), 5)
cat(c$n, "\n")                    # 6

# 函数是一等值：可以传、可以检查、可以动态调用
apply_fn <- function(f, x) f(x)                    # 把函数当参数
cat(apply_fn(as.Counter, 3)$n, "\n")               # 3
cat(paste(names(formals(add.default)), collapse = ","), "\n")   # x,...

# 给已有函数"加方法"= 注册新的 f.class
add.Counter2 <- function(x, k = 1, ...) structure(list(n = x$n * k), class = "Counter2")
as.Counter2 <- function(n) structure(list(n = n), class = "Counter2")
cat(add(as.Counter2(2), 3)$n, "\n")                # 6
print(methods("add"))                               # add.Counter / add.Counter2 / add.default

# S4 的替代：正式注册
setGeneric("shift", function(object, dx) standardGeneric("shift"))
setClass("P", representation(x = "numeric"))
setMethod("shift", signature("P", "numeric"),
          function(object, dx) { object@x <- object@x + dx; object })
p <- shift(new("P", x = 1), 2)
cat(p@x, "\n")                                       # 3
```

R 的"扩展"就是注册方法函数，只要泛型函数存在就能加方法，不需要改原代码，这一点与 Julia 相似；区别在于 R 的分派按 `class` 属性（S3）或签名表（S4）在运行时查找，而 Julia 按类型系统。`...` 在 S3 方法签名里几乎是必需项，因为泛型函数会把它原样传给方法；漏写 `...` 常导致"unused argument"错误，这是 R 方法最常见的签名陷阱。`methods("add")` 能列出所有已注册的方法，但只对当前命名空间可见的才列出来。`do.call(f, list(...))` 是运行时构造调用的惯用法，配合 `match.fun`（把名字或函数统一成函数对象）使用。R 里没有真正的重载，参数默认值与 `...` 负责承担"同一函数多种用法"的需求。

📘 [R · 方法分派](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatch)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 完全没有"方法与函数"的区分：所有函数都是自由函数，`x.f(y)` 只是 `T.f(x, y)` 的语法糖，因此方法引用就是普通函数引用，函数指针类型也不需要区分成员与静态。Zig 没有重载（名字必须唯一）、没有动态派发、没有扩展方法；给已有类型加行为的唯一方式是写自由函数，或者用 `usingnamespace` 把一组函数塞进某个命名空间（该功能在新版本中已被弱化，推荐直接显式限定）。

```zig
// 版本基线：Zig 0.15
const std = @import("std");

const Counter = struct {
    n: i32,
    pub fn init(n: i32) Counter { return .{ .n = n }; }
    pub fn get(self: Counter) i32 { return self.n; }
    pub fn add(self: Counter, k: i32) Counter { return .{ .n = self.n + k }; }
    pub fn add2(self: Counter, k: i32, times: i32) Counter {   // 不能重载，只能换名
        return .{ .n = self.n + k * times };
    }
};

fn twice(c: Counter) i32 {                    // 自由函数：与类型无绑定关系
    return c.get() * 2;
}

pub fn main() !void {
    const c = Counter.init(1);
    const f = Counter.get;                     // 函数是一等值：普通函数指针
    var buf: [64]u8 = undefined;
    const s = try std.fmt.bufPrint(&buf, "{d} {d} {d}\n", .{
        f(c),                                  // 1
        c.add(2).get(),                        // 3（语法糖，等价 Counter.add(c, 2)）
        Counter.add2(c, 2, 3).get(),           // 7
    });
    std.debug.print("{s}", .{s});
    std.debug.print("{d}\n", .{twice(c)});      // 2
    const g: *const fn (Counter) i32 = Counter.get;   // 显式函数指针类型
    std.debug.print("{d}\n", .{g(c)});                 // 1
}
```

因为没有隐式 `this`，Zig 的函数指针统一是 `*const fn (T) Ret`，不像 C++ 需要成员函数指针那套 `.*`/`->*` 语法；反过来，Zig 也没有 `std::bind` 那种"固定接收者"的便利，需要手工写一个包装函数或捕获上下文的结构体。方法调用 `c.add(2)` 与 `Counter.add(c, 2)` 由编译器生成相同代码，选择哪种写法纯看可读性；社区惯例是链式调用用点号、需要强调命名空间时用 `Counter.`。想模拟重载必须换名（`add`/`add2`）或者用 `comptime` 参数与泛型函数（`fn add(self: Counter, k: anytype)`），后者能按传入类型在编译期分支，这是 Zig 表达"多态"的主要方式。没有扩展方法意味着不能在别的包里给 `Counter` 添加成员；社区的做法是把自由函数放进自己的模块命名空间，调用时写 `my_ext.twice(c)`。

📘 [Zig · 函数](https://ziglang.org/documentation/master/#Functions)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的"方法与函数"关系是同一张表的两种取用方式：`function t:m()` 只是 `function t.m(self)` 的语法糖，`t.m(t, arg)` 与 `t:m(arg)` 完全等价，`t.m` 拿到的就是普通函数值。因此没有绑定方法对象，`local f = obj.m` 会丢掉 `self`（除非显式传），函数可以被复制、替换、塞进别的表。Lua 没有重载，参数数量不做检查，多了少了自己处理。

```lua
-- 版本基线：Lua 5.5
local Counter = {}
Counter.__index = Counter
function Counter.new(n) local o = setmetatable({}, Counter); o.n = n or 0; return o end
function Counter:get() return self.n end
function Counter:add(k, times)                    -- 没有重载：用可选参数
  times = times or 1
  self.n = self.n + k * times
  return self
end

local c = Counter.new(1)
print(c:get())                       -- 1
print(c:add(2, 3):get())             -- 7
print(Counter.get(c))                -- 7    完全等价的函数调用
local f = Counter.get                -- 取到的是普通函数，没有 self
print(f(c))                          -- 7
local bound = function(k) return c:add(k) end   -- 手工绑定
bound(3)
print(c:get())                       -- 10

-- 把函数当值放进表做分派
local ops = { inc = Counter.add, get = Counter.get }
ops.inc(c, 1)
print(ops.get(c))                    -- 11
print(type(Counter.add), type(c.add))  -- function function
```

`local f = obj.m` 后 `f()` 必然出错（`self` 是 nil），这是 Lua 新手最常见的运行时错误；正确做法是 `local f = obj.m; f(obj)` 或者用 `obj:m()`。因为没有方法绑定对象，Lua 里实现"回调"时通常选择传函数加显式对象参数，而不是传"绑定方法"。可选参数用 `x = x or default` 处理（注意 `false` 会被 `or` 吞掉，需要 `if x == nil then` 才能正确处理布尔假值）。`Counter.add` 与 `c.add` 是同一个函数对象（通过 `__index` 找到），所以给 `Counter.add` 重新赋值会立即影响所有实例，这是 Lua 元表模型的直接体现。运算符重载不是给函数起名，而是给元表的元方法字段赋值（`Counter.__add = function(a, b) ... end`）。

📘 [Lua 5.5 · 函数定义](https://www.lua.org/manual/5.5/manual.html#3.4.11)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的方法在运行时就是原型上的函数，`obj.method` 是普通函数值，`this` 由调用点决定；TypeScript 额外提供了编译期的 `this` 参数，让"方法摘下来后调用"变成编译错误。类型层面支持重载签名（多个 `function f(...)` 声明加一个实现签名，或类里的多个重载签名），但实现只有一个。扩展能力靠声明合并与接口合并，编译器不会生成代码。

```typescript
// 版本基线：TypeScript 7
class Counter {
  constructor(private n: number) {}
  get(): number { return this.n; }
  add(k: number): this;                                            // 重载签名：只有签名没有实现
  add(k: number, times: number): this;                             // 重载签名：只有签名没有实现
  add(k: number, times?: number): this { this.n += k * (times ?? 1); return this; }  // 实现签名
  toString(): string { return `Counter(${this.n})`; }
}
interface Counter { twice(): number }        // 声明合并：给类补类型
Counter.prototype.twice = function (this: Counter) { return this.get() * 2; };

const c = new Counter(1);
c.add(2, 3);
console.log(String(c), c.twice());            // Counter(7) 14
const bound: () => number = c.get.bind(c);      // 运行时绑定
const unbound: (c: Counter) => number = Counter.prototype.get;
console.log(bound(), unbound(c));               // 7 7
const loose = c.get;                             // 类型是 () => number
try { (loose as unknown as () => number).call(undefined); } catch { console.log('🛑 丢 this'); }

// 显式 this 参数：编译期就拦住"摘方法"
class Strict {
  n = 1;
  get(this: Strict): number { return this.n; }
}
const s = new Strict();
const detached = s.get;                          // 类型是 (this: Strict) => number
// detached();                                   // 🛑 编译错误：this 上下文丢失
```

重载在 TypeScript 里是纯类型构造：签名列表供调用方检查，实现签名对外不可见，实现必须能兼容所有重载签名（常用可选参数或联合类型兜底）。方法 tear-off 在类型上保留 `this` 信息，只有带显式 `this` 参数的方法会被编译器拦截；不写 `this` 参数的方法取下来后类型是普通函数，编译不报错但运行时可能崩——两者要按场景选。接口合并（`interface Counter { twice(): number }`）能把新方法并入已有类型，模块增强（`declare module "./m" { ... }`）能补第三方模块，但两者都只改类型：`Counter.prototype.twice = ...` 这行运行时赋值必须自己写，忘了就会 `undefined is not a function`。给内建原型加方法同样可行，但会污染全局并可能与标准冲突，不要做。

📘 [TypeScript · 声明合并](https://www.typescriptlang.org/docs/handbook/declaration-merging.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的函数是一等值，方法只是"以属性形式存放的函数"，取值时不带任何绑定；`obj.method` 得到函数本体，`this` 完全由调用点决定。没有重载（同名属性只有最后赋值生效）、没有静态检查。扩展能力是原型赋值与 `Object.defineProperty`，`Function.prototype.bind` 是唯一的内建绑定手段。ES2022 起类字段箭头函数成为"每实例一份绑定方法"的标准写法。

```javascript
// /tmp/verify/methods.js（node 24.20.0 实测；文档按 Node 26 写）
class Counter {
  n = 0;
  constructor(n) { this.n = n; }
  get() { return this.n; }
  add(k, times = 1) { this.n += k * times; return this; }   // 默认参数代替重载
  inc = () => { this.n += 1; return this; }                  // 类字段箭头函数：自动绑定
}
const c = new Counter(1);
c.add(2, 3);
console.log(c.get());                    // 7
const detached = c.get;
try { detached(); } catch (e) { console.log('🛑 ' + e.constructor.name); }   // 🛑 TypeError
const rebound = detached.bind(c);         // 显式绑定
rebound();
console.log(c.get());                     // 7（get 只读，不改变计数）
const arrow = c.inc;                       // 箭头字段已经绑定，摘下来也能用
arrow();
console.log(c.get());                      // 8

// 原型扩展：等价于给所有实例加方法
Counter.prototype.times = function (k) { return this.n * k; };
console.log(c.times(2));                   // 16
console.log(Object.keys(c));               // [ 'n', 'inc' ] ← 箭头字段是自有属性
console.log(Object.getOwnPropertyNames(Counter.prototype));  // [ 'constructor', 'get', 'add', 'times' ]
```

类字段箭头函数（`inc = () => {...}`）与原型方法有一个常被忽略的差别：前者是**每个实例一份**的自有属性，会出现在 `Object.keys` 里、无法被 `super` 调用、占用更多内存；后者在原型上共享一份，可被 `super` 调用、可被继承与覆盖。React 类组件流行箭头字段是为了免去 bind，但代价就在这里。`bind` 返回一个新函数，`this` 被永久固定，之后再 `call` 也改不掉。`Function.prototype.bind` 只能绑 `this` 和前若干参数（偏函数应用），不能像 C++ 的成员函数指针那样表达"类型上的未绑定方法"——`Counter.prototype.get` 取到的就是普通函数，调用时必须 `fn.call(c)` 或 `fn(c)` 加显式接收者。修改内建原型（`Array.prototype`、`Object.prototype`）会在所有代码里生效，可能破坏 `for...in`、`JSON.stringify` 行为，也可能与未来标准方法撞名，不要做。

📘 [MDN · bind](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的方法与函数关系分两层：类内方法可以当可调用对象（`[$obj, 'method']`、`'Class::staticMethod'`、PHP 8.1 起的一等可调用语法 `$obj->method(...)`）传给 `call_user_func`、`array_map` 或任何接受 `callable` 的地方；运行时还能用 `Closure::fromCallable` 转换。PHP 没有重载（同名方法只能一个，替代是默认参数与 `...$args`），但支持重写；扩展能力靠 trait（水平复用）与 8.4 的属性钩子（在属性声明处挂逻辑）。

```php
// 版本基线：PHP 8.5
class Counter
{
    public function __construct(private int $n) {}
    public function get(): int { return $this->n; }
    public function add(int $k, int ...$extra): static
    {
        $this->n += $k + array_sum($extra);        // 变长参数代替重载
        return $this;
    }
    public static function make(int $n): static { return new static($n); }
    public function __toString(): string { return "Counter({$this->n})"; }
}

trait Twice                                       // trait：水平插入方法
{
    public function twice(): int { return $this->get() * 2; }
}

final class LoudCounter extends Counter
{
    use Twice;                                     // 把 trait 的方法合进来
}

$c = LoudCounter::make(1)->add(2, 3, 4);
echo $c, ' ', $c->twice(), PHP_EOL;                // Counter(10) 20

// 可调用对象：数组 / 字符串 / 一等可调用语法
$cb1 = [$c, 'get'];                                 // 数组形式
$cb2 = 'LoudCounter::make';                          // 静态方法字符串
$cb3 = $c->get(...);                                  // PHP 8.1 一等可调用语法
$cb4 = Closure::fromCallable([$c, 'get']);            // 转成 Closure
echo $cb1(), ' ', ($cb2)(9)->get(), ' ', $cb3(), PHP_EOL;   // 10 9 10
var_dump($cb4 instanceof Closure);                     // bool(true)

// 动态调用与魔术兜底
echo $c->{'ge' . 't'}(), PHP_EOL;                       // 10
class Ghost { public function __call($name, $args) { return "missing $name"; } }
echo (new Ghost())->whatever(), PHP_EOL;                  // missing whatever
```

一等可调用语法 `$obj->method(...)`（8.1+）比 `[$obj, 'method']` 好用的地方在于：它为 IDE 与静态分析提供了类型信息，创建的 `Closure` 与原方法共享作用域（`$this` 与可见性都保留）。`Closure::fromCallable` 与 `Closure::bind` 能把闭包的 `$this` 与作用域换成别的对象或类，这是 Laravel 等框架实现"在外部访问私有成员"的基础，但它是明确的边界突破，业务代码里应慎用。`__call`/`__callStatic` 是找不到方法时的兜底，与 Ruby 的 `method_missing` 定位相同，但 `method_exists` 不会同步感知（`is_callable` 会因为有 `__call` 而返回 true），所以用它写动态 API 时要在文档里写清楚。trait 的方法被合入使用它的类，冲突时用 `insteadof` 与 `as` 解决；trait 不能独立实例化，也不能给"用了它的类"加接口之外的契约。

📘 [PHP · 一等可调用语法](https://www.php.net/manual/en/functions.first_class_callable_syntax.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 把方法对象化得最彻底：`obj.method(:name)` 返回绑定了接收者的 `Method`，`Klass.instance_method(:name)` 返回 `UnboundMethod`（必须 `bind` 之后才能调用），两者都能 `to_proc` 变成块传给 `map`。方法查找沿祖先链，找不到就落到 `method_missing`。Ruby 不支持方法重载（同名方法后者覆盖前者，参数靠默认值与 `*args` 吸收），重写用普通定义加 `super`；扩展有三档：`include`、`prepend`、`refine`。

```ruby
# /tmp/verify/methods.rb（ruby 4.0.6 实测）
class Counter
  attr_reader :n
  def initialize(n) = @n = n
  def inc = (@n += 1; self)
  def add(k, times = 1) = Counter.new(@n + k * times)   # 默认参数代替重载
  def to_s = "Counter(#{@n})"
  def method_missing(name, *args)
    return "缺失 #{name}" if name.to_s.start_with?("ghost_")
    super
  end
  def respond_to_missing?(name, _p = false) = name.to_s.start_with?("ghost_") || super
end

c = Counter.new(1)
m = c.method(:add)                  # Method：绑定接收者，可当一等值
puts m.call(2, 3)                   # Counter(7)
puts [1, 2].map(&:to_s).inspect         # ["1", "2"]：Symbol#to_proc 也是方法引用的一种
um = Counter.instance_method(:add)   # UnboundMethod：必须 bind 到实例
puts um.bind(Counter.new(0)).call(5)  # Counter(5)
puts c.ghost_a                       # 缺失 ghost_a
puts [c, Counter.new(2)].map(&:to_s).inspect   # ["Counter(1)", "Counter(2)"]
```

`Method#to_proc` 让方法能直接当块用（`[c, d].map(&:to_s)` 或 `arr.map(&c.method(:to_s))`），这是 Ruby 相对其他语言最顺手的地方之一；但注意块调用时参数数量必须匹配，`add(k, times = 1)` 一参调用合法，把需要两个参数的方法 `to_proc` 后传给 `map` 会抛 `ArgumentError`。`UnboundMethod#bind` 有类型检查：只能绑到 `kind_of?` 定义类的实例上，绑错类抛 `TypeError`。`method_missing` 的性能开销与调试难度都比 `define_method` 大得多，能用后者就用后者（`define_method` 还能自动更新 `instance_methods`）。三种扩展要分清：`include` 把模块插到类后面（类方法优先）、`prepend` 插到类前面（模块先执行且可 `super`）、`refine` 只在 `using` 的词法作用域内生效。猴子补丁（直接重开 `class String` 并加方法）影响全局，绝不要用于内建类。

📘 [Ruby · Method](https://docs.ruby-lang.org/en/master/Method.html)

{{% /tab %}}

{{< /tabpane >}}

### 方法解析与派发

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有继承，只有两种派发路径：泛型参数（`fn f<S: Shape>(s: &S)`）在编译期为每个具体类型生成一份代码，叫单态化（monomorphization），是静态派发，可内联、零开销；`&dyn Shape` 是 trait object，带一张 vtable 指针，是动态派发，一个函数体服务所有实现类型。方法调用的解析顺序是"固有方法 → trait 方法（按作用域内可见的 trait）→ 自动解引用/取址"。

```rust
// /tmp/verify/dispatch.rs（rustc 1.98.1 实测）
trait Shape { fn area(&self) -> f64; fn name(&self) -> String { "shape".into() } }
struct Circle(f64);
struct Square(f64);
impl Shape for Circle {
    fn area(&self) -> f64 { 3.141592653589793 * self.0 * self.0 }
    fn name(&self) -> String { "circle".into() }
}
impl Shape for Square { fn area(&self) -> f64 { self.0 * self.0 } }

fn static_area<S: Shape>(s: &S) -> f64 { s.area() }     // 泛型：单态化，静态派发
fn dynamic_area(s: &dyn Shape) -> f64 { s.area() }       // trait object：vtable 派发
fn make(kind: &str) -> Box<dyn Shape> {
    match kind { "c" => Box::new(Circle(1.0)), _ => Box::new(Square(2.0)) }
}

fn main() {
    println!("{} {}", static_area(&Circle(1.0)), dynamic_area(&Circle(1.0)));  // 3.141592653589793 3.141592653589793
    let shapes: Vec<Box<dyn Shape>> = vec![make("c"), make("s")];
    for s in &shapes { println!("{} {}", s.name(), s.area()); }  // circle 3.141592653589793 / shape 4
}
```

选择哪种派发是显式的设计决定：泛型参数更快但会让二进制膨胀（每个类型一份代码），`dyn Trait` 更小更灵活但每次调用多一次间接跳转、不能内联。一个类型可以同时被两者使用，转换用 `&c as &dyn Shape` 或 `Box::new(c) as Box<dyn Shape>`。trait 里带默认实现的方法进入 vtable，实现类型可以覆盖；trait object 要求 trait 是"对象安全"的（没有泛型方法、没有返回 `Self` 的方法、没有关联常量）。Rust 没有虚构造函数、没有基类指针，所以没有 C++ 的菱形继承与切片问题，代价是没有继承复用——组合与 trait 默认实现是替代品。调用 `s.area()` 时编译器还会自动插入 `&`/`*` 调整（auto-ref/deref），这也是 `Rc<T>` 上能直接调 `T` 方法的原因。

📘 [Rust · trait object](https://doc.rust-lang.org/book/ch17-02-trait-objects.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的派发方式有三种。`class` 的方法默认走 vtable（动态派发），标 `final` 或写进 `extension` 里（不覆盖）时编译器可以改成静态派发；协议要求的方法走 witness table，也是动态派发；而**协议扩展里提供的方法不进 witness table**，它们按变量的静态类型选择实现。值类型（`struct`/`enum`）的方法默认静态派发。

```swift
// /tmp/verify/dispatch.swift（swiftc 6.4 实测）
protocol Shape { func area() -> Double }                 // 协议要求：witness table
extension Shape { func name() -> String { "shape" } }     // 协议扩展：静态派发

struct Circle: Shape { let r: Double; func area() -> Double { 3.141592653589793 * r * r } }
struct Square: Shape { let a: Double; func area() -> Double { a * a } }
extension Circle { func name() -> String { "circle" } }   // 具体类型自己的 name

func total(_ shapes: [Shape]) -> Double { shapes.reduce(0) { $0 + $1.area() } }
func genericTotal<S: Shape>(_ shapes: [S]) -> Double { shapes.reduce(0) { $0 + $1.area() } }

let shapes: [Shape] = [Circle(r: 1), Square(a: 2)]
print(total(shapes))                    // 7.141592653589793
print(genericTotal([Circle(r: 1)]))     // 3.141592653589793
let c = Circle(r: 1)
print(c.name())                          // circle ← Circle 自己的 name
let asShape: Shape = c
print(asShape.name())                    // shape  ← ⚠️ 协议扩展按静态类型选择
print((asShape as! Circle).name())       // circle

class Base { func who() -> String { "Base" } }
class Sub: Base { override func who() -> String { "Sub" } }
print([Base(), Sub()].map { $0.who() })  // ["Base", "Sub"]
```

`asShape.name()` 打印 `shape` 而不是 `circle`，这是 Swift 里最值得记住的派发陷阱：协议扩展提供的方法不参与动态派发，如果希望子类型能定制行为，必须把它写成协议要求（`protocol Shape { func name() -> String }`）而不是只写在 `extension` 里。`@objc dynamic` 是第三种派发路径，把方法暴露给 Objective-C runtime，支持 KVO、`responds(to:)` 与运行时替换，代价是失去 Swift 的优化；只在需要与 ObjC 互操作或用 swizzling 时才用。泛型函数的调用点在编译期静态绑定，但函数体内对协议要求的调用默认走 witness table（一份代码服务所有类型）；编译器在看得到具体类型时会做泛型特化，把 witness 调用变成静态派发并内联，`some Shape`（opaque type）与 `any Shape`（existential）的区别正在于"静态已知具体类型 vs 走 witness table 的装箱"：`some` 编译期已知具体类型，`any` 走 witness table。继承的类用 vtable，`final` 类整体可静态派发，这是 Swift 性能调优的常见手段。

📘 [Swift · 协议](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/protocols/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的派发是二元的：具体类型上的方法调用在编译期静态解析（甚至可内联）；接口值上的调用通过 itable（接口类型 + 具体类型组成的表）在运行时找到函数指针，属于动态派发。Go 没有继承、没有虚函数关键字，接口是唯一的抽象机制，接口满足是隐式的（结构化检查）。嵌入（embedding）提供"方法提升"，但它不是继承，派发目标仍是嵌入字段的具体类型。

```go
// /tmp/verify/go/dispatch.go（go 1.27.1 实测）
package main

import "fmt"

type Shape interface {
	Area() float64
	Name() string
}
type Named struct{ n string }

func (n Named) Name() string { return n.n }        // 方法被提升到嵌入它的类型

type Circle struct {
	Named
	r float64
}
type Square struct {
	Named
	a float64
}

func (c Circle) Area() float64 { return 3.141592653589793 * c.r * c.r }
func (s Square) Area() float64 { return s.a * s.a }

func totalArea(shapes []Shape) float64 {           // 接口切片：itable 派发
	t := 0.0
	for _, s := range shapes { t += s.Area() }
	return t
}

func main() {
	c := Circle{Named{"circle"}, 1}
	s := Square{Named{"square"}, 2}
	fmt.Println(totalArea([]Shape{c, s}))    // 7.141592653589793
	fmt.Println(c.Name(), c.Named.n)          // circle circle
	var sh Shape = c
	fmt.Println(sh.Area())                     // 3.141592653589793
	var nilShape Shape
	fmt.Println(nilShape == nil)               // true
}
```

接口值在运行时是一对（类型, 数据）指针，只有这两者都为 nil 时接口才等于 nil；把 `(*T)(nil)` 塞进接口会得到一个"非 nil 的接口包着 nil 指针"，`err != nil` 判断因此失效——这是 Go 最常见的陷阱之一。嵌入带来的是方法提升而不是覆盖：`Circle` 自己定义 `Area` 就遮蔽了嵌入字段的同名方法，但没有虚表，`Named.Name` 里永远不会回跳到 `Circle`。接口满足是编译期检查的隐式行为，所以"这个类型实现了哪些接口"需要靠工具（`go doc`）而不是声明去查。空接口 `any` 不做任何方法要求，配合类型断言（`v.(T)`）或类型 switch 可以在运行时恢复具体类型。性能上，接口调用有间接跳转与装箱开销，热点路径上能用具体类型就用具体类型。

📘 [Go spec · 接口类型](https://go.dev/ref/spec#Interface_types)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的方法是运行时的属性查找：先在实例字典找，再沿 MRO（C3 线性化得到的类列表）找，属性若是描述符就触发 `__get__` 完成绑定。多态不靠继承声明而靠 duck typing——只要对象有那个方法就能调。找不到属性时落到 `__getattr__`，`super()` 按 MRO 取"下一个类"的版本，这让协作式多重继承成为可能。

```python
# /tmp/verify/dispatch.py（python3 3.14.7 实测）
class A:
    def who(self): return "A"
class B(A):
    def who(self): return "B+" + super().who()
class C(A):
    def who(self): return "C+" + super().who()
class D(B, C):
    def who(self): return "D+" + super().who()

print(D().who())                          # D+B+C+A
print([k.__name__ for k in D.__mro__])    # ['D', 'B', 'C', 'A', 'object']

def describe(x):                           # duck typing：不检查类型，只调用行为
    return x.who()
class Fake:
    def who(self): return "Fake"
print(describe(Fake()))                    # Fake

class Dyn:
    def __getattr__(self, name):            # 常规查找失败后触发
        if name.startswith("g_"):
            return lambda: f"动态 {name}"
        raise AttributeError(name)
print(Dyn().g_x())                          # 动态 g_x

from functools import singledispatch        # 按第一个参数类型分派（模拟重载）
@singledispatch
def area(x): return "unknown"
@area.register
def _(x: int): return x * x
@area.register
def _(x: str): return len(x)
print(area(3), area("abcd"), area(3.5))     # 9 4 unknown
```

MRO 由 C3 线性化算法生成，保证每个类只出现一次且保持局部优先顺序；`super()` 不是"父类"而是"MRO 里的下一个类"，所以在菱形结构中每个类的方法都能被依次调用一次（协作式多重继承），这也是 `D().who()` 能串起 `D+B+C+A` 的原因。`__getattr__` 与 `__getattribute__` 要分清：后者拦截**所有**属性访问（写错容易死循环，必须显式 `object.__getattribute__`），前者只在前者失败后兜底。Python 只有单分派（一个接收者），要按多个参数类型分派需自己用 `functools.singledispatch` 组合或者上 `multipledispatch` 这类第三方库。属性查找的性能敏感路径应避免 `__getattr__` 兜底与深层 MRO，`__slots__` 能去掉实例字典减少内存与查找开销。

📘 [Python · MRO](https://docs.python.org/3/howto/mro.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 编译到 JVM，所以派发语义跟 Java 一致：类方法走 vtable，接口方法走 itable；唯一差别是 Kotlin 类的方法**默认 final**，允许重写必须显式 `open`（接口方法天然开放）。`override` 是强制的。扩展函数不参与派发，按静态类型解析。

```kotlin
open class Shape {                                  // open 才能被继承与重写
    open fun name(): String = "shape"                // open 才能被重写
    fun sealed(): String = "sealed"                   // 默认 final，静态派发
}
class Circle(val r: Double) : Shape() {
    override fun name(): String = "circle"
}
interface HasArea { fun area(): Double }             // 接口方法默认可重写
class Sq(val a: Double) : HasArea { override fun area() = a * a }

fun describe(s: Shape): String = s.name()             // 参数类型 Shape：vtable 派发
fun describe(s: HasArea): String = "area=${s.area()}" // 重载：编译期按静态类型选

fun Shape.extra(): String = "extra"                  // 扩展：静态解析

fun main() {
    val shapes: List<Shape> = listOf(Shape(), Circle(1.0))
    println(shapes.map { it.name() })               // [shape, circle]
    println(describe(Circle(1.0) as Shape))          // circle
    println(describe(Sq(2.0)))                        // area=4.0
    println(Circle(1.0).extra())                      // extra
    val s: Shape = Circle(1.0)
    println(s.extra())                                // extra（扩展只看静态类型）
}
```

`open`/`final` 的选择是 Kotlin 相对 Java 最大的设计意图：默认关闭继承与重写，避免"为继承而设计"的脆基类问题；代价是要给每个可扩展点显式加 `open`。`override` 的方法默认仍是开放的，想禁止继续重写要写 `final override`。扩展函数与成员函数同名时成员优先，且两个重载 `describe(Shape)` 与 `describe(HasArea)` 在调用点按**静态类型**选择——把 `Sq` 赋给 `Any` 变量后就选不到 `HasArea` 版本。数据类、密封类（`sealed`）、`when` 穷尽检查是 Kotlin 替代"用继承表达多种情况"的常用手段：密封类的层次在编译期封闭，`when` 分支可以静态穷尽，比运行期 dispatch 更安全。

📘 [Kotlin · 继承](https://kotlinlang.org/docs/inheritance.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的方法默认全部是虚方法：只有 `static`、`private`、`final` 以及构造函数不参与动态派发，其余调用都按对象的运行时类型选择实现。JVM 用 vtable（类）与 itable（接口）实现，但现代 JIT 会做内联缓存与类型 Profile，把"实际上只有一种类型"的调用点优化成静态调用。接口的默认方法也参与派发。

```java
// 版本基线：Java 26（LTS 25）
class Shape {
    String name() { return "shape"; }              // 默认虚
    static String kind() { return "Shape"; }        // static：静态绑定
    final String sealed() { return "sealed"; }      // final：不可重写，可静态绑定
    private String secret() { return "secret"; }     // private：不参与派发
}
class Circle extends Shape {
    private final double r;
    Circle(double r) { this.r = r; }
    @Override String name() { return "circle"; }
}
interface HasArea {
    double area();
    default String unit() { return "u"; }            // 默认方法：走 itable 派发
}

public class Main {
    static String describe(Shape s) { return s.name(); }   // 编译期签名 Shape，运行时看对象
    public static void main(String[] args) {
        Shape[] shapes = { new Shape(), new Circle(1) };
        for (Shape s : shapes) System.out.print(s.name() + " ");   // shape circle
        System.out.println();
        System.out.println(describe(new Circle(1)));                 // circle
        System.out.println(new Circle(1).sealed() + Shape.kind());    // sealedShape
        HasArea a = new HasArea() { public double area() { return 4.0; } };
        System.out.println(a.area() + " " + a.unit());                // 4.0 u
    }
}
```

动态派发带来的经典陷阱是"构造函数调用可重写方法"：父类构造器执行时子类字段还是默认值，重写方法会读到 `null`/`0`。Java 与 C++ 在这点上不同——Java 默认虚，C++ 默认静态，所以 Java 里这个问题更常见（JEP 513 正是为了缓解构造期的初始化顺序问题）。`static` 方法不参与重写但可以被"隐藏"（hiding）：子类写同名 `static` 方法只是遮蔽，通过父类引用调用仍走父类版本，这与实例方法的重写语义完全不同。字段访问永远静态绑定（按引用的编译期类型），只有方法调用才动态派发，这条规则解释了"字段被遮蔽"的现象。接口默认方法冲突时必须在实现类里显式 `Interface.super.method()` 指定。

📘 [JLS · 方法调用的运行时求值](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.12.4)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的默认选择与 Java 相反：成员函数默认静态绑定，只有 `virtual` 才进入 vtable 做动态派发，纯虚函数（`= 0`）让类成为抽象类。这一设计把"是否有运行时代价"的决定权交给程序员，代价是容易忘记 `virtual` 而导致多态静默失效。多重继承引出菱形问题与"切片"，虚拟继承与指针/引用传参是解法。

```cpp
// /tmp/verify/oo.cpp（Apple clang 21, -std=c++23 实测）
#include <iostream>

struct A { virtual ~A() = default; virtual const char* who() const { return "A"; } };
struct B : A { const char* who() const override { return "B"; } };
struct C : A { const char* who() const override { return "C"; } };
struct D : B, C {                       // 菱形：D 里有两份 A 子对象
    const char* who() const override { return "D"; }
};
struct E : virtual A { };               // 虚继承：E、F 共享唯一一份 A
struct F : virtual A { };
struct G : E, F { const char* who() const override { return "G"; } };

struct Static { void hi() const { std::cout << "Static::hi\n"; } };
struct Shadow : Static { void hi() const { std::cout << "Shadow::hi\n"; } };

int main() {
    D d; C* pc = &d;
    std::cout << pc->who() << '\n';        // D：vtable 派发
    G g; A* pa = &g;
    std::cout << pa->who() << '\n';        // G：虚继承后转 A* 不再二义
    Shadow s; Static* ps = &s;
    ps->hi();                               // Static::hi（非虚：静态绑定）
    s.hi();                                 // Shadow::hi
}
```

把 `D` 转成 `A*` 是编译错误（两份 `A` 子对象，二义），必须先用 `static_cast` 指定走 `B` 还是 `C`；`virtual` 继承让公共基类只保留一份，代价是访问虚基类成员要多一次间接寻址，且 `sizeof` 与布局更复杂。非虚函数通过基类指针调用的是基类版本（`Static::hi`），这就是"忘了 `virtual` 多态就没了"的现场。按值传基类会切片（slicing），派生部分与 vtable 指针被切掉，务必用 `const T&` 或 `T*`。析构函数在多态基类里必须是 `virtual`，否则 `delete` 基类指针不会调用派生析构。`override` 与 `final` 是 C++11 起用来防止"签名写错导致没重写"的编译期检查，应该总是写。vtable 派发无法内联，但 `final` 类/方法与 `-fdevirtualize` 能让编译器去虚化。

📘 [cppreference · virtual 说明符](https://en.cppreference.com/w/cpp/language/virtual)

{{% /tab %}}

{{% tab header="C" %}}

C 里没有派发机制：函数调用在编译期（或链接期）绑定到具体地址，没有 vtable、没有运行期方法查找。要模拟运行期多态，只能自己维护函数指针表并在结构体里存类型标签，然后手工 `switch` 或间接调用。C 也没有名字修饰，所以"方法解析"在 C 里就是"链接器符号解析"。

```c
/* /tmp/verify/spec.c（Apple clang 21, -std=c23 实测） */
#include <stdio.h>

typedef enum { KIND_CIRCLE, KIND_SQUARE } Kind;      /* 手工的类型标签 */

typedef struct Shape Shape;
struct Shape {
    Kind kind;                                        /* 运行期判断靠这个字段 */
    double (*area)(const Shape *);                     /* 或者靠函数指针表 */
    void   (*destroy)(Shape *);
};
typedef struct { Shape base; double r; } Circle;
typedef struct { Shape base; double a; } Square;

static double circle_area(const Shape *s) {
    const Circle *c = (const Circle *)s;               /* 手工向下转换，没有检查 */
    return 3.141592653589793 * c->r * c->r;
}
static double square_area(const Shape *s) {
    const Square *q = (const Square *)s;
    return q->a * q->a;
}
static void noop_free(Shape *s) { (void)s; }

int main(void) {
    Circle c = { { KIND_CIRCLE, circle_area, noop_free }, 1.0 };
    Square q = { { KIND_SQUARE, square_area, noop_free }, 2.0 };
    Shape *shapes[2] = { (Shape *)&c, (Shape *)&q };
    for (int i = 0; i < 2; i++)
        printf("%.1f\n", shapes[i]->area(shapes[i]));   /* 3.1 / 4.0，人工间接调用 */
    return 0;
}
```

函数指针表是唯一可行的"虚函数"方案，但编译器无法帮你检查表是否填全、类型转换是否安全：`(const Circle *)s` 这种向下转换如果 `kind` 判断写错就是 UB。工程上通常两者并用——用 `kind` 标签做分支（可读、可调试），用函数指针表做高频调用路径。没有重载与泛型，同一组操作只能靠命名约定（`shape_area_circle`）或宏生成；`_Generic` 能在编译期按类型选择表达式，但分支必须在宏展开时全部写出来，不能像模板那样递归实例化。C 的静态派发在性能上是最好的（直接调用、可内联），这也是大量底层库坚持 C ABI 的原因。

📘 [cppreference · C 函数声明](https://en.cppreference.com/w/c/language/functions)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的核心就是多分派：调用 `f(a, b)` 时，运行期拿全部实参的类型去方法表里找最具体的方法（most specific method），既不是单分派也不是静态重载。方法按参数类型组织，`abstract type` 提供层次，`Union` 与类型参数表达约束。多分派让"运算符按两边类型分派"这种在其他语言里要特判的事情变得自然，代价是可能出现歧义（ambiguity）。

```julia
# 版本基线：Julia 1.13
abstract type Shape end
struct Circle <: Shape; r::Float64; end
struct Square <: Shape; a::Float64; end

area(s::Circle) = pi * s.r^2
area(s::Square) = s.a^2
area(s::Shape)  = error("未实现 area")      # 抽象类型兜底
area(v::AbstractVector{<:Shape}) = sum(area, v)   # 容器：按元素类型分派

println(area(Circle(1.0)))        # 3.141592653589793
println(area([Circle(1.0), Square(2.0)]))   # 7.141592653589793
println(which(area, (Circle,)))   # 查看具体选中哪个方法

# 歧义：两个方法互不更具体
f(x::Int, y::Any) = "int,any"
f(x::Any, y::Int) = "any,int"
try
    f(1, 1)
catch e
    println(typeof(e))            # MethodError（提示 ambiguous）
end
f(x::Int, y::Int) = "int,int"     # 补一个更具体的方法消歧
println(f(1, 1))                   # int,int
println(length(methods(f)))        # 3
```

歧义发生在两个方法的签名都匹配、且谁也不比谁更具体时（经典例子是 `(Int, Any)` 与 `(Any, Int)`），修复办法只有一个：在交集处加一个更具体的方法。`Union` 类型可以精确表达"这个参数接受 A 或 B"，比 `Any` 更具体，常用于消除歧义。类型参数（`Vector{<:Shape}`）与 `where` 子句让方法签名的表达力远超单分派语言。多分派的方法数量增长很快，`methods(f)` 与 `@which` 是必备工具；编译期会为每个具体调用做特化（specialization），所以第一次调用有编译延迟。Julia 没有 `this`，接收者只是第一个参数，"面向对象"的写法要靠约定（`area(shape)` 而不是 `shape.area()`），而 `shape.area()` 只是 `area(shape)` 的点号语法。

📘 [Julia · 方法表与歧义](https://docs.julialang.org/en/v1/manual/methods/#Ambiguities)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的实例方法默认非虚：想支持运行期多态必须写 `virtual`（或 `abstract`），重写写 `override`。调用 `virtual` 方法走 vtable，`sealed override` 或 `final` 类可让 JIT 去虚化；接口调用走接口映射表（interface map）。JIT 有内联缓存，实际性能往往接近静态调用。C# 还支持 `new` 关键字隐藏基类成员，这与 `override` 语义完全不同。

```csharp
// 版本基线：C# 14 / .NET 10
using System;

public abstract class Shape
{
    public abstract double Area();                 // 抽象方法：派生类必须实现
    public virtual string Name() => "shape";        // 虚方法：可重写
    public string Sealed() => "sealed";             // 非虚：静态绑定
}
public sealed class Circle : Shape                 // sealed：可去虚化
{
    private readonly double r;
    public Circle(double r) => this.r = r;
    public override double Area() => 3.141592653589793 * r * r;
    public override string Name() => "circle";
}
public class Square : Shape
{
    public double A { get; }
    public Square(double a) => A = a;
    public override double Area() => A * A;
    public new string Sealed() => "hidden";          // new：隐藏，不是重写
}

public interface IHasArea { double Area(); }

public class Program
{
    public static void Main()
    {
        Shape[] shapes = { new Circle(1), new Square(2) };
        double total = 0;
        foreach (var s in shapes) { total += s.Area(); Console.Write(s.Name() + " "); }  // circle square
        Console.WriteLine($"\n{total}");                              // 7.141592653589793
        Square sq = new Square(2);
        Shape asShape = sq;
        Console.WriteLine($"{sq.Sealed()} {asShape.Sealed()}");        // hidden sealed
    }
}
```

`new` 隐藏与 `override` 重写的区别常被搞混：`new` 只是让子类引入一个同名成员，通过基类引用调用的仍是基类版本；`override` 才替换虚表条目，两种引用都得到子类版本。C# 里接口方法实现可以使用显式实现（`double IHasArea.Area() => ...`），此时只有把对象转成接口才能调到该方法，用于解决成员名冲突与隐藏实现细节。结构体（`struct`）无法继承，其接口调用会被装箱（除非用泛型约束 `where T : IHasArea`），这是值类型上多态的主要性能陷阱。`sealed` 类/方法除了表达设计意图，还给 JIT 提供了去虚化机会；`abstract` 成员只能出现在抽象类或接口里。C# 没有多重继承（类只能单继承，接口可以多个），因此不存在菱形继承问题，但要注意接口默认方法冲突时必须在实现类中显式指定。

📘 [MS Learn · 多态](https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/object-oriented/polymorphism)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的实例方法默认都是虚的：任何没标 `static` 的成员方法都能被 `@override` 重写，调用走运行期的类方法表；`@override` 只是注解（漏写只有 lint 警告）。Dart 用隐式接口实现"面向接口编程"：任何类都可以被 `implements`，此时只取签名、必须全部实现。扩展方法与扩展类型不参与派发，编译期静态解析。

```dart
// 版本基线：Dart 3.13
abstract class Shape {
  double area();                              // 抽象方法：子类必须实现
  String name() => 'shape';                    // 具体方法：默认可重写
}
class Circle implements Shape {
  final double r;
  Circle(this.r);
  @override double area() => 3.141592653589793 * r * r;
  @override String name() => 'circle';
}
class Square implements Shape {
  final double a;
  Square(this.a);
  @override double area() => a * a;
  @override String name() => 'square';
}

double total(List<Shape> shapes) {            // 参数类型 Shape：动态派发
  var t = 0.0;
  for (final s in shapes) t += s.area();
  return t;
}

void main() {
  final shapes = <Shape>[Circle(1), Square(2)];
  print(shapes.map((s) => s.name()).toList());   // [circle, square]
  print(total(shapes));                           // 7.141592653589793
  dynamic d = Circle(1);                          // dynamic：完全运行期解析
  print(d.area());                                // 3.141592653589793
}
```

`implements` 与 `extends` 的差别是 Dart 里最容易踩的：`implements` 只拿接口不拿实现，包括 `name()` 这种带默认实现的方法也必须重新实现（因为接口只描述签名）；`extends` 才继承实现并可以 `super`。Dart 没有虚函数关键字，也没有 `final` 方法，想禁止重写只能在类上加 `final`/`sealed`（Dart 3 的类修饰符）。`dynamic` 类型让所有调用在运行时通过 `noSuchMethod` 解析，性能差且失去静态检查，只在互操作或高度动态场景使用；`Object?` 加 `is` 检查 + 类型提升是更好的替代。类修饰符体系（Dart 3）值得记住：`base` 强制子类必须继承、`interface` 禁止继承只允许实现、`final` 禁止本库之外的继承与实现（同一 library 内仍可继承或实现）、`sealed` 限定同库内穷尽子类，它们共同把"可扩展性"从默认开放改成显式声明。

📘 [Dart · 类](https://dart.dev/language/classes)

{{% /tab %}}

{{% tab header="R" %}}

R 的派发是运行时的：S3 的 `UseMethod` 按第一个参数的 `class` 属性依次查找 `f.类名`，S4 的 `standardGeneric` 按正式的签名表匹配（支持多参数联合分派），R5/R6 的对象系统则把方法存进对象自己的环境。R 没有编译期检查，方法不存在只会在调用时报错。函数查找与变量查找一样走搜索路径（search path），因此同名泛型函数可能被后加载的包遮蔽。

```r
# 版本基线：R 4.6
area <- function(x, ...) UseMethod("area")             # S3 泛型
area.default <- function(x, ...) stop("没有 area 方法")  # 兜底
area.circle <- function(x, ...) pi * x$r^2
area.square <- function(x, ...) x$a^2
area.list <- function(x, ...) vapply(x, area, numeric(1))   # 对容器也能分派

circle <- function(r) structure(list(r = r), class = "circle")
square <- function(a) structure(list(a = a), class = "square")
shapes <- list(circle(1), square(2))

cat(area(circle(1)), "\n")                 # 3.141593
cat(sum(area(shapes)), "\n")                # 7.141593（area.list 再逐个分派）
print(methods("area"))                       # area.circle / area.default / area.list / area.square

# 多重继承在 S3 里是 class 向量：先找到的先生效
obj <- structure(list(), class = c("special", "circle"))
area.special <- function(x, ...) "special 优先"
cat(area(obj), "\n")                         # special 优先
cat(area(circle(2)), "\n")                   # 12.56637
```

S3 的分派只看第一个参数、只看 `class` 属性，`area.default` 是必需的安全网；`class` 是向量时按顺序匹配，所以"多重继承"在 S3 里表现为优先级列表。S4 通过 `setGeneric` 建立正式泛型，`signature()` 可以同时约束多个参数，冲突时按距离与继承关系选择；S4 的方法表存在泛型函数的属性里，用 `selectMethod`、`showMethods`、`existsMethod` 检查。R5（`setRefClass`）与 R6 采用引用语义，方法通过 `$` 挂在对象上，不需要全局泛型函数，但失去了 `UseMethod` 那种"同一个名字服务所有类型"的统一性。R 的 `Ops` 组泛型是一个特殊技巧：`Ops.circle` 一次性覆盖 `+`、`-`、`*`、`/`、`^`、`%%`、`%/%`、`==`、`!=`、`<`、`>`、`<=`、`>=`，实现自定义类型的运算符重载。

📘 [R · S4 方法](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#S4-methods)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有任何运行期派发：`x.f(y)` 在编译期就确定成 `T.f(x, y)` 的直接调用，可以被内联，没有 vtable、没有接口、没有虚函数。想要"多态"有三条编译期路线：`comptime` 参数（按类型分支生成代码）、`anytype` 与泛型函数（单态化）、tagged union 加 `switch`（运行期分支但仍是直接调用）。Zig 甚至不在结构体里存函数指针表，除非你自己加。

```zig
// 版本基线：Zig 0.15
const std = @import("std");

const Circle = struct { r: f64, pub fn area(s: Circle) f64 { return 3.141592653589793 * s.r * s.r; } };
const Square = struct { a: f64, pub fn area(s: Square) f64 { return s.a * s.a; } };

// tagged union：运行期多态，但分派靠 switch 而非 vtable
const Shape = union(enum) {
    circle: Circle,
    square: Square,

    pub fn area(self: Shape) f64 {
        return switch (self) {                 // 编译期检查穷尽性
            .circle => |c| c.area(),
            .square => |s| s.area(),
        };
    }
};

fn totalArea(shapes: []const Shape) f64 {      // 直接调用，无间接跳转
    var t: f64 = 0;
    for (shapes) |s| t += s.area();
    return t;
}

// comptime 泛型：每个类型生成一份特化代码（单态化）
fn describe(shape: anytype) []const u8 {
    const T = @TypeOf(shape);
    return switch (T) {
        Circle => "circle",
        Square => "square",
        else => @compileError("未知形状类型"),
    };
}

pub fn main() void {
    const shapes = [_]Shape{ .{ .circle = .{ .r = 1 } }, .{ .square = .{ .a = 2 } } };
    std.debug.print("{d}\n", .{totalArea(&shapes)});        // 7.141592653589793
    std.debug.print("{s} {s}\n", .{ describe(Circle{ .r = 1 }), describe(Square{ .a = 2 }) });
}
```

Zig 的取舍很明确：把"能不能在运行期换实现"这件事从语言里拿掉，换取没有隐式间接调用、可预测的性能与完整的编译期检查。tagged union 加 `switch` 是 Zig 表达"一组固定变体"的惯用法，`switch` 的穷尽性由编译器强制，漏一个变体就编译失败；这与 Rust 的 `enum` 加 `match` 是同一思路，区别是 Zig 没有 trait object 那条动态路径。`comptime`/`anytype` 泛型在编译期为每个具体类型生成一份代码，跟 Rust 的单态化等价，代价是二进制膨胀。需要真正运行期可替换行为时（插件、动态后端），Zig 只能手工定义函数指针结构体，或者依赖外部 ABI（C 的函数指针）。

📘 [Zig · 编译期与 comptime](https://ziglang.org/documentation/master/#comptime)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 没有方法派发，但有属性访问的元方法链条：读 `t.k` 时如果 `t.k` 是 nil 且 `t` 有元表，就调用 `__index`（表则继续查、函数则调用），这条链可以层层嵌套，实现"类继承"与"默认值"。写 `t.k = v` 则走 `__newindex`。调用 `t:m()` 的解析发生在读 `t.m` 之后，因此继承的方法也能被正确吊起（但接收者仍是原对象）。Lua 只有这一种动态机制，没有接口、没有类型检查。

```lua
-- 版本基线：Lua 5.5
local Base = {}
Base.__index = Base
function Base.new(n) return setmetatable({ n = n }, Base) end
function Base:describe() return "Base(" .. self.n .. ")" end

local Loud = setmetatable({}, { __index = Base })   -- 类级继承链
Loud.__index = Loud
function Loud.new(n)
  local o = Base.new(n)
  return setmetatable(o, Loud)
end
function Loud:describe() return "Loud(" .. self.n .. ")" end   -- 覆盖

local b, l = Base.new(1), Loud.new(2)
print(b:describe(), l:describe())      -- Base(1) Loud(2)

-- 动态兜底：__index 是函数时按需计算
local Dyn = setmetatable({}, { __index = function(_, k) return "动态 " .. k end })
print(Dyn.foo, Dyn.bar)                -- 动态 foo 动态 bar

-- __newindex 拦截写入
local Guard = setmetatable({}, { __newindex = function(t, k, v)
  if type(v) ~= "number" then error("只允许数字: " .. k) end
  rawset(t, k, v)
end })
Guard.a = 1
print(Guard.a)                         -- 1
print(pcall(function() Guard.b = "x" end))   -- false 只允许数字: b
```

`__index` 链的查找开销与链长成正比，深层继承在热点路径上会明显变慢；`rawget`/`rawset` 可以绕过元方法直接操作表，实现内部状态时常用。`__index` 同时是表与函数会优先用表（如果键在表里），函数形式只在前者失败后调用；用函数做 `__index` 时记得用 `rawget` 或缓存，否则每次访问都要执行一遍逻辑。Lua 的"接口"只能是文档约定，`type()` 只区分 8 种基础类型，对象之间的多态靠"有没有那个方法"来判断——`if obj.describe then obj:describe() end` 是常见写法。`setmetatable` 只能给表设置元表（每表一个），这也是 Lua 继承模型在概念上比类语言更简单的原因。

📘 [Lua 5.5 · __index 元方法](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的"派发"分两层：运行时与 JavaScript 完全一致（原型链 + `this`），编译期则是结构化类型系统在检查兼容性——只要形状匹配就允许调用，不要求继承或 `implements` 声明。这种结构子类型（structural typing）让跨库组合容易，但也意味着"类型上有这个方法"不等于"运行时真的有"。`this` 参数与 `override` 是它给方法解析加的两道编译期保险。

```typescript
// 版本基线：TypeScript 7
interface Shape { area(): number; name?(): string }   // 可选方法：调用前要判空

class Circle {
  constructor(public r: number) {}
  area(): number { return 3.141592653589793 * this.r * this.r }
  name(): string { return 'circle' }
}
class Square {
  constructor(public a: number) {}
  area(): number { return this.a * this.a }
}

function total(shapes: Shape[]): number {     // 结构化：不要求 Circle/Square 显式 implements
  return shapes.reduce((t, s) => t + s.area(), 0)
}
const shapes: Shape[] = [new Circle(1), new Square(2)];
console.log(shapes.map(s => s.name?.() ?? '?')); // [ 'circle', '?' ]  name 是可选方法
console.log(total(shapes));                       // 7.141592653589793

class Base { who(this: Base): string { return 'Base' } }
class Sub extends Base { override who(): string { return 'Sub' } }
const b: Base = new Sub();
console.log(b.who());                             // Sub（运行时原型链派发）
// const wrong: Base = { who() { return 1 } };    // 🛑 编译错误：返回类型不兼容
const loose = { who: () => 'loose' };              // 没有继承，结构兼容即可
console.log((loose as Base).who());                 // loose ← 编译期通过、运行期无关
```

结构化类型最实用的地方是不用为了传参而写 `implements`：`Circle` 只要形状对就能塞进 `Shape[]`。代价是误报与漏报都存在——`as` 断言能骗过编译器，运行时该崩还是崩；可选方法（`name?()`）必须判空后再调，否则运行时是 `undefined is not a function`。`override` 关键字（TS 4.3+，配合 `noImplicitOverride`）强制子类重写时写明意图，漏写会编译报错，这比 JavaScript 只靠运行时才发现安全得多。`this` 参数除了类型检查，还能表达多态 `this`（返回 `this` 表示"返回当前子类实例"），链式 API 因此能保持类型不被拓宽。`declare module` 与接口合并能补类型，但不会生成任何运行时代码——类型声明的世界与运行时的世界必须自己保持一致。

📘 [TypeScript · 类型兼容性](https://www.typescriptlang.org/docs/handbook/type-compatibility.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的方法解析只有一条规则：沿原型链找属性，找到就调用，`this` 由调用表达式的形式决定。没有接口、没有类型、没有编译期检查，`obj.method()` 里 `method` 是不是函数要到运行时才知道。`instanceof` 沿原型链判断，`in` 与 `hasOwnProperty` 检查属性存在性，`Object.create` 与 `class` 是构造原型链的两种写法。

```javascript
// /tmp/verify/methods.js（node 24.20.0 实测；文档按 Node 26 写）
class Base {
  who() { return 'Base'; }
}
class Sub extends Base {
  who() { return 'Sub'; }
}
const b = new Sub();
console.log(b.who());                        // Sub（原型链找到 Sub.prototype.who）
console.log(b instanceof Base, b instanceof Sub);   // true true
console.log('who' in b, b.hasOwnProperty('who'));    // true false（who 在原型上）

const viaProto = Object.create(Base.prototype);      // 手工搭原型
console.log(viaProto.who());                          // Base
console.log(Object.getPrototypeOf(Sub.prototype) === Base.prototype);  // true

// 鸭子类型：不看类型只看有没有方法
function describe(x) {
  if (typeof x.who === 'function') return x.who();
  return 'no who';
}
console.log(describe({ who: () => 'duck' }), describe(42));   // duck no who

// Proxy：拦截方法查找（比改原型更安全的动态方案）
const logged = new Proxy(new Base(), {
  get(target, prop, receiver) {
    if (typeof target[prop] === 'function') {
      return (...args) => { console.log('调用', String(prop)); return target[prop](...args); };
    }
    return Reflect.get(target, prop, receiver);
  },
});
console.log(logged.who());                    // 调用 who / Base
```

`instanceof` 只检查原型链，跨 iframe 或 `Object.create(null)` 的对象会让它失效；`typeof`/`in`/`Array.isArray` 往往更可靠。`this` 绑定与原型查找是两件独立的事：查找决定"调用哪个函数"，调用形式决定"函数里 `this` 是谁"，所以把原型方法摘出来调用会崩，而用 `Proxy`/`bind` 可以改变行为。`Proxy` 的 `get` 陷阱是拦截方法查找最灵活的手段（不用改原型、作用域局部），代价是每次属性访问都有开销且难以调试。JS 里没有真正的"接口实现的编译期检查"，替代是 JSDoc `@implements`、TypeScript 或运行时的形状断言（`typeof x.m === 'function'`）。`for...in` 会遍历原型链上的可枚举属性，判断自身属性要用 `Object.hasOwn`（或旧的 `hasOwnProperty`）。

📘 [MDN · 继承与原型链](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Inheritance_and_the_prototype_chain)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的方法解析在运行时进行：`$obj->m()` 按对象所属类沿继承链查找，接口与抽象方法提供编译期约束，`parent::`、`self::`、`static::` 三种写法分别表示"父类实现""当前类定义""调用者类（后期静态绑定）"。找不到方法时落到 `__call` / `__callStatic`，属性访问落到 `__get`/`__set`。PHP 支持单继承加多接口，trait 用于水平复用实现。

```php
// 版本基线：PHP 8.5
abstract class Shape
{
    abstract public function area(): float;                 // 抽象方法：子类必须实现
    public function name(): string { return 'shape'; }        // 具体方法：可重写
    public static function kind(): string { return static::class; }   // 后期静态绑定
}
final class Circle extends Shape
{
    public function __construct(private float $r) {}
    public function area(): float { return 3.141592653589793 * $this->r ** 2; }
    public function name(): string { return 'circle'; }
}
class Square extends Shape
{
    public function __construct(private float $a) {}
    public function area(): float { return $this->a ** 2; }
    public function __call(string $name, array $args): string { return "missing $name"; }
}

function total(array $shapes): float {
    $t = 0.0;
    foreach ($shapes as $s) $t += $s->area();                 // 动态派发
    return $t;
}
$shapes = [new Circle(1), new Square(2)];
echo implode(' ', array_map(fn($s) => $s->name(), $shapes)), PHP_EOL;  // circle shape
echo total($shapes), PHP_EOL;                                  // 7.141592653589793
echo Circle::kind(), PHP_EOL;                                   // Circle（static:: 指向调用者）
echo (new Square(1))->whatever(), PHP_EOL;                       // missing whatever
var_dump($shapes[0] instanceof Shape);                          // bool(true)
```

三种作用域解析要分清：`self::` 绑定到书写它的类（写死在基类里）、`static::` 绑定到实际调用的类（后期静态绑定，工厂与 `get_class` 场景需要）、`parent::` 调用父类实现。抽象方法只声明签名，接口则连具体方法都不给实现，两者都参与运行时的类检查；`final` 类与方法禁止进一步重写。`__call` 让"未定义方法"变成可控行为（Laravel 的门面、Eloquent 的动态查询都靠它），但它会掩盖拼写错误，且 `method_exists` 不会自动感知（`is_callable` 在 PHP 8 起会因为 `__call` 返回 true）。PHP 是单继承，接口可以多实现，trait 通过 `use` 合入方法；三个来源的同名方法优先级是"类自身 > trait > 继承的父类方法"，trait 之间冲突要用 `insteadof`/`as` 显式解决。

📘 [PHP · 后期静态绑定](https://www.php.net/manual/en/language.oop5.late-static-bindings.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 是纯粹的单分派：消息发给一个接收者，运行时沿 `ancestors` 链查找方法，第一个匹配者胜出。方法查找顺序是"单例类 → prepend 的模块 → 类自身 → include 的模块 → 父类 → Object → Kernel → BasicObject"，找不到就发 `method_missing`。`super` 沿祖先链继续往后找，不是"跳到父类"。运算符、`[]`、`<<`、`==` 都是方法，所以派发规则对它们同样适用。

```ruby
# /tmp/verify/refine.rb（ruby 4.0.6 实测）
module Extra
  def describe = "Extra:" + super        # prepend 的模块能 super 到原实现
end
class Shape
  def describe = "Shape"
end
class Circle < Shape
  def describe = "Circle<" + super + ">"
end
Circle.prepend(Extra)

puts Circle.new.describe          # Extra:Circle<Shape>
puts Circle.ancestors.take(4).inspect   # [Extra, Circle, Shape, Object]

# 动态方法：define_method 比 method_missing 更好（会更新 instance_methods）
class Dyn
  [:a, :b].each { |n| define_method("get_#{n}") { "值 #{n}" } }
  def method_missing(name, *args)
    return "兜底 #{name}" if name.to_s.start_with?("x_")
    super
  end
  def respond_to_missing?(name, _p = false) = name.to_s.start_with?("x_") || super
end
d = Dyn.new
puts [d.get_a, d.get_b, d.x_y].inspect   # ["值 a", "值 b", "兜底 x_y"]
puts Dyn.instance_methods(false).sort.inspect  # [:get_a, :get_b, :method_missing]（respond_to_missing? 是 private）
puts d.respond_to?(:x_y)                  # true（靠 respond_to_missing?）
```

`prepend` 让模块排在类之前，模块方法里 `super` 就能调到类原本的实现，这是实现"装饰/增强"最干净的方式（比 alias_method 链可靠）；`include` 只把模块放在类之后，类自己的同名方法优先。单分派意味着多态只看接收者一个对象，想按参数类型分派只能自己写 `case` 或上多重分派库（`multi` gem）。`method_missing` 是同步钩子，会拖慢所有未命中查找并让调试困难，能用 `define_method` 就用它（还会正确更新 `instance_methods` 与 `respond_to?`）；非用不可时必须配套 `respond_to_missing?`。`Module#refine` 是作用域受限的猴子补丁，只在 `using` 之后的词法作用域生效（前面的验证代码显示 `"abc".respond_to?(:shout)` 在 `using` 前是 `false`、之后是 `true`），适合给内建类加方法而不污染全局。`Module#alias_method` 与 `super` 组合是 Rails 里常见的"在不改原实现的前提下加行为"的手法。

📘 [Ruby · 方法查找与 ancestors](https://docs.ruby-lang.org/en/master/Module.html#method-i-ancestors)

{{% /tab %}}

{{< /tabpane >}}

### 特殊方法

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 没有构造函数语法：惯例是用返回 `Self` 的关联函数 `new`，`Default::default()` 提供默认值。析构靠 `Drop` trait，在值离开作用域时确定性执行（不是 GC 回调），因此可以安全地释放文件句柄、锁等资源，这就是 RAII。运算符重载通过标准库的 `std::ops` trait 完成，`==`/`Ord` 有独立的 trait，且需要与 `Eq`/`Hash` 保持一致。

```rust
// /tmp/verify/spec.rs（rustc 1.98.1 实测）
use std::ops::Add;

#[derive(Debug, PartialEq)]
struct Vec2 { x: i32, y: i32 }

impl Vec2 {
    fn new(x: i32, y: i32) -> Self { Self { x, y } }     // 关联函数充当构造函数
}
impl Add for Vec2 {                                       // 运算符重载
    type Output = Vec2;
    fn add(self, o: Vec2) -> Vec2 { Vec2::new(self.x + o.x, self.y + o.y) }
}
impl Drop for Vec2 {                                      // 析构：作用域结束即跑
    fn drop(&mut self) { println!("drop {}-{}", self.x, self.y); }
}

fn main() {
    let a = Vec2::new(1, 2);
    let b = Vec2::new(3, 4);
    let s = a + b;
    println!("{:?}", s);                                  // Vec2 { x: 4, y: 6 }
    println!("{}", s.x == 4 && s.y == 6);                  // true
}   // a、b 被移动进 add，在 add 返回时先析构（drop 3-4 / drop 1-2），这里只析构 s（drop 4-6）
```

`Drop::drop` 不能手工调用（会 double free），需要提前释放就用 `std::mem::drop(x)`；实现 `Drop` 的类型不能同时是 `Copy`。`Drop` 的调用顺序是局部变量按声明逆序、字段按声明顺序，这个确定性是 Rust 与 Go/Java 最大的区别。`std::ops` 里可重载的运算符包括 `Add`、`Sub`、`Mul`、`Div`、`Rem`、`Neg`、`Not`、`BitAnd`、`BitOr`、`BitXor`、`Shl`、`Shr`、`Index`、`IndexMut`、`Deref`、`DerefMut`、`AddAssign` 等一系列 `*Assign`，以及 `Fn`/`FnMut`/`FnOnce`；不能重载 `==` 的运算符形式（用 `PartialEq`）、不能自定义 `&&`/`||`（无短路重载）、不能定义新的运算符。`Deref` 重载会造成"方法解析穿透"（`&T` 能调 `U` 的方法），这也是 `String` 能调 `&str` 方法的原因，但滥用会让代码难懂。给类型加 `#[derive(Debug, PartialEq, Eq, Hash, Clone, Copy)]` 能自动生成大部分"魔术方法"，比手写安全。

📘 [Rust · Drop trait](https://doc.rust-lang.org/std/ops/trait.Drop.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用 `init` 表达构造：指定初始化器（designated）负责初始化所有存储属性并向上调 `super.init`，便利初始化器（`convenience`）必须委托给同类的 `self.init`；`required init` 强制子类实现。析构用 `deinit`，在引用计数归零时调用，时机确定但线程不确定。运算符重载是定义静态函数，`callAsFunction` 让实例可调用，`subscript` 定义下标。

```swift
// /tmp/verify/special2.swift（swiftc 6.4 实测）
final class Box: CustomStringConvertible, Equatable, Hashable {
    let v: Int
    init(_ v: Int) { self.v = v }                       // 指定初始化器
    convenience init() { self.init(0) }                  // 便利初始化器：必须委托 self.init
    deinit { print("deinit \(v)") }                       // 析构：引用计数归零
    var description: String { "[\(v)]" }                  // 类似 toString
    static func == (l: Box, r: Box) -> Bool { l.v == r.v }
    func hash(into h: inout Hasher) { h.combine(v) }
    static func + (l: Box, r: Box) -> Box { Box(l.v + r.v) }   // 运算符重载
    static prefix func - (b: Box) -> Box { Box(-b.v) }          // 前缀运算符
    subscript(i: Int) -> Int { v + i }                          // 下标
    func callAsFunction(_ k: Int) -> Box { Box(v * k) }          // 实例可调用
}
var b: Box? = Box(3)
let sum = b! + Box(4)        // Box(4) 是临时值，表达式结束即 deinit 4
print(b!, sum, b![10])      // [3] Box(7) 13
print(b! == Box(3))          // true（比较用的临时 Box(3) 先析构，故先看到 deinit 3）
b = nil                      // deinit 3
```

`init` 的规则是 Swift 最严格的纪律之一：指定初始化器必须先把自己类的存储属性全部初始化，才能调用 `super.init`；便利初始化器不能碰存储属性，只能 `self.init(...)`。结构体的成员逐一初始化器（memberwise initializer）是编译器自动生成的，一旦你手写任何 `init`，它就消失（写进 `extension` 可以保留）。`deinit` 只能存在于类（`struct` 没有析构），其中不能调用 `self` 的异步方法、不能抛错、不能被手工调用；`deinit` 不是资源管理的唯一手段，确定性的清理应该用 `defer` 或 `withExtendedLifetime`。运算符重载必须是 `static func`（`prefix`/`postfix`/`infix` 修饰位置），`Equatable`、`Hashable`、`Comparable` 的自动合成能省去手写 `==`/`hash`/`<`，但自定义 `==` 时一定要让 `hash` 一致。`@objc` 类继承 `NSObject` 时 `deinit` 与 ObjC 的 `dealloc` 语义经过桥接，是介入资源释放的边界。

📘 [Swift · 初始化与析构](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/deinitialization/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 没有构造函数、没有析构函数、没有运算符重载、没有魔术方法：构造靠 `NewXxx` 工厂函数，资源释放靠显式 `Close()` 加 `defer`，字符串化靠实现 `fmt.Stringer`。`runtime.SetFinalizer` 提供不可靠的终结器钩子——它只在对象被 GC 回收时可能执行，也可能永不执行、或在程序退出时不执行。

```go
// /tmp/verify/go/special.go（go 1.27.1 实测）
package main

import (
	"fmt"
	"runtime"
)

type Box struct{ V int }

func NewBox(v int) *Box { return &Box{V: v} }        // 工厂代替构造函数

func (b Box) String() string { return fmt.Sprintf("[%d]", b.V) }   // fmt.Stringer

type Res struct{ name string }

func (r *Res) Close() error { fmt.Println("close", r.name); return nil }
func use(r *Res) { defer r.Close(); fmt.Println("使用", r.name) }   // defer 保证 cleanup

func main() {
	b := NewBox(3)
	fmt.Println(b)                     // [3]   String() 被 fmt 自动套用
	use(&Res{"res"})                    // 使用 res → close res
	runtime.SetFinalizer(b, func(x *Box) { fmt.Println("finalizer", x.V) })
	runtime.GC()
	fmt.Println("主流程结束")             // finalizer 可能在之前、之后或根本不出现
}
```

`defer` 是 Go 里资源清理的正统做法：按后进先出执行，即使 panic 也会执行，因此常见的模式是 `f, err := os.Open(...); defer f.Close()`。`runtime.SetFinalizer` 的语义陷阱很多：终结器在独立 goroutine 中运行，对象在那之后可能被"复活"，终结器只能设一次，且不能保证在程序结束前运行——所以它只适合做资源泄漏的最后兜底，绝不能当析构函数用（`os.File` 就是"平时用 `Close`，忘了被 GC 时靠终结器兜底"）。Go 没有运算符重载，自定义类型不能支持 `+`/`==`（`==` 只对可比较类型按值比较，切片、map、函数不可比较）；`fmt.Stringer`、`error`、`sort.Interface`、`io.Reader` 这些标准接口是"特殊方法"的替代形态，实现它们就能接入标准库生态。构造与校验要分开：`NewXxx` 返回 `(*T, error)` 是惯例，避免 panic。

📘 [Go · runtime.SetFinalizer](https://pkg.go.dev/runtime#SetFinalizer)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的特殊方法最多也最成体系：`__new__` 负责分配、`__init__` 负责初始化、`__del__` 是引用计数归零时的回调（不保证时机）、`__enter__`/`__exit__` 支撑 `with`、`__str__`/`__repr__` 管显示、`__eq__`/`__hash__`/`__len__`/`__getitem__`/`__call__` 管协议。运算符重载就是实现对应的 `__add__`、`__sub__` 等方法，`__slots__` 与 `@dataclass` 是减少样板代码的工具。

```python
# /tmp/verify/special.py（python3 3.14.7 实测）
import gc
gc.disable()                       # 关掉分代 GC，让引用计数的效果在输出里可见

class Box:
    def __new__(cls, v):            # 分配：先于 __init__，返回值必须是实例
        print("new")
        return super().__new__(cls)
    def __init__(self, v):          # 初始化：只负责赋值，不能有返回值
        print("init")
        self.v = v
    def __repr__(self): return f"Box({self.v})"     # 调试表示，容器里显示这个
    def __str__(self): return f"[{self.v}]"          # 面向用户
    def __eq__(self, o): return isinstance(o, Box) and self.v == o.v
    def __hash__(self): return hash(self.v)
    def __len__(self): return self.v
    def __getitem__(self, i): return self.v + i
    def __call__(self, k): return Box(self.v * k)
    def __del__(self): print("del", self.v)          # 引用计数归零时调用

b = Box(3)
print(repr(b), str(b), len(b), b[10])   # Box(3) [3] 3 13
x = b(2)
print(x.v, b == Box(3), hash(Box(1)) == hash(Box(1)))   # 6 True True（比较用的临时对象会先打印 del 3 / del 1 / del 1）
del x                                    # del 6
del b                                    # del 3
```

`__new__` 与 `__init__` 的分工是理解 Python 构造的关键：不可变类型（`int`、`str`、`tuple`）的值只能在 `__new__` 里决定，因此它们都在 `__new__` 里做事；单例、缓存、子类返回别的类型也靠 `__new__`。`__del__` 是"引用计数归零时"的回调，CPython 下通常及时，但循环引用要等 `gc.collect()`（因此绝不能把资源释放寄托在它上面）；确定清理用 `with` 语句加 `__enter__`/`__exit__`，或 `contextlib.contextmanager`/`contextlib.closing` 装饰器。定义 `__eq__` 而忘记 `__hash__` 会让实例不可哈希（Python 3 里 `__hash__` 被自动置为 `None`），要放进 `set`/`dict` 必须两个都定义；同理 `__hash__` 只应基于不可变字段。`__slots__` 去掉实例字典、`@dataclass(frozen=True)` 自动生成 `__init__`/`__repr__`/`__eq__`/`__hash__`，是"特殊方法最多但也最容易自动化"的体现。

📘 [Python · 数据模型（特殊方法名）](https://docs.python.org/3/reference/datamodel.html#special-method-names)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用主构造函数/次构造函数表达构造，`init` 块放校验逻辑；没有析构函数（JVM 上有 GC，需要确定性释放就用 `use {}` 或 `Closeable`）。运算符重载限定在一组固定符号上，用 `operator fun` 加 `plus`、`minus`、`times`、`get`、`set`、`invoke`、`compareTo`、`contains` 等固定函数名。特殊方法还包括 `get`/`set`/`invoke`/`componentN`/`iterator`。

```kotlin
class Box(val v: Int) : Comparable<Box> {
    init { require(v >= -1000 && v <= 1000) { "v 超出允许范围" } }   // init 块：构造期校验
    constructor() : this(0)                                // 次构造函数：委托主构造
    operator fun plus(o: Box): Box = Box(v + o.v)           // 运算符重载
    operator fun unaryMinus(): Box = Box(-v)
    operator fun get(i: Int): Int = v + i                    // 下标
    operator fun invoke(k: Int): Box = Box(v * k)             // 实例可调用
    override operator fun compareTo(o: Box): Int = v.compareTo(o.v)
    operator fun component1() = v                             // 解构声明用
    override fun toString(): String = "[$v]"
    override fun equals(o: Any?): Boolean = o is Box && o.v == v
    override fun hashCode(): Int = v
}
fun main() {
    val b = Box(3)
    println("$b ${b + Box(4)} ${-b} ${b[10]} ${b(2)}")   // [3] [7] [-3] 13 [6]
    val (x) = b                                            // 解构
    println("$x ${b == Box(3)} ${b < Box(4)}")             // 3 true true
    listOf(Box(1), Box(2)).sorted().forEach { println(it) }  // 依赖 compareTo
    java.io.File("/tmp/x").use { }                          // use：自动 close（代替析构）
}
```

`operator` 关键字是硬约束：只有 `kotlin` 预定义的那组函数名配合 `operator` 才能被编译器展开成运算符，随便起名不行，且**不能定义新的运算符**。与 Java 的互操作要点：`equals`/`hashCode`/`toString` 来自 `Any`，重写时要用 `override`；`compareTo` 实现后自动获得 `<`/`>`；`componentN` 让 `val (a, b) = obj` 可用（数据类自动生成）。`invoke` 让实例可以像函数一样调用（`b(2)`），在 DSL 与工厂里很常见——注意它会让"传对象"与"传函数"在使用上难以区分，可能影响可读性。Kotlin 没有析构函数也不该有：JVM 的 GC 不保证时机，需要确定性释放就实现 `Closeable`/`AutoCloseable` 并用 `use {}`（等价于 Java 的 try-with-resources），或者用 `Cleaner`（Java 9+）做最后的兜底。

📘 [Kotlin · 运算符重载](https://kotlinlang.org/docs/operator-overloading.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 用与类同名的构造函数表达构造，支持重载与 `this(...)`/`super(...)` 委托；Java 25 起构造函数体可以在 `super(...)` 之前写语句（JEP 513），但那段代码不能引用 `this`。析构方面 `Object.finalize` 已被废弃（Java 9 起 `@Deprecated`，Java 18 起标记 `forRemoval`），替代方案是 `try-with-resources` 配合 `AutoCloseable`，以及 `java.lang.ref.Cleaner` 做兜底。Java 没有运算符重载，没有析构函数。

```java
// 版本基线：Java 26（LTS 25）
import java.lang.ref.Cleaner;

class Box implements AutoCloseable {
    static final Cleaner CLEANER = Cleaner.create();       // 兜底清理：不保证时机
    private final int v;
    private final Cleaner.Cleanable cleanable;

    Box(int v) {
        if (v < 0) throw new IllegalArgumentException("v 必须非负");  // JEP 513 允许在委托前校验
        this.v = v;
        this.cleanable = CLEANER.register(this, () -> System.out.println("cleaner " + v));
    }
    Box() { this(0); }                                       // 构造重载 + this(...) 委托
    int v() { return v; }
    @Override public void close() { cleanable.clean(); }       // 确定性释放
    @Override public String toString() { return "[" + v + "]"; }
    @Override public boolean equals(Object o) { return o instanceof Box b && b.v == v; }
    @Override public int hashCode() { return Integer.hashCode(v); }

    public static void main(String[] args) {
        try (Box b = new Box(3)) {            // try-with-resources：自动 close
            System.out.println(b);             // [3]
        }                                      // close 在这里调用 → cleaner 3
        Box other = new Box(7);
        System.out.println(other.equals(new Box(7)));   // true
        System.gc();                            // cleaner 可能执行、也可能不执行
    }
}
```

`finalize` 被废弃的原因是它不可预测、可能让对象"复活"、拖慢 GC、异常会被吞掉；官方的替代路径是 `AutoCloseable`（确定性）+ `Cleaner`（兜底），而 `Cleaner` 注册的回调**不能捕获被清理对象本身**，否则对象永远无法回收——这是最常见的实现错误。构造函数重载要靠参数列表区分，`this(...)` 必须是构造函数里的第一条语句（JEP 513 之后允许在它之前写不触及 `this` 的语句）。`equals`/`hashCode`/`toString` 来自 `Object`，重写必须保持契约：`equals` 为真则 `hashCode` 相等；`instanceof` 模式匹配（Java 16+）让 `equals` 的写法简洁不少。Java 的 `record`（16+）会自动生成构造、访问器、`equals`、`hashCode`、`toString`，是"特殊方法自动化"的现代答案；紧凑构造器（compact constructor）可以在其中做参数校验或规范化。运算符重载在 Java 里不存在——`+` 只有数值加法与字符串拼接两种内建语义，`BigDecimal` 也只能用 `add`/`multiply` 方法。

📘 [JEP 513 · Flexible Constructor Bodies](https://openjdk.org/jeps/513)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的特殊方法种类最多：构造函数（默认、拷贝、移动、委托）、析构函数（RAII 的基石）、拷贝/移动赋值运算符、`operator+` 一类的运算符重载、`operator[]`、`operator()`、类型转换运算符、`new`/`delete`。构造顺序是"虚基类 → 基类 → 成员（按声明顺序）→ 构造函数体"，析构顺序严格相反。

```cpp
// 版本基线：C++23
#include <iostream>
#include <string>
#include <utility>

struct Box {
    int v;
    Box() : v(0) { std::cout << "默认构造\n"; }
    explicit Box(int x) : v(x) { std::cout << "int 构造 " << v << '\n'; }
    Box(const Box& o) : v(o.v) { std::cout << "拷贝构造 " << v << '\n'; }
    Box(Box&& o) noexcept : v(o.v) { o.v = -1; std::cout << "移动构造 " << v << '\n'; }
    Box& operator=(const Box&) = default;                 // 拷贝赋值
    ~Box() { std::cout << "析构 " << v << '\n'; }           // 成员按声明逆序析构
    Box operator+(const Box& o) const { return Box(v + o.v); }   // 运算符重载
    Box operator-() const { return Box(-v); }
    int operator[](int i) const { return v + i; }
    Box operator()(int k) const { return Box(v * k); }
    explicit operator bool() const { return v != 0; }        // 转换运算符
};
int main() {
    Box a{3};
    Box b = a + Box{4};             // C++17 起保证拷贝消除，这里不发生移动构造
    std::cout << b.v << ' ' << b[10] << ' ' << b(2).v << '\n';   // 7 17 int 构造 14 / 14
    std::cout << static_cast<bool>(b) << '\n';                    // 1（bool 默认打印成 1）
}                                    // 局部量与临时量逆序析构：b 先，a 后
```

典型的三法则/五法则：只要自定义了析构、拷贝构造、拷贝赋值、移动构造、移动赋值中的任何一个，其余几个通常都要一起定义（否则资源会被 double free 或泄漏）；C++11 起可以 `= default` / `= delete` 显式表达。构造函数的成员初始化列表按**声明顺序**执行，与书写顺序无关；初始化列表里能直接构造成员，比在函数体里赋值少一次赋值开销。析构函数在多态基类里必须 `virtual`，否则 `delete` 基类指针是 UB。`explicit` 阻止隐式转换（如 `Box b = 3;`），写单参构造函数时几乎总该加。移动语义需要 `noexcept` 才能在容器扩容时被使用。运算符重载有一条重要约束：至少一个操作数是用户定义类型，不能改变内建运算符的优先级与结合性，也不能重载 `::`、`.`、`.*`、`?:`、`sizeof` 等。C++ 没有自动生成的 `equals`/`hashCode`，C++20 的 `operator<=>` 与 `= default` 能自动生成全套比较。

📘 [cppreference · 构造函数](https://en.cppreference.com/w/cpp/language/constructor)

{{% /tab %}}

{{% tab header="C" %}}

C 什么都没有：没有构造函数、没有析构函数、没有运算符重载、没有魔术方法，甚至没有 RAII。构造靠 `init` 函数，析构靠 `destroy`/`free` 函数，清理顺序要靠 `goto` 集中处理（Linux 内核风格的 `goto out;`）。运算符是语言内建的、不可重载，`==` 对结构体不合法（要逐字段比较或 `memcmp`）。

```c
/* /tmp/verify/spec.c（Apple clang 21, -std=c23 实测） */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { char *name; int v; } Box;

static int box_init(Box *b, const char *name, int v) {     /* 构造函数 */
    b->name = malloc(strlen(name) + 1);
    if (!b->name) return -1;                                /* 手工错误处理 */
    strcpy(b->name, name);
    b->v = v;
    return 0;
}
static void box_destroy(Box *b) { free(b->name); b->name = NULL; }   /* 析构函数 */

static int box_equal(const Box *a, const Box *b) {          /* == 只能自己写 */
    return a->v == b->v && strcmp(a->name, b->name) == 0;
}

int main(void) {
    Box a, b;
    if (box_init(&a, "x", 3) != 0) return 1;                /* 必须检查每一步 */
    if (box_init(&b, "x", 3) != 0) { box_destroy(&a); return 1; }   /* 手工回滚 */
    printf("%d\n", box_equal(&a, &b));                       /* 1 */
    box_destroy(&b);
    box_destroy(&a);
    return 0;
}
```

在 C 里"资源管理"是一门手工技艺：每个 `malloc` 都要有对应的 `free`，中途失败必须回滚已获取的资源（`goto cleanup` 惯用法就是为此而生），任何一条提前 `return` 都可能泄漏。`memcmp` 比较结构体是不可靠的，因为填充字节（padding）的内容未定义，必须逐字段比较。C 也没有类型转换运算符与下标运算符重载，`a[i]` 只对指针/数组有意义。C23 提供了一些便利（`nullptr`、`constexpr`、二进制字面量、`typeof`），但依然没有引入类语义与 RAII。实际工程中的替代是：用宏模拟泛型容器（配合 `_Generic`）、用 `__attribute__((cleanup))`（GCC/Clang 扩展）模拟 `defer` 式的自动清理、或者写 C++ 封装再暴露 C API。

📘 [cppreference · C 内存管理](https://en.cppreference.com/w/c/memory)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的构造靠类型构造器（`T(...)`）与内部构造器/外部构造器方法，析构靠 `finalizer` 注册的回调（GC 触发，不保证时机）。运算符重载就是给 `Base.:+` 这类函数加方法，没有独立的"运算符重载"语法。`Base.show`、`Base.hash`、`Base.:(==)`、`Base.iterate`、`Base.getindex`、`Base.setindex!`、`Base.length` 是接入语言协议的钩子。

```julia
# 版本基线：Julia 1.13
struct Box
    v::Int
    function Box(v::Int)                  # 内部构造器：可以做校验与规范化
        abs(v) > 1000 && throw(ArgumentError("v 超出允许范围"))
        new(v)
    end
end
Box() = Box(0)                             # 外部构造器：便捷重载

Base.:+(a::Box, b::Box) = Box(a.v + b.v)          # 运算符重载 = 加方法
Base.:-(a::Box) = Box(-a.v)
Base.:(==)(a::Box, b::Box) = a.v == b.v
Base.hash(a::Box, h::UInt) = hash(a.v, h)          # 与 == 保持一致
Base.show(io::IO, a::Box) = print(io, "[", a.v, "]")
Base.getindex(a::Box, i::Int) = a.v + i             # 下标：a[i]
Base.length(a::Box) = a.v
Base.iterate(a::Box, s = 0) = s >= a.v ? nothing : (s, s + 1)   # 可迭代

b = Box(3)
println(b, " ", b + Box(4), " ", -b, " ", b[10], " ", length(b))   # [3] [7] [-3] 13 3
println(b == Box(3), " ", 1 in collect(b))                          # true true

holder = Ref{Any}(b)
finalizer(holder) do x                              # 终结器：GC 时可能调用
    println("finalizer 触发")
end
holder[] = nothing
GC.gc()
println("主流程结束")
```

`new` 只能在内部构造器里调用，它负责设置不可变字段；外部构造器（定义在 `struct` 外的同名方法）负责便捷签名与转换，两者都是**方法**，因此可以被分派——这与 Java 的"构造函数不能是虚的"形成对比。自定义 `==` 必须同时自定义 `hash`，否则 `Dict`/`Set` 行为不一致（Julia 的哈希契约与 Python 相同）。`show(io, x)` 是打印协议的正规入口，`print` 与 `println` 最终都会调到它；只定义 `show(io, x)` 就能让 REPL 与 `string(x)` 都正确工作，不要用 `Base.show(x)`（那是旧签名）。`getindex`/`setindex!`/`iterate`/`length` 让自定义类型获得下标、迭代、`in` 等语法能力。`finalizer` 注册在某个对象上，触发时机由 GC 决定，只适合做兜底；确定性清理要用 `do` 块配合 `try/finally`（`open(f, path) do io` 这种形式就是标准模式）。

📘 [Julia · 构造器](https://docs.julialang.org/en/v1/manual/constructors/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的构造函数与类同名，支持 `this(...)` 委托、静态构造函数、终结器（`~ClassName`，即 `Finalize` 重写）；析构的正统做法是实现 `IDisposable` 并配合 `using`/`await using`，终结器只用于兜底非托管资源。运算符重载用 `operator` 关键字，`implicit`/`explicit` 定义类型转换，`Dispose` 与终结器之间用 `GC.SuppressFinalize` 协调。

```csharp
// 版本基线：C# 14 / .NET 10
using System;

public sealed class Box : IDisposable
{
    private readonly int v;
    private bool disposed;

    public Box(int v)
    {
        if (v < 0) throw new ArgumentOutOfRangeException(nameof(v));
        this.v = v;
    }
    public Box() : this(0) { }                    // this(...) 委托
    static Box() { Console.WriteLine("静态构造只跑一次"); }   // 静态构造函数
    ~Box() => Console.WriteLine($"终结器 {v}");    // 终结器：GC 时机，不保证

    public int V => v;
    public void Dispose()                          // IDisposable：确定性清理
    {
        if (disposed) return;
        disposed = true;
        GC.SuppressFinalize(this);                  // 已显式清理，不必再跑终结器
        Console.WriteLine($"Dispose {v}");
    }

    public static Box operator +(Box a, Box b) => new(a.v + b.v);   // 运算符重载
    public static Box operator -(Box a) => new(-a.v);
    public static implicit operator int(Box b) => b.v;               // 隐式转换
    public static explicit operator Box(int v) => new(v);             // 显式转换
    public override string ToString() => $"[{v}]";
    public override bool Equals(object? o) => o is Box b && b.v == v;
    public override int GetHashCode() => v.GetHashCode();
}

public class Program
{
    public static void Main()
    {
        using (var b = new Box(3))                  // using：离开作用域自动 Dispose
        {
            Box sum = b + new Box(4);
            int n = sum;                             // 隐式转换
            Console.WriteLine($"{b} {sum} {n}");        // [3] [7] 7（n 由隐式转换得到）
        }
        var box = new Box(1);
        Console.WriteLine(box.Equals(new Box(1)));     // true
        Console.WriteLine(box == new Box(1));          // false：没有重载 operator ==，走引用比较
    }
}
```

清理的完整模式是"实现 `IDisposable`，`Dispose` 里释放托管与非托管资源、调用 `GC.SuppressFinalize`，终结器只作为兜底"；如果类型不持有非托管资源就不要写终结器（有终结器的对象会多活一轮 GC，成本明显）。`Dispose` 应该幂等（重复调用无副作用），`using` 与 C# 8 的 `using` 声明（`using var x = ...;`）都会自动调用它；`IAsyncDisposable` 与 `await using` 处理异步释放。运算符重载的规则与 C++ 类似但更严格：`operator ==` 一旦重载就必须与 `Equals`/`GetHashCode` 保持一致（编译器会给出警告），而且 C# 不会自动把 `==` 接到 `Equals` 上——类不重载 `operator ==` 时 `==` 仍然是引用比较，只有 `record` 会自动合成 `==`/`Equals`/`GetHashCode`。此外 `&&`/`||` 必须先重载 `true`/`false` 才能重载，`[]` 不能作为运算符重载（要用索引器 `this[int]`），复合赋值由 `+` 自动派生。`implicit` 转换要克制使用（可能引入难以发现的隐式行为），跨类型转换优先用 `explicit` 或工厂方法。`record` 类型自动生成 `Equals`/`GetHashCode`/`ToString`/`with` 表达式所需的一切，是"特殊方法自动化"的首选。

📘 [MS Learn · 运算符重载](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/operator-overloading)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 用命名构造函数（`ClassName.name(...)`）与工厂构造函数（`factory`）表达构造，`initializer list` 在构造函数体之前初始化字段；没有析构函数，替代是 `Finalizer`（GC 时机不保证）与显式 `close()`/`dispose()`。运算符重载通过声明 `operator +` 等成员完成，可重载的运算符集合由语言固定。

```dart
// 版本基线：Dart 3.13
class Box {
  static final Finalizer<Box> _fin = Finalizer<Box>((b) => print('finalizer ${b.v}'));

  final int v;
  Box(this.v) : assert(v >= -1000 && v <= 1000, 'v 超出允许范围') {   // 初始化列表 + 构造体
    _fin.attach(this, this);                      // 注册终结器（GC 时机）
  }
  Box.zero() : this(0);                            // 命名构造函数
  factory Box.fromString(String s) => Box(int.parse(s));   // 工厂构造函数
  Box._raw(this.v);                                // 私有命名构造

  Box operator +(Box o) => Box(v + o.v);           // 运算符重载
  Box operator -() => Box(-v);                      // 一元减
  int operator [](int i) => v + i;                  // 下标
  Box call(int k) => Box(v * k);                    // 实例可调用
  @override String toString() => '[$v]';
  @override bool operator ==(Object o) => o is Box && o.v == v;
  @override int get hashCode => v.hashCode;
  void dispose() => print('dispose $v');             // 显式清理
}

void main() {
  final b = Box(3);
  print('$b ${b + Box(4)} ${-b} ${b[10]} ${b(2)}');  // [3] [7] [-3] 13 [6]
  print('${b == Box(3)} ${Box.fromString('7')}');     // true [7]
  b.dispose();                                        // 确定性清理要自己调
  Box.zero();                                          // finalizer 不保证触发
}
```

`operator` 可重载的集合是固定的：`+`、`-`、`*`、`/`、`~/`、`%`、`&`、`|`、`^`、`~`、`<<`、`>>`、`>>>`、`[]`、`[]=`、`<`、`>`、`<=`、`>=`、`==`、`unary-`；`==` 与 `hashCode` 必须一起重写（重写 `==` 而不重写 `hashCode` 会破坏 `HashMap`），且 `==` 必须是 `bool operator ==(Object other)` 签名。`factory` 构造函数可以有返回值、可以做缓存或返回子类型（这正是 `const` 构造与单例的实现手段），普通构造函数不能 `return`。初始化列表（`:` 之后的部分）在构造体之前执行，可用来给 `final` 字段赋值、调用 `super` 与写 `assert`；`late final` 字段可以延后到构造体里赋值。`Finalizer` 附着在对象上，回调不能捕获该对象（否则永不回收），且只在 GC 时触发——Dart 没有 `deinit`，需要确定性释放的场景要自己设计 `dispose()` 并配合 `try/finally`。`extension type` 也能声明成员与运算符，是给现有类型加"运算符视图"的轻量手段。

📘 [Dart · 运算符重载（类成员）](https://dart.dev/language/methods#operators)

{{% /tab %}}

{{% tab header="R" %}}

R 用函数当构造函数（`structure`、`new`、或者自定义 `T <- function(...)`），没有析构函数，但有 `reg.finalizer` 注册的终结器（在 GC 时调用）。魔术方法表现为泛型函数的方法名：`print`/`format`/`as.character`/`length`/`[`/`[[`/`$`/`Ops`/`Summary`/`Math`/`str` 等等，都是可以按 class 注册的泛型。S4/R5 系统还提供 `initialize`、`show`、`validity` 等专门的钩子。

```r
# 版本基线：R 4.6
Counter <- function(n) structure(list(n = n), class = "Counter")   # 构造函数就是函数
print.Counter <- function(x, ...) cat("Counter(", x$n, ")\n", sep = "")   # print 方法
format.Counter <- function(x, ...) paste0("Counter(", x$n, ")")
length.Counter <- function(x) x$n                                   # length() 钩子
`[.Counter` <- function(x, i) x$n + i                                # 下标钩子
Ops.Counter <- function(e1, e2) {                                    # 组泛型：一次覆盖多个运算符
  a <- if (inherits(e1, "Counter")) e1$n else e1
  b <- if (inherits(e2, "Counter")) e2$n else e2
  switch(.Generic, "+" = Counter(a + b), "-" = Counter(a - b), "*" = Counter(a * b),
         stop("不支持的运算符: ", .Generic))
}
c1 <- Counter(3)
print(c1)                                    # Counter(3)
cat(format(c1), "\n")                         # Counter(3)
cat(length(c1), c1[10], (c1 + Counter(4))$n, "\n")   # 3 13 7

e <- new.env()                                # 终结器注册在环境上
reg.finalizer(e, function(env) cat("finalizer 触发\n"), onexit = TRUE)
rm(e); gc()                                    # 触发时机由 GC 决定

# S4 的钩子：initialize / show / validity
setClass("P", representation(x = "numeric"),
         validity = function(object) if (object@x < 0) "x 必须非负" else TRUE)
setMethod("initialize", "P", function(.Object, x = 0) { .Object@x <- x; validObject(.Object); .Object })
setMethod("show", "P", function(object) cat("P(", object@x, ")\n", sep = ""))
show(new("P", x = 2))                          # P(2)
cat(isVirtualClass("P"), "\n")                  # FALSE
```

R 的"构造函数"是普通函数，S3 里通常用 `structure(list(...), class = "...")` 打类标签，S4 用 `new("Class", ...)` 并会调用 `initialize` 方法，R6 用 `ClassName$new(...)`。`Ops` 是组泛型（group generic），定义 `Ops.Counter` 就同时接管 `+`、`-`、`*`、`/`、`^`、`%%`、`%/%`、`==`、`!=`、`<`、`>`、`<=`、`>=` 十三个运算符，用 `.Generic` 变量区分当前是哪一个；同类的组泛型还有 `Math`、`Summary`、`Complex`。`reg.finalizer` 可以注册在环境、外部指针或 S4 对象上，`onexit = TRUE` 表示 R 退出时也调用，但时机完全由 GC 决定，不能用于释放关键资源；文件与连接要用 `on.exit(close(con))` 或 `withr::defer`。S4 的 `validity` 函数与 `validObject()` 提供对象完整性检查，`setValidity` 可以后加，这是 S4 相对 S3 的主要优势之一。

📘 [R · 组泛型 Ops](https://stat.ethz.ch/R-manual/R-devel/library/base/html/groupGeneric.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有构造函数、析构函数、运算符重载与魔术方法：`init` 只是社区惯例的函数名，清理要用 `deinit` 手工调用（`defer x.deinit()` 是标准写法），格式化输出靠 `format` 方法。运算符是内建的、不可重载，`==` 对结构体逐字段比较（`std.meta.eql` 提供通用值比较）。

```zig
// 版本基线：Zig 0.15
const std = @import("std");

const Box = struct {
    v: i32,
    pub fn init(v: i32) Box { return .{ .v = v }; }          // 惯例：init 当构造函数
    pub fn add(self: Box, o: Box) Box { return .{ .v = self.v + o.v }; }   // 没有运算符重载
    pub fn eql(self: Box, o: Box) bool { return self.v == o.v; }
    pub fn format(self: Box, writer: *std.Io.Writer) std.Io.Writer.Error!void {   // 格式化钩子
        try writer.print("[{d}]", .{self.v});
    }
};

const Buffer = struct {
    alloc: std.mem.Allocator,
    data: []u8,
    pub fn init(alloc: std.mem.Allocator, n: usize) !Buffer {
        return .{ .alloc = alloc, .data = try alloc.alloc(u8, n) };
    }
    pub fn deinit(self: *Buffer) void {                      // 惯例：deinit 当析构函数
        self.alloc.free(self.data);
    }
};

pub fn main() !void {
    const a = Box.init(3);
    const b = Box.init(4);
    std.debug.print("{f} {f} {}\n", .{ a, a.add(b), a.eql(Box.init(3)) });   // [3] [7] true

    var buf = try Buffer.init(std.heap.page_allocator, 8);
    defer buf.deinit();                       // 作用域退出时释放（编译器保证）
    buf.data[0] = 'x';
    std.debug.print("{c} {d}\n", .{ buf.data[0], buf.data.len });          // x 8
}
```

Zig 把 RAII 拆成了两半：`defer` 提供确定性的执行时机，但释放动作必须你自己写（`deinit`），编译器不会自动调用它——忘记 `defer buf.deinit()` 就是内存泄漏，测试时可用 `std.testing.allocator` 的 `checkAlloc` 抓住。`init`/`deinit` 只是命名惯例，语言不识别；因为没有构造/析构魔法，Zig 的类型可以安全地按值拷贝（没有隐藏的复制钩子），需要"移动语义"时用 `*T` 显式表达。没有运算符重载意味着 `+` 永远只对数值/向量有效，自定义类型只能用命名函数（`a.add(b)`）；`==` 对结构体做逐字段比较（包含数组与嵌套结构体），但对含指针的字段比较的是地址，需要值比较就用 `std.meta.eql`。`format` 方法（签名 `fn format(self, writer: *std.Io.Writer)`）让类型能被 `{f}` 打印，这是 Zig 里唯一接近"魔术方法"的东西；0.15 起 `{}` 遇到带 `format` 方法的类型会报 ambiguous 编译错误，必须写成 `{f}`（想跳过自定义格式则写 `{any}`）。

📘 [Zig · defer 与错误处理](https://ziglang.org/documentation/master/#defer)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的构造就是普通函数（惯例 `new`），析构靠元方法 `__gc`（在 GC 回收带元表的对象时调用，需要先 `setmetatable`）、`__close`（`<close>` 变量离开作用域时调用，用于确定清理）。运算符重载全部通过元方法完成，字符串化用 `__tostring`，可调用用 `__call`，下标读写用 `__index`/`__newindex`。魔术方法的名字必须精确匹配。

```lua
-- 版本基线：Lua 5.5
local Box = {}
Box.__index = Box
function Box.new(v)                                   -- 构造函数（惯例命名）
  return setmetatable({ v = v }, Box)
end
Box.__tostring = function(self) return "[" .. self.v .. "]" end   -- 字符串化
Box.__add = function(a, b) return Box.new(a.v + b.v) end           -- 运算符重载
Box.__unm = function(a) return Box.new(-a.v) end                    -- 一元负
Box.__eq = function(a, b) return a.v == b.v end                      -- == （同类型才调用）
Box.__lt = function(a, b) return a.v < b.v end                        -- <
Box.__index = function(self, k) return Box[k] or ("缺失 " .. k) end   -- 动态兜底
function Box:__call(k) return Box.new(self.v * k) end                  -- 实例可调用
Box.__gc = function(self) print("gc " .. self.v) end                    -- 终结器
Box.__close = function(self, err) print("close " .. self.v) end          -- <close>

local a, b = Box.new(3), Box.new(4)
print(tostring(a), tostring(a + b), tostring(-a))   -- [3] [7] [-3]
print(a == Box.new(3), a < b)                        -- true true
print(a.whatever)                                     -- 缺失 whatever
print(tostring(a(2)))                                 -- [6]

do
  local r <close> = Box.new(9)                        -- 离开作用域自动 __close
  print("块内", tostring(r))                           -- 块内 [9]
end
collectgarbage()                                      -- 触发 __gc（不保证顺序）
```

`__eq` 只在两个操作数都是表且元方法相同时才调用（Lua 5.5 的规则），比较数字与自定义类型不会走它；`__lt`/`__le` 是关系运算符的入口；Lua 5.4 起已经移除了「用 `__lt` 模拟 `__le`」的回退，缺 `__le` 时 `<=` 会直接报错，所以两个都要写。`__index` 既是继承链也是动态属性兜底的机制，写成函数时要注意性能与递归；`__newindex` 只在键不存在时触发（存在则直接赋值，除非用 `rawset`）。`__gc` 在 Lua 5.5 里需要对象在 `setmetatable` 时就带有该元方法（表在之后才设置元方法会不生效），且回收顺序不确定；`<close>` 变量（5.4+）提供确定性的清理，比 `__gc` 可靠得多，`__close` 会收到错误对象作为第二个参数，可在其中判断是否异常退出。`__call` 让表可以像函数一样调用，这是 Lua 里实现"可调用对象"的唯一方式，注意它与普通方法调用的可读性差异。

📘 [Lua 5.5 · 元方法](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的特殊方法与 JavaScript 相同（构造、`toString`、`Symbol.toPrimitive` 等），类型系统额外提供了参数属性、`readonly` 字段、`abstract` 构造签名以及 `override` 检查。没有运算符重载、没有析构函数；资源清理用显式方法或 `Symbol.dispose`（Explicit Resource Management，配合 `using`）。类型层面可以给内置符号方法补声明。

```typescript
// 版本基线：TypeScript 7
class Vec {
  constructor(public x: number, public y: number) {}   // 参数属性：自动声明 + 赋值
  static readonly zero = new Vec(0, 0);
  add(o: Vec): Vec { return new Vec(this.x + o.x, this.y + o.y); }   // 没有 + 重载
  toString(): string { return `Vec(${this.x},${this.y})`; }
  [Symbol.toPrimitive](hint: string): number | string {               // 符号方法
    return hint === 'string' ? this.toString() : this.x + this.y;
  }
  static from(v: { x: number; y: number }): Vec { return new Vec(v.x, v.y); }
}
abstract class Shape {                                  // 抽象类
  abstract area(): number;
  constructor(public readonly name: string) {}           // 只读字段
}
class Circle extends Shape {
  constructor(public r: number) { super('circle'); }
  override area(): number { return 3.141592653589793 * this.r ** 2; }
}
const v = new Vec(1, 2);
console.log(String(v), Number(v));                         // Vec(1,2) 3
console.log(v.add(new Vec(3, 4)).toString());              // Vec(4,6)
const c: Shape = new Circle(1);
console.log(c.name, c.area());                              // circle 3.141592653589793

class Res implements Disposable {                           // 显式资源管理（TS 5.2+ 类型）
  constructor(public id: number) {}
  [Symbol.dispose](): void { console.log('dispose', this.id); }
}
{
  const r = new Res(1);
  r[Symbol.dispose]();                                      // 显式调用
}
```

参数属性（`constructor(public x: number)`）是 TypeScript 独有的语法糖：它同时声明字段、声明构造参数、生成赋值语句；加上 `readonly` 就是不可变字段，但要注意它只在编译期约束，运行时的 `#private` 才是真正隔离。`abstract` 成员只能在抽象类里声明，子类必须实现，编译器会检查；`override` 关键字与 `noImplicitOverride` 一起用能拦住"想重写却写错签名"的情况。类型层面没有运算符重载，但可以通过声明合并给内置符号补类型（如 `Object.prototype.toString`），运行时行为仍要自己实现。`Symbol.dispose` 与 `using`（TS 5.2+ / ES2026）让"离开作用域自动清理"成为语言能力，编译目标不支持时需要 polyfill；在它可用之前，惯例是显式 `close()`/`dispose()` 加 `try/finally`。构造重载在 TS 里靠重载签名表达（多个 `constructor(...)` 声明 + 一个实现），与方法的处理方式一致。

📘 [TypeScript · 类（参数属性与 abstract）](https://www.typescriptlang.org/docs/handbook/2/classes.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的构造是 `constructor` 方法（每个类只能有一个，不能重载），`new.target` 可以检测是否被 `new` 调用；没有析构函数，唯一的回收信号是 `FinalizationRegistry`（弱回调、不保证执行）。符号方法（`Symbol.toPrimitive`、`Symbol.hasInstance`、`Symbol.iterator`、`Symbol.toStringTag`、`Symbol.dispose`）是 JS 里最接近"魔术方法"的机制，运算符重载不存在——只能通过 `valueOf`/`toString`/`Symbol.toPrimitive` 影响转换行为，不能定义新的运算符。

```javascript
// /tmp/verify/final.js（node 24.20.0 实测；文档按 Node 26 写）
class Box {
  constructor(v) { this.v = v; }             // constructor：唯一构造函数
  toString() { return `[${this.v}]`; }        // 字符串化
  valueOf() { return this.v; }                // 数值化
  [Symbol.toPrimitive](hint) { return hint === 'string' ? `S${this.v}` : this.v; }  // 优先级最高
  static [Symbol.hasInstance](x) { return typeof x === 'object' && 'v' in x; }       // instanceof 钩子
  get [Symbol.toStringTag]() { return 'BoxTag'; }
}
const b = new Box(3);
console.log(`${b}`, b + 1, Object.prototype.toString.call(b));   // S3 4 [object BoxTag]
console.log(b instanceof Box, {v: 9} instanceof Box);              // true true

const registry = new FinalizationRegistry((held) => console.log('回收', held));
let tmp = { name: 'tmp' };
registry.register(tmp, 'tmp 的标记');      // 注册时必须持有强引用
tmp = null;                                 // 解除强引用≠立即回收

class Res {
  constructor(n) { this.n = n; }
  [Symbol.dispose]() { console.log('dispose', this.n); }   // 显式资源管理钩子
}
{
  const r = new Res(1);
  r[Symbol.dispose]();                      // 显式调用；`using r = ...` 可自动调用
}
```

`Symbol.toPrimitive` 的优先级高于 `valueOf` 与 `toString`，`hint` 取 `"number"`、`"string"`、`"default"`（`+` 与 `==` 是 `"default"`）；没有它时 `+` 走 `valueOf` 再 `toString`，因此 `box + 1` 与 `` `${box}` `` 可能得到完全不同的结果。`Symbol.hasInstance` 重载 `instanceof` 会让所有 `x instanceof Box` 都走你的逻辑，跨 Realm/iframe 时很有用，但也会让人困惑。`FinalizationRegistry` 的回调运行在微任务里、时机不确定，注册的"持有值"不能引用被观察对象本身，否则永不回收——它只能做兜底，不能当析构函数。`Symbol.dispose` 与 `using`（Explicit Resource Management）提供确定性的清理，是目前最接近 RAII 的机制，但需要运行时/转译支持。JS 没有运算符重载：数值、字符串、BigInt 的运算符语义固定，只能靠 `Symbol.toPrimitive` 影响"对象怎么变成原始值"。`constructor` 若返回一个对象会替换 `new` 的结果（返回原始值则忽略），这是 `new.target` 之外另一个容易被遗忘的规则。

📘 [MDN · Symbol.toPrimitive](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Symbol/toPrimitive)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 `__construct` 表达构造、`__destruct` 表达析构（在引用计数归零或脚本结束时调用，顺序不保证），`__get`/`__set`/`__isset`/`__unset`/`__call`/`__callStatic`/`__toString`/`__invoke`/`__clone`/`__serialize`/`__unserialize`/`__debugInfo` 是完整的魔术方法清单。PHP 没有运算符重载，唯一例外是枚举（enum）可以实现接口，但 `+`/`==` 不能被自定义。

```php
// 版本基线：PHP 8.5
class Box
{
    private array $data = [];
    public function __construct(private readonly int $v) {}      // 构造器属性提升
    public function __destruct() { echo "析构 {$this->v}", PHP_EOL; }
    public function __get(string $n): mixed {                     // 未定义属性读取
        return $this->data[$n] ?? "虚拟 $n";
    }
    public function __set(string $n, mixed $val): void { $this->data[$n] = $val; }
    public function __isset(string $n): bool { return isset($this->data[$n]); }
    public function __call(string $n, array $a): string { return "调用 $n(" . count($a) . ")"; }
    public static function __callStatic(string $n, array $a): string { return "静态 $n"; }
    public function __toString(): string { return "[{$this->v}]"; }
    public function __invoke(int $k): self { return new self($this->v * $k); }
    public function __clone() { echo "克隆", PHP_EOL; }             // 深拷贝钩子
    public function __debugInfo(): array { return ['v' => $this->v]; }
}

$b = new Box(3);
echo $b, PHP_EOL;                       // [3]
echo $b->extra, PHP_EOL;                 // 虚拟 extra（__get）
$b->x = 1;
var_dump(isset($b->x));                   // bool(true)
echo $b->whatever(1, 2), PHP_EOL;          // 调用 whatever(2)
echo Box::nope(), PHP_EOL;                  // 静态 nope
echo $b(2), PHP_EOL;                         // [6]（__invoke）
$c = clone $b;                                // 克隆
print_r($c);                                   // __debugInfo
unset($b);                                      // 引用归零 → 析构 3
```

魔术方法的名字必须以双下划线开头且拼写精确（`__to_string`、`__contruct` 这类拼写错误不会报警告，只会静默地不生效）；PHP 8 起还会检查魔术方法的签名，参数与返回类型必须与官方约定的列表兼容，写错会直接报错。`__get`/`__set` 只在属性不可访问（未定义或私有）时触发，因此它们与 `readonly`、类型声明、属性钩子（8.4+）会互相影响：如果属性声明了类型且已有钩子，`__get` 不会再被调用。`__destruct` 在循环引用中依赖 GC（PHP 有专门的循环收集器），脚本结束时析构顺序不确定，所以数据库连接、文件句柄这类资源应该显式 `close()` 或用 `try/finally`。`__clone` 是对象复制的钩子（浅拷贝后调用），深拷贝必须在其中手工复制引用字段；`__serialize`/`__unserialize`（7.4+）取代了 `__sleep`/`__wakeup`，与 `__debugInfo`、`__toString`、`__invoke` 一起构成"魔术方法全家桶"。PHP 没有运算符重载：`+` 只对数组做并集、对数字做加法，自定义类型必须用方法（`$a->plus($b)`）。

📘 [PHP · 魔术方法](https://www.php.net/manual/en/language.oop5.magic.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 `initialize` 作构造钩子（`new` 负责分配再调用它），没有析构函数，但可以 `ObjectSpace.define_finalizer` 注册终结器（GC 时机不保证）。魔术方法体系集中在 `method_missing`、`respond_to_missing?`、`to_s`、`inspect`、`==`、`eql?`、`hash`、`<=>`、`coerce`、`[]`、`call`、`to_proc`、`each`。运算符就是方法，因此重载运算符与定义普通方法没有区别。

```ruby
# /tmp/verify/final.rb（ruby 4.0.6 实测）
class Box
  include Comparable                  # 由 <=> 免费获得 < <= > >= == between?
  attr_reader :v
  def initialize(v) = @v = v          # 构造钩子
  def to_s = "[#{@v}]"                 # 面向用户
  def inspect = "Box(#{@v})"            # 调试表示
  def <=>(o) = v <=> o.v                # 定义它 + Comparable 就有全部比较
  def ==(o) = o.is_a?(Box) && v == o.v
  def eql?(o) = self == o
  def hash = v.hash
  def coerce(o) = [Box.new(o), self]     # 让 2 + box 也能工作
  def +(o)
    Box.new(v + (o.is_a?(Box) ? o.v : o))
  end
  def [](i) = v + i                     # 索引
  def call(k) = Box.new(v * k)           # 实例可调用
end
b = Box.new(3)
puts "#{b} #{b.inspect} #{b + 2} #{2 + b} #{b[10]} #{b.(2)}"   # [3] Box(3) [5] [5] 13 [6]
puts [b < Box.new(4), b == Box.new(3), b.between?(Box.new(1), Box.new(4))].inspect
puts({ Box.new(1) => "a" }[Box.new(1)])   # a（hash + eql? 生效）
finalized = []
ObjectSpace.define_finalizer(b, proc { |id| finalized << id })
b = nil
GC.start
puts "终结器触发次数：#{finalized.size}"     # 1（不保证及时）
```

`coerce` 是 Ruby 让"字面量在左边"也能工作的钩子：`2 + box` 先尝试 `Integer#+`，失败后调用 `box.coerce(2)` 得到 `[Box.new(2), box]`，再执行 `Box.new(2) + box`——所有数值类型（`Integer`、`Float`、`Rational`、`Complex`）都遵守这个协议，自定义数值类型应实现它。`Comparable` 由 `<=>` 派生全部比较运算符，`Enumerable` 由 `each` 派生出 `map`/`select`/`include?` 等几十个方法，这是 Ruby 模块混入最典型的用法。`hash` 与 `eql?` 必须一起重写才能正确用于 `Hash`/`Set`（`==` 用于比较，`eql?` 用于哈希查找，两者语义可以不同但通常保持一致）。`ObjectSpace.define_finalizer` 的回调**不能捕获被终结的对象本身**（否则对象永不回收），且终结器只在 GC 时跑，不能用于释放文件句柄——确定性清理用块方法与 `ensure`（`File.open(path) { |f| ... }`）。`define_method` 生成的动态方法优于 `method_missing`，后者要配 `respond_to_missing?` 并会拖慢所有未命中的方法查找。

📘 [Ruby · ObjectSpace](https://docs.ruby-lang.org/en/master/ObjectSpace.html)

{{% /tab %}}

{{< /tabpane >}}
