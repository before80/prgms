+++
title = "accessCtrl"
date = 2026-09-19T12:00:00+08:00
weight = 17
type = "docs"
description = "18 种语言的访问控制对照：可见性修饰符、模块与文件级封装、约定式私有、封装与反射的边界"
isCJKLanguage = true
draft = false
+++

# 访问控制：18 种语言对照

访问控制这件事，各语言的分歧点在四个层面依次展开：**第一个层面是类或类型的成员修饰符**（`public`/`private`/`protected` 这一套到底有几个、默认是哪一级）；**第二个层面是模块与文件的边界**（封装单位是类、是文件、是包、还是 crate，边界不同则同一个关键字含义完全不同）；**第三个层面是没有强制机制时怎么表达私有**（下划线约定、名称改写、闭包）；**第四个层面是这些边界能不能被反射和内存操作绕过去**。这四个层面构成本页的四个子主题，每个子主题一套 18 语言标签页。最根本的分歧可以归纳成一句话：有的语言把可见性当成**编译期契约**，编译通过、运行时想怎么看就怎么看（TypeScript、C++、Java 的 `private` 都在此列）；有的语言把它当成**运行时的真边界**，语言层面根本不提供通向内部的路径（JavaScript 的 `#`、Rust 的 `mod` 私有、Dart 的库级下划线、Lua 的闭包 upvalue）；还有一批语言**压根不做强制**，只留下划线这类命名约定（Python、R、Julia、Lua 的表字段）。本页反复回到的核心区分就是「真私有」与「编译期私有」，请读者在每个子主题里都拿这把尺子去量一遍。

## 访问控制

**一页速览**

| 语言 | 有没有 / 关键字写法 | 一句话说明 / 关键差异 | 关键陷阱 |
| --- | --- | --- | --- |
| Rust | 有，`pub`、`pub(crate)`、`pub(super)`、`pub(in path)`、`pub(self)` | 默认全私有，可见性沿 `mod` 树按「祖先后代」规则判定，是编译期硬约束 | 父模块私有不等于子模块可见；路径链上任何一环私有，下游全都进不去 |
| Swift | 有，`open`、`public`、`package`、`internal`、`fileprivate`、`private` | 默认 `internal`（模块内），`private` 在同文件的扩展里仍然可见 | `package`（5.9 起）必须由构建系统传 `-package-name`，否则直接编译报错 |
| Go | 只有导出/未导出，靠标识符首字母大小写 | 封装单位是 package，大写导出、小写包内，运行时无法突破 | `internal` 目录是构建工具的约定，不是语言规则；reflect 读不到小写字段的值 |
| Python | 没有强制机制，`_` 与 `__` 是约定加名称改写 | 运行时一切皆可访问，`__name` 只是被改写成 `_类名__name` | `__all__` 只管 `from m import *`；`@final` 与 `Final` 只对类型检查器生效 |
| Kotlin | 有，`public`、`private`、`protected`、`internal` | 默认 `public`；`internal` 以「模块」为界（一个 Gradle/Maven 模块或一次编译调用） | 顶层声明不能用 `protected`；`internal` 编译后在 JVM 字节码里名字仍在，Java 能直接调 |
| Java | 有，`public`、`protected`、`private`，以及不加修饰符的包私有 | 包私有（package-private）是默认；JPMS 再叠一层 `exports` / `opens` | 模块系统只对具名模块生效；`setAccessible` 在 JDK 17 后对 JDK 内部默认被拒 |
| C++ | 有，`public`、`protected`、`private`，另有 `friend` | `class` 默认 `private`、`struct` 默认 `public`，全部是编译期检查 | `#define private public` 能骗过编译器但破坏 ODR；`friend` 让封装出现正式缺口 |
| C | 没有访问修饰符 | 靠 `static` 给内部链接、头文件只放不完整类型、命名加 `_` 前缀 | 有完整类型定义就能改结构体任何字段；`const` 只是编译期约束不是内存保护 |
| Julia | 没有访问修饰符，有 `export` 与 `public` | 限定名 `M.x` 永远可访问，模块系统不做隐藏；`public`（1.11 起）只是 API 声明 | `export` 只影响 `using` 带进来的名字；`public` 完全没有命名空间效果 |
| C# | 有，`public`、`private`、`protected`、`internal`、`protected internal`、`private protected`，以及 `file`（C# 11） | 顶层类型默认 `internal`、成员默认 `private`；`file` 把类型限制在单个源文件 | `file` 不能与任何访问修饰符组合，也不能出现在非 file 类型的签名里；类型默认是 `internal` 而非 `public` |
| Dart | 有，下划线 `_` 前缀，作用域是 library | 库级私有：`_x` 在同一个 library（含 `part` 文件）内可见，跨库不可见 | 一个文件默认就是一个 library，加了 `part` 后整个 part 组共享私有成员 |
| R | 没有强制机制，靠 NAMESPACE 与 `.` 前缀约定 | 包的导出面由 `NAMESPACE` 的 `export` 决定，`pkg::name` 只取导出名 | 内部名字用 `pkg:::name` 一律能拿到；`assignInNamespace` 还能直接改包内绑定 |
| Zig | 有，`pub`，其余一律文件内私有 | 文件即容器（文件就是一个 struct），`pub` 决定能否被别的文件看见 | 结构体字段永远「公开」；访问控制是 comptime 检查，但没有任何运行时反射能绕过它 |
| Lua | 没有访问修饰符 | 模块就是返回一个 table；真私有只能靠闭包 upvalue，`_` 前缀只是约定 | `debug.getupvalue` / `debug.getlocal` 能把闭包里的私有量翻出来 |
| TypeScript | 有，`public`、`private`、`protected`、`readonly`，另有 ECMAScript 的 `#` | 修饰符编译期擦除、运行时不存在；`#` 是真正的运行时私有 | `private` 字段在 JS 侧照样能读写；`@internal` 需要 `stripInternal` 才从 `.d.ts` 消失 |
| JavaScript | 有，`#` 私有字段/方法（ES2022），`static {}` 静态块 | `#` 是真私有，类外连语法上都无法引用；闭包与 WeakMap 是更老的真私有方案 | `#` 不是属性名，`this["#x"]`、`Object.keys`、`JSON.stringify` 全都拿不到它 |
| PHP | 有，`public`、`protected`、`private`，8.4 起 `private(set)` 非对称可见性 | 运行时强制、同类实例之间也互相可访问；属性钩子（8.4）让访存逻辑可拦截 | 8.1 起 `ReflectionProperty::setAccessible()` 已无效果；`private(set)` 属性自动 `final` |
| Ruby | 有，`public`、`protected`、`private`，另有 `private_class_method`、`private_constant` | `private` 只禁止显式 receiver 调用，实例变量天生私有 | `send` 能调用私有方法；`private` 对常量与类方法无效，要用专门的方法 |

### 可见性修饰符

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的可见性是一个**编译期硬约束**，而且默认方向是「全私有」：不加 `pub` 的东西只有定义它的模块及其后代能用。修饰符一共五个写法，`pub` 之外都带限定范围，`pub(in path)` 里的 `path` 必须从 `crate`、`self` 或 `super` 开头（2018 edition 之后的规则），并且每一段都必须直接指向模块、不能是 `use` 引进来的名字。

```rust
mod outer {
    pub mod inner {
        pub(in crate::outer) fn outer_visible() {}
        pub(crate) fn crate_visible() {}     // 整个 crate
        pub(super) fn super_visible() {}     // 父模块 outer
        pub(self) fn self_visible() {}       // 等价于不加 pub
        pub fn all_visible() {}
    }
    pub fn call() {
        inner::outer_visible();              // ✅
        inner::crate_visible();              // ✅
        inner::super_visible();              // ✅
        // inner::self_visible();            // 🛑 E0603: function `self_visible` is private
    }
}
fn main() {
    outer::inner::crate_visible();           // ✅ 同 crate 可见
    outer::inner::all_visible();             // ✅
    outer::call();                           // ✅
    println!("ok");                          // ok
}
```

真正的重头戏是「私有的字段 + 公有的访问器」这个组合：`Engine` 结构体的 `rpm` 字段在模块外既读不到也写不到，连 `e.rpm` 这种写法都会直接编译失败，只有模块自己的后代（含 `#[cfg(test)] mod tests`）能碰。也就是说 Rust 的单元测试天然能测试私有实现，不需要 `InternalsVisibleTo` 或 `@testable` 这类额外机制。`pub(crate)` 是把可见性放宽到整棵 crate 树，`pub(super)` 放宽到父模块——它们都只是**额外加一层限制**，并不能保证在指定范围内处处可达：路径上任何一环是私有的，下游照样进不去。

```rust
mod engine {
    pub struct Engine { rpm: u32 }                // 字段私有：模块外无法直接读写
    impl Engine {
        pub fn new() -> Self { Engine { rpm: 0 } }
        pub fn stats(&self) -> String { format!("{}", self.rpm) }
        pub(crate) fn warm(&mut self) { self.rpm = 800; }
        fn internal_step(&mut self) { self.rpm += 1; }
    }
    pub fn demo() {
        let mut e = Engine::new();
        e.warm();
        e.internal_step();                        // ✅ 同模块
        println!("{}", e.stats());                // 801
    }
    #[cfg(test)]
    mod tests {
        use super::*;
        #[test]
        fn can_touch_private_field() {
            let mut e = Engine::new();
            e.internal_step();                    // ✅ 子模块能访问父模块私有项
            assert_eq!(e.rpm, 1);
        }
    }
}
fn main() {
    engine::demo();
    let mut e = engine::Engine::new();
    e.warm();                                     // ✅ pub(crate)
    // e.rpm = 1;                                 // 🛑 E0616: field `rpm` is private
    println!("{}", e.stats());                    // 800
}
```

两个常见的坑：一是把 `pub` 加在子项上就以为外部能访问，实际上从 crate 根到该项的路径上每一环都得是可见的；二是 `pub use` 重导出能「短路」隐私链——`pub use self::implementation::api;` 之后，外部可以通过 `api::f` 访问原本藏在私有模块里的东西，这正是 lib 里扁平 API 的常用手法，也是审计 API 面时最容易看漏的地方。枚举变体与 `pub trait` 的关联项是两个例外，它们在 `pub` 容器里默认就是公开的。

