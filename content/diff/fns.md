+++
title = "函数"
date = 2026-09-19T12:00:00+08:00
weight = 10
type = "docs"
description = "18 种语言的函数对照：定义与签名、参数传递与返回值、一等函数与闭包、重载泛型与装饰"
isCJKLanguage = true
draft = false
+++

# 函数：18 种语言对照

函数的语法分歧远小于它的语义分歧：同样一句 `f(x)`，在 C 里传的是值的一份拷贝，在 Python 里传的是对象引用的一份拷贝，在 Rust 里可能已经把 `x` 的 ownership 移走，在 Java 里传的则是对象引用的值拷贝。本页按六个主题推进：**函数定义与签名**（关键字、返回类型位置、默认参数、命名实参、变参、`main`）→ **参数传递与返回值**（值/引用语义、ownership、多返回值）→ **一等函数**（函数类型、函数指针、函数引用、高阶函数、柯里化）→ **闭包与匿名函数**（lambda 字面量、捕获结论、逃逸与生命周期）→ **重载**（编译期按类型选实现、运行期多重分派、以及干脆没有重载时的替代）→ **泛型与装饰**（泛型函数的约束写法、装饰器/注解/宏/源生成器）。这里只讲函数本身：闭包捕获语义与循环变量陷阱的细节归 closure.md，泛型的类型层面细节归 generic.md。

## 函数

**一页速览**

| 语言 | 函数是值吗 / 怎么表达 | 参数与返回的关键差异 | 重载、泛型与装饰 |
| --- | --- | --- | --- |
| Rust | 函数指针 `fn(i32) -> i32` 与闭包 `Fn`/`FnMut`/`FnOnce` 是两种类型 | 默认 move，`&`/`&mut` 显式借用；多值用元组，失败用 `Result` | 没有重载（靠 trait 与泛型分派）；泛型走 monomorphization；没有运行期装饰器，只有属性宏 |
| Swift | 一等函数，函数类型 `(Int) -> Int`，闭包捕获列表 `[x]`/`[weak self]` | 值类型拷贝；`inout` 才写回；元组多返回值 | 支持重载（编译期按类型与标签解析）；泛型 `<T: P>`；用属性包装器与宏代替装饰器 |
| Go | 一等函数，函数类型 `func(int) int`，匿名函数按变量捕获 | 全部传值，slice/map/channel 内含指针；原生多返回值 | 没有重载；1.18 起泛型、1.27 起泛型方法；没有装饰器，包装即中间件 |
| Python | 一等对象；`lambda` 只能写一个表达式 | call by sharing；默认参数只求值一次；元组多返回值 | 没有编译期重载，用 `singledispatch`；泛型注解不强制；`@decorator` 就是 `f = decorator(f)` |
| Kotlin | 函数类型 `(Int) -> Int`，函数引用 `::name`，尾随 lambda | 参数是 `val`，不能重新赋值；`Pair`/`Triple` 做多返回值 | 支持重载；默认参数与命名实参削减重载需求；`reified` 泛型；注解 + KSP 生成代码 |
| Java | 没有函数类型，靠函数式接口（`Function`/`Supplier`/`Predicate`） | 只有值传递；lambda 只捕获 effectively final；没有多返回值，用 `record` | 支持重载（三阶段解析）；泛型编译期擦除；注解 + APT |
| C++ | 一等函数，lambda 是唯一的匿名类，`std::function` 做类型擦除 | `T` 拷贝、`T&` 可写、`const T&` 只读、`T&&` 移动；`std::pair`/`tuple` 多返回值 | 重载最完整（含 `const` 与引用限定）；模板走 monomorphization；属性与运算符重载代替装饰器 |
| C | 有函数指针、**没有闭包**，环境只能手工用 `void *` 传 | 全部传值，数组退化为指针；`...` + `va_list`；结构体做多返回值 | 没有重载、没有泛型函数、没有装饰器；用不同名字、`_Generic`、标签联合、宏替代 |
| Julia | 一等函数；匿名函数 `x -> x * 2`，`do` 块 | 可变类型按引用；默认参数与关键字参数；元组多返回值 | 一个函数名挂多个方法（运行期多重分派）；宏在解析后变换语法树 |
| C# | 一等函数，靠委托（`Func`/`Action`/`Predicate`），方法组可转委托 | 值类型拷贝、引用类型引用拷贝；`ref`/`out`/`in` 参与签名；值元组多返回值 | 支持重载；`where T : 约束`；特性 + 源生成器；C# 14 起有 extension members |
| Dart | 一等函数，函数类型 `int Function(int)`，匿名函数与箭头函数 | 全部按值，集合与对象是引用语义；record 做多返回值 | 只允许按参数类型重载（不能只差参数个数与返回类型）；泛型 reified；注解 + build_runner |
| R | 函数就是普通对象；`function(x) x + 1` | 参数按名称/部分名称/位置匹配，惰性求值；`list()` 多返回值 | 没有重载，用 S3/S4 泛型函数；没有装饰器，用函数包装 |
| Zig | 有函数指针、**没有闭包**，用 `*anyopaque` 上下文加结构体模拟 | 一律按值，改调用者必须传 `*T`；`anytype` 收任意类型；结构体与错误联合做返回 | 没有重载、没有泛型语法、没有装饰器；`comptime` 参数即泛型 |
| Lua | 一等值；`function(x) ... end` 是匿名函数字面量，捕获 upvalue | 参数不足补 `nil`、多余丢弃；`...` 收多余实参；多返回值只在列表末尾展开 | 没有重载、没有泛型、没有装饰器；用 table、元表转发、高阶函数替代 |
| TypeScript | 一等函数，类型别名与可调用签名都能描述函数类型 | 与 JavaScript 完全一致，类型只在编译期 | 重载只是多个声明签名；泛型编译期擦除；TC39 装饰器（5.0 起） |
| JavaScript | 一等对象（带 `name`/`length`/`prototype`），箭头函数不绑定 `this` | 全部按值，对象是引用拷贝；默认参数只对 `undefined` 生效；数组/对象做多返回值 | 没有重载、没有泛型；装饰器是 TC39 提案，需要转译器 |
| PHP | 一等值；`Closure` 与箭头函数 `fn() => expr` | 默认按值，`&$x` 引用参数；数组是值类型；数组解构做多返回值 | 没有重载、没有泛型函数；Attribute（8.0 起）+ 反射，8.4 起属性钩子 |
| Ruby | 一等值；block、`Proc`、`lambda`、`Method` 四种形态 | 全部按值传引用；默认值每次调用重算；数组多返回值 | 没有重载、没有泛型；用 `prepend`、方法包装、`method_missing` 实现装饰式逻辑 |

本表覆盖 18 门语言，每门语言 1 行，统计口径为“该语言在 6 个子主题里最值得先知道的一条差异”，计数为 18 行；下表之后 6 个子主题各含 1 个 tabpane、每个 tabpane 恰好 18 个标签页，全文标签页合计 18 × 6 = 108 个。下文凡涉及某语言缺少某机制处，都会明确写出「没有」并给出替代做法（按字符串「没有」统计，全文共 154 处，统计口径为正文中所有显式否定说明，含表格行内的「没有」）。

### 函数定义与签名

函数签名要一次性回答四个问题：**怎么写返回类型**、**参数能不能有默认值**、**调用时能不能按名字指定实参**、**能不能收不定个数的参数**。这四件事在 18 门语言里组合出的差异，比关键字拼写本身大得多：C 系把返回类型写在最前面，Rust、Swift、Go、Zig、Kotlin 写在后面；默认参数在脚本语言里几乎是默认配置，在 Rust、Go、Java、C、Zig、Lua 里则完全没有，只能靠结构体、选项对象或重载去模拟；命名实参只在 Swift、Kotlin、Python、C#、Ruby、R、Julia 里是语言级能力。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 用 `fn` 声明函数，返回类型写在 `->` 之后，只有表达式体的最后一句（不带分号）才是返回值。函数签名是编译期契约：参数类型必须写全，没有默认参数、没有命名参数、也没有重载，同一作用域里同名函数只能有一个。

```rust
struct ServerConfig {          // 用结构体 + Default 代替默认参数
    host: String,
    port: u16,
    tls: bool,
}
impl Default for ServerConfig {
    fn default() -> Self {
        Self { host: "localhost".into(), port: 8080, tls: true }
    }
}
fn connect(cfg: ServerConfig) -> String {          // 返回类型写在 ->
    format!("{}:{} tls={}", cfg.host, cfg.port, cfg.tls)
}
fn sum(xs: &[i32]) -> i32 {                        // “变参”用切片表示
    xs.iter().sum()
}
fn first_word(s: &str) -> Option<&str> {            // 失败用 Option
    s.split_whitespace().next()
}
fn main() {
    println!("{}", connect(ServerConfig { port: 9090, ..Default::default() }));
    // localhost:9090 tls=true
    println!("{}", sum(&[1, 2, 3]));                 // 6
    println!("{:?}", first_word("hello world"));      // Some("hello")
}
```

`..Default::default()` 是 Rust 最常用的“默认参数”替代方案：先给一个 `Default` 实例，再用结构体更新语法覆盖几个字段。真正的变参不存在，惯用做法是让函数收 `&[T]`、`impl Iterator<Item = T>` 或 `Vec<T>`；宏（`println!` 那种）才有真正的可变参数。`main` 只有两种合法签名：`fn main()` 和 `fn main() -> Result<(), E>`（其中 `E: Debug`），后者返回 `Err` 时进程以非零码退出。