📘 [Rust Reference · Visibility and privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 有六个访问级，从宽到窄依次是 `open`、`public`、`package`、`internal`、`fileprivate`、`private`，默认级别是 `internal`（整个模块可见）。它把「能读」和「能写」拆开，于是有 `private(set)` 这种写法；也把「能用」和「能继承/覆写」拆开，`open` 才允许跨模块继承，`public` 不允许。`package` 是 Swift 5.9 通过 SE-0386 加入的，用来在「模块」和「整个世界」之间补一个「同一个 package 内的多个模块」这一级。

```swift
class Base {
    private var secret = 1                 // 仅本类型（及本文件中该类型的扩展）
    fileprivate var fileSecret = 2         // 本文件
    internal var moduleSecret = 3          // 本模块（默认）
    public var api = 4                     // 模块外可读，但不可被 override
    open var overridable = 5               // 模块外可继承/覆写（仅 class 成员）
    private(set) var counter = 0           // 读公开、写私有
    func bump() { counter += 1; secret += 1 }
}
extension Base {
    func peek() -> Int { secret }          // ✅ 同文件的扩展能看到 private
}
let b = Base()
b.bump()
print(b.counter, b.peek())                 // 1 2
// print(b.secret)                         // 🛑 'secret' is inaccessible due to 'private' protection level
```

`package` 是**上下文关键字**，所以 `package var package: String` 这种声明仍然合法；但 `package` 不能与其它访问修饰符组合。它由构建系统定义边界：编译器只认 `-package-name` 传进来的字符串，两个模块的包名相同才算同一个 package。SwiftPM 会自动传入包身份串，其它构建系统要自己传；不传的话，任何 `package` 声明都会直接编译失败，报 `requires a package name; set it with the compiler flag -package-name`。另外 `package` 单独出现时**不允许**跨模块继承或覆写（跨模块继承或覆写只有 `open` 才有），所以它比 `public` 更接近 `internal` 的继承模型。

```swift
// 用 `swiftc vis2.swift` 编译会失败，必须加 -package-name
package func pkgAPI() -> Int { 7 }
// 🛑 error: the package access level used on 'pkgAPI()' requires a package name;
//    set it with the compiler flag -package-name
```

最该记住的规则是 `private` 与 `fileprivate` 的分工：`private` 的作用域是「声明的类型 + 本文件中该类型的扩展」，`fileprivate` 是整份文件。也就是说同一个文件里给类型写扩展，扩展内能直接看到 `private` 成员，但另一个文件里的扩展就看不到——这是 Swift 里非常常用的组织方式。测试代码要用 `@testable import` 才能看到被测模块的 `internal`，前提是被测模块以 `-enable-testing` 编译，这等于在编译产物里留了一个正式的口子。

📘 [Swift · Access Control](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 只有两个访问级别，判定标准是**标识符的首字母是不是 Unicode 大写字母**：大写即导出（exported），小写或下划线开头即未导出（unexported，包内可见）。它没有 `public`/`private` 关键字，封装单位是 package 而不是类型或文件，同一 package 内无论分多少个文件都共享未导出名字。这种设计让「可见性」完全体现在命名上，读代码时看首字母就知道 API 边界。

```go
package main

import "fmt"

type account struct {        // 小写类型名：仅包内可见
	Owner   string           // 大写字段：导出
	balance int              // 小写字段：包内可见，包外彻底看不见
}

func (a *account) Balance() int  { return a.balance }  // 导出方法读私有字段
func (a *account) deposit(n int) { a.balance += n }    // 小写方法：包内

func main() {
	a := account{Owner: "ada", balance: 10}
	a.deposit(5)
	fmt.Println(a.Owner, a.Balance())   // ada 15
}
```

关键规则有三条。第一，未导出**不是编译期幻觉**：包外连字段名都写不出来，反射也只能拿到字段名（`reflect.Type.Field(i).Name`）却拿不到值——`Value.CanInterface()` 与 `CanSet()` 都是 `false`，强行 `Int()` 会 panic，`SetInt` 更不可能。第二，结构体的可比较性、嵌入字段的提升规则都跟可见性正交，嵌入一个未导出类型会导致它的导出方法也无法从包外调用。第三，文件不构成边界，同一个包里一个文件定义的私有函数另一个文件可以直接用；如果要跨包共享「只在某个子树内可见」的东西，得靠构建约定而不是语言。

```go
v := reflect.ValueOf(&a).Elem()
f := v.FieldByName("balance")
fmt.Println(f.CanInterface(), f.CanSet())   // false false
// f.Int()                                   // 🛑 panic: reflect.Value.Int using value obtained using unexported field
v.FieldByName("Owner").SetString("grace")    // ✅ 导出字段可写
```

包级约定上，`internal` 目录是最常被误认为语言特性的一条：任何位于名为 `internal` 的目录下的包，只能被该目录父目录那棵子树里的包导入，这是 `go build` 强制的构建规则，不是类型系统的一部分，所以反射与 `unsafe` 都不受影响。还有一点是「未导出字段 + 导出的构造函数」是 Go 里做不变量的标准手法，例如 `time.Time` 就把内部字段全部隐藏，只留方法。

📘 [Go spec · Declarations and scope](https://go.dev/ref/spec#Declarations_and_scope)

{{% /tab %}}

{{% tab header="Python" %}}

Python **没有强制性的访问控制**，只有两条纯约定：单下划线 `_name` 表示「内部使用，请勿触碰」，双下划线 `__name` 触发编译期的名称改写（name mangling）。改写规则很具体：在类体内出现的标识符 `__spam`（最多一个尾随下划线）会被文本替换成 `_ClassName__spam`，其中 `ClassName` 是**当前类的名字、去掉前导下划线**；这个改写对方法名、属性名、全局名都生效。

```python
class Account:
    def __init__(self, owner: str, balance: int) -> None:
        self.owner = owner          # 公开：纯约定
        self._balance = balance     # 单下划线：约定「内部」，不强制
        self.__pin = 1234           # 双下划线：触发名称改写

class Account2:
    _internal = 1
    __mangled = 2   # 变成 _Account2__mangled

a = Account("ada", 10)
print(a.owner)                 # ada
print(a._balance)              # 10   ⚠️ 能访问，只是约定
# print(a.__pin)               # 🛑 AttributeError
print(a._Account__pin)         # 1234  名称改写后照样能访问
print(hasattr(a, "__pin"), hasattr(a, "_Account__pin"))   # False True
print([n for n in vars(Account2) if "mangled" in n])       # ['_Account2__mangled']
```

名称改写**不是加密**：它只是把名字换成了另一个更长的名字，任何人写出 `a._Account__pin` 就能读写，这正是它存在的意义——防止子类无意中覆盖父类的私有属性，而不是防止有意的访问。另一个常见误解是 `__all__`：它只影响 `from module import *` 时导出哪些名字，对 `import module; module._x` 毫无约束力。类型层面的 `typing.Final` 与 `@final`（`typing.final`）只对静态检查器有意义，运行时只看 `__annotations__`，什么都拦不住；`__slots__` 则是唯一稍微「硬」一点的限制，它禁止凭空添加新属性，但已有属性照样能改。

```python
from typing import Final

class Config:
    __slots__ = ("_url",)
    MAX: Final = 10                # typing.Final 只是给类型检查器看的
    def __init__(self, url: str) -> None:
        object.__setattr__(self, "_url", url)
    @property
    def url(self) -> str:
        return self._url

c = Config("https://x.example")
try:
    c.extra = 1                    # 🛑 AttributeError（消息随版本变化）
except AttributeError as e:
    print("AttributeError:", str(e)[:30])   # AttributeError: 'Config' object has no attribu
object.__setattr__(c, "_url", "https://y.example")   # ⚠️ 强制改私有字段
print(c.url, c.MAX, Config.__annotations__)   # https://y.example 10 {'MAX': typing.Final}
```

所以 Python 的工程实践是「约定 + 文档 + linter + 类型检查器」四件套：`_` 前缀被 `pylint`/`ruff` 这类工具识别为受保护成员并给出告警，`@final` 被 `mypy` 强制执行，`__slots__` 顺手省内存并挡住误写。真正想要不可绕过的私有，只能把实现搬到 C 扩展里，让 Python 层根本拿不到那个对象——标准库里不少模块就是这么做的。

📘 [Python Reference · Private name mangling](https://docs.python.org/3/reference/expressions.html#private-name-mangling)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 有四个访问修饰符：`public`（默认）、`private`、`protected`、`internal`。它们的边界跟 Java 有一处关键差异——`internal` 的「模块」不是 Maven 坐标或 Gradle 项目，而是「一起编译的一组 Kotlin 文件」，具体包括 IntelliJ 模块、Gradle/Maven 的 source set、一次 `kotlinc` 调用产生的所有文件；Android 里通常就是一个 Gradle module。`protected` 在 Kotlin 里不能用于顶层声明，也不能用于对象表达式，它比 Java 的 `protected` 更窄——不包含包内可见那一层。

```kotlin
// 顶层声明
public val all = 1              // 默认就是 public，写出来只是显式
internal val inModule = 2       // 同一个编译模块内可见
private val inFile = 3          // 本文件内可见（顶层 private 的最广范围就是文件）

class Account(private val owner: String) {   // 构造函数私有参数自动变成私有属性
    internal var balance = 0                 // 模块内可见
    protected open fun hook() {}             // 只有子类可见（不能用在顶层）
    private fun audit() {}                   // 类内可见
    fun deposit(n: Int) { balance += n; audit() }
}

class Sub : Account("x") {
    override fun hook() { balance + 1 }      // ✅ 子类能访问 internal 与 protected
}
```

要注意 `internal` 只在 Kotlin 编译器视角下有效：编译到 JVM 字节码时，`internal` 声明仍是 `public`，名字里带的 `$module_name` 后缀只是防冲突，Java 代码可以直接调用它。官方给这个现象的建议是给 API 加 `@JvmSynthetic`（把这个声明对 Java 调用者隐藏）或者干脆别把内部 API 暴露给 Java 消费方。同理，`private` 顶层声明的实际可见范围是**文件**而不是「模块的一部分由编译器细分」——Kotlin 没有 Java 的包私有（package-private），跨文件的包内共享一律用 `internal`。

```kotlin
class Api {
    internal fun internalApi() {}      // 模块内可见
    @JvmSynthetic fun onlyForKotlin() {}   // 对 Java 调用者不可见
    @PublishedApi internal fun usedByInline() {}
    // @PublishedApi 让 internal 声明可以出现在 public inline 函数体里
}
```

最后两个实际用得到的点：`@PublishedApi` 是给「`public inline` 函数用到了 `internal` 声明」这种情况开的后门，否则编译器直接报错；可见性可以单独加在 getter/setter 上（`var x: Int = 0 private set`），这跟 Swift 的 `private(set)`、PHP 8.4 的 `private(set)` 是同一个思路的不同拼法。Kotlin 里没有 `open`/`public` 的区分——类默认 `final`，要继承必须显式加 `open`，这跟 Swift 把「可见」和「可继承」分成两级正好相反。

📘 [Kotlin · Visibility modifiers](https://kotlinlang.org/docs/visibility-modifiers.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的成员访问级别有四种，从宽到窄是 `public`、`protected`、包私有（package-private，即**不写任何修饰符**）、`private`。默认级别是包私有，这一点跟 C# 的成员默认 `private` 不同，也是 Java 初学者最容易忽略的一格。判定规则在 JLS 里定义为两条同时成立才可访问：成员声明允许该访问级别，且成员所在的类型本身可访问（JLS 6.6.1）。堆叠在包之上的是 JPMS 模块系统（Java 9 起），它用 `module-info.java` 里的 `exports` / `opens` / `requires` 再加一层边界。

```java
package shop;
public class Account {
    public String owner = "ada";        // 全世界可访问
    protected int balance = 10;         // 同包 + 子类
    int pin = 1234;                     // 包私有：同包可访问（默认）
    private String secret = "s3";       // 仅本类（含同类其它实例）

    public int peek(Account other) {
        return other.balance + other.pin;   // ✅ 同类实例之间可以互访 protected/private
    }
}
```

`private` 挡不住**同一个类的另一个实例**，这是 JLS 明确规定的：访问控制以「哪个类里写的代码」为准，而不是「访问的是哪个对象」。方法上的规则类似，接口里的成员默认 `public`，Java 9 起允许 `private` 接口方法（只能被接口内的默认方法或静态方法调用）。类与类之间的可见性只有两种：顶层类只能是 `public` 或包私有，嵌套类才可以使用全部四种。

```java
module shop {
    requires java.base;               // 隐含，写出来只是说明
    exports shop.api;                 // 只有这个包对外可见
    opens shop.model to com.fasterxml.jackson.databind;   // 只对指定模块开放反射
}
// 运行期补救：java --add-opens java.base/java.lang=ALL-UNNAMED
```

JPMS 的价值在于把「编译期可见」和「反射可用」拆成两个开关：`exports` 管编译期与普通运行期访问，`opens` 只管反射（`setAccessible` 能不能成功）。只 `exports` 不 `opens` 的包，运行时反射改私有字段会被拒。JDK 17 起（JEP 403，Strongly Encapsulate JDK Internals）默认连 `--illegal-access=permit` 也没有了，对 `java.*` 内部包的深反射必须显式 `--add-opens`，这让「反射万能」的时代在 JDK 生态里基本结束。没有 `module-info.java` 的 classpath 应用则处在「无名模块」世界，所有包都被 `exports` 出去，`opens` 也全部打开。

📘 [JLS · Access Control](https://docs.oracle.com/javase/specs/jls/se25/html/jls-6.html#jls-6.6)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有三种访问说明符 `public`、`protected`、`private`，默认值取决于用哪个关键字声明类型：`class` 的成员与基类默认 `private`，`struct` 与 `union` 默认 `public`。全部检查都发生在**编译期**，编译完成之后没有任何机制能阻止别人读写你标记为 `private` 的内存——这正是「编译期私有」的教科书案例。`friend` 是官方提供的一个正式缺口，被声明为友元的函数或类可以访问私有成员。

```cpp
#include <cstdio>
class Widget {
public:
    int api() const { return secret_; }
protected:
    int inherited_ = 1;                   // 派生类可见
private:
    int secret_ = 42;                     // 只有本类与 friend 可见
    friend int peek(const Widget &);      // friend 打开一个洞
};
struct Pod { int x = 1; };                 // struct 默认 public
int peek(const Widget &w) { return w.secret_; }
int main() {
    Widget w;
    std::printf("%d %d %d\n", w.api(), peek(w), Pod{}.x);   // 42 42 1
    // std::printf("%d\n", w.secret_);    // 🛑 error: 'secret_' is private
}
```

几条容易被忽略的规则：访问权限是**按名字**而不是按对象判定的，所以同类实例之间可以互访私有成员；派生类即使继承方式为 `public`，也只能通过基类接口访问基类私有成员，`using Base::member;` 只能改变**继承而来的可见性**（比如把 `protected` 成员在派生类里重新暴露成 `public`），不能提升原本就 `private` 的东西；`friend` 既可以是函数也可以是整个类，还可以是模板的特定实例化。真正要注意的是 C++ 的封装在**二进制层面不存在**：`#define private public` 之类的预处理器把戏能让编译器完全失去判断依据，代价是破坏 ODR（不同翻译单元看到的结构体布局若不一致，就是未定义行为），所以只能当调试手段，绝不能进产品代码。

```cpp
#include <cstdio>
#define private public          // ⚠️ 经典恶作剧：预处理器把 private 换成 public
class Secret { private: int hidden_ = 7; };
#undef private
int main() { Secret s; std::printf("%d\n", s.hidden_); }   // 7
```

实践上的取舍是：`private` 用来表达「这个类的实现细节」并配合 Pimpl 惯用法（头文件里只放 `std::unique_ptr<Impl>`，完整定义藏在 `.cpp`）来同时获得编译期与链接期隔离；`protected` 因为对封装伤害最大而被不少风格指南要求慎用，理由是子类会依赖基类的实现细节，改动基类就容易崩。至于 `const` 成员，它跟访问控制是两件事，`const` 只约束编译期能写什么。

📘 [cppreference · Access specifiers](https://en.cppreference.com/w/cpp/language/access)

{{% /tab %}}

{{% tab header="C" %}}

C **没有访问修饰符**，语言里根本不存在 `public`/`private`/`protected` 这三个关键字。它的封装完全靠三件事拼出来：`static` 让函数或全局变量获得内部链接（名字只在当前翻译单元可见）、头文件里只暴露不完整类型（`struct account;`）而把完整定义留在 `.c` 里、以及给内部符号加 `_` 前缀的命名约定。这三条都做不到「结构体字段级」的隐藏——只要能看到完整定义，任何字段都能改。

```c
#include <stdio.h>
/* C 没有任何访问修饰符：private 全靠 static（内部链接）与头文件约定 */
struct account {                 /* 定义放进 .c，头文件只放不完整类型才是真封装 */
    const char *owner;            /* 无修饰符：谁拿到指针谁就能改 */
    long balance;
};
static long g_calls = 0;          /* static：内部链接，别的翻译单元看不到这个名字 */
static void bump(void) { g_calls++; }   /* static 函数：本翻译单元私有 */
long account_balance(const struct account *a) { bump(); return a->balance; }
int main(void) {
    struct account a = {"ada", 10};
    struct account *p = (struct account *)&a;
    p->balance = 99;              /* 结构体字段没有访问控制，改得动 */
    printf("%s %ld %ld\n", a.owner, account_balance(&a), g_calls);   /* ada 99 1 */
    return 0;
}
```

`static` 是 C 里唯一真正由链接器执行的边界：内部链接的名字在目标文件里不会进入符号表，别的翻译单元引用不到，多个 `.c` 里可以有同名 `static` 函数互不冲突。头文件守卫（`#ifndef`）与 `static inline` 是工程约定而非访问控制——`static inline` 把函数定义放进头文件，效果是每个翻译单元各有一份副本，因此不能有可变状态。命名上，以下划线加大写字母或双下划线开头的标识符被标准保留给实现，用户代码用了是未定义行为，所以「内部函数加 `_` 前缀」在 C 里要写成 `prefix_internal_name` 这种带项目前缀的形式才安全。

`const` 跟访问控制也常被混为一谈：`const` 对象只是编译器禁止直接写，用强制转换去掉 `const` 再写属于未定义行为（`const int n = 41; int *p = (int *)&n; *p = 42;` 之后再读 `n`，实测在 clang 21 的 `-O0` 与 `-O2` 下都仍打印 41，因为编译器把 `const` 值折叠了），而且 `const` 管不到别人手里的非 `const` 指针别名。真正要跨模块边界做封装，C 的标准答案是「不完整类型 + 构造函数 + 访问器函数」，把 `struct` 的定义彻底藏在实现文件里，调用方连字段名都不知道。

📘 [cppreference · Storage class specifiers](https://en.cppreference.com/w/c/language/storage_duration)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia **没有访问修饰符**，模块系统不做隐藏：官方手册明确写着「unlike other languages, Julia has no facilities for truly hiding module internals」，因为带限定名的访问 `M.name` 永远是可行的。它提供两个名字管理关键字：`export` 决定 `using M` 时哪些名字被带进调用方命名空间，`public`（Julia 1.11 起）只把名字标记为公共 API 但**不影响命名空间**。

```julia
module Shop
export total                      # using Shop 会带入 total
public Account, rate              # 标为公共 API，但不会带入命名空间
struct Account                    # 不在 export 也不在 public：纯内部
    balance::Int
end
total(a::Account) = a.balance
rate() = 0.1
_secret() = 42                    # 下划线约定：内部
end

using .Shop
total(Shop.Account(7))            # 7        ✅ 导出的名字直接可用
# Account                          # 🛑 UndefVarError（public 不产生命名空间效果）
Shop.Account                       # ✅ 限定名永远可访问
Shop._secret()                     # 42      ⚠️ 下划线挡不住任何人
Base.ispublic(Shop, :Account)       # true
Base.ispublic(Shop, :_secret)       # false
```

需要分清三件事。`export` 与 `public` 都不构成强制边界，差别只在「导入时是否自动进入命名空间」与「是否被 `Base.ispublic` 认可为公共 API」；`public` 目前在语法上只能出现在文件或模块的顶层，这是为了兼容 Julia 1.11 之前把 `public` 当普通标识符的代码，官方也提醒别再把 `public` 当变量名用。`import M: f` 与 `using M: f` 的差异同样重要：只有 `import` 形式允许在**不加模块路径**的前提下给 `f` 添加方法，用 `using` 带进来的函数要扩展必须写 `M.f(...)`，这是 Julia 防止误改他人函数的机制。

```julia
module A
export f
f() = 1
end
module B
import ..A: f            # import 才允许直接扩展
f(::Int) = 2             # ✅ 给 A.f 加方法
end
```

反射层面 Julia 也不设防：`fieldnames(Account)`、`getfield(a, :balance)`、`Base.uncompiled` 之类都能直接看到内部结构，`getfield` 甚至能读到没有访问器的字段。所以 Julia 的封装是**社会契约**：包作者用 `export`/`public` 声明 API 面，用下划线标内部，用户靠约定不去碰；真要改内部，语言不会拦你，但升级包时后果自负。测试代码的常见做法是直接 `using MyPkg` 后访问内部函数，因为同一个包内的模块本来就没边界。

📘 [Julia · Modules](https://docs.julialang.org/en/v1/manual/modules/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 有六个可组合的访问级别：`public`、`private`、`protected`、`internal`、`protected internal`（并集：本程序集**或**派生类）、`private protected`（交集：本程序集**且**是派生类）；C# 11 又加了 `file` 修饰符，把顶层类型限制在单个源文件内。默认值容易记错：**顶层类型默认 `internal`**（不是 `public`），**类与结构的成员默认 `private`**，而枚举成员与接口成员默认 `public`。命名空间本身没有访问限制，官方明确说不要在命名空间上写访问修饰符。

```csharp
namespace Shop;

internal class Account            // 顶层类型默认 internal，写出来只是显式
{
    public string Owner = "ada";              // 不限制
    protected int Balance = 10;               // 本类 + 派生类
    internal int Pin = 1234;                  // 本程序集
    protected internal int Limit = 100;       // 本程序集 或 派生类
    private protected int Cap = 50;           // 本程序集 且 派生类
    private string secret = "s3";             // 仅本类型（含同类其它实例）

    public int Peek(Account other) => other.secret.Length + other.Pin;   // ✅ 同类实例互访
}

file class HiddenWidget           // C# 11：只在当前文件可见
{
    public int Work() => 42;
}
```

`file` 修饰符的细节值得单独记：它**不能与任何访问修饰符组合**，只能加在顶层类型上；嵌套在 file 类型里的类型也一并变成文件局部；其它文件可以声明同名类型而不会冲突；成员查找会优先解析到本文件的 file 类型，这样源生成器生成的辅助类型不会跟用户代码撞名。file 类型还有一个反向限制——它不能作为任何**非 file 类型**的字段类型或成员签名类型出现（但公开类型可以隐式实现 file 接口，显式实现只能在同文件内用）。

```csharp
// File1.cs
file interface IWidget { int ProvideAnswer(); }
file class HiddenWidget { public int Work() => 42; }

public class Widget : IWidget {          // ✅ 公开类型隐式实现 file 接口
    public int ProvideAnswer() => new HiddenWidget().Work();
    // private HiddenWidget w;           // 🛑 file 类型不能做非 file 类型的字段
}
// File2.cs
public class HiddenWidget { }            // ✅ 与 File1.cs 的 file 类型不冲突
```

程序集边界上的实际控制手段是 `[assembly: InternalsVisibleTo("MyTests")]`，它把 `internal` 声明开放给指定程序集——这几乎总是给测试项目用的，代价是被点名的程序集从此能看到全部 internal 面（强命名程序集还需要公钥）。C# 没有 Java 那种包私有，同一程序集内跨文件的「包内共享」一律用 `internal`；想在程序集内部再细分「只有派生类可见」，`private protected` 就是为此设计的交集语义。

📘 [MS Learn · Accessibility levels](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/accessibility-levels)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的访问控制只有一种形式：标识符以 `_` 开头即私有，作用域是**库（library）**而不是类或文件。一个 `.dart` 文件默认自成一个库，这个文件里声明的所有 `_` 开头成员互相可见；用 `part` / `part of` 把多个文件拼成一个库之后，这些文件共享同一个私有作用域。Dart 3.0 引入的类修饰符（`interface`、`base`、`final`、`sealed`、`mixin`）管的是继承与实现的开放性，跟这里说的成员可见性不是一回事，两者经常被混淆。

```dart
// account.dart —— 这个文件本身就是一个 library
class Account {
  final String owner;
  int _balance;              // 私有：只有本库内可见
  Account(this.owner, this._balance);
  int get balance => _balance;
  void _audit() {}           // 私有方法
}

int _helper() => 1;          // 私有顶层函数

void main() {
  final a = Account('ada', 10);
  print(a.owner);            // ada
  print(a.balance);          // 10
  print(a._balance + _helper());   // 11  ✅ 同库内可以访问
}
```

跨库就完全看不到：另一个文件 `import` 进来之后，写 `a._balance` 会直接编译失败，而 IDE 甚至不会在补全里列出它——这是 Dart 相对 Python 的一个显著优势，`_` 是被编译器强制的边界，而不是社会约定。副作用是「库内全部文件共享私有」：一旦用了 `part`，任何 `part` 文件里的代码都能碰到其它 part 文件的私有成员，所以官方风格指南建议慎用 `part`，倾向用小库 + `import`。

```dart
// library.dart
library shop;
part 'account.dart';          // account.dart 里要写 `part of 'library.dart';`
part 'internal.dart';         // 两个 part 共享同一个私有作用域
```

导出面上，`export 'src/impl.dart' show PublicApi hide InternalApi;` 可以精确控制库对外暴露哪些名字，`show` 与 `hide` 可以组合；`package:xxx/xxx.dart` 里的 `src/` 目录是 pub 工具层的约定——按惯例外部不应 import 进 `src/`，但工具链本身并不阻止。Dart 里没有 `protected`，需要「只给子类用」的成员时只能靠 `@protected` 注解加 linter 提示，或者把成员私有再加一组受保护的钩子方法。类修饰符补充说明：`final class` 禁止本库之外的继承与实现（同库内仍可继承或实现）、`interface class` 只能实现不能继承、`sealed class` 只能在同库内被继承（配合模式匹配的穷尽性检查），这些约束都在编译期执行。

📘 [Dart · Libraries & imports](https://dart.dev/language/libraries)

{{% /tab %}}

{{% tab header="R" %}}

R **没有访问修饰符**，封装由包机制与命名约定共同承担：包的对外接口写在与包同级的 `NAMESPACE` 文件里，`export(...)` 列出的名字可以用 `pkg::name` 访问，未导出的名字只能用三冒号 `pkg:::name`。也就是说 R 的边界是「约定 + 导出清单」，语言本身不做强制——只要写出 `:::`, 内部函数、内部数据一律拿得到。

```r
# 包 mypkg 的 NAMESPACE
export(total)
export(Account)
exportPattern("^[^\\.]")     # 导出所有不以 . 开头的名字（常用的一揽子写法）
S3method(print, Account)     # 注册 S3 方法（不需要用户直接调用）
importFrom(stats, median)

# R/account.R
Account <- function(owner, balance) {
  structure(list(owner = owner, balance = balance), class = "Account")
}
total <- function(a) a$balance          # 导出
.internal_rate <- function() 0.1         # 以 . 开头：约定为内部
```

三冒号与双冒号的区别是 R 里最实用的一条判据：`mypkg::total` 只在名字被导出时可用，`mypkg:::.internal_rate` 无视导出清单直接取；用 `:::` 访问未导出对象在 `R CMD check` 里会报 NOTE，提交 CRAN 前必须清掉，这算是工具链给出的一点点「软强制」。`exportPattern` 的写法解释了为什么 R 社区约定内部函数用 `.` 开头——只要正则写成 `^[^\\.]`，它们就自动不进入导出面。

```r
mypkg::total                       # ✅ 导出名可用
mypkg:::.internal_rate             # ✅ 内部名也能拿到（R CMD check 会 NOTE）
env <- asNamespace("mypkg")
get(".internal_rate", envir = env)  # 0.1：直接进命名空间环境取
assignInNamespace(".internal_rate", function() 0.9, ns = "mypkg")   # ⚠️ 直接改包内绑定
```

环境（environment）是 R 反射能力最强的地方：`asNamespace()` 拿到包的命名空间环境，`get`/`assign`/`ls` 可以随意读写其中任何绑定，`assignInNamespace` 甚至能在运行时替换包内函数（官方文档把它列为「不推荐、仅供开发使用」，因为它会让其它已编译的引用失效）。另外 R 里对象系统自带一层类似可见性的东西：`$.Account` 之类的 S3 方法、R6 类的 `private` 参数、`methods::setClass` 的 `@` 槽位都能表达「只有本类的成员能碰」，但这些都是各个对象系统自己的语义，不是语言级关键字。

📘 [Writing R Extensions · NAMESPACE files](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Package-namespaces)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 只有一种访问修饰符 `pub`，其余一切都是「文件内私有」。它的容器规则很特别：**一个文件就是一个 struct**，文件顶层声明的函数、变量、类型都是这个容器的成员，`pub` 决定它们能否被别的文件通过 `@import` 看见。Zig 没有类，也没有成员可见性——struct 的字段永远可以从外部读写（字段的访问面由类型的可见性间接决定），所以「隐藏字段」只能靠不导出该类型、或者把类型定义留在实现文件里。

```zig
// account.zig —— 文件即容器，等价于一个 struct
pub const Account = struct {          // pub：别的文件能看见这个类型
    owner: []const u8,                 // 字段无可见性概念，外部可读写
    balance: i64,
    pub fn init(owner: []const u8) Account {
        return .{ .owner = owner, .balance = 0 };
    }
};

fn helper() i64 { return 1; }          // 未加 pub：仅本文件可见

pub fn tag() []const u8 { return "shop"; }
```

从别的文件访问时，`@import("account.zig")` 得到的是一个结构体类型值，只有带 `pub` 的声明能取到：`account.helper()` 会编译失败，报 `'helper' is not marked 'pub'`。Zig 的可见性检查发生在**语义分析（编译期）**，所以正常路径上没有任何运行时手段能绕过它——没有反射、没有 `setAccessible`、没有运行时代码生成。要刻意突破的话只有 `@field` 与指针强制转换之类的 unsafe 操作，而它们的前提仍然是你先拿到那个类型与内存。

```zig
const std = @import("std");
const account = @import("account.zig");

pub fn main() void {
    const a = account.Account.init("ada");
    std.debug.print("{s}\n", .{account.tag()});   // shop
    // account.helper();                          // 🛑 error: 'helper' is not marked 'pub'
    std.debug.print("{d}\n", .{@field(a, "balance")});   // 0：@field 按名字取字段（必须存在）
    // @field(a, "nope");                         // 🛑 编译期错误：no field named 'nope'
}
```

两个细节。第一，`pub` 只是「容器成员对其它文件可见」，**不控制字段**：想限制字段访问就得让类型的定义不公开，只导出构造函数和访问器函数，或者用 `opaque {}` 表示一个只有指针大小、内部结构完全未知的类型（C 互操作常用）。第二，Zig 有另一个叫 `export` 的关键字，它管的是「把这个声明放进生成的二进制符号表，给 C 用」，跟源码级可见性是两回事——`pub` 决定 Zig 代码能不能引用，`export` 决定链接器能不能找到。`@field` 与 `@hasField` 都是 comptime 求值的内建函数，字段名写错是编译错误，不会变成运行时的空值。

📘 [Zig · Documentation · Import and containers](https://ziglang.org/documentation/master/#import)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有访问修饰符**，因为它连类都没有：模块就是一个返回 table，成员就是 table 字段，`local` 只能让名字在**当前 chunk**（文件或函数）的词法作用域里存在，管不到 table 字段。所以 Lua 里「私有」有两种实现：约定式（`_` 前缀，纯靠人自觉）与真私有（把数据放进闭包 upvalue，外部既没有字段名也没有路径能拿到）。

```lua
-- Lua 没有访问修饰符；真私有靠闭包，约定式私有靠下划线
local Account = {}
Account.__index = Account

function Account.new(owner, balance)
  local self = setmetatable({}, Account)
  self.owner = owner        -- 公开字段
  self._balance = balance   -- 约定式私有：只是名字，谁都改得动
  return self
end

function Account:balance() return self._balance end

local a = Account.new("ada", 10)
print(a.owner, a:balance())      -- ada 10
a._balance = 999                 -- ⚠️ 约定被打破
print(a:balance())               -- 999
```

闭包版本才是真的封不住也拿不到：`balance` 只作为 upvalue 存在，外部连字段名都没有，`b._balance = 999` 只是往 table 上新增了一个毫不相干的键。代价是每个实例都要新建一组函数（内存开销）、没有 `__index` 共享、也不能 `debug.getinfo` 之外的方式内省，所以性能敏感的库反而宁可用 `_` 约定加 `setmetatable` 共享方法表。

```lua
local function new_private(owner, balance)
  local self = { owner = owner }
  function self:balance() return balance end          -- balance 是 upvalue
  function self:deposit(n) balance = balance + n end  -- 只有闭包能改
  return self
end
local b = new_private("grace", 5)
b:deposit(3)
print(b.owner, b:balance(), b._balance)   -- grace 8 nil
b._balance = 999                          -- 写了个不相干的字段
print(b:balance())                        -- 8
```

`setmetatable` 的 `__index` 与 `__newindex` 还能做出「只读表」或「代理表」的错觉，`__newindex` 收到写请求时可以选择报错，但调用方一句 `rawset(t, k, v)` 就绕过去了——`rawset`/`rawget` 明确按「不触发元方法」操作，这也是 Lua 里所有「表级访问控制」都不堪一击的原因。元表本身也不是安全的：`debug.setmetatable`、`getmetatable`（配 `__metatable` 字段虽然能挡住 `getmetatable`，但挡不住 `debug` 库）都能改。总结：Lua 的封装强度取决于你把数据放在 table 里还是闭包里，`_` 前缀只提供可读性。

📘 [Lua 5.5 Reference Manual · Visibility and upvalues](https://www.lua.org/manual/5.5/manual.html#3.5)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 有两套完全不同的「私有」写法，必须分清：`private` / `protected` / `readonly` 是**类型层面的修饰符，编译后整体擦除**，生成的 JavaScript 里那个属性就是个普通属性；`#name` 是 ECMAScript 原生私有字段，编译到较老目标时由编译器模拟、编译到 ES2022+ 时原样保留，是**运行时的真私有**。默认可见性是 `public`，`protected` 只在类及其子类内可访问，`private` 只在声明它的类内可访问（同类实例之间可以互访）。

```typescript
class Account {
  public owner: string;              // 默认就是 public
  protected balance: number;         // 本类 + 子类
  private secret: string;            // 仅本类（编译期）
  readonly id: string;               // 只能构造期赋值
  #pin: number;                      // ES 原生真私有
  constructor(owner: string, id: string) {
    // 赋值顺序与字段声明顺序保持一致，Object.keys 的顺序才可预期
    this.owner = owner; this.balance = 0;
    this.secret = "s3"; this.id = id; this.#pin = 1234;
  }
  peek(other: Account) { return other.secret; }   // ✅ 同类实例互访
  get pin() { return this.#pin; }
}

const a = new Account("ada", "A1");
(a as any).secret;      // "s3"   ⚠️ private 只是编译期，运行时是普通属性
(a as any).balance;     // 0
// (a as any).#pin;     // 🛑 SyntaxError：私有名字在类外无法引用
console.log(Object.keys(a));   // [ 'owner', 'balance', 'secret', 'id' ]
```

`readonly` 也是一个纯编译期约束：它只禁止在构造器之外赋值，运行时属性照样可写，而且它跟 `private` 可以叠加成 `private readonly`。`private` 与 `#` 最关键的差别在「谁来强制」——前者由 TS 编译器检查，一个 `as any` 或 `// @ts-ignore` 就能穿透，而且如果属性出现在对象字面量或结构化类型里，鸭子类型还可能让不该访问的代码通过；后者由 JS 引擎强制，属性存放在独立的私有名字空间里，`Object.keys`、`JSON.stringify`、`for...in`、`Reflect.ownKeys` 都不会列出它，外部连语法上引用它的方式都没有。

```typescript
/** @internal */
export function debugOnly() {}    // 配合 tsconfig 的 stripInternal: true，
                                  // 这一项会从生成的 .d.ts 里被删掉
```

`@internal` 是 JSDoc 标记，本身不做任何检查：只有把 `stripInternal` 打开，它才在生成声明文件时把这些声明剔掉，效果是「包外看不到类型」；但它不会阻止运行时代码被 import，也不会从 `.js` 产物中移除，所以它只适合标注「不承诺兼容性」的实验性 API。实践建议很明确：库的对外边界用 `@internal` + `stripInternal` 管理声明面，真正需要防止运行时篡改的数据用 `#`，而 `private` 只当作「团队内部约定」的机器可读版本，别把它当安全边界。

📘 [TypeScript · Class members: private and protected](https://www.typescriptlang.org/docs/handbook/2/classes.html#member-visibility)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的私有字段 `#name`（ES2022 正式纳入规范）是**真正的运行时私有**：它以 `#` 开头、声明在类体里，名字存在于一个独立于字符串键的私有名字空间，作用域严格限制在类体内（包括类里定义的静态块、方法、访问器）。类外引用 `obj.#name` 不是「访问不到」而是**语法错误**，因为 `#name` 在那个词法位置根本没有被解析成一个合法的引用。这是本页「真私有」的代表，与 TypeScript 的 `private` 形成鲜明对照。

```javascript
class Counter {
  #count = 0;                          // 真私有字段
  static #instances = 0;               // 私有静态字段
  static { Counter.#instances = 0; }   // 静态块（ES2022）
  #bump() { this.#count += 1; }        // 私有方法
  inc() { this.#bump(); return this.#count; }
  static has(obj) { return #count in obj; }   // 私有字段可用 in 检测
}
const c = new Counter();
console.log(c.inc(), c.inc());       // 1 2
// console.log(c.#count);            // 🛑 SyntaxError
console.log(Object.keys(c));          // []
console.log(Counter.has(c));          // true
console.log(JSON.stringify(c));       // {}
```

`#` 字段不出现在任何枚举里：`Object.keys` 给空数组，`JSON.stringify` 给 `{}`，`Reflect.ownKeys` 也看不到，`Object.getOwnPropertyNames` 同样没有。唯一的探测手段是 `#count in obj`（`in` 运算符专门支持私有名字，前提是代码写在能解析该私有名字的类体内），所以常见的「友元」写法就是暴露一个静态方法 `static has(obj) { return #x in obj; }`。另一个必须记住的点是 `#` 不允许「后加」：类外无法给对象动态挂上私有字段，也不能通过继承把父类的 `#x` 变成子类的——子类写 `#x` 会得到完全不同的私有名字。

```javascript
// 闭包 + WeakMap 也能做到真私有（# 出现之前的做法）
function makeCounter() {
  let n = 0;                          // 闭包变量，外部拿不到
  return { inc: () => ++n, get: () => n };
}
const f = makeCounter();
f.inc();
console.log(f.get(), Object.keys(f));   // 1 [ 'inc', 'get' ]

const priv = new WeakMap();           // WeakMap：外部拿不到 key
class Legacy {
  constructor() { priv.set(this, { n: 0 }); }
  inc() { return ++priv.get(this).n; }
}
const l = new Legacy();
l.inc();
console.log(l.inc(), Reflect.ownKeys(l).length);   // 2 0
```

闭包方案的原型是 IIFE（立即执行函数表达式）返回一个对象，公开方法通过作用域链访问私有变量；WeakMap 方案把私有状态挂在以实例为键的 WeakMap 上，好处是实例可以被垃圾回收（不会因为私有状态而泄漏）、多个类可以共享同一份访问函数，坏处是每次访问都要查表、调试时看不到值。三种方案的选择标准很实际：单一实例、少量方法用闭包；需要类继承与优雅调试用 `#`；需要跨类共享私有状态（例如几个协作类要互相看到对方内部）用 WeakMap。要注意 `#` 与构造函数参数属性、`Object.defineProperty` 都无关，它不进原型链、不能被 `delete`、也不能被 `with` 语句捕获。

📘 [MDN · Private class features](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Private_class_fields)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 有 `public`、`protected`、`private` 三个标准的成员可见性关键字（常量自 7.1 起也可加），**默认是 `public`**——属性、方法、常量都是不写就公开。真正的特色是 PHP 8.4 引入的**非对称可见性**：属性可以分别为读（`get`）和写（`set`）指定不同的作用域，写法是在主可见性后加括号形式的 `set` 修饰，例如 `public private(set) string $title`。PHP 8.5 起这套写法也可以用在静态属性上。

```php
class Book
{
    public function __construct(
        public private(set) string $title,      // 读：public；写：private
        public protected(set) string $author,   // 读：public；写：protected
        protected private(set) int $pubYear,    // 读：protected；写：private
    ) {}
}

class SpecialBook extends Book
{
    public function update(string $author, int $year): void
    {
        $this->author = $author;   // ✅ 继承类可写 protected(set)
        $this->pubYear = $year;    // 🛑 Fatal Error：private(set) 属性是 final
    }
}

$b = new Book('How to PHP', 'Peter H. Peterson', 2024);
echo $b->title;              // ✅ Works
$b->title = 'How not to PHP';   // 🛑 Fatal Error
```

非对称可见性的四条硬规则要背下来：**只有带类型的属性**才能单独指定 `set` 可见性；`set` 必须与主可见性相同或更严格（`public protected(set)` 合法，`protected public(set)` 直接语法错误）；`private(set)` 的属性**自动是 `final`**，子类不得重新声明；对属性取引用（`&$obj->prop`）与对数组属性做写入都按 `set` 可见性判定，因为这两种操作都可能改值。另外 `private(set)` 中间**不能有空格**，`private( set )` 是解析错误。继承时子类可以把主可见性或 `set` 可见性放宽（不得收紧），而 `private` 属性被「覆盖」其实只是新建了一个内部名字不同的新属性。

```php
class Manager
{
    public private(set) static int $calls = 0;   // PHP 8.5：静态属性也支持非对称可见性
    public function doAThing(): string { self::$calls++; return "some string"; }
}
$m = new Manager();
$m->doAThing();
echo Manager::$calls;    // ✅ 1
Manager::$calls = 5;      // 🛑 Fatal error: Cannot modify private(set) property
```

PHP 的 `private` 有一个跟 Java、C#、C++ 一致的特性：**同一个类的不同实例之间可以互访私有成员**，因为可见性判定看的是「代码写在哪个类里」。与之相比，属性钩子（property hooks，8.4 引入）带来的是另一维度的控制——`get`/`set` 钩子可以让读写走自定义逻辑，而钩子内部访问真实存储用 `$this->prop`（钩子里的直接读写不会递归）。把 `private(set)` 和钩子组合起来，就能做出「外部只读、内部可写、写的时候还要校验」的一体化封装，这在 8.4 之前必须靠 `__set` 加 `private` 属性手工拼。

📘 [PHP · Visibility](https://www.php.net/manual/en/language.oop5.visibility.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的可见性关键字是 `public`、`protected`、`private`，它们**不是修饰符而是方法**（`Module#public`、`Module#private`、`Module#protected`），调用之后会改变后续方法定义的默认可见性，也可以传符号参数单独改某个方法：`private :foo`。`private` 的全部含义是「不能用显式 receiver 调用」，所以 `obj.foo` 会直接 NoMethodError；唯一的例外是 receiver 写成字面量 `self`（Ruby 2.7 起允许，`self.foo` 与私有 setter `self.foo = 1` 都可以），而 `protected` 的含义是「当 receiver 是同类或子类实例时可以显式调用」。

```ruby
class Account
  VERSION = "1.0"
  private_constant :VERSION   # 常量私有：Account::VERSION 会 NameError
  def initialize(owner, balance)
    @owner = owner            # 实例变量天生私有，没有可见性语法
    @balance = balance
  end
  attr_reader :balance        # 公开读方法（生成 def balance）
  def same_as?(other) = self <=> other   # ✅ 类内部调用 protected 方法
  protected
  def <=>(other) = balance <=> other.balance   # 类外显式调用会 NoMethodError
  private
  def secret = "pin"
  public
  def reveal = secret         # ✅ 类内部隐式 receiver 调用私有方法
end

a = Account.new("ada", 10)
b = Account.new("bob", 20)
a.balance                     # 10
a.same_as?(b)                 # -1
a.reveal                      # "pin"
a <=> b                       # 🛑 NoMethodError: protected method '<=>'
```

Ruby 的两个特色是常量与类方法需要**专门的私有化方法**：`private_constant :NAME` 让 `Account::VERSION` 直接抛 `NameError`，`private_class_method :new` 之类的写法可以封住构造入口（工厂方法模式的标配），`module_function` 则把实例方法同时变成模块的私有实例方法与公开单例方法。实例变量没有可见性概念——`@balance` 在任何地方都不能通过语法直接访问，只能靠 `instance_variable_get` 反射，这算是 Ruby 里「天然私有」的部分。

```ruby
class Account
  VERSION = "1.0"
  private_constant :VERSION
  def initialize(owner, balance)
    @owner = owner
    @balance = balance
  end
  attr_reader :balance
  private
  def secret = "pin"
end

a = Account.new("ada", 10)
a.secret                              # 🛑 NoMethodError: private method 'secret'
a.send(:secret)                        # "pin"   ⚠️ send 无视 private
a.instance_variable_get(:@balance)     # 10      ⚠️ 实例变量也能反射出来
Account::VERSION                       # 🛑 NameError: private constant
Account.const_get(:VERSION)            # "1.0"   反射照样能拿到
```

所以 Ruby 的 `private` 是「防手滑」而不是「防有心」：`send` / `__send__` 可以调用任何私有方法，`public_send` 才会尊重可见性，`instance_variable_get` / `instance_variable_set` 可以读写任何实例变量，`const_get` 可以取私有常量。测试代码普遍用 `send` 去测私有方法，这也是社区公认的用法。`refinements`（`refine` + `using`）不是访问控制，它提供的是「在限定作用域内改写类的方法」，常被用来做依赖注入与测试替身：`refine` 的效果只在写了 `using` 的文件或模块内生效，文件外完全看不到。

📘 [Ruby · Module#private](https://docs.ruby-lang.org/en/master/Module.html#method-i-private)

{{% /tab %}}

{{< /tabpane >}}

### 模块与文件级封装

封装的边界到底画在哪里，比成员修饰符更能决定一个项目的可维护性。Rust 画在 `mod` 树上，Go 画在 package 上，Swift 画在 module（再加 5.9 的 package），Java 画在 package 与 JPMS module，C# 画在 assembly + file，Dart 画在 library，R 画在 package 的 NAMESPACE，C 画在翻译单元，C++ 则同时有 namespace（只是名字与 ADL 的划分）与 C++20 modules（真正的隔离单位）。下面每个标签页逐一落实边界定义、跨边界机制、以及「fileprivate 与 package-private 这一级别各语言怎么表达」。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的封装单位是 `mod` 树，而 `mod` 既可以是内联块也可以是整个文件，文件与模块通过「文件名 = 模块名」的规则对应（`foo.rs` 或 `foo/mod.rs` 作为 `mod foo;` 的实现）。可见性沿树按「祖先-后代」规则判定：私有项对定义它的模块及其所有后代可见，`pub` 项还要保证从 crate 根到它的路径上每一环都可见。`pub use` 是调整 API 面的核心工具，它把深层路径里的项重导出到浅层，从而「短路」隐私链。

```rust
// src/lib.rs
pub use crate::inner::api::Thing;        // 对外暴露为 my_crate::Thing

mod inner {                              // 私有模块：外部看不到这个路径
    pub mod api {
        pub struct Thing;
        pub(crate) fn crate_only() {}    // 整个 crate 可见
        pub(super) fn parent_only() {}   // inner 可见
    }
}
// 外部 crate：my_crate::Thing ✅（重导出）；my_crate::inner::api::Thing 🛑
```

几个实务要点。第一，`mod test` 作为子模块天然能访问父模块私有项，所以 Rust 的单元测试不需要任何特权机制；集成测试放在 `tests/` 目录下是独立的 crate，只能看到 `pub` 面，这正好形成「单测看内部 / 集成测看外部」的双层结构。第二，`pub(crate)` 是最常用的「crate 内共享」级别，等价于「没有下游 crate 能看到」，比 `pub` 更能锁住 API 面；`#[doc(hidden)] pub` 则是「技术上公开但不承诺」的半公开写法，常见于宏内部需要的辅助项，因为宏展开后的代码在调用者 crate 里也必须能引用到它们。第三，Rust 没有「同一个 crate 内多个文件自动共享私有」这回事——`mod` 的私有边界是严格的，同 crate 的兄弟模块之间也不能互访对方的私有项，只能靠 `pub(crate)` 或 `pub(super)` 显式放宽。

```rust
mod a { pub(crate) fn shared() {} fn hidden() {} }
mod b {
    pub fn use_it() { super::a::shared(); }   // ✅ pub(crate)
    // pub fn nope() { super::a::hidden(); }  // 🛑 兄弟模块的私有项
}
```

📘 [Rust Reference · Modules](https://doc.rust-lang.org/reference/items/modules.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的默认封装单位是 **module**（一个 framework 或 app target 编译出来的东西），源文件是次一级单位，`package`（5.9 起）插在两者之间。它没有 Java 那种「包」的概念，同名类型分在不同 module 里靠 module 名消歧，所以跨 module 的 `internal` 完全不可见。测试要越过 module 边界必须用 `@testable import`（被测模块需以 `-enable-testing` 编译）。

```swift
// Engine 模块内
public struct MainEngine {
    public init() {}
    public var stats: String { "ok" }
    package func run() {}          // 同 package 的其它模块可见（SE-0386）
    internal func helper() {}      // 仅 Engine 模块
    fileprivate func local() {}    // 仅本文件
}
// Game 模块（同一 package，构建时传相同的 -package-name）
// import Engine
// MainEngine().run()               // ✅ package
// MainEngine().helper()            // 🛑 internal 跨模块不可见
```

`@testable import` 的代价要说清楚：它把模块的 `internal` 面整体开放给测试 target，并且要求被测模块以 testability 模式编译（SwiftPM 的 debug 构建默认开启，release 不开），这会在产物里保留额外信息、轻微影响优化。测试里要访问 `private` 成员则无路可走——连 `@testable` 也不行，只能在源文件里加 `#if DEBUG` 包一层 `internal` 访问器。`fileprivate` 是 Swift 独有的「文件级」级别，跟 C# 的 `file`、C 的 `static` 属于同一类需求：给一个只在单文件里使用的辅助类型或函数一个正式的、编译器强制的边界，而不是靠命名。

```swift
// 两种「内部」的差别
fileprivate struct Cache { }        // 只在本文件可见
private struct Impl { }             // 只在当前声明作用域（含同文件同类型的扩展）可见
package struct Shared { }           // 同 package 的其它模块可见（需 -package-name）
```

实际工程里推荐的组织方式是「一个 module 一个明确的 public API 面，其余全部 internal」：`public` 一旦发出就变成兼容性承诺，`package` 适合拆出来的工具模块与主模块共享，`fileprivate`/`private` 用于文件内的实现细节。Swift 6 的严格并发检查会让 `public` 类型还要满足 `Sendable` 等约束，这也是控制 API 面时不得不一起考虑的因素。

📘 [Swift · Access Control](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的封装单位是 package，一个目录一个 package，目录内的所有文件共享作用域。跨 package 的可见性只由标识符首字母决定，另外有两个辅助机制：`internal` 目录与 `vendor` 目录。`internal` 的规则由 `go build` 实现——路径中任何位置出现名为 `internal` 的目录，该目录下的包只能被以 `internal` 的父目录为根的那棵子树里的包导入；`vendor` 则是把依赖副本放进项目里。

```go
// 目录布局
// myapp/
//   main.go                  package main，可以 import myapp/internal/store
//   internal/store/store.go  package store，只能被 myapp 目录树内的包导入
//   other/lib/lib.go         package lib，位于 myapp 目录树之外
//
// other/lib 里写 import "myapp/internal/store" 会直接编译失败：
// use of internal package myapp/internal/store not allowed
```

`internal` 与可见性是正交的两套东西：`internal` 限制的是**谁能 import 这个包**，而标识符大小写限制的是**导入了之后能用包里的哪些名字**。所以 `internal/store` 里也可以有导出名，只是只有 `myapp` 目录树内的包能拿到；反过来，一个公开的包 `pkg/util` 里的小写名字谁都用不了。官方在 Go Modules 里还提供了 `internal` 的变体思路——用模块路径 `example.com/x/internal/y` 达到同样的效果，规则适用于模块路径而不仅是文件系统目录。

```go
// package store（位于 internal/store）
package store
type DB struct{ dsn string }          // 导出类型，但包本身只能是内部包
var defaultDB = &DB{}                 // 未导出变量
func Open(dsn string) *DB { return &DB{dsn: dsn} }   // 导出构造函数
```

`vendor` 目录的作用是锁定依赖副本并让构建脱离网络，它跟封装无关，但经常被拿来跟 `internal` 一起讨论「项目边界」。测试方面，Go 允许同一个目录里写 `package store` 的测试文件（内部测试，能访问未导出项）和 `package store_test` 的测试文件（外部测试，只能访问导出项），这两种测试文件可以共存于同一个目录，是极少数「同一目录两个包名」的合法情形。跨包共享内部实现的推荐做法是抽出 `internal` 子包，而不是把东西标成导出再靠注释说「别用」，因为大小写是编译期强制的、注释不是。

📘 [Go · Internal packages](https://go.dev/doc/go1.4#internalpackages)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的封装单位是 module 与 package，但两者都不提供强制访问控制。module 是 `.py` 文件，package 是含 `__init__.py` 的目录（或 PEP 420 的命名空间包），import 一个 module 后模块内的名字默认全部可访问。控制对外面的办法有三个：`__all__` 决定 `from m import *` 导入哪些名字、单下划线命名约定表示内部、以及 `__init__.py` 里做重导出把内部结构藏在后面。

```python
# mypkg/__init__.py
from ._impl import Client          # 把实现藏在 _impl 里，对外只暴露 Client
from ._impl import Client as _Client  # ⚠️ 下划线别名能避免 from mypkg import * 带出去

__all__ = ["Client"]               # 只影响 from mypkg import *
__version__ = "1.0"

# mypkg/_impl.py
class Client:
    def __init__(self) -> None:
        self._transport = object()   # 内部字段，约定私有

# 使用方
# from mypkg import Client         # ✅
# from mypkg import _impl          # ⚠️ 能 import，只是约定上不该
# import mypkg; mypkg._impl.Client # ⚠️ 一样能拿到
```

常见误区是把 `__all__` 当防火墙。它的语义只在 `from module import *` 时生效，而且有子模块时行为更绕：`from package import *` 只会带出 `__all__` 列的名字，但 `import package.sub` 依然成立。真正的封装靠布局——把实现放进 `_internal` 子包或 `_impl` 模块，让公开路径的长度为零、内部路径带下划线，再用文档与类型存根（`.pyi`）声明公共 API 面。类型存根在这里有个额外好处：`py.typed` 包可以只给公共 API 写 `.pyi`，类型检查器就会把 `.pyi` 里没有的名字视为不可用，`mypy` 会直接报错，等于给「约定」加了一层静态强制。

```python
# mypkg/_impl.pyi（或 mypkg/__init__.pyi）只声明公共面
class Client:
    def __init__(self) -> None: ...
```

测试与生产的边界在 Python 里没有语言支持：pytest 直接 `from mypkg._impl import Client` 就能测内部，社区的惯例是「测试可以碰私有，但不该依赖私有实现细节」。如果确实需要白盒测试接口，标准的做法是在 `_impl` 里留一个 `_testing` 子模块（名字仍然带下划线，但把它当稳定的测试 API 维护），比让测试到处摸私有属性可控得多。命名空间包（PEP 420）让多个目录拼成同一个包，此时没有 `__init__.py` 可以放重导出，跨目录的可见性完全靠命名约定，这一点在大型 monorepo 里尤其容易失控。

📘 [Python Tutorial · Packages](https://docs.python.org/3/tutorial/modules.html#packages)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的封装单位是**模块**（module），其定义是「一起编译的一组 Kotlin 文件」：IntelliJ 模块、Gradle/Maven 的 source set、一次 `kotlinc` 调用产生的所有文件。`internal` 就以此为界，跨模块不可见。Kotlin 没有 Java 的包私有：包里可见的东西必须写成 `internal` 才会跨文件共享，而 `internal` 的范围又通常比包大。多平台项目里，「模块」进一步细化为每个 target 的编译单元，`internal` 在 common 与 platform 源码之间共有可见性，跨 target 则要按平台规则判断。

```kotlin
// src/main/kotlin/shop/Account.kt
package shop
internal class Ledger {               // 模块内可见：别的 Gradle 模块看不到
    internal fun record() {}
}
private fun fileHelper() {}           // 顶层 private：本文件

// src/main/kotlin/shop/Report.kt（同一个 Gradle 模块）
package shop
fun build() { Ledger().record() }     // ✅ internal 跨文件可用，与 package 无关
```

`internal` 在 JVM 上的实现细节必须知道：编译后它仍然是 `public` 成员，只是名字里带上了模块名做后缀（例如 `record$my_module`），`@JvmName` 还能改写这个名字。因此从 Java 调用它可以成功，只是名字难看；官方推荐给「不想让 Java 用」的 API 加 `@JvmSynthetic`，它会给声明加上 `ACC_SYNTHETIC` 标志，Java 编译器直接忽略。`@PublishedApi` 则解决另一个方向的问题：`public inline` 函数体里引用了 `internal` 声明时，必须给那个声明加 `@PublishedApi`，因为内联后的代码要出现在调用方模块里。

```kotlin
class Repo {
    @PublishedApi internal fun raw() = 1     // 允许被 public inline 函数引用
    internal fun secret() = 2
    @JvmSynthetic fun kotlinOnly() = 3       // Java 调用者看不到
}
public inline fun use(r: Repo) = r.raw()     // ✅ 需要 @PublishedApi
```

多平台项目里的可见性要注意 `expect`/`actual` 配对：`expect` 声明的可见性必须与 `actual` 一致，`internal expect` 在 common 里可见，各平台 actual 也必须是 `internal`。测试方面，Kotlin 的测试 source set 与主 source set 通常属于同一个编译模块（Gradle 配置为 `associate`），因此测试能直接访问 `internal`；如果是独立的测试模块，就得靠 `testFixtures` 或把内部 API 标成 `@VisibleForTesting`（这只是注解，不改变实际可见性）。没有 `@PublishedApi`、`@JvmSynthetic`、`@VisibleForTesting` 这类注解时，Kotlin 的可见性完全是编译器的，跟运行时无关。

📘 [Kotlin · Visibility modifiers](https://kotlinlang.org/docs/visibility-modifiers.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的封装单位有三层：类、包、模块（JPMS）。包是 `package` 声明加目录结构，包私有成员在同一个包内可见——注意「同一个包」要求包名完全相同，即使两个源目录分别是 `src/main` 与 `src/test`，只要都声明 `package shop` 就算同包，这也是 Maven 布局下测试能访问包私有成员的原理。JPMS 的模块在包之上再加一层：`module-info.java` 里的 `exports` 与 `opens` 决定哪些包对外可见。

```java
// module-info.java
module shop.app {
    requires java.logging;
    exports shop.api;                                   // 编译期与运行期可见
    opens shop.model to com.example.orm;                 // 只对指定模块开放深反射
    uses shop.api.Plugin;
    provides shop.api.Plugin with shop.internal.MyPlugin;
}
// 没有 exports shop.internal; → 其它模块连 import 都不行
```

`exports` 与 `opens` 的分工是 JPMS 最实用的部分：`exports` 管普通的编译期与运行期访问，`opens` 管反射（`setAccessible` 是否允许）。只 `exports` 不 `opens` 的包，用反射改私有字段会抛 `InaccessibleObjectException`。`opens` 加 `to 模块名` 的写法 是精准放行，适合给 Jackson、Hibernate 这类框架开一个指定口子，而不是把整个包无条件打开。JPMS 的另一个特点是**只对具名模块生效**：classpath 上的代码落在无名模块里，无名模块能读所有具名模块导出的包，自己却全部开放，所以大量老项目即使升到 JDK 25 也感觉不到模块系统的存在。

```java
package shop.api;
public class Service {
    void packagePrivate() {}          // 同包可访问（含同包的测试类）
    protected void forSubclass() {}   // 同包 + 子类
    private void impl() {}
}
// src/test/java/shop/api/ServiceTest.java 里可以直接调 packagePrivate()
```

测试与生产代码的边界在 Java 里就靠「同包 + 不同源目录」这一招：不需要 `InternalsVisibleTo`（.NET）或 `@testable`（Swift），只要测试类声明同样的包名就能访问包私有成员。真要访问 `private` 只能用反射加 `setAccessible(true)`，对 JDK 自己的类在 17 之后会被拒，对普通应用类仍然可以（因为它们的模块没有 `opens` 限制，无名模块默认全开）。`jlink`/`jdeps` 这类工具还会用模块图做裁剪，这也让「哪些包被 `exports`」变成发布 API 时必须认真维护的信息，而不是可选的注释。

📘 [Oracle · Understanding Java 9 modules](https://docs.oracle.com/javase/specs/jls/se25/html/jls-7.html#jls-7.7)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 有两个层次的组织单位：`namespace` 只是「名字的划分与 ADL 的作用域」，**不提供任何访问控制**——写在 `namespace impl` 里的东西，外部照样能 `impl::thing()`；真正的隔离单位是 C++20 引入的 **modules**（`module`/`import`/`export`），它把编译单元变成了可导入的语义单位，没有 `export` 的声明在模块外不可见，而且不会像头文件那样产生宏与名字的泄漏。

```cpp
// shop.cppm（模块接口单元）
export module shop;
export int total(int a, int b) { return a + b; }   // 导出：import shop 后可用
int helper() { return 1; }                          // 未导出：模块外不可见，也不进入符号查找

// main.cpp
import shop;
int main() { return total(1, 2) + helper(); }       // 🛑 error: 'helper' was not declared
```

没有模块时，C++ 的隔离手段只有 `namespace` + 匿名 namespace + `static`：匿名 namespace 里的东西具有内部链接，等价于 C 的 `static`，只在当前翻译单元可见；`.cpp` 里定义的辅助函数如果加 `static` 或放进匿名 namespace，别的 `.cpp` 就链接不到。但宏与 `#include` 的顺序仍然会穿透一切 namespace——头文件里定义的 `#define private public` 就是明证，这也是模块最被期待的价值：`import` 不引入宏、不产生文本替换，模块内的宏不会泄漏给导入方（除非显式 `export` 宏，C++20 的宏导出能力有限）。

```cpp
namespace shop {
    namespace { int private_helper() { return 1; } }   // 内部链接：本翻译单元
    int api() { return private_helper(); }
}
// 另一个 .cpp
// shop::private_helper();    // 🛑 链接错误（内部链接）
```

`using` 声明与指令是名字层面的工具，跟可见性正交：`using Base::member;` 可以在派生类里把继承而来的成员重新暴露（只对 `protected`/`public` 继承有效，不能提升基类的 `private`），`using namespace std;` 是名字查找的便利而不是访问控制。C++23 里 `std::print` 等新设施仍然全部依赖这个模型。实践建议是：真心需要模块边界就用 C++20 modules（构建系统支持度是关键前提），暂时用不了就靠匿名 namespace + 头文件只放接口 + Pimpl 的经典组合，别指望 `namespace` 能挡住任何人。

📘 [cppreference · Modules](https://en.cppreference.com/w/cpp/language/modules)

{{% /tab %}}

{{% tab header="C" %}}

C 的封装单位是**翻译单元**（translation unit，一个 `.c` 文件预处理后形成的编译单元），边界由链接属性决定：默认外部链接的东西在整个程序里可被引用，加 `static` 变内部链接。头文件不是语言结构，只是文本包含，所以「头文件里放什么」完全靠工程约定，编译器不会因为某个函数没在头文件里声明就禁止别的 `.c` 调用它（隐式声明在 C99 后是错误，但显式 `extern` 声明仍然可以，前提是签名匹配）。

```c
/* account.h —— 对外接口：只放不完整类型与函数声明 */
#ifndef ACCOUNT_H
#define ACCOUNT_H
typedef struct account account;        /* 不完整类型：调用方不知道字段 */
account *account_new(const char *owner, long balance);
long account_balance(const account *a);
void account_free(account *a);
#endif

/* account.c —— 实现：完整定义与内部函数都在这里 */
struct account { const char *owner; long balance; };
static long g_calls = 0;               /* 内部链接 */
static void bump(void) { g_calls++; }  /* 内部链接 */
account *account_new(const char *o, long b) { bump(); ... }
```

这个「不完整类型 + 构造/析构/访问器」的组合是 C 里唯一真正跨翻译单元有效的封装：调用方连 `sizeof(account)` 都算不出来，只能通过指针操作，字段布局可以随意改而不影响使用方。`static` 的边界是链接器执行的，所以比头文件约定硬得多——把内部函数写成 `static` 之后，就算别人手写 `extern` 声明也链接不到。头文件守卫（`#ifndef`）只防重复包含，跟可见性无关；`static inline` 把定义放进头文件是为了让内联可行，代价是每个翻译单元各有一份、不能有可变状态。

```c
/* 头文件里放 static 变量的经典陷阱 */
static int counter = 0;      /* ⚠️ 每个包含它的 .c 各有一份副本，互不相干 */
```

还有一个常被忽略的边界是符号可见性（visibility）：GCC/Clang 的 `__attribute__((visibility("hidden")))` 或 `-fvisibility=hidden` 可以让外部链接的符号不进入动态符号表，这是共享库真正控制导出面的手段，比 `static` 更灵活（同一个符号在静态库里可见、在动态库里隐藏）。命名规范上，C23 之后以下划线开头的名字仍有大量保留给实现的情形（`_` 加小写字母在文件作用域保留、`__` 或 `_` 加大写任何位置保留），所以「内部函数加一个下划线」这种做法在 C 里比在 Python 里危险，正确做法是加项目级前缀。

📘 [cppreference · Translation units and linkage](https://en.cppreference.com/w/c/language/storage_duration#Linkage)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的封装单位是 module，文件与模块**没有对应关系**：`include("file.jl")` 只是把文件内容在包含它的模块的全局作用域里求值，一个模块可以跨多个文件，一个文件也可以定义多个模块。官方手册明确说明模块的三个特性是「独立命名空间」「命名空间管理（`export`/`public`/`using`/`import`）」「可预编译」，而不包括访问控制。

```julia
module Shop
export Account, total            # using Shop 会把这些名字带进来
public rate                      # 1.11 起：标为公共 API，但不带入命名空间
include("account.jl")            # 在 Shop 的全局作用域里求值
include("report.jl")
end
```

`using` 与 `import` 的差异是 Julia 模块系统里最实际的一条规则：`using Shop` 会带入 `Shop` 这个名字以及全部导出名；`import Shop` 只带入模块名，之后要写 `Shop.total`；`using Shop: total` 只带入 `total`；`import Shop: total` 不仅带入还允许**不带模块路径**地给 `total` 添加方法。用 `using` 带进来的函数想扩展必须写 `Shop.total(x) = ...`，这是 Julia 刻意的防护——避免误改别人的函数。

```julia
module A
export f
f() = 1
end
module B
import ..A: f            # 只有 import 形式允许直接扩展
f(::Int) = 2             # ✅ 给 A.f 加方法
# 若写成 using ..A: f，则必须写 A.f(::Int) = 2
end
```

模块初始化与预编译也影响封装实践：模块里可以定义 `__init__()`，它在模块被加载后**只调用一次**，用来做运行时的初始化（例如给 C 库指针赋值），预编译期间不会执行；依赖外部状态的全局量如果直接写在模块顶层，会连同预编译结果一起被固化，这属于「实现细节泄漏到镜像里」的陷阱。测试上，Julia 的 `Test` 标准库与包结构没有强绑定，`runtests.jl` 里 `using MyPkg` 之后就可以直接调用内部函数，所以「只测公共 API」在 Julia 里要靠纪律：把测试拆成 `test/public/` 与 `test/internal/` 是常见做法。`Base.ispublic(m, :name)` 是 1.11 起可用的公共方法，工具链（如文档系统、REPL 帮助）靠它给非公共名字加警告。

📘 [Julia · Code Loading and Modules](https://docs.julialang.org/en/v1/manual/code-loading/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的封装单位是 **assembly**（程序集，通常是一个 `.dll`/`.exe`）与 **namespace**。namespace 只是名字划分，官方明确说「不要给 namespace 加访问修饰符，命名空间没有访问限制」；真正执行可见性的是 assembly——`internal` 以此为界，`InternalsVisibleTo` 可以把它开放给指定的友元程序集。C# 11 的 `file` 修饰符则把边界细化到单个源文件。

```csharp
// Shop.csproj 里的程序集是一个 boundary
namespace Shop.Api;                     // namespace 本身无访问限制
public class Client { internal void Warm() {} }

// AssemblyInfo.cs —— 把 internal 面开放给测试程序集
[assembly: InternalsVisibleTo("Shop.Tests")]
// 强命名程序集需要写全公钥：
// [assembly: InternalsVisibleTo("Shop.Tests, PublicKey=0024000004800000...")]
```

`InternalsVisibleTo` 的两个实际约束：它写在**被访问方**（生产程序集）里，所以是「主动开放」而不是测试单方面偷看；强命名程序集必须写完整公钥，漏写公钥是**编译期**错误 CS1726（编译器会提示强命名程序集必须在 `InternalsVisibleTo` 声明里指定公钥），只有公钥写了但与友元程序集实际公钥不匹配时才会在运行时失败。开放范围是全部 `internal` 声明，没有更细的粒度——想只给测试开放某几个类型，只能靠 `[assembly: InternalsVisibleTo]` + 约定，或者把那部分抽成单独的 `.Internals` 项目。

```csharp
// File1.cs
file class HiddenWidget { public int Work() => 42; }
// File2.cs
public class HiddenWidget { }              // ✅ 同名不冲突
// 另一个文件里：
// HiddenWidget w = new();                 // 解析到 File2.cs 的 public 版本
```

`file` 与 `namespace` 的关系也要说清楚：file 类型仍然属于它所在的 namespace，只是名字的作用域被限制在文件中，所以同一 namespace 下不同文件可以有同名 file 类型。跨程序集访问 `file` 类型是不可能的，连 `InternalsVisibleTo` 也帮不上（`file` 比 `internal` 更窄）。测试与生产代码的边界实践中，推荐顺序是：优先让 API 本身可测（public 面足够）、其次用 `InternalsVisibleTo`、最后才考虑把测试塞进生产程序集。另外 `async`/`yield` 生成的编译器合成类型、`record` 生成的 `EqualityContract` 等都属于实现细节，不要当成可用 API。

📘 [MS Learn · InternalsVisibleTo](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.internalsvisibletoattribute)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的封装单位是**库（library）**，而库由 `part` 机制组成：一个主文件用 `library` 命名、用 `part 'x.dart'` 引入若干部件文件，这些部件文件开头写 `part of`，整体共享一个私有作用域。默认情况下一个 `.dart` 文件自成一个库，所以下划线私有在单文件库里的作用域就等于文件；一旦用了 `part`，私有成员会在整个 part 组内互相可见。

```dart
// shop.dart（库入口）
library shop;
part 'src/account.dart';
part 'src/report.dart';
export 'src/account.dart' show Account;    // 只导出 Account
export 'src/report.dart' hide InternalReport;

// src/account.dart
part of '../shop.dart';
class Account {
  int _balance = 0;                  // 在 shop 库的所有 part 里可见
  void _audit() {}
}
// src/report.dart
part of '../shop.dart';
void use(Account a) => a._balance += 1;   // ✅ 跨 part 访问私有
```

`part` 的代价是作用域污染：整个 part 组共享私有，一个文件里的 `_helper` 与另一个文件里的 `_helper` 会冲突（除非同名同签名），而 IDE 的重构能力也会变差。因此 Dart 官方风格指南建议优先用 `import` + `export` 组织，`part` 只在「确实需要共享私有实现」或「代码生成产物必须与主文件同库」时使用——`json_serializable`、`freezed` 这类代码生成器生成的 `.g.dart`/`.freezed.dart` 就是写成 part 的，因为它们要访问主文件里的私有字段。

```dart
// 库的对外 API 面由 export/show/hide 决定
export 'src/impl.dart' show PublicApi, helpers hide InternalApi;
// package 里 src/ 目录的约定：外部不应 import package:foo/src/xxx.dart
// 违反时由 analyzer 的 implementation_imports lint 提示
```

`package:foo/src/...` 的约定值得单独说明：pub 的 lint（`implementation_imports`）会在你从别的包 import 进 `src/` 时报信息，这是 Dart 生态里少见的、由工具链执行的封装约定；但同一个包内部跨 `src/` 目录 import 是完全正常的。Dart 3.0 的类修饰符把「继承/实现的开放面」也纳入封装讨论：`sealed` 类型只能在同库内被继承（因此可以放心用穷尽性 `switch`），`interface` 类禁止被继承只允许实现，`base` 类强制子类也标 `base`，`final` 类禁止本库之外的继承与实现。这些修饰符与 `_` 私有、`part` 作用域三者配合，才构成 Dart 完整的封装工具箱。

📘 [Dart · Class modifiers](https://dart.dev/language/class-modifiers)

{{% /tab %}}

{{% tab header="R" %}}

R 的封装单位是 **package**，边界由 `NAMESPACE` 文件与包安装后的命名空间环境共同定义。`pkg::name` 只能取到导出的名字，`pkg:::name` 无视导出清单；包内部的函数互相调用时不需要任何限定符，它们在同一个命名空间环境里。文件与包也没有绑定关系：包的 `R/` 目录下所有 `.R` 文件按字典序被 `source` 进同一个命名空间环境，所以文件不构成边界。

```r
# DESCRIPTION 与 NAMESPACE 决定包的接口
# NAMESPACE
export(Account)
export(total)
exportPattern("^[^\\.]")            # 导出全部不以 . 开头的名字
S3method(print, Account)
importFrom(stats, median)
importFrom(utils, head)
```

`.onLoad` 与 `.onAttach` 是包生命周期里的两个钩子：`.onLoad(libname, pkgname)` 在包被加载（无论是否 attach）时执行，用来初始化内部状态；`.onAttach` 在 `library(pkg)` 时执行。两者都写在包的 R 代码里、名字由约定识别（它们以小点开头，因此 `exportPattern("^[^\\.]")` 不会把它们导出），这让「包内部状态」的初始化有一个正式的落脚点。注意 `.onLoad` 里不应该调用用户的代码，也不该依赖其它包的 attach 状态。

```r
# R/zzz.R
.pkgenv <- new.env(parent = emptyenv())     # 包私有环境：内部状态的标准容器
.onLoad <- function(libname, pkgname) {
  .pkgenv$cache <- list()                   # 初始化
}
.onAttach <- function(libname, pkgname) {
  packageStartupMessage("mypkg loaded")
}
```

`.pkgenv` 这种「包内私有环境」是 R 里组织内部状态的主流写法：它是个普通环境对象，只有包内函数能通过名字取到，外部虽然能用 `mypkg:::.pkgenv` 拿到，但正常使用中被命名约定挡住。`R CMD check` 会对使用 `:::` 访问外部包未导出对象、以及对未声明的全局变量赋值给出 NOTE/WARNING，这构成了 R 生态里最接近强制的一层检查。测试方面 `testthat` 提供 `test_check("mypkg")` 在包命名空间环境内运行测试的机制，因此测试可以直接调用内部函数——这跟 Python 的处境类似：能测内部，但要不要依赖内部取决于纪律。

```r
# tests/testthat/test-internal.R
test_that("internal rate is reachable", {
  expect_equal(mypkg:::.internal_rate(), 0.1)     # 直接取内部函数
  env <- asNamespace("mypkg")
  expect_true(is.function(get("total", envir = env)))
})
```

📘 [Writing R Extensions · Package namespaces](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Package-namespaces)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的封装单位是**文件**：每个 `.zig` 文件就是一个容器（语义上等价于 struct），通过 `@import("path.zig")` 得到它的类型值，只有标了 `pub` 的声明能从外部取到。import 是**编译期**行为，路径必须是字符串字面量或 comptime 已知值，所以不存在动态导入、也不存在通过字符串在运行时找到「私有」声明的路径。`@import("std")` 是特例，指向标准库根。

```zig
// src/shop/store.zig
const std = @import("std");
pub const Store = struct {
    items: std.ArrayList(u32),                 // 字段无可见性，外部可读写
    pub fn init(allocator: std.mem.Allocator) Store { ... }
    fn rehash(self: *Store) void { ... }       // 未加 pub：仅本文件可见
};
pub fn open() Store { ... }
```

跨文件访问时，容器成员以外的名字（顶层函数、变量、类型）受 `pub` 约束，`@import` 返回的结构体类型还能被继续 `pub` 转发：`pub const store = @import("shop/store.zig");` 让上层模块把子模块暴露出去。标准库的组织方式是理解 Zig 封装的最佳例子——`std` 根文件的 `pub` 声明构成官方 API 面，`std.os` 之类的内部命名空间依赖具体版本，std 内部大量使用「文件私有 + 显式 pub 转发」来控制暴露面。

```zig
// src/root.zig
pub const store = @import("shop/store.zig");    // 转发：外部可以 mylib.store.open()

// 别的包
const mylib = @import("mylib");
// mylib.store.rehash();                        // 🛑 私有函数
```

两个约束值得注意。第一，「文件即 struct」意味着同一个文件里的所有声明共享同一个容器，没有「文件内的子模块」这回事；要再分层就只有再拆文件，或者用嵌套的 struct 容器（`pub const inner = struct { ... };`）。第二，Zig 的可见性检查在 comptime 完成，运行时没有任何反射能取到私有声明：`@field` 只能按名字取**字段**（且名字必须存在，否则编译错误），`std.meta` 的字段遍历只看得到字段、看不到函数，也没有「按名字调用函数」的内建。测试方面，Zig 允许在源文件里写 `test { ... }` 块，它们与被测代码在同一文件中，因此能直接访问私有声明——这是 Zig 里白盒测试的标准方式，不需要任何额外开放机制。

📘 [Zig · Documentation · Import](https://ziglang.org/documentation/master/#import)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的模块就是**返回一个 table**（或任意值）的 chunk，封装单位是 chunk 的词法作用域：`local` 声明的名字只在本 chunk 内可见，返回 table 的字段则完全由返回者决定。`require` 负责查找与缓存（`package.loaded`、`package.path`、`package.searchers`），同一次 `require` 只执行一次，之后的调用直接返回缓存值。因此 Lua 的模块边界有两种：真的（`local` 变量）与假的（table 里的字段）。

```lua
-- shop.lua
local M = {}                       -- 返回的 table 就是公开 API 面
local rate = 0.1                   -- 真私有：chunk 局部，外部拿不到

function M.total(n) return n * (1 + rate) end
function M.set_rate(r) rate = r end   -- 只能通过这个入口改

return M                           -- 只有 M 被暴露
```

`local` 的作用域规则是这一切的基础：`local` 声明之后到 chunk 结束（或到所在 `do` 与 `end` 围起来的块 块结束）的名字解析为局部变量，函数里的 `local` 则是每次调用新建一份。要让「模块级私有」成立，只需把私有量写成 `local` 而不是 `M._xxx`——这是 Lua 里唯一语言级、不可绕过的封装（除了 `debug` 库）。`require` 的缓存语义也有个常见陷阱：模块内的可变状态（`local state = {}`）在 `require` 缓存下是单例，如果想每个使用者各有一份，模块应该返回一个工厂函数而不是数据表。

```lua
-- factory.lua：返回工厂函数，避免模块级单例状态
return function(opts)
  local state = {}                  -- 每次调用一份，外部无法访问
  return {
    get = function(k) return state[k] end,
    set = function(k, v) state[k] = v end,
  }
end
```

`_ENV` 是 Lua 5.2+ 的环境机制，它把「全局变量」变成了对 `_ENV` 这个 upvalue 的字段访问，因此可以做到「沙箱」：给一段代码一个空 `_ENV`，它就什么全局都看不见（`setfenv` 的现代替代）。这也意味着 Lua 的「模块边界」可以通过 `_ENV` 彻底重写，但这属于高级用法，容易让调试变得困难。最后提醒一点：`package.loaded["mymod"] = nil` 可以强制下次 `require` 重新加载模块，这是测试里常用的重置手段；反过来，如果模块初始化失败抛错，`require` 不会缓存失败状态，下一次会重试。

📘 [Lua 5.5 Reference Manual · Modules](https://www.lua.org/manual/5.5/manual.html#6.3)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的封装单位完全沿用 ECMAScript：一个文件如果含顶层 `import`/`export` 就是**模块**，否则是**脚本**（所有顶层声明进入全局作用域，这是最容易踩的边界坑）。模块作用域是语言层面强制的，跨模块只能用 `export` 暴露的名字；模块之外没有「包」的概念，包边界由 `package.json` 的 `exports` 字段和解析算法定义。

```typescript
// package.json —— 决定外界能 import 到哪些路径（Node 的 exports 字段）
{
  "name": "shop",
  "type": "module",
  "exports": {
    ".": { "types": "./dist/index.d.ts", "default": "./dist/index.js" },
    "./utils": "./dist/utils.js"
  }
}
// 未列入 exports 的子路径一律不可导入：
// import x from "shop/src/internal.js"   // 🛑 ERR_PACKAGE_PATH_NOT_EXPORTED
```

`isolatedModules` 是最该打开的一项编译选项：它禁止那些「编译单文件无法确定语义」的写法——重新导出类型必须用 `export type`（否则转译器会把它当运行时值保留下来，在只做转译不类型检查的构建链里就会出错）、`const enum` 不能跨文件使用等。开启它等于向「每个文件独立转译」的现代工具链（esbuild、SWC、Vite、Babel）看齐，也让 `.d.ts` 的生成更可靠。

```typescript
// isolatedModules 下必须写清楚哪些是类型
export type { User } from "./types.js";        // ✅ 类型导出用 export type
export { Client } from "./client.js";          // ✅ 值导出
// export { User } from "./types.js";          // 🛑 isolatedModules 报错

// 声明合并 / 全局扩充：不是模块的文件才会影响全局
declare global { interface Window { appVersion: string } }
export {};                                      // 让本文件成为模块，declare global 才合法
```

类型层面还有一层「导出面」控制手段：`@internal` 注释配合 `stripInternal` 从 `.d.ts` 里剔除声明、`"types"` 条件只指向一个精简的入口声明、`/// <reference types="..." />` 决定全局类型从哪来。要记得 `package.json` 的 `exports` 是**运行时与类型解析共同遵守**的边界，而 `stripInternal` 只改声明文件——两者配合才能同时挡住「运行时 import」与「类型层面使用」。最后是路径别名（`paths`）只在类型检查与打包器里生效，不会改变运行时的解析规则，所以 tsconfig 里配的别名必须在构建产物里被正确重写，否则运行时报模块找不到。

📘 [TypeScript · Modules](https://www.typescriptlang.org/docs/handbook/2/modules.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 现在有两套模块系统：**ESM**（`import`/`export`，静态结构、顶层 `this` 是 `undefined`、严格模式）与 **CJS**（`require`/`module.exports`，动态、可条件调用、顶层 `this` 是 `module.exports`）。两者作用域模型的共同点是「模块内顶层声明不进入全局」，但 ESM 是语言级模块，CJS 只是函数包装（Node 把文件包进一个函数，`require`/`module`/`exports` 是参数），所以 CJS 里的变量其实处于函数作用域。

```javascript
// esm.mjs —— ESM：静态导入，模块作用域
export const API = "v1";              // 命名导出
export default function init() {}     // 默认导出
const internal = 1;                    // 未导出：模块外不可见（真不可见）

// cjs.cjs —— CJS：导出的对象就是对外面
const internal = 1;                    // 模块包装函数内，外部拿不到
module.exports = { api: "v1" };        // 只有这个对象暴露出去
```

ESM 与 CJS 互操作是实践中的最大痛点：CJS 可以 `require()` 一个 ESM 模块（Node 22+ 起在满足条件时支持，此前不行），ESM 可以 `import` CJS 模块（默认导出即 `module.exports`，命名导出靠静态分析尽力推断，常常推不出来）。`package.json` 的 `"type": "module"` 决定 `.js` 按哪种解析，`.mjs`/`.cjs` 则强制指定；`exports` 字段的 `import`/`require` 条件允许同一个包对两种消费方提供不同入口，这也是「双包」（dual package）问题的来源——同一个包被同时加载成 ESM 与 CJS 会导致两份模块状态，`instanceof` 判断可能失败。

```javascript
// 全局与模块作用域的差别
var leaked = 1;          // 在 CJS 里是模块包装函数的局部变量，不泄漏到 global
globalThis.shared = 2;    // ✅ 显式挂到全局
```

闭包与 IIFE 是模块系统普及之前的封装手段，今天仍然有用武之地：IIFE `(function(){ ... })()` 把私有变量关在函数作用域里、只返回公开接口；UMD 是 IIFE 的兼容版本，同时支持 AMD、CJS 与全局变量三种消费方式。要注意 ESM 的绑定是**实时（live）只读**的：导入方看到的是导出方变量的当前值，但它不能赋值，这与 CJS `module.exports` 是普通对象（可以随意改写）不同。动态 `import()` 返回 Promise，可以实现按需加载与条件加载，但它不改变模块作用域的可见性规则，只改变加载时机。

📘 [MDN · JavaScript modules](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Modules)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的封装单位是 **namespace** 与 **class**，而 namespace 只影响名字解析，不做访问控制：写了 `namespace Shop;` 之后，`Shop\Client` 仍然可以被任何代码 `new \Shop\Client()`。真正的边界靠类的 `private`/`protected` 与「自动加载器只暴露该暴露的类」这条工程约定来建立。`use` 语句是编译期的别名机制，把一个长名字导入当前文件的短名，不改变任何可见性。

```php
// src/Shop/Account.php
namespace Shop;

use Shop\Internal\Ledger;         // 别名导入，纯粹是名字便利

final class Account
{
    public function __construct(private int $balance = 0) {}
    public function total(): int { return $this->balance + (new Ledger())->fees(); }
}

// src/Shop/Internal/Ledger.php —— 目录名约定为「内部」
namespace Shop\Internal;
final class Ledger { public function fees(): int { return 1; } }
```

Composer 的自动加载是这里的关键机制：`composer.json` 的 `autoload.psr-4` 把 `Shop\` 映射到 `src/Shop/`，于是「哪个文件对应哪个类名」变成约定，任何一个类只要符合映射就能被自动加载，**不存在「这个类不可见」的机制**。想限制外界使用某个类，只能靠：把类放进 `Internal` 子命名空间并写文档、给类加 `@internal` 注解（IDE 与静态分析器会警告）、或者用 `final` + 私有构造器封住继承与实例化。

```php
/** @internal 这个类不是公开 API，请勿依赖 */
final class Ledger { }

// 想封住实例化：私有构造器 + 静态工厂
final class Config
{
    private function __construct(private array $data) {}
    public static function fromArray(array $d): self { return new self($d); }
}
```

`@internal` 注解（配合 Psalm、PHPStan 的 `@internal` 支持）能做到「跨包引用内部符号就报错」，这是 PHP 里最接近编译期边界的东西；它需要静态分析器才生效，运行时毫无作用。命名空间还有一个容易踩的细节：`use function` 与 `use const` 是分别导入的，不写 `function`/`const` 关键字只会导入类名；而没写 `use` 时，未限定的函数名会先在本命名空间找、再回退到全局，类名则**不会**回退到全局（必须写 `\` 前缀或 `use`），这个不对称经常导致「明明有这个类却报找不到」。8.4 起的属性钩子让 getter/setter 可以内联在属性声明里，这让「私有属性 + 公开访问器」的样板代码大幅减少，也顺便让可见性声明更集中。

📘 [PHP · Namespaces](https://www.php.net/manual/en/language.namespaces.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的封装单位是 **class/module** 与**文件**，没有命名空间式的访问控制：`module Shop` 只是常量命名空间，`Shop::Ledger` 从任何地方都能引用，除非用 `private_constant` 关掉。`require` / `require_relative` 是文件加载机制，加载进来的常量全部进入全局常量表，所以文件本身不构成边界。常量查找遵循词法作用域链（`Module.nesting`）再向上到祖先链，最后到 `Object`，这也是 Ruby 里常量解析最容易困惑的地方。

```ruby
# shop.rb
module Shop
  VERSION = "1.0"
  private_constant :VERSION          # 关掉 Shop::VERSION 的直接访问
  class Account
    def initialize(owner) = @owner = owner
  end
  module Internal                   # 命名约定：Internal 子模块表示内部实现
    class Ledger
      def fees = 1
    end
  end
end

Shop::Account.new("ada")             # ✅
Shop::Internal::Ledger.new           # ⚠️ 能引用，只是约定上不该
Shop::VERSION                        # 🛑 NameError: private constant
Shop.const_get(:VERSION)             # "1.0"   反射照样拿得到
```

常量查找的规则值得单独记：`Module.nesting` 里的词法作用域优先级最高，然后是包含它的模块的祖先链（`Module#ancestors`），最后才到顶层 `Object`；因此在一个嵌套类里引用 `Ledger` 可能解析到完全出乎意料的地方，写 `Shop::Internal::Ledger` 或 `::Ledger` 才确定。`private_constant` 只限制直接写 `Shop::VERSION` 这种路径访问，`const_get` 与 `Module#const_source_location` 之类的反射 API 依旧畅通——这一点跟 Ruby 的其它私有机制完全一致。

```ruby
module Outer
  class Inner
    def where = Module.nesting     # [Outer::Inner, Outer]
  end
end
Outer::Inner.new.where             # 词法链：先 Outer::Inner，再 Outer
```

自动加载与代码组织的现代做法是 Zeitwerk（Rails 默认）：它按「文件名 → 常量名」的约定映射目录结构，`Shop::Internal::Ledger` 必须位于 `shop/internal/ledger.rb`，并且鼓励（但不强制）用 `private_constant` 或把内部类放进独立的 `Shop::Internal` 模块来标示边界。测试与生产的边界在 Ruby 里没有语言支持，`RSpec` 常见做法是用 `send` 调用私有方法、用 `stub_const` 替换常量，社区共识是「允许测试碰内部，但一旦测试因内部重构而破裂，就要反思这个内部是否真的是内部」。

📘 [Ruby · Modules and constants](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 约定式私有

没有强制机制的语言怎么表达「这是内部实现」？答案通常是三件套：**命名约定**（`_` 或 `.` 前缀）、**作用域技巧**（闭包、局部表、`static`）、以及**导出清单**（`__all__`、`NAMESPACE`、`export`）。这一节的重点是把每种语言的「约定」与「真边界」区分开，并说明闭包封装模式（IIFE、返回对象、WeakMap）为什么至今仍然必要——因为在多数动态语言里，闭包是唯一语言级不可绕过的隐私单位。判断标准很简单：如果一段代码能在不改动被封装模块的前提下读到内部状态，那它就是约定式私有。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 里没有「约定式私有」的必要，因为默认就是私有、且编译期强制。它唯一接近约定的东西是下划线前缀用于**抑制未使用警告**（`let _unused = ...`、参数名 `_x`），以及 `#[doc(hidden)] pub` 这种「技术上公开、文档里不写」的半公开标记。模块私有的强制来自编译器，所以 Rust 不需要靠命名来表达边界。

```rust
pub struct Engine {
    rpm: u32,                    // 私有字段：模块外不可访问（编译期）
    _cache: Vec<u32>,            // 下划线前缀：抑制 dead_code 警告，不是访问控制
}

#[doc(hidden)]
pub fn internal_helper() {}      // 外部能调用，但不出现在文档里（给宏用）

fn private_impl() {}             // 真正的私有：同模块及其后代可见
```

`#[doc(hidden)]` 是宏作者的标准做法：`pub` 是必须的，因为宏展开后的代码在**调用者 crate** 里要能引用这个项，而 `#[doc(hidden)]` 让它从 rustdoc 里消失、从心理上标记为「不承诺兼容」。这跟 Python 的 `_` 前缀解决的是同一个问题，但 Rust 至少有编译器保证「文档里没有的东西在跨 crate 时也可能真的不可达」——只要不加 `pub` 就行。

```rust
// 惯用法：内部实现放私有模块，公开面全在 crate 根用 pub use 拼出来
mod internal { pub struct Impl; }
pub use internal::Impl as PublicApi;   // 外部只看到 PublicApi
```

与「约定式」相关的另一个 Rust 惯例是 `_` 模式绑定：`let _ = expr;` 立即丢弃值（对带 `Drop` 的类型有实际语义差异），`let _x = expr;` 是绑定但抑制警告，两者不同。这个差异跟访问控制无关，但在审阅「以下划线表示内部」的代码时要留意——Rust 里下划线在**绑定位置**有语义，而在**标识符名字**里只是风格。

📘 [Rust Reference · Visibility](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的约定式私有已经被语言机制基本取代：`fileprivate`、`private`、`package` 三个级别覆盖了「文件内 / 类型内 / 包内」三种需求，因此社区不再需要靠 `_` 前缀表达内部。Swift 里常见的前导下划线主要出现在**标准库与编译器生成的 API** 上（例如 `_print_unlocked`、`@_spi`、`__consuming`），语义是「非官方 API、随时可能变」，而不是「私有」。

```swift
struct Account {
    private var balance = 0              // 语言级：类型内
    fileprivate var cache: Int? = nil     // 语言级：文件内
    package var shared = 0                // 语言级：包内（需 -package-name）
    var balanceValue: Int { balance }     // 公开只读
}

// @_spi：官方「非公开但有意的口子」，只有显式 import 才可见
@_spi(Debugging) public func dumpState() {}
// 使用方：@_spi(Debugging) import MyModule
```

`@_spi(group)` 是 Swift 里最接近「约定式私有」的官方机制，名字里的下划线表示它是非稳定的编译期特性：它把 API 放在模块正常接口之外，只有调用方用 `@_spi(group)` 标注 import 才能用。SE-0386 的提案里把它列为 `package` 的替代方案并明确否定了它，理由是 SPI 面向「必须跨分发边界的特定客户」，而模块内部共享不需要这么重的仪式。实践建议：模块内的共享一律 `internal`，包内跨模块用 `package`，文件内用 `fileprivate`，不要用 `_` 前缀造第二套约定——Swift 的编译器不会因为你加了下划线就少给你一层保护，反而会让 API 面变得混乱。

```swift
// 反例：靠下划线表达「内部」的代码在 Swift 里没有额外保护
func _internalHelper() {}      // 仍然是 internal，同模块谁都能调
// 正解：
internal func internalHelper() {}
```

测试与内部 API 的关系也在这里收束：`@testable import` 打开的是 `internal` 面，`package` 面在同一个 SwiftPM 包里对测试 target 也是可见的（测试 target 与主 target 同包），`private`/`fileprivate` 面则永远只能靠同文件才能碰到。所以 Swift 的项目里真正需要「约定」的地方很少，反而常见的是「不小心把 `internal` 当成了私有」——一个 Gradle 模块之外的同事 `import` 你的 framework 时看不到 `internal`，但同一个库里的另一个文件全都看得到。

📘 [Swift · Access Control](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/accesscontrol/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 里几乎没有「约定式私有」的位置：**小写标识符 = 包内**这条规则由编译器强制，属于规则而不是约定。最容易被误当成「约定」的是下划线前缀，但它同样**不是**靠自觉的约定——Go spec 明确规定下划线 `_` 按小写字母处理，导出性只看标识符首字符是否为 Unicode 大写字母（Lu），所以 `_cache`、`_helper` 与 `cache`、`helper` 一样都是未导出的，编译器与 `reflect` 都按未导出名对待。真正属于「约定」的只有两类：`internal` 目录（由构建工具强制）与生成代码的文件名/文件头标记（工具链共同遵守的文本约定）。

```go
package store

var _cache = map[string]int{}       // ✅ 未导出：spec 把 `_` 当作小写字母
var cache = map[string]int{}        // ✅ 未导出（惯用写法：首字母小写）
var Cache = map[string]int{}        // 导出：首字符是 Unicode 大写字母
func _helper() {}                   // ✅ 未导出，但下划线前缀不符合 Go 命名习惯
func helper() {}                    // ✅ 未导出且惯用

// 命名约定（非语言强制）：
// - internal/ 目录：构建工具强制，只能被父目录子树内的包导入
// - 生成代码用 zz_generated_*.go 命名，并在文件头写上官方约定的 generated code 标记注释
```

Go spec 对导出的定义是「标识符的第一个字符是 Unicode 大写字母（Unicode 类别 Lu）」，而同一页的 Letters and digits 一节明确规定下划线 `_`（U+005F）按小写字母处理，所以 `_cache`、`_mask` 与 `cache`、`mask` 一样都不可导出——下划线前缀在 Go 里**确实能藏住名字**，而且藏得比 Python 更硬（编译器强制），只是它不符合 Go 的命名习惯（`golint`/`staticcheck` 会提示），惯用写法是首字母小写。跨语言写作时真正容易搞反的是这一点：Python 的 `_x` 只是社会约定，Go 的 `_x` 是编译期强制的未导出名。

```go
type Config struct {
    Timeout int              // 导出
    retries int              // 未导出
    _mask   uint32           // ✅ 也未导出：首字符 `_` 按小写字母处理
}
```

Go 里真正需要「约定」的场景是「包内分层」：同一个包里想区分「给包外用的」与「包内其它文件用的」，语言层只有导出/未导出两档，所以社区做法是把内部实现拆成 `internal` 子包，或者用注释分组（`// Package-level helpers`）。生成代码的识别也靠命名约定：文件头那行官方的 generated code 标记注释（约定的正则形如 `^// Code generated .* DO NOT EDIT\.$`，必须出现在最前面）由 `gofmt`、`go vet` 与各类 lint 识别，是 Go 生态里少见的、工具链共同遵守的文本约定，比文件名的约定更可靠。

📘 [Go spec · Exported identifiers](https://go.dev/ref/spec#Exported_identifiers)

{{% /tab %}}

{{% tab header="Python" %}}

Python 是「约定式私有」的典型代表，语法层面只有三条相关规则：单下划线前缀表示内部、双下划线触发名称改写、`__all__` 控制 `import *`。`typing.Final` 与 `@final` 是被类型检查器执行的静态约束，运行时毫无作用；`__slots__` 是唯一在运行时生效的结构限制（禁止动态添加属性），但它不保护已有属性的值。

```python
from typing import Final, final

class Repo:
    CACHE_SIZE: Final = 128          # Final：mypy 禁止重新赋值，运行时只是注解
    def __init__(self) -> None:
        self._items: list[int] = []   # 约定私有
        self.__secret = "s3"          # 改写成 _Repo__secret

    @final
    def freeze(self) -> None: ...     # 子类覆写会被 mypy 报错

r = Repo()
r._items.append(1)                    # ⚠️ 约定被打破：可以，只是不该
r._Repo__secret = "x"                 # ⚠️ 名称改写不是保护
print(Repo.CACHE_SIZE, r._items)      # 128 [1]
```

mypy/pyright 的「私有」检查是这套约定的实际价值所在：访问 `r._items` 时，`mypy` 只在**跨模块**使用时才报 `error: "Repo" has no attribute ...`（同模块内不报），访问 `r.__secret` 在类外会报错（因为改写过），覆写 `@final` 方法会报错，重新赋值 `Final` 属性会报错。也就是说「约定」在带类型标注的代码里获得了工具级强制，这是 Python 近年最重要的实践变化：把 `_` 与 `@final` 当机器可执行的文档来用。

```python
# 名称改写的规则细节：最多一个尾随下划线，前导下划线会被去掉参与类名构造
class _Foo:                 # 前导下划线在类名里被去掉 → _Foo__x
    __x = 1                 # 实际名字 _Foo__x
class Foo_:
    __x = 1                 # 实际名字 _Foo___x
class Foo:
    __x_ = 1                # 尾随一个下划线：不改写，就叫 __x_
    __x__ = 1               # 前后双下划线（dunder）：不改写
```

`__all__` 的准确语义是「`from module import *` 时导出哪些名字」，它不影响 `import module` 之后的属性访问，也不影响 `from module import name` 这种显式导入（显式导入永远可以取到未列入 `__all__` 的名字）。闭包封装在 Python 里用得相对少，因为类与模块已经提供了足够的作用域；最常见的用法是装饰器内部的 `wrapper` 用 `functools.wraps` 保留元信息，以及工厂函数返回的对象把状态关在闭包里。

```python
def make_counter():
    n = 0                       # 闭包变量：外部只能通过返回的闭包访问
    def inc() -> int:
        nonlocal n
        n += 1
        return n
    return inc

c = make_counter()
print(c(), c())                 # 1 2
# n                            # 🛑 NameError：确实拿不到
print(c.__closure__[0].cell_contents)   # 2  ⚠️ 但反射能翻出来
```

闭包在 Python 里也不能算「真私有」：函数的 `__closure__` 元组里每个 cell 的 `cell_contents` 就是 upvalue 的值，`inspect` 与 `ctypes` 还能做更深入的内存操作。所以 Python 的封装强度最终取决于「实现是否在 C 扩展里」——把关键逻辑写进 C/Rust 扩展、只暴露 Python 层接口，是 Python 里唯一接近硬边界的手段。

📘 [Python Reference · Private name mangling](https://docs.python.org/3/reference/expressions.html#private-name-mangling)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 有编译器强制的可见性，因此不需要靠 `_` 前缀表达内部；社区里下划线主要出现在**属性委托的 backing property**（`private val _state = MutableStateFlow(...)`，公开 `val state: StateFlow<...> = _state`）以及 `_` 作为未使用参数的占位（lambda 单参数可以用 `it`，多参数用 `_` 只能用于解构声明）。这些都是风格约定，不是访问控制。

```kotlin
class ViewModel {
    private val _state = MutableStateFlow(0)      // backing property：约定私有
    val state: StateFlow<Int> = _state.asStateFlow()   // 对外只读
    fun bump() { _state.value += 1 }
}

// 解构声明里的 _ 表示跳过
val (a, _, c) = Triple(1, 2, 3)
println("$a $c")                                  // 1 3
```

Kotlin 里真正需要注意的「约定 vs 强制」是 `internal` 的边界：它在 Gradle 模块内强制，但**跨模块编译时仍然会被 Kotlin 编译器检查**，所以比 Java 的包私有更严格；而一旦有 Java 消费方，`internal` 就退化成「名字难看但可用」的约定。官方给出的应对是 `@JvmSynthetic`（对 Java 不可见）与 `@JvmName`（改回好看的名字），但它们都只是注解层面的处理，真正的边界仍然由 Kotlin 编译器在编译 Kotlin 代码时执行。测试 source set 与主 source set 共享 `internal` 面这一点也常被忽略——`src/test/kotlin` 里的测试能直接访问 `internal` 声明，因为 Gradle 把它们配置成同一个编译模块（`associate`）。

```kotlin
// 反射也能绕过 Kotlin 的 private（JVM 平台）
val f = Repo::class.java.getDeclaredField("secret")
f.isAccessible = true
val v = f.get(repo)          // ⚠️ private 在 JVM 上只是编译期修饰
```

需要特别澄清一点：Kotlin 的 `private` 在编译到 JVM 后是字节码里的 `private` 标志，Java 反射加 `setAccessible(true)` 就能突破，跟 Java 自己的 `private` 一样。Kotlin/JS 与 Kotlin/Native 的私有语义则由各自的编译后端实现，通常更严格（JS 后端会做重命名），但这些都不是语言规范承诺的「安全边界」。所以 Kotlin 项目里 `private` 的定位应该是「编译期契约」：它能防止团队内部的误用，不能防止有心的访问。

📘 [Kotlin · Visibility modifiers](https://kotlinlang.org/docs/visibility-modifiers.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的「约定式私有」有一个正式的名字：**包私有**（package-private，不写修饰符）。它经常被当作「模块内部的公开」使用——同一个包内的所有类互相可见，这在 JDK 内部代码里极为常见（`java.util` 里大量包私有类与包私有字段）。JDK 9 引入模块后，包私有被 `exports` 再包了一层，于是「包内公开、对外隐藏」终于有了一个完整表达。另外 Java 9 起接口可以有 `private` 方法，这是接口内部拆分的官方工具。

```java
package java.util;             // JDK 内部包：不 exports，外部无法访问
class ArrayList {              // 包私有类：java.util 之外看不到
    transient Object[] elementData;   // 包私有字段：同包可访问
    private int size;                 // 私有字段（同类可访问）
}

// 应用代码里的常见用法
package shop.internal;
class Helper { }               // 包私有：约定为「模块内部」
public interface Api {
    default void run() { check(); }     // ✅ 接口 default 方法调用私有方法
    private void check() {}             // Java 9+：接口私有方法
}
```

包私有作为「约定」的可信度取决于**包名是否被独占**：如果同一个包名被多个 jar 提供（split package，JPMS 明确禁止，但 classpath 世界允许），那么包私有就变成了跨 jar 的公共 API。这正是 JDK 团队推动模块系统的重要动因之一——`sun.misc.Unsafe` 之类的类在 classpath 时代只是「名字看起来像内部」，实际上谁都能用。`@apiNote`、`@implSpec`、`@implNote` 这类 Javadoc 标签是另一层约定：`@implSpec` 明确告诉实现者「覆写时必须遵守这个契约」，「约定」由此变成文档化承诺。

```java
// Javadoc 里的层次：约定靠文档，强制靠模块
/**
 * @apiNote 这个方法的调用方注意事项
 * @implSpec 子类覆写时应保持的不变量
 * @implNote 当前实现的具体细节，可能变化
 */
public void process() {}
```

反射是约定式私有的终点：`Field.setAccessible(true)` 能打开任何应用类的 `private` 字段（因为未具名模块默认全开），但它们一旦指向 JDK 内部包，在 Java 17 之后会被强封装拒绝。`MethodHandles.privateLookupIn` 是 JDK 9 提供的「合法突破」通道，需要目标模块对调用方 `opens`；`VarHandle` 则提供字段级的读写句柄，同样受模块边界约束。所以 Java 的封装是「三层叠加」：类修饰符（编译期）、包（编译期 + 构建约定）、模块（编译期 + 运行期强封装），其中最硬的一层是模块。

📘 [JLS · Access Control](https://docs.oracle.com/javase/specs/jls/se25/html/jls-6.html#jls-6.6)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的约定式私有有两条主流写法：把内部实现放进匿名 namespace 或加 `static`（这两者是语言级的内部链接，比约定硬），以及在名字上加 `_` 后缀（Google 风格用 `member_`、LLVM 风格用 `Member`）或 `impl` 后缀。真正的成员可见性由 `private`/`protected` 表达，但因为编译期检查可被预处理绕过，C++ 里「约定」常常被用来表达比 `private` 更弱的层次，例如「公开但不建议使用」。

```cpp
namespace shop {
namespace {                       // 匿名 namespace：内部链接，本翻译单元可见
int hidden_counter = 0;
void bump() { ++hidden_counter; }
}

class Widget {
public:
    int api() const;                        // 稳定 API
    // 约定：detail 命名空间里的东西不承诺兼容
    namespace detail { int raw(); }
private:
    int secret_ = 42;                       // 语言级私有
};
}

// 头文件里常见的「公开但内部」标记
namespace shop::detail {                    // 命名约定：detail = 实现细节
struct Impl;
}
```

`detail` 命名空间是 C++ 生态里最通行的约定（Boost、{fmt}、nlohmann/json 都用它）：它把实现在物理上放在公开名字旁边，靠命名告诉使用者「别依赖」。这跟 Python 的 `_` 前缀是同一个思路，区别是 C++ 里可以同时用 `namespace {}` 或 `static` 给真正需要隐藏的东西硬边界，只是代价是内联与模板实例化受限。`[[deprecated]]`（C++14）与 `[[deprecated("msg")]]` 是给「不想让你用但还留着」的 API 加编译期警告的官方手段，比纯命名约定强一档。

```cpp
[[deprecated("use api() instead")]]
int old_api();          // 调用时报编译警告（可用 -Wno-deprecated-declarations 关掉）
```

另一个现实是 ODR（One Definition Rule）让「约定」在 C++ 里有额外风险：同一个类的定义在头文件里必须对所有翻译单元完全一致，任何通过宏改可见性的做法都可能让不同 `.cpp` 看到不同的类布局，从而产生未定义行为。所以 C++ 的封装策略通常是「头文件尽量只暴露接口（Pimpl、抽象基类），实现细节放进 `.cpp` 或模块内部」，而不是依赖命名约定——这跟动态语言的思路正好相反。

📘 [cppreference · Namespaces and internal linkage](https://en.cppreference.com/w/cpp/language/namespace)

{{% /tab %}}

{{% tab header="C" %}}

C 是约定式私有的发源地之一：`static` 给内部链接（语言级、链接器强制），而 `_` 前缀是历史遗留的命名习惯。关键是 C 标准对下划线开头的标识符有**保留规则**：任何位置以两个下划线或「下划线 + 大写字母」开头的标识符、以及文件作用域以单个下划线开头的标识符，都保留给实现使用，用户代码使用它们是未定义行为。所以「内部函数加一个下划线」在 C 里是不安全的，正确做法是加项目前缀。

```c
/* 保留标识符（不要用） */
int __reserved;              /* 🛑 双下划线开头：保留给实现 */
int _Reserved;               /* 🛑 下划线 + 大写：保留给实现 */
int _local;                  /* ⚠️ 文件作用域下划线 + 小写：也保留给实现 */
/* 正确做法：项目前缀 */
int shop_internal_counter;   /* ✅ 语义清晰且不侵入保留空间 */
```

`static` 与 `_` 前缀解决的是不同层次的问题：`static` 是**链接期**的真边界（别的翻译单元链接不到这个名字），`_` 前缀只是给人看的。所以真正想把实现藏起来，只能把定义放进 `.c` 并声明 `static`，头文件里连名字都不出现。工程上还有 `attribute` 层面的手段：`__attribute__((visibility("hidden")))`、`-fvisibility=hidden`、以及 `static inline` 放头文件（后者是为了性能而不是封装）。

```c
/* api.h —— 只暴露接口 */
#ifndef SHOP_API_H
#define SHOP_API_H
typedef struct shop_ctx shop_ctx;         /* 不完整类型：字段彻底隐藏 */
shop_ctx *shop_open(const char *dsn);
void shop_close(shop_ctx *);
#endif

/* api.c —— 实现与内部符号 */
struct shop_ctx { void *impl; int mode; };        /* 完整定义只在这里 */
static int validate(const char *dsn) { return dsn != 0; }
static void *g_pool;                              /* 内部状态 */
shop_ctx *shop_open(const char *dsn) { ... }
```

`const` 与 `_` 前缀类似，常被误当作保护：`const` 只约束编译期直接写入，`memcpy((void *)&c, ...)` 或强制转换都能改（属于未定义行为，但编译器不一定拦住）。真正需要跨模块隐藏状态的 C 代码，标准答案是「不完整类型 + 分配函数」，让调用方连 `sizeof` 都算不出来。C23 之后 `typeof`、`nullptr`、`constexpr` 等新特性都没有改变这套模型——C 的封装一直是构建与链接层面的工程问题，而不是类型系统的问题。

📘 [C standard · Reserved identifiers (C23 7.33)](https://en.cppreference.com/w/c/language/identifier)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 没有强制私有，靠两条约定：下划线前缀表示内部实现，以及「不在手册里的就不是公共 API」。1.11 引入 `public` 关键字之后，第二条约定终于有了机器可读的版本——`public` 只是把名字标记为公共 API，不影响命名空间，但让 `Base.ispublic` 与 REPL 帮助系统能给出准确提示。

```julia
module Shop
export total                  # 导出：using Shop 时带入
public Account, rate          # 1.11+：声明为公共 API，但不带入命名空间

struct Account
    balance::Int
end
total(a::Account) = a.balance
rate() = 0.1
_round(x) = round(x; digits = 2)   # 下划线约定：内部
end

Shop.Account                    # ✅ 限定名永远可用
Shop._round(1.234)              # 1.23  ⚠️ 下划线挡不住任何人
Base.ispublic(Shop, :rate)      # true
Base.ispublic(Shop, :_round)    # false
```

`public` 的语法限制要记清：它只能出现在模块或文件的**顶层**（不能写在函数体里、不能写在 `let`/`begin` 里），官方说明这是为了兼容 1.11 之前把 `public` 当普通变量名的历史代码，并提醒别再把 `public` 用作用户标识符。要在 `VERSION < v"1.11"` 的环境里用同样的能力，官方给的方案是 Compat.jl 的 `@compat public a, b, c` 或版本判断加 `eval(Meta.parse("public a, b, c"))`。

```julia
# 让工具链识别「内部」的另一条路：文档字符串里显式标注
"""
    _round(x)

内部辅助函数，不保证兼容性。
"""
_round(x) = round(x; digits = 2)
```

闭包与局部作用域在 Julia 里的地位跟 Python 类似：`let` 块与函数内部的局部变量天然不可从外部访问，工厂函数返回的闭包把状态关起来是可行的（`Counter() = (n = Ref(0); () -> (n[] += 1))`），但 `Base.uncompiled`、`fieldnames`、`getfield` 这些反射工具依旧能把结构翻出来，所以 Julia 的封装强度跟 Python 是同一量级。工程上的关键是纪律：包作者在 `CHANGELOG` 与文档里明确哪些是 API，用 `public`/`export` 标注，剩下的用下划线，用户则养成「非 `public` 名字升级时不保证兼容」的预期。

📘 [Julia 1.11 Highlights · New `public` keyword](https://julialang.org/blog/2024/10/julia-1.11-highlights/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的 `internal` 是语言级强制（编译期），但它在实践中经常被当作「程序集内的约定」使用：程序集往往是一个 NuGet 包，所以 `internal` 的语义就是「不对外承诺」。`InternalsVisibleTo` 让测试可以看进来，代价是开放整个 `internal` 面。另外 C# 里也有 `_` 前缀约定（私有字段 `_name` 是官方代码风格建议之一），但它纯粹是命名风格，与 `internal`/`private` 的表达能力无关。

```csharp
namespace Shop;

public class Account
{
    private int _balance;              // 字段下划线前缀：官方命名规范建议
    internal int Pin { get; set; }      // 程序集内可见（编译期强制）
    public string Owner { get; } = "ada";

    private protected int Cap = 50;     // 本程序集 + 派生类（交集）
    protected internal int Limit = 100; // 本程序集 或 派生类（并集）
}

// 测试项目通过程序集特性看进来
// [assembly: InternalsVisibleTo("Shop.Tests")]
```

`internal` 与「约定」的差别在于**谁来看得见**：`internal` 是编译期强制的程序集边界，跨程序集无法引用（除非 `InternalsVisibleTo`）；而下划线前缀没有任何强制，同程序集内谁都能访问。C# 里还有几个半约定标记：`[EditorBrowsable(EditorBrowsableState.Never)]` 让 IDE 的补全不显示（但不影响编译）、`[Obsolete("...", error: true)]` 让使用变成编译错误、`[RequiresPreviewFeatures]` 需要显式开启预览特性才能用。这些注解的共同点是「只影响工具体验与编译告警」，不改变实际的访问权限。

```csharp
using System.ComponentModel;

[EditorBrowsable(EditorBrowsableState.Never)]
public void LegacyHelper() { }        // IDE 补全里隐藏，编译仍可通过

[Obsolete("Use Total() instead", error: true)]
public void OldTotal() { }            // 使用即编译错误
```

程序集拆分是 C# 里控制内部面的主要手段：把实现放进 `Shop.Core`、只把接口类暴露在 `Shop.Api` 里，用 `internal` 加上 `InternalsVisibleTo` 组合精确控制谁能看到。这与 Java 的「模块 + 包私有 + exports」思路一致，但 C# 的边界是程序集（DLL 文件），粒度比 JPMS 模块粗，比 package 细。要注意 `InternalsVisibleTo` 的开放是**单向且全局**的：被点名的程序集能看到全部 `internal`，不能只开放一部分，这是它跟 Swift 的 `package` 或 C# 的 `file` 之间最大的表达力差距。

📘 [MS Learn · Access modifiers](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/classes-and-structs/access-modifiers)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `_` 前缀**不是约定，而是真正的库级私有**：编译器会检查，跨库引用直接编译失败。这是 Dart 相对 Python 最大的优势，也让 Dart 里几乎没有「约定式私有」的需求。真正剩下靠约定的部分有两个：`src/` 目录（包内部实现，靠 `implementation_imports` lint 提示）与 `@internal` 注解（`meta` 包里提供，配合 analyzer 报错）。

```dart
// lib/src/internal.dart —— src/ 目录：约定为包内部实现
class Ledger {
  int fees() => 1;
}

// lib/shop.dart —— 公开入口：只导出要暴露的东西
export 'src/account.dart' show Account;
export 'src/report.dart' hide InternalReport;
// 外部写 import 'package:shop/src/internal.dart' 会触发 implementation_imports lint
```

`@internal` 是 Dart 里最接近「强制约定」的注解：来自 `package:meta`，当它被用在库的**公开 API** 上时 analyzer 会报 `invalid_use_of_internal_member`（需要开启相应 lint/诊断规则），前提是消费方也启用 analyzer。它的语义是「标为内部，跨包使用就报错」，与 Python 的 `@final` 一样属于「工具级强制、语言级不强制」。跟 `_` 的区别是 `@internal` 用在**导出**的成员上（想公开但不想被跨包用），而 `_` 是直接不导出（物理上不可见）。

```dart
import 'package:meta/meta.dart';

@internal
class Ledger {                    // 跨包使用 analyzer 会报 invalid_use_of_internal_member
  int fees() => 1;
}

class Account {
  int _balance = 0;               // ✅ 真私有：跨库连编译都过不去
  void _audit() {}
}
```

闭包在 Dart 里也能做真私有，但用得比 JavaScript 少得多，因为 `_` 已经解决了大部分问题；常见的闭包用法是把状态关在 `StatefulWidget` 的 `State` 里，或者用 `late final` + 初始化函数模拟惰性单例。需要「会话级」私有状态时，Dart 社区更愿意用私有字段 + `Zone`/`InheritedWidget` 这样的框架机制，而不是闭包。总结 Dart 的位置：它的 `_` 比 Python 硬（编译期、跨库不可见），比 Rust/Go 软（没有类型级、字段级的区别），在库边界上是本页里少有的「约定与强制几乎重合」的语言。

📘 [Dart · Privacy](https://dart.dev/language/libraries#privacy)

{{% /tab %}}

{{% tab header="R" %}}

R 的约定式私有有两套并存的规则：`NAMESPACE` 的 `exportPattern` 用正则过滤导出面（社区惯例是排除以 `.` 开头的名字），以及对象系统各自的私有表达（R6 类的 `private`、`setClass` 的槽位、`environment` 封装）。`.onLoad`/`.onAttach` 这类以小点开头的钩子函数正是这套约定的产物——它们必须是包内可见的，但不该出现在导出面里。

```r
# R/zzz.R —— 以小点开头：约定为内部
.pkgenv <- new.env(parent = emptyenv())
.onLoad <- function(libname, pkgname) { .pkgenv$n <- 0 }

# NAMESPACE 里的配套写法
exportPattern("^[^\\.]")     # 导出所有不以 . 开头的名字：自动排除 .pkgenv / .onLoad
```

`exportPattern` 的语义是「用正则匹配名字来决定导出」，因此它是**约定驱动**的：只要内部函数不以 `.` 开头就会被意外导出，反过来 `exportPattern("^[^\\.]")` 也会把本来想隐藏的、不以点开头的辅助函数一起暴露。更可控的写法是显式列出 `export(...)`，然后用 `R CMD check` 的「未导出对象在文档里」检查来兜底。R6 类（`R6::R6Class`）提供了 `private` 参数，是 R 生态里少数真正成体系的可见性模型，它的实现是把私有成员放进封闭环境，公开方法通过闭包捕获环境来访问——本质上是闭包封装模式在 R 里的落地。

```r
Counter <- R6::R6Class("Counter",
  private = list(
    n = 0,                                # 私有字段
    bump = function() private$n <- private$n + 1  # 私有方法
  ),
  public = list(
    inc = function() { private$bump(); invisible(self) },
    value = function() private$n
  )
)
c1 <- Counter$new()
c1$inc()
c1$value()            # 1
c1$n                  # 🛑 NULL：private 字段不在公开面上
```

值得强调的是 R 里环境的可操作性让「私有」几乎总能在运行时被打破：`assignInNamespace` 能替换包内函数，`environment(f)` 能拿到函数的闭包环境并直接 `assign` 新值，`unlockBinding` 能解开锁定绑定。所以 R 包的内部实现更像「源码可读、但不承诺兼容」的开放实现，而不是黑盒。生产实践上，团队内部分享内部函数时应该走「包内调用 + 文档说明」，跨包调用才是需要警惕的信号（`R CMD check` 的 NOTE 正是为此设计的）。

📘 [Writing R Extensions · NAMESPACE](https://cran.r-project.org/doc/manuals/r-release/R-exts.html#Package-namespaces)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的可见性是语言级强制的（`pub` 与文件私有），所以几乎没有「约定式私有」的位置。剩下的是官方风格指南的命名约定：类型用 `TitleCase`（即 PascalCase）、函数用 `camelCase`（返回类型本身的构造器也用 `TitleCase`）、其余包括变量与常量一律 `snake_case`；`std` 内部则用 `std.os`、`std.posix` 这类命名空间表示「平台/内部实现」。这些约定由 `zig fmt`（只管格式，不管命名）与代码评审维护，与访问控制无关。

```zig
// 风格约定（官方 style guide 的 Names 一节）
const MyStruct = struct {              // 类型：TitleCase
    field: u32,                         // 字段：snake_case
    const max_size = 1024;              // 常量：snake_case（与变量同类）
    fn helper(self: MyStruct) void {}   // 函数：camelCase
};

// std 内部的层级命名（非强制，靠命名表达「这是内部实现」）
// std.os.linux.*  /  std.posix.*  /  std.crypto.*
```

`std` 内部有一个值得学习的做法：`std` 的根文件只 `pub` 出稳定的门面，具体实现分散在子文件里，用 `pub const` 逐层转发；当某个 API 被判定不稳定时，标准库把它从 `std` 根移除或改名，而不是加 `_` 前缀。Zig 0.15 的 `std.ArrayList`（非托管版本）就是这类演进的例子——API 名称本身承载兼容性承诺，而不是靠命名前缀。

```zig
// std 门面模式：根文件转发，实现藏在子文件
pub const ArrayList = @import("array_list.zig").ArrayList;
pub const StringHashMap = @import("hash_map.zig").StringHashMap;
// 子文件里未 pub 的辅助函数对外不可见（编译期强制）
```

构建层面还有一层「约定」：`build.zig` 里通过 `addModule`/`addImport` 决定哪个模块能被 import，以及是否用 `-D` 选项开启 `std.testing`。测试的写法是 `test "name" { ... }` 块，它们与被测代码在同一个文件里，所以能访问私有声明——Zig 不需要 `@testable` 之类的机制，因为「测试代码在源文件里」本身就是语言设计的一部分。要测试跨文件的私有实现，Zig 的思路是显式导出一个 `pub const testing = struct { ... }` 子命名空间，把测试用的入口集中声明，这比让测试 crate 到处摸私有要清晰。

📘 [Zig · Style Guide](https://ziglang.org/documentation/master/#Style-Guide)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 是「约定式私有」与「真私有」界线最清楚的语言：`_` 前缀是纯约定，闭包 upvalue 是真私有，`local` 是语言级作用域。三个工具各司其职，选错了就会得到「看起来封装了、其实一戳就破」的代码。另一个常被忽略的事实是 Lua 里的「类」本身就是约定：`Account = {}; Account.__index = Account` 是一套手工搭建的元表协议，不是语言内建。

```lua
-- 约定式：字段名带下划线
local M = {}
function M.new(balance) return setmetatable({_balance = balance}, M) end
M.__index = M
function M:get() return self._balance end
-- 任何持有对象的人都能：obj._balance = 999

-- 真私有：闭包 upvalue + 返回表
local function new(balance)
  return {
    get = function() return balance end,
    add = function(n) balance = balance + n end,
  }
end
local a = new(10)
a.add(5)
print(a.get(), a._balance)      -- 15 nil
```

闭包方案的另一个变体是「私有方法也放闭包里、公开方法互相调用」，代价是内部方法之间不能通过 `self` 互相找到，得靠前向声明或用局部函数名互相引用。Lua 5.5 里 `global` 变成了保留字（用来显式声明全局变量），这也让「不小心创建全局变量」这个经典陷阱的告警更明确，但跟私有无关。性能上闭包方案每个实例都要新建一批函数对象，字段方案共享 `__index` 上的方法，所以热点路径通常选字段方案 + 下划线约定。

```lua
-- 闭包方案里内部方法互相调用：用局部函数名互相引用
local function new(value)
  local state = value
  local function normalize() return state end
  local function get() return normalize() end
  local function set(v) state = v end
  return { get = get, set = set }
end
```

`debug` 库是这一切的终点：`debug.getupvalue(f, i)` 能按索引取出闭包捕获的变量名与值，`debug.getlocal` 能读函数的局部变量，`debug.setmetatable` 能改元表，`debug.sethook` 能挂钩执行。这些 API 的官方定位是调试用途，但语言层面并不阻止生产代码调用它们，所以 Lua 里没有「不可绕过」的私有——所谓的真私有是指「不借助 debug 库就拿不到」，这已经能满足绝大多数封装需求。工程建议：把 `debug` 库在沙箱环境里移除（用 `_ENV` 限制），就能把「真私有」变成「实际不可达」。

📘 [Lua 5.5 Reference Manual · Debug Library](https://www.lua.org/manual/5.5/manual.html#6.10)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 里 `private` 是**编译期私有**：它只存在于类型信息里，编译成 JavaScript 之后那个属性完全是普通属性，`Object.keys` 能看到、`obj.privateField` 能读写。想要真私有必须用 ECMAScript 的 `#`。在这两者之间还有一层工具级约定：`@internal` 注解配合 `stripInternal` 从 `.d.ts` 里剔除声明，让包外连类型都看不到。

```typescript
class Repo {
  private secret = "s3";           // 编译期私有：运行时是普通属性
  #realSecret = "s3";              // ✅ 真私有：运行时不可访问
  read() { return this.secret + this.#realSecret; }
}

const r = new Repo();
console.log((r as any).secret);    // "s3"  ⚠️ 编译期私有被绕过
// console.log((r as any).#realSecret);   // 🛑 SyntaxError
```

`@internal` 的用法有个前提容易被忽略：`stripInternal` 只在生成声明文件时生效，它从 `.d.ts` 里删掉被标记的声明，于是消费方（用你的 `.d.ts` 做类型检查）看不到它们。但如果消费方直接引用你的 `.ts` 源码（monorepo 里常见），`@internal` 就完全不生效，因为 `stripInternal` 只在 `declaration` 输出阶段起作用。所以 `@internal` 的定位是「发布包的声明面控制」，不是团队内部的可见性工具。

```typescript
/** @internal */
export function debugOnly(): void {}

// tsconfig.json
// { "compilerOptions": { "stripInternal": true, "declaration": true } }
// → debugOnly 只会从 .d.ts 里消失，.js 里仍然存在
```

monorepo 里真正控制模块边界的是**项目引用**（project references）+ `paths`：把每个包拆成独立的 tsconfig 项目，只通过 `exports`/`main` 声明的入口 import，`paths` 别名指向源码时可以用 `eslint-plugin-import` 的 `no-restricted-paths` 之类规则禁止跨包深引用。类型层面的 `export type` 与 `isolatedModules` 则保证「只导出类型的东西不会留下运行时残留」。总结 TypeScript 的定位：它的封装完全依赖三件外部的东西——ECMAScript 的 `#`（运行时）、声明文件生成（发布面）、lint/项目结构（monorepo 内部），语言自身只提供编译期检查这一层。

📘 [TypeScript · Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 里「约定式私有」的历史比 `#` 长得多：早期用 `_name` 前缀（至今仍能在库代码里看到），后来用闭包做真私有，再后来用 WeakMap 做「可以挂在实例上、但外部拿不到 key」的私有状态，ES2022 的 `#` 才把真私有变成语法。这四种手段的强度差别很大，选错会直接影响封装是否可靠。

```javascript
// 1) 下划线前缀：纯约定
class A { constructor() { this._x = 1; } }
new A()._x;                                  // 1  ⚠️ 随便访问

// 2) 闭包：真私有，但每个实例一份函数
function makeB() { let x = 1; return { get: () => x, set: (v) => { x = v; } }; }

// 3) WeakMap：真私有，共享方法，实例可被回收
const priv = new WeakMap();
class C {
  constructor() { priv.set(this, { x: 1 }); }
  get x() { return priv.get(this).x; }
}

// 4) #：真私有，语法级
class D { #x = 1; get x() { return this.#x; } }
```

IIFE（立即执行函数表达式）是模块系统出现前的标准封装模式，今天仍然适用于「不希望被打包器处理、也不希望污染模块作用域」的小段代码；它的现代写法是利用块级作用域 `{ let x = 1; globalThis.get = () => x; }`。返回值模式（返回对象字面量而不是 `this`）是闭包封装的关键技巧：不要 `return this`，因为 `this` 上的东西外部都能改；返回一组闭包，外部就只能通过这些闭包访问内部状态。

```javascript
const counter = (() => {
  let n = 0;                                  // IIFE 内的局部变量：真私有
  return Object.freeze({                      // 冻结可防止替换方法
    inc: () => ++n,
    get: () => n,
  });
})();
counter.inc();
console.log(counter.get(), Object.keys(counter));   // 1 [ 'inc', 'get' ]
// counter.n                                    // undefined
```

要在几种方案间选择，判据是三条：**是否需要实例级状态**（需要就用 `#` 或 WeakMap，闭包会导致 `this` 绑定问题）、**是否在意内存**（闭包每实例一组函数，WeakMap 每次访问要查表，`#` 是引擎优化的）、**是否需要跨实例共享私有**（只有 WeakMap 与 `#` 的静态方法（`static has(o) { return #x in o }`）能做到）。现代代码的推荐顺序很明确：能用 `#` 就用 `#`，需要「友元」语义时用 WeakMap，闭包留给函数式的小工具与单例。`Object.freeze` 是补充手段，它冻结对象自身属性的可写性与可配置性，但不影响闭包变量的值，也不阻止替换整个对象引用。

📘 [MDN · Private class features](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Private_class_fields)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的可见性是**运行时强制**的，所以「约定式私有」在 PHP 里主要是给静态分析器看的注解：`@internal`（Psalm/PHPStan 支持，跨包使用报错）以及 `@deprecated`。另外 PHP 有一个别处少见的约定：`_` 前缀在 PHP 社区基本不用（历史上有过 `_method` 风格，现代 PSR 规范没有这种约定），取而代之的是 `Internal` 子命名空间与 `@internal` 注解。

```php
namespace Shop;

/** @internal 非公开 API：跨包使用 Psalm/PHPStan 会报错 */
final class Ledger
{
    public function fees(): int { return 1; }
}

final class Account
{
    private int $balance = 0;       // 运行时强制
    public function total(): int { return $this->balance + (new Ledger())->fees(); }
}
```

PHP 里最需要「约定」的地方是**属性钩子与 readonly 的交互**：`readonly` 属性只能在初始化时写一次，任何后续写入（含反射、`__set`）都会抛 `Error`；而属性钩子（PHP 8.4）允许把一个属性变成「计算属性」，这时候 `ReflectionProperty::getValue()` 拿到的是钩子计算结果，想读原值要用 `getRawValue()`。这些语义都必须靠文档与静态分析器理解，运行时不会给你「这只是内部实现」的提示。

```php
class Money
{
    public function __construct(
        public readonly int $amount,
    ) {}

    public int $doubled {
        get => $this->amount * 2;      // 8.4 属性钩子：无 backing store
    }
}
$m = new Money(10);
echo $m->doubled;                       // 20
$rp = new ReflectionProperty(Money::class, 'doubled');
echo $rp->isVirtual() ? "virtual" : "stored";   // virtual
$rp->getValue($m);                       // 20（走钩子）
```

`final` 与 `@final` 的关系值得单独提一句：`final` 是语言级的（禁止继承/覆写），`@final` 是注解级的（Psalm/PHPStan 报错，运行时无效果）。PHP 8.1 起 `readonly` 是语言级的，8.4 起非对称可见性也是语言级的，这让 PHP 的「编译期/运行期」分工变得清晰：可见性、readonly、final 都是运行时强制的，`@internal`/`@final`/`@deprecated` 这类注解是静态分析层面的。跟 Python 对比，PHP 的 `private` 更硬（运行时真拦截），但跨包「内部 API」的表达仍然只能靠注解与文档。

📘 [PHP · Property Hooks](https://www.php.net/manual/en/language.oop5.property-hooks.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 是「约定式私有」用得最重的语言之一，因为它的 `private` 只禁止显式 receiver 调用，而 `send`、`instance_variable_get`、`const_get`、`define_method` 等反射 API 全都能绕过去。社区为此发展出一套约定：内部实现放在 `Internal` 子模块、用 `private_constant` 关掉常量、用 `module_function` 暴露模块级函数、用 `protected` 精确表达「同类实例之间可用」。

```ruby
module Shop
  class Account
    def initialize(owner) = @owner = owner
    attr_reader :owner
    def compare(other) = self <=> other  # ✅ 类内部调用 protected
    protected
    def <=>(other) = @owner <=> other.owner   # 类外显式调用会 NoMethodError
    private
    def secret = "pin"
  end

  module_function                       # 模块级函数：私有实例方法 + 公开单例方法
  def helper = 1
end

a = Shop::Account.new("ada")
a.compare(Shop::Account.new("bob"))      # -1  ✅ 类内部走的 protected 路径
Shop.helper                              # 1   ✅ module_function 的公开面
a.secret                                 # 🛑 NoMethodError: private method
a.send(:secret)                           # "pin"   ⚠️ send 绕过
```

`module_function` 是 Ruby 里表达「工具函数」的官方机制：它把实例方法变成模块的**私有**实例方法，同时复制一份作为模块的**公开**单例方法，所以 `Shop.helper` 可用而 `include Shop` 之后 `helper` 不可被外部调用。工厂与单例常用 `private_class_method :new` 封住构造函数，只暴露 `create` 之类的入口。这些机制的共同点是：它们让「正确用法」变得自然，而绕过它们需要写出明显不正常的代码（`send`、`instance_variable_get`），这本身就是一种有效的社会约束。

```ruby
class Registry
  private_class_method :new         # 封住 new
  def self.instance
    @instance ||= new                # ✅ 类内部仍能调用
  end
  def initialize = @items = {}
end
Registry.instance                    # ✅
Registry.new                         # 🛑 NoMethodError: private method 'new'
```

Ruby 的 refinements 是另一条与封装相关的路：它能在限定作用域内改写类的方法，用来做测试替身或行为注入，效果不泄漏到作用域外（`using` 只在当前文件/模块内生效）。它常被拿来跟 monkey patching 对比，但要注意 refinement 也有反射绕过方式（`Module#refine` 定义的模块可以被人重新打开）。整体上，Ruby 的封装强度取决于「团队是否遵守约定 + 是否有代码评审」，语言本身提供的是可读性的支持而不是安全性，这也解释了为什么 Ruby 生态特别强调测试覆盖与静态分析（RuboCop、Sorbet、RBS）。

📘 [Ruby · Modules and classes](https://docs.ruby-lang.org/en/master/syntax/modules_and_classes_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 封装与反射的边界

这一节把所有语言放到同一张桌子上问一个问题：**你标记的私有，别人花多大力气能读能写？**答案分成三档。第一档是「语言层面没有通向内部的路径」——JavaScript 的 `#`、Rust 的 `mod` 私有、Go 的未导出字段（反射连值都读不到）、Zig 的文件私有、Lua 的闭包 upvalue（不算 `debug` 库），这些是真私有。第二档是「编译器拦住了，但运行时工具能打开」——Java 的 `setAccessible` + `--add-opens`、C# 的 `BindingFlags.NonPublic` + `UnsafeAccessor`、Kotlin 的 JVM 反射、PHP 的 `ReflectionProperty` 与 `Closure::bind`、Ruby 的 `send`/`instance_variable_get`、Python 的 `object.__setattr__`，这些是**编译期私有**。第三档是「全靠约定」——R 的 `:::`、Julia 的 `getfield`、C 的指针运算，语言不承诺任何保护。序列化框架与 ORM 之所以持续依赖反射，正是因为第二档语言里的「私有」从来不是运行时边界；而测试替身与依赖注入则进一步说明，很多设计压力不是封装的失败，而是封装的用途被误判了。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的封装在编译期就是硬的，运行时也不存在反射 API 能按名字取字段——标准库没有 `Reflection` 这类东西，`std::any::Any` 只能做运行时类型判断（`downcast_ref`），前提是你得先拿到 `&dyn Any`，而把值转成 `&dyn Any` 需要 `'static` 且类型本身可以被引用。所以 Rust 里唯一的「绕过」路径是 `unsafe` 加裸指针，或者自己写宏在**编译期**展开代码。

```rust
mod secret {
    pub struct Vault { code: u32 }          // 字段私有
    impl Vault {
        pub fn new() -> Self { Vault { code: 42 } }
        pub fn code(&self) -> u32 { self.code }   // 公开访问器
    }
}

fn main() {
    let v = secret::Vault::new();
    println!("{}", v.code());     // 42
    // v.code                      // 🛑 E0616: field `code` is private
    // 没有反射能按名字取到 code；唯一出路是 unsafe 指针运算，需自己保证布局
    let raw: *const secret::Vault = &v;
    let first = unsafe { *(raw as *const u32) };   // ⚠️ 依赖字段顺序，UB 风险自负
    println!("{}", first);        // 42
}
```

`serde` 是 Rust 生态解决「反射式序列化」的正统答案：它不用运行时反射，而是**编译期派生**——`#[derive(Serialize)]` 生成的代码在 crate 内部展开，因此可以访问私有字段，但生成的 impl 是普通 Rust 代码，外部无法凭空对任意类型做同样的事。这就是 Rust 与 Java/C# 生态的根本差别：序列化能力来自为每个类型生成的代码，而不是来自「任何类型都能被反射」这个前提。代价是必须为类型显式派生或用 `#[serde(remote = "...")]` 描述外部类型，无法对第三方类型做「无侵入」的序列化。

```rust
#[derive(serde::Serialize)]
pub struct Vault {
    code: u32,                     // 私有字段也能被派生代码访问（宏在 crate 内展开）
    #[serde(skip)]
    cached: Option<u32>,
}
```

所以 Rust 里的封装边界非常清楚：**编译期契约同时也是运行时事实**（除非用 `unsafe`）。这带来的设计压力反而小一些——你不需要为「框架要反射怎么办」而主动放宽可见性，`serde`、`clap`、`thiserror` 这些框架都走派生宏路线；反过来说，动态插件式的能力（运行时按字符串查字段、动态构造对象）在 Rust 里天然受限，需要显式设计成 trait 对象加工厂注册表。

📘 [Rust · Visibility and privacy](https://doc.rust-lang.org/reference/visibility-and-privacy.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的反射（`Mirror`）是**只读**且**不破坏可见性**的：`Mirror(reflecting:)` 能枚举出结构体与类的字段标签和值，包括 `private` 字段，但它只能读、不能写，也不能调用方法。这个设计是刻意的——官方文档明确 `Mirror` 的用途是调试与展示（`CustomReflectable`、playground 显示），不是访问控制通道。

```swift
struct Vault {
    private let code = 42
    private var cache: Int? = nil
}
let m = Mirror(reflecting: Vault())
for child in m.children {
    print(child.label ?? "?", child.value)   // code 42 / cache nil
}
// Mirror 无法写回：没有 set 能力
```

能读 `private` 的字段值意味着封装在**数据可见性**上不是绝对边界——任何拿到实例的代码都能用 `Mirror` 把内部值打印出来。但 Swift 里没有像 Java 的 `setAccessible` 或 C# 的 `UnsafeAccessor` 那样的官方写入口，也没有类似 `sun.misc.Unsafe` 的逃生舱；要真正改值只能靠 `withUnsafeMutablePointer(to:)` 加内存布局假设（属于未定义行为，绝不能用于生产）。所以 Swift 的私有是「可读不可写」的编译期契约。

```swift
// 真正需要外部读写私有状态时的官方通道：显式设计接口
struct Vault {
    private(set) var code = 42         // 外部只读、内部可写
    mutating func reset() { code = 0 } // 唯一的写入口
}
var v = Vault()
print(v.code)      // 42
// v.code = 1      // 🛑 setter 不可访问
```

序列化方面 Swift 的 `Codable` 走**编译期合成**：`Encodable`/`Decodable` 的 `init(from:)` 与 `encode(to:)` 由编译器为你的类型自动合成，合成代码能访问私有属性（因为它在类型内部），因此 `Codable` 从未要求你把属性改成 `internal`。这跟 Rust 的派生宏是同一个思路。测试与依赖注入方面，Swift 没有运行时反射式 DI 容器的主流方案，社区更倾向构造器注入 + 协议抽象，这既回避了反射也回避了放宽可见性。`@testable` 只影响编译期可见性，不影响运行时。

📘 [Swift · Mirror](https://developer.apple.com/documentation/swift/mirror)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的 `reflect` 对未导出字段是**只读名字、不读值**：`Type.Field(i).Name` 能拿到字段名（因为名字在类型元数据里），但 `Value.Field(i)` 得到的值 `CanInterface()` 为 `false`，`Int()`/`String()` 这类取值方法会 panic，`Set` 也不允许。`unsafe` 是官方指定的逃生舱：`unsafe.Pointer` 加字段偏移可以读写任意字段，代价是失去类型安全与版本兼容保证。

```go
package main

import (
	"fmt"
	"reflect"
)

type Vault struct {
	Code  int
	code  int      // 未导出
}

func main() {
	v := Vault{Code: 1, code: 42}
	rv := reflect.ValueOf(&v).Elem()
	fmt.Println(rv.FieldByName("code").CanInterface(),   // false
		rv.FieldByName("code").CanSet())                 // false
	// rv.FieldByName("code").Int()   // 🛑 panic: using value obtained using unexported field
	fmt.Println(reflect.TypeOf(v).Field(1).Name)          // code（名字仍可见）
	fmt.Println(rv.FieldByName("Code").CanSet())          // true
}
```

用 `unsafe` 读写未导出字段在实践中确实存在，标准库自己就这么干（例如 `reflect` 与 `sync` 内部的实现），但第三方库用它会绑定到具体结构体布局，任何一个字段顺序变化都会静默出错。官方在 `unsafe` 包的文档里明确说「使用 unsafe 的代码不在 Go 1 兼容性承诺范围内」，这就是为什么 ORM 与 JSON 库都选择「只处理导出字段」：`encoding/json` 忽略未导出字段，`encoding/xml` 同理，`sql.Rows.Scan` 需要你传入目标变量的指针。要序列化私有字段，标准做法是实现 `MarshalJSON`/`UnmarshalJSON`（或 `encoding.TextMarshaler`），由类型自己决定暴露什么。

```go
type Vault struct{ code int }

func (v Vault) MarshalJSON() ([]byte, error) {
	return []byte(fmt.Sprintf(`{"code":%d}`, v.code)), nil   // 类型自己决定序列化什么
}
```

依赖注入在 Go 里同样不依赖反射：主流做法是构造器注入与接口，少数 DI 框架（如 `wire`）用**代码生成**而不是反射，理由是显式依赖图更易读、启动更快。测试替身就是接口的另一种实现，不需要访问私有成员。所以 Go 的封装边界在所有语言里属于偏硬的一档：编译期挡住跨包访问，运行时只留下 `unsafe` 这条明码标价的危险通道。

📘 [Go · reflect: CanInterface](https://pkg.go.dev/reflect#Value.CanInterface)

{{% /tab %}}

{{% tab header="Python" %}}

Python **没有强制的封装**，任何「私有」都能被绕过，但绕过的难度分三档：单下划线只需直接写名字、双下划线要写出改写后的名字（`_Class__name`）、`__slots__` 与 C 扩展则构成真正的障碍。`object.__setattr__`、`vars()`、`__dict__`、`inspect.getattr_static` 这些 API 让「读」几乎没有成本。

```python
import inspect

class Vault:
    def __init__(self) -> None:
        self._a = 1            # 约定私有
        self.__b = 2           # 改写成 _Vault__b

v = Vault()
v._a = 99                       # ⚠️ 直接改
v._Vault__b = 88                # ⚠️ 改写后直接改
object.__setattr__(v, "_a", 77)  # ⚠️ 绕过自定义 __setattr__
print(v._a, v._Vault__b, vars(v))
# 77 88 {'_a': 77, '_Vault__b': 88}
print(inspect.getattr_static(v, "_Vault__b"))   # 88：不触发描述符协议
```

`__slots__` 是唯一在**结构**层面生效的限制：定义了 `__slots__` 之后，实例不再有 `__dict__`，因此不能动态添加未声明的属性；但如果 `__slots__` 里声明了 `_x`，`_x` 照样能改。真正接近硬边界的是**描述符 + 属性**的组合：把值放在闭包或 C 结构里，用 `@property` 只提供读；以及把关键实现写成 C 扩展模块（`_json`、`_pickle` 就是这么做的），Python 层无法触及内部状态。`ctypes` 甚至能直接改 CPython 对象内存（例如修改 `float` 的值、改变小整数缓存），所以「Python 里没有秘密」在语言层面是准确的。

```python
import ctypes
x = 1.0
ctypes.pythonapi.PyFloat_AsDouble.restype = ctypes.c_double   # 只读示例
# 用 ctypes 修改对象内存需要精确知道 PyObject 布局，属于高度版本相关操作
```

序列化与 ORM 是 Python 里最依赖反射的领域，也最能说明「私有不是运行时边界」：`pickle` 用 `__reduce_ex__` 与 `__dict__` 默认序列化**所有**实例属性（含双下划线改写后的名字），`dataclasses.asdict` 只处理字段，`pydantic` 在 v2 用 Rust 核心做校验、通过 `__pydantic_private__` 单独管理私有属性。这些框架实际上在鼓励你把「需要被序列化/校验的数据」放在公开字段里、把「真正的实现细节」放在闭包或私有属性里——因为框架能看到的东西和你以为它能看到的东西是两回事。依赖注入方面，Python 主流方案（`FastAPI` 的 `Depends`、`pytest` 的 fixture）都是**显式参数注入**，不需要反射式容器，这是 Python 生态里一个务实的选择。

📘 [Python Data Model · Customizing attribute access](https://docs.python.org/3/reference/datamodel.html#customizing-attribute-access)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 跑在 JVM 上，因此它的 `private` 与 `internal` 都**只是编译期修饰**：Java 反射（`getDeclaredField` + `setAccessible(true)`）能读写任何字段，`internal` 编译后甚至就是 `public`，Java 代码可以直接调用。Kotlin 自己提供的遮掩手段是 `@JvmSynthetic`（对 Java 调用者隐藏）与 `@PublishedApi`（限定 inline 使用），它们改的是字节码标志，不是访问控制。

```kotlin
class Vault(private val code: Int = 42) {
    internal fun internalApi(): Int = code
    @JvmSynthetic fun kotlinOnly(): Int = code
}

// JVM 反射绕过（在 Kotlin 里也能写）
fun hack(v: Vault): Int {
    val f = Vault::class.java.getDeclaredField("code")
    f.isAccessible = true                 // ⚠️ 打开 private
    return f.getInt(v)
}
// 42
```

这里最需要注意的实践后果是**库的 API 面在 Java 侧比 Kotlin 侧更大**：一个 Kotlin 库标了 `internal` 的类，Java 用户（或任何 JVM 语言）能通过 `Vault$Companion` 这类名字访问到，`@JvmSynthetic` 只是让 Java **编译器**看不见。所以如果目标是「只给 Kotlin 用户」，得靠 `@JvmSynthetic` 加文档；如果目标是「谁都不能乱用」，只能靠模块化（JPMS）与 `jdeps`/自定义 lint 检查。

```kotlin
// 序列化框架的取舍：kotlinx.serialization 是编译期插件 + 代码生成
@Serializable
data class User(val name: String, @Transient val cache: Int = 0)
// 私有属性默认不参与序列化；要参与需显式声明并提供构造入口
```

Kotlin 生态在反射与封装上的选择跟 Rust/Swift 类似：官方序列化方案 `kotlinx.serialization` 走**编译器插件 + 代码生成**，因此不需要把属性改成 `public`；而 Java 生态的 Jackson 走运行时反射，遇到 Kotlin 的 `private` 属性需要 `-parameters` 编译参数或用 `@JsonProperty` 显式标注，这正好展示了两条路线的差异——编译期方案要求你显式参与，运行时方案要求你主动放宽可见性。依赖注入方面，Kotlin 常见选择是构造器注入（Koin 用 DSL + 反射，Dagger/Hilt 用注解处理器与代码生成），其中代码生成路线同样不需要放宽可见性。

📘 [Kotlin · Visibility modifiers](https://kotlinlang.org/docs/visibility-modifiers.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 是「反射绕过封装」这个话题的原产地：`AccessibleObject.setAccessible(true)` 从 1.2 起就能打开任何 `private` 成员，`sun.misc.Unsafe` 甚至能直接改内存。转折点是 Java 9 的模块系统与 Java 16/17 的强封装：JDK 16 起默认拒绝「深反射」到 JDK 内部（JEP 396 默认 `--illegal-access=deny`），JDK 17 起用 JEP 403 彻底移除宽松模式，`setAccessible` 对 `java.*` 内部包会抛 `InaccessibleObjectException`，必须显式 `--add-opens` 或 `--add-exports` 才有例外。

```java
import java.lang.reflect.Field;

public class Vault {
    private int code = 42;
    public static void main(String[] args) throws Exception {
        Vault v = new Vault();
        Field f = Vault.class.getDeclaredField("code");
        f.setAccessible(true);           // ⚠️ 打开 private（应用类仍可行）
        System.out.println(f.getInt(v));  // 42
        f.setInt(v, 99);
        System.out.println(v.code);       // 99   仅同类可访问，这里在 Vault 内部
    }
}
```

为什么应用类还能打开？因为 classpath 上的代码处在**无名模块**里，无名模块默认 `opens` 全部包。一旦你的类被打进具名模块（有 `module-info.java`），`setAccessible` 就要看该包是否 `opens`；JDK 自身的类则从 17 起默认全封闭，唯一的例外是启动时用 `--add-opens java.base/java.lang=ALL-UNNAMED` 之类的参数，这正是 Spring、Hibernate、Lombok 在 JDK 17+ 上常见启动报错的来源。`sun.misc.Unsafe` 的内存操作（`objectFieldOffset` + `putObject`）仍然可用，但它对记录类（records）与隐藏类有额外限制，而且在 JDK 23+ 逐步被 `VarHandle` 与 `MemorySegment`（FFM API）取代。

```java
// 官方推荐的现代替代：MethodHandle + privateLookupIn（需 opens）
import java.lang.invoke.*;
MethodHandles.Lookup lookup = MethodHandles.privateLookupIn(Vault.class, MethodHandles.lookup());
VarHandle vh = lookup.findVarHandle(Vault.class, "code", int.class);
vh.set(v, 7);
```

序列化与 ORM 是这层张力的最大受益者也是最大受害者：Jackson、Hibernate、Gson 都依赖反射读写私有字段，所以它们必须处理模块边界（`opens` 声明、`--add-opens` 参数，或使用 `MethodHandles.privateLookupIn`）。Java 官方的 `java.io.Serializable` 走的是「语言内建序列化」，它绕过构造器、能读写私有字段，也因此背上了「脆弱、有安全风险」的名声，现代项目更倾向显式 DTO 或 JSON 而非原生序列化。`ObjectInputFilter`（JEP 290）是给反序列化加白名单的官方机制，但它防的是安全问题，不改变「反射能读写私有」这个事实。结论很明确：**Java 的 `private` 是编译期契约，模块系统是运行期的一道闸门，但两者都不构成安全边界**。

📘 [Oracle · JEP 403: Strongly Encapsulate JDK Internals](https://openjdk.org/jeps/403)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的封装是编译期检查，运行时**完全没有元数据**（除非显式启用 RTTI 与调试信息），因此不存在「反射 API 打开私有」这回事。绕过的两条路是预处理器与内存操作：`#define private public` 骗过编译器（破坏 ODR，见下），或者用 `reinterpret_cast` 直接按已知布局读写。两者的共同点是都要求你知道目标类型的内存布局，一旦布局变化就静默出错。

```cpp
#include <iostream>
#define private public          // ⚠️ 预处理器不知道访问控制
#include "vault.h"               // vault.h 里 class Vault { private: int code_; };
#undef private
int main() {
    Vault v;
    std::cout << v.code_;        // 7：编译通过，但这是 ODR 违规（未定义行为）
}
```

ODR 违规为什么危险：如果别的翻译单元在没有这个宏的情况下包含了同一个头文件，那么同一个类在两个翻译单元里的**成员访问性不同**，标准要求类的定义在所有翻译单元中完全相同（token 序列一致），违反即未定义行为。实际后果可能是布局错乱、内联函数被错误合并、`std::vector<Vault>` 的大小假设不一致等等——所以这个技巧只能出现在一次性调试脚本里，不能进版本库。

```cpp
// 合法的「显式打开」：friend
class Vault {
    friend struct VaultTester;         // 给测试一个正式的口子
    friend void serialize(const Vault &, std::string &);
    int code_ = 42;
};
struct VaultTester {
    static int read(const Vault &v) { return v.code_; }   // ✅ 合法访问
};
```

`reinterpret_cast` 与 `memcpy` 的路线更危险：它是未定义行为（严格别名规则、对齐要求、有虚表时的对象布局），只是在实践中常常「能用」。真正在 C++ 里需要序列化与反射时，主流方案是**显式声明**：手写 `serialize` 函数、用宏生成访问器（Boost.Serialization 风格）、或用 C++20 的 `reflect` 提案（尚未标准化）与第三方库（`magic_enum`、`reflect-cpp`）。这跟 Rust 的派生宏、Swift 的 `Codable` 合成是同一种哲学：序列化能力由类型作者显式授予，而不是由语言无条件提供。测试替身与依赖注入在 C++ 里通常通过接口（纯虚类）+ 构造器注入 + 链接期替换实现，`friend struct XxxTester` 是给白盒测试留口子的常见做法。

📘 [cppreference · Access specifiers](https://en.cppreference.com/w/cpp/language/access)

{{% /tab %}}

{{% tab header="C" %}}

C 没有任何反射机制，所以「绕过封装」在 C 里只有两条路：**指针运算**（拿到结构体定义的任何代码都能按偏移读写任意字段）与**链接层面的手段**（`static` 之外的一切外部符号都能被链接到）。`const` 是编译期约束，强制转换去掉 `const` 再写是未定义行为。

```c
#include <stdio.h>
int main(void) {
    const int n = 41;                   /* const 对象 */
    int *p = (int *)&n;                 /* 强制去掉 const */
    *p = 42;                            /* 🛑 写 const 对象：未定义行为 */
    printf("%d\n", n);                  /* clang 21 -O0/-O2 均输出 41：这次写入被折叠掉了 */
    return 0;
}
```

实测结果很说明问题：`n` 打印出来还是 41，因为编译器把 `const` 对象当作编译期常量折叠，写入被优化掉了。但未定义行为不承诺任何一种结果——同一台 clang 21 上，把 `const` 放进结构体字段（`struct vault { const int code; }; ... *p = 99`）却会真的打印 99。也就是说，能不能改、改了之后读到什么，完全取决于优化器与代码形状，绝不能依赖。想改一个 `const` 对象并让所有读取者看到，标准做法是把它改成非 `const`（或 `volatile const` 并接受性能损失），而不是靠强制转换。

```c
/* 真封装：不完整类型 + 访问器，外部连 sizeof 都算不出来 */
/* vault.h */
typedef struct vault vault;
vault *vault_new(int code);
int vault_get(const vault *v);
/* vault.c */
struct vault { int code; };
vault *vault_new(int c) { vault *v = malloc(sizeof *v); v->code = c; return v; }
int vault_get(const vault *v) { return v->code; }
```

序列化在 C 里从来不是「框架反射」，而是手写 `memcpy` + 显式字段顺序，或者用协议描述文件（protobuf、FlatBuffers）生成代码。这也解释了为什么 C 的结构体布局兼容性是一个严肃话题：`#pragma pack`、字节序、位域实现定义行为都直接影响二进制兼容，所以「把结构体定义藏进 `.c`」不只是封装，也是 ABI 稳定性策略。依赖注入在 C 里通过函数指针表（vtable 风格）与链接期替换（弱符号、`--wrap`）实现，测试替身则常用 `#include` 被测 `.c` 文件或链接 mock 实现的方式，都不需要任何可见性突破。结论：C 的封装是**构建与链接工程**，语言本身只提供 `static` 与 `const` 这两个工具。

📘 [cppreference · const qualifier](https://en.cppreference.com/w/c/language/const)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的反射能力很强：`fieldnames(T)`、`getfield(x, :name)`、`getproperty`、`methods(f)`、`@which`、`code_lowered`、`Base.uncompiled` 都能深入类型与方法内部。模块层面 `getfield(Module, :name)` 可以取出任何绑定，包括未导出的。所以 Julia 的封装完全是「社会契约」，官方手册也把它表述为「Julia 没有真正隐藏模块内部的手段」。

```julia
module Shop
struct Vault
    code::Int
    _cache::Int
end
_secret() = :hidden
end

v = Shop.Vault(42, 1)
fieldnames(Shop.Vault)            # (:code, :_cache)
getfield(v, :_cache)              # 1        ⚠️ 无访问器也能读
# setfield!(v, :code, 99)          # 🛑 不可变 struct 不能改字段：immutable struct of type Vault
getfield(Shop, :_secret)          # _secret 函数对象
Shop._secret()                    # :hidden  ⚠️ 限定名永远可用
```

`getfield` 与 `setfield!` 的行为要区分清楚：对 `struct`（不可变）只能用 `getfield` 读；对 `mutable struct` 才能 `setfield!(x, :field, value)`，而且它绕过任何 `setproperty!` 重载——也就是说，即使你为类型定义了校验逻辑，`setfield!` 也能跳过。这一点跟 Python 的 `object.__setattr__` 绕过自定义 `__setattr__` 完全对应，是「语言提供的元操作总是优先于用户定义的访问路径」这类设计的共同后果。

```julia
mutable struct Guarded
    x::Int
end
function Base.setproperty!(g::Guarded, name::Symbol, v)
    name === :x && v < 0 && error("x must be >= 0")
    setfield!(g, name, v)          # 校验路径
end
g = Guarded(1)
g.x = 5                            # ✅ 走 setproperty!
# g.x = -1                         # 🛑 error: x must be >= 0
setfield!(g, :x, -1)                # ⚠️ 直接绕过校验
```

序列化上，Julia 的 `Serialization` 标准库用内建的 `serialize`/`deserialize`，它按类型结构写入（可以处理不可变值、循环引用、共享引用），因此同样绕过任何访问器；`JSON3`、`StructTypes` 这类第三方库则通过 `StructTypes.StructType` 的显式声明来定义序列化面，走的是「类型作者显式授予」的路线。依赖注入在 Julia 里通常通过函数参数与多重派发实现（`solve(problem, solver)`），不流行反射式容器。测试方面 Julia 的 `Test` 标准库配合包结构，测试可以直接调用内部函数（`Pkg.test` 会把测试代码加载进主包环境），`Base.ispublic` 只影响文档与帮助，不影响可访问性。实践结论：Julia 的 `public`/`export`/下划线构成**文档化契约**，真正的隔离只能靠「把实现放进不导出的子模块 + 依赖方不越界」，安全边界必须由进程或网络隔离提供。

📘 [Julia Base · Reflection and introspection](https://docs.julialang.org/en/v1/base/base/#Reflection-and-introspection)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的反射能读写私有成员：`GetField(name, BindingFlags.NonPublic | BindingFlags.Instance)` 加 `SetValue` 就能改私有字段，`GetMethod(..., NonPublic)` 能调用私有方法。.NET 8 起官方给出了一个**正式且高性能**的替代方案 `UnsafeAccessorAttribute`：把 `extern static` 方法与属性标注成访问器，运行时会为它生成直达目标成员的实现，绕开反射的开销与部分限制。

```csharp
using System.Runtime.CompilerServices;

public class Vault { private int code = 42; private void Reset() { code = 0; } }

public static class VaultAccess
{
    [UnsafeAccessor(UnsafeAccessorKind.Field, Name = "code")]
    public static extern ref int Code(Vault v);

    [UnsafeAccessor(UnsafeAccessorKind.Method, Name = "Reset")]
    public static extern void Reset(Vault v);
}

var v = new Vault();
VaultAccess.Code(v) = 99;          // ⚠️ ref 返回：可直接赋值
VaultAccess.Reset(v);
Console.WriteLine(VaultAccess.Code(v));   // 0
```

`UnsafeAccessor` 的规则值得记：方法的首参数类型决定「从哪个类型上找成员」（**不沿着类型层次向上找**），字段访问器必须返回 `ref`，静态成员的首个参数会被忽略（可以传 `null`），泛型支持自 .NET 9 起，签名不匹配时抛 `MissingFieldException`/`MissingMethodException`。它比反射快得多（接近直接访问），所以在序列化库与热点路径上正在取代 `FieldInfo.SetValue`。

```csharp
// 传统反射路径（仍有使用场景，且受 InternalsVisibleTo / 安全模型影响）
var f = typeof(Vault).GetField("code", System.Reflection.BindingFlags.NonPublic
                                     | System.Reflection.BindingFlags.Instance);
f!.SetValue(v, 7);
```

.NET 没有 JVM 那样的「模块强封装」默认拒绝机制：反射对应用程序集一律可行，`InternalsVisibleTo` 只影响编译期可见性（对反射无影响，反射本来就能看 `private`），`UnsafeAccessor` 也不检查 `internal`/`private`。真正的限制来自 AOT 与裁剪：Native AOT 下大量反射 API 需要 `[DynamicallyAccessedMembers]` 标注，否则裁剪器可能把成员删掉，`UnsafeAccessor` 在这种场景下反而是更可靠的方案。序列化方面，`System.Text.Json` 支持源生成器（`JsonSerializerContext`）走编译期代码生成路线，跟反射路线（`JsonSerializer.Serialize` 默认）并存；EF Core 则大量依赖反射与表达式树，这也是它需要在模型里显式声明属性的原因之一。测试与依赖注入上，`Microsoft.Extensions.DependencyInjection` 主要靠构造器注入与编译期生成的工厂，`Moq`/`NSubstitute` 用动态代理（`DispatchProxy` 或 Castle DynamicProxy）不需要访问私有成员。结论：**C# 的 `private` 是编译期契约，反射与 `UnsafeAccessor` 让它在运行时形同虚设**。

📘 [MS Learn · UnsafeAccessorAttribute](https://learn.microsoft.com/en-us/dotnet/api/system.runtime.compilerservices.unsafeaccessorattribute)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的 `_` 私有是**编译期强制、运行时真实存在但不可达**：编译到 VM 时私有名字会被改写成带 library URI 的符号（`_balance@1234`），编译到 JS 时会做混淆式重命名，无论哪种情况，外部代码都无法用源码里的名字引用到它。Dart 有反射（`dart:mirrors`）可以读私有成员，但它**只在 Dart VM 上可用，不支持 AOT 与 Web**，Flutter 与 `dart compile exe` 都用不了，这让它实际上退出了生产可用的工具集。

```dart
// lib/vault.dart
class Vault {
  int _code = 42;
  int get code => _code;
}

// 另一个库里
import 'vault.dart';
void main() {
  final v = Vault();
  print(v.code);        // 42
  // v._code            // 🛑 编译错误：跨库不可见
}
```

`dart:mirrors` 的限制值得写清楚：官方文档把它标为「只支持 Dart VM，不支持 dart2js/dart2wasm 与 AOT 编译」，Flutter 明确不支持。也就是说在移动端与 Web 上，Dart 的封装是没有运行时逃生舱的——这跟 Java/C# 形成了鲜明对比。要在跨库场景下真正共享内部实现，Dart 的官方答案是 `part`（同一个 library 内共享私有），而不是反射。

```dart
// 需要跨文件共享私有实现 → part，而不是反射
// lib/shop.dart
library shop;
part 'src/account.dart';
// lib/src/account.dart
part of '../shop.dart';
// 两个文件共享同一个私有作用域
```

`json_serializable` 与 `freezed` 走的是**编译期代码生成**：`build_runner` 生成的 `.g.dart` 必须以 `part` 方式并入主文件，才能访问主文件里的私有字段并生成 `fromJson`/`toJson`。这跟 Rust 的派生宏、Swift 的 `Codable` 合成、Kotlin 的 `kotlinx.serialization` 是同一策略，也解释了 Dart 里 `part` 为什么没有被淘汰——它承担了「代码生成器需要访问私有」这个实际需求。依赖注入方面 `get_it`、`provider` 靠显式注册而不是反射（`get_it` 的 `registerFactory` 直接传构造函数），测试替身用接口的另一种实现或 `mockito` 的代码生成（`@GenerateMocks`，也是 build_runner 产物）。结论：Dart 的封装在主流编译目标上是**真边界**，这在本页的语言里属于第一档。

📘 [Dart · dart:mirrors](https://api.dart.dev/stable/dart-mirrors/dart-mirrors-library.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的反射能力覆盖了整个运行时对象系统：`asNamespace()` 拿到包的命名空间环境，`get`/`assign`/`ls` 读写任意绑定，`assignInNamespace()` 直接替换包内函数，`environment(f)` 取函数的闭包环境，`unlockBinding()` 解开锁定。这些 API 都是官方文档化的，`R CMD check` 会给使用 `:::` 访问外部包内部对象发 NOTE，但语言本身完全不阻止。

```r
# 读：拿到包内任意绑定
env <- asNamespace("stats")
ls(env)[1:3]                                  # 环境里的前三个名字
get("median", envir = env)                     # 函数对象
stats:::C_median                               # ⚠️ 三冒号：未导出对象也能取

# 写：替换包内函数（开发/调试用，官方不推荐生产使用）
assignInNamespace("median", function(x, ...) 0, ns = "stats")
median(1:10)                                   # 0     ⚠️ 已被替换

# 闭包环境也能拆
f <- function() { x <- 1; function() x }
environment(f())                               # 里面有 x
get("x", envir = environment(f()))              # 1
```

`assignInNamespace` 的官方态度很明确：它被放在「仅供开发与调试」的定位上，因为替换包内函数不会让已经编译/内联的引用失效，可能造成难以追踪的不一致。R6 类的 `private` 也拦不住环境操作——R6 的实现就是把私有成员放进一个封闭环境，但 `Counter$private` 之类的内部路径在知道结构后依然可及（`R6Class` 生成的 `private` 环境可以在 `self` 上找到）。所以 R 里没有真私有。

```r
library(R6)
Counter <- R6Class("Counter",
  private = list(n = 0),
  public = list(inc = function() { private$n <- private$n + 1; invisible(self) },
                value = function() private$n)
)
c1 <- Counter$new(); c1$inc()
c1$value()                       # 1
c1$n                             # NULL：公开面看不到
c1$.__enclos_env__$private$n      # ⚠️ 知道内部结构就能拿到
```

序列化与 ORM 在 R 里同样靠反射：`saveRDS`/`readRDS` 按对象结构序列化，`unserialize` 能还原环境、闭包与引用（因此也能还原私有状态）；`DBI` 与各类 ORM（`dbplyr`）靠 `environment` 与表达式捕获工作。依赖注入在 R 里很少用容器，主流做法是函数参数与 `options()`，测试替身用 `testthat::local_mocked_bindings()` 或 `mockery` 包——它们本质上就是在命名空间环境里临时替换绑定。结论：**R 的私有只是命名习惯与导出清单，任何运行时操作都能穿透**；如果 R 代码要处理敏感数据，安全边界必须放在进程、数据库权限或 API 层，而不是对象封装里。

📘 [R · assignInNamespace](https://stat.ethz.ch/R-manual/R-devel/library/utils/html/getFromNamespace.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 没有运行时反射，只有 comptime 的内省：`@typeInfo`、`@field`、`@hasField`、`std.meta.fields` 都是编译期求值的，因此它们看到的东西**就是编译器允许你看到的东西**。文件级私有的声明在 `@typeInfo` 里不会以「可访问」的形式出现——你无法用 `@field` 从一个容器里取未 `pub` 的函数，因为 `@field` 只作用于**字段**，而且名字必须静态可知。

```zig
const std = @import("std");

const Vault = struct {
    code: u32,                      // 字段：无可见性，外部可读写
    fn reset(self: *Vault) void { self.code = 0; }   // 未 pub：仅本文件
};

pub fn main() void {
    var v = Vault{ .code = 42 };
    std.debug.print("{d}\n", .{@field(v, "code")});   // 42  按名字取字段
    // Vault.reset(&v);                                // 🛑 'reset' is not marked 'pub'
    // @field(Vault, "reset");                         // 🛑 不行：@field 只用于字段
    const info = @typeInfo(Vault).@"struct";
    inline for (info.fields) |f| {
        std.debug.print("{s}\n", .{f.name});            // code（字段可见，函数不在其中）
    }
}
```

要强调的是「comptime 仍受约束」这一点：`@typeInfo` 只暴露**类型**的公开结构（字段列表、类型、对齐），不暴露容器的私有声明；想遍历一个模块里所有函数是不可能的，因为 Zig 没有「模块成员清单」这种运行时/编译期元数据可供遍历。这也意味着 Zig 里「依赖注入容器」这类东西不会以反射形式出现，而是靠 `build.zig` 在编译期组装（模块导入图就是注入图）。

```zig
// 编译期组装：build.zig 决定谁能 import 谁
// exe.root_module.addImport("store", store_mod);
// 没被 addImport 的模块在源码里根本 @import 不到（编译错误）
```

结构体字段永远是公开的这一点在 Zig 里是刻意的设计取舍：官方把「字段可见性」留给类型本身（用 `opaque {}` 或把定义藏进实现文件），而不是给每个字段加修饰符。测试方面 `test` 块与源文件同文件，所以能访问私有声明；跨文件测试想访问私有实现，只能把测试放进实现文件。安全模型上，Zig 的 `@ptrCast`、`@alignCast`、`std.mem.bytesAsValue` 等 unsafe 操作可以按已知布局读写内存，但前提仍然是你得先拿到那块内存与类型——没有「按字符串找成员」的路径。所以 Zig 的封装在编译期与运行时都是连贯的：**编译器允许看见的就是你能看见的全部**。

📘 [Zig · Documentation · comptime](https://ziglang.org/documentation/master/#comptime)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的反射工具是 `debug` 库，它能翻出几乎一切：`debug.getupvalue(f, n)` 按索引读闭包捕获的变量名与值、`debug.setupvalue` 改写它、`debug.getlocal`/`setlocal` 读写栈上局部变量、`debug.getinfo` 拿函数来源、`debug.setmetatable` 换元表（绕过 `__metatable` 保护）。官方把这些 API 定位为「调试与内省」，但语言不阻止生产代码调用它们。

```lua
-- 闭包私有：只能被 debug 库翻开
local function counter()
  local n = 0
  return { inc = function() n = n + 1; return n end }
end
local c = counter()
c.inc()
print(c.inc())                 -- 2
-- 用 debug 读 upvalue
local i = 1
while true do
  local name, val = debug.getupvalue(c.inc, i)
  if not name then break end
  print("upvalue", name, val)   -- upvalue n 2
  i = i + 1
end
debug.setupvalue(c.inc, 1, 100) -- ⚠️ 直接改写私有状态
print(c.inc())                  -- 101
```

元表层面的「保护」同样不堪一击：`__metatable` 字段能让 `getmetatable(t)` 返回一个假值，但 `debug.getmetatable(t)` 会无视它；只读表的 `__newindex` 拦截会被 `rawset` 绕过；`__index` 代理表也能被 `rawget` 绕过。唯一真正的封装是「数据只存在于闭包 upvalue 或 C 模块内部」，连名字都不暴露，此时不借助 `debug` 就无法枚举——这就是 Lua 里「真私有」的准确含义。

```lua
-- 沙箱：用 _ENV 限制可见的全局，连同 debug 一起拿走
local sandbox_env = { print = print, math = math }   -- 不提供 debug
local f = load("return 1 + 1", "chunk", "t", sandbox_env)
print(f())                                            -- 2
-- 此时 chunk 内部连 debug 这个名字都解析不到
```

实践中把 `debug` 库从沙箱里移除（通过 `_ENV` 或自定义 `load` 的环境）就能把「真私有」升级成「实际不可达」，这是游戏服务器与嵌入式 Lua 的标准做法。序列化在 Lua 里通常手写 `toTable`/`fromTable`，或者依赖 `serpent`、`json` 这类库遍历 table——它们只能看到 table 字段，看不到闭包 upvalue，所以闭包封装顺便让「意外序列化内部状态」变成了不可能。依赖注入在 Lua 里就是「把函数/表作为参数传进去」，测试替身直接替换参数或 `package.loaded` 里的模块，不需要任何可见性突破。

📘 [Lua 5.5 Reference Manual · Debug Library](https://www.lua.org/manual/5.5/manual.html#6.10)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的 `private`/`protected` 是**编译期私有**：编译产物里没有任何痕迹，`(obj as any).field`、`Object.keys`、`JSON.stringify` 全都能读到。`#` 是 ECMAScript 的真私有，编译到 ES2022 及以上时原样保留，编译到更低目标时由编译器用 WeakMap 模拟——注意最后这种情况的强度会变：模拟实现也是「外部拿不到」的，但它依赖编译器生成的辅助代码，不是引擎原生机制。

```typescript
class Vault {
  private code = 42;        // 编译期私有
  #pin = 1234;              // 真私有（ES2022+）
}
const v = new Vault();
console.log((v as any).code);      // 42   ⚠️ 运行时是普通属性
console.log(Object.keys(v));        // [ 'code' ]  ← #pin 不出现
// console.log((v as any).#pin);    // 🛑 SyntaxError
console.log(JSON.stringify(v));     // {"code":42}
```

`stripInternal` + `@internal` 是另一层：它从 `.d.ts` 里删除声明，让消费方的类型检查看不到这些 API，但不影响运行时代码，也不影响直接引用 `.ts` 源码的 monorepo 内部。这两层加在一起给出 TypeScript 的完整答案：**运行时的真私有只有 `#`，声明面的隐藏靠 `stripInternal`，其余都是编译期约定**。

```typescript
// 框架与 ORM 的实际做法
// - ORM（TypeORM/Prisma）：Prisma 用代码生成（客户端由 schema 生成），TypeORM 用装饰器 + reflect-metadata
// - 装饰器 + reflect-metadata 需要 emitDecoratorMetadata，会把类型信息写进元数据
import "reflect-metadata";
function Column(): PropertyDecorator {
  return (target, key) => {
    // 通过 Reflect.getMetadata("design:type", target, key) 读类型
  };
}
class User { @Column() name!: string; }
```

装饰器与 `reflect-metadata` 说明了「编译期私有」在实际框架里如何被绕过：装饰器拿到的 `target`/`key` 是运行时对象与属性名，`reflect-metadata` 还提供类型元数据，因此被 `private` 标记的属性照样能被框架读写——这也解释了为什么 TypeScript 的 ORM 生态大量使用装饰器（实验性装饰器）或代码生成（Prisma、Drizzle）。依赖注入方面，`InversifyJS` 等容器依赖 `reflect-metadata` + 装饰器，`tsyringe` 同理；它们都工作在运行时，`private` 对它们没有任何约束力。如果确实要阻止框架访问，唯一的办法是用 `#`，但那也意味着框架（同样）拿不到——所以设计上要在「框架可访问」与「真私有」之间做取舍。

📘 [TypeScript · Classes](https://www.typescriptlang.org/docs/handbook/2/classes.html#private)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的 `#` 字段在运行时是真私有，**外部没有任何 API 能读到它**：`Object.getOwnPropertyNames`、`Reflect.ownKeys`、`Object.getOwnPropertySymbols` 都不包含私有名字，`JSON.stringify` 也是空对象。唯一的合法探测是 `#name in obj`（且必须写在能解析该私有名字的类体内），所以「友元」只能通过类自己暴露的静态方法来造。

```javascript
class Vault {
  #code = 42;
  static peek(v) { return v.#code; }        // 类内可以互访私有
  static has(obj) { return #code in obj; }   // in 检测（ES2022）
}
const v = new Vault();
console.log(Vault.peek(v), Vault.has(v));    // 42 true
console.log(Vault.has({}));                   // false  普通对象没有该私有字段
console.log(Reflect.ownKeys(v));              // []
console.log(Object.getOwnPropertyNames(v));   // []
```

既然没有反射通道，框架该怎么办？答案是**让类主动配合**：`toJSON()` 由序列化方调用、`Symbol.toPrimitive`/`Symbol.iterator` 控制转换、静态工厂方法暴露需要共享的内部信息。JSON 序列化尤其明确——`JSON.stringify` 只调用 `toJSON()`（如果存在）并枚举自有可枚举属性，因此 `#` 字段默认不会被序列化；要序列化就让类型实现 `toJSON()`。这跟 Rust/Swift 的派生、Dart/Kotlin 的代码生成是同一思路：**序列化面由类型作者显式声明**。

```javascript
class Vault {
  #code = 42;
  toJSON() { return { code: this.#code }; }    // 显式决定序列化面
}
console.log(JSON.stringify(new Vault()));       // {"code":42}
```

依赖注入与测试替身在 JS 里同样不需要突破私有：模块系统（ESM）本身就是注入点（`import` 换成参数、或用 `node:test` 的 mock）、类可以设计成构造器接收依赖、`vm`/`worker` 可以加载替身实现。只有极少数测试框架的「私有方法 spy」需求会撞上 `#`，此时要么改设计（把逻辑抽成模块级函数，模块级函数可以被 spy）、要么用 `#foo in obj` 式的友元钩子。从封装强度看，JavaScript 的 `#` 是本页第一档里最彻底的一个：**它不是「访问受限制」，而是「从语言层就没有访问路径」**。需要注意的边界有两个：一是 `#` 字段在构造函数执行完之前访问会抛错（字段在构造期按声明顺序初始化，父类构造器访问子类私有字段必然失败）；二是 `#` 不能动态添加，也不能通过 `Object.defineProperty` 定义，因此无法做「后挂私有状态」。

📘 [MDN · Private class features](https://developer.mozilla.org/docs/Web/JavaScript/Reference/Classes/Private_class_fields)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的可见性是**运行时强制**的，但反射与 `Closure::bind` 提供了官方绕过通道。`ReflectionProperty::setAccessible()` 从 PHP 8.1 起已经没有任何效果（所有属性默认可通过反射访问），PHP 8.5 正式把它标记为废弃；`Closure::bind()` 则允许把一个匿名函数绑定到指定对象的类作用域，于是函数体里就能直接读写 `private`。

```php
class Vault {
    public function __construct(
        private int $code = 42,
        public readonly string $name = "v",
    ) {}
}

$v = new Vault();

// 1) 反射读私有（8.1 起无需 setAccessible）
$rp = new ReflectionProperty(Vault::class, 'code');
echo $rp->getValue($v);              // 42
$rp->setValue($v, 99);               // ⚠️ 能写
echo $rp->getValue($v);              // 99

// 2) Closure::bind 换作用域
$read = Closure::bind(fn() => $this->code, $v, Vault::class);
echo $read();                         // 99
```

`Closure::bind` 的语义值得说清楚：第二个参数给对象、第三个参数给作用域类名，绑定后闭包里的 `$this` 是那个对象、可见性按第三个参数那个类判定；传 `null` 作为作用域可以让闭包失去作用域（访问不了 `private`）。它常被用在调试工具与序列化库里，也可以用来实现「只读视图」：绑定一个只读闭包给外部。序列化方面，PHP 的 `serialize()` 会保留 `private` 与 `protected` 属性的**名字改写形式**（`\0ClassName\0prop`、`\0*\0prop`），`__serialize()`/`__sleep()` 是控制序列化面的官方钩子；`json_encode` 只处理 `public` 属性（实现 `JsonSerializable` 可以自定义），这也是 PHP 生态里「私有属性默认不出现在 JSON 里」的原因。

```php
class Vault {
    private int $code = 42;
    public function jsonSerialize(): array { return ['code' => $this->code]; }
}
```

`readonly` 与属性钩子带来两个新的交互点：`readonly` 属性在 `unserialize` 或克隆时由引擎特殊处理，已经初始化过的 `readonly` 属性被反射修改会抛 `Error`；8.4 起 `readonly` 的隐含 set 可见性从 `private(set)` 放宽为 `protected(set)`，所以子类可以初始化父类的 `readonly` 属性。属性钩子（8.4）让 `getValue()` 的结果可能来自钩子计算而非存储，此时要用 `getRawValue()` 读原始值，反过来 `setRawValue()` 会绕过 `set` 钩子直接写存储。依赖注入方面 PHP 的容器（Symfony DI、Laravel）大量使用反射读构造器参数类型并自动装配，这也意味着**构造器参数与类型声明实际上是框架的公开 API**；测试替身靠接口 + `PHPUnit` 的 mock（运行时生成代理类）实现，不需要访问私有。结论：**PHP 的 `private` 是运行时机制，但反射让它在运行时失守**，唯一无法被反射改变的是 `final` 的继承约束与 `readonly` 的单次写入语义。

📘 [PHP · ReflectionProperty::setAccessible (deprecated since 8.5)](https://www.php.net/manual/en/reflectionproperty.setaccessible.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的反射工具最齐全：`send`/`__send__` 调用私有方法、`public_send` 尊重可见性、`instance_variable_get`/`set` 读写实例变量、`const_get` 取私有常量、`define_method` 动态定义、`method(:x).unbind` 拿到 `UnboundMethod`、`Module#private_instance_methods` 列出私有方法。`private` 的全部作用只是「禁止显式 receiver 调用」，所以这些 API 都能绕过去。

```ruby
class Vault
  def initialize = @code = 42
  private
  def reset = @code = 0
end

v = Vault.new
v.reset                                   # 🛑 NoMethodError: private method 'reset'
v.send(:reset)                             # ✅ 绕过
v.instance_variable_get(:@code)             # 0
v.instance_variable_set(:@code, 7)          # ✅ 直接改
Vault.private_instance_methods(false)       # [:reset, :initialize]（Ruby 4.0 实测）
v.method(:reset).call                       # ✅ Method 对象也能调私有方法
```

`v.method(:reset)` 能取到私有方法的 `Method` 对象并调用，这是比 `send` 更隐蔽的绕过方式；`public_send` 与 `send` 的差别是前者会做可见性检查，所以在写库时用它来表达「我尊重你的封装」。另一个与封装相关的机制是 `Refinements`：它能在限定作用域内改写方法，用来替换依赖或做测试替身，且不会泄漏到作用域之外；但它同样不是访问控制，`Module#refine` 定义出来的模块可以被重新打开。

```ruby
# refinements 做测试替身：只在当前作用域生效
module FakeClock
  refine Time.singleton_class do
    def now = Time.at(0)
  end
end
class Service
  using FakeClock
  def stamp = Time.now.to_i          # 0
end
puts Service.new.stamp                # 0
puts Time.now.to_i > 0                # true：作用域外仍是真实时间
```

序列化与 ORM 在 Ruby 里高度依赖反射：`Marshal.dump` 直接序列化实例变量（包含私有状态）、`ActiveRecord` 用 `instance_variable_get`/`instance_variable_set` 读写属性、`YAML.load` 与 `JSON`（配 `as_json`）各有各的面。`attr_accessor` 生成的是公开方法，但内部仍存在 `@ivar`，所以「私有字段」在 Ruby 里几乎总是可以通过 `instance_variable_get` 拿到。依赖注入方面 Ruby 主流是构造器注入（`initialize(dep:)`），测试替身用 `double`/`instance_double`（`RSpec` 会校验方法存在性，这对重构友好）或依赖替换。结论：**Ruby 的 `private` 是「防手滑」的编译期之外的软约束**，它有效是因为打破它的代码很显眼（`send`、`instance_variable_get`），而不是因为技术上不可能。

📘 [Ruby · Module#private](https://docs.ruby-lang.org/en/master/Module.html#method-i-private)

{{% /tab %}}

{{< /tabpane >}}

**几个特殊的边界判断**

`InternalsVisibleTo`（C#）、`@testable`（Swift）、`associate` 配置下的测试 source set（Kotlin）、同包测试类（Java）这四种机制解决的是同一个问题——**让测试看到生产代码的内部**，但它们的强度不同：C# 与 Swift 是显式的程序集/模块级开关，Java 靠「同包名」这一语言事实免费获得，Kotlin 靠构建配置。Rust、Go、Zig、Dart 这类「测试与源码同文件或同包」的模型则根本不需要这类机制。

关于「封装是编译期契约还是安全边界」，可以给出一条可操作的判据：**如果绕过封装需要写 `unsafe`、反射、`send` 这类一眼可疑的代码，那它是契约；如果绕过它只是换个正常写法就能做到，那它连契约都算不上**。按这个尺度排下来，JavaScript 的 `#`、Rust 的模块私有、Go 的未导出字段、Zig 的文件私有属于真边界；Java/C#/Kotlin/PHP/Swift 的 `private` 属于契约；Python/R/Julia/Lua 表字段/C 结构体字段属于命名习惯。序列化框架与 ORM 的设计压力正来自这里：它们要么走编译期代码生成（Rust 派生、Swift `Codable`、Dart/Kotlin 代码生成、C# 源生成器），要么就得在文档里要求你放宽可见性（Java 的 `opens`、Python 的 `__dict__`）。测试替身与依赖注入则提醒我们：需要被替换的东西应该是**接口**而不是内部字段，把封装当安全边界用，最终会在第一次需要序列化或打桩时崩塌。