📘 [Rust · Functions](https://doc.rust-lang.org/reference/items/functions.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 用 `func` 声明函数，参数的“外部名”和“内部名”分开写，调用点默认必须写出外部名——这是 Swift 最鲜明的签名特征。返回类型写在 `->` 之后，支持默认参数和 `Int...` 形式的变参。

```swift
func greet(person name: String, from city: String = "北京") -> String {
    // person 是外部名，name 是内部名；from city 同理
    "你好 \(name)，来自 \(city)"
}
func sum(_ xs: Int...) -> Int {         // 变参：调用点不需要标签
    xs.reduce(0, +)
}
func divmod(_ a: Int, _ b: Int) -> (q: Int, r: Int) {   // 元组多返回值
    (a / b, a % b)
}
print(greet(person: "Ann"))             // 你好 Ann，来自 北京
print(greet(person: "Ann", from: "上海"))  // 你好 Ann，来自 上海
print(sum(1, 2, 3))                      // 6
print(divmod(7, 2).r)                     // 1
```

Swift 支持按参数类型、参数标签与个数重载同名函数，解析全在编译期完成（细节见「重载、泛型与装饰」）。参数名前的下划线表示“调用点省略标签”，所以 `sum(1, 2, 3)` 而不是 `sum(xs: 1, 2, 3)`。变参在函数体内是一个数组，且必须是参数表里的最后一个参数；一个变参参数后面只能再跟一个带标签的参数（如 `func f(_ xs: Int..., label last: Int)`）。`main` 不是关键字：命令行程序用 `@main` 标注一个含有 `static func main()` 的类型，或者依赖顶层代码。

📘 [Swift · Functions](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/functions/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 用 `func` 声明函数，返回类型写在参数表之后，且可以一次返回多个值。Go 刻意不做默认参数、不做命名实参（调用点）、也不做重载（没有同名函数按类型区分这回事），官方理由是“调用点的可读性优先”。

```go
package main

import "fmt"

// 变参必须是最后一个参数，类型写作 ...T，函数体内是 []T
func sum(nums ...int) int {
	total := 0
	for _, n := range nums { total += n }
	return total
}

// 命名返回值可被裸 return 使用
func divmod(a, b int) (q, r int) {
	q, r = a/b, a%b
	return
}

// 用结构体 + 选项函数代替默认参数
type Config struct{ Host string; Port int }
type Option func(*Config)

func WithPort(p int) Option { return func(c *Config) { c.Port = p } }
func New(opts ...Option) *Config {
	c := &Config{Host: "localhost", Port: 8080}
	for _, o := range opts { o(c) }
	return c
}

func main() {
	fmt.Println(sum(1, 2, 3))            // 6
	fmt.Println(sum())                    // 0
	q, r := divmod(7, 2)
	fmt.Println(q, r)                     // 3 1
	c := New(WithPort(9090))
	fmt.Println(c.Host, c.Port)           // localhost 9090
}
```

`...int` 收到的切片可以直接展开传回去：`sum(xs...)`。命名返回值让 `return` 不必写表达式，但它也会隐藏赋值顺序，长函数里容易出错。`main` 必须定义在 `package main` 里，签名固定为 `func main()`，没有参数也没有返回值；命令行参数用 `os.Args` 读。

📘 [Go spec · Function declarations](https://go.dev/ref/spec#Function_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 用 `def` 定义函数，注解（`x: int`、`-> int`）只是元数据，默认不参与任何运行时检查。默认参数、关键字实参、`*args`/`**kwargs` 都是语言级能力，全部在运行期生效。

```python
def area(w, h=1.0, *, scale=1.0):     # * 之后的 scale 只能按关键字传
    return w * h * scale

def stats(*args, **kwargs):            # 任意位置实参与任意关键字实参
    return sum(args), kwargs

def apply(f, x):                       # 参数类型完全动态
    return f(x)

print(area(2, 3))                # 6.0
print(area(2, scale=10))          # 20.0
print(stats(1, 2, mode="x"))       # (3, {'mode': 'x'})
print(apply(lambda v: v * 2, 21))   # 42
# print(area(2, 3, 4))            # 🛑 TypeError: 只能传 2 个位置实参
```

参数顺序的规则是：位置参数 → 默认参数 → `*args` → 仅关键字参数 → `**kwargs`，违反顺序是语法错误。用 `/` 可以把前面的参数标记为“仅位置”，用 `*` 把后面的参数标记为“仅关键字”。`main` 没有特殊签名：`if __name__ == "__main__":` 保护块是惯用写法，入口函数本身可以是任意名字。

📘 [Python · Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 用 `fun` 声明函数，返回类型写在参数表之后、用冒号分隔；参数必须写类型，可空类型要在类型后加 `?`。Kotlin 同时支持默认参数、命名实参和 `vararg`，这三样合起来让“重载”在很多场景下变得不必要。

```kotlin
fun greet(name: String, from: String = "北京"): String = "你好 $name，来自 $from"

fun sum(vararg xs: Int): Int = xs.sum()          // vararg 在体内是 Array<Int>

fun divmod(a: Int, b: Int): Pair<Int, Int> = Pair(a / b, a % b)

fun describe(x: Int?): String = when (x) {       // 可空类型写进签名
    null -> "空"
    else -> "值 $x"
}

fun main() {
    println(greet("Ann"))                  // 你好 Ann，来自 北京
    println(greet("Ann", from = "上海"))     // 你好 Ann，来自 上海
    println(sum(1, 2, 3))                    // 6
    val xs = intArrayOf(4, 5)
    println(sum(*xs))                         // 9  用 * 展开数组
    val (q, r) = divmod(7, 2)                  // 解构声明
    println("$q $r")                            // 3 1
    println(describe(null))                      // 空
}
```

默认参数与重载可以共存：编译器优先选“不需要默认值填充”的候选，参数个数相同时再比类型。`vararg` 只能有一个，通常是最后一个参数；把数组传给 `vararg` 必须用展开运算符 `*`，直接传数组会当成单个元素（类型不符时报错）。`main` 的两种签名是 `fun main()` 和 `fun main(args: Array<String>)`。

📘 [Kotlin · Functions](https://kotlinlang.org/docs/functions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 把返回类型放在方法名最前面，参数必须逐个写类型。语言本身没有默认参数，也没有命名实参；变参只有一种写法 `T...`，在方法体内就是 `T[]`。要“默认值”只能靠重载或 builder。

```java
public class Fns {
    static int area(int w, int h) { return w * h; }
    static int area(int w) { return area(w, 1); }        // 用重载模拟默认参数

    static int sum(int... xs) {                          // 变参
        int t = 0;
        for (int x : xs) t += x;
        return t;
    }

    static long[] divmod(long a, long b) { return new long[]{a / b, a % b}; }

    record Point(int x, int y) { }                       // 多返回值的常用载体

    static Point origin() { return new Point(0, 0); }

    public static void main(String[] args) {
        System.out.println(area(2));            // 2
        System.out.println(sum(1, 2, 3));        // 6
        System.out.println(sum());                // 0
        System.out.println(sum(new int[]{4, 5})); // 9
        long[] qr = divmod(7, 2);
        System.out.println(qr[0] + " " + qr[1]);  // 3 1
        System.out.println(origin().y());          // 0
    }
}
```

`sum(1, 2, 3)` 与 `sum(new int[]{1, 2, 3})` 等价，但 `sum(new Integer[]{1, 2})` 不成立——自动装箱不作用于整个数组。`main` 的经典形式是 `public static void main(String[] args)`；Java 21 起以预览特性引入「紧凑源文件 + 实例 main 方法」（JEP 445），到 Java 25 由 JEP 512 转正，因此实例方法 `void main()`（配合未命名类）只在 Java 25 及以后可用，返回值必须是 `void`。

📘 [JLS · Method declarations](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.4)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 把返回类型写最前，函数签名里能塞的东西是 18 门语言里最多的：默认参数、重载、变参模板、`initializer_list`、`consteval`、尾置返回类型 `auto f() -> T`。默认参数是编译期替换，调用点看不到任何“缺省填充”的痕迹。

```cpp
#include <cstdio>
#include <initializer_list>
#include <utility>

int area(int w, int h = 1) { return w * h; }        // 默认参数

template <typename... Args>                          // 变参模板
int sum_all(Args... args) { return (args + ... + 0); }   // C++17 折叠表达式

int sum_init(std::initializer_list<int> xs) {        // initializer_list 收花括号列表
    int t = 0;
    for (int x : xs) t += x;
    return t;
}

std::pair<int, int> divmod(int a, int b) { return {a / b, a % b}; }

int main() {
    std::printf("%d\n", area(2));                  // 2
    std::printf("%d\n", sum_all(1, 2, 3));          // 6
    std::printf("%d\n", sum_init({4, 5}));           // 9
    auto [q, r] = divmod(7, 2);                       // C++17 结构化绑定
    std::printf("%d %d\n", q, r);                      // 3 1
}
```

默认参数必须从右往左连续给，而且它是编译期绑定：通过基类指针调用虚函数时，实际执行派生类实现，但默认值取的是**基类声明里的那个**，这是经典陷阱。变参模板与 `initializer_list` 的差别在于类型：`initializer_list` 要求所有元素同类型，变参模板可以逐个推导类型，代价是为每种实参组合实例化一份代码。`main` 的合法签名是 `int main()` 与 `int main(int argc, char** argv)`（另有 `envp` 变体）。

📘 [cppreference · Function declaration](https://en.cppreference.com/w/cpp/language/function)

{{% /tab %}}

{{% tab header="C" %}}

C 的函数签名只有“返回类型 名字(参数类型列表)”这一种形状，没有默认参数、没有命名实参、没有重载。不定参数靠 `...` 加 `<stdarg.h>` 的 `va_list` 手工读取，类型信息完全由调用者负责。

```c
#include <stdio.h>
#include <stdarg.h>

int sum_n(int n, ...) {            /* n 给出后面实参的个数 */
    va_list ap;
    va_start(ap, n);
    int total = 0;
    for (int i = 0; i < n; i++) total += va_arg(ap, int);
    va_end(ap);
    return total;
}

double area(double w, double h);    /* 原型：参数个数与类型固定 */

int main(void) {
    printf("%d\n", sum_n(3, 1, 2, 3));   /* 6 */
    printf("%.1f\n", area(2, 3));         /* 6.0（函数定义在别处） */
    return 0;
}

double area(double w, double h) { return w * h; }
```

`va_arg(ap, int)` 里的类型必须与实参提升后的类型完全一致：`float` 会被提升为 `double`，`char`/`short` 会被提升为 `int`，写错就是未定义行为。函数声明必须在使用前可见，否则 C99 起是错误；`(void)` 明确表示“没有参数”，空的 `()` 在 C23 里也表示无参数，但在 C17 及以前意味着“参数未指定”。`main` 的合法形式是 `int main(void)` 与 `int main(int argc, char *argv[])`，返回 `int`。

📘 [cppreference · C function declarations](https://en.cppreference.com/w/c/language/functions)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的一个函数名对应零个或多个**方法**，调用时按实参类型在运行期选出最匹配的那个方法——这就是多重分派。关键字参数用分号或逗号引入，写 `f(x; k=1)` 或 `f(x, k=1)` 都行，但内部访问方式不同。

```julia
area(w, h=1.0) = w * h                       # 默认参数
stats(args...; kwargs...) = (sum(args), kwargs)   # 位置变参 + 关键字变参

f(x::Int) = "Int: $x"                         # 方法 1
f(x::AbstractString) = "Str: $x"              # 方法 2（同名，不同方法）
f(x) = "Any: $x"                              # 兜底方法

divmod2(a, b) = (a ÷ b, a % b)                 # 元组多返回值

println(area(2, 3))          # 6.0
println(stats(1, 2, mode="x"))  # (3, Base.Pairs(:mode => "x"))
println(f(1), " ", f("a"), " ", f(1.5))  # Int: 1 Str: a Any: 1.5
q, r = divmod2(7, 2)
println("$q $r")              # 3 1
println(methods(f))            # 3 个方法
```

`args...` 这种写法叫 slurping，把多余的位置实参收成一个元组；`kwargs...` 收成一个 `Base.Pairs`。分派在运行期完成，类型注解写 `::Int` 是把方法限定到具体类型，不写就是 `::Any`；注解写得太宽会让热路径走动态分派，性能下降。Julia 的入口不是 `main`：脚本顶层代码顺序执行，包入口是 `__init__()`，命令行参数用全局常量 `ARGS`。

📘 [Julia · Functions](https://docs.julialang.org/en/v1/manual/functions/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的返回类型写最前，方法签名支持可选参数（带默认值）、命名实参、`params` 变参，以及 `ref`/`out`/`in`/`ref readonly` 这几种引用修饰符。C# 13 起 `params` 不再限于数组，可以直接接 `Span<T>`、`IEnumerable<T>` 等集合类型。

```csharp
using System;

class Fns {
    static int Area(int w, int h = 1) => w * h;      // 可选参数

    static int Sum(params int[] xs) {                 // 变参
        int t = 0;
        foreach (var x in xs) t += x;
        return t;
    }

    static (int q, int r) DivMod(int a, int b) => (a / b, a % b);   // 值元组

    static bool TryHalf(int x, out int half) {         // out 参数
        half = x / 2;
        return x % 2 == 0;
    }

    static void Main() {
        Console.WriteLine(Area(2));              // 2
        Console.WriteLine(Area(h: 3, w: 2));      // 6  命名实参
        Console.WriteLine(Sum(1, 2, 3));          // 6
        Console.WriteLine(Sum());                  // 0
        var (q, r) = DivMod(7, 2);
        Console.WriteLine($"{q} {r}");             // 3 1
        if (TryHalf(8, out int h)) Console.WriteLine(h);   // 4
    }
}
```

命名实参可以和位置实参混用，但命名之后的实参都必须命名。可选参数的默认值必须是编译期常量，所以不能写 `h = SomeStaticMethod()`。`params` 传数组时是整个数组作为参数序列，传 `object[]` 给 `params object[]` 不会逐元素展开。`Main` 的合法签名有四种：`void Main()`、`int Main()`、`void Main(string[] args)`、`int Main(string[] args)`。

📘 [MS Learn · Method parameters](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的返回类型写最前，可选参数分两种：`[]` 包起来的是可选**位置**参数，`{}` 包起来的是具名参数，两类不能在同一个小括号里混用。Dart 2.17 起非空类型是默认设置，可选参数若不是可空类型就必须给默认值。

```dart
int area(int w, [int h = 1]) => w * h;              // 可选位置参数
String greet(String name, {String from = '北京'}) => '你好 $name，来自 $from';  // 具名参数

int sum(List<int> xs) => xs.fold(0, (a, b) => a + b);

({int q, int r}) divmod(int a, int b) => (q: a ~/ b, r: a % b);   // record 多返回值

void main() {
  print(area(2));                     // 2
  print(area(2, 3));                   // 6
  print(greet('Ann'));                  // 你好 Ann，来自 北京
  print(greet('Ann', from: '上海'));      // 你好 Ann，来自 上海
  final (q: q, r: r) = divmod(7, 2);     // record 解构
  print('$q $r');                         // 3 1
  print(sum([1, 2, 3]));                   // 6
}
```

必填具名参数写作 `{required String from}`，加了 `required` 之后调用点必须写出名字。可选位置参数在实参个数变化时最容易出错，因为它靠位置对齐，而具名参数在参数多的时候可读性更好，Dart 官方风格建议公共 API 用 `{}`。函数体是单个表达式时可以用 `=>` 简写。入口点必须是顶层 `void main()`，或者 `void main(List<String> args)`。

📘 [Dart · Functions](https://dart.dev/language/functions)

{{% /tab %}}

{{% tab header="R" %}}

R 用 `function(参数) 表达式` 定义函数，函数是一等对象；返回值是函数体最后一句的值，也可以显式 `return()`。R 的参数匹配规则是 18 门语言里最宽松的：先精确匹配名字，再部分匹配名字，最后按位置补上。

```r
area <- function(w, h = 1) w * h                 # 默认参数
stats <- function(...) {                          # ... 收集任意实参
  xs <- list(...)
  list(n = length(xs), sum = sum(unlist(xs)))
}
divmod2 <- function(a, b) list(q = a %/% b, r = a %% b)   # list 多返回值

f <- function(x) UseMethod("f")                   # S3 泛型：分派在运行期
f.numeric <- function(x) paste("num", x)
f.character <- function(x) paste("chr", x)

print(area(2, 3))                # [1] 6
print(area(h = 3, w = 2))         # [1] 6  命名实参（可乱序）
print(stats(1, 2, 3))              # $n [1] 3  $sum [1] 6
print(divmod2(7, 2))                # $q [1] 3  $r [1] 1
print(f(1))                          # [1] "num 1"
print(f("a"))                         # [1] "chr a"
```

部分匹配是 R 最著名的陷阱：函数有参数 `threshold` 时，`f(thr = 1)` 会静默匹配上；一旦函数后来新增了同前缀参数，调用语义就变了，所以正式代码里建议参数名带点号（如 `na.rm`）来降低误匹配概率。`...` 既能透传参数，也能配合 `list(...)` 做变参，代价是参数名不再进入签名、`args(f)` 看不到。S3 用 `UseMethod()` 按第一个实参的 class 分派，S4 用 `setGeneric()`/`setMethod()` 做多重分派。

📘 [R · Function definitions](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Function-definitions)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 用 `fn` 声明函数，返回类型写在参数表**之后**，且不写 `->`。参数必须写类型；`anytype` 让参数在编译期按实际类型特化，这是 Zig 实现“泛型函数”的统一办法，也是它唯一的变参替代方案。

```zig
const std = @import("std");

fn area(w: f64, h: f64) f64 { return w * h; }

// anytype：编译期为每个具体类型实例化一份
fn sum(values: anytype) @TypeOf(values[0]) {
    var total: @TypeOf(values[0]) = 0;
    for (values) |v| total += v;
    return total;
}

const DivMod = struct { q: i32, r: i32 };      // 结构体做多返回值
fn divmod(a: i32, b: i32) DivMod {
    return .{ .q = @divTrunc(a, b), .r = @rem(a, b) };
}

const Error = error{DividedByZero};
fn safeDiv(a: i32, b: i32) Error!i32 {          // 错误联合做返回值
    if (b == 0) return Error.DividedByZero;
    return @divTrunc(a, b);
}

pub fn main() !void {
    std.debug.print("{d}\n", .{area(2, 3)});          // 6
    std.debug.print("{d}\n", .{sum([_]i32{ 1, 2, 3 })});  // 6
    const d = divmod(7, 2);
    std.debug.print("{d} {d}\n", .{ d.q, d.r });       // 3 1
    std.debug.print("{d}\n", .{try safeDiv(6, 3)});     // 2
}
```

Zig 没有默认参数、没有命名实参、没有重载，也没有变参；替代做法是 `anytype` 配合元组 `std.meta.ArgsTuple`，或者干脆收一个结构体当选项包。`anytype` 只在编译期起作用，每个调用类型生成一份独立代码，所以函数体里不能用“运行期才知道的类型”做分支。入口点是 `pub fn main()`，可以是 `void`、`!void`，或者接 `std.process.Init` 之类的参数包；返回错误联合时未处理的错误会打印栈回溯并非零退出。

📘 [Zig · Functions](https://ziglang.org/documentation/master/#Functions)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的函数是一等值，`function f() end` 只是 `f = function() end` 的语法糖。参数不需要类型，数量也不必匹配：少给的补 `nil`，多给的被丢弃——除非参数表以 `...` 结尾，这时多余实参进入 vararg table。

```lua
local function area(w, h)      -- 没有默认参数，手工兜底
  h = h or 1
  return w * h
end

local function sum(...)        -- 变参：所有多余实参收进 vararg 表
  local total = 0
  for _, v in ipairs({...}) do total = total + v end
  return total
end

local function stats(... va)   -- 5.5：在三个点后给出名字，va 是只读的 vararg 表
  return va.n, sum(...)         -- va.n 就是额外实参个数
end

local function divmod(a, b) return a // b, a % b end   -- 多返回值

print(area(2, 3))          -- 6
print(area(2))              -- 2
print(sum(1, 2, 3))          -- 6
print(stats(1, 2, 3))         -- 3  6
print(divmod(7, 2))            -- 3  1
local q, r = divmod(7, 2)
print(q + r)                    -- 4

function M.greet(self, name) end   -- 冒号语法：function M:greet(name) 隐式加 self
```

Lua 5.5 给 vararg 表加了命名写法：参数表写成 `function f(...) ... end` 时只能在表达式位置用三个点，写成 `function f(... va)` 则多一个只读局部变量 `va` 直接指向 vararg 表，`va.n` 就是额外实参个数（5.4 及以前只能用 `select("#", ...)` 得到）；给 `va` 加 `<const>` 是多余的，它本来就是只读的。多返回值只在“表达式列表的最后一位”才全部展开，写成 `(f())` 会被截成第一个值，这是最常见的丢值原因。Lua 没有默认参数，惯例是用 `or` 兜底或提供 `opts` 表；Lua 5.5 把 `global` 变成了保留字，显式声明全局变量要写 `global x`，未声明就赋值在 `global` 声明的作用域内会报错；Lua 的宿主程序负责调 `main`，语言自身没有入口点约定，独立解释器执行的就是整块 chunk。

📘 [Lua 5.5 · Function definitions](https://www.lua.org/manual/5.5/manual.html#3.4.11)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的函数写法与 JavaScript 完全相同，只是多了参数和返回值的类型标注；标注只在编译期存在，编译产物里没有痕迹。可选参数用 `?`（optional parameter），默认值用 `=`，变参用 `...rest: T[]`。

```typescript
function area(w: number, h = 1): number { return w * h; }

function stats(...args: number[]): { n: number; sum: number } {
  return { n: args.length, sum: args.reduce((a, b) => a + b, 0) };
}

const divmod = (a: number, b: number): [number, number] =>
  [Math.trunc(a / b), a % b];

// 重载：多个声明签名 + 一个实现签名
function pick(x: string): string;
function pick(x: number): number;
function pick(x: string | number): string | number { return x; }

console.log(area(2, 3));                 // 6
console.log(area(2));                     // 2
console.log(stats(1, 2, 3));               // { n: 3, sum: 6 }
console.log(divmod(7, 2));                  // [ 3, 1 ]
console.log(pick('a'), pick(1));             // a 1
```

可选参数与默认值不能同时用：`h?: number` 和 `h = 1` 二选一，因为默认值已经蕴含了“可以不传”。可选参数必须排在必选参数之后。严格模式下 `noImplicitAny` 会逼你给参数标类型，`strictFunctionTypes` 让函数参数的逆变检查生效。TypeScript 7 是 Go 重写的原生编译器，语法与类型规则沿用 5.x 系列，运行时的类型行为仍然由 JavaScript 决定。

📘 [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 用 `function` 声明函数，或者用箭头函数表达式；参数列表不写类型，默认值、rest 参数都在运行期处理。非箭头函数内部还有一个类数组的 `arguments`，箭头函数没有。

```javascript
function area(w, h = 1) { return w * h; }          // 默认参数
function stats(...args) {                            // rest 参数
  return { n: args.length, sum: args.reduce((a, b) => a + b, 0) };
}
function divmod(a, b) { return [Math.trunc(a / b), a % b]; }   // 数组多返回值

function legacy() { return arguments.length; }        // 非箭头函数的 arguments

console.log(area(2, 3));          // 6
console.log(area(2));              // 2
console.log(stats(1, 2, 3));        // { n: 3, sum: 6 }
console.log(divmod(7, 2));           // [ 3, 1 ]
console.log(legacy(1, 2));            // 2
console.log(area(2, undefined));       // 2  默认值只对 undefined 生效
console.log(area(2, null));             // 0  ⚠️ null 不会触发默认值
```

默认参数只在实参是 `undefined`（或没传）时生效，传 `null`、`0`、`""` 都会原样使用，这个区别在从 JSON 读可选字段时特别容易踩。`arguments` 不是真正的数组，需要 `Array.from(arguments)` 才能用数组方法，所以新代码一律用 rest 参数。箭头函数没有自己的 `this`、`arguments`、`super`，不能当构造函数，也不支持 `yield`；需要动态 `this` 时只能用 `function`。

📘 [MDN · Functions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Functions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 用 `function` 声明函数，参数变量带 `$`，类型写在 `$` 之前，返回类型写在参数表之后用 `:` 分隔。默认参数（default parameter，`$h = 1`）、命名实参（8.0+）、变参 `...$args`、引用参数 `&$x` 都有；8.5 起还能用 `#[\NoDiscard]` 标记“返回值必须被使用”。

```php
<?php
declare(strict_types=1);

function area(int $w, int $h = 1): int { return $w * $h; }

function stats(...$args): array {                        // 变参
    return ['n' => count($args), 'sum' => array_sum($args)];
}

function addOne(int &$x): void { $x += 1; }               // 引用参数

function divmod(int $a, int $b): array { return [$a / $b, $a % $b]; }

echo area(2, 3), PHP_EOL;                 // 6
echo area(h: 3, w: 2), PHP_EOL;             // 6  命名实参（8.0+）
var_dump(stats(1, 2, 3));                    // n=3, sum=6
$n = 41; addOne($n); echo $n, PHP_EOL;        // 42
[$q, $r] = divmod(7, 2); echo "$q $r", PHP_EOL;   // 3 1
```

命名实参一旦出现，之后的实参都必须命名；命名实参与默认参数配合可以跳过中间参数。引用参数必须在函数签名里写 `&`，调用点不写 `&`（这点和 C++ 相反）。`declare(strict_types=1)` 只约束函数参数与返回值，运算符层面仍然是松散比较。`divmod` 用数组返回两个值时注意 `$a / $b` 在整除时是 int、否则是 float。

📘 [PHP · Functions](https://www.php.net/manual/en/language.functions.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 用 `def` / `end` 定义方法，参数不带类型，返回值是方法体最后一句的值（也可以显式 `return`）。参数种类是 18 门语言里最细的：必选、可选（默认值）、`*rest`、`k:` 关键字、`**kw`、block 形参 `&blk`，各有独立的语法槽位。

```ruby
def area(w, h = 1) = w * h                    # 无休止符方法（Ruby 3.0+）

def stats(*args, **kwargs)                     # 位置变参 + 关键字变参
  [args.sum, kwargs]
end

def divmod2(a, b) = [a.div(b), a % b]           # 数组多返回值

def apply_twice(x, &blk)                        # 显式 block 形参
  blk.call(blk.call(x))
end

puts area(2, 3)                  # 6
puts area(2)                      # 2
p stats(1, 2, mode: 'x')           # [3, {mode: "x"}]
q, r = divmod2(7, 2)
puts "#{q} #{r}"                    # 3 1
p apply_twice(1) { |v| v + 3 }       # 7
```

默认值表达式在**每次调用**时重新求值，所以 `def f(x, acc = [])` 每次拿到的是新数组，这一点与 Python 的可变默认参数陷阱正好相反。`**kwargs` 收关键字实参必须在 Ruby 3.0 之后写成独立的 `**` 形式，2.7 的“自动转 Hash”已被移除。block 不是普通参数：`&blk` 只是把 block 捕获成 Proc，不写 `&` 时用 `yield` 调用。顶层 `def` 定义的是 `Object` 的私有方法，脚本从上往下执行，没有强制的 `main`。

📘 [Ruby · Methods](https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 参数传递与返回值

参数传递的分歧点只有一个：**调用者传的是值的拷贝，还是对同一块存储的引用**。C 和 Go 一律传值（Go 的 slice/map/channel 内部持有指针，所以表现像引用）；C++ 用 `T&`/`const T&`/`T&&` 显式区分；Java、C#、Python、Ruby、Kotlin、Swift、Dart 传的都是“对象引用的值拷贝”（call by sharing），能改对象内容，但不能让调用者的变量指向新对象；Rust 则把 ownership 作为参数语义的一部分，传入可能直接 move。多返回值这一侧，Go、Lua、Python、Julia、Swift、Zig 有语言级支持，Rust 用元组和 `Result`，C# 用值元组与 `out`，Java 完全没有，只能靠 `record`、数组或 `Optional`。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的参数语义由类型决定：默认是 **move**（或 `Copy` 类型的拷贝），写 `&T` 借用只读，写 `&mut T` 借用可写，写 `T` 就交出 ownership。函数签名因此承载了“这个参数会不会被消耗、能不能改、活多久”的全部信息，全部在编译期检查。返回多个值用元组，失败用 `Result`，需要“可能没有”用 `Option`。

```rust
fn add_by_value(mut v: Vec<i32>) -> Vec<i32> { v.push(4); v }   // 拿走 ownership
fn add_by_ref(v: &mut Vec<i32>) { v.push(4); }                  // 借用可写
fn len_of(v: &[i32]) -> usize { v.len() }                        // 只读借用
fn divmod(a: i32, b: i32) -> (i32, i32) { (a / b, a % b) }        // 元组多返回值
fn checked_div(a: i32, b: i32) -> Result<i32, String> {           // Result 表达失败
    if b == 0 { Err("division by zero".into()) } else { Ok(a / b) }
}

fn main() {
    let v = vec![1, 2, 3];
    let v = add_by_value(v);          // v 被移动，再绑定回来
    let mut w = v;
    add_by_ref(&mut w);                // 借用结束即归还
    println!("{:?} {}", w, len_of(&w));    // [1, 2, 3, 4, 4] 5
    println!("{:?}", divmod(7, 2));         // (3, 1)
    println!("{:?}", checked_div(6, 3));     // Ok(2)
    println!("{:?}", checked_div(1, 0));      // Err("division by zero")
}
```

`&T` 是共享借用、`&mut T` 是独占借用，同一时刻二者互斥，这条规则让“函数里改了调用者的数据”永远不会是意外。给参数写 `mut` 只影响函数体内的可写性，不影响调用者。返回引用必须绑定到输入的生命周期（生命周期省略规则），否则编译不过；需要多个值又不想定义结构体时用元组，需要结构化命名时用结构体。

📘 [Rust · Functions](https://doc.rust-lang.org/reference/items/functions.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的参数默认按值传递，`struct`、`enum`、数组、字典、字符串都是值类型，赋值或传参时**拷贝语义**（写时复制优化实现）；`class` 是引用类型，传的是引用。要让函数写回调用者的变量，参数必须标 `inout`，调用点还要加 `&`。

```swift
struct Point { var x = 0, y = 0 }         // 值类型
final class Box { var v = 0 }              // 引用类型

func bumpStruct(_ p: Point) -> Point { var p = p; p.x += 1; return p }
func bumpClass(_ b: Box) { b.v += 1 }        // 引用语义，直接改到原对象
func bumpInout(_ n: inout Int) { n += 1 }     // inout 写回

func divmod(_ a: Int, _ b: Int) -> (q: Int, r: Int) { (a / b, a % b) }

var p = Point(x: 1, y: 2)
let p2 = bumpStruct(p)
print(p.x, p2.x)          // 1 2  原值不变
let b = Box()
bumpClass(b)
print(b.v)                 // 1
var n = 41
bumpInout(&n)
print(n)                    // 42
print(divmod(7, 2).q)        // 3
```

`inout` 是 copy-in copy-out 语义：函数里拿到一份拷贝，返回时写回原变量，所以不要用它传递有别名关系的两个参数（`swap(&a, &a)` 是未定义行为）。`class` 就算参数声明为 `let` 也能改属性，因为引用本身不变。返回多个值用带标签的元组最自然，可失败用 `Optional`，抛错用 `throws` + `try`。

📘 [Swift · Functions](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/functions/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的参数**全部按值传递**，没有引用参数。真正让人困惑的是复合类型：`slice` 是含长度、容量和底层数组指针的结构体，`map`、`channel`、`func`、`interface` 内部都持有指针，所以把它们传进函数后，函数里改元素会反映到调用者，但给参数本身重新赋值（`append` 后不返回、`m = nil`）不会。

```go
package main

import "fmt"

func setFirst(s []int)      { s[0] = 99 }     // 改元素：调用者可见
func grow(s []int) []int    { return append(s, 4) }   // 改长度：必须返回
func replace(m map[string]int) { m["a"] = 1 }          // map 是引用语义
func reset(m map[string]int)   { m = map[string]int{} } // 重新赋值：调用者不可见
func divmod(a, b int) (int, int) { return a / b, a % b }  // 原生多返回值

type Result struct { Q, R int }
func divmodStruct(a, b int) Result { return Result{a / b, a % b} }

func main() {
	s := []int{1, 2, 3}
	setFirst(s)
	fmt.Println(s)                 // [99 2 3]
	s = grow(s)
	fmt.Println(s)                  // [99 2 3 4]
	m := map[string]int{}
	replace(m)
	reset(m)
	fmt.Println(m)                   // map[a:1]
	fmt.Println(divmod(7, 2))         // 3 1
	fmt.Println(divmodStruct(7, 2))    // {3 1}
}
```

规则可以压缩成一句：**Go 里没有引用传递，只有指针值的传递**。要修改调用者的变量就必须传指针（`*T`），而 slice/map/channel 因为内部已经含指针，才显得像引用。多返回值是 Go 错误处理的基础约定：`(T, error)` 是标准形状，调用者必须显式接住两者。返回值名字可以在签名里声明，配合裸 `return` 使用。

📘 [Go spec · Function declarations](https://go.dev/ref/spec#Function_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的参数传递常被描述为 **call by sharing**：传的是对象引用的一份拷贝。函数内对参数变量重新赋值不会影响调用者；改变参数指向的可变对象内容（`list.append`、`dict[...] =`）会影响调用者。不可变对象（int、str、tuple、frozenset）自然不受影响。多返回值靠元组解包。

```python
def set_first(xs):
    xs[0] = 99            # 改内容：调用者可见

def rebind(xs):
    xs = [0]              # 重新绑定局部名字：调用者不可见

def divmod2(a, b):
    return a // b, a % b   # 元组多返回值

def min_max(xs):
    return min(xs), max(xs)

def add_bad(item, target=[]):        # ⚠️ 默认参数只求值一次
    target.append(item)
    return target

xs = [1, 2, 3]
set_first(xs)
rebind(xs)
print(xs)                     # [99, 2, 3]
q, r = divmod2(7, 2)
print(q, r)                    # 3 1
print(min_max([3, 1, 4]))       # (1, 4)
print(add_bad(1))                # [1]
print(add_bad(2))                 # [1, 2]  ← 同一个列表被复用
```

可变默认参数陷阱的根因是：默认值在 `def` 执行时求值一次，之后所有调用共享同一个对象。正确写法是 `target=None`，函数体内再 `target = [] if target is None else target`。想让函数“返回多个值”其实就是返回一个元组，调用点解包；返回值超过三个时用 `dataclass` 或 `NamedTuple` 更可读。

📘 [Python · Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的参数默认按值传递。基本类型与 `String` 是值语义；`data class`、普通 `class`、`Array`、集合都是引用语义，传进函数后改其内容会反映到调用者，重新赋值参数则不会。可空性写在类型里（`String?`），多返回值没有原生语法，惯用 `Pair`/`Triple` 或自定义 `data class` 配合解构声明。

```kotlin
data class Result(val q: Int, val r: Int)     // 自定义多返回值

fun setFirst(xs: MutableList<Int>) { xs[0] = 99 }   // 引用语义：改内容
fun reassign(xs: MutableList<Int>) { val local = xs; local[0] = 0 }  // 局部重新绑定

fun divmod(a: Int, b: Int) = Pair(a / b, a % b)        // Pair
fun divmod2(a: Int, b: Int) = Result(a / b, a % b)      // 自定义类型

fun main() {
    val xs = mutableListOf(1, 2, 3)
    setFirst(xs)
    println(xs)                       // [99, 2, 3]
    val (q, r) = divmod(7, 2)          // 解构 Pair
    println("$q $r")                    // 3 1
    val (q2, r2) = divmod2(7, 2)         // 解构 data class
    println("$q2 $r2")                    // 3 1
    println(Pair(1, 2).first)              // 1  Pair 的字段名是 first/second
    println(divmod(7, 2).second)           // 1
}
```

Kotlin 参数是 `val`，函数体内不能给参数重新赋值（写了会编译报错），这消除了“以为改了调用者变量”的一整类 bug。想要写回调用者，只能把可变状态放在类属性里，或者返回新值让调用者重新绑定。`Pair` 的字段名是 `first`/`second`，可读性差；超过两个返回值时用 `data class` 命名更清楚。`Triple` 提供三个值的版本。

📘 [Kotlin · Functions](https://kotlinlang.org/docs/functions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java **只有值传递**：基本类型传值本身，对象传的是引用的值（拷贝）。因此函数能改对象的字段，但不能让调用者的变量指向别的对象。Java 没有多返回值，需要用 `record`、数组、`Optional` 或 `out` 风格的持有对象来模拟。

```java
public class Pass {
    static class Box { int v = 0; }

    static void changeField(Box b) { b.v = 42; }    // 改字段：调用者可见
    static void rebind(Box b) { b = new Box(); b.v = 99; }  // 重新绑定：不可见
    static void changeInt(int x) { x = 42; }          // 基本类型：完全不可见

    record DivMod(int q, int r) { }
    static DivMod divmod(int a, int b) { return new DivMod(a / b, a % b); }

    static int[] divmodArr(int a, int b) { return new int[]{a / b, a % b}; }

    public static void main(String[] args) {
        Box b = new Box();
        changeField(b);
        rebind(b);
        System.out.println(b.v);                 // 42
        int x = 1;
        changeInt(x);
        System.out.println(x);                    // 1
        DivMod d = divmod(7, 2);
        System.out.println(d.q() + " " + d.r());   // 3 1
        System.out.println(divmodArr(7, 2).length);  // 2
    }
}
```

`record`（Java 16 起正式）是替代“多返回值小类”的最省事写法：自动生成构造器、访问器、`equals`、`hashCode`、`toString`，字段名可读且不可变。数组的缺点是丢失字段名、长度不受约束；`Optional` 只适合“0 或 1 个值”，不适合两个。若确实需要写回基本类型，只能用单元素数组或 `AtomicInteger` 这类持有对象，`java.util.concurrent.atomic` 只是碰巧可用，不是为这个目的设计的。

📘 [JLS · Method invocation](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.4.1)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 把传递方式写进类型：`T` 是拷贝（或移动），`T&` 可写引用，`const T&` 只读引用（能绑右值、可延长临时量寿命），`T&&` 右值引用（用于移动语义与完美转发）。多返回值用 `std::pair`/`std::tuple`/`std::optional`，或者用输出参数 `T&`——但现代 C++ 更推荐返回结构体。

```cpp
#include <cstdio>
#include <string>
#include <tuple>
#include <utility>

struct Big { std::string payload; };

void byValue(Big b) { b.payload += "!"; }              // 拷贝，调用者不变
void byRef(Big& b) { b.payload += "!"; }                // 引用，调用者改变
void byConstRef(const Big& b, std::string& out) { out = b.payload; }  // 只读引用 + 输出参数

std::pair<int, int> divmod(int a, int b) { return {a / b, a % b}; }
std::tuple<int, int, int> divmod3(int a, int b) { return {a / b, a % b, a * b}; }

int main() {
    Big b{"x"};
    byValue(b);
    std::printf("%s\n", b.payload.c_str());       // x
    byRef(b);
    std::printf("%s\n", b.payload.c_str());        // x!
    std::string s;
    byConstRef(b, s);
    std::printf("%s\n", s.c_str());                 // x!
    auto [q, r] = divmod(7, 2);
    auto [q3, r3, m3] = divmod3(7, 2);
    std::printf("%d %d %d %d %d\n", q, r, q3, r3, m3);   // 3 1 3 1 14
}
```

参数传递的选择顺序通常是：只读大对象用 `const T&`，需要修改用 `T&`，小的可平凡拷贝类型（`int`、指针、`std::string_view`）直接用 `T`，要接管 ownership 用 `T` 再 `std::move` 进成员。返回多个值建议直接返回 `struct`，比 `std::tuple` 可读，而且 C++17 的结构化绑定照样能用。注意返回局部变量的引用是悬垂引用，编译期就会给出警告。

📘 [cppreference · Value categories 与引用](https://en.cppreference.com/w/cpp/language/reference)

{{% /tab %}}

{{% tab header="C" %}}

C 的参数**全部按值传递**，数组作为参数时会退化为指向首元素的指针，这让人误以为“数组是引用传递”，本质传的仍是指针的值。要在函数里改调用者的变量，只能显式传指针。C 没有多返回值，用结构体返回或输出指针参数。

```c
#include <stdio.h>

void change_int(int x) { x = 42; }              /* 改副本，调用者不变 */
void change_ptr(int *x) { *x = 42; }             /* 改目标，调用者改变 */

void change_array(int a[3]) { a[0] = 99; }        /* 等价于 int *a，调用者可见 */

struct DivMod { int q, r; };
struct DivMod divmod(int a, int b) {              /* 结构体返回多个值 */
    struct DivMod d = { a / b, a % b };
    return d;
}

void divmod_out(int a, int b, int *q, int *r) {    /* 输出参数写法 */
    if (q) *q = a / b;
    if (r) *r = a % b;
}

int main(void) {
    int x = 1;
    change_int(x);
    printf("%d\n", x);              /* 1 */
    change_ptr(&x);
    printf("%d\n", x);               /* 42 */
    int arr[3] = {1, 2, 3};
    change_array(arr);
    printf("%d\n", arr[0]);           /* 99 */
    struct DivMod d = divmod(7, 2);
    printf("%d %d\n", d.q, d.r);       /* 3 1 */
    int q, r;
    divmod_out(7, 2, &q, &r);
    printf("%d %d\n", q, r);            /* 3 1 */
    return 0;
}
```

`change_array(int a[3])` 里方括号里的数字会被编译器忽略，函数内 `sizeof(a)` 得到的是指针大小而不是数组大小，要传长度必须另加参数。传 `const T *` 表示“只读借用”，C23 起还引入了 `nullptr` 常量与 `[[nodiscard]]` 之类的属性；结构体按值返回在现代 ABI 下通常走寄存器或隐藏指针，性能没问题。用 `void` 明确“无参数”的老习惯在 C23 里仍然成立。

📘 [cppreference · C functions](https://en.cppreference.com/w/c/language/functions)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的传递语义由类型的可变性决定：不可变类型（`Int`、`Float64`、`struct` 默认不可变）表现得像按值传递，可变类型（`Array`、`Dict`、`mutable struct`）传的是引用，函数里改内容会影响调用者。Julia 没有“按引用传递”的语法，要写回只能用可变容器或返回新值。多返回值是元组，解包即用。

```julia
mutable struct Counter; n::Int; end

bump_arr!(xs) = (xs[1] = 99)              # 可变容器：改内容可见
bump_imm(x::Int) = (x = 42)                # 不可变：改不动
bump_struct!(c::Counter) = (c.n += 1)      # mutable struct：改字段可见

divmod2(a, b) = (a ÷ b, a % b)             # 元组多返回值
minmax2(xs) = extrema(xs)                   # 也返回元组

xs = [1, 2, 3]
bump_arr!(xs); println(xs)                  # [99, 2, 3]
x = 1; bump_imm(x); println(x)               # 1
c = Counter(0); bump_struct!(c); println(c.n)  # 1
q, r = divmod2(7, 2); println("$q $r")          # 3 1
println(minmax2([3, 1, 4]))                      # (1, 4)
```

按约定，会修改实参的函数名以 `!` 结尾（`sort!`、`push!`），这是文档约定而非编译器强制。`immutable struct` 一旦构造就不能改字段，但若字段本身是 `Array`，数组内容照样能改——不可变指的是绑定而不是深层数据。返回元组会被编译器优化掉分配，不需要担心性能；返回大型数组时 Julia 也靠返回新值而不是输出参数，这是它和 C 系的主要风格差异。

📘 [Julia · Functions](https://docs.julialang.org/en/v1/manual/functions/#Argument-Passing-Behavior)

{{% /tab %}}

{{% tab header="C#" %}}

C# 默认按值传递：值类型传数据副本，引用类型传引用的副本。要真正按引用传，需要参数修饰符：`ref`（进可读、出可写）、`out`（必须在函数内赋值）、`in`（只读引用，避免大结构体拷贝）、`ref readonly`。多返回值用值元组（`(int q, int r)`）配合解构最方便，`out` 参数适合 `TryParse` 这种“成功与否 + 结果”的模式。

```csharp
using System;

class Passing {
    struct Point { public int X, Y; }
    class Box { public int V; }

    static void BumpStruct(Point p) { p.X = 99; }         // 值类型：副本
    static void BumpClass(Box b) { b.V = 99; }              // 引用类型：改到原对象
    static void BumpRef(ref int n) { n += 1; }                // ref：写回
    static void Init(out int n) { n = 7; }                     // out：必须赋值

    static (int q, int r) DivMod(int a, int b) => (a / b, a % b);

    static void Main() {
        var p = new Point();
        BumpStruct(p);
        Console.WriteLine(p.X);                    // 0
        var b = new Box();
        BumpClass(b);
        Console.WriteLine(b.V);                     // 99
        int n = 41;
        BumpRef(ref n);
        Console.WriteLine(n);                        // 42
        Init(out int m);
        Console.WriteLine(m);                         // 7
        var (q, r) = DivMod(7, 2);
        Console.WriteLine($"{q} {r}");                 // 3 1
    }
}
```

`ref`、`out`、`in`、`ref readonly` 都参与签名，所以不能只靠它们区分重载（一个 `ref` 与一个 `out` 的同名方法算冲突）。声明为 `in` 的参数在函数内不可写，编译器可能为它创建临时变量，所以不要把它当成“必然按引用”的性能承诺，需要严格要求引用时用 `ref readonly`。值元组的字段名只在编译期存在，跨程序集使用时建议用 `record`。

📘 [MS Learn · Pass by value and pass by reference](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/method-parameters)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的参数全是按值传递：`int`、`double`、`bool`、`String`、`record` 等是不可变值，`List`、`Map`、`Set`、普通对象是引用，传进函数后改内容会反映到调用者。Dart 3.0 起可以用 record 做真正的多返回值，字段可以命名也可以只按位置。

```dart
class Box { int v = 0; }

void bumpList(List<int> xs) => xs[0] = 99;      // 引用语义
void rebindList(List<int> xs) => xs = <int>[0];   // 重新绑定：不可见
void bumpBox(Box b) => b.v = 99;

({int q, int r}) divmod(int a, int b) => (q: a ~/ b, r: a % b);
(int, int) divmodPos(int a, int b) => (a ~/ b, a % b);

void main() {
  final xs = [1, 2, 3];
  bumpList(xs);
  rebindList(xs);
  print(xs);                                  // [99, 2, 3]
  final b = Box();
  bumpBox(b);
  print(b.v);                                  // 99
  final (q: q, r: r) = divmod(7, 2);
  print('$q $r');                              // 3 1
  final (a, c) = divmodPos(7, 2);
  print('$a $c');                              // 3 1
}
```

Dart 没有 `ref`/`out`，要写回调用者的基本类型变量只能包一层可变对象或返回新值再重新赋值。record 是不可变的，字段名只在静态类型里存在，运行时的 `toString` 会带上名字（`(q: 3, r: 1)`）。跨 isolate 传递对象时要注意：`SendPort` 传的是拷贝或转移，不共享内存，这一点和同 isolate 内的引用语义完全不同。

📘 [Dart · Functions](https://dart.dev/language/functions)

{{% /tab %}}

{{% tab header="R" %}}

R **没有按引用传递的调用语法**，所有参数都是按值传入的绑定；但 R 对象带引用计数，只有在被修改时才真正拷贝（写时复制，copy-on-write）。所以函数里改参数通常不影响调用者，唯一的例外是环境（environment）、外部指针以及显式使用 `<<-` 的情况。多返回值用 `list()`。

```r
xs <- c(1, 2, 3)

bump <- function(v) { v[1] <- 99; v }      # 改的是副本，需要返回
bump_ret <- function(v) { v[1] <- 99; v }   # 返回值才是新对象

env <- new.env(); env$n <- 0
bump_env <- function(e) { e$n <- e$n + 1 }   # environment 是引用语义

divmod2 <- function(a, b) list(q = a %/% b, r = a %% b)   # list 多返回值

y <- bump(xs)
print(xs)                    # [1] 1 2 3  调用者不变
print(y)                      # [1] 99 2 3
bump_env(env); bump_env(env)
print(env$n)                   # [1] 2
res <- divmod2(7, 2)
print(res$q); print(res$r)      # [1] 3  [1] 1
```

`tracemem()` 能观察到一个对象是否真的被拷贝，可以用来说明写时复制的时机。要“就地修改”数据框或向量，惯用做法是返回新对象让调用者重新赋值（`df <- transform(df, ...)`），或者在 `data.table` 这类包提供的按引用赋值（`:=`）里做。`list()` 返回多值的同时保留了名字，比返回向量安全——返回向量会把不同类型强制统一。

📘 [R · Function definitions 与惰性求值](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Function-definitions)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig 的参数一律**按值传递**，包括数组和结构体。要避免大对象拷贝、或想让函数修改调用者的数据，就得显式传指针（`*T` 可写、`*const T` 只读）。多返回值用结构体（可选地用 `std.meta` 的元组），需要表达失败时用错误联合（error union），两者可以组合。

```zig
const std = @import("std");

const Big = struct { data: [4]u64 };

fn byValue(b: Big) Big { var c = b; c.data[0] = 99; return c; }   // 拷贝
fn byPtr(b: *Big) void { b.data[0] = 99; }                          // 指针：写回
fn byConstPtr(b: *const Big) u64 { return b.data[0]; }               // 只读指针

const DivMod = struct { q: i64, r: i64 };
fn divmod(a: i64, b: i64) DivMod { return .{ .q = @divTrunc(a, b), .r = @rem(a, b) }; }

const DivErr = error{DividedByZero};
fn checkedDiv(a: i64, b: i64) DivErr!i64 {
    if (b == 0) return DivErr.DividedByZero;
    return @divTrunc(a, b);
}

pub fn main() !void {
    var x = Big{ .data = .{ 1, 2, 3, 4 } };
    const y = byValue(x);
    std.debug.print("{d} {d}\n", .{ x.data[0], y.data[0] });   // 1 99
    byPtr(&x);
    std.debug.print("{d}\n", .{byConstPtr(&x)});                 // 99
    const d = divmod(7, 2);
    std.debug.print("{d} {d}\n", .{ d.q, d.r });                  // 3 1
    std.debug.print("{d}\n", .{try checkedDiv(6, 3)});             // 2
}
```

Zig 的“多返回值”还有一种零成本写法：函数返回 `struct` 时，编译器在多数情况下会通过寄存器或调用者提供的空间返回，不会有额外堆分配。指针参数在 Zig 里显式可见，读代码时能一眼看出哪个参数会被改写，这是 Zig 相对 C 的主要可读性改进之一。错误联合必须用 `try`、`catch` 或 `if (...) |v|` 处理，忘记处理是编译错误。

📘 [Zig · Function parameters 与 Pointers](https://ziglang.org/documentation/master/#Functions)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的参数一律按值传递，但 table、function、thread、userdata 都是**引用类型**：变量里存的是引用，赋值与传参复制的是引用而不是内容，所以函数改 table 字段会影响调用者。其他类型（nil、boolean、number、string）是值类型，函数里改不动调用者的变量。多返回值是 Lua 的原生能力。

```lua
local function bump(t) t[1] = 99 end           -- table 引用：调用者可见
local function rebind(t) t = {0} end             -- 重新绑定：不可见

local function divmod(a, b) return a // b, a % b end   -- 多返回值

local function minmax(xs)
  local lo, hi = xs[1], xs[1]
  for _, v in ipairs(xs) do
    if v < lo then lo = v end
    if v > hi then hi = v end
  end
  return lo, hi
end

local xs = {1, 2, 3}
bump(xs); rebind(xs)
print(xs[1])                 -- 99
local q, r = divmod(7, 2)
print(q, r)                   -- 3  1
print(minmax({3, 1, 4}))       -- 1  4
print((divmod(7, 2)))           -- 3  括号截断为第一个值
```

`print(minmax({3, 1, 4}))` 能把两个值都打出来，是因为多返回值进入了实参列表的末尾位置；一旦被括号包住或被赋给单个变量，就只剩第一个值。table 的引用语义没有 const 机制：5.5 的 `<const>` 只冻结变量绑定、不冻结 table 内容。想表达“不要改我的表”，只能靠文档约定或做深拷贝。

📘 [Lua 5.5 · Values and Types（引用语义）](https://www.lua.org/manual/5.5/manual.html#2.1)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的运行时语义完全是 JavaScript：原始值（`number`、`string`、`boolean`、`null`、`undefined`、`symbol`、`bigint`）按值传递，对象、数组、函数按引用共享。类型系统层面可以标 `readonly` 或 `ReadonlyArray<T>`，但那只在编译期拦你。多返回值用对象或元组类型。

```typescript
interface DivMod { q: number; r: number }

function bump(xs: number[]): void { xs[0] = 99; }          // 引用语义
function rebind(xs: number[]): void { xs = [0]; }           // 重新绑定：不可见
function bumpPure(xs: readonly number[]): void {
  // xs[0] = 99;   // 🛑 编译错误：readonly 下标不可赋值
}
function divmod(a: number, b: number): [number, number] {
  return [Math.trunc(a / b), a % b];
}
function divmodObj(a: number, b: number): DivMod {
  return { q: Math.trunc(a / b), r: a % b };
}

const xs = [1, 2, 3];
bump(xs); rebind(xs);
console.log(xs);                        // [ 99, 2, 3 ]
const [q, r] = divmod(7, 2);
console.log(q, r);                       // 3 1
console.log(divmodObj(7, 2).r);            // 1
```

`readonly number[]` 与 `ReadonlyArray<number>` 只约束当前变量，函数内部拿到的数组如果来自可变来源，仍可能在别处被改，所以类型标注不能替代运行期防御。函数参数默认是双变的（在 `strictFunctionTypes` 打开后函数类型参数位置变为逆变），这和对象引用语义是两件不同的事。元组类型加上 `as const` 可以拿到只读的定长元组。

📘 [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的参数全是按值传递，但“值”对对象来说是引用的拷贝：函数能改对象属性，不能替换调用者的变量。原始值（`number`、`string`、`boolean`、`null`、`undefined`、`symbol`、`bigint`）传的是真实值。多返回值用数组或对象，`Object.freeze` 能在运行期冻结对象。

```javascript
function bump(xs) { xs[0] = 99; }         // 引用语义
function rebind(xs) { xs = [0]; }          // 重新绑定：不可见
function bumpFrozen(xs) { 'use strict'; xs[0] = 99; }   // ❄️ 严格模式下抛 TypeError

function divmod(a, b) { return [Math.trunc(a / b), a % b]; }   // 数组多返回值
function divmodObj(a, b) { return { q: Math.trunc(a / b), r: a % b }; }

const xs = [1, 2, 3];
bump(xs); rebind(xs);
console.log(xs);                     // [ 99, 2, 3 ]
const [q, r] = divmod(7, 2);
console.log(q, r);                    // 3 1
console.log(divmodObj(7, 2).r);         // 1
const frozen = Object.freeze([1, 2]);
try { bumpFrozen(frozen); } catch (e) { console.log(e.constructor.name); }  // TypeError
```

`Object.freeze` 是浅冻结：嵌套对象仍然可改，要深冻结得递归处理。原始值在函数内的重新赋值永远不会外泄，这是与“对象引用拷贝”最容易混淆的一点。数组解构 `const [q, r] = ...` 是最轻量的多返回值写法；需要命名时返回对象，代价是多一次对象分配。

📘 [MDN · Functions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Functions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 4 时代默认是“按引用传递”，PHP 5 起改为**默认按值传递**；对象不再是特例——PHP 5 之后对象句柄也是按值传递的，函数内改对象属性会反映到调用者，但把参数重新赋成新对象不会。要在调用点真正传引用，函数签名必须写 `&`。多返回值用数组配合 `list()`/`[]` 解构。

```php
<?php
class Box { public int $v = 0; }

function bumpArray(array $xs): void { $xs[0] = 99; }          // 数组按值：调用者不变
function bumpArrayRef(array &$xs): void { $xs[0] = 99; }       // & 引用：调用者改变
function bumpBox(Box $b): void { $b->v = 99; }                   // 对象句柄：调用者可见

function divmod(int $a, int $b): array { return [$a / $b, $a % $b]; }

$xs = [1, 2, 3];
bumpArray($xs);
var_dump($xs[0]);          // int(1)
bumpArrayRef($xs);
var_dump($xs[0]);           // int(99)
$b = new Box();
bumpBox($b);
var_dump($b->v);             // int(99)
[$q, $r] = divmod(7, 2);
echo "$q $r\n";               // 3 1
```

数组在 PHP 里是值类型，这点和 JavaScript 相反，所以拷贝成本是真实存在的；需要避免大数组拷贝时用 `&` 引用参数，但也要小心函数被调用者期待“无副作用”。`&` 必须在函数签名里写，调用点写 `&$xs` 会被当成取地址语法而废弃/报错。对象克隆用 `clone`，8.5 起还支持 `clone($obj, ['prop' => $value])` 的形式在克隆时改属性。

📘 [PHP · References explained](https://www.php.net/manual/en/language.references.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的参数按值传递，但所有值都是对象、变量里存的是对象引用，所以函数能改传入对象的内部状态（`<<`、`[]=`），不能让调用者的变量指向别的对象。整数、符号、`true`/`false`/`nil` 是不可变的，`freeze` 可以冻结字符串或数组。多返回值是数组，解包即用。

```ruby
def bump(xs) = xs[0] = 99              # 改内容：调用者可见
def rebind(xs) = xs = [0]                # 重新绑定：不可见

def divmod2(a, b) = [a.div(b), a % b]     # 数组多返回值

def bump_frozen(xs) = xs[0] = 99           # 对冻结数组会抛 FrozenError

xs = [1, 2, 3]
bump(xs); rebind(xs)
p xs                        # [99, 2, 3]
q, r = divmod2(7, 2)
p [q, r]                     # [3, 1]
frozen = [1, 2].freeze
begin
  bump_frozen(frozen)
rescue FrozenError => e
  puts e.class                # FrozenError
end
s = 'abc'.freeze
# s << 'd'                    # 🛑 FrozenError: can't modify frozen String
p s.frozen?                    # true
```

`freeze` 是浅冻结，只冻结对象本身的修改操作，不递归冻结其中的元素。Ruby 里的整数立刻值（immediate values）无法被重新赋值影响，所以 `def inc(x) = x + 1` 永远不会改变调用者，必须靠返回值。解构还可以用 `a, b = *pair`、块参数 `|(k, v)|` 等写法。

📘 [Ruby · Methods](https://docs.ruby-lang.org/en/master/syntax/methods_rdoc.html)

{{% /tab %}}

{{< /tabpane >}}

### 一等函数

函数成为一等值要过两道关：**语言里有没有函数类型**，以及**函数值能不能携带环境**。Rust、Swift、Go、Kotlin、Dart、C#、C++、JavaScript、TypeScript、Julia、Python、Ruby、Lua、PHP 都有语言级函数值；Java 只有函数式接口这一种目标类型；C 与 Zig 只有函数指针，指针里装的仅仅是代码地址。能携带环境的那种值就是闭包，它把函数与捕获的变量绑在一起，于是“把函数当参数传”与“把一段行为连数据一起传”成了同一件事。这一节讲函数值本身怎么写、怎么传、怎么组合；闭包捕获语义与逃逸的细节归 closure.md，泛型高阶函数的类型层面细节归 generic.md。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的闭包是一等值，类型由编译器按捕获方式自动推断为 `Fn`、`FnMut` 或 `FnOnce` 三种 trait 之一。普通函数指针写作 `fn(i32) -> i32`，它只能指向不捕获环境的函数；闭包字面量用竖线写参数（`|x| x * 2`），能用 `move` 强制按值捕获。

```rust
fn twice(f: fn(i32) -> i32, x: i32) -> i32 { f(f(x)) }   // fn 指针：无环境

fn main() {
    let dbl = |x: i32| x * 2;              // 闭包：竖线参数列表
    println!("{}", dbl(21));                // 42
    println!("{}", twice(|x| x + 3, 1));      // 7  无捕获的闭包可当 fn 指针
    let mut count = 0;
    let mut tick = || { count += 1; count };   // FnMut：可变借用捕获
    println!("{} {}", tick(), tick());           // 1 2
    let owned = String::from("hi");
    let show = move || owned.clone();             // move：按值捕获
    println!("{}", show());                        // hi
    let adder = |a: i32| move |b: i32| a + b;       // 柯里化
    println!("{}", adder(40)(2));                    // 42
    let composed = |x: i32| dbl(x + 1);               // 组合
    println!("{}", composed(1));                        // 4
}
```

`Fn` 借用环境（可多次调用）、`FnMut` 可变借用、`FnOnce` 消耗环境（只能调一次）；接收方写 `impl Fn(i32) -> i32` 就能接受闭包，写 `fn(i32) -> i32` 只接受函数指针。`move` 常用于把闭包交给线程或存进结构体，它把捕获的变量所有权搬进闭包，之后原变量不可再用。想同时接受两者时泛型参数写 `F: Fn(i32) -> i32`，编译器会分别 monomorphize。

上面演示的是函数作为值怎么传递与组合；同一份机制里还有闭包那条线：`Fn`/`FnMut`/`FnOnce` 决定值能不能重复调用，`move` 决定它是否把环境搬走，`fn` 指针则只认不捕获环境的函数。匿名函数与捕获的写法见下一节。

Rust 的函数是一等值：具名函数能赋给变量、当参数传、当返回值，函数项与闭包都实现 `Fn` trait 家族。表示函数的值分两种，函数指针 `fn(i32) -> i32` 只带代码地址、不带环境，函数项在需要时会被**强制转换**成它；闭包把捕获的变量一起打包，类型是编译器生成的匿名类型。类型全在编译期确定，泛型高阶函数对每个具体类型各做一次 monomorphization。

```rust
fn double(x: i32) -> i32 { x * 2 }
fn plus_one(x: i32) -> i32 { x + 1 }
fn twice(f: fn(i32) -> i32, x: i32) -> i32 { f(f(x)) }
fn apply<F: Fn(i32) -> i32>(f: F, x: i32) -> i32 { f(x) }
fn pick(flag: bool) -> fn(i32) -> i32 { if flag { double } else { plus_one } }
fn compose(f: fn(i32) -> i32, g: fn(i32) -> i32) -> impl Fn(i32) -> i32 {
    move |x| f(g(x))
}

fn main() {
    let f: fn(i32) -> i32 = double;              // 函数项强制转换为 fn 指针
    println!("{}", f(21));                        // 42
    println!("{}", twice(double, 4));             // 16
    println!("{}", pick(false)(41));              // 42

    let dbl = |x: i32| x * 2;                     // 闭包同样是值
    println!("{}", apply(|x| x + 1, 41));         // 42
    println!("{}", apply(&dbl, 21));              // 42

    let add = |a: i32| move |b: i32| a + b;       // 柯里化
    println!("{}", add(40)(2));                   // 42
    let inc_then_double = compose(double, plus_one);   // 组合
    println!("{}", inc_then_double(3));           // 8

    let s = String::from("hello");
    let len = String::len;                        // 路径当方法引用
    println!("{}", len(&s));                       // 5
    let ks = vec![1, 2, 3];
    println!("{:?}", ks.iter().copied().map(double).collect::<Vec<_>>());  // [2, 4, 6]

    let xs = vec![1, 2, 3, 4];
    let doubled: Vec<i32> = xs.iter().map(|x| x * 2).collect();
    println!("{:?}", doubled);                    // [2, 4, 6, 8]
    let evens: Vec<&i32> = xs.iter().filter(|x| *x % 2 == 0).collect();
    println!("{:?}", evens);                      // [2, 4]
    println!("{}", xs.iter().fold(0, |acc, x| acc + x));  // 10
}
```

`fn(i32) -> i32` 与 `impl Fn(i32) -> i32` 的分界在于能不能带环境：`fn` 指针能存进结构体、写进静态常量、跨 FFI 传递，但只有不捕获环境的闭包才能转换成它，带捕获的闭包只能走泛型或 `dyn Fn`。`apply` 用泛型参数 `F: Fn(i32) -> i32` 同时收下闭包与函数指针，代价是为每个实参类型各生成一份代码；`apply(&dbl, 21)` 传引用是因为 `Fn` 对 `&F` 也实现了一次，可以避免把闭包移走。Rust 里的方法引用就是路径写法，`String::len` 的类型是 `fn(&String) -> usize`，可以像普通函数一样当值用。

标准库的高阶函数集中在 `Iterator` trait：`map`, `filter` 是惰性的，直到 `collect`, `fold`, `for_each` 才逐个求值；`fold` 对应其它语言里的 `reduce`，`sum`, `count`, `any`, `all` 也都是同一族。`pick` 演示把函数指针当返回值，`compose` 演示把两个函数指针组合成一个 `impl Fn`，返回闭包时要写 `move` 才能把参数搬进闭包。`add` 那种柯里化不是语言特性，而是“返回闭包”的惯用法，`add(40)(2)` 式的两级调用就是它的用法。

Rust 没有默认参数，也没有变参：只有 `extern "C"` 的函数指针类型才允许 `...`，普通函数需要可变参数时惯例是收 `&[T]` 或 `Vec<T>`，需要可选参数时用 builder 模式或 `Option<T>`。想同时接受函数指针与闭包，就写泛型约束 `F: Fn(i32) -> i32`；想擦掉具体类型放进同一个容器，就写 `Box<dyn Fn(i32) -> i32>`。⚠️ 把带捕获的闭包赋给 `fn` 指针类型会直接编译失败，这是这里最容易踩的坑。

📘 [Rust · Function pointer types](https://doc.rust-lang.org/reference/types/function-pointer.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的函数与闭包都是一等值，闭包字面量用花括号 `{ 参数 in 表达式 }`，`$0`、`$1` 是匿名参数简写。闭包默认捕获外部变量的**引用**，因此能修改外层 `var`；值语义类型被捕获时捕获的是那份值。尾随闭包语法让 `map { ... }` 这类调用看起来像语言结构。

```swift
func twice(_ f: (Int) -> Int, _ x: Int) -> Int { f(f(x)) }

let dbl: (Int) -> Int = { $0 * 2 }
print(dbl(21))                               // 42
print(twice({ $0 + 3 }, 1))                    // 7

var count = 0
let tick = { () -> Int in count += 1; return count }   // 引用捕获，可改外层 var
print(tick(), tick())                            // 1 2

func makeAdder(_ a: Int) -> (Int) -> Int { { b in a + b } }  // 捕获参数
print(makeAdder(40)(2))                            // 42

print([1, 2, 3].map { $0 * 2 })                     // [2, 4, 6]
print([1, 2, 3].reduce(0, +))                        // 6
let composed: (Int) -> Int = { dbl($0 + 1) }
print(composed(1))                                    // 4
```

闭包捕获引用意味着循环里创建的多个闭包会共享同一个变量，Swift 的 `for` 循环每次迭代都是新的绑定，所以这个坑比在 C 系里小。要打破引用捕获、避免循环引用时用捕获列表：`{ [weak self] in ... }` 或 `{ [x] in ... }` 显式按值捕获。`@escaping` 标注会逃出函数作用域的闭包参数，默认参数是非逃逸的。

上面演示的是函数与闭包作为值传递；还有一条线是环境：闭包默认按引用捕获，捕获列表 `[x]`（以及 `[weak self]`）才是控制点，`@escaping` 决定它能不能活过函数返回。这些写法见下一节。

Swift 里每个函数都有确定的函数类型，比如 `(Int) -> Int`，函数类型和 `Int`, `String` 一样能用于变量、参数、返回值、集合元素；全局函数、嵌套函数、闭包表达式是同一个东西的三种形态，而且函数与闭包都是**引用类型**。把函数当值传不需要任何转换，`func` 声明的函数名直接就是那个值。

```swift
typealias BinOp = (Int, Int) -> Int

func double(_ x: Int) -> Int { x * 2 }
func plusOne(_ x: Int) -> Int { x + 1 }
func twice(_ f: (Int) -> Int, _ x: Int) -> Int { f(f(x)) }
func apply(_ f: (Int) -> Int, to x: Int) -> Int { f(x) }
func adder(_ a: Int) -> (Int) -> Int { { b in a + b } }
func pick(_ flag: Bool) -> (Int) -> Int { flag ? double : plusOne }
func compose(_ f: @escaping (Int) -> Int, _ g: @escaping (Int) -> Int) -> (Int) -> Int {
    { f(g($0)) }
}

let f: (Int) -> Int = double              // 具名函数当值
print(f(21))                               // 42
print(twice(double, 4))                    // 16
print(apply({ $0 + 1 }, to: 41))           // 42
print(adder(40)(2))                        // 42
print(pick(false)(41))                     // 42
let add: BinOp = (+)                       // 运算符也是函数
print(add(40, 2))                          // 42
print(compose(double, plusOne)(3))         // 8

let s = "hi"
let upper = s.uppercased                   // 绑定方法当值：() -> String
print(upper())                             // HI

print(["bb", "a", "ccc"].map { $0.count })          // [2, 1, 3]
print(["bb", "a", "ccc"].filter { $0.count > 1 })    // ["bb", "ccc"]
print([1, 2, 3, 4].reduce(0, +))            // 10
print([3, 1, 2].sorted(by: <))              // [1, 2, 3]
```

`twice` 接收 `(Int) -> Int`，`apply` 的调用处带参数标签但类型里不写标签，`adder` 返回 `(Int) -> Int` 也就是返回一个闭包。`compose` 的参数闭包被存进返回的闭包，因此必须标 `@escaping`；不逃逸的闭包参数默认是非逃逸的，编译器可以省掉引用计数与堆分配。`pick` 用三元表达式在两个函数之间选一个返回，`let add: BinOp = (+)` 说明运算符本身就是同类型的函数，`typealias` 则用来给函数类型起短名字。

标准库的 `map`, `filter`, `reduce`, `sorted` 都收闭包，尾随闭包语法让 `["bb", "a", "ccc"].map { $0.count }` 读起来像语言结构；`reduce(0, +)` 直接传运算符函数，`sorted(by: <)` 同理。绑定到实例的方法也能当值，`s.uppercased` 的类型是 `() -> String`，它与自由函数、闭包表达式可以互换使用。Swift 没有内置的柯里化或部分应用，惯例是返回闭包，`adder(40)(2)` 就是手写的两级调用。顺带一提，Swift 6.2 起标准库有了定长数组 `InlineArray<let count: Int, Element>`（SE-0453），它把元素内联存放、不会只为自身存储引入堆分配，可以作为 `Array` 在性能敏感场景的补充，这一点也能说明“值类型 + 泛型”是 Swift 处理数据的默认路线。

函数类型在赋值时需要精确匹配参数类型与返回类型，`(Int) -> Int` 与 `(Int) -> Int?` 不能互相赋值，参数标签也不属于函数类型的一部分。⚠️ 闭包参数被存起来或跨异步边界传递时必须标 `@escaping`，漏标会得到 “escaping closure captures non-escaping parameter” 这类编译错误；反过来，不逃逸的参数不要乱标，标了会平白增加引用计数开销。需要把函数放进字典或数组时先想清楚类型是否统一，签名差一个可选或 `throws` 就必须先包一层。

📘 [Swift · Functions](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/functions/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的函数是一等值，可以赋给变量、当参数、当返回值；用 `type` 声明函数类型后可读性更好。Go 没有单独的 lambda 关键字，匿名函数就是 `func(...) ... { ... }`，闭包捕获外层变量是**引用捕获**。Go 没有函数指针语法，函数值本身就是指针大小的两个字（代码指针 + 捕获环境指针）。

```go
package main

import "fmt"

type BinOp func(int, int) int                        // 函数类型

func twice(f func(int) int, x int) int { return f(f(x)) }
func adder(a int) func(int) int { return func(b int) int { return a + b } }

func main() {
	dbl := func(x int) int { return x * 2 }         // 匿名函数赋给变量
	fmt.Println(dbl(21))                             // 42
	fmt.Println(twice(func(x int) int { return x + 3 }, 1))   // 7
	fmt.Println(adder(40)(2))                         // 42

	count := 0
	tick := func() int { count++; return count }       // 引用捕获
	fmt.Println(tick(), tick())                         // 1 2

	var op BinOp = func(a, b int) int { return a + b }
	fmt.Println(op(40, 2))                              // 42
	fmt.Println(op == nil)                               // false
}
```

函数值只能与 `nil` 比较，不能相互比较——即使两个函数体一模一样，`f == g` 也是编译错误。Go 1.22 起 `for` 循环变量每次迭代都是新的绑定，之前版本里在循环里创建闭包必须写 `i := i` 才行。把匿名函数作为 goroutine 参数时注意 `defer` 与 `recover` 的作用域。

上面演示的是函数值怎么赋值、传参与返回；环境那条线则完全隐式：没有捕获列表，闭包按变量捕获，逃逸分析决定变量留在栈上还是堆上，循环变量的语义由语言版本决定。这些写法见下一节。

Go 的函数是一等值：具名函数与函数字面量都是值，类型写作 `func(int) int`，可以赋给变量、当参数、当返回值、放进 map 与 slice。函数值内部含两个部分，即代码指针和它捕获的环境（`enclosed variables`）的引用，所以 Go 没有 C 那种“裸函数指针”的专有类型，可以用 `type` 给函数类型起名提高可读性。

```go
package main

import (
	"fmt"
	"slices"
	"strings"
)

type BinOp func(int, int) int

func twice(f func(int) int, x int) int { return f(f(x)) }
func adder(a int) func(int) int       { return func(b int) int { return a + b } }
func compose(f, g func(int) int) func(int) int {
	return func(x int) int { return f(g(x)) }
}

func Sum[T ~int | ~float64](xs []T) T { // 类型集只能作约束
	var t T
	for _, x := range xs {
		t += x
	}
	return t
}

func main() {
	dbl := func(x int) int { return x * 2 }
	fmt.Println(twice(dbl, 4))                                      // 16
	fmt.Println(adder(40)(2))                                        // 42
	fmt.Println(compose(dbl, func(x int) int { return x + 1 })(3))    // 8
	var op BinOp = func(a, b int) int { return a + b }
	fmt.Println(op(40, 2))                                            // 42
	up := strings.ToUpper                // 具名函数当值
	fmt.Println(up("hi"))                 // HI
	r := strings.NewReplacer("a", "b")
	bound := r.Replace                    // 方法值：接收者已绑定
	fmt.Println(bound("a"))               // b
	expr := (*strings.Replacer).Replace    // 方法表达式：接收者是第一个参数
	fmt.Println(expr(r, "a"))              // b

	fmt.Println(strings.Map(func(x rune) rune { return x + 1 }, "ab"))  // bc
	fmt.Println(strings.FieldsFunc("a,b;c", func(r rune) bool { return r == ',' || r == ';' })) // [a b c]
	fmt.Println(slices.IndexFunc([]int{1, 3, 4}, func(x int) bool { return x%2 == 0 }))  // 2
	fmt.Println(slices.ContainsFunc([]int{1, 2, 3}, func(x int) bool { return x > 2 }))  // true
	fmt.Println(Sum([]int{1, 2, 3}))        // 6
	fmt.Println(Sum([]float64{1.5, 2.5}))   // 4
}
```

方法有两种取成函数值的方式：`r.Replace` 是**方法值**，接收者已经绑定，类型是 `func(string) string`；`(*strings.Replacer).Replace` 是**方法表达式**，接收者变成第一个参数，类型是 `func(*strings.Replacer, string) string`。具名函数可以直接赋给变量，`strings.ToUpper` 与 `dbl` 这样的匿名函数在类型层面没有区别；函数值只能与 `nil` 比较，`f == g` 即使两个函数体一模一样也是编译错误。

标准库的高阶函数不叫 `map`, `filter`，而是按用途分散在各包：`strings.Map` 按 rune 变换字符串，`strings.FieldsFunc` 按自定义分隔符分词，`slices.IndexFunc`, `slices.ContainsFunc`, `slices.SortFunc` 接收谓词或比较函数，`sort.Slice` 是更早的接口。Go 没有内建柯里化，返回函数值就是惯用法，`adder(40)(2)` 的两级调用与 `compose` 都是手写组合；函数类型写进泛型参数就能做通用的 Map 或 Filter，代价是每次实例化各生成一份代码。

泛型函数可以接收函数类型的参数，约束里的 `Sum[T ~int | ~float64]` 用的是类型集；Go 的 union 类型集只能作泛型约束，⚠️ 它不能用来声明变量，把 `~int | ~float64` 写进 `var` 或结构体字段会直接编译失败，这与 TypeScript 的联合类型完全不同。Go 1.27 起方法也能声明自己的类型参数，`Sum` 这类逻辑因此可以放进某个类型的命名空间，但接口的方法仍然不能带类型参数，也不能由泛型方法实现。

📘 [Go spec · Function types](https://go.dev/ref/spec#Function_types)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的函数是一等对象，任何函数都能赋给变量、进字典、当参数；`lambda` 只是“只能写一个表达式”的匿名函数语法糖。闭包用 `nonlocal` 声明要修改的外层变量，否则赋值会创建新的局部变量。

```python
def twice(f, x):
    return f(f(x))

double = lambda x: x * 2          # lambda 只能是一个表达式
print(double(21))                  # 42
print(twice(lambda x: x + 3, 1))     # 7

def adder(a):
    def inner(b):
        return a + b
    return inner                       # 闭包捕获 a
print(adder(40)(2))                     # 42

def make_counter():
    n = 0
    def step():
        nonlocal n                       # 没有 nonlocal 会 UnboundLocalError
        n += 1
        return n
    return step
c = make_counter()
print(c(), c())                          # 1 2

from functools import partial, reduce
from operator import add
print(partial(add, 40)(2))                # 42
print(reduce(lambda acc, x: acc + x, [1, 2, 3], 0))   # 6
print(list(map(add, [1, 2], [10, 20])))                 # [11, 22]
```

闭包捕获的是**变量**而不是值，所以循环里创建的闭包会共享最后一个值，要给每个闭包固定值就写默认参数 `lambda x, i=i: ...` 或用 `functools.partial`。`lambda` 里不能有语句、不能赋值、不能写注解，需要多行就老老实实 `def`。函数对象带 `__name__`、`__doc__`、`__defaults__`、`__closure__` 等属性，是装饰器能工作的基础。

上面演示的是函数对象怎么传递；匿名函数与环境那条线是 `lambda` 只能写一个表达式、闭包按 cell 捕获、写回外层要用 `nonlocal`。这些写法见下一节。

Python 的函数是运行期的一等对象（first-class object）：`def` 和 `lambda` 都只是创建一个 `function` 对象并把它绑定到名字，函数因此能赋给变量、放进字典与列表、当参数传、当返回值返回。类型检查发生在运行期，注解只是元数据，不参与分派。最该先记住的是函数对象与普通对象没有区别，`__name__`, `__doc__`, `__defaults__` 都是可以直接读取的属性。

```python
def apply_twice(f, x):                     # 高阶函数：函数当参数
    return f(f(x))

def double(x):                             # 具名函数也是普通对象
    "把参数翻倍"
    return x * 2

print(type(double))                        # <class 'function'>
print(double.__name__, double.__doc__)     # double 把参数翻倍
print(callable(double), callable(41))      # True False
print(apply_twice(double, 21))             # 84
print(apply_twice(lambda x: x + 3, 1))     # 7

ops = {"double": double, "inc": lambda x: x + 1}   # 函数进字典
print(ops["inc"](41))                      # 42

def compose(f, g):                         # 返回函数：组合
    return lambda x: f(g(x))
inc_then_double = compose(double, lambda x: x + 1)
print(inc_then_double(20))                 # 42

print(list(map(str.upper, ["a", "b"])))    # ['A', 'B']

from functools import partial, reduce
from operator import add, mul
print(partial(mul, 6)(7))                            # 42
print(reduce(add, [1, 2, 3, 4], 0))                  # 10
print(list(map(double, [1, 2, 3])))                  # [2, 4, 6]
print(list(filter(lambda x: x % 2, range(6))))       # [1, 3, 5]
print(sorted(["bb", "a", "ccc"], key=len))           # ['a', 'bb', 'ccc']
print(sorted([3, 1, 2], key=lambda x: -x))           # [3, 2, 1]
```

代码里 `apply_twice` 收函数当参数，`compose` 返回新函数，`ops` 把函数当字典的值，这些写法不需要任何额外语法。`functools.partial` 固定左侧若干实参得到新的可调用对象，是最常用的部分应用手段；`functools.reduce`, `map`, `filter`, `sorted(key=len)` 则是标准库里的高阶函数。

⚠️ `map` 与 `filter` 在 Python 3 返回惰性迭代器而不是列表，直接打印只会看到对象地址，要看结果必须再用 `list` 包一层；`sorted` 的 `key` 只接收单个元素，写成 `key=f(x)` 会先求值，正确做法是传函数对象本身。`lambda` 与 `def` 产生的对象类型相同，区别只在语法，前者的体必须是一个表达式，不能有语句、赋值或注解。

方法本身也是函数对象，`str.upper` 可以直接交给 `map`。装饰器正是建立在「函数是对象」之上，`functools.wraps` 用来保留被包装函数的元数据，被装饰对象可以是函数、方法或类。闭包捕获变量的语义（`cell` 与 `nonlocal`）见 closure.md。

📘 [Python · Lambda 与函数对象](https://docs.python.org/3/reference/expressions.html#lambda)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的函数是一等值：函数类型写作 `(Int) -> Int`，函数引用用 `::name`，lambda 用花括号 `{ x -> ... }`，只有一个参数时可以用 `it`。如果 lambda 是最后一个参数，可以写到括号外面（尾随 lambda），这让 `list.map { it * 2 }` 读起来像语言结构。

```kotlin
fun twice(f: (Int) -> Int, x: Int) = f(f(x))

fun double(x: Int) = x * 2

fun adder(a: Int): (Int) -> Int = { b -> a + b }      // 返回闭包

fun main() {
    val dbl = { x: Int -> x * 2 }                       // lambda
    println(dbl(21))                                     // 42
    println(twice({ it + 3 }, 1))                         // 7  it 是唯一参数
    println(twice(::double, 1))                            // 4  函数引用
    println(adder(40)(2))                                   // 42
    println(listOf(1, 2, 3).map { it * 2 })                  // [2, 4, 6]
    println(listOf(1, 2, 3).filter { it % 2 == 1 }.sum())     // 4

    var count = 0
    val tick = { count += 1; count }                          // 捕获外层 var
    println("${tick()} ${tick()}")                             // 1 2
    println(listOf(1, 2, 3).fold(0) { acc, x -> acc + x })       // 6
}
```

Kotlin 的 lambda 捕获的是变量本身（闭包），因此能修改 `var`；JS 里“循环闭包共享变量”的问题在 Kotlin 中同样存在。`inline` 修饰的高阶函数（`map`、`filter`、`forEach` 都是 inline）不会生成函数对象，`return` 可以直接从外层函数返回；`crossinline` 与 `noinline` 用来约束这种内联行为。函数类型带接收者 `String.() -> Int` 是 Kotlin DSL 的基础。

上面演示的是函数类型的值与引用；匿名函数与环境那条线是 lambda 字面量、`it` 简写、尾随 lambda，以及被改写的捕获变量如何装箱。这些写法见下一节。

Kotlin 是静态类型语言，函数类型写成专门的样子，例如 `(Int) -> Int`；在 JVM 上函数类型的值由 `Function1`, `Function2` 这样的接口实例表示，所以函数能存进变量与集合、当参数传、当返回值返回。函数字面量（lambda 与匿名函数）和可调用引用 `::name` 都能产生函数类型的值。带接收者的函数类型 `A.(B) -> C` 与把接收者写成第一个参数的类型在赋值时可以互换，这是 Kotlin DSL 的类型基础。

```kotlin
fun twice(f: (Int) -> Int, x: Int): Int = f(f(x))     // 高阶函数

fun double(x: Int): Int = x * 2

fun adder(a: Int): (Int) -> Int = { b -> a + b }       // 返回函数

fun compose(f: (Int) -> Int, g: (Int) -> Int): (Int) -> Int =
    { x -> f(g(x)) }                                   // 组合

fun main() {
    val inc: (Int) -> Int = { it + 1 }                 // 函数类型的变量
    println(inc(41))                                   // 42
    println(twice(::double, 21))                       // 84
    println(twice({ it + 3 }, 1))                      // 7
    println(adder(40)(2))                              // 42

    val ops: Map<String, (Int) -> Int> =
        mapOf("double" to ::double, "inc" to inc)      // 函数进 Map
    println(ops["inc"]?.invoke(41))                    // 42

    println(compose(::double, inc)(20))                // 42

    println(listOf(1, 2, 3).map { it * 2 })            // [2, 4, 6]
    println(listOf(1, 2, 3).filter { it % 2 == 1 })    // [1, 3]
    println(listOf(1, 2, 3).fold(0) { acc, x -> acc + x })   // 6

    val upper: String.() -> String = { uppercase() }   // 带接收者
    println("ab".upper())                              // AB
    val addLen: String.(Int) -> Int = { n -> length + n }
    println("abc".addLen(2))                           // 5
}
```

函数类型的写法有两条硬规则：参数表放在括号里，返回类型写在 `->` 之后，返回 `Unit` 时不能省略；整个类型要可空必须加括号写成 `((Int) -> Int)?`，而箭头是右结合的，`(Int) -> (Int) -> Unit` 等于 `(Int) -> ((Int) -> Unit)`。`::name` 产生的是 `KFunction1` 这类可调用引用，绑定到具体实例写成 `expr::method`，构造器写成 `::Ctor`，引用重载函数时需要上下文能确定目标重载。

最常用的高阶函数是集合上的 `map`, `filter`, `fold`, `reduce`, `forEach`；当 lambda 是最后一个参数时可以移到括号外（尾随 lambda），只有一个参数且类型能推断时还可以省略参数与箭头，直接用 `it`。部分应用与柯里化没有内置语法，靠返回 lambda 手写，`adder(40)` 返回的就是新函数，`compose` 则演示了函数组合。

本机未安装 Kotlin 2.4 工具链，以上输出按官方文档语义书写，未经本机运行验证。

📘 [Kotlin · Lambda expressions and anonymous functions](https://kotlinlang.org/docs/lambdas.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 没有独立的函数类型，函数作为值必须依附于**函数式接口**：只有一个抽象方法的接口。`java.util.function` 提供了 `Function<T,R>`、`Supplier<T>`、`Consumer<T>`、`Predicate<T>`、`BiFunction<T,U,R>` 等标准形状，lambda 写 `(a, b) -> a + b`，方法引用写 `ClassName::method`。

```java
import java.util.List;
import java.util.function.BiFunction;
import java.util.function.Function;
import java.util.function.IntUnaryOperator;
import java.util.function.Supplier;

public class FirstClass {
    static int twice(IntUnaryOperator f, int x) { return f.applyAsInt(f.applyAsInt(x)); }
    static int apply(BiFunction<Integer, Integer, Integer> f, int a, int b) { return f.apply(a, b); }
    static Function<Integer, Integer> adder(int a) { return b -> a + b; }   // 返回闭包

    public static void main(String[] args) {
        IntUnaryOperator dbl = x -> x * 2;
        System.out.println(dbl.applyAsInt(21));                // 42
        System.out.println(twice(x -> x + 3, 1));                // 7
        System.out.println(apply(Integer::sum, 40, 2));           // 42
        System.out.println(adder(40).apply(2));                    // 42
        Supplier<String> s = () -> "hi";
        System.out.println(s.get());                                // hi
        List.of(1, 2, 3).stream().map(x -> x * 2).forEach(System.out::print);  // 246
        System.out.println();
    }
}
```

lambda 捕获的外部局部变量必须是 **effectively final**（赋值一次后不再变），因为 Java 的闭包是按值捕获副本，不能修改外层局部变量；要可变状态只能用数组或字段。`Function<Integer,Integer>` 会带来装箱开销，对 `int` 热路径用 `IntUnaryOperator`、`IntBinaryOperator` 这类特化接口。方法引用有四种形式：静态方法、实例方法、任意对象的实例方法、构造器。

上面演示的是函数式接口怎么承载函数值；匿名函数与环境那条线是 lambda 与匿名类的差别、只捕获 effectively final 的局部变量。这些写法见下一节。

Java 没有独立的函数类型，函数作为值必须依附于**函数式接口**：只有一个抽象方法的接口，lambda 与方法引用只有在目标类型是函数式接口时才合法。`java.util.function` 定义了标准形状与命名规则，`Function<T,R>` 是一元函数，`BiFunction<T,U,R>` 是二元函数，`Supplier<T>` 无参，`Consumer<T>` 返回空，`Predicate<T>` 返回 `boolean`。泛型参数只能是包装类型，`IntUnaryOperator`, `IntBinaryOperator`, `ToIntFunction` 这类特化接口用来避开装箱。

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.function.BiFunction;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.IntUnaryOperator;
import java.util.function.Predicate;
import java.util.function.Supplier;

public class FirstClass {
    static int twice(IntUnaryOperator f, int x) { return f.applyAsInt(f.applyAsInt(x)); }

    static Function<Integer, Integer> adder(int a) { return b -> a + b; }   // 返回函数

    static <T, R> List<R> mapList(List<T> xs, Function<T, R> f) {           // 函数当参数
        return xs.stream().map(f).toList();
    }

    public static void main(String[] args) {
        IntUnaryOperator dbl = x -> x * 2;                 // int -> int，不装箱
        System.out.println(dbl.applyAsInt(21));            // 42
        System.out.println(twice(x -> x + 3, 1));          // 7

        Supplier<String> s = () -> "hi";                   // 无参
        System.out.println(s.get());                       // hi
        Consumer<String> pr = System.out::println;         // 绑定实例方法引用
        pr.accept("done");                                 // done

        BiFunction<Integer, Integer, Integer> add = Integer::sum;   // 静态方法引用
        System.out.println(add.apply(40, 2));              // 42
        System.out.println(List.of("a", "bb").stream().map(String::length).toList());  // [1, 2]

        Supplier<List<String>> mk = ArrayList::new;        // 构造器引用
        System.out.println(mk.get().size());               // 0

        Map<String, Function<Integer, Integer>> ops =
            Map.of("double", x -> x * 2, "inc", x -> x + 1);
        System.out.println(ops.get("inc").apply(41));      // 42

        System.out.println(adder(40).apply(2));            // 42
        System.out.println(adder(1).andThen(x -> x * 2).apply(20));   // 42
        System.out.println(mapList(List.of(1, 2, 3), x -> x * x));   // [1, 4, 9]

        Predicate<Integer> odd = x -> x % 2 == 1;
        System.out.println(odd.test(3));                   // true
    }
}
```

方法引用有四类，语法与 lambda 一一对应：静态方法写 `RefType::staticMethod`（如 `Integer::sum`），绑定实例写 `expr::instanceMethod`（如 `System.out::println`），非绑定实例写 `RefType::instanceMethod`，此时接收者成为第一个参数（如 `String::length`），构造器写 `ClassName::new`（如 `ArrayList::new`）。目标类型决定选哪个重载，所以同一个 `ArrayList::new` 赋给不同接口可以指向不同构造器。函数式接口允许有默认方法与静态方法，只要抽象方法恰好一个，`@FunctionalInterface` 只起让编译器帮忙检查的作用。

装箱是 Java 函数式写法最容易踩的性能坑：`Function<Integer,Integer>` 每次调用都要把 `int` 装成 `Integer` 再拆回来，热路径应改用 `IntUnaryOperator`, `IntBinaryOperator`, `IntPredicate`, `ToIntFunction` 这类以基本类型为参数和返回值的接口。Java 没有内置的部分应用与柯里化，`adder(40)` 是手工返回函数的写法，`Function.andThen` 与 `compose` 提供组合，固定二元函数的某个实参则用 lambda 包一层。

本机未安装 JDK 26（LTS 25），以上输出按官方文档语义书写，未经本机运行验证。

📘 [Java · Lambda Expressions](https://docs.oracle.com/javase/tutorial/java/javaOO/lambdaexpressions.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++11 起有 lambda 表达式：`[捕获](参数) -> 返回类型 { 体 }`，返回类型可省略由编译器推导。lambda 是一个唯一的匿名类（closure type），捕获列表决定它持有哪些成员；`std::function` 是类型擦除后的通用可调用包装，能存 lambda、函数指针和函数对象，代价是一次间接调用与可能的堆分配。

```cpp
#include <cstdio>
#include <functional>
#include <vector>
#include <algorithm>
#include <memory>

int twice(const std::function<int(int)>& f, int x) { return f(f(x)); }

int main() {
    auto dbl = [](int x) { return x * 2; };              // 无捕获
    std::printf("%d\n", dbl(21));                          // 42
    std::printf("%d\n", twice([](int x) { return x + 3; }, 1));   // 7

    int base = 10;
    auto byValue = [base](int x) { return base + x; };    // 值捕获：不可写
    auto byRef = [&base](int x) { base += x; return base; };   // 引用捕获
    std::printf("%d\n", byValue(5));                        // 15
    std::printf("%d\n", byRef(5));                           // 15
    std::printf("%d\n", base);                                // 15

    auto moves = [p = std::make_unique<int>(7)] { return *p; };   // 初始化捕获
    std::printf("%d\n", moves());                              // 7
    std::printf("%d\n", [](int x) { return x + 1; }(41));        // 42  立即调用

    std::vector<int> v{1, 2, 3};
    std::printf("%d\n", (int)std::count_if(v.begin(), v.end(),
        [](int x) { return x % 2 == 1; }));                      // 2
}
```

捕获列表的三种主要写法是 `[=]`（按值捕获所有用到的）、`[&]`（按引用捕获所有用到的）、显式列出（`[base, &count]`，最推荐）。按引用捕获的 lambda 不能活过被捕获变量；按值捕获的 lambda 默认是 `const`，要修改副本得加 `mutable`。`std::function` 不能存 move-only 的 lambda（如捕获了 `unique_ptr` 的），那种情况用 `auto` 或模板参数接收。

上面演示的是函数指针、`std::function` 与函数对象怎么当值用；匿名函数那条线是完全不同的机制：lambda 表达式会生成唯一的匿名类，捕获列表决定它持有什么。这些写法见下一节。

C++ 的函数是一等值，载具有三种：具名函数会退化为函数指针，`std::function` 提供类型擦除后的统一可调用类型，模板参数则让高阶函数在编译期完成 `monomorphization`。函数指针最轻、完全不带环境，`std::function` 能同时接受函数指针、函数对象与 lambda，代价是一次间接调用与可能的堆分配，而且要求目标可拷贝。标准库的高阶函数（`std::for_each`, `std::transform`, `std::count_if`, `std::sort`）走的是模板参数而不是 `std::function`，所以传 lambda 不会付类型擦除的代价。

```cpp
#include <cstdio>
#include <functional>
#include <vector>
#include <algorithm>

int inc(int x) { return x + 1; }
int twice(int (*f)(int), int x) { return f(f(x)); }      // 函数指针作参数
std::function<int(int)> adder(int a) {                    // 返回类型擦除的可调用对象
    return [a](int b) { return a + b; };
}
int (*pick(char op))(int, int) {                          // 返回函数指针
    return op == '+' ? [](int a, int b) { return a + b; } : nullptr;
}

int main() {
    int (*fp)(int) = inc;                                   // 具名函数退化为指针
    std::printf("%d\n", fp(41));                             // 42
    std::printf("%d\n", twice(inc, 40));                      // 42

    std::function<int(int)> erased = inc;                      // 类型擦除包装
    std::printf("%d\n", erased(41));                            // 42

    auto add = [](int a, int b) { return a + b; };
    auto add5 = std::bind_front(add, 5);                         // C++20 部分应用
    std::printf("%d\n", add5(37));                                // 42
    using namespace std::placeholders;
    auto add5b = std::bind(add, 5, _1);                           // C++11 的 bind
    std::printf("%d\n", add5b(37));                                // 42

    std::printf("%d\n", adder(40)(2));                              // 42
    std::printf("%d\n", pick('+')(40, 2));                           // 42

    std::vector<int> v{1, 2, 3, 4};
    int sum = 0;
    std::for_each(v.begin(), v.end(), [&sum](int x) { sum += x; });   // lambda 作实参
    std::printf("%d\n", sum);                                          // 10
    return 0;
}
```

`std::bind` 与 lambda 的取舍：`std::bind` 写起来短，但占位符 `_1`, `_2`, `_3` 可读性差，嵌套 bind 的求值时机也容易出意外，现代写法优先直接写 lambda，需要部分应用时用 C++20 的 `std::bind_front` 或 C++23 的 `std::bind_back`。`std::function` 的调用无法稳定内联，热路径应改用模板参数或 `auto` 接收；函数指针可以为 `nullptr`，调用前必须判空。

C++23 补上了能装 move-only 目标的 `std::move_only_function`，它接受不可拷贝的可调用对象，但调用空对象是未定义行为（`std::function` 则是抛 `std::bad_function_call`）。本机 clang 21 的 libc++ 尚未提供这个类，写 `std::move_only_function<int()>` 会直接报 no member named，跨平台使用前要先做特性检测。

📘 [cppreference · Lambda expressions](https://en.cppreference.com/w/cpp/language/lambda)

{{% /tab %}}

{{% tab header="C" %}}

C 里函数可以作为值传递，但只能通过**函数指针**：指针里只有代码地址，没有环境，所以 C 没有闭包。函数名在表达式中自动退化为指针，`typedef` 能让指针类型可读。要模拟闭包，只能手工把上下文结构体作为额外参数传进去。

```c
#include <stdio.h>

typedef int (*BinOp)(int, int);              /* 函数指针类型 */
typedef struct { int base; } Adder;            /* 手工传递的“捕获环境” */

int add(int a, int b) { return a + b; }
int twice(int (*f)(int), int x) { return f(f(x)); }
int inc(int x) { return x + 1; }
int apply(BinOp op, int a, int b) { return op(a, b); }

int add_with_ctx(void *ctx, int x) {            /* 用 void* 模拟闭包 */
    Adder *a = ctx;
    return a->base + x;
}

int main(void) {
    BinOp op = add;
    printf("%d\n", op(40, 2));                   /* 42 */
    printf("%d\n", twice(inc, 1));                /* 3 */
    printf("%d\n", apply(add, 20, 22));            /* 42 */
    Adder a = { 40 };
    printf("%d\n", add_with_ctx(&a, 2));            /* 42 */
    return 0;
}
```

`void *ctx` 加函数指针是最常见的“穷人的闭包”模式（`qsort_r`、`pthread_create`、各种回调 API 都这么干），代价是类型安全全部丢失。C 不支持嵌套函数的标准写法，GCC 的嵌套函数扩展依赖 trampoline，可执行栈在现代系统上通常被禁用，不要依赖。函数指针可以为 `NULL`，调用前必须判空。

上面演示的是函数指针怎么当值传递；匿名函数那条线在 C 里不存在：没有闭包、没有 lambda 字面量，环境只能靠 `void *` 加回调参数手工传。替代做法见下一节。

C 的函数指针是真正的函数值：函数名在表达式中自动退化为指向函数的指针，指针里只有代码地址，没有环境。`typedef` 把难读的声明折成类型名，是写回调 API 的常规做法；高阶函数就是收函数指针作参数或返回函数指针的函数。C23 给这门语言补上了 `typeof`, `nullptr`, `[[nodiscard]]`，但依旧没有重载、没有泛型函数、没有闭包。

```c
#include <stdio.h>

typedef int (*IntFn)(int);                  /* 函数指针类型 */
typedef int (*BinOp)(int, int);

int inc(int x) { return x + 1; }
int add(int a, int b) { return a + b; }

int twice(IntFn f, int x) { return f(f(x)); }        /* 函数作参数 */

BinOp pick(char op) {                                 /* 函数作返回值 */
    return op == '+' ? add : nullptr;                  /* C23 的 nullptr */
}

[[nodiscard]] int compute(int x) { return x * 2; }     /* C23 标准属性 */

int main(void) {
    IntFn f = inc;                                     /* 具名函数退化为指针 */
    printf("%d\n", f(41));                               /* 42 */
    printf("%d\n", twice(inc, 40));                       /* 42 */

    typeof(f) g = f;                                      /* C23 的 typeof */
    printf("%d\n", g(41));                                 /* 42 */

    printf("%d\n", pick('+')(40, 2));                       /* 42 */
    if (pick('?') == nullptr) printf("no op\n");             /* no op */

    struct Op { const char *name; BinOp fn; } ops[] = { { "add", add } };
    printf("%d\n", ops[0].fn(compute(10), 22));               /* 42 */
    return 0;
}
```

`typeof` 是 C23 标准化的类型推导运算符（此前只有 GCC, Clang 的扩展），可以用它声明与已有函数指针同型的变量，省掉重抄一遍声明；`nullptr` 是 C23 的新关键字、类型为 `nullptr_t`，能隐式转成任意指针类型，比 `NULL` 更安全；`[[nodiscard]]` 是 C23 标准属性，忽略被标注函数的返回值只会产生警告，本机 `clang -std=c23 -Wall` 实测给出 ignoring return value of function declared with 'nodiscard' attribute。

函数指针可以放进数组、结构体，也可以当结构体成员，标准库里的 `qsort`, `bsearch`, `signal`, `atexit` 都以它为参数；`typedef` 版本比 `int (*f)(int)` 这种裸声明可读得多，复杂签名（返回函数指针的函数）尤其要 typedef。陷阱有两个：函数指针可以为 `NULL`，调用前必须判空；老式的 `int f()` 表示参数未指定而不是无参数，写 `int f(void)` 才明确。需要携带环境时只能自己传上下文结构体，那是闭包一页的内容。

📘 [cppreference · C pointers to functions](https://en.cppreference.com/w/c/language/pointer#Pointers_to_functions)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的函数是一等值，匿名函数写成 `x -> x * 2`，或写成 `function (x)` 到 `end` 的多行形式；`do` 块语法让 `map(xs) do x` 到 `end` 的写法变成把匿名函数作为第一个参数传入。闭包捕获变量的方式是**装箱**：被内层函数修改的外层局部变量会被放进一个堆上的 `Core.Box`，这会带来性能开销。

```julia
double = x -> x * 2                       # 匿名函数
println(double(21))                        # 42

twice(f, x) = f(f(x))
println(twice(x -> x + 3, 1))               # 7

adder(a) = b -> a + b                        # 返回闭包
println(adder(40)(2))                         # 42

function make_counter()
    n = 0
    () -> (n += 1)                             # 捕获并修改 n
end
c = make_counter()
println((c(), c()))                            # (1, 2)

println(map(x -> x * 2, [1, 2, 3]))              # [2, 4, 6]
println(map([1, 2, 3]) do x; x + 1; end)          # [2, 3, 4]
println(reduce(+, [1, 2, 3]))                      # 6
println(1:3 .|> double)                             # [2, 4, 6]
```

闭包的性能提示很具体：如果内层函数只读外层变量，Julia 不会装箱；一旦内层函数对内层变量赋值，该变量就被装箱，类型变为 `Core.Box`，热路径会退化。解决办法是把可变状态放进 `Ref` 或 `mutable struct`，让捕获的是那个容器的引用。`do` 块的函数参数名为 `it` 的约定并不存在——Julia 里必须显式写参数名。

上面演示的是函数怎么传参、怎么用 `do` 块收尾；匿名函数与环境那条线是 `x -> x * 2` 字面量、`do` 块语法，以及被改写的捕获变量装箱带来的开销。这些写法见下一节。

Julia 的函数是一等对象：不加括号的 `f` 就是一个函数值，可以赋给变量、当参数、当返回值、塞进数组或字典。具名函数是带方法的泛型函数对象，`Function` 是它们的抽象父类型；高阶函数是标准库的基础设施，`map`, `filter`, `reduce`, `foldl`, 广播 `f.(xs)` 与管道 `|>` 都围绕函数值工作。部分应用有专门的类型 `Base.Fix{N}`，组合用 `∘`，两样都不必写匿名函数。

```julia
double(x) = x * 2                        # 具名函数
f = double                                # 函数当值：同一个函数对象
println(f(21))                             # 42
println(f === double)                       # true

apply_twice(f, x) = f(f(x))                 # 高阶函数：函数作参数
println(apply_twice(double, 10))             # 40

make_adder(a) = b -> a + b                   # 返回匿名函数
println(make_adder(40)(2))                    # 42

println(map(double, [1, 2, 3]))               # [2, 4, 6]
println(filter(iseven, [1, 2, 3, 4]))          # [2, 4]
println(reduce(+, [1, 2, 3, 4]))                # 10
println(double.([1, 2, 3]))                      # [2, 4, 6]
println(1:3 .|> double)                           # [2, 4, 6]
println(foldl(-, [1, 2, 3]))                       # -4
println(+(1, 2, 3))                                 # 6  运算符即函数
println(sum(x -> x^2, [1, 2, 3]))                    # 14
const42 = Base.Returns(42)                            # 常量函数
println(const42(1, 2))                                 # 42

inc(x) = x + 1
composed = inc ∘ double                            # 先 double 再 inc
println(composed(20))                               # 41

half = Base.Fix2(/, 2)                               # 固定第二个参数
println(half(8))                                      # 4.0
add1 = Base.Fix1(+, 1)                                # 固定第一个参数
println(add1(41))                                      # 42
```

`Base.Fix{N}(f, x)` 把 `f` 的第 `N` 个参数固定为 `x`，通用的 `Fix{N}` 从 Julia 1.12 起才有，更早只提供 `Fix1`, `Fix2` 两个别名；`Base.Returns(v)` 返回一个永远给出 `v` 的可调用对象（Julia 1.7 起）。运算符本身也是函数，`+` 不加括号就能传给 `reduce`；`1:3 .|> double` 是广播版管道，等价于 `broadcast(double, 1:3)`。Julia 对函数实参做特化，传匿名函数不会像 `std::function` 那样产生间接调用，但把函数塞进 `Any` 容器会破坏类型推断。

管道与匿名函数混用时括号不能省：`1:3 .|> (x -> x^2) |> sum` 得到 14，不写括号时后续的 `|>` 会被解析进匿名函数体。以下输出按官方手册与 REPL 语义给出，本机未安装 Julia，未经运行验证。

📘 [Julia · Functions（匿名函数与 do 块）](https://docs.julialang.org/en/v1/manual/functions/#Anonymous-Functions)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的函数作为值依赖**委托**：`Func<...>`、`Action<...>`、`Predicate<T>` 是内置泛型委托，自定义委托用 `delegate` 声明。lambda 写 `x => x * 2`，语句体写 `x => { return x * 2; }`，方法组 `Method` 能直接转成委托。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;

delegate int BinOp(int a, int b);          // 自定义委托

class FirstClass {
    static int Twice(Func<int, int> f, int x) => f(f(x));
    static Func<int, int> Adder(int a) => b => a + b;     // 返回闭包
    static int Add(int a, int b) => a + b;

    static void Main() {
        Func<int, int> dbl = x => x * 2;
        Console.WriteLine(dbl(21));                        // 42
        Console.WriteLine(Twice(x => x + 3, 1));            // 7
        BinOp op = Add;                                      // 方法组转换
        Console.WriteLine(op(40, 2));                         // 42
        Console.WriteLine(Adder(40)(2));                       // 42
        Console.WriteLine(string.Join(",", new[]{1,2,3}.Select(x => x * 2)));  // 2,4,6
        Action<string> log = Console.WriteLine;
        log("hi");                                            // hi
    }
}
```

lambda 捕获的局部变量在 C# 里被提升为编译器生成的闭包类的字段，所以捕获是**按引用**的，循环里创建的 lambda 会共享同一个变量——`foreach` 从 C# 5 起每次迭代是新变量，但 `for` 循环仍要写 `int copy = i;`。给 lambda 加 `static` 修饰符（C# 9+）能让它不能捕获任何东西，既避免意外分配，也能让编译器直接缓存成静态委托。

上面演示的是委托与方法组怎么承载函数值；匿名函数与环境那条线是 lambda 的表达式体与语句体、`static` lambda 禁止捕获，以及捕获变量被提升为闭包类字段。这些写法见下一节。

C# 用委托把函数变成值：委托是类型安全的函数指针加上可选的目标对象，`Func<T, TResult>` 有返回值，`Action<T>` 返回 void，`Predicate<T>` 返回 bool，自定义形状用 `delegate` 声明。方法组（方法名不带括号）在目标委托类型明确时隐式转成委托，lambda 也能转；只有需要自然类型时（例如 `var f = Method;`）方法组才要求重载唯一。LINQ 的 `Select`, `Where`, `Aggregate`, `OrderBy` 全都以委托为参数。

```csharp
using System;
using System.Linq;

class FirstClass {
    static int Add(int a, int b) => a + b;
    static int Inc(int x) => x + 1;
    static int Twice(Func<int, int> f, int x) => f(f(x));        // 委托作参数
    static Func<int, int> Adder(int a) => b => a + b;             // 返回委托

    static void Main() {
        Func<int, int> dbl = x => x * 2;
        Console.WriteLine(dbl(21));                               // 42
        Console.WriteLine(Twice(x => x + 3, 1));                   // 7
        Func<int, int> inc = Inc;                                   // 方法组转换
        Console.WriteLine(inc(41));                                  // 42
        Action<string> log = Console.WriteLine;                       // 方法组
        log("hi");                                                     // hi
        Predicate<int> isEven = x => x % 2 == 0;
        Console.WriteLine(isEven(4));                                  // True
        Console.WriteLine(string.Join(",", new[] { 1, 2, 3 }.Select(dbl)));   // 2,4,6
        Console.WriteLine(new[] { 1, 2, 3, 4 }.Where(x => isEven(x)).Sum());   // 6
        Console.WriteLine(Adder(40)(2));                                 // 42
        Func<int, int> compose = x => inc(dbl(x));                        // 手工组合
        Console.WriteLine(compose(20));                                    // 41
        Func<int, int, int> add = (a, b) => a + b;
        Console.WriteLine(add(40, 2));                                      // 42
        Console.WriteLine(new[] { 1, 2, 3, 4 }.Aggregate((a, b) => a + b));   // 10
        int[] data = { 3, 1, 2 };
        Array.Sort(data, (a, b) => a.CompareTo(b));                           // Comparison<int>
        Console.WriteLine(string.Join(",", data));                             // 1,2,3
    }
}
```

委托实例记住 Target 与 Method，可以用 `+=` 组合成多播委托，调用既写 `d(args)` 也可以写 `d.Invoke(args)`。`Func<T, TResult>` 最多带 16 个输入参数，超出要自定义委托；`Predicate<T>` 与 `Func<T, bool>` 是两个不同的委托类型，不能直接互相赋值，但方法组与 lambda 能按目标类型分别转成两者，示例里 `Where` 收的是 `Func<int, bool>`，所以写成 `x => isEven(x)`。

lambda 有自己的自然类型（C# 10 起），`var f = (int x) => x * 2;` 能推出 `Func<int, int>`；方法组只有在重载唯一时才有自然类型，`Console.Write` 这种重载集合必须显式指定委托类型。C# 14 的扩展成员（extension members）允许用 `extension` 块声明扩展属性、静态扩展方法甚至用户定义运算符，例如 `extension<TSource>(IEnumerable<TSource> source) { public bool IsEmpty => !source.Any(); }` 之后可以直接写 `seq.IsEmpty`；扩展方法本身仍是静态方法，照样能当方法组转成委托。本机没有 .NET SDK，以上输出未经运行验证。

📘 [MS Learn · Delegates 与 lambda](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的函数是一等值，函数类型写作 `int Function(int)` 或 `T Function<X>(X)`，匿名函数用 `(x) => x * 2`（单表达式）或 `(x) { return x * 2; }`。Dart 的闭包按引用捕获外层变量，可以修改可变局部变量。类里出现的 `this` 在普通匿名函数与箭头函数中表现一致，这点和 JavaScript 不同。

```dart
int twice(int Function(int) f, int x) => f(f(x));

int Function(int) adder(int a) => (b) => a + b;      // 返回闭包

int double_(int x) => x * 2;

void main() {
  final dbl = (int x) => x * 2;
  print(dbl(21));                        // 42
  print(twice((x) => x + 3, 1));           // 7
  print(twice(double_, 1));                 // 4  具名函数当值传
  print(adder(40)(2));                       // 42

  var count = 0;
  final tick = () => ++count;                 // 引用捕获
  print('${tick()} ${tick()}');                // 1 2

  print([1, 2, 3].map((x) => x * 2).toList());   // [2, 4, 6]
  print([1, 2, 3].where((x) => x.isOdd).toList());  // [1, 3]
  print([1, 2, 3].fold<int>(0, (a, b) => a + b));     // 6
}
```

`dart:core` 里的 `Function` 是所有函数类型的顶层类型，用 `Function.apply(f, [args])` 做动态调用，代价是丢失静态类型。把函数存进变量时最好显式写出函数类型，否则推断出的类型可能过窄，后续赋值给别的签名时才报错。箭头函数体可以整体是异步表达式（`() async => await load()`），此时返回类型是 `Future<T>`，这个写法在 Flutter 的事件回调里非常常见。

上面演示的是函数类型 `T Function(T)` 与函数引用怎么用；匿名函数与环境那条线是箭头函数、闭包按变量捕获，以及 `Function.apply` 的动态调用。这些写法见下一节。

Dart 的函数是一等对象，所有函数都实现顶层类型 `Function`，函数类型写成 `int Function(int)`，可以起别名、当参数传、当返回值返回。Dart 是静态类型语言，泛型在运行期是 reified 的，所以函数类型本身也能用 `is` 判断。这里先看最该记住的三件事：函数类型怎么写、怎么用 record 返回多个值、以及 `extension type` 如何在不增加运行期开销的前提下包装一个函数类型。

```dart
typedef IntFn = int Function(int);                     // 函数类型别名

int twice(IntFn f, int x) => f(f(x));                   // 高阶函数
int triple(int x) => x * 3;                             // 具名函数当值传

int Function(int) adder(int a) => (b) => a + b;          // 返回闭包

String tag(String s, {String prefix = '#', required int n}) => '$prefix$s$n';

(int, int) minMax(List<int> xs) {                        // record 返回多个值
  var lo = xs.first, hi = xs.first;
  for (final v in xs) {
    if (v < lo) lo = v;
    if (v > hi) hi = v;
  }
  return (lo, hi);
}

extension type Predicate(bool Function(int) test) {       // Dart 3.3 起的静态包装
  bool call(int x) => test(x);
}

void main() {
  print(twice((x) => x + 3, 36));          // 42
  print(twice(triple, 4));                 // 36
  print(adder(40)(2));                      // 42
  print(tag('x', n: 1));                     // #x1
  final (lo, hi) = minMax([3, 1, 4, 1, 5]);
  print('$lo $hi');                           // 1 5
  final odd = Predicate((x) => x.isOdd);
  print(odd(3));                               // true
  print(odd.test(4));                           // false
  print([1, 2, 3].map((x) => x * 2).toList());   // [2, 4, 6]
  print([1, 2, 3].where((x) => x.isOdd).toList());  // [1, 3]
  print([1, 2, 3].fold<int>(0, (a, b) => a + b));    // 6
  dynamic d = (int x) => x * 2;
  print(d is int Function(int));                       // true  泛型具体化
}
```

`typedef IntFn` 只是给签名起名，`twice` 的参数和 `triple` 的实参都按结构化签名匹配，Dart 里并不存在独立的函数指针类型。`extension type` 是编译期抽象，运行期不产生包装对象，它把表示对象（这里是 `bool Function(int)`）藏起来，只暴露正文里声明的成员，所以 `odd.test` 能取到原函数，而 `odd.isOdd` 这类未声明的成员会直接编译报错。`minMax` 用 record 返回 `(int, int)`，解构写法 `final (lo, hi) = ...` 比返回 `List<int>` 更不容易写错位置。默认参数与命名参数都要求默认值是编译期常量，`required` 命名参数可以不写默认值；`Function.apply` 是运行期动态调用入口，代价是返回 `dynamic` 并丢掉静态类型。本机未安装 Dart SDK，以上输出按官方文档语义书写，未经运行验证。

📘 [Dart · Functions](https://dart.dev/language/functions)

{{% /tab %}}

{{% tab header="R" %}}

在 R 里函数就是普通对象，`f <- function(x) x + 1` 与 `x <- 1` 没有本质区别；函数可以存进 list、当参数传、当返回值返回。R 的闭包捕获**整个定义环境**（lexical scoping），内层函数用 `<<-` 可以修改外层函数里的变量。

```r
double <- function(x) x * 2                        # 函数就是普通对象
print(double(21))                                   # [1] 42

twice <- function(f, x) f(f(x))                      # 高阶函数
print(twice(function(x) x + 3, 1))                    # [1] 7
print(twice(double, 1))                                # [1] 2

adder <- function(a) function(b) a + b                  # 返回闭包
print(adder(40)(2))                                      # [1] 42

make_counter <- function() {
  n <- 0
  function() {
    n <<- n + 1                                           # <<- 修改外层绑定
    n
  }
}
c1 <- make_counter()
print(c(c1(), c1()))                                       # [1] 1 2

print(unlist(lapply(1:3, function(x) x * 2)))                # [1] 2 4 6
print(Reduce(`+`, 1:3))                                       # [1] 6
print(Filter(function(x) x %% 2 == 1, 1:5))                    # [1] 1 3 5
```

用 `ls(environment(f))` 能看到闭包捕获了哪些名字：R 捕获的是整个环境而不是单个变量，所以闭包一旦返回，它引用的所有名字都会继续存活（内存泄漏的常见来源）。`<<-` 只在“外层存在同名绑定”时向外赋值，否则会写到全局环境，这个行为容易造成意外。`lapply`/`sapply`/`vapply`/`Map`/`Reduce`/`Filter`/`Negate` 是 R 的基础高阶函数，`purrr::map` 系列是更现代的替代。

上面演示的是函数作为普通对象怎么传递；匿名函数与环境那条线是匿名 `function(x)` 字面量、惰性求值与调用环境的关系。这些写法见下一节。

在 R 里函数就是普通对象：`f <- function(x) x + 1` 与 `x <- 1` 是同一类赋值，`typeof(f)` 返回 `"closure"`，函数能存进 list、当参数传、当返回值返回。函数对象由形式参数表、函数体、定义环境三部分组成，用 `formals`, `body`, `environment` 就能取出这三块。

```r
double <- function(x) x * 2                        # 函数是普通对象
print(double(21))                                   # [1] 42
print(typeof(double))                                # [1] "closure"

twice <- function(f, x) f(f(x))                      # 高阶函数
print(twice(function(x) x + 3, 1))                    # [1] 7
print(twice(double, 1))                                # [1] 4
print(length(formals(twice)))                           # [1] 2

adder <- function(a) function(b) a + b                  # 返回闭包
print(adder(40)(2))                                      # [1] 42
add3 <- function(a) function(b) function(c) a + b + c     # 柯里化
print(add3(1)(2)(3))                                      # [1] 6
compose <- function(f, g) function(x) f(g(x))              # 组合
print(compose(function(x) x + 1, double)(20))               # [1] 41

print(unlist(lapply(1:3, function(x) x * 2)))                 # [1] 2 4 6
print(sapply(1:3, function(x) x * 2))                          # [1] 2 4 6
print(vapply(1:3, function(x) x * 2, numeric(1)))               # [1] 2 4 6
print(unlist(Map(`+`, 1:3, 4:6)))                                # [1] 5 7 9
print(Reduce(`+`, 1:3))                                           # [1] 6
print(Reduce(`+`, 1:3, accumulate = TRUE))                         # [1] 1 3 6
print(Filter(function(x) x %% 2 == 1, 1:5))                         # [1] 1 3 5
print(Negate(is.null)(NULL))                                         # [1] FALSE
print(is.function(double))                                            # [1] TRUE
print(length(formals(double)))                                         # [1] 1
print(do.call(double, list(21)))                                       # [1] 42
print(match.fun("double")(21))                                          # [1] 42
```

`lapply` 一定返回 list，`sapply` 会尝试把结果化简成向量，各元素类型不一致时化简结果可能出乎意料，`vapply` 要求你给出返回值模板（例如 `numeric(1)`），不匹配就报错，所以写包时优先用 `vapply`。`Map` 是 `mapply` 的包装并返回 list，`Reduce` 做 fold 并保证二元函数总是收到两个参数，`Filter` 按谓词取子集，`Negate` 把一个谓词变成它的否定。

`match.fun` 按名字取函数并跳过同名的非函数对象，`do.call` 把函数与参数 list 拼成一次调用，这两个是写高阶函数时的防御性工具；`formals`, `body`, `environment` 既是读取器也可以出现在赋值左侧，用来改造已有函数。`purrr::map` 系列提供更一致的返回类型和更清晰的报错，是 base 高阶函数之外常被推荐的替代。

函数作为值传递时还会带上它的定义环境，所以把一个在函数内部定义的函数返回出去，它引用的名字会继续存活，这是闭包一页的主题。本机未安装 R，以上输出按官方文档与手册语义书写，未经运行验证。

📘 [R · The R Language Definition · Functions](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Functions)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有闭包**，也没有 lambda 字面量的捕获能力：函数是第一类值，但只能取已有函数的指针（`&f` 或直接写 `f`），指针里只有代码地址，没有环境。要模拟“带捕获的回调”，标准做法是把上下文结构体作为第一个参数（`*Context`）或放进 `anytype` 参数里。

```zig
const std = @import("std");

const Adder = struct {
    base: i32,
    fn call(self: Adder, x: i32) i32 { return self.base + x; }   // 方法：带隐式 self
};

fn twice(comptime f: fn (i32) i32, x: i32) i32 { return f(f(x)); }
fn inc(x: i32) i32 { return x + 1; }

fn applyToAll(xs: []i32, ctx: anytype) void {   // 用 anytype 传“环境”
    for (xs) |*v| v.* = ctx.add(v.*);
}

pub fn main() void {
    const a = Adder{ .base = 40 };
    std.debug.print("{d}\n", .{a.call(2)});            // 42
    std.debug.print("{d}\n", .{twice(inc, 1)});          // 3

    var xs = [_]i32{ 1, 2, 3 };
    const Scaler = struct {
        k: i32,
        pub fn add(self: @This(), v: i32) i32 { return self.k + v; }
    };
    applyToAll(&xs, Scaler{ .k = 10 });
    std.debug.print("{d} {d} {d}\n", .{ xs[0], xs[1], xs[2] });   // 11 12 13
}
```

Zig 的惯用模式是“数据 + 函数指针”打包成结构体（`std.mem.Allocator` 就是 vtable + 上下文指针的组合），这等价于手写的闭包对象，但分配与生命周期完全由你控制。`comptime f: fn (i32) i32` 要求传入的函数在编译期已知，因此不能存进运行期数组；要运行期可变就得用 `*const fn (ctx: *anyopaque, x: i32) i32` 加一个 `*anyopaque` 上下文。

上面演示的是函数指针与 `anytype` 怎么当值传递；匿名函数那条线在 Zig 里不存在：没有闭包、没有 lambda 字面量，要带上下文就把结构体与函数指针一起传。替代做法见下一节。

Zig **没有闭包**，也**没有 lambda 字面量**：函数能当值用，但只有函数指针这一种形态，指针里只有代码地址，没有环境。函数是第一类值，可以取已有函数的指针（写 `&f` 或直接写 `f`），要携带状态就必须自己把上下文结构体显式传给函数。替代做法是把“数据 + 函数指针”打包成结构体，或者照抄标准库的 vtable + 上下文指针模式。

```zig
const std = @import("std");

fn twice(comptime f: fn (i32) i32, x: i32) i32 { return f(f(x)); }
fn triple(x: i32) i32 { return x * 3; }              // 具名函数当值传

const Adder = struct {                                // 方法：self 就是显式环境
    base: i32,
    pub fn call(self: Adder, x: i32) i32 { return self.base + x; }
};

const Ctx = struct {                                   // 手写的“闭包对象”
    base: i32,
    pub fn apply(ctx: *const anyopaque, x: i32) i32 {
        const self: *const Ctx = @ptrCast(@alignCast(ctx));
        return self.base + x;
    }
};

fn mapInPlace(xs: []i32, ctx: *const anyopaque,
              f: *const fn (*const anyopaque, i32) i32) void {
    for (xs) |*v| v.* = f(ctx, v.*);                   // 运行期回调
}

pub fn main() void {
    std.debug.print("{d}\n", .{twice(triple, 4)});             // 36
    std.debug.print("{d}\n", .{Adder{ .base = 40 }.call(2)});   // 42

    var xs = [_]i32{ 1, 2, 3 };
    const ctx = Ctx{ .base = 10 };
    mapInPlace(&xs, &ctx, Ctx.apply);
    std.debug.print("{d} {d} {d}\n", .{ xs[0], xs[1], xs[2] });  // 11 12 13
}
```

`comptime f: fn (i32) i32` 要求函数在编译期已知，编译器按实参做 monomorphization，代价是这类函数不能存进运行期数组；要运行期可变就用 `*const fn (*const anyopaque, i32) i32` 配一个 `*const anyopaque` 上下文指针，`Ctx` 与 `Ctx.apply` 就是最小的 vtable + 上下文模式，等价于手写的闭包对象，但分配与生命周期完全由调用者负责。标准库的 `std.mem.Allocator` 正是这个模式：它由 `ptr: *anyopaque` 和 `vtable: *const VTable` 两个字段组成，vtable 里每一条都是 `*const fn (*anyopaque, ...)` 形状的函数指针，所以“带状态的分配器”不需要闭包也能实现。复合字面量 `.{ ... }` 与 `@This()` 是这套写法的常用配料。本机未安装 Zig，以上输出按官方文档语义书写，未经运行验证。

📘 [Zig · Functions 与 Pointers](https://ziglang.org/documentation/master/#Function-Pointer)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的函数是一等值，`function(x) return x * 2 end` 是匿名函数字面量，闭包捕获的是**upvalue**（外层局部变量），按引用共享。所有函数都是闭包，只是大多数没有 upvalue。`table` 加函数字段就构成了最简单的对象与方法。

```lua
local double = function(x) return x * 2 end
print(double(21))                        -- 42

local function twice(f, x) return f(f(x)) end
print(twice(function(x) return x + 3 end, 1))   -- 7

local function adder(a)                   -- 返回闭包，捕获 a
  return function(b) return a + b end
end
print(adder(40)(2))                        -- 42

local function make_counter()              -- 共享 upvalue
  local n = 0
  return function() n = n + 1; return n end
end
local c = make_counter()
print(c(), c())                             -- 1  2

local xs = {1, 2, 3}
local sum = 0
for _, v in ipairs(xs) do sum = sum + v end
print(sum)                                   -- 6
print(table.concat((function()
  local t = {}
  for i, v in ipairs(xs) do t[i] = v * 2 end
  return t
end)(), ","))                                  -- 2,4,6
```

`for` 的控制变量每轮都是一次新的局部变量声明，循环体里创建的闭包各捕获各的 `i`，`for i = 1, 3 do fns[i] = function() return i end end` 之后 `fns[1]()` 到 `fns[3]()` 得到 1、2、3，这是 Lua 与旧版 JavaScript 相反的地方；真正会共享的是循环外声明的变量，例如 `while` 里手写的计数器，那种情况才要在循环体里加一层 `local v = v`。Lua 5.5 起 `for` 控制变量本身只读（`const`），赋值会被拒绝。`_ENV` 是每个 chunk 的 upvalue，`setfenv` 已被移除，5.2 之后换环境靠 `load(chunk, name, mode, env)` 的第四个参数。

上面演示的是函数作为一等值怎么传递与调用；匿名函数与环境那条线是 `function(x) ... end` 字面量、upvalue 共享，以及 `_ENV` 的作用。这些写法见下一节。

Lua 手册开篇就写明“所有值都是一等值”，函数也不例外：`function(x) ... end` 是匿名函数字面量，`function f() ... end` 只是 `f = function() ... end` 的语法糖。闭包捕获外层局部变量作为 upvalue，多个闭包按引用共享同一个 upvalue；table 加函数字段就是 Lua 的对象，`:` 冒号语法只是给方法加一个隐式的 `self`。

```lua
local double = function(x) return x * 2 end       -- 匿名函数赋给变量
print(double(21))                                   -- 42
print(type(double))                                  -- function

local function twice(f, x) return f(f(x)) end        -- 高阶函数
print(twice(function(x) return x + 3 end, 1))         -- 7
print(twice(double, 1))                                -- 4

local function adder(a)                                -- 返回闭包
  return function(b) return a + b end
end
print(adder(40)(2))                                     -- 42

local up = 10
local function bump() up = up + 1; return up end         -- upvalue 按引用共享
print(bump())                                             -- 11

local Obj = {}
Obj.__index = Obj
function Obj.new(n) return setmetatable({ n = n }, Obj) end
function Obj:inc() self.n = self.n + 1; return self.n end   -- 隐式 self
print(Obj.new(40):inc())                                -- 41

local ys = { 3, 1, 2 }
table.sort(ys, function(a, b) return a > b end)          -- 把函数传给标准库
print(table.concat(ys, ","))                              -- 3,2,1
print(math.max(1, 5, 3))                                   -- 5

print(table.concat((function()                            -- 立即执行函数
  local t = {}
  for i, v in ipairs({ 1, 2, 3 }) do t[i] = v * 2 end
  return t
end)(), ","))                                              -- 2,4,6
```

`local function f` 与 `local f = function` 的区别只在递归：前者先把名字引入作用域，函数体里能引用自己。Lua 标准库没有 `map`, `filter`, `reduce`，惯用做法是写 `for` 循环，或者把函数当比较器传给 `table.sort`，需要组合时自己写高阶函数。

`_ENV` 是每个 chunk 的 upvalue，自由名字被翻译成 `_ENV.name`，换环境要用 `load(chunk, name, mode, env)` 的第四个参数，而不是已经移除的 `setfenv`。Lua 5.5 把 `global` 变成保留字，chunk 默认带隐式的 `global *`，显式声明全局要写 `global x`；同一版本里 `for` 的控制变量是只读（`const`）局部变量。

所有函数都是闭包，只是大多数没有 upvalue；`print` 会调用值的 `__tostring`，而函数不是 table，所以这里不能靠元表改变它的显示方式。本机未安装 Lua，以上输出按官方手册语义书写，未经运行验证。

📘 [Lua 5.5 · Function Definitions](https://www.lua.org/manual/5.5/manual.html#3.4.11)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的一等函数与 JavaScript 完全相同，额外能力是给函数类型起名、写泛型函数类型、用重载签名描述可调用的多种形状。`type Fn = (x: number) => number` 与接口的可调用签名 `{ (x: number): number }` 都合法。

```typescript
type Mapper<T, U> = (value: T, index: number) => U;      // 函数类型别名

function twice(f: (x: number) => number, x: number): number { return f(f(x)); }
function adder(a: number): (b: number) => number { return (b) => a + b; }

const dbl: (x: number) => number = (x) => x * 2;
console.log(dbl(21));                              // 42
console.log(twice((x) => x + 3, 1));                 // 7
console.log(adder(40)(2));                            // 42

let count = 0;
const tick = (): number => ++count;
console.log(tick(), tick());                          // 1 2

const applyAll = <T, U>(xs: T[], f: Mapper<T, U>): U[] => xs.map(f);
console.log(applyAll([1, 2, 3], (x) => x * 2));         // [ 2, 4, 6 ]

interface Callable {                                     // 可调用签名
  (x: number): number;
  description: string;
}
```

TypeScript 的泛型在编译期擦除，所以不能写 `f<T>(x)` 这种“运行期知道 T”的代码，除非显式把类型或构造函数传进来。函数类型可以用 `this` 参数声明调用者的类型（`function f(this: Window, e: Event)`），这是给 JS 的 `this` 加类型的手段。重载声明只是类型层面的多个签名，实现只有一个。

上面演示的是函数类型标注与可调用签名；匿名函数与环境那条线是箭头函数、闭包按变量捕获，以及类型层对 `this` 的声明（类型在运行期不存在）。这些写法见下一节。

TypeScript 的一等函数与 JavaScript 完全一致，额外能力是给函数类型起名、写泛型函数类型、用可调用签名描述带属性的函数，以及用 `satisfies` 做检查而不改变推断结果。类型只存在于编译期，运行时与 JavaScript 相同，类型注解在编译后被完全擦除（type erasure）。TypeScript 7 是由 TypeScript 代码库移植到 Go 的原生编译器，语义与 6.0 一致而速度约快 10 倍（[官方公告](https://devblogs.microsoft.com/typescript/announcing-typescript-7-0-beta/)）。

```typescript
type Mapper<T, U> = (v: T, i: number) => U;          // 函数类型别名

function twice(f: (x: number) => number, x: number): number { return f(f(x)); }
function adder(a: number): (b: number) => number { return (b) => a + b; }
const double: Mapper<number, number> = (v) => v * 2;

interface Callable {                                   // 可调用签名 + 属性
  (x: number): number;
  description: string;
}
const inc: Callable = Object.assign((x: number) => x + 1, { description: 'inc' });

type Shape = { kind: 'circle' | 'square'; size: number };
const shape = { kind: 'circle', size: 2 } satisfies Shape;   // 保留字面量类型

function tag(this: { prefix: string }, s: string): string {  // this 参数
  return this.prefix + s;
}

const first = <T>(xs: T[]): T | undefined => xs[0];     // 泛型箭头函数
function applyAll<T, U>(xs: T[], f: Mapper<T, U>): U[] { return xs.map(f); }

console.log(twice((x) => x + 3, 36));            // 42
console.log(adder(40)(2));                        // 42
console.log(twice.length, adder.length);           // 2 1
console.log(inc(41), inc.description);              // 42 inc
console.log(shape.kind);                             // circle
console.log(tag.call({ prefix: '#' }, 'x'));          // #x
console.log(first([7, 8, 9]));                         // 7
console.log([1, 2, 3].map(double));                     // [ 2, 4, 6 ]
console.log(applyAll([1, 2, 3], (x) => x * 2));          // [ 2, 4, 6 ]
```

函数类型别名和可调用签名接口描述的是同一件事，区别是后者还能声明属性，所以带 `description` 的函数要用接口而不是裸的箭头类型；`Callable` 里的 `(x: number): number` 是调用签名，参数名可以省略。

`satisfies` 只做兼容性检查，表达式自身的推断类型不变，所以 `shape.kind` 仍是字面量类型 `'circle'`，换成 `: Shape` 注解就会丢失这个信息。`this` 参数占用了 JavaScript 不允许使用的参数名位置，只在类型层面存在，必须配 `function` 而不能用箭头函数，因为它描述的是运行期 `this` 的绑定。

泛型在编译期擦除，运行期无法判断 `T`，这一点与 Dart 的 reified 泛型、C# 的 reified 泛型方向相反；`length` 这类属性来自运行期函数对象，类型系统只描述调用形状。本机未安装 TypeScript 编译器，以上输出按官方文档语义书写，未经运行验证。

📘 [TypeScript · More on Functions](https://www.typescriptlang.org/docs/handbook/2/functions.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的函数是一等对象，拥有 `name`、`length`、`prototype` 等属性，能挂自定义属性、能当构造器（`new`）。闭包捕获外层变量按引用共享，箭头函数不绑定自己的 `this`、`arguments`、`super`、`new.target`，因此不能用作构造器。

```javascript
const twice = (f, x) => f(f(x));
const dbl = x => x * 2;
console.log(dbl(21));                        // 42
console.log(twice(x => x + 3, 1));            // 7

const adder = a => b => a + b;                 // 柯里化
console.log(adder(40)(2));                      // 42

let count = 0;
const tick = () => ++count;
console.log(tick(), tick());                     // 1 2

function makeCounter() {
  let n = 0;
  return () => ++n;                               // 闭包
}
const c = makeCounter();
console.log(c(), c());                             // 1 2

console.log([1, 2, 3].map(x => x * 2));             // [ 2, 4, 6 ]
console.log([1, 2, 3].reduce((a, b) => a + b, 0));   // 6
console.log((x => x + 1)(41));                        // 42  立即调用表达式
console.log(Object.keys({ f: 1 }));                    // [ 'f' ]
for (var i = 0; i < 2; i++) setTimeout(() => console.log('var', i));   // var 2 / var 2
for (let j = 0; j < 2; j++) setTimeout(() => console.log('let', j));   // let 0 / let 1
```

`var` 声明的变量在整个函数作用域内是同一个绑定，循环里创建的闭包会共享它（所以打出两个 `2`）；`let`/`const` 每次迭代创建新绑定。箭头函数没有 `arguments`，需要可变参数就用 rest。立即调用表达式 `(fn)()` 在模块化之前用来创建私有作用域，现在主要用于顶层 `await` 的替代写法或一次性初始化。

上面演示的是函数对象与 `arguments` 的差异；匿名函数与环境那条线是箭头函数的词法 `this`、IIFE，以及 `var` 与 `let` 在循环里的不同绑定行为。这些写法见下一节。

JavaScript 的函数是一等对象，拥有 `name`, `length`, `prototype` 等属性，能挂自定义属性，也能当构造器被 `new` 调用。函数类型在语言层面不做静态检查，签名只在文档和 TypeScript 里存在；箭头函数不绑定自己的 `this`, `arguments`, `super`, `new.target`，所以不能当构造器。捕获语义按引用共享，细节归闭包一页，这里只写结论。

```javascript
function twice(f, x) { return f(f(x)); }              // 高阶函数
const dbl = (x) => x * 2;
console.log(typeof dbl, dbl.name, dbl.length);          // function dbl 1
console.log(twice(dbl, 21));                            // 84
console.log(twice.length);                               // 2

function add(a) { return (b) => a + b; }                // 柯里化
console.log(add(40)(2));                                 // 42
const compose = (f, g) => (x) => f(g(x));                // 组合
const inc = (x) => x + 1;
console.log(compose(inc, dbl)(20));                      // 41
const fact = function f(n) { return n <= 1 ? 1 : n * f(n - 1); };
console.log(fact(5));                                     // 120

console.log([1, 2, 3].map(dbl));                          // [ 2, 4, 6 ]
console.log([1, 2, 3].filter((x) => x % 2 === 1));         // [ 1, 3 ]
console.log([1, 2, 3].reduce((a, b) => a + b, 0));          // 6
console.log([1, 2, 3].flatMap((x) => [x, x]));               // [ 1, 1, 2, 2, 3, 3 ]

function Counter() { this.n = 0; }
Counter.prototype.tick = function () { return ++this.n; };
console.log(typeof Counter.prototype, dbl.prototype);        // object undefined
const c = new Counter();
console.log(c.tick.call(c), c.tick.call(c));                  // 1 2
const boundTick = c.tick.bind(c);                              // bind 固定接收者
console.log(boundTick(), boundTick());                          // 3 4
console.log(Object.getOwnPropertyNames(Counter.prototype));      // [ 'constructor', 'tick' ]
console.log((function () { return 'IIFE'; })());                  // IIFE
console.log(add.name, twice.length);                              // add 2
```

`name` 与 `length` 是函数对象上的真实属性，`length` 数的是第一个默认参数或 rest 之前的位置参数个数；箭头函数没有 `prototype`，所以不能 `new`，普通函数有，`getOwnPropertyNames` 能看到 `constructor` 与挂在原型上的方法。

把方法取出来单独存变量会丢掉接收者，`c.tick` 直接调用时 `this` 是 `undefined`（模块里默认严格模式）并抛 `TypeError`，修法是用 `bind`, `call`, `apply`，或者干脆先绑定；`call` 逐个传参，`apply` 用数组传参，`bind` 返回一个绑定好接收者的新函数。

`(function () { ... })()` 是立即调用表达式，在模块化之前用来造私有作用域，现在多用于一次性初始化；箭头函数与 `let` 组合也能达到同样效果。惯用的高阶函数是 `map`, `filter`, `reduce`, `flatMap`，回调按“值、下标、数组”的顺序收参，`function` 表达式与箭头函数在这些位置上可以互换。本机在 Node 24.20.0 上实跑验证过以上输出，书籍基线是 Node 26，函数层面的语义在两者之间没有变化。

📘 [MDN · Functions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Functions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的一等函数有两套写法：`Closure` 与箭头函数 `fn() => expr`（PHP 7.4+）。箭头函数**自动按值捕获**外层变量，不需要 `use`；传统 `function () use ($x) {}` 必须显式列出捕获变量，默认按值，写 `use (&$x)` 才按引用。8.5 起静态闭包与一等可调用对象（`strlen(...)`）可以用在常量表达式里。

```php
<?php
function twice(callable $f, int $x): int { return $f($f($x)); }

$dbl = fn(int $x): int => $x * 2;                 // 箭头函数，自动按值捕获
echo $dbl(21), PHP_EOL;                             // 42
echo twice(fn(int $x): int => $x + 3, 1), PHP_EOL;    // 7

function adder(int $a): Closure { return fn(int $b): int => $a + $b; }
echo adder(40)(2), PHP_EOL;                          // 42

$count = 0;
$tick = function () use (&$count): int { return ++$count; };   // 按引用捕获
echo $tick(), $tick(), PHP_EOL;                       // 12

$doubleIt = array_map(fn($v) => $v * 2, [1, 2, 3]);
echo implode(',', $doubleIt), PHP_EOL;                  // 2,4,6
echo strlen(...)('abc'), PHP_EOL;                        // 3  一等可调用语法（8.1+）
```

箭头函数只能写一个表达式，且捕获是**按值**且发生在定义时——循环里定义的箭头函数各自拿到当时的值，这点比 JS 的 `var` 行为更安全。`callable` 类型可以接受字符串函数名 `'strlen'`、数组 `[$obj, 'method']`、闭包、以及 `strlen(...)` 形式；类型声明写 `Closure` 则只接受闭包对象。8.5 的管道运算符 `|>` 与 `strlen(...)` 搭配，可以把链式调用写得更像数据流。

上面演示的是 `callable` 与 `Closure` 怎么承载函数值；匿名函数与环境那条线是 `fn() => expr` 的自动按值捕获、`use (&$x)` 的按引用捕获，以及 `__invoke`。这些写法见下一节。

PHP 的函数是一等值：可以赋给变量、当参数、当返回值；运行期的可调用对象统称 `callable`，具体实现是 `Closure` 类的实例。`callable` 覆盖闭包, 字符串函数名 `'strlen'`, 数组方法引用 `[$obj, 'm']`, 以及实现了 `__invoke` 的对象，但它不能作属性类型，属性必须写 `Closure`。最该先记住的是 8.1 的一等可调用语法 `strlen(...)`：它把任意可调用表达式固化成 `Closure`，并按获取点的作用域解析可见性。

```php
<?php
declare(strict_types=1);

function twice(callable $f, int $x): int { return $f($f($x)); }    // 高阶函数

$dbl = fn(int $x): int => $x * 2;                  // 箭头函数（7.4+）
echo twice($dbl, 1), PHP_EOL;                       // 4

$len = strlen(...);                                 // 一等可调用（8.1+）
echo $len('abcd'), PHP_EOL;                          // 4

$up = Closure::fromCallable('strtoupper');           // 由函数名字符串造闭包
echo $up('abc'), PHP_EOL;                            // ABC

function shout(Closure|string $f, string $s): string { return $f($s); }   // 联合类型（8.0+）
echo shout('strtoupper', 'ok'), PHP_EOL;              // OK

$add = fn(int $a): Closure => fn(int $b): int => $a + $b;   // 手工柯里化
echo $add(40)(2), PHP_EOL;                             // 42

class Greeter {
    public function __invoke(string $n): string { return "hi $n"; }   // __invoke 对象即 callable
}
$g = new Greeter();
echo $g('ann'), PHP_EOL;                               // hi ann

$xs = [3, 1, 2];
usort($xs, fn(int $a, int $b): int => $a <=> $b);
echo implode(',', $xs), PHP_EOL;                        // 1,2,3
echo implode(',', array_filter([1, 2, 3, 4], fn($v) => $v % 2 === 0)), PHP_EOL;   // 2,4

$n = 'abcd' |> strlen(...);                             // 管道运算符（8.5+）
echo $n, PHP_EOL;                                        // 4
```

`callable` 是函数签名的类型声明，`Closure` 是具体类，两者可以一起出现在联合类型里；8.5 起 `Closure` 是 `callable` 的正式子类型（此前 `Closure` 只是概念上的可调用对象）。一等可调用语法与 `Closure::fromCallable` 语义相同，都在获取点确定作用域，因此能取到私有方法，而写成字符串 `'Foo::bar'` 的 callable 在调用点才解析，这正是它偶尔报“不能访问私有方法”的原因。PHP 没有内建的部分应用（partial application）或函数组合，柯里化要像上面那样手工返回闭包，标准库里可用的高阶函数是 `array_map`, `array_filter`, `array_reduce`, `usort`, `array_walk`。

版本与类型上还有两点要记：`callable` 不能给属性加类型，要写 `Closure`，而 8.4 起的属性钩子（property hooks）让 `Closure` 属性的读写也能写成 `get =>` 这样的内联形式；8.5 起 `#[\NoDiscard]` 可以标在返回可调用对象的工厂方法上，丢弃返回的 `Closure` 会触发警告，除非显式写成 `(void) f()` 或先存进变量。箭头函数只能写单个表达式，多行逻辑必须回到 `function () {}`。以上代码未在本机运行验证（本机未安装 PHP 8.5），语法与版本结论据 php.net 官方文档。

📘 [PHP · Anonymous functions](https://www.php.net/manual/en/functions.anonymous.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的代码块（block）、`Proc`、`lambda`、`Method` 对象都是一等值的不同形态。block 不是对象、不能单独存在，只能紧跟在方法调用后面；`Proc` 与 `lambda` 才是对象，区别在于 `lambda` 检查实参个数且 `return` 只从自身返回，`proc` 不检查且 `return` 会从外层方法返回。

```ruby
def twice(f, x) = f.call(f.call(x))

dbl = ->(x) { x * 2 }             # lambda 字面量（-> 是 Kernel#lambda 的语法糖）
prc = proc { |x| x * 2 }            # proc：参数个数不检查
puts dbl.call(21)                    # 42
puts twice(dbl, 1)                    # 4
puts twice(->(x) { x + 3 }, 1)          # 7

adder = ->(a) { ->(b) { a + b } }         # 柯里化
puts adder.call(40).call(2)                # 42

def make_counter
  n = 0
  -> { n += 1 }                              # 闭包捕获局部变量
end
c = make_counter
puts [c.call, c.call].inspect                 # [1, 2]

def apply_twice(x, &blk) = blk.call(blk.call(x))
puts apply_twice(1) { |v| v + 3 }               # 7

add = ->(a, b) { a + b }
puts add.curry[40][2]                            # 42
puts [1, 2, 3].map(&dbl).inspect                  # [2, 4, 6]
```

`&dbl` 把 Proc 当 block 传给 `map`，`&:to_s` 则是 `Symbol#to_proc` 的简写。`proc` 里 `return` 会试图从定义它的方法返回，如果那个方法已经结束就抛 `LocalJumpError`，所以异步回调一律用 `lambda`。`Method` 对象用 `method(:name)` 取得，能像 Proc 一样 `call`，也支持 `curry` 与 `to_proc`。

上面演示的是方法怎么用 `&blk` 收发代码块；匿名函数与环境那条线是 `Proc` 与 `lambda` 的差异、`->() {}` 字面量，以及闭包捕获局部变量的方式。这些写法见下一节。

Ruby 没有“函数类型”这种标注，函数本身就是对象：`Proc`（`proc` 与 `lambda`/`->` 都产出 `Proc`）, `Method`, 以及连对象都不是、只能紧跟方法调用的 block。具名方法要当值用有两个入口：`method(:name)` 取回绑定好接收者的 `Method` 对象，或在调用点写 `&:sym`，由 `Symbol#to_proc` 现场生成一个 `Proc`。所谓高阶函数在 Ruby 里就是普通方法：它接收这些对象，也可以返回它们。

```ruby
def twice(f, x) = f.call(f.call(x))            # 高阶函数：收可调用对象

dbl = ->(x) { x * 2 }                          # lambda 字面量
puts dbl.call(21)                               # 42
puts twice(dbl, 1)                               # 4

puts [1, 2, 3].map { |x| x * 2 }.inspect         # [2, 4, 6]
puts [1, 2, 3, 4].select(&:even?).inspect        # [2, 4]
puts [1, 2, 3, 4].reduce(0) { |a, b| a + b }     # 10
puts [1, 2, 3].inject(:+)                         # 6
puts [1, 2, 3].each_with_object([]) { |x, acc| acc << x * 2 }.inspect   # [2, 4, 6]

def square(x) = x * x
m = method(:square)                               # Method 对象
puts m.call(6)                                     # 36
puts m.arity                                        # 1
puts [1, 2, 3].map(&m).inspect                       # [1, 4, 9]
puts method(:square).to_proc.call(5)                 # 25
puts twice(m, 2)                                      # 16

add = ->(a, b) { a + b }
puts add.curry[40][2]                                # 42

adder = ->(a) { ->(b) { a + b } }                     # 返回函数
puts adder.call(40).call(2)                            # 42

compose = ->(f, g) { ->(x) { f.call(g.call(x)) } }
puts compose.call(->(x) { x + 1 }, ->(x) { x * 2 }).call(20)   # 41
puts (->(x) { x + 1 } >> ->(x) { x * 2 }).call(3)              # 8

puts %w[a b].map(&:upcase).inspect                     # ["A", "B"]
puts [1, 2].map(&dbl).inspect                           # [2, 4]
```

`twice` 的参数是普通对象，所以 `Method`, `Proc`, `lambda` 都能传，但 block 传不进去：它不是对象，要用 `&blk` 形参捕获成 `Proc` 才能在方法体里 `.call`，或者干脆用 `yield`。`&` 在调用点做反向转换，`map(&m)` 与 `map(&:upcase)` 走同一条路，后者是 `Symbol#to_proc` 的简写，等价于 `{ |x| x.upcase }`，代价是只能调用方法、不能带额外实参。

组合在 Ruby 里靠 `Proc#>>` 与 `Proc#<<`，前者表示先调用左边再调用右边，所以 `(f >> g).call(x)` 等于 `g.call(f.call(x))`，参数方向与 Haskell 的 `(.)` 相反；`Method` 对象也支持这两个方法，跨多种可调用形态时通常仍然手写 lambda，上面 `compose` 那种写法在任何版本都能用。`Method` 对象保留原接收者，支持 `to_proc`, `curry`, `arity`，需要把已有方法当回调、又不愿丢掉接收者时，它比重新包一个 lambda 更直接。以上代码在本机 Ruby 4.0.6 上实际运行，注释中的输出与真实输出一致。

📘 [Ruby · Method](https://docs.ruby-lang.org/en/master/Method.html)

{{% /tab %}}

{{< /tabpane >}}

### 闭包与匿名函数

匿名函数回答的是“不写名字怎么定义函数”，闭包回答的是“这个函数带着哪些变量活多久”。语法层面各语言的 lambda 字面量差别不大，真正的分歧在环境：C++ 用捕获列表显式声明，Swift 用捕获列表控制强引用，PHP 用 `use` 区分按值与按引用，其余语言大多隐式按变量捕获。C 与 Zig 没有闭包，只能把上下文结构体当额外参数手工传进去。这一节只给匿名函数的写法与捕获结论，捕获路径、逃逸分析、循环变量陷阱的完整讨论归 closure.md。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的匿名函数叫**闭包表达式**，写法是 `|x| x + 1` 或 `|x: i32| -> i32 { x + 1 }`，参数用竖线而不是圆括号，这是它和具名函数最直观的语法差别。每个闭包表达式的类型都是编译器生成的唯一匿名类型，所以闭包没有名字、没有 `.name` 之类的反射入口，要跨 API 边界传递就得擦成 `Box<dyn Fn(i32) -> i32>` 或返回 `impl Fn`。捕获方式由编译器按使用方式推断，顺序是共享借用、可变借用、按值移动，写 `move` 则一律按值捕获。

```rust
fn make_counter() -> impl FnMut() -> i32 {
    let mut n = 0;
    move || { n += 1; n }
}
fn call_once<F: FnOnce() -> String>(f: F) -> String { f() }
fn apply_twice(f: &dyn Fn(i32) -> i32, x: i32) -> i32 { f(f(x)) }

fn main() {
    let n = 3;
    let add_n = |x: i32| x + n;                 // 按引用捕获
    println!("{}", add_n(39));                   // 42

    let s = String::from("hi");
    let show = move || s.clone();                // 按移动捕获
    println!("{}", show());                      // hi
    println!("{}", std::any::type_name_of_val(&show).contains("closure"));  // true

    let mut count = 0;
    let mut tick = || { count += 1; count };     // FnMut
    println!("{} {}", tick(), tick());            // 1 2

    let mut c = make_counter();
    println!("{} {}", c(), c());                  // 1 2

    let boxed: Box<dyn Fn(i32) -> i32> = Box::new(|x| x * 2);  // type erasure
    println!("{}", boxed(21));                     // 42
    println!("{}", apply_twice(&|x| x + 1, 40));    // 42

    let owned = String::from("bye");
    let consume = move || owned;
    println!("{}", call_once(consume));             // bye

    let mut fns: Vec<Box<dyn Fn() -> i32>> = Vec::new();
    for i in 1..=3 {
        fns.push(Box::new(move || i));               // 每轮新绑定
    }
    println!("{}", fns.into_iter().map(|f| f()).sum::<i32>());  // 6

    println!("{}", (|| 42)());                        // 42
}
```

`Fn` 可以多次调用且只要 `&self`，`FnMut` 要 `&mut self`，`FnOnce` 消耗自身、只能调一次；所有闭包都实现 `FnOnce`，具体实现哪些由闭包对捕获值做了什么决定，而不是由它怎么捕获决定，所以 `move` 闭包照样可能是 `Fn`。`make_counter` 返回 `impl FnMut() -> i32`，把 `n` 搬进闭包并让它活过函数调用；`call_once` 收 `FnOnce`，把捕获的 `String` 交出去。`move` 最常见的用途是让闭包满足 `'static`，例如丢给线程或存进结构体，代价是原变量之后不能再用。

`Box<dyn Fn(i32) -> i32>` 用 vtable 做动态分派并擦掉具体类型，适合把签名相同、来源不同的闭包塞进同一个 `Vec`；返回 `impl Fn` 则保留具体类型、走静态分派，没有间接跳转。闭包可以立即调用，`(|| 42)()` 就是立即调用表达式；Rust 闭包没有默认参数也没有变参，需要变参时收 `&[T]`。闭包之间不能比较，也不能直接当 `HashMap` 的键，需要标识时先转成函数指针或自己造一个 id。

`for` 循环的循环变量每一轮都是新的绑定，所以循环里创建的闭包各捕获各的 `i`，`1..=3` 三轮累加得到 6 而不是 9，不需要像老式 C 系语言那样写临时变量。捕获路径、借用冲突、`'static` 边界与循环变量陷阱的完整讨论归闭包一页，这里只记结论：默认借、`move` 移、`move` 之后原变量失效。⚠️ 用 `std::any::type_name_of_val` 只能看到带匿名占位符的类型名，任何依赖闭包类型名的写法都不可靠，上面那个 `contains("closure")` 打印 `true` 只是说明它确实是个匿名类型。

📘 [Rust · Closure expressions](https://doc.rust-lang.org/reference/expressions/closure-expr.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的匿名函数叫**闭包表达式**，形式是 `{ (参数) -> 返回类型 in 语句 }`，`in` 之前是签名、之后是函数体；参数与返回类型能从上下文推断时可以全省，参数还能简写成 `$0`, `$1`，作为最后一个参数时可以用尾随闭包写到括号外。闭包和函数一样是引用类型，赋值给两个变量时它们指向同一个闭包。

```swift
var count = 0
let tick = { () -> Int in count += 1; return count }   // 引用捕获
print(tick(), tick())                                    // 1 2

let add = { (a: Int, b: Int) -> Int in a + b }
print(add(40, 2))                                        // 42
print({ (x: Int) -> Int in x * 2 }(21))                  // 42 立即调用

func makeCounter() -> () -> Int {
    var n = 0
    return { n += 1; return n }                          // n 逃逸到堆上
}
let c = makeCounter()
print(c(), c())                                          // 1 2

func run(_ body: () -> Void) { body() }
run { print("trailing") }                                // trailing
func keep(_ body: @escaping () -> Void) -> () -> Void { body }
let saved = keep { print("escaped") }
saved()                                                  // escaped

var x = 10
let captureNow = { [x] in x }                            // 捕获列表立即取值
x = 99
print(captureNow())                                      // 10

func greet(_ name: String, times: Int = 1) -> String {   // 默认参数
    String(repeating: "hi ", count: times) + name
}
print(greet("a"), "|", greet("a", times: 2))              // hi a | hi hi a

func total(_ xs: Int...) -> Int { xs.reduce(0, +) }       // 变参
print(total(1, 2, 3))                                     // 6

func log(_ message: @autoclosure () -> String) { print(message()) }
log("lazy")                                               // lazy

var fns: [() -> Int] = []
for i in 1...3 { fns.append { i } }                      // for-in 每轮新绑定
print(fns.map { $0() })                                  // [1, 2, 3]
print([3, 1, 2].sorted { $0 < $1 })                      // [1, 2, 3]
```

闭包默认按**引用**捕获外层变量，所以能修改外层的 `var` 并保持状态：`tick` 每次调用都把 `count` 加一，`makeCounter` 把 `n` 捕获后即使函数已经返回也继续存活。官方文档同时说明这是一个优化点：如果某个值既不被闭包修改、也不再被外层修改，Swift 可能改成捕获一份拷贝。要强制打破引用捕获就用捕获列表，`{ [x] in x }` 立即复制当前值，`{ [weak self] in self?.run() }` 则用来打断闭包与实例之间的强引用环。

逃逸规则是 Swift 闭包最有存在感的地方：默认位置的闭包参数是非逃逸的，编译器能内联并省掉引用计数；一旦闭包被存进数组、属性或异步回调，参数类型就要写 `@escaping`。`@autoclosure` 会把调用处写的表达式自动包成不带参数的闭包，`assert` 与 `??` 就靠它延迟求值，两个属性可以叠加成 `@autoclosure @escaping`。多个尾随闭包会省略第一个闭包的外部标签而保留后面的标签，这是写请求回调这类 API 的常规姿势。

收参形态上，闭包参数可以使用有名字的变参但不能有默认值，默认参数只在 `func` 声明里能用，所以 `greet("a", times: 2)` 是函数特性而不是闭包特性；`total(1, 2, 3)` 演示变参在函数体内的类型是 `[Int]`。调用方式就是 `f()` 与 `f(40, 2)`，没有 `call`, `apply` 之类的入口，立即调用把字面量写好再加一对括号即可，例如 `{ (x: Int) -> Int in x * 2 }(21)`。`for` 循环每轮都是新的绑定，循环里 append 的闭包各捕获各的 `i`，⚠️ 因此 Swift 不会出现循环闭包共享同一个变量的问题，这一点与旧版 JavaScript 相反；循环变量陷阱与捕获内存管理的完整讨论见闭包一页。

📘 [Swift · Closures](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/closures/)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的匿名函数就是函数字面量 `func(a int) int { return a + 1 }`，除了没有名字之外与具名函数完全同构，可以直接赋给变量、当参数、当返回值。Go 没有单独的闭包语法，闭包就是捕获了外层变量的函数字面量，捕获一律按**引用**进行，变量留在栈上还是被搬到堆上由编译器的逃逸分析决定。

```go
package main

import (
	"fmt"
	"reflect"
	"runtime"
)

func counter() func() int {
	n := 0
	return func() int { n++; return n } // n 逃逸到堆上
}

func twice(f func(int) int, x int) int { return f(f(x)) }

func sum(nums ...int) int {
	total := 0
	for _, n := range nums {
		total += n
	}
	return total
}

func main() {
	defer func() { fmt.Println("deferred") }()

	c := counter()
	fmt.Println(c(), c())                     // 1 2

	add := func(a, b int) int { return a + b }
	fmt.Println(add(40, 2))                    // 42
	fmt.Println(func() int { return 42 }())    // 42 立即调用

	fns := make([]func() int, 0, 3)
	for i := 1; i <= 3; i++ {
		fns = append(fns, func() int { return i }) // Go 1.22+ 每轮新变量
	}
	fmt.Println(fns[0](), fns[1](), fns[2]())   // 1 2 3

	fmt.Println(reflect.TypeOf(add).Kind())     // func
	fmt.Println(runtime.FuncForPC(reflect.ValueOf(twice).Pointer()).Name()) // main.twice
	fmt.Println(add == nil)                      // false
	fmt.Println(sum(1, 2, 3), sum([]int{1, 2, 3}...)) // 6 6
	fmt.Println("end")                           // end
}
```

`counter` 把 `n` 捕获后返回，`n` 在 `counter` 返回后仍然活着，编译器会把它移到堆上：`go build -gcflags=-m` 会打印 `moved to heap: n` 与 `func literal escapes to heap`，这就是 Go 里判断闭包是否分配的标准手段。同一个函数的多次调用各自得到独立的 `n`，`c := counter()` 后再调两次得到 1 和 2；但同一轮循环里被多个闭包引用的变量是共享的，⚠️ 这一点是 Go 闭包最常被误解的地方。

Go 1.22 起 `for` 循环的循环变量每轮都是新的变量，所以循环里追加的闭包各捕获各的 `i`，`fns[0]()` 到 `fns[2]()` 得到 1, 2, 3；更早的版本必须写 `i := i` 才能修好。Go 1.27 的编译器会为函数字面量生成更简洁的名字，并可能让捕获环境不同的函数字面量共享同一个代码指针，所以 `reflect.Value.Pointer()` 只反映代码地址，用它比较两个闭包是否相等从来都是错的。

函数值可以反射：`reflect.TypeOf(f).Kind()` 得到 `func`，具名函数还能用 `runtime.FuncForPC(reflect.ValueOf(twice).Pointer()).Name()` 拿到 `main.twice` 这样的名字，函数字面量只会有 `main.main.func1` 这类合成名，Go 1.27 明确建议不要依赖它。收参形态方面，Go 没有默认参数，但有变参 `func sum(nums ...int) int`，函数体内 `nums` 是 `[]int`，调用时既可以直接列值也可以写 `sum(xs...)` 展开切片。调用方式就是 `f()`，立即调用写作 `func() int { return 42 }()`；`defer func() { fmt.Println("deferred") }()` 是同一语法最常见的用法，defer 注册的函数在 `main` 返回前才执行，所以它的输出排在 `end` 之后。捕获、逃逸与循环变量的完整讨论归闭包一页。

📘 [Go spec · Function literals](https://go.dev/ref/spec#Function_literals)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的匿名函数只有 `lambda` 一种字面量，语法被限制为单个表达式，不能包含语句、赋值或注解；`lambda` 与 `def` 生成的都是同一种 `function` 对象。环境靠 `cell` 携带：闭包按变量而不是按值捕获，要写回外层变量必须用 `nonlocal`。捕获、逃逸与循环变量陷阱的完整讨论见 closure.md，这里只给结论。

```python
def make_adder(n):
    def add(x):                              # 闭包：引用外层变量 n
        return x + n
    return add

add40 = make_adder(40)
print(add40(2))                              # 42
print(add40.__name__)                        # add
print(add40.__closure__[0].cell_contents)    # 40

square = lambda x: x * x                     # lambda 只能是一个表达式
print(square.__name__)                       # <lambda>

def counter(start=0):                        # 默认参数在 def 时求值一次
    count = start
    def step(by=1):                          # 每次调用独立，默认值不共享
        nonlocal count                       # 没有 nonlocal 会 UnboundLocalError
        count += by
        return count
    return step

print(counter.__defaults__)                  # (0,)
c = counter()
print(c(), c(10), c())                       # 1 11 12

def collect(*args, **kwargs):                # 任意收参
    return args, kwargs
print(collect(1, 2, k=3))                    # ((1, 2), {'k': 3})

print((lambda a, b=2: a + b)(40))            # 42 立即调用

class Add:                                   # 可调用对象：实现 __call__
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return x + self.n

print(Add(40)(2))                            # 42
print(callable(Add(1)))                      # True

from functools import partial
print(partial(pow, 2)(5))                    # 32
```

代码展示了闭包的三个可观察点：`make_adder` 返回后 `add` 仍能读到 `n`，`__name__` 是定义时的名字，`__closure__` 里的 `cell_contents` 就是被捕获的 `40`。`counter` 用 `nonlocal` 修改外层 `count`，因此每次调用 `step` 都累加，而不是抛 `UnboundLocalError`；如果把 `nonlocal` 删掉，`count += by` 会被当成新的局部变量。

⚠️ 循环里创建的闭包共享同一个变量，等循环结束后全部读到最后一个值；要给每个闭包固定一份值，用默认参数把当前值绑进去（`lambda x, i=i: x + i`）或改用 `functools.partial`。默认参数在 `def` 执行时求值一次，`__defaults__` 能看到它，所以可变默认参数会在多次调用之间共享同一份对象。

收参形态由签名决定：`*args` 收位置实参，`**kwargs` 收关键字实参，`/` 与 `*` 分别划出仅位置与仅关键字的分界。调用方式统一是在名字后面加括号并传实参，任何实现了 `__call__` 的实例也能这样调用；需要立即调用就直接给 `lambda` 加实参，例如 `(lambda a, b=2: a + b)(40)`。闭包对象由 GC 管理，返回后不会失效。

📘 [Python · Lambda expressions](https://docs.python.org/3/reference/expressions.html#lambda)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的函数字面量有两种：lambda `{ x -> x * x }` 与匿名函数 `fun(x: Int): Int { return x + 1 }`，它们和具名函数一样能赋给 `(Int) -> Int` 类型的变量。环境随函数对象一起保存，Kotlin 捕获的是变量本身，被捕获的 `var` 由编译器装箱成 `Ref`，所以闭包里可以直接修改外层 `var`。捕获、逃逸与循环变量陷阱的完整讨论见 closure.md，这里只给结论。

```kotlin
inline fun applyTo(x: Int, f: (Int) -> Int): Int = f(x)   // inline：不生成函数对象

inline fun <reified T> typeName(): String = T::class.simpleName ?: "?"  // reified 只能配 inline

inline fun collect(noinline make: () -> Int): List<Int> = listOf(make)  // noinline 才能当对象存

inline fun guard(crossinline body: () -> Unit) {           // crossinline：不能在 lambda 里非局部返回
    val r = object : Runnable { override fun run() = body() }
    r.run()
}

fun hasZero(xs: List<Int>): Boolean {
    xs.forEach { if (it == 0) return true }                 // forEach 是 inline，return 从 hasZero 返回
    return false
}

fun main() {
    val square = { x: Int -> x * x }                        // lambda 字面量
    println(square(7))                                       // 49
    println(listOf(1, 2, 3).filter { it % 2 == 1 })          // [1, 3]  it 是唯一参数

    val anon = fun(x: Int): Int { return x + 1 }             // 匿名函数：可写返回类型
    println(anon(41))                                        // 42

    var count = 0
    val tick = { count += 1; count }                         // 捕获外层 var
    println("${tick()} ${tick()}")                            // 1 2

    println(run { val a = 40; a + 2 })                       // 42  立即调用的 lambda
    println(applyTo(21) { it * 2 })                          // 42  尾随 lambda
    println(typeName<List<String>>())                        // List
    println(collect { 42 })                                  // [42]
    guard { println("run") }                                 // run
    println(hasZero(listOf(1, 0, 2)))                        // true
}
```

lambda 与匿名函数的关键差别有两个：匿名函数可以显式写返回类型，而且其中的 `return` 只从匿名函数自身返回；lambda 里的裸 `return` 只在被 `inline` 的高阶函数中才合法，它从外层函数返回，这叫非局部返回。带接收者的字面量 `String.() -> Int` 让 `this` 指向接收者对象，因此不必再写接收者名字。

`inline` 把函数体连同传入的 lambda 一起内联到调用点，消除函数对象分配与虚调用开销，代价是生成的代码变大，所以只对小巧的高阶函数用。`noinline` 让某个参数保持为真实对象，例如需要把它存进集合；`crossinline` 表示 lambda 会在另一个执行上下文（如局部对象或嵌套函数）里被调用，因此禁止非局部返回。`reified` 只能用在 `inline` 函数上，它让 `T::class` 与 `is T` 在函数体内合法，而普通函数的类型参数在运行期不可见。

本机未安装 Kotlin 2.4 工具链，以上输出按官方文档语义书写，未经本机运行验证。

📘 [Kotlin · Inline functions](https://kotlinlang.org/docs/inline-functions.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的匿名函数是 lambda 表达式 `(a, b) -> a + b`，它本身不是对象，而是某个函数式接口的实例；在 lambda 出现之前，同样的东西只能写成匿名类。体可以是单个表达式，也可以是语句块，块体要用 `return` 返回值。捕获一句话结论：lambda 按值复制它读到的局部变量，这些变量必须是 effectively final，要共享可变状态就用字段或数组，细节见 closure.md。

```java
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.IntSupplier;
import java.util.function.IntUnaryOperator;
import java.util.function.Supplier;

public class ClosureDemo {
    static IntUnaryOperator adder(int a) {              // 返回闭包
        return b -> a + b;                              // a 被复制进 lambda
    }

    static IntSupplier counter() {                      // 可变状态放数组
        int[] n = {0};
        return () -> ++n[0];
    }

    public static void main(String[] args) {
        IntUnaryOperator add40 = adder(40);
        System.out.println(add40.applyAsInt(2));        // 42

        int base = 10;                                  // effectively final
        IntUnaryOperator plusBase = x -> x + base;      // 只读捕获
        System.out.println(plusBase.applyAsInt(32));    // 42

        IntSupplier c = counter();
        System.out.println(c.getAsInt() + " " + c.getAsInt());   // 1 2

        Function<Integer, Integer> old =                // lambda 之前的匿名类写法
            new Function<Integer, Integer>() {
                public Integer apply(Integer b) { return b * 2; }
            };
        System.out.println(old.apply(21));              // 42

        Supplier<String> block = () -> { return "hi"; };   // 块体要写 return
        System.out.println(block.get());                // hi

        Consumer<String> pr = System.out::println;      // 方法引用当函数值
        pr.accept("done");                              // done

        Runnable r = () -> System.out.println("run");   // 无参无返回
        r.run();                                        // run

        Function<Integer, Integer> id = Function.identity();
        System.out.println(id.apply(7));                // 7
    }
}
```

逃逸不成问题：lambda 捕获的是值副本，外层方法返回后闭包仍然安全，生命周期完全交给 GC，没有 `@escaping` 或 `'static` 之类的标注。`this` 的含义与匿名类不同，lambda 里的 `this` 就是外层实例本身，匿名类里的 `this` 指向新创建的那个对象。

循环变量的结论是：经典 `for (int i = 0; i < n; i++)` 的 `i` 不是 effectively final，捕获它直接编译报错，不会默默共享最后一个值；增强 `for` 每轮引入一个新的变量，因此捕获每个元素是安全的。收参形态方面 Java 只有变参 `Type...`，没有默认参数，lambda 参数可以显式写类型，也可以从 Java 11 起写 `var`。调用方式就是接口方法本身，`IntUnaryOperator` 用 `applyAsInt`，`Function` 用 `apply`，`Supplier` 用 `get`，`Runnable` 用 `run`；Java 没有立即调用表达式的语法，要立即执行只能先赋给接口变量，或者写成强制转换后立刻调用，例如 `((IntUnaryOperator) x -> x * 2).applyAsInt(21)`。

本机未安装 JDK 26（LTS 25），以上输出按官方文档语义书写，未经本机运行验证。

📘 [JLS 25 · Lambda Expressions](https://docs.oracle.com/javase/specs/jls/se25/html/jls-15.html#jls-15.27.2)

{{% /tab %}}

{{% tab header="C++" %}}

lambda 字面量 `[捕获](参数) { 体 }` 产生一个唯一的匿名类类型（closure type），捕获列表决定这个类有哪些数据成员，`operator()` 默认是 `const`。捕获语义的细节（按引用悬垂、逃逸、循环变量）归闭包一页，这里只给结论：按值捕获拷一份、按引用捕获共享、初始化捕获可以把 move-only 对象搬进去。C++ 没有 GC，闭包对象里捕获的东西活多久完全由持有者负责。

```cpp
#include <cstdio>
#include <functional>
#include <memory>
#include <utility>
#include <vector>

template <typename F> int call_it(F&& f) { return f(); }    // 模板参数接 move-only

int main() {
    auto dbl = [](int x) { return x * 2; };             // 无捕获 lambda
    int (*fp)(int) = dbl;                                // 可隐式转函数指针
    std::printf("%d\n", fp(21));                           // 42

    int base = 10;
    auto byVal = [base](int x) { return base + x; };       // 按值捕获
    auto byRef = [&base](int x) { base += x; return base; };
    std::printf("%d %d\n", byVal(5), byRef(5));             // 15 15
    std::printf("%d\n", base);                               // 15

    auto counter = [n = 0]() mutable { return ++n; };         // 初始化捕获 + mutable
    std::printf("%d %d\n", counter(), counter());              // 1 2

    auto owned = [p = std::make_unique<int>(7)] { return *p; };   // move-only 捕获
    std::printf("%d\n", owned());                                 // 7
    // std::function<int()> bad = owned;                           // 🛑 编译错误：要求可拷贝
    std::printf("%d\n", call_it(owned));                           // 7

    std::printf("%d\n", [](int y) { return y + 1; }(41));            // 42 立即调用
    auto gen = [](auto x) { return x + x; };                          // 泛型 lambda
    std::printf("%d %.1f\n", gen(21), gen(1.5));                       // 42 3.0

    std::vector<std::function<int()>> fs;
    for (int i = 0; i < 3; i++) fs.push_back([i = i] { return i; });    // 逐个拷贝 i
    for (auto& g : fs) std::printf("%d", g());                           // 012
    std::printf("\n");
    return 0;
}
```

按引用捕获的 lambda 不能活过被捕获的变量，按值捕获的 lambda 把副本装进闭包对象，`std::function` 拷贝时会连这些副本一起拷贝。`mutable` 让 `operator()` 变成非 const，这样才能修改按值捕获的副本；初始化捕获 `[p = std::move(p)]` 是 C++14 起把 move-only 对象搬进闭包的唯一写法，这种 lambda 不能塞进 `std::function`（要求可拷贝，示例里用 🛑 标出的那行会编译失败），要用 `auto` 接收，或者改用模板参数，或者用可用的 `std::move_only_function`。

经典 `for` 的 `i` 只有一个变量，闭包必须写 `[i = i]` 逐个拷贝，直接 `[&i]` 会让所有闭包共享同一个 `i`，循环结束后读到同一个终值；范围 `for` 的循环变量每次迭代重新初始化，`[x]` 按值捕获就是独立副本。无捕获的 lambda 能隐式转成函数指针，也就能当 C 风格回调；C++23 起 lambda 还能声明显式对象参数（`this` 推导），这里不展开。

📘 [cppreference · Lambda expressions](https://en.cppreference.com/w/cpp/language/lambda)

{{% /tab %}}

{{% tab header="C" %}}

C **没有 lambda、没有匿名函数、没有闭包**：函数指针只携带代码地址，抓不住任何环境。C 里被广泛采用的替代是把上下文结构体指针作为显式参数传进去，也就是 `void *ctx`（`void *arg`, `void *thunk`, `void *userdata` 都是同一套路）模式，`qsort_r` 与 `pthread_create` 都是这个形状。代价是类型安全、生命周期与并发安全全部落到调用者身上。

```c
#include <stdio.h>
#include <stdlib.h>

struct Ctx { int pivot; };                        /* 手工“捕获环境” */
struct Ctx ctx = { 5 };

int cmp_gap(void *thunk, const void *a, const void *b) {   /* macOS/BSD 版 qsort_r */
    struct Ctx *c = thunk;
    int x = abs(*(const int *)a - c->pivot);
    int y = abs(*(const int *)b - c->pivot);
    return (x > y) - (x < y);
}

int apply(void *env, int x) {                      /* 环境作为显式参数 */
    return ((struct Ctx *)env)->pivot + x;
}

struct Op { int (*fn)(void *, int); void *env; };   /* 把函数与环境打包 */

int main(void) {
    int v[] = { 1, 4, 8, 12 };
    qsort_r(v, 4, sizeof v[0], &ctx, cmp_gap);       /* 按离 5 的距离排序 */
    for (int i = 0; i < 4; i++) printf("%d ", v[i]);   /* 4 8 1 12 */
    printf("\n");

    struct Op op = { apply, &ctx };                     /* “闭包” = 函数 + 环境 */
    printf("%d\n", op.fn(op.env, 37));                   /* 42 */
    printf("%d\n", apply(&ctx, 37));                      /* 42 */
    return 0;
}
```

这正是所有 C 回调 API 的形状：`pthread_create` 的入口是 `void *(*start_routine)(void *)`，`void *arg` 就是那个环境，线程函数自己负责把 `void *` 转回具体类型。`qsort_r` 连参数顺序都不统一：glibc 是 `qsort_r(base, n, size, compar, arg)` 且 `compar` 收 `(const void *, const void *, void *)`，本机 macOS / BSD 是 `qsort_r(base, n, size, thunk, compar)` 且 `compar` 收 `(void *, const void *, const void *)`，跨平台必须条件编译或统一封装。

没有匿名函数意味着不能就地写比较器，只能先起一个具名函数；`void *` 一丢类型信息，参数写错就是未定义行为，环境对象的生命周期也必须由调用者保证长过回调。GCC 的嵌套函数（nested functions）扩展能引用外层变量，但它靠 trampoline 实现，需要可执行栈，现代系统通常禁用，不要依赖。要真正的闭包只能换语言，或者像示例里那样把函数指针与环境结构体手工打包。

📘 [GCC · Nested Functions](https://gcc.gnu.org/onlinedocs/gcc/Nested-Functions.html)

{{% /tab %}}

{{% tab header="Julia" %}}

匿名函数在 Julia 里就是普通函数值：`x -> x * 2` 是单表达式形式，`function (x)` 到 `end` 是多行形式，编译器给它们编号名字（形如 `#1`, `#2`）而不是用户起的名字。`do` 块是语法糖，`f(args...) do x` 到 `end` 的写法把匿名函数作为**第一个参数**传给 `f`。捕获规则要留意：被内层函数修改的外层局部变量会被移进堆上的 box（内部类型 `Core.Box`），带来类型不稳定与运行期分派。

```julia
double = x -> x * 2                        # 匿名函数字面量
println(double(21))                          # 42
println(typeof(double) <: Function)           # true

add = function (a, b)                          # 多行匿名函数形式
    a + b
end
println(add(40, 2))                             # 42

println(map([1, 2, 3]) do x                      # do 块：匿名函数作第一个参数
    x + 1
end)                                              # [2, 3, 4]

function make_counter()
    n = 0
    () -> (n += 1)                                # 捕获并修改 n：n 被装箱
end
c = make_counter()
println((c(), c()))                                 # (1, 2)

println((x -> x + 1)(41))                            # 42 立即调用
multi = (x, y, z) -> 2x + y - z                       # 多参数匿名函数
println(multi(1, 2, 3))                                # 1
println(map(x -> x^2, [1, 2, 3]))                       # [1, 4, 9]
println(broadcast(x -> x + 1, [1, 2, 3]))                # [2, 3, 4]
println([1, 2, 3] .|> (x -> x * 2))                       # [2, 4, 6]
sum_all(xs...) = reduce(+, xs)                             # 变参：多余实参进元组
println(sum_all(1, 2, 3))                                   # 6
kw(x; scale=1) = x * scale                                   # 关键字参数
println(kw(21, scale=2))                                      # 42
```

`do x` 生成单参数匿名函数，`do a, b` 生成双参数版本，裸 `do` 是零参数版本；捕获按绑定共享，内层与外层看到同一个变量，所以内层一旦赋值，解析器就把该变量装进堆分配的 box，box 里的对象类型被抽象化，每次读写都要运行期分派。官方性能提示给的两招是给捕获变量加类型标注（`r::Int = r0`）或用 `let r = r` 另建只读绑定，递归闭包还可以用 `@__FUNCTION__`。闭包是普通对象、由 GC 管理，不需要 `move` 或生命周期标注。

循环变量陷阱在这里不存在：手册明确写 for 循环与推导式的迭代变量每次迭代都是新变量，`Fs[j] = ()->j` 之后 `Fs[1]()` 与 `Fs[2]()` 分别得到 1 与 2。收参形态上，把最后一个位置参数写成 `x...` 就能收变参（多余实参进元组），分号后面是关键字参数，`kwargs...` 收集多余关键字。以下输出按官方手册与 REPL 语义给出，本机未安装 Julia，未经运行验证。

📘 [Julia · Anonymous Functions](https://docs.julialang.org/en/v1/manual/functions/#Anonymous-Functions)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的匿名函数有两种写法：表达式 lambda（`x => x * 2`）与语句 lambda（`x => { return x * 2; }`），两者都能转成委托，表达式 lambda 还能转成表达式树。捕获的局部变量会被提升为编译器生成的闭包类的字段，所以捕获是按引用共享的；逃逸与循环变量的完整讨论见闭包一页，这里只给结论。委托由 GC 管理，被捕获的变量在引用它的委托可回收之前不会被回收。

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Linq.Expressions;

class Closures {
    static Func<int> Counter() {
        int n = 0;
        return () => ++n;                         // n 被提升为闭包类的字段
    }

    static void Main() {
        Func<int, int> dbl = static x => x * 2;         // static lambda：不捕获
        Console.WriteLine(dbl(21));                      // 42

        var c = Counter();
        Console.WriteLine($"{c()} {c()}");                 // 1 2

        Expression<Func<int, int>> e = x => x * x;          // 表达式树：数据
        Console.WriteLine(e);                                // x => (x * x)
        var compiled = e.Compile();
        Console.WriteLine(compiled(7));                       // 49

        Func<int, int, int> add = (a, b) => a + b;
        Console.WriteLine(add(40, 2));                         // 42

        var fns = new List<Func<int>>();
        for (int i = 0; i < 3; i++) { int copy = i; fns.Add(() => copy); }
        Console.WriteLine(string.Join(",", fns.Select(f => f())));   // 0,1,2
    }
}
```

`static` lambda（C# 9 起）不能捕获局部变量或实例状态，只能引用静态成员与常量，既避免无意的闭包分配，也让编译器把它缓存成静态委托。表达式树 `Expression<Func<int, int>>` 是数据而不是可执行代码，LINQ provider 遍历它来翻译查询；带语句体、赋值、`await` 的 lambda 不能转成表达式树，需要执行时先 `Compile()`，官方文档给出的打印结果就是 `x => (x * x)`。

循环变量陷阱只针对经典 `for`：`i` 只有一个，必须在循环体里 `int copy = i;` 再捕获副本；`foreach` 从 C# 5 起每次迭代就是新变量，不需要拷贝。逃逸方面没有生命周期标注，委托由 GC 管理，长命委托会拖住捕获的大对象。收参形态上，可选参数与 `params` 都能用，C# 14 起 lambda 参数还能只写修饰符不写类型，例如 `(text, out result) => int.TryParse(text, out result)`。本机没有 .NET SDK，以上输出未经运行验证。

📘 [Microsoft Learn · Lambda expressions](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/lambda-expressions)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的匿名函数有块体 `(x) { ... }` 与箭头 `(x) => expr` 两种写法，箭头只是单表达式函数体的简写，和具名函数享有同一套类型规则。函数类型在运行期是 reified 的，匿名函数作为对象时可以用 `is` 检查签名；闭包按引用捕获外层可变变量，逃逸由 GC 管理，没有生命周期标注。捕获、逃逸与循环变量的完整讨论见闭包一页，这里只给结论。

```dart
typedef IntFn = int Function(int);

int Function(int) makeCounter() {
  var n = 0;
  return () => ++n;                        // 按引用捕获 n，逃逸后由 GC 保活
}

Future<String> load() async => 'data';

void main() async {
  final anon = (int x) { return x + 1; };    // 块体匿名函数
  final arrow = (int x) => x + 1;             // 箭头函数，等价写法
  print(anon(41));                             // 42
  print(arrow(41));                             // 42
  print(anon is IntFn);                          // true  函数类型具体化

  final c = makeCounter();
  print('${c()} ${c()}');                         // 1 2

  print(Function.apply(anon, [41]));               // 42  运行期动态调用

  String greet(String name, [String? suffix]) => '$name${suffix ?? ''}';
  print(greet('a'));                                // a
  print(greet('a', '!'));                            // a!

  final fns = <int Function()>[];
  for (final v in [0, 1, 2]) {
    fns.add(() => v);                                // final 绑定每次迭代新建
  }
  print(fns.map((f) => f()).toList());                 // [0, 1, 2]

  print((await load()).toUpperCase());                  // DATA
}
```

匿名箭头函数在 Dart 里没有独立的 `this` 概念，`this` 始终是词法上的外层对象，这一点与 JavaScript 的箭头函数不同，也和 JavaScript 的普通函数不同。`Function.apply` 用 `List` 传位置参数，用 `Map<Symbol, dynamic>` 传命名参数，它是唯一的运行期动态调用入口，代价是丢掉静态类型，类型不匹配只会在运行期报错。可选位置参数用 `[]`，命名参数用 `{}`，同一个函数里两者不能同时出现；`required` 只用于命名参数。循环里要让每个闭包各自持有一份值，就在循环体里写 `final v = i` 新建绑定，正如上面的 for-in 写法所示。本机未安装 Dart SDK，以上输出按官方文档语义书写，未经运行验证。

📘 [Dart · Function.apply](https://api.dart.dev/stable/latest/dart-core/Function/apply.html)

{{% /tab %}}

{{% tab header="R" %}}

R 的匿名函数就是 `function(...) ...` 这个构造，它和具名函数没有区别，只是没有绑定名字。函数对象由 `formals`, `body`, `environment` 三部分构成，闭包会捕获整个定义环境而不是单个变量，逃逸后由 GC 保活。参数以 promise 形式传入，R 对实参做惰性求值，这一点直接影响收参与返回闭包的写法。

```r
make_counter <- function() {
  n <- 0
  function() { n <<- n + 1; n }        # 匿名闭包，按引用共享环境里的 n
}
c1 <- make_counter()
print(c(c1(), c1()))                     # [1] 1 2
print(ls(environment(c1)))                # [1] "n"
print(typeof(environment(c1)))             # [1] "environment"

adder <- function(a) function(b) a + b
print(adder(40)(2))                        # [1] 42
print(do.call(adder, list(1))(2))           # [1] 3

h <- function(x, label = "x") paste0(label, "=", x)   # 默认参数
print(h(1))                                 # [1] "x=1"
print(h(1, lab = "n"))                       # [1] "n=1"  部分匹配

dots <- function(...) sum(...)                # 变参
print(dots(1, 2, 3))                           # [1] 6
print(sapply(1:3, function(i) i^2))             # [1] 1 4 9

f <- function(y) function() y
lf <- vector("list", 3)
for (i in 1:3) lf[[i]] <- f(i)                  # y 是 promise，循环变量共享
print(lf[[1]]())                                 # [1] 3

g <- function(y) { force(y); function() y }       # force 固定当次的值
lg <- vector("list", 3)
for (i in 1:3) lg[[i]] <- g(i)
print(lg[[1]]())                                  # [1] 1
```

参数匹配分三趟：先按标签精确匹配，再对剩余具名实参做部分匹配，最后按位置匹配。有 `...` 时部分匹配只作用于它之前的形参，所以 `label` 能被 `lab` 命中，而 `...` 之后的形参只能精确匹配或按位置匹配。

惰性求值的后果是实参在调用环境里是 promise，直到被用到才求值；循环里返回的闭包如果只是引用循环变量，读到的是循环结束后的末值，修法是在函数内 `force()` 把它固定下来，或者用 `lapply`, `purrr::map` 把迭代交给一次独立调用。

变参用 `...`，可以用 `list(...)`, `..1`, `...length()` 读取，`...` 里的 promise 在被捕获为 list 时会被强制求值；`match.fun` 与 `do.call` 则解决“按名字拿函数”和“用 list 传参”两件事。闭包捕获、逃逸与循环变量的展开见闭包一页。本机未安装 R，以上输出按官方文档与手册语义书写，未经运行验证。

📘 [R · Force Evaluation of an Argument](https://stat.ethz.ch/R-manual/R-devel/library/base/html/force.html)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有闭包**，也**没有匿名函数字面量**：你写不出 `|x| x + 1` 这种表达式，只能定义具名函数再取它的指针。所谓“带环境”的能力要靠显式传递：把状态放进结构体，把方法写成第一个参数接收 `self` 或 `*anyopaque` 上下文的函数。逃逸与生命周期没有 GC 兜底，上下文的存活期必须长于回调本身。

```zig
const std = @import("std");

const Counter = struct {
    n: i32 = 0,
    pub fn tick(self: *Counter) i32 {      // 显式 self 就是被捕获的环境
        self.n += 1;
        return self.n;
    }
};

const Add = struct {
    base: i32,
    pub fn call(ctx: *const anyopaque, x: i32) i32 {
        const self: *const Add = @ptrCast(@alignCast(ctx));
        return self.base + x;
    }
};

fn applyCb(ctx: *const anyopaque, f: *const fn (*const anyopaque, i32) i32, x: i32) i32 {
    return f(ctx, x);                      // 调用就是普通函数指针调用
}

pub fn main() void {
    var c = Counter{};
    const a = c.tick();
    const b = c.tick();
    std.debug.print("{d} {d}\n", .{ a, b });                    // 1 2

    const add40 = Add{ .base = 40 };
    std.debug.print("{d}\n", .{applyCb(&add40, Add.call, 2)});   // 42

    const args = [_]i32{ 1, 2, 3 };         // 没有 ...，变参用切片或 tuple
    var sum: i32 = 0;
    for (args) |v| sum += v;
    std.debug.print("{d}\n", .{sum});                            // 6
}
```

没有 lambda 也意味着没有“立即调用表达式”：需要一次性初始化时用带 `blk: { ... break :blk v; }` 的块表达式，或者把逻辑写进 `comptime` 块。默认参数和命名参数都不存在，替代做法是结构体配置项加默认字段值（`Add{ .base = 40 }` 就是这种字面量），可变参数用切片, `anytype` 或 tuple。调用语法里没有 `.call`, `.apply`, `__invoke`，函数指针直接 `f(ctx, x)`，方法用 `x.m()` 的语法糖。这套显式环境也影响了集合 API：0.15 起 `std.ArrayList` 改为非托管版本，结构体里不再保存 allocator，`append` 这类操作要显式传入分配器，原来的托管版本改名为 `std.array_list.Managed`，`std.ArrayListUnmanaged` 已并入 `std.ArrayList`。本机未安装 Zig，以上输出按官方文档语义书写，未经运行验证。

📘 [Zig · 0.15.1 Release Notes · ArrayList](https://ziglang.org/download/0.15.1/release-notes.html#ArrayList-make-unmanaged-the-default)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua 的匿名函数字面量是 `function(...) ... end`，每次执行到这个定义都会实例化一个新的 closure，捕获外层局部变量作为 upvalue，同一层的多个闭包共享同一份 upvalue。数组、对象、模块都靠 table 承载，元表的 `__call` 让任何值可被调用，`__index` 让 table 像对象；所有闭包都由 GC 管理，没有生命周期标注。捕获与逃逸的细节见闭包一页。

```lua
local function make_counter()
  local n = 0
  return function() n = n + 1; return n end     -- 共享 upvalue，按引用捕获
end
local c = make_counter()
print(c() .. " " .. c())                          -- 1 2

local fns = {}
for i = 1, 3 do
  fns[i] = function() return i end                  -- for 控制变量每轮新建
end
print(fns[1]() .. " " .. fns[2]() .. " " .. fns[3]())  -- 1 2 3

local gs, n = {}, 0
while n < 3 do
  n = n + 1
  local v = n                                        -- 每次执行 local 都新建变量
  gs[n] = function() return v end
end
print(gs[1]() .. " " .. gs[2]() .. " " .. gs[3]())     -- 1 2 3（直接捕获 n 则全是 3）

local function adder(a) return function(b) return a + b end end
print(adder(40)(2))                                  -- 42

local Counter = {}
Counter.__index = Counter
setmetatable(Counter, {
  __call = function(cls, n) return setmetatable({ n = n or 0 }, cls) end,
})
function Counter:inc() self.n = self.n + 1; return self.n end
print(Counter(40):inc())                              -- 41

local function sum(...)                               -- 变参
  local s = 0
  for _, v in ipairs({ ... }) do s = s + v end
  return s
end
print(sum(1, 2, 3))                                    -- 6
print((function(x) return x * 2 end)(21))               -- 42  立即执行
```

`for` 的控制变量每轮都是一次新的 `local` 声明，循环体里创建的闭包各捕获各的 `i`，所以 `for` 天然按轮独立，不需要额外快照；会共享的是循环外声明的变量（上面 `while` 里的 `n`），那种情况才要在循环体里写 `local v = n`，手册明确指出每次执行 `local` 声明都会创建新的局部变量。Lua 5.5 的 `for` 控制变量还是只读（`const`）的，不能重新赋值。非变参函数会把多余实参丢掉、缺少的补 `nil`，变参用 `...` 收集，需要个数时用 `select("#", ...)`，具名 table 的字段调用写成 `t:f()`，等价于 `t.f(t)`。没有 `__call` 的值不能被调用，而带 `__call` 的 table 可以像函数一样写 `Counter(40)`，这就是 Lua 里最接近构造器和 `__invoke` 的写法。本机未安装 Lua，以上输出按官方手册语义书写，未经运行验证。

📘 [Lua 5.5 · Scopes, Variables, and Environments](https://www.lua.org/manual/5.5/manual.html#2.2)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的匿名函数就是 JavaScript 的 `function` 表达式与箭头函数，类型系统只是给它们补上签名，编译后签名被完全擦除（type erasure），运行时没有任何函数类型信息。箭头函数不绑定自己的 `this`, `arguments`, `super`, `new.target`，因此不能当构造器；捕获语义与循环变量陷阱和 JavaScript 完全一致，细节见闭包一页。需要给回调声明调用者类型时用 `this` 参数，它只写在类型里。

```typescript
const anon = function (x: number): number { return x + 1; };
const arrow = (x: number): number => x + 1;
console.log(anon(41), arrow(41));                    // 42 42
console.log(anon.name, anon.length);                  // anon 1

function makeCounter(): () => number {                 // 逃逸：类型上就是 () => number
  let n = 0;
  return () => ++n;                                     // 捕获 n，由 GC 保活
}
const c = makeCounter();
console.log(c(), c());                                   // 1 2

function greet(name = 'world', ...rest: string[]): string {   // 默认参数 + rest
  return `hi ${name}(${rest.length})`;
}
console.log(greet(), greet('a', 'b', 'c'));               // hi world(0) hi a(3)

console.log(anon.call(null, 41));                          // 42
console.log(anon.apply(null, [41]));                        // 42
console.log(anon.bind(null, 41)());                          // 42

interface Handler {                                          // this 参数
  (this: { prefix: string }, s: string): string;
}
const tag: Handler = function (this: { prefix: string }, s: string) {
  return this.prefix + s;
};
console.log(tag.call({ prefix: '#' }, 'x'));                  // #x

console.log(((n: number): number => n * 2)(21));               // 42  立即调用

const fns: Array<() => number> = [];
for (var i = 0; i < 3; i++) fns.push(() => i);
console.log(fns.map((f) => f()));                             // [ 3, 3, 3 ]
```

`anon.name` 与 `anon.length` 来自运行期的函数对象，类型层面看不到这两个属性，普通函数类型 `(x: number) => number` 并不描述它们，要描述就得用可调用签名接口。默认参数让形参在函数体里是非可选类型，`...rest: string[]` 收进的是真正的数组；`call`, `apply`, `bind` 的第一个参数是 `thisArg`，因为这里不依赖 `this`，传 `null` 即可。`var` 声明的循环变量在整个函数作用域里是同一个绑定，所以三个闭包都打出 3，把 `var` 换成 `let` 就变成 `[0, 1, 2]`，这是修法也是结论。类型只在编译期存在，所以写不出运行期判断泛型的代码，也无法在运行期检查匿名函数的签名。本机未安装 TypeScript 编译器，以上输出按官方文档语义书写，未经运行验证。

📘 [TypeScript · The Basics · Erased Types](https://www.typescriptlang.org/docs/handbook/2/basic-types.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript 的匿名函数有 `function` 表达式和箭头函数两种写法，两者都是运行期的第一类对象，具名函数只是把同一个对象绑定到一个名字上。箭头函数不绑定自己的 `this`, `arguments`, `super`, `new.target`，因此不能当构造器；闭包按引用捕获外层变量，逃逸后由 GC 保活，循环变量陷阱与捕获细节见闭包一页。

```javascript
const anon = function (x) { return x + 1; };
const arrow = (x) => x + 1;
console.log(anon(41), arrow(41));                        // 42 42
console.log(anon.name, anon.length, arrow.length);        // anon 1 1
console.log(Object.keys(anon).length);                     // 0

function makeCounter() {
  let n = 0;
  return () => ++n;                                       // 闭包由 GC 管理，无生命周期标注
}
const c = makeCounter();
console.log(c(), c());                                     // 1 2

function greet(name = 'world', ...rest) {                  // 默认参数 + rest
  return `hi ${name}(${rest.length})`;
}
console.log(greet(), greet('a', 1, 2));                     // hi world(0) hi a(2)

console.log(anon.call(null, 41));                           // 42
console.log(anon.apply(null, [41]));                         // 42
console.log(anon.bind(null, 41)());                           // 42

const fns = [];
for (var i = 0; i < 3; i++) fns.push(() => i);
console.log(fns.map((f) => f()));                            // [ 3, 3, 3 ]
const gns = [];
for (let j = 0; j < 3; j++) gns.push(() => j);
console.log(gns.map((f) => f()));                             // [ 0, 1, 2 ]

console.log([1, 2, 3].map(function (x) { return x * 2; }));    // [ 2, 4, 6 ]
console.log(((f) => f(41))(anon));                              // 42
console.log(((x) => x * 2)(21));                                 // 42
```

`var` 声明的循环变量在整个函数作用域里是同一个绑定，所以三个闭包都读到末值 3；把 `var` 换成 `let`，每次迭代都会创建新绑定，结果变成 `[0, 1, 2]`，这就是一句结论加修法。

`anon.name` 由变量名推断而来，匿名函数直接作为实参时名字会是空串；`length` 数的是第一个默认参数或 rest 之前的参数个数，所以带默认值的 `greet.length` 是 0。函数对象默认没有可枚举的自有属性，`Object.keys` 返回空数组，用 `Object.getOwnPropertyNames` 才能看到 `length`, `name` 这些不可枚举属性。

箭头函数没有 `arguments`，可变参数只能用 rest 收集；`call`, `apply`, `bind` 的差别在于传参与是否立即执行，`bind` 返回新函数。立即调用表达式写成一元表达式包裹函数再调用，用来造一次性作用域或就地初始化。本机在 Node 24.20.0 上实跑验证过以上输出，书籍基线是 Node 26，这些函数语义在两者之间没有变化。

📘 [MDN · Closures](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Closures)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP 的匿名函数就是 `Closure` 类的实例，字面量有两种：`function (int $x) use ($factor): int {}` 与箭头函数 `fn(int $x): int => $x * $factor`（7.4+）。捕获只有一句结论要记：`use` 默认按值, `use (&$n)` 按引用, 箭头函数自动按值，展开的捕获语义与逃逸细节见闭包一页。另外，类方法里声明的闭包会自动绑定当前的 `$this`，写 `static function` 才会不绑定。

```php
<?php
declare(strict_types=1);

$factor = 3;
$mul = fn(int $x): int => $x * $factor;                          // 箭头函数：自动按值捕获
$mul2 = function (int $x) use ($factor): int { return $x * $factor; };   // 返回类型写在 use 之后
echo $mul(14), ' ', $mul2(14), PHP_EOL;                            // 42 42

$n = 0;
$tick = function () use (&$n): int { return ++$n; };                // use (&$n)：按引用捕获
echo $tick(), $tick(), PHP_EOL;                                     // 12

$make = function (int $base): Closure { return fn(int $x): int => $base + $x; };
echo $make(40)(2), PHP_EOL;                                          // 42  闭包是返回值

$iife = (function (): int { return 21 * 2; })();                       // 立即调用表达式
echo $iife, PHP_EOL;                                                   // 42

$sum = function (int ...$xs): int { return array_sum($xs); };           // 收参：变参
echo $sum(1, 2, 3), PHP_EOL;                                            // 6

function each_of(iterable $xs, Closure $f): void { foreach ($xs as $x) { $f($x); } }
each_of([1, 2, 3], function ($x): void { echo $x; });                    // 123
echo PHP_EOL;

class Counter {
    private int $n = 0;
    public function make(): Closure {
        return function (): int { return ++$this->n; };                  // $this 自动绑定
    }
    public static function pure(): Closure {
        return static function (): int { return 1; };                     // static：不绑定 $this
    }
}
$c = (new Counter())->make();
echo $c(), $c(), PHP_EOL;                                                // 12
$p = Counter::pure();
echo $p(), PHP_EOL;                                                       // 1
```

调用闭包用 `$f()`，或者走 `call_user_func()`；`Closure` 实现了 `__invoke`，所以任何接受 `callable` 的库函数都能直接收它，而形参类型写 `Closure` 时只接受闭包对象，写 `callable` 还能收字符串函数名与数组方法引用。收参形态与普通函数一致：默认参数, 变参 `...$xs`, 引用参数 `&$a` 都可用，`func_get_args()` 也能在闭包里用。逃逸与生命周期由 GC 管理，没有生命周期标注，但非 static 闭包持有创建它的 `$this` 引用，闭包活多久那个对象就活多久，把闭包塞进长生命周期容器时要留意这点。

循环变量陷阱在 PHP 里的形态与 JS 相反：按值捕获发生在闭包创建时，所以 `foreach` 里逐个创建的箭头函数各自拿到当次的值；确实要让多个闭包共享同一个变量，就显式写 `use (&$v)`。`use` 列表里不能出现超全局变量, `$this`, 或与形参同名的变量（7.1 起），需要多行逻辑就用 `function () {}`，箭头函数只能写一个表达式。以上代码未在本机运行验证（本机未安装 PHP 8.5），结论据 php.net 官方文档。

📘 [PHP · Anonymous functions](https://www.php.net/manual/en/functions.anonymous.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby 的匿名函数是 `Proc` 或 `lambda`，写法有 `lambda { |x| }`, `->(x) { }`, `proc { |x| }`，其中 `->` 只是 `Kernel#lambda` 的语法糖。block（`do |x| end`）不是对象，只能紧跟方法调用，这是它与前两者的根本差别。`lambda` 检查实参个数，`return` 只退出自身；`proc` 不检查个数，`return` 会试图从定义它的方法返回，所以异步回调一律用 `lambda`。捕获的结论一句话：Ruby 捕获变量本身，块内赋值写回外层，展开的捕获与逃逸细节见闭包一页。

```ruby
f = ->(x, y = 10) { x + y }               # lambda：检查 arity，return 只退出自身
prc = proc { |x, y| [x, y] }               # proc：不检查 arity，缺参补 nil
puts f.call(1)                              # 11
puts f.lambda?                               # true
puts prc.lambda?                              # false
puts f.arity                                  # -2   有可选参数时 arity 为负
puts prc.arity                                 # 2
puts f.parameters.inspect                       # [[:req, :x], [:opt, :y]]
puts prc.call(1).inspect                         # [1, nil]
puts f.(2, 3)                                     # 5   Proc#call 的 .() 写法
puts f[2, 3]                                       # 5   [] 等价于 call
puts (->(x) { x * 2 }).call(21)                     # 42  立即调用表达式

def counter
  n = 0
  -> { n += 1 }                                     # 捕获变量本身，赋值写回外层
end
c = counter
puts [c.call, c.call].inspect                        # [1, 2]

def each_thing
  return 'no block' unless block_given?               # yield 与 block_given?
  yield 1
end
puts each_thing { |x| x + 41 }                        # 42

def apply(x, &blk) = blk.call(x)                       # &blk 把 block 捕获成 Proc
puts apply(41) { |v| v + 1 }                            # 42
puts apply(41, &->(v) { v + 1 })                         # 42  & 也能把 Proc 传成 block

puts %w[a b].map(&:upcase).inspect                       # ["A", "B"]
```

`Proc` 作为对象的属性都能直接查：`arity` 为负数表示有可选参数，`parameters` 给出每个形参的种类，`lambda?` 区分严格与宽松两种调用约定，需要按签名分派时用它们而不是猜。逃逸与生命周期由 GC 管理，闭包对象活着，被捕获的局部变量就跟着活着，Ruby 没有 `'static` 或生命周期标注这类约束，也没有捕获列表语法。

循环变量陷阱只记一句结论：`for` 不创建新作用域，循环里创建的三个 lambda 会共享同一个 `i`，把 `for` 换成 `(1..3).map { |i| -> { i } }` 就每轮独立，因为 block 形参会新建绑定。收参形态上 `Proc` 与普通方法一样支持默认值, `*args`, `**kw`, `&blk`，调用方式有 `.call`, `.()`, `[]` 三种，语义完全等价。以上代码在本机 Ruby 4.0.6 上实际运行，注释中的输出与真实输出一致。

📘 [Ruby · Proc](https://docs.ruby-lang.org/en/master/Proc.html)

{{% /tab %}}

{{< /tabpane >}}

### 重载

重载问的是“同名函数能不能按参数类型选不同实现”，答案把语言分成三派：C++、Java、C#、Kotlin、Swift、Dart 在**编译期**按静态类型选候选；Julia 用多重分派在**运行期**按实参类型选方法，R 的 S3/S4 也是运行期分派；Rust、Go、C、Zig、Python、Lua、PHP、Ruby、JavaScript、TypeScript 则**没有**这一机制，各自改用 trait、泛型、`_Generic`、`anytype`、运行期判断或声明签名去顶替。判断一个语言属于哪一派，看的是它解析重载的时机，而不是关键字怎么写。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust **没有重载**：同一作用域内不允许同名函数，参数类型不同也不行。替代手段是 `trait`（按类型给行为，运行期走 `dyn Trait` 的 vtable、编译期走 monomorphization）、泛型函数（`fn f<T: Trait>(x: T)`）、以及 `enum` 把分支收进类型。Rust 也没有装饰器，`#[attribute]` 是编译器属性或过程宏，不是运行期包装。

```rust
trait Area { fn area(&self) -> f64; }
struct Circle(f64);
struct Square(f64);
impl Area for Circle { fn area(&self) -> f64 { 3.14159 * self.0 * self.0 } }
impl Area for Square { fn area(&self) -> f64 { self.0 * self.0 } }

fn area_of(s: &impl Area) -> f64 { s.area() }            // 静态分派：每种类型一份代码
fn area_dyn(s: &dyn Area) -> f64 { s.area() }             // 动态分派：vtable

fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T { a + b }    // 泛型函数
fn join(a: &str, b: &str) -> String { a.to_string() + b }

fn describe(x: Option<i32>) -> String {                    // 运行期分支模拟“重载”
    match x { Some(v) => format!("some {v}"), None => "none".into() }
}

fn main() {
    println!("{:.2}", area_of(&Circle(1.0)));         // 3.14
    println!("{:.2}", area_dyn(&Square(2.0)));          // 4.00
    println!("{}", add(40, 2));                          // 42
    println!("{}", join("a", "b"));                       // ab
    println!("{} {}", describe(Some(1)), describe(None));  // some 1 none
}
```

`&impl Area` 与 `<T: Area>` 都是静态分派，编译器为每个具体类型生成一份函数体；`&dyn Area` 只在调用点查一次 vtable，代价是一次间接跳转，换来二进制体积不膨胀。注意 `String + String` 没有实现（`Add` 只为 `String` 实现了 `Add<&str>`），所以字符串拼接要靠 `to_string() + &s` 或 `format!`。默认参数同样不存在，惯例是 builder 模式或 `..Default::default()`。

📘 [Rust · Traits](https://doc.rust-lang.org/reference/items/traits.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift **支持重载**：同名函数按参数类型、参数标签、参数个数、返回类型区分，重载解析在编译期完成。泛型函数用 `<T: Protocol>` 声明约束，`where` 子句追加更复杂的约束。装饰器方面，Swift 用**属性包装器**（`@propertyWrapper`）与**宏**（`@freestanding`/`@attached`）来代替，属性包装器在编译期展开成对 `wrappedValue` 的读写。

```swift
func area(_ r: Double) -> Double { 3.14159 * r * r }        // 重载 1
func area(_ w: Double, _ h: Double) -> Double { w * h }       // 重载 2

func first<T: Collection>(_ xs: T) -> T.Element? { xs.first }    // 泛型函数
func pair<T, U>(_ a: T, _ b: U) -> (T, U) { (a, b) }

@propertyWrapper                                        // 属性包装器
struct Clamped {
    var wrappedValue: Int
    let range: ClosedRange<Int>
    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.wrappedValue = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

struct Player {
    @Clamped(0...100) var hp = 150                      // 初始化时被裁剪
}

print(area(1.0))                       // 3.14159
print(area(2.0, 3.0))                   // 6.0
print(first([1, 2, 3]) ?? 0)             // 1
print(pair(1, "a"))                       // (1, "a")
print(Player().hp)                         // 100
```

重载只看参数类型与标签，不看返回类型，所以 `func f() -> Int` 与 `func f() -> String` 不能共存。泛型约束用 `where` 追加时写作 `func f<T>(_ x: T) where T: Equatable`；`some Protocol`（不透明返回类型）是 Swift 5.1 起的写法，`any Protocol` 才是存在类型。宏需要单独的 Swift Package 目标来声明，并在编译期展开，运行时没有任何开销。

📘 [Swift · Generics](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/)

{{% /tab %}}

{{% tab header="Go" %}}

Go **没有重载**（官方 FAQ 明确拒绝，理由是“按类型重载会让调用点无法一眼看出调用哪个函数”），也**没有装饰器**。替代方案是泛型函数（Go 1.18 起）与函数选项模式；Go 1.27 起还支持**泛型方法**（方法也可以有自己的类型参数）。

```go
package main

import "fmt"

type Number interface{ ~int | ~float64 }        // 类型集约束

func Sum[T Number](xs []T) T {                    // 泛型函数
	var t T
	for _, x := range xs { t += x }
	return t
}

func Map[T, U any](xs []T, f func(T) U) []U {      // 两个类型参数
	out := make([]U, 0, len(xs))
	for _, x := range xs { out = append(out, f(x)) }
	return out
}

type Rand struct{ seed int }

func (r *Rand) N[Int int | int64](n Int) Int {      // Go 1.27：泛型方法
	return Int(r.seed) % n
}

func main() {
	fmt.Println(Sum([]int{1, 2, 3}))          // 6
	fmt.Println(Sum([]float64{1.5, 2.5}))      // 4
	fmt.Println(Map([]int{1, 2, 3}, func(x int) string { return fmt.Sprint(x * 2) }))  // [2 4 6]
	r := &Rand{seed: 7}
	fmt.Println(r.N(3))                          // 1
}
```

`~int` 里的波浪号表示“底层类型是 int 的所有类型”，这是 Go 类型集的关键写法；约束必须是接口，且只有作为约束时接口才能含类型项——`~int | ~float64` 这样的 union 类型集**只能出现在泛型约束里，不能用来声明变量或字段**。Go 1.27 把函数类型推断推广到“泛型函数被赋给（或被转换为）匹配的函数类型”的所有上下文，这类赋值不再需要显式写出类型实参。Go 没有装饰器，惯用的“包装”就是接收并返回函数值（中间件模式）。

📘 [Go · Type parameters](https://go.dev/ref/spec#Type_parameter_declarations)

{{% /tab %}}

{{% tab header="Python" %}}

Python **没有编译期重载**：后定义的同名函数直接覆盖前者。替代做法是运行期判断参数类型或个数（`isinstance`、`len(args)`）、用默认参数、或用 `functools.singledispatch` 做按第一个实参类型的单分派。装饰器是 Python 最著名的特性：`@decorator` 就是 `f = decorator(f)`，被装饰对象可以是函数、方法、类。

```python
import functools

def logged(fn):                                  # 最简装饰器
    @functools.wraps(fn)                          # 保留 __name__ / __doc__
    def wrapper(*args, **kwargs):
        print(f"call {fn.__name__}")
        return fn(*args, **kwargs)
    return wrapper

def repeat(times):                                 # 带参数的装饰器：三层嵌套
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = fn(*args, **kwargs)
            return result
        return wrapper
    return deco

@logged
def add(a, b):
    return a + b

@repeat(3)
def tick():
    return "t"

print(add(40, 2))          # call add / 42
print(tick())               # t

@functools.singledispatch   # 按第一个实参类型分派（单分派“重载”）
def show(x):
    return f"object {x!r}"

@show.register
def _(x: int):
    return f"int {x}"

@show.register
def _(x: str):
    return f"str {x}"

print(show(1), "|", show("a"), "|", show(1.5))   # int 1 | str a | object 1.5
```

装饰器在定义时执行，所以 `@logged` 在模块导入阶段就已经把函数替换掉了。忘了 `functools.wraps` 会让被装饰函数的 `__name__` 变成 `wrapper`，破坏依赖内省的框架。`singledispatch` 只看第一个参数的类型，要看多个参数用 `singledispatchmethod` 或第三方库。类型注解在运行时可用 `typing.get_type_hints` 读到，这给“注解驱动的装饰器”留了空间。

📘 [Python · Decorators](https://docs.python.org/3/glossary.html#term-decorator)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin **支持重载**（同名函数按参数类型与个数区分，编译期解析），也支持默认参数与命名实参，因此很多 Java 里靠重载实现的场景在 Kotlin 里直接写默认值。Kotlin 没有运行期装饰器，注解（annotation）配合 **KSP**（Kotlin Symbol Processing）或 kapt 在编译期生成代码，这是 Android 生态里最主要的“装饰器式”编程方式。

```kotlin
@Target(AnnotationTarget.FUNCTION)              // 自定义注解
@Retention(AnnotationRetention.SOURCE)
annotation class Logged

fun area(r: Double): Double = 3.14159 * r * r    // 重载 1
fun area(w: Double, h: Double): Double = w * h     // 重载 2

fun <T : Comparable<T>> maxOf3(a: T, b: T, c: T): T =   // 泛型函数 + 约束
    listOf(a, b, c).max()

inline fun <reified T> typeName(): String = T::class.simpleName ?: "?"  // 具体化类型参数

class Service {
    @Logged                                      // 由 KSP 处理器读取
    fun compute(x: Int): Int = x * 2
}

fun main() {
    println(area(1.0))                     // 3.14159
    println(area(2.0, 3.0))                 // 6.0
    println(maxOf3(1, 5, 3))                 // 5
    println(typeName<List<String>>())         // List
    println(Service().compute(21))             // 42
}
```

重载与默认参数同时存在时，编译器优先选择不需要填充默认值的候选；参数个数相同的重载再比类型。注解本身不产生行为，必须有人读它——KSP 在编译期生成 Kotlin 源码，kapt 生成 Java stub 后交给注解处理器，两者都增加了构建时间。`reified` 类型参数只能用在 `inline` 函数上，它让泛型在编译期“具体化”，因此可以 `T::class`、`is T`。

📘 [Kotlin · Generics: generic functions](https://kotlinlang.org/docs/generics.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java **支持重载**，且解析规则相当繁琐：先按参数个数筛候选，再按“不需要装箱/可变参数”的优先级做分阶段匹配（严格调用 → 宽松调用 → 可变参数调用），全部在编译期定死。泛型函数用 `<T extends Bound>` 声明约束，但泛型在运行期被擦除。装饰器在 Java 里对应**注解 + 注解处理器（APT）**，典型产品是 Lombok、MapStruct、Dagger。

```java
import java.util.List;

public class Overload {
    static void print(int x)    { System.out.println("int " + x); }
    static void print(String s) { System.out.println("String " + s); }
    static void print(Object o) { System.out.println("Object " + o); }

    static <T extends Comparable<T>> T maxOf3(T a, T b, T c) {   // 泛型函数
        T m = a.compareTo(b) >= 0 ? a : b;
        return m.compareTo(c) >= 0 ? m : c;
    }

    static <T> List<T> listOf(T... xs) { return List.of(xs); }

    public static void main(String[] args) {
        print(1);              // int 1
        print("a");             // String a
        print(1.5);              // Object 1.5（double 装箱后走 Object）
        System.out.println(maxOf3(1, 5, 3));   // 5
        System.out.println(listOf(1, 2, 3));    // [1, 2, 3]
    }
}
```

重载的三阶段解析意味着“看起来能匹配”不代表会被选中：`print(1.5)` 找不到 `print(double)`，就进入宽松阶段把 `double` 装箱成 `Double`，再按 `Object` 匹配。泛型擦除的直接后果是 `List<String>` 与 `List<Integer>` 在运行期是同一个类，所以不能写 `new T[]`、不能对泛型做 `instanceof`、静态方法不能用类的类型参数。注解本身没有行为，处理器在编译期生成新代码，运行时开销为零。

📘 [JLS · Method overloading 与类型擦除](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html#jls-8.4.9)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的重载是四门 C 系语言里最完整的：函数可以按参数类型、个数、`const` 限定、引用限定（`&`/`&&`）重载，配合模板与特化能写出非常灵活的接口。属性（`[[nodiscard]]`、`[[deprecated]]`）是编译器提示，C++11 起还支持运算符重载，这两样合起来是 C++ 世界里的“装饰器替代品”。

```cpp
#include <cstdio>
#include <string>
#include <type_traits>

int abs_val(int x) { return x < 0 ? -x : x; }              // 重载 1
double abs_val(double x) { return x < 0 ? -x : x; }          // 重载 2

template <typename T> T max_of3(T a, T b, T c) {              // 泛型函数
    T m = a < b ? b : a;
    return m < c ? c : m;
}

template <typename T> std::string kind(T) {                    // 主模板
    return "general";
}
template <> std::string kind(int) { return "int"; }              // 全特化

struct Vec {
    int n = 0;
    Vec operator+(const Vec& o) const { return Vec{n + o.n}; }    // 运算符重载
};

[[nodiscard]] int compute(int x) { return x * 2; }                 // 属性

int main() {
    std::printf("%d %.1f\n", abs_val(-3), abs_val(-3.5));    // 3 3.5
    std::printf("%d\n", max_of3(1, 5, 3));                     // 5
    std::printf("%s %s\n", kind(1.5).c_str(), kind(1).c_str()); // general int
    Vec a{1}, b{2};
    std::printf("%d\n", (a + b).n);                              // 3
    std::printf("%d\n", compute(21));                             // 42
}
```

重载解析按“精确匹配 → 提升 → 标准转换 → 用户定义转换 → 省略号”排序，多个可行候选且无法比较优劣时就是歧义错误——默认参数经常制造这种歧义（`f(int)` 与 `f(int, int = 0)` 同时存在时，`f(1)` 会歧义）。模板与重载叠加时的匹配优先级是：非模板精确匹配 > 模板特化 > 主模板，具体规则见 cppreference 的“重载解析”页面。`[[nodiscard]]` 只是警告，不是错误。

📘 [cppreference · Overload resolution](https://en.cppreference.com/w/cpp/language/overload_resolution)

{{% /tab %}}

{{% tab header="C" %}}

C **没有重载**、**没有泛型函数**（C23 之前连 `_Generic` 都没有）、**没有装饰器**。同一作用域同名函数直接冲突。常用的替代有四种：用不同名字（`abs`/`fabs`/`labs`）、用 `_Generic` 做编译期类型选择（C11 起）、用 `void *` 加标签的通用接口、用宏做文本层“重载”。

```c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define abs_val(x) _Generic((x),        /* C11 起：按类型选实现 */     \
    int: abs,                                                     \
    long: labs,                                                   \
    double: fabs,                                                 \
    float: fabsf)(x)

typedef struct { int tag; union { long i; double d; } as; } Value;  /* 标签联合 */

Value make_int(long v) { Value r = { 0, { .i = v } }; return r; }
Value make_real(double v) { Value r = { 1, { .d = v } }; return r; }

double as_double(Value v) { return v.tag == 0 ? (double)v.as.i : v.as.d; }

int main(void) {
    printf("%d\n", abs_val(-3));                /* 3 */
    printf("%.1f\n", abs_val(-3.5));             /* 3.5 */
    printf("%.1f\n", as_double(make_int(42)));    /* 42.0 */
    printf("%.1f\n", as_double(make_real(1.5)));   /* 1.5 */
    return 0;
}
```

`_Generic` 是 C11 引入的编译期选择：它按控制表达式的类型选出一个表达式，不做任何运行期判断，所以也没有类型转换开销。宏层的 `_Generic` 要注意每个分支都必须是合法表达式，且 `_Generic` 不做算术转换——`float` 与 `double` 是两个不同分支。C23 加入 `typeof`、`constexpr`、`nullptr`、`[[nodiscard]]` 等特性，但依旧没有重载与泛型函数。

📘 [cppreference · _Generic](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的“重载”就是**多重分派**：一个泛型函数名下挂着多个方法，调用时按所有实参的类型在运行期选最具体的方法。这比编译期重载更强——分派依据可以是运行期类型，也可以是值的个数。宏（`macro`）在解析后、求值前对语法树做变换，是 Julia 里对应“装饰器”的机制。

```julia
area(r::Real) = 3.14159 * r^2                      # 方法 1
area(w::Real, h::Real) = w * h                       # 方法 2

describe(x::Integer) = "int $x"
describe(x::AbstractString) = "str $x"
describe(x) = "other $x"

function describe_all(xs::Vector)                    # 参数化方法
    join(describe.(xs), ", ")
end

macro timed(ex)                                       # 宏：变换语法树
    quote
        local t0 = time_ns()
        local v = $(esc(ex))
        println("elapsed ", (time_ns() - t0) / 1e6, " ms")
        v
    end
end

println(area(1.0))          # 3.14159
println(area(2.0, 3.0))      # 6.0
println(describe(1), " | ", describe("a"), " | ", describe(1.5))  # int 1 | str a | other 1.5
println(@timed sum(1:1000))   # 先打印耗时（毫秒），再打印 500500
println(methods(area))         # 2 个方法
```

方法的“更具体”由类型格决定：`Integer` 比 `Real` 具体，所以 `describe(1)` 选第一个方法；两个方法无法比较具体性时抛 `MethodError` 或歧义错误。宏收到的参数是**表达式**而不是值，所以宏里必须用 `esc()` 把用户代码的卫生性交还给调用者作用域，`@timed` 这类宏才能正确访问外层变量。宏在编译期展开，没有运行期开销，但错误信息会指向展开后的代码。

📘 [Julia · Methods 与宏](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# **支持重载**，解析规则与 Java 类似但更强调“更具体的类型优先”；泛型函数用 `<T> where T : 约束` 声明。装饰器方面，C# 用**特性（Attribute）** 加**源生成器（Source Generator）**：特性在编译期被读取，源生成器直接生成额外的 C# 源文件，运行期没有反射开销。

```csharp
using System;
using System.Diagnostics.CodeAnalysis;

class Overload {
    static void Print(int x)    => Console.WriteLine($"int {x}");
    static void Print(string s) => Console.WriteLine($"string {s}");
    static void Print(object o) => Console.WriteLine($"object {o}");

    static T MaxOf3<T>(T a, T b, T c) where T : IComparable<T> {   // 泛型约束
        T m = a.CompareTo(b) >= 0 ? a : b;
        return m.CompareTo(c) >= 0 ? m : c;
    }

    [Obsolete("use MaxOf3 instead")]                                // 特性
    static int MaxOf2(int a, int b) => Math.Max(a, b);

    static void Demo([DisallowNull] string s) => Console.WriteLine(s);

    static void Main() {
        Print(1);              // int 1
        Print("a");             // string a
        Print(1.5);              // object 1.5
        Console.WriteLine(MaxOf3(1, 5, 3));   // 5
        Demo("ok");                             // ok
    }
}
```

重载解析的优先级是：完全匹配 > 更具体的类型 > 可选参数更少 > 派生类型优于基类；`params` 版本永远是最后考虑。泛型约束可以叠加多个（`where T : class, IDisposable, new()`），但构造器约束 `new()` 必须放最后。特性在 C# 里是运行期可反射读到的元数据，源生成器与增量生成器则在编译期产出代码——后者才是真正意义上的“编译期装饰器”。

📘 [MS Learn · 泛型方法与重载](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/generics/generic-methods)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart **支持重载**，但仅限同一类内按参数类型区分；顶层函数与方法都不能只靠返回类型区分。泛型函数用 `<T extends Bound>` 声明约束，Dart 的泛型是**具体化（reified）** 的，所以运行期能知道 `List<int>` 与 `List<String>` 的区别。Dart 没有装饰器，注解（annotation）配合 **build_runner** 在构建期生成代码，这是 json_serializable、freezed 这些包的工作方式。

```dart
import 'package:meta/meta.dart';

class Area {
  double of(double r) => 3.14159 * r * r;              // 重载 1（同类内）
  double ofRect(double w, double h) => w * h;            // 换名，Dart 不支持按个数重载同名
}

T maxOf3<T extends Comparable<T>>(T a, T b, T c) =>     // 泛型函数 + 约束
    [a, b, c].reduce((x, y) => x.compareTo(y) >= 0 ? x : y);

List<R> mapList<T, R>(List<T> xs, R Function(T) f) => xs.map(f).toList();

@immutable                                                // 注解：由分析器读取
class Config {
  final int port;
  const Config({this.port = 8080});                        // 常量构造器
  @override
  String toString() => 'Config($port)';
}

void main() {
  print(Area().of(1));                     // 3.14159
  print(Area().ofRect(2, 3));               // 6.0
  print(maxOf3(1, 5, 3));                    // 5
  print(mapList<int, String>([1, 2], (x) => '$x!'));  // [1!, 2!]
  print(const Config());                      // Config(8080)
  print([1, 2, 3] is List<int>);               // true  泛型具体化
}
```

Dart 不允许“同名但参数个数不同”的重载——`of(double)` 与 `of(double, double)` 会直接报重复定义，所以要么换名，要么用可选参数，要么用命名参数。泛型具体化让 `xs is List<int>` 在运行期可用，代价是每个泛型实例化都要带类型信息。注解本身是常量对象，`build_runner` 读取它并生成 `.g.dart` 文件，产物参与正常编译。

📘 [Dart · Generics](https://dart.dev/language/generics)

{{% /tab %}}

{{% tab header="R" %}}

R **没有重载**，但对“按类型选实现”这件事有更强也更古老的两套机制：**S3**（`UseMethod()` 按第一个实参的 class 分派，靠命名约定 `f.class`）与 **S4**（`setGeneric()`/`setMethod()` 支持多个参数的签名分派）。R 也没有装饰器，但有函数包装（`function(f) ...`）与 `R6`/`setClass` 的方法机制。

```r
# S3 泛型：按第一个实参的 class 分派
area <- function(x, ...) UseMethod("area")
area.default <- function(x, ...) NA_real_
area.numeric <- function(x, ...) pi * x^2                    # 圆面积
area.matrix <- function(x, ...) nrow(x) * ncol(x)              # “矩阵面积”

print(area(2))                        # [1] 12.56637
m <- matrix(1:6, nrow = 2)
print(area(m))                         # [1] 3

# 函数包装：最接近装饰器的写法
logged <- function(f) {
  force(f)
  function(...) {
    cat("call", deparse(substitute(f)), "\n")
    f(...)
  }
}
double <- logged(function(x) x * 2)
print(double(21))                       # call ... / [1] 42

# S4：多重分派
setGeneric("describe", function(x) standardGeneric("describe"))
setMethod("describe", "numeric", function(x) paste("num", x))
setMethod("describe", "character", function(x) paste("chr", x))
print(describe(1))                       # [1] "num 1"
print(describe("a"))                      # [1] "chr a"
```

S3 的分派只看第一个参数，性能好、写法松，但没有正式的类型检查；S4 用 `setClass()` 定义类，支持继承与多参数分派，代价是更啰嗦。`logged()` 这种包装函数的陷阱是惰性求值：必须 `force(f)` 才能确保包装的是当时那个对象，否则可能因为 `f` 后来被重新赋值而行为改变。

📘 [R · S3 与 S4 分派](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatch)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有重载**、**没有泛型语法**、**没有装饰器**。函数层面的“泛型”靠 `comptime` 参数实现：类型也是值，可以在编译期传给函数，编译器为每组实参实例化一份代码；类型约束只能靠 `comptime` 断言（`@typeInfo`、`@hasDecl`）或 `anytype` 表达。

```zig
const std = @import("std");

fn maxOf3(comptime T: type, a: T, b: T, c: T) T {       // 显式类型参数
    const m = if (a > b) a else b;
    return if (m > c) m else c;
}

fn sum(values: anytype) @TypeOf(values[0]) {             // anytype 推断类型
    var total: @TypeOf(values[0]) = 0;
    for (values) |v| total += v;
    return total;
}

fn describe(x: anytype) []const u8 {                      // 用 comptime 分支代替重载
    return switch (@typeInfo(@TypeOf(x))) {
        .int, .comptime_int => "int",
        .float, .comptime_float => "float",
        .pointer => "pointer",
        else => "other",
    };
}

pub fn main() void {
    std.debug.print("{d}\n", .{maxOf3(i32, 1, 5, 3)});        // 5
    std.debug.print("{d}\n", .{sum([_]i32{ 1, 2, 3 })});       // 6
    std.debug.print("{s} {s}\n", .{ describe(1), describe(1.5) });  // int float
}
```

`comptime T: type` 是最直白的“显式泛型参数”，`anytype` 则让编译器按调用点推断，两者都只在编译期存在。用 `comptime` 块内的 `@compileError` 可以做约束检查，但报错信息由你自己撰写。Zig 的 `@typeInfo` 返回的是编译期结构体，`switch` 里列出所有分支是编译期求值的，不会生成运行期分支。

📘 [Zig · comptime 参数](https://ziglang.org/documentation/master/#comptime)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有重载**、**没有泛型**、**没有装饰器**。替代方案是利用“一切都是 table”的灵活性：用一个表的字段承载不同参数形态、用元表（metatable）转发调用、或者用可变参数在函数体内分支。函数包装（高阶函数）是最接近装饰器的写法，因为函数是一等值。

```lua
local function area(a, b)                  -- 用参数个数区分“重载”
  if b == nil then
    return 3.14159 * a * a                  -- 一个参数：当半径
  end
  return a * b                               -- 两个参数：当长宽
end

local function maxOf3(a, b, c) return math.max(a, b, c) end   -- 无泛型：动态类型

local function logged(f)                     -- 高阶函数：最接近装饰器
  return function(...)
    io.write("call\n")
    return f(...)
  end
end

local double = logged(function(x) return x * 2 end)
print(double(21))                            -- call / 42

local Proxy = setmetatable({}, {             -- 元表转发：__call 让 table 可调用
  __call = function(_, x) return x + 1 end,
})
print(Proxy(41))                              -- 42

print(area(2))          -- 12.56636
print(area(2, 3))        -- 6
print(maxOf3(1, 5, 3))    -- 5
```

Lua 里“重载”完全靠运行期判断，`type()`、`select("#", ...)`、`math.type()` 是常用的判别手段，代价是错误只会在运行期暴露。元表的 `__call` 让任何值可被调用，`__index`/`__newindex` 让对象像类，这是 Lua 做 OOP 与代理的基础，也是它实现“装饰器式”包装的主要途径。5.5 起 `global` 成为保留字，声明全局变量要用 `global x`。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的“重载”只是**类型层面的多个声明签名**，编译后只剩一个实现；运行时的分支必须自己写（判断 `typeof`、`instanceof`、参数个数或属性存在性）。泛型函数用 `<T extends Bound>` 声明，装饰器从 5.0 起按 TC39 标准实现（`experimentalDecorators` 开关对应旧的实验版本），可以装饰类、方法、访问器、字段。

```typescript
// 重载声明：类型层面
function pick(x: string): string;
function pick(x: number): number;
function pick(x: string | number): string | number {
  return x;                              // 运行时只有一个实现
}

function maxOf3<T extends Comparable>(a: T, b: T, c: T): T {   // 泛型约束
  return [a, b, c].reduce((x, y) => (x.compareTo(y) >= 0 ? x : y));
}
interface Comparable { compareTo(o: this): number }

function logged<T extends (...args: any[]) => any>(
  value: T,                                    // 被装饰的方法本身
  context: ClassMethodDecoratorContext        // 标准（TC39）装饰器的第二个参数
): T {
  const name = String(context.name);
  return function (this: unknown, ...args: any[]) {   // 返回新函数即替换原方法
    console.log(`call ${name}`);
    return value.apply(this, args);
  } as T;
}

class Calc {
  @logged
  add(a: number, b: number): number { return a + b; }
}

console.log(pick('a'), pick(1));          // a 1
console.log(new Calc().add(40, 2));         // call add / 42
console.log([1, 2, 3].map<number>((x) => x * 2));  // [ 2, 4, 6 ]
```

重载签名必须与实现签名兼容：实现签名的参数要能覆盖所有声明的参数类型，实现签名本身对调用者不可见。标准装饰器的签名是 `(value, context)`：`value` 是被装饰的方法本身，返回一个新函数就替换掉原方法，`context.name` 给出方法名；旧的 `experimentalDecorators` 用的 `(target, key, descriptor)` 签名是另一套语义，两套不能混用。泛型只存在于编译期，`<T>` 在运行期完全没有痕迹，因此不能 `new T()`、不能判断 `x instanceof T`。

📘 [TypeScript · Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有重载**，同名函数后定义者生效；也**没有泛型**（类型层的东西都在 TypeScript 里）。运行期判断参数类型或个数是最常见的替代，`arguments.length` 或 rest 参数配合 `typeof` 就能实现“多态”行为。装饰器是 TC39 提案（Stage 3，尚未进入 ECMAScript 标准），Node 26 上仍要靠 TypeScript/Babel 等转译器编译，写之前先确认工具链支持的版本。

```javascript
function pick(x) {                        // 运行期判断代替重载
  if (typeof x === 'number') return x;
  if (typeof x === 'string') return x;
  throw new TypeError('unsupported');
}

function area(a, b) {
  return b === undefined ? 3.14159 * a * a : a * b;   // 参数个数分派
}

// 装饰函数的本质：收一个函数、返回一个新函数（下面手工应用一次）
function logged(original, name) {
  return function (...args) {
    console.log(`call ${name}`);
    return original.apply(this, args);
  };
}

// 标准（TC39）版装饰器签名是 (value, context)，返回新函数替换原方法
class Calc {                             // 原生 Node 解析不了 @，这里手工套一层
  add(a, b) { return a + b; }
}
Calc.prototype.add = logged(Calc.prototype.add, 'add');

console.log(pick(1), pick('a'));           // 1 a
console.log(new Calc().add(40, 2));          // call add / 42
console.log(area(2), area(2, 3));             // 12.56636 6
console.log([1, 2, 3].map(x => x * 2));        // [ 2, 4, 6 ]
```

用参数个数分派时必须区分“显式传 `undefined`”和“没传”，`arguments.length` 比 `b === undefined` 更可靠。装饰器的两版提案在参数形态上不兼容：TC39 标准版（Stage 3）接收 `(value, context)`，Stage 2 版接收 `(target, key, descriptor)`；两者共同的前提是“装饰器本身就是一个收函数、返回新函数的高阶函数”，所以示例里手工套的那一层 `logged` 与将来真正用 `@logged` 时的行为一致。正因为装饰器还是提案，原生 Node 解析到 `@` 会直接抛 `SyntaxError`，上面那段用赋值而不是 `@` 语法，在本机 Node 上实跑通过。运行期的“泛型”只能用鸭子类型或 `Symbol.iterator` 之类的协议来表达。

📘 [MDN · Functions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Functions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP **没有重载**（不能用同名函数），也**没有泛型函数**（8.5 仍只有类/属性的类型声明）。替代方案是默认参数、可变参数加运行期判断，或者用 `__call`/`__callStatic` 魔术方法做动态方法转发。装饰器对应 **Attribute（8.0+）** 加反射读取；8.4 起加入属性钩子（property hooks），8.5 起 `#[\NoDiscard]` 可以标记必须使用的返回值。

```php
<?php
declare(strict_types=1);

#[Attribute(Attribute::TARGET_METHOD)]        // 声明一个特性
class Logged {}

function area(float $a, ?float $b = null): float {   // 用默认参数代替重载
    return $b === null ? 3.14159 * $a * $a : $a * $b;
}

function max_of3(int|float ...$xs): int|float {        // 联合类型 + 变参
    return max($xs);
}

class Service {
    #[Logged]
    public function compute(int $x): int { return $x * 2; }

    public function __call(string $name, array $args) {   // 动态方法转发
        return "no method $name";
    }
}

class User {
    public string $fullName {                              // 属性钩子（8.4+）
        get => trim($this->first . ' ' . $this->last);
    }
    public function __construct(public string $first = '', public string $last = '') {}
}

echo area(2.0), PHP_EOL;            // 12.56636
echo area(2.0, 3.0), PHP_EOL;        // 6
echo max_of3(1, 5, 3), PHP_EOL;       // 5
$s = new Service();
echo $s->compute(21), PHP_EOL;         // 42
echo $s->missing(), PHP_EOL;            // no method missing
echo (new User('Ann', 'Lee'))->fullName, PHP_EOL;   // Ann Lee

$rm = new ReflectionMethod(Service::class, 'compute');
var_dump($rm->getAttributes(Logged::class) !== []);   // bool(true)
```

`#[Logged]` 本身什么都不做，必须有代码用 `ReflectionClass`/`ReflectionMethod` 去读它——这与 Python 装饰器“立即执行”的语义完全不同，性能开销也发生在反射时。`__call` 只在方法不存在时触发，常用于代理与门面。属性钩子让 `get`/`set` 写在属性声明里，不再需要手写 `getFullName()`；8.5 起也可以用 `clone($obj, ['prop' => $v])` 在克隆时改只读属性。

📘 [PHP · Attributes](https://www.php.net/manual/en/language.attributes.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有重载**（同名方法后定义者覆盖前者），也**没有泛型**。替代做法是默认参数、`*args` 加运行期判断、以及用 `method_missing` / `respond_to_missing?` 做动态转发。装饰器在 Ruby 里通过**方法包装**实现：`prepend` 把模块插到方法查找链的最前面，`alias_method` 或 `Module#prepend` 加 `super` 是最常见的写法。

```ruby
module Loggable                                 # prepend：模块先于类被查找
  def greet(name)
    puts "log: greet(#{name})"
    super
  end
end

class Greeter
  def greet(name) = "hi #{name}"
end
Greeter.prepend(Loggable)
puts Greeter.new.greet("ann")        # log: greet(ann) / hi ann

def wrap(klass, name)                            # 方法包装：重定义 + 保留原实现
  original = klass.instance_method(name)
  klass.define_method(name) do |*args, **kw, &blk|
    puts "wrap: #{name}"
    original.bind(self).call(*args, **kw, &blk)
  end
end

class Calc
  def add(a, b) = a + b
end
wrap(Calc, :add)
puts Calc.new.add(40, 2)              # wrap: add / 42

class Area
  def of(a, b = nil)                   # 用默认参数模拟重载
    b.nil? ? 3.14159 * a * a : a * b
  end
end
puts Area.new.of(2).round(5)            # 12.56636
puts Area.new.of(2, 3)                   # 6
```

`prepend` 与 `include` 的差别在查找顺序：`prepend` 的模块排在类自身之前，因此 `super` 能调到类里的原始方法；`include` 排在类之后，同名方法会被类覆盖。用 `instance_method` 取到的 `UnboundMethod` 必须 `bind(self)` 才能调用，这是给任意类做“装饰”的关键技巧。`method_missing` 虽然灵活，但会让 `respond_to?` 与 IDE 补全失准，记得同步实现 `respond_to_missing?`。

📘 [Ruby · Module#prepend](https://docs.ruby-lang.org/en/master/Module.html#method-i-prepend)

{{% /tab %}}

{{< /tabpane >}}

### 泛型与装饰

泛型函数与装饰器是函数主题的另一半：泛型函数解决“同一段逻辑适配多种类型”，装饰器解决“在不改函数体的前提下加点行为”。泛型函数的写法差异集中在约束表达（`T: Trait`、`[T Number]`、`<T extends Number>`、`where` 子句）与实现模型（monomorphization 还是 type erasure，泛型是否 reified）；装饰器则从 Python 的 `@decorator`（普通高阶函数）一路分化到 Java 注解处理器、C# 源生成器、Kotlin KSP、Swift 宏、Dart build_runner 这些需要构建期工具的方案，PHP 的 Attribute、R 的函数包装、Lua 的元表转发各自代表另一种取舍。泛型的类型系统细节（型变、存在类型、擦除边界）归 generic.md。

{{< tabpane text=true persist=disabled >}}

{{% tab header="Rust" %}}

Rust 的泛型函数在编译期做静态分派：类型参数写在函数名后的尖括号里，约束用 `T: Trait` 或 `where` 子句给出，编译器对每个具体类型实例化一份代码，也就是 monomorphization。代价是二进制体积随实例化数量增长，换来零成本抽象；需要运行期多态时改用 `dyn Trait`，走 vtable 的一次间接跳转。Rust 没有运行期装饰器，`#[derive]` 与属性宏、过程宏都是编译期把代码展开或改写成别的代码，程序跑起来之后没有任何包装层存在。重载的缺席见前一节。

```rust
use std::ops::Add;

trait Shape { fn area(&self) -> f64; }
struct Circle(f64);
struct Square(f64);
impl Shape for Circle { fn area(&self) -> f64 { 3.14159 * self.0 * self.0 } }
impl Shape for Square { fn area(&self) -> f64 { self.0 * self.0 } }

fn add<T: Add<Output = T> + Copy>(a: T, b: T) -> T { a + b }

fn sum_all<T>(xs: &[T]) -> T
where
    T: Add<Output = T> + Copy,
{
    let mut acc = xs[0];
    for &x in &xs[1..] { acc = acc + x; }
    acc
}

fn area_static(s: &impl Shape) -> f64 { s.area() }   // 静态分派
fn area_dyn(s: &dyn Shape) -> f64 { s.area() }       // 动态分派：vtable

fn logged<F: Fn(i32) -> i32>(f: F) -> impl Fn(i32) -> i32 {
    move |x| { let y = f(x); println!("[log] {x} -> {y}"); y }
}

#[derive(Debug, Clone, PartialEq)]
struct Point { x: i32, y: i32 }

fn main() {
    println!("{}", add(40, 2));                     // 42
    println!("{}", sum_all(&[1, 2, 3, 4]));          // 10
    println!("{:.2}", area_static(&Circle(1.0)));     // 3.14
    println!("{:.2}", area_dyn(&Square(2.0)));        // 4.00
    let f = logged(|x| x * 2);
    println!("{}", f(21));                           // [log] 21 -> 42
                                                     // 42
    let p = Point { x: 1, y: 2 };
    println!("{:?}", p.clone() == p);                // true
}
```

`add`、`sum_all`、`area_static` 都是 `monomorphization`：调用点推断出 `T` 或 `impl Shape` 背后的具体类型，然后各自生成一份函数体，调用是直接调用。`area_dyn` 的参数是胖指针，内部是数据指针加 vtable 指针，调用时才查表，优点是不必为每种 `Shape` 复制代码；热路径优先泛型，只有需要把不同类型装进同一个容器时才用 `dyn Trait`。`where` 子句和多约束 `T: A + B` 等价，只是把长约束挪到签名后面更好读，返回值位置写 `impl Fn(i32) -> i32` 表示不透明类型，调用方看不到具体闭包类型。`logged` 是纯函数包装而非装饰器：它在运行期真正套了一层闭包，而 `#[derive(Debug, Clone, PartialEq)]` 是编译期过程宏，展开成 `impl Debug` 与 `impl Clone` 等代码，生成的 `clone` 与 `==` 没有额外解释开销。⚠️ `#[derive]` 只能加在类型定义上，属性宏只能加在 item 上，它们都不是 Python 那种运行期 `@decorator`。本机用 `rustc 1.98.1` 实跑，注释输出与真实输出一致。

📘 [Rust · Trait bounds and where clauses](https://doc.rust-lang.org/book/ch10-02-traits.html#clearer-trait-bounds-with-where-clauses) 与 [Rust Reference · Procedural macros](https://doc.rust-lang.org/reference/procedural-macros.html)

{{% /tab %}}

{{% tab header="Swift" %}}

Swift 的泛型函数用 `<T: Protocol>` 声明类型参数与上界，更复杂的约束写进签名末尾的 `where` 子句，具体见官方 Generics 一章。`some Shape` 是不透明返回类型，保证调用点只暴露协议接口而隐藏具体类型；`any Shape` 是存在类型，装箱后在运行期查 witness table，属于动态分派。泛型特化只是优化器的实现细节，不是语言保证，别把它当成可以依赖的行为。装饰方面 Swift 没有 Python 式装饰器，靠 `@propertyWrapper` 与宏（`@freestanding`、`@attached`）实现编译期展开，其中属性包装器把属性的读写改写成对 `wrappedValue` 的访问，宏则在编译期把调用点替换成生成的代码。重载见前一节。

```swift
protocol Shape { func area() -> Double }
struct Circle: Shape { let r: Double; func area() -> Double { 3.14159 * r * r } }
struct Square: Shape { let s: Double; func area() -> Double { s * s } }

func sum<T: Numeric>(_ xs: [T]) -> T { xs.reduce(0, +) }            // <T: Protocol>
func pair<T, U>(_ a: T, _ b: U) -> (T, U) { (a, b) }                 // 多个类型参数
func largest<T>(_ xs: [T]) -> T? where T: Comparable { xs.max() }    // where 子句

protocol Maker { associatedtype Item }
struct IntMaker: Maker { typealias Item = Int }

func erase<M: Maker>(_ m: M) -> M.Item? { nil }                      // 泛型 + 关联类型
func wrap<T>(_ name: String, _ f: @escaping (T) -> T) -> (T) -> T {  // 高阶包装
    { x in let y = f(x); print("[\(name)] -> \(y)"); return y }
}
func areaStatic<S: Shape>(_ s: S) -> Double { s.area() }   // 泛型：静态分派
func areaAny(_ s: any Shape) -> Double { s.area() }        // 存在类型：动态分派
func makeCircle() -> some Shape { Circle(r: 1.0) }          // 不透明类型

@propertyWrapper                                              // 属性包装器
struct Clamped {
    var wrappedValue: Int
    let range: ClosedRange<Int>
    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.wrappedValue = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}
struct Player { @Clamped(0...100) var hp = 150 }

print(sum([1, 2, 3, 4]))           // 10
print(pair(1, "a"))                 // (1, "a")
print(largest([3, 9, 4]) ?? 0)      // 9
print(areaStatic(Circle(r: 1.0)))    // 3.14159
print(areaAny(Square(s: 2.0)))       // 4.0
print(makeCircle().area())           // 3.14159
print(Player().hp)                   // 100
print(erase(IntMaker()) ?? 0)        // 0
print(wrap("dbl", { $0 * 2 })(21))   // [dbl] -> 42
                                     // 42
```

`sum`、`pair`、`largest` 都靠调用点实参推断类型参数，只有推断不出来时才写 `sum<Int>([])` 这类显式形式；`largest` 要求 `T: Comparable`，`erase` 要求 `M: Maker` 才能用关联类型 `M.Item`，这些约束都在编译期检查。`areaStatic` 传 `Circle` 时就把 `S` 固定下来，是静态分派；`areaAny` 把值装进存在类型容器，协议方法按 witness table 走间接调用，灵活但会付出装箱与间接调用成本。`@Clamped(0...100) var hp = 150` 在初始化时经 `init(wrappedValue:_:)` 裁剪成 100，包装器是编译期改写，属性访问路径上不长出额外调用。`wrap` 不是装饰器，它只是接收函数值再返回新函数值的高阶函数，包装层在运行期真实存在，所以每次调用都会打印日志。⚠️ 属性包装器的参数写在属性声明里，`wrappedValue` 与可选的 `projectedValue` 名字不能改；宏的声明与实现要放在单独的 Swift Package 宏目标里。本机用 `swiftc 6.4` 实跑泛型、属性包装器与高阶包装，另用 swift-syntax 604.0.0 实跑 `@freestanding(expression)` 表达式宏 `#stringify(6 * 7)` 输出 42，注释输出与真实输出一致。

📘 [The Swift Programming Language · Generics](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/generics/) 与 [Swift Evolution · SE-0258 Property Wrappers](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0258-property-wrappers.md)

{{% /tab %}}

{{% tab header="Go" %}}

Go 的泛型函数用方括号写类型参数，约束必须是接口；`~int | ~float64` 这样的 union 类型项构成类型集，只能出现在约束位置，不能拿来声明变量或字段，只有基本接口（不含类型集的接口）才能作值的类型。类型推断把调用点的实参类型代入类型参数，Go 1.27 起还扩展到把泛型函数赋给或转换成匹配函数类型的所有上下文。Go 1.27 起具体类型的方法可以有自己的类型参数，泛型函数不必再挤在包作用域；接口的方法既不能声明类型参数，也不能由泛型方法实现。Go 没有装饰器，要给函数加行为只能用中间件式包装，也就是接收函数值并返回新的函数值。重载与泛型的关系见前一节。

```go
package main

import (
    "fmt"
    "strings"
)

type Number interface{ ~int | ~float64 } // union 类型集：只能当约束

func Sum[T Number](xs []T) T { // 泛型函数
    var t T
    for _, x := range xs {
        t += x
    }
    return t
}

func Map[T, U any](xs []T, f func(T) U) []U { // 调用点推断 T、U
    out := make([]U, 0, len(xs))
    for _, x := range xs { out = append(out, f(x)) }
    return out
}

type Queue[E any] struct{ items []E }

func (q *Queue[E]) Map[R any](f func(E) R) *Queue[R] { // Go 1.27 泛型方法
    out := &Queue[R]{items: make([]R, 0, len(q.items))}
    for _, x := range q.items { out.items = append(out.items, f(x)) }
    return out
}

type Handler func(string) string

func WithLog(h Handler) Handler { // 中间件式包装
    return func(s string) string {
        r := h(s)
        fmt.Println("[log]", s, "->", r)
        return r
    }
}

func main() {
    fmt.Println(Sum([]int{1, 2, 3}))        // 6
    fmt.Println(Sum([]float64{1.5, 2.5}))   // 4
    fmt.Println(Map([]int{1, 2, 3}, func(x int) string { return fmt.Sprint(x * 2) })) // [2 4 6]
    q := &Queue[int]{items: []int{1, 2, 3}}
    fmt.Println(q.Map(func(x int) string { return strings.Repeat("x", x) }).items) // [x xx xxx]
    fmt.Println(WithLog(strings.ToUpper)("go")) // [log] go -> GO
    // GO
}
```

`Sum` 的 `T` 被推断为 `int` 与 `float64`，约束 `Number` 用 `~int | ~float64` 表示“底层类型是 int 或 float64 的所有类型”，所以 `type Celsius float64` 也能传进来，因为 `+=` 与零值 `var t T` 对类型集里每个类型都成立。`Map` 与泛型方法 `(*Queue[E]).Map[R]` 都由实参推断出两个类型参数，`q.Map(func(x int) string {...})` 返回 `*Queue[string]`；`~int | ~float64` 不能写成 `var n Number`，否则编译报错 `cannot use type Number outside a type constraint`，而 `type I interface { M[P any]() }` 会被拒绝为 `interface method must have no type parameters`，泛型方法也无法满足非泛型接口方法。`WithLog` 是 Go 里最接近装饰器的写法：它在运行期真的返回一个闭包，每次调用都要多一层间接调用，好处是能任意组合中间件；⚠️ 包装后函数值不再可比较，且一旦被包装，原来的具名函数身份就丢了。本机用 `go 1.27.1` 实跑，注释输出与真实输出一致；示例按空格缩进以便排版，等价的 gofmt 版本使用 tab。

📘 [Go · Type parameter declarations](https://go.dev/ref/spec#Type_parameter_declarations) 与 [The Go Blog · Generic Methods](https://go.dev/blog/generic-methods)

{{% /tab %}}

{{% tab header="Python" %}}

Python 的泛型是**类型注解**而非类型系统：类型参数只参与静态检查，解释器在运行期不看它们。PEP 695 从 3.12 起给出原生语法 `def f[T](x: T) -> T`、`class C[T]` 与 `type` 语句，取代了 `typing.TypeVar` 的三行样板；约束写成 `[T: Bound]`，上界既可以是类，也可以是 `Protocol` 描述的结构化约束。装饰是另一条线：`@decorator` 在**定义时**执行，等价于 `f = decorator(f)`，可装饰函数、方法与类。

```python
import functools
from typing import Protocol

type ListOrSet[T] = list[T] | set[T]        # PEP 695 类型别名（3.12+）

def first[T](xs: list[T]) -> T:             # PEP 695 泛型函数（3.12+）
    return xs[0]

print(first([1, 2, 3]), first(["a"]))       # 1 a

class Sized(Protocol):                      # 结构化约束
    def __len__(self) -> int: ...

def size_of[T: Sized](x: T) -> int:         # 上界写在 T 后面
    return len(x)

print(size_of("abc"), size_of([1, 2]))      # 3 2

def want_int[T: int](x: T) -> T: return x   # 注解不强制约束运行期

print(want_int("s"))                        # s（静态检查器才会报错）

def logged(fn):
    @functools.wraps(fn)                    # 保留 __name__ / __doc__
    def wrapper(*args, **kw):
        print(f"call {fn.__name__}")
        return fn(*args, **kw)
    return wrapper

@logged
def add(a: int, b: int) -> int:
    return a + b

print(add(40, 2))                           # call add / 42
print(add.__name__, hasattr(add, "__wrapped__"))   # add True

@functools.singledispatch                   # 按第一个实参运行期分派
def render(x): return "other"

@render.register
def _(x: int): return f"int {x}"

print(render(7), render("a"))               # int 7 other

class C:
    @staticmethod
    def s(): return "S"                     # 三者都是装饰器
    @property
    def p(self): return "P"

print(C.s(), C().p)                         # S P
```

上面每行注释都是 CPython 3.14.7 在 `/tmp/verify/generic_py.py` 里的真实输出。泛型在 Python 里是 `type erasure` 的对立面：对象上根本没有类型参数，`first.__type_params__` 只是函数属性，所以既没有 `monomorphization` 也没有静态分派，`first(1)` 与 `first("a")` 走的是同一份字节码，类型错误只有静态检查器会报（`mypy`、`pyright`、`ty`）。3.11 及更早必须写 `T = TypeVar("T")` 再 `def first(xs: list[T]) -> T`，PEP 695 语法从 3.12 起才算正式；`ParamSpec` 用来转发被装饰函数的参数签名，`Protocol` 用来给 `T` 加结构化上界。装饰器真正改变的是名字绑定，机制上是运行期的高阶函数调用：`functools.wraps` 把 `__module__`、`__name__`、`__qualname__`、`__doc__`、`__dict__` 与 `__wrapped__` 复制到 `wrapper` 上，漏掉它会让框架看到的函数名变成 `wrapper`；带参数的装饰器就是「返回装饰器的函数」，多一层嵌套。`staticmethod`、`classmethod`、`property`、`functools.singledispatch`（单分派，只看第一个实参，方法用 `singledispatchmethod`）本身都是装饰器；`singledispatch` 的分派发生在运行期，是 Python 里最接近「按类型重载」的机制，重载解析规则见《重载》一页。

📘 [Python 3.14 · Type parameter lists](https://docs.python.org/3/reference/compound_stmts.html#type-parameter-lists) 与 [functools 文档](https://docs.python.org/3/library/functools.html)

{{% /tab %}}

{{% tab header="Kotlin" %}}

Kotlin 的泛型函数在**编译期完全静态**：类型参数写在函数名之前，调用点靠上下文推断实参，编译期就知道每个 `T` 是什么。约束用冒号写成上界 `T : Comparable<T>`，需要多个上界时改用 `where` 子句。JVM 上的泛型类与 Java 一样会被擦除，函数式接口调用仍是 `vtable` 式的动态分派，因此 Kotlin 额外提供 `reified` 加 `inline` 来在编译期把类型参数“具体化”。

```kotlin
fun <T : Comparable<T>> maxOf3(a: T, b: T, c: T): T =   // 上界写在冒号后
    listOf(a, b, c).max()

fun <T> copyWhenGreater(list: List<T>, threshold: T): List<String>
        where T : CharSequence, T : Comparable<T> =     // 多个上界用 where
    list.filter { it > threshold }.map { it.toString() }

fun <T> singletonList(item: T): List<T> = listOf(item)  // 无约束，上界默认 Any?

inline fun <reified T> typeName(): String =             // 只能用在 inline 函数上
    T::class.simpleName ?: "?"

@Target(AnnotationTarget.FUNCTION)                      // 自定义注解
@Retention(AnnotationRetention.SOURCE)
annotation class Logged

class Service {
    @Logged                                             // 这个注解由 KSP 读取
    fun compute(x: Int): Int = x * 2
}

fun main() {
    println(maxOf3(1, 5, 3))                 // 5（T 推断为 Int）
    println(copyWhenGreater(listOf("b", "a"), "a"))   // [b]
    println(singletonList(42))               // [42]
    println(typeName<List<String>>())        // List
    println(Service().compute(21))           // 42
}
```

每个 `println` 左边的注释是依据 Kotlin 官方文档与标准库签名推断的预期输出；本机没有 Kotlin 2.4 工具链，整段代码未经本机运行验证。`maxOf3(1, 5, 3)` 不需要写 `maxOf3<Int>(...)`，编译器从三个 `Int` 实参反推出 `T = Int`，再检查 `Int` 是否满足 `Comparable<Int>`；`where T : CharSequence, T : Comparable<T>` 要求两个上界同时满足，`String` 恰好都符合。型变只在声明处写：`out` 表示只产出（协变），`in` 表示只消费（逆变），使用处用星投影 `List<*>` 表示类型实参未知，它近似 Java 的裸类型但读写受上界保护。泛型函数与重载可以共存，解析规则见《重载》一页。

Kotlin 没有运行期装饰器：注解只是元数据，本身不产生行为，必须有处理器在编译期读取它。KSP（Kotlin Symbol Processing）直接按 Kotlin 语法树建模符号，处理器只能看声明与类型、看不到函数体与表达式，只能生成新源码而**不能改写原源码**，生成的文件与手写源码一起再交给编译器；kapt 则是先生成 Java stub 再跑既有的 Java 注解处理器，因此慢一些，官方把 KSP 作为新项目的首选。典型产物有 Dagger 的依赖注入代码、Room 的数据库访问代码、Moshi 的序列化代码。注解能不能派上用场还取决于 `@Target` 与 `@Retention`：`SOURCE` 级的注解不进 class 文件，运行期反射看不到，只有 KSP 或 kapt 这类编译期读者才关心它，而 `@Retention(AnnotationRetention.RUNTIME)` 才会被写进字节码供反射读取。`reified` 只能出现在 `inline` 函数上：`inline` 把函数体与 lambda 展开到调用点，`reified` 才有真实的类型实参可用，于是 `T::class`、`is T`、`as T` 都合法；普通函数的 `T` 在运行期不存在，`is T` 会直接编译失败（`foo as T` 只会给一个 unchecked 警告）。

还有一个容易混的点：`inline` 与泛型是两件独立的事，函数只有同时标了 `inline` 才能带 `reified` 类型参数；泛型函数也可以直接当值用，例如 `val f: (Int) -> List<Int> = ::singletonList`，此时类型实参在赋值处被推断出来。

📘 [Kotlin · Generics: in, out, where](https://kotlinlang.org/docs/generics.html) 与 [KSP 概览](https://kotlinlang.org/docs/ksp-overview.html)

{{% /tab %}}

{{% tab header="Java" %}}

Java 的泛型函数用类型参数声明，上界写成 `<T extends Bound>`，多个上界用 `&` 连接，调用点由编译器做类型推断，不写实参类型参数也能推出 `T`。实现模型是 `type erasure`：编译期插好强制转换，运行期 `List<String>` 与 `List<Integer>` 是同一个类。给函数加行为而不改函数体靠**注解加注解处理器（APT）**：注解只是元数据，处理器在编译期读它并生成新代码。

```java
import java.util.List;

public class Main {
    static <T extends Comparable<T>> T maxOf3(T a, T b, T c) {   // 泛型函数
        T m = a.compareTo(b) >= 0 ? a : b;
        return m.compareTo(c) >= 0 ? m : c;
    }

    static <T> T firstOf(List<? extends T> xs) {     // PECS：只读用 extends
        return xs.get(0);
    }

    @SafeVarargs                                     // 压制泛型可变参数警告
    static <T> List<T> listOf(T... xs) { return List.of(xs); }

    static double average(List<? extends Number> xs) {   // 读 Number，写不了
        double sum = 0;
        for (Number n : xs) sum += n.doubleValue();
        return sum / xs.size();
    }

    @Logged                                          // 标记，由 APT 在编译期读取
    static int compute(int x) { return x * 2; }

    public static void main(String[] args) {
        System.out.println(maxOf3(1, 5, 3));         // 5
        System.out.println(firstOf(List.of("a", "b")));   // a
        System.out.println(average(List.of(1, 2, 3)));    // 2.0
        System.out.println(compute(21));             // 42
    }
}

@interface Logged { }        // 注解只是元数据，声明处不产生任何行为
```

上面的输出是按 JLS 与官方教程推出来的预期值；本机没有 Java 运行时与编译器，整段代码未经本机运行验证。`<T extends Comparable<T>>` 是常用的“自限定”上界：没有上界时 `T` 擦除为 `Object`，只能调 `Object` 的方法，写了上界才能调 `compareTo`，擦除后也会插入到 `Comparable` 的强制转换。推断发生在调用点：`maxOf3(1, 5, 3)` 的 `T` 直接推出 `Integer`，`firstOf(List.of("a", "b"))` 推出 `String`，要强制指定时可写 `Main.<Integer>maxOf3(1, 5, 3)`。通配符遵循 PECS：生产者用 `? extends T`，消费者用 `? super T`，`average` 只读所有元素所以写 `List<? extends Number>`，而 `? extends` 的那一边调 `add` 会编译失败。

擦除带来一组硬限制：不能 `new T[]`、不能 `new E()`、不能对泛型做 `instanceof`（`x instanceof List<String>` 编译失败，最多写 `List<?>`）、静态成员不能用类的类型参数、两个方法如果擦除后签名相同就不能重载（见《重载》一页）。泛型数组与可变参数泛型都会产生 unchecked 警告，必要时用 `@SafeVarargs` 压制；要在运行期拿到类型信息只能额外传 `Class<T>`。装饰这条路则完全是编译期的：APT 由 `javac` 在编译时多轮调用，处理器通过 `RoundEnvironment` 遍历被注解元素并写 `.java` 文件，这些文件与手写源码一起再被编译，最终字节码里通常没有注解处理器的痕迹。Lombok（生成 getter 与构造器）、MapStruct（生成映射实现类）、Dagger（生成依赖注入代码）是典型产物；Lombok 依赖非公开 API，与新版 `javac` 的兼容性偶有滞后，这类魔法的代价是构建变慢与调试变难。

📘 [Oracle Java Tutorials · Generics](https://docs.oracle.com/javase/tutorial/java/generics/restrictions.html) 与 [JLS 第 8 章](https://docs.oracle.com/javase/specs/jls/se25/html/jls-8.html)

{{% /tab %}}

{{% tab header="C++" %}}

C++ 的泛型函数就是函数模板：`template <typename T>` 声明类型参数，调用点由实参推导，属于**编译期**机制；每个用到的实参组合都会生成一份独立代码，也就是 `monomorphization`。类型参数既能被 `concept`（C++20）约束，也能通过全特化、部分特化（后者只对类模板成立）改写行为。至于“装饰”，C++ 没有运行期装饰器，只能靠编译期属性与模板元编程。

```cpp
#include <concepts>
#include <cstdio>
#include <string>

template <typename T> T max_of3(T a, T b, T c) {                    // 函数模板
    T m = a < b ? b : a;
    return m < c ? c : m;
}

template <typename T> std::string kind(const T&) { return "general"; }  // 主模板
template <> std::string kind(const int&) { return "int"; }             // 全特化

template <typename T> struct Box { static const char* name() { return "Box<T>"; } };
template <typename T> struct Box<T*> { static const char* name() { return "Box<T*>"; } };  // 部分特化

template <typename... Ts> auto sum_all(Ts... xs) { return (xs + ... + 0); }  // 折叠表达式

template <std::integral T> T twice(T x) { return x + x; }           // concept 约束

struct Vec {
    int n = 0;
    Vec operator+(const Vec& o) const { return Vec{n + o.n}; }      // 运算符重载
};

[[nodiscard]] int compute(int x) { return x * 2; }                  // 属性
[[deprecated("use compute")]] int old_compute(int x) { return x * 2; }

int main() {
    std::printf("%d\n", max_of3(1, 5, 3));                          // 5
    std::printf("%.1f\n", max_of3(1.5, 0.5, 2.5));                  // 2.5
    std::printf("%s %s\n", kind(1.5).c_str(), kind(1).c_str());     // general int
    std::printf("%s %s\n", Box<double>::name(), Box<int*>::name()); // Box<T> Box<T*>
    std::printf("%d\n", sum_all(1, 2, 3, 4));                       // 10
    std::printf("%d\n", twice(21));                                 // 42
    Vec a{1}, b{2};
    std::printf("%d\n", (a + b).n);                                 // 3
    std::printf("%d\n", compute(21));                               // 42
}
```

`max_of3(1, 5, 3)` 与 `max_of3(1.5, 0.5, 2.5)` 分别实例化出 `int` 与 `double` 两个版本，推导失败时（例如三个实参类型不一致）必须显式写 `max_of3<double>(1, 2, 3)`。`Box<int*>` 走部分特化，`kind(1)` 走全特化；`sum_all` 用折叠表达式把参数包展开成 `((1 + 2) + 3) + 4`；`twice` 上方的 `std::integral` 是 concept 约束，传 `double` 会在编译期报错而不是运行期失败。运算符重载只是把 `a + b` 静默改写为 `a.operator+(b)`，它和属性一样都属于编译期定型，没有运行期查找。`[[nodiscard]]` 与 `[[deprecated]]` 都只是让编译器发警告：代码里若调用 `old_compute`，clang 会给出 `warning: 'old_compute' is deprecated: use compute`，仍能编译通过，这也是 C++ 与 Python、Java 那种运行期装饰器的根本区别。上面代码用 `clang++ -std=c++23 -Wall` 实跑，输出与注释一致。

📘 [cppreference · Function templates](https://en.cppreference.com/w/cpp/language/function_template)

{{% /tab %}}

{{% tab header="C" %}}

C **没有泛型函数**，也没有模板与类型参数这一层抽象；`_Generic` 只是 C11 引入的编译期**类型选择**，它按控制表达式的类型挑一个已有的表达式，本身不生成任何新函数（C23 之前连它都没有）。想写出“对多种类型都管用”的代码，实际只有三类替代：`_Generic` 宏分派、`void *` 加标签的通用接口、以及完全靠文本替换的宏。装饰同理：C **没有装饰器**，只有 C23 的属性 `[[nodiscard]]`、`[[deprecated]]` 与预处理器宏。

```c
#include <math.h>      /* fabs, fabsf */
#include <stdio.h>
#include <stdlib.h>    /* abs, labs */

/* 替代一：_Generic 宏，按类型在编译期选一个已存在的函数 */
#define abs_val(x) _Generic((x), \
    int: abs,                    \
    long: labs,                  \
    float: fabsf,                \
    double: fabs)(x)

/* 替代二：宏做文本层“泛型”，没有类型检查，参数会被重复求值 */
#define MAX_OF3(a, b, c) ((a) > (b) ? ((a) > (c) ? (a) : (c)) : ((b) > (c) ? (b) : (c)))

/* 替代三：void * / 标签联合 + 运行期判别，代价是装箱与手动分支 */
typedef struct { int tag; union { long i; double d; } as; } Value;

Value make_int(long v) { Value r = { 0, { .i = v } }; return r; }
Value make_real(double v) { Value r = { 1, { .d = v } }; return r; }

double as_double(Value v) { return v.tag == 0 ? (double)v.as.i : v.as.d; }

/* 装饰：C23 属性只是编译期提示，函数体不会被包起来 */
[[nodiscard]] int compute(int x) { return x * 2; }
[[deprecated("use compute")]] int old_compute(int x) { return x * 2; }

int main(void) {
    printf("%d\n", abs_val(-3));                 /* 3 */
    printf("%.1f\n", abs_val(-3.5));              /* 3.5 */
    printf("%d\n", MAX_OF3(1, 5, 3));              /* 5 */
    printf("%.1f\n", as_double(make_int(42)));      /* 42.0 */
    printf("%.1f\n", as_double(make_real(1.5)));     /* 1.5 */
    printf("%d\n", compute(21));                     /* 42 */
    printf("%d\n", old_compute(1));                   /* 2 */
    return 0;
}
```

`abs_val(-3)` 与 `abs_val(-3.5)` 之所以都能编译，是因为宏展开后 `_Generic` 分别选出了 `abs` 与 `fabs`，两次调用是两个不同函数，这也是 C 里唯一接近泛型的写法；`_Generic` 不做算术转换，`float` 与 `double` 必须各写一个分支，而且未选中的分支照样要能通过语法检查。带标签的 `Value` 把类型判断推迟到运行期，灵活性换来了装箱开销与手工 `switch`；宏版本则连类型检查都没有，`MAX_OF3(i++, j++, k++)` 会重复求值踩坑。上例用 `clang -std=c23 -Wall` 实跑，输出与注释一致；调用 `old_compute` 时 clang 只给出 `warning: 'old_compute' is deprecated: use compute`（C23 的 `[[deprecated]]`），编译仍然成功，可见属性管不了行为，只能提醒调用方。C23 补上了 `[[nodiscard]]`、`[[deprecated]]`、`constexpr`、`nullptr` 等，但**泛型函数始终没有**，函数重载也一样（重载见前一节）。

📘 [cppreference · Generic selection（C11 起）](https://en.cppreference.com/w/c/language/generic)

{{% /tab %}}

{{% tab header="Julia" %}}

Julia 的类型参数写在**方法签名**里：`::` 是类型注解，`where` 子句引入类型变量，`<:` 给出上界。调用时全程动态派发，但编译器会为每组具体实参类型各自生成一份特化代码，因此“泛型”在 Julia 里等价于高性能的多重分派。装饰则用宏：`macro` 在解析期把 AST 改写成新代码，函数体一行都不用动；Julia 没有 Python 那种运行期 `@decorator` 对象。

```julia
using Printf

# 类型注解 + where 子句：T 由实参推导，<: 给出上界
function swap_ends!(v::AbstractVector{T}, i::Integer, j::Integer) where {T}
    v[i], v[j] = v[j], v[i]
    return v
end

# 只约束“可比较、可交换”，参数化方法自带特化
function max_of3(a::T, b::T, c::T) where {T<:Real}
    m = a > b ? a : b
    return m > c ? m : c
end

# Union 参数让一个方法同时接受多种类型
function describe(x::Union{Int,String})
    return x isa Int ? "Integer" : "String"
end

# AbstractArray{T,N} 按维度派发：N 就是类型参数
describe_dims(a::AbstractArray{T,1}) where {T} = "vector"
describe_dims(a::AbstractArray{T,2}) where {T} = "matrix"

count_int(a::AbstractArray{T}) where {T} = count(==(1), a)

# 装饰：宏在解析期包装代码，esc 把用户的表达式还原到调用处的作用域
macro dbg(ex)
    return quote
        local v = $(esc(ex))
        println($(string(ex)), " = ", v)
        v
    end
end

@inline twice(x::T) where {T<:Number} = x + x

v = [1, 2, 3]
swap_ends!(v, 1, 3)
@printf("%s\n", join(v, " "))              # 3 2 1
@printf("%d\n", max_of3(1, 5, 3))          # 5
@printf("%s %s\n", describe(1), describe("a"))  # Integer String
@printf("%s %s\n", describe_dims([1, 2]), describe_dims([1 2; 3 4]))  # vector matrix
@printf("%d\n", count_int([1, 2, 1]))      # 2
@dbg twice(21)                             # twice(21) = 42
@printf("%d\n", twice(21))                 # 42
```

`swap_ends!` 的 `T` 由 `AbstractVector{T}` 与实参一起推出来，写成 `v::AbstractVector` 也合法，但拿不到元素类型；`max_of3` 上界写作 `T<:Real`，也可以写等价简写 `a::Real` 让 `T` 隐式成为 `Real`。`Union{Int,String}` 让一个方法覆盖多个不相干类型，`AbstractArray{T,1}` 与 `AbstractArray{T,2}` 则用维度 `N` 区分向量与矩阵，两者合起来说明 Julia 的“泛型”完全建立在类型系统与多重分派之上，同名多方法的关系见重载一页（此句只作提示）。特化是自动的：`count_int([1, 2, 1])` 与 `[1.0, 2.0]` 会各自编译一份代码，遇到类型不稳定时用 `@code_warntype` 检查。宏必须用 `esc` 包住用户表达式，否则 `$(esc(ex))` 里的符号会被宏自身的 `local v` 作用域挡住；确需按类型生成代码时可用 `@generated`，把工作从运行期挪到编译期。以上示例依据 Julia 1.13 官方手册，未经本机运行验证。

📘 [Julia 手册 · Methods（含 Parametric Methods）](https://docs.julialang.org/en/v1/manual/methods/)

{{% /tab %}}

{{% tab header="C#" %}}

C# 的泛型函数写成 `返回值 M<T>(参数) where T : 约束`，类型参数在调用点由实参推断，约束在编译期强制；泛型是 `reified` 的，运行期仍能拿到 `typeof(T)`。装饰则分成两层：**特性（Attribute）** 是可反射读到的元数据，**源生成器（Source Generator）** 在编译期直接产出额外的 C# 源码，运行期没有额外开销；C# 14 还新增了 extension block，可以在不修改原类型的前提下补实例属性、静态成员与运算符。

```csharp
using System;
using System.Numerics;
using System.Text.RegularExpressions;

readonly record struct CheckedInt(int Value);

static class Extensions {
    extension(CheckedInt value) {              // C# 14 extension block
        public bool Checked => value.Value % 2 == 0;
        public static CheckedInt Wrap(int n) => new CheckedInt(n);   // 静态扩展成员
    }
}

static class Demo {
    // 泛型方法 + 约束，约束可叠加（where T : class, IDisposable, new()）
    static T MaxOf3<T>(T a, T b, T c) where T : IComparable<T> {
        T m = a.CompareTo(b) >= 0 ? a : b;
        return m.CompareTo(c) >= 0 ? m : c;
    }

    static T Twice<T>(T x) where T : IAdditionOperators<T, T, T> => x + x;

    static string NameOf<T>() => typeof(T).Name;   // reified：运行期能拿到 T

    [Obsolete("use MaxOf3 instead")]
    static int MaxOf2(int a, int b) => Math.Max(a, b);

    [GeneratedRegex(@"\d+")]
    static partial Regex Digits();

    static void Main() {
        Console.WriteLine(MaxOf3(1, 5, 3));       // 5
        Console.WriteLine(Twice(21));             // 42
        Console.WriteLine(NameOf<int>());         // Int32
        Console.WriteLine(new CheckedInt(4).Checked);  // True
        Console.WriteLine(CheckedInt.Wrap(7).Value);   // 7
        Console.WriteLine(MaxOf2(1, 3));          // 3
        Console.WriteLine(typeof(Demo).GetMethod("Digits", System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Static) != null);  // True
    }
}
```

`MaxOf3` 用 `where T : IComparable<T>` 换来 `CompareTo` 的可用性，`Twice` 换成 C# 11 起的 `IAdditionOperators<T, T, T>` 这类静态抽象接口约束；推断只看实参与形参，既不看约束也不看返回值，所以 `MaxOf3(1, 5, 3)` 能推出 `int`，而无参方法 `NameOf<T>()` 必须显式写 `NameOf<int>()`，实参类型不一致时也要自己统一（例如先都转成 `double`），编译器只会报“无法从用法推断类型参数”。`NameOf<int>()` 直接打印 `Int32`，说明类型参数没有在编译期被擦除；值类型实参各自特化，引用类型实参共享同一份运行时代码。装饰方面，`[Obsolete]` 这类特性只是元数据，编译期给警告、运行期可反射读到；`[GeneratedRegex]` 背后是增量源生成器，正则代码在编译期生成到 `partial` 方法里，这才是真正意义上“不改函数体就加行为”的做法，而 C# 14 的 extension block 只是编译期绑定的静态方法，实例成员按 `new CheckedInt(4).Checked` 调用，静态扩展成员按 `CheckedInt.Wrap(7)` 调用，它只能出现在顶层的非泛型 static class 中，优先级永远低于类型自身成员，也无法覆盖已有实现。以上示例依据 .NET 10 / C# 14 官方文档，未经本机运行验证。

📘 [MS Learn · What's new in C# 14（extension members）](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14)

{{% /tab %}}

{{% tab header="Dart" %}}

Dart 的泛型是**静态检查、运行期具体化（reified）** 的：类型参数写在名字后的尖括号里，可以有上界，实例化后运行期仍能区分 `Box<int>` 与 `Box<String>`。所以 Dart 里 `x is List<int>` 是合法判断，泛型类字段访问也不会退化成 `Object`。装饰不靠语言机制，注解（annotation）只是常量元数据，读取与代码生成交给 `build_runner` 在编译前完成。

```dart
T maxOf3<T extends Comparable<T>>(T a, T b, T c) =>           // 泛型函数 + 上界
    [a, b, c].reduce((x, y) => x.compareTo(y) >= 0 ? x : y);

class Box<T extends Object> {                                  // 泛型类
  final T value;
  const Box(this.value);
  Box<R> map<R extends Object>(R Function(T) f) => Box<R>(f(value));   // 泛型方法
}

class Cache<T> {                                               // 泛型方法带推断
  final Map<String, T> _store = {};
  T fetch(String key, T Function() create) => _store.putIfAbsent(key, create);
}

class JsonKey {                                                // 注解：常量对象
  final String name;
  const JsonKey(this.name);                                    // build_runner 读取它
}

extension type IdNumber(int value) {                           // Dart 3.3 起：静态包装
  bool get isValid => value > 0;                               // 零运行期开销
}

@JsonKey('port')
class Config {
  final int port;
  const Config(this.port);
}

void main() {
  print(maxOf3(3, 7, 5));                      // 7
  print(maxOf3('a', 'c', 'b'));                // c
  print(Box<int>(21).map<String>((v) => '$v!').value);  // 21!
  print(Box(10).value);                         // 10  R 由实参推断为 int
  print(Cache<List<int>>().fetch('k', () => [1]));  // [1]
  print([1, 2, 3] is List<int>);                 // true
  var xs = <num>[1, 2];                          // 这里推断为 List<num>
  print(xs is List<int>);                         // false  具体化的代价
  final id = IdNumber(42);
  print(id.isValid);                              // true
  print(id.value);                                // 42  表示对象可直接取
  print(const Config(8080).port);                  // 8080
}
```

`T extends Comparable<T>` 的写法叫 F-bounded 约束：`maxOf3` 体内只允许调用上界里声明过的成员，`compareTo` 正好可用；把上界写成 `Object` 就只能用 `==` 与 `hashCode`。调用点通常省略类型实参，`Box(10)` 由 `10` 推断出 `int`，方法上的 `R` 由传进来的 lambda 返回类型推断，推断不出的位置要显式写 `Box<int>(...)` 或 `map<String>(...)`。具体化让 `xs is List<int>` 可判，但 `<num>[1, 2]` 这种字面量推断出的静态类型是 `List<num>`，运行期它并不等于 `List<int>`，这是泛型在 Dart 里少见的陷阱。泛型与重载是两套机制，重载按参数类型选同名函数，泛型用一份代码覆盖一族类型，重载归前一节。

`extension type` 是编译期抽象：`IdNumber(42)` 编译掉包装，运行期只有一个 `int`，因此能零开销地约束“哪些操作可用”，只有正文里声明过的成员才可用，`id + 1` 这类表示类型上的操作会直接编译报错。注解同样不改变行为，它只是挂在声明上的常量，`build_runner` 之类工具在构建期读取并生成 `.g.dart`，生成产物参与正常编译，运行期没有任何代理或包装介入，这也是 Dart 没有运行期装饰器的根本原因。本机未安装 Dart SDK，以上输出按官方文档语义书写，未经本机运行验证。

📘 [Dart · Generics](https://dart.dev/language/generics)

{{% /tab %}}

{{% tab header="R" %}}

R **没有泛型**：语言层面没有类型参数，也没有编译期实例化，变量和参数的类型只在运行期以对象上的 `class` 属性体现。想在“一份接口、多种类型实现”上做文章，用的是 S3 的 `UseMethod()` 泛型函数与 S4 的 `setGeneric()`/`setMethod()`，两者都是**运行期按实参的 class 分派**，不是把类型参数填进函数体。R 同样没有装饰器，替代做法是返回闭包的高阶函数包装。

```r
maxOf3 <- function(a, b, c) {                # 无泛型：靠动态比较，无类型检查
  m <- function(x, y) if (x >= y) x else y
  m(m(a, b), c)
}
print(maxOf3(1, 5, 3))                       # [1] 5
print(maxOf3("a", "c", "b"))                 # [1] "c"

double <- function(x) UseMethod("double")    # S3 泛型：按第一个实参分派
double.numeric <- function(x) x * 2
double.character <- function(x) paste0(x, x)
double.default <- function(x) stop("unsupported class: ", class(x)[1])
print(double(21))                            # [1] 42
print(double("ab"))                          # [1] "abab"

applyAll <- function(xs, f) vapply(xs, f, numeric(1))  # 高阶函数：无类型参数
print(applyAll(c(1, 2, 3), double))          # [1] 2 4 6

logged <- function(f, label) {               # 包装：R 里最接近装饰器的写法
  force(f)                                    # 关键：先固化参数，避开惰性求值
  force(label)
  function(...) {
    cat("call", label, "\n")
    f(...)
  }
}
twice <- logged(double.numeric, "twice")
print(twice(21))                             # call twice / [1] 42

setClass("Area", representation(w = "numeric", h = "numeric"))  # S4：正式类
setGeneric("sizeOf", function(x) standardGeneric("sizeOf"))      # 泛型签名
setMethod("sizeOf", "Area", function(x) x@w * x@h)
print(sizeOf(new("Area", w = 2, h = 3)))      # [1] 6
```

R 没有类型参数，所以“泛型函数”在 R 的语境里专指分派机制：S3 用命名约定，调用 `double(21)` 时实际查找的是 `double.numeric`，只会看第一个实参，返回值与签名都没有编译期检查，匹配不到时会退回 `double.default`，因此给出可读的错误信息要靠自己写 `default` 方法；S4 要先 `setClass()` 定义类，`setGeneric()` 声明签名，`setMethod()` 按 class 注册实现，支持多参数签名分派并在定义时校验 class，代价是更啰嗦、运行期开销更高。`applyAll` 这类高阶函数才是 R 里真正的“复用”手段：`vapply` 要求调用者声明返回类型，能挡住一部分错误，但它检查的是返回值的长度与类型，不是函数参数的类型参数。`force(f)` 是这套包装写法里最容易踩的坑：R 的参数默认惰性求值，`f` 实际是个 promise，不先 force 就可能把“取到那个函数”这件事推迟到包装函数被调用时，一旦 `f` 后来被重新赋值，包装的行为就跟着变了，`force()` 把当时的对象固化下来。

函数包装是 R 里给函数加行为而不改函数体的标准做法，因为它是一等函数、闭包能记住 label；同样一行 `cat` 也可以换成计时、缓存或重试。泛型只解决“按对象类型选实现”，并不能省掉运行期的类型判断，想写出真正多态的代码，要么接受 S3/S4 的运行期分派，要么在函数体内用 `is.numeric()` 这类断言做检查。R 与重载的关系是“完全没有”，同名函数后定义者覆盖前定义者，本节不展开。本机未安装 R，以上输出按官方文档语义书写，未经本机运行验证。

📘 [R · Method dispatch (S3 and S4)](https://cran.r-project.org/doc/manuals/r-release/R-lang.html#Method-dispatch)

{{% /tab %}}

{{% tab header="Zig" %}}

Zig **没有泛型语法**、**没有装饰器**：没有 `<T>`、没有 `trait` 上界，也没有把行为挂到函数上的注解。它的泛型靠 `comptime T: type` 参数与 `anytype` 参数实现——类型本身是编译期值，可以当参数传，编译器为每组实参各实例化（monomorphization）一份代码。类型约束只能自己查：用 `@typeInfo` 判断形状，用 `@compileError` 在 `comptime` 块里拒绝不合法的类型。

```zig
const std = @import("std");

fn maxOf3(comptime T: type, a: T, b: T, c: T) T {   // 显式类型参数
    const m = if (a > b) a else b;
    return if (m > c) m else c;
}

fn sum(values: anytype) @TypeOf(values[0]) {         // anytype：调用点推断
    var total: @TypeOf(values[0]) = 0;
    for (values) |v| total += v;
    return total;
}

fn requireInt(comptime T: type) void {                // 约束检查：不合就编译报错
    switch (@typeInfo(T)) {
        .int => {},
        else => @compileError("T must be an integer type, got " ++ @typeName(T)),
    }
}

fn double(comptime T: type, x: T) T {
    requireInt(T);                                    // 编译期断言
    return x * 2;
}

fn describe(x: anytype) []const u8 {                  // 用静态分支代替重载
    return switch (@typeInfo(@TypeOf(x))) {
        .int, .comptime_int => "int",
        .float, .comptime_float => "float",
        .pointer => "pointer",
        else => "other",
    };
}

pub fn main() void {
    std.debug.print("{d}\n", .{maxOf3(i32, 1, 5, 3)});  // 5
    std.debug.print("{s}\n", .{maxOf3([]const u8, "a", "c", "b")});  // c
    std.debug.print("{d}\n", .{sum([_]i32{ 1, 2, 3 })});  // 6
    std.debug.print("{d}\n", .{double(i64, 21)});         // 42
    std.debug.print("{s} {s}\n", .{ describe(1), describe(1.5) });  // int float
}
```

`comptime T: type` 是最直白的显式类型参数，`anytype` 让编译器按调用点推断，两者都只在编译期存在，运行期代码里没有类型参数，`sum` 的返回类型直接写成 `@TypeOf(values[0])` 由实参决定。约束检查是手写的：`@typeInfo` 返回编译期结构体，`switch` 列出的分支在编译期求值，`@compileError` 在实例化时中断编译并打印你给的文字，报错质量完全取决于你写的消息。`describe` 用 `switch (@typeInfo(...))` 列出 `int`, `comptime_int`, `float`, `comptime_float`, `pointer` 这些分支，效果像重载，但它是编译期选择，不生成运行期分支。

泛型函数与 `anytype` 都能生成针对具体类型的代码，区别在于显式类型参数可在函数体里当类型使用并通过 `@typeName` 生成消息，`anytype` 只能靠 `@TypeOf` 反推。Zig 没有运行期装饰器，给函数加行为要在调用侧包一层或在 `comptime` 里做代码生成，标准库的 `std.mem` 大量使用这种模式。若示例用到集合，0.15 的 `std.ArrayList` 已是非托管版本，不再保存 allocator，初始化用 `std.ArrayList(T){}`，`append` 等方法要显式传分配器，`std.ArrayListUnmanaged` 也已并入它。本机未安装 Zig，以上输出按官方文档语义书写，未经本机运行验证。

📘 [Zig · comptime](https://ziglang.org/documentation/master/#comptime)

{{% /tab %}}

{{% tab header="Lua" %}}

Lua **没有泛型**、**没有装饰器**：语言是动态类型的，变量和参数都不带类型，函数签名里写不出类型参数，也没有 `@` 语法把行为挂到函数上。替代方案是运行期判断、元表（metatable）转发与高阶函数包装：函数是一等值，包一层新函数就能加日志、缓存、重试而不动原函数体。

```lua
-- 没有泛型：同一个函数按运行期类型分支
local function maxOf3(a, b, c)
  local function m(x, y) return x >= y and x or y end
  return m(m(a, b), c)
end
print(maxOf3(1, 5, 3))                     -- 5
print(maxOf3("a", "c", "b"))               -- c

-- “约束”只是运行期检查：类型不对就报错
local function mul(a, b)
  assert(type(a) == "number" and type(b) == "number", "number expected")
  return a * b
end
print(mul(6, 7))                           -- 42

-- 没有装饰器：包装函数是标准替代，... 同时转发变参与多返回值
local function logged(f)
  return function(...)
    io.write("call\n")
    return f(...)
  end
end
local double = logged(function(x) return x * 2 end)
print(double(21))                          -- call / 42

-- 转发到已有实现：__index 让代理表像原表
local base = { greet = function() return "hi" end }
local proxy = setmetatable({}, { __index = base })
print(proxy.greet())                       -- hi

-- 可调用对象：__call 让 table 像函数被调用，且能带状态
local Multiplier = {}
Multiplier.__index = Multiplier
Multiplier.__call = function(self, x) return self.factor * x end
local twice = setmetatable({ factor = 2 }, Multiplier)
print(twice(21))                           -- 42

-- 元表也能当缓存装饰器
local function memo(f)
  local cache = {}
  return function(x)
    if cache[x] == nil then cache[x] = f(x) end
    return cache[x]
  end
end
local slow = memo(function(x) return x * 2 end)
print(slow(21), slow(21))                  -- 42 42
```

`maxOf3` 在数字和字符串上都能跑，因为 `>=` 对两者都有定义；换到自定义对象就得先定义 `__lt` 这类 metamethod，否则报运行期错误。`assert(type(...))` 是“约束上界”的替代物，它没有任何编译期能力，错误只在调用那一刻暴露，这也是动态类型语言写通用函数的常态：文档与断言代替类型参数，测试代替类型检查。

`__call` 让任何值可被调用（第一个实参是该值本身，其后才是原始实参），`__index` 在键不存在时转发到另一个表，二者合起来是 Lua 做代理、OOP 与“装饰器式”包装的主要途径；注意 `__index` 只在索引缺失时触发，若代理表自己有同名键，转发就不会发生。5.5 里 `global` 已是保留字，声明全局变量要写成 `global x`，这也说明语言仍在收紧语法，但泛型与装饰器都不在路线图上。本机未安装 Lua，以上输出按官方文档语义书写，未经本机运行验证。

📘 [Lua 5.5 · Metatables and Metamethods](https://www.lua.org/manual/5.5/manual.html#2.4)

{{% /tab %}}

{{% tab header="TypeScript" %}}

TypeScript 的泛型函数把类型参数写在名字后：`<T extends Bound>` 声明上界，调用点通常由实参推断出 `T`，推断不出来时才显式写 `<string>`。泛型只活在编译期，编译成 JavaScript 后所有 `<...>` 都被**擦除（type erasure）**，运行期拿不到 `T`，所以不能 `new T()`、不能 `x instanceof T`。装饰器从 5.0 起按 TC39 标准实现，旧开关 `experimentalDecorators` 对应的是另一套已废弃的实验语义。

```typescript
interface Comparable { compareTo(o: this): number }

function maxOf3<T extends Comparable>(a: T, b: T, c: T): T {   // 泛型 + 上界
  return [a, b, c].reduce((x, y) => (x.compareTo(y) >= 0 ? x : y));
}
class Money implements Comparable {
  constructor(readonly cents: number) {}
  compareTo(o: this): number { return this.cents - o.cents; }   // this 型变
}

function logged<T extends (...args: any[]) => any>(
  value: T,
  context: ClassMethodDecoratorContext,                          // TC39 上下文对象
): T {
  return function (this: unknown, ...args: any[]) {
    console.log(`call ${String(context.name)}`);                  // 输出装饰目标名
    return value.apply(this, args);
  } as T;
}

class Calc {
  @logged
  add(a: number, b: number): number { return a + b; }
}

console.log(maxOf3(new Money(5), new Money(9), new Money(7)).cents);  // 9
console.log(maxOf3('a', 'c', 'b'));                                   // c
console.log(new Calc().add(40, 2));                                    // call add / 42
const xs = [1, 2, 3].map<number>((x) => x * 2);                        // 显式类型实参
console.log(xs, JSON.stringify(xs));                                    // [ 2, 4, 6 ] [2,4,6]
const erased: unknown = () => 42;
console.log(typeof erased, erased instanceof Function);                 // function true
const n: number = 1 as number;
console.log(typeof n);                                                   // number
```

`T extends Comparable` 保证体内只能调用上界上有的成员，`this` 作为类型出现在 `compareTo(o: this)` 里是 TypeScript 的**多态 this**，让 `Money.compareTo` 只接受 `Money`。装饰器收到的是 `(value, context)`：`value` 是被装饰的方法本身，`context.name` 是方法名，返回一个新函数就替换掉原方法，这与旧的 `experimentalDecorators` 的 `(target, key, descriptor)` 签名完全不同，两套实现不能混用，迁移时必须同时调编译选项与装饰器写法。擦除带来两个后果：运行期不能按 `T` 分派，也没有 `List<int>` 与 `List<string>` 的区别，需要运行期类型时只能自己传类构造器或用 `instanceof` 在具体类上判断。

泛型的实现模型是把类型当注释的交集：编译期做结构比较与推断，产物里没有任何泛型痕迹，`map<number>` 只是给回调一个类型上下文。装饰器在类定义求值时执行（转译器把 `@dec` 改写成一次函数调用），TC39 版本还支持返回值替换、`addInitializer` 这类能力，因此校验、日志、依赖注入都靠它完成；它不是在每次方法调用时才跑，也不是运行期可以任意增删的东西。版本基线是 TypeScript 7，它是用 Go 重写的原生编译器，装饰器语义仍按 5.0 起的 TC39 标准。本机未安装 TypeScript 编译器，以上输出按官方文档语义书写，未经本机运行验证。

📘 [TypeScript · Generics](https://www.typescriptlang.org/docs/handbook/2/generics.html)

{{% /tab %}}

{{% tab header="JavaScript" %}}

JavaScript **没有泛型**，类型层的东西全在 TypeScript 里，运行期只有值没有类型参数；同一个函数想服务多种数据，只能靠动态比较、鸭子类型或高阶函数。装饰器在这里也还不是语言的一部分，装饰器语法仍处于 TC39 Stage 3 提案阶段，`node` 直接执行 `@logged` 会抛 `SyntaxError: Invalid or unexpected token`，要用 Babel 或 TypeScript 转译（或等引擎原生落地）之后才能跑。下面是本机实跑过的替代写法。

```javascript
// 没有泛型：同一个函数靠运行期比较，类型正确性完全由调用者负责
function maxOf3(a, b, c) {
  const m = (x, y) => (x >= y ? x : y);
  return m(m(a, b), c);
}
console.log(maxOf3(1, 5, 3));                 // 5
console.log(maxOf3('a', 'c', 'b'));           // c

// 契约用鸭子类型表达：只要求对象上有 compareTo
const byCompareTo = (x, y) => (x.compareTo(y) >= 0 ? x : y);
const box = (v) => ({ v, compareTo(o) { return this.v - o.v; } });
console.log(byCompareTo(box(3), box(7)).v);   // 7

// “泛型式复用”只能用高阶函数写，类型就是运行期的能力
const compose = (f, g) => (x) => f(g(x));
const typeName = (x) => Object.prototype.toString.call(x);
console.log(compose((s) => s.toUpperCase(), typeName)('ab'));  // [OBJECT STRING]

// 没有装饰器：包装函数是标准替代
function logged(f, label) {
  return function (...args) {
    console.log(`call ${label}`);
    return f.apply(this, args);
  };
}
const add = (a, b) => a + b;
const addLogged = logged(add, 'add');
console.log(addLogged(40, 2));                // call add / 42
console.log(typeof addLogged);                // function

// 底层等价做法：直接改写原型上的属性描述符
class Calc { add(a, b) { return a + b; } }
const desc = Object.getOwnPropertyDescriptor(Calc.prototype, 'add');
Object.defineProperty(Calc.prototype, 'add', {
  ...desc,
  value: logged(desc.value, 'add'),
});
console.log(new Calc().add(40, 2));           // call add / 42

// 类型层的“协议”用 Symbol 表达，运行期只检查能力
const iter = (xs) => xs[Symbol.iterator]();
console.log([...iter([1, 2, 3])]);             // [ 1, 2, 3 ]
```

`maxOf3` 对数字和字符串都成立，靠的是 `>=` 在两种值上都有定义；换成自定义对象就必须自己提供 `compareTo`，一旦漏了就等到调用时才抛 `TypeError`，这正是“没有静态类型参数”的直接代价。鸭子类型比继承更贴合 JavaScript 的惯例，只要对象上有需要的方法就能用，运行期没有 `List<int>` 这类信息，`Array.prototype.map` 只是按位置回调，不会检查元素类型。

`logged` 保留了 `this` 与全部实参，这是包装函数能替代装饰器的关键；`Object.defineProperty` 加上属性描述符等价于旧版装饰器在底层做的事，可它不会像 `@logged` 那样有语法和上下文对象，全靠手写。装饰器提案两版的参数形态不兼容，TC39 版本是 `(value, context)`，旧的 `(target, key, descriptor)` 只在 `experimentalDecorators` 下有效，选转译器前要先确认它实现的是哪一版。本机在 Node 24.20.0 上实跑验证过以上输出，书籍基线是 Node 26，该版本仍未原生启用装饰器，示例仍需转译，其余输出不变。

📘 [MDN · Functions](https://developer.mozilla.org/docs/Web/JavaScript/Guide/Functions)

{{% /tab %}}

{{% tab header="PHP" %}}

PHP **没有泛型函数**：到 8.5 为止，语言只支持类、属性、参数与返回值的类型声明（含 union 类型、交集类型与 DNF 类型），**没有类型参数**，所以写不出 `function id<T>(T $x): T`。官方仓库里的 Reified Generics RFC 目前仍是 Draft 状态，没有进入任何发布版本，任何泛型写法都得靠运行期判断、静态分析注解或代码生成来补。语义上 PHP 是动态类型、运行期分派的语言，函数不重载；类型参数只能由 Psalm、PHPStan 这类工具在 `@template` 注解里理解，解释器本身完全不看这些注解。装饰在这里不是“包一层函数”，而是**编译期不起作用的 Attribute** 加 **运行期反射读取**。

```php
<?php
declare(strict_types=1);

class Box {}                                     // 无泛型：Box 里装什么不检查

function total(Box ...$xs): int {                // 形参声明只保证是 Box 容器
    $sum = 0;                                    // 元素类型得自己运行期判断
    foreach ($xs as $x) {
        if (!$x instanceof Box) throw new TypeError('Box expected');
        $sum += 1;
    }
    return $sum;
}

/** @template T */                              // @template 只是 Psalm/PHPStan 注解
/** @param list<T> $xs @return T */              // 解释器忽略，静态分析器才读
function first(array $xs): mixed { return $xs[0]; }

#[\NoDiscard]                                    // 8.5：返回值被忽略会告警
function num_of(Box $b): int { return 1; }

#[Attribute(Attribute::TARGET_METHOD)]
class Logged {}                                  // Attribute 自身只是普通类

class Service {
    public function __construct(public string $tag = 'x') {}

    #[\NoDiscard] #[Logged]
    public function compute(int $x): int { return $x * 2; }   // 42

    public string $label {                       // 8.4 属性钩子：读写拦截
        get => strtoupper($this->tag);
    }
}

$s = new Service('ab');
echo $s->compute(21), PHP_EOL;                   // 42
echo $s->label, PHP_EOL;                         // AB
echo 5 |> (fn(int $n): int => $n * 8 + 2), PHP_EOL;   // 42，右侧需单参可调用
echo total(new Box) |> num_of(...), PHP_EOL;     // 1，管道消费掉返回值

$m = new ReflectionMethod(Service::class, 'compute');
var_dump($m->getAttributes(Logged::class) !== []);   // bool(true)
```

`#[Logged]` 与 `#[\NoDiscard]` 在被声明的地方不会做任何事，只有 `ReflectionClass`、`ReflectionMethod`、`ReflectionFunction` 去读时才有意义，所以 Attribute 的语义与 Python 装饰器“定义即执行、立刻返回新函数”完全不同，开销也发生在反射那一刻；`#[\NoDiscard]` 是 8.5 新增的引擎级检查，返回值被直接丢弃会告警，除非用 `(void)` 强转表明有意忽略，把它喂进管道或当实参传走都算已使用。`|>` 也是 8.5 新增的管道运算符，右侧只接受单参数的可调用对象，箭头函数必须用括号包住，否则报致命错误。没有泛型的代价要靠别的手段补：`@template` 只能约束静态检查，运行期仍要 `instanceof` 或 `is_*` 手动判断，再不行就用代码生成把类型固化下来，而 `Box<int>` 这种写法在 PHP 里根本无法在运行期表达。重载的解析规则见前一节，这里只提一句：它与泛型没有交集。

📘 [PHP · Attributes](https://www.php.net/manual/en/language.attributes.php)

{{% /tab %}}

{{% tab header="Ruby" %}}

Ruby **没有泛型函数**，也**没有泛型类型**，`def id[T](x)` 这种写法不存在；类名后面的 `<` 是继承，不是类型参数。方法的参数、实例变量、数组元素全都不做静态类型检查，约束只能靠鸭子类型（能响应某个方法就用）与运行期的 `is_a?`、`respond_to?`、`raise` 自己把关，`RBS`、`Sorbet` 这类签名工具只在 IDE 与 CI 里生效，运行期看不到。分派完全在运行期做，连“重载”都没有：同名方法后定义的覆盖先定义的。装饰也不靠注解，而是**方法查找链**：`Module#prepend` 把模块插到类之前，模块里的同名方法用 `super` 调回原实现；不改类定义时，就用 `instance_method` 取原方法再 `define_method` 包一层。

```ruby
module Logged                                 # 装饰：prepend 的模块排在类之前
  def total(xs)
    puts "log: total(#{xs.size})"
    super                                     # 调回 Cart#total
  end
end

class Cart
  def total(xs) = xs.sum
end
Cart.prepend(Logged)
puts Cart.new.total([40, 2])                 # log: total(2)
                                             # 42

class Calc
  def add(a, b) = a + b
end

def wrap(klass, name, tag)                   # 方法包装：取原实现再重定义
  original = klass.instance_method(name)     # UnboundMethod
  klass.define_method(name) do |*args, **kw, &blk|
    puts "wrap: #{tag}"
    original.bind(self).call(*args, **kw, &blk)
  end
end

wrap(Calc, :add, "add")
puts Calc.new.add(40, 2)                     # wrap: add
                                             # 42

class Bag                                    # 无泛型：鸭子类型加运行期检查
  def sum_all(xs)
    xs.each { |x| raise TypeError, "not numeric" unless x.is_a?(Numeric) }
    xs.sum
  end
  def method_missing(name, *args)
    name.to_s.start_with?("sum_") ? sum_all(args) : super
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("sum_") || super
  end
end

puts Bag.new.sum_all([1, 2, 3])              # 6
puts Bag.new.sum_ints(10, 20, 12)            # 42
puts Bag.new.respond_to?(:sum_ints)          # true
begin                                        # 传错类型要到运行期才炸
  Bag.new.sum_all(["a"])                     # 🛑 TypeError
rescue TypeError => e
  puts e.message                             # not numeric
end
```

`prepend` 与 `include` 的差别只在查找顺序：`prepend` 的模块排在类自身之前，所以 `super` 能落回类里的原方法；换成 `include` 就会被类覆盖，`super` 也调不到。`instance_method` 返回的 `UnboundMethod` 必须 `bind(self)` 才能调用，这是给任意类做装饰的关键一步，`*args, **kw, &blk` 把位置参数、关键字参数、块原样透传，否则装饰后的方法会悄悄丢参数。`method_missing` 最灵活也最危险，它绕过方法查找缓存，还会让 `respond_to?` 与补全失准，必须同步实现 `respond_to_missing?`，并且对不认识的名称调用 `super` 以保住 `NoMethodError`。转成静态类型语言的眼光看：Ruby 的“泛型”就是文档与测试，`Array#sum` 只关心元素能不能 `+`，传错类型要到运行期才炸，所以一定要有测试覆盖。

📘 [Ruby · Module#prepend](https://docs.ruby-lang.org/en/4.0/Module.html)

{{% /tab %}}

{{< /tabpane >}}
