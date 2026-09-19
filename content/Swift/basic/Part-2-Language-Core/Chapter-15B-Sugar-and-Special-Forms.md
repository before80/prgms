+++
title = "第15B章 语法糖与特殊写法：语言替你少打字的地方"
weight = 151
date = "2026-09-15T09:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 15B 章：语法糖与特殊写法：语言替你少打字的地方

> 语法糖不是零食，是编译器替你省略的那几百次机械操作。这一章把散落在前面十几章里的“同一个意思，更短的写法”集中起来，也补上那些你在别人的 Swift 代码里一定会撞见、却很少有教程专门讲的特殊形式。糖要会吃，也要知道它包的到底是什么。

前面十五章是“把话说完整”，这一章是“把话说漂亮”。两者指的是同一件事，但短写法的边界更多、坑也更细。所以本章的每一节都分成两半：先给糖，再给它的底和边界。

## 15B.1 语法糖：写法不同，语义相同

语法糖（syntactic sugar）只改变代码的写法，不改变它的含义。编译器会把糖“脱糖”成底层形式再处理。所以判断一段代码是不是糖，方法很简单：能不能用另一种更长、更绕、但完全等价的方式写出来。

```swift
let sugar: [Int] = [1, 2]
let desugared: Array<Int> = [1, 2]
print(sugar == desugared, type(of: sugar) == type(of: desugared))
// prints: true true
```

`[Int]` 和 `Array<Int>` 是同一个类型的两种写法，`type(of:)` 会告诉你编译器心里的真名。理解了这一点，你就不会再把语法糖当成“另一种类型”或者“另一种语义”。

这一章之后，读到陌生写法时你可以问自己三个问题：

1. 这是什么语法糖？脱糖之后是什么？
2. 糖有没有额外约束（类型必须一致、必须穷举、必须显式标注）？
3. 省下来的字，值不值得让读者多想一想？

有些糖在前面章节已经讲过，本章不重复展开，只留一张索引表：

| 语法糖 | 哪里讲过 |
| --- | --- |
| 三元运算符 `a ? b : c` | 第 7 章 |
| 复合赋值 `+=`、`-=`、`*=`、`<<=` … | 第 7 章 |
| `typealias` 类型别名 | 第 8.5 节 |
| `is`、`as?`、`as!` | 第 8.6 节 |
| `guard` / `guard let`：`if` 加提前返回的固定套路 | 第 9.3 节 |
| `T!` 隐式解包可选值 | 第 9.7 节 |
| `try?` / `try!` | 第 15 章 |
| 枚举一行写多个用例、整数原始值自动递增、`indirect` | 第 16 章 |
| 属性包装器 `@Wrapper` 与 `$属性` | 第 19.7 节 |
| 结果构建器 `@resultBuilder`、`@ViewBuilder` | 第 15B.18 节、第 22.8 节 |
| 宏 `#Preview`、`#expect`、`@Observable`、`@Model`、`#Predicate` | 第 26 章 |
| 并发标注 `@MainActor`、`nonisolated` | 第 31、32 章 |

本章负责剩下那些“散落在各处、或者根本没人集中讲过”的部分。

## 15B.2 类型的糖：`[Int]`、`[K: V]`、`Int?`

类型层面的糖最常见，也最容易被忽略：

```swift
let a: [Int] = [1, 2, 3]
let b: Array<Int> = [1, 2, 3]
let c: Int? = 3
let d: Optional<Int> = 3
let e: [String: Int] = ["one": 1]
let f: Dictionary<String, Int> = ["one": 1]

print(a == b, c == d, e == f)
// prints: true true true
print(type(of: a), type(of: c), type(of: e))
// prints: Array<Int> Optional<Int> Dictionary<String, Int>

// 糖可以嵌套，含义就是一层层展开
let nested: [[String: Int]] = [["one": 1]]
let optionalNested: [Int?] = [1, nil]
print(nested, optionalNested.compactMap { $0 })
// prints: [["one": 1]] [1]
```

对照关系是：

| 糖 | 底层写法 | 备注 |
| --- | --- | --- |
| `[Int]` | `Array<Int>` | 数组 |
| `[String: Int]` | `Dictionary<String, Int>` | 字典 |
| `Int?` | `Optional<Int>` | 可选值 |
| `Set<Int>` | — | 没有糖，只能写全 |
| `[[Int]]` | `Array<Array<Int>>` | 嵌套没有额外规则 |

注意 `Set` 没有对应的简写，只能写全名。所以看到 `Set<Int>` 时不必惊讶：它本来就没有糖可吃。

糖到这里还没结束。`Int?` 除了省掉 `Optional<Int>` 这层名字，还自带一个很多人第一次听会愣一下的规则：**可选值不用初始化，它自己就是 `nil`**。其他所有类型都必须有初值，只有可选值是例外。

```swift
struct Profile {
    var nickname: String?      // 不用写 = nil
    var age: Int
}

let guest = Profile(age: 30)   // 逐成员初始化器直接省略了 nickname
let mia = Profile(nickname: "Mia", age: 30)
print(guest.nickname == nil, mia.nickname ?? "-")
// prints: true Mia

class Session {
    var token: String?         // 类属性同样默认 nil
}
print(Session().token == nil)
// prints: true

func local() {
    var pending: Int?          // 局部变量也不用先赋值
    print(pending == nil)
    pending = 3
    print(pending!)
}
local()
// prints: true
// prints: 3
```

两条推论值得记住：一是**可选值的“空”是语言级的默认状态**，不是靠谁赋值赋出来的；二是逐成员初始化器也会把这种默认值算进去，所以 `Profile(age: 30)` 直接可用（第 17 章会再讲逐成员初始化器的规则）。

顺手说清两件常被混在一起的事：

- `typealias UserID = Int` 只是给已有类型挂一个更好读的名字，**不会创建新类型**，所以 `UserID` 和 `Int` 可以互相当对方用（第 8.5 节）。
- `some P` 和 `any P` **不是语法糖**：前者是隐藏具体类型的不透明类型，后者是“什么都能装的盒子”，语义各不相同，只是写法都短（第 22–24 章）。

`typealias` 还能带泛型参数，专门用来给“长得吓人的嵌套类型”起短名：

```swift
typealias Pair<T> = (T, T)
typealias Handler<T> = (Result<T, any Error>) -> Void

let point: Pair<Int> = (1, 2)
let handler: Handler<String> = { print($0) }
handler(.success("done"))
print(point.0 + point.1)
// prints: success("done")
// prints: 3
```

注意它仍然是别名：`Pair<Int>` 和 `(Int, Int)` 是同一个类型，只是前者读起来更像一句话。真正的“类型包装”要靠结构体或 `struct UserID: Hashable { ... }` 这种写法，而不是别名。

## 15B.3 字面量的糖：数字与字符串的各种写法

字面量是最早接触、也最容易停在“一种写法”上的地方。第 2.5 节已经从**源码结构**的角度把它们讲全了；这里换个角度，把它们当成“写法上的糖”再收一遍，并补上两个第 2 章没有展开的细节：`type(of:)` 看到的类型，以及多行字符串的行尾续行。

数字字面量可以先“长得好看一点”：

```swift
let million = 1_000_000      // 下划线只是给人看的
let hex = 0x1F               // 十六进制：31
let binary = 0b1010          // 二进制：10
let octal = 0o17             // 八进制：15
let scientific = 1e6         // 科学计数法
let small = 1.5e-3           // 0.0015
let hexFloat = 0x1p4         // 十六进制浮点：1 × 2⁴

print(million, hex, binary, octal, scientific, small, hexFloat)
// prints: 1000000 31 10 15 1000000.0 0.0015 16.0
print(type(of: million), type(of: scientific), type(of: hexFloat))
// prints: Int Double Double
```

两点提醒：下划线**只存在于源码里**，打印出来不会有；`1e6` 是浮点字面量（默认 `Double`），想要整数就老老实实写 `1_000_000`。

字符串字面量的写法更丰富，先看转义：

```swift
let escapes = "制表\t换行\n反斜杠\\引号\"结束\0"
let smile = "\u{1F600}"      // 用 Unicode 标量写出任意字符
let accent = "\u{00E9}"

print(escapes.count, smile, accent)
// prints: 16 😀 é
print(smile.count, accent.count)
// prints: 1 1
```

`\t`、`\n`、`\\`、`\"`、`\0` 都是转义序列，`\u{...}` 则可以直接写出码位。注意最后一行：一个 emoji 也是一个 `Character`，所以它只占一个 `count`（第 5.2 节解释过 `count` 数的不是字节）。

超过一行的文本用三引号。多行字符串有个容易被忽略的规则：**结尾三引号的缩进会从所有行里被剪掉**。

```swift
let poem = """
    第一行
      第二行缩进
    第三行
    """
print(poem)
// prints: 第一行
// prints:  第二行缩进
// prints: 第三行
print(poem.split(separator: "\n").count)
// prints: 3
```

第二行前面多出来的两个空格是字符串内容的一部分：整体缩进被剪掉之后，它比兄弟行多缩进的两格就留下来了。另外，行尾写一个反斜杠可以把两行粘成一行：

```swift
let joined = """
    只有一行\
    其实是同一行
    """
print(joined)
// prints: 只有一行其实是同一行
```

最后一类：**原始字符串**。用 `#"..."#` 包起来时，反斜杠不再是转义符，插值也要多写一个井号。

```swift
let path = #"C:\Users\nick"#              // 不用再把反斜杠写成 \\
let nested = ##"里面写 #" 也没问题"##     // 井号越多，“保护层”越厚
let name = "Mia"
let greeting = #"你好，\#(name)！"#       // 井号数量要和包裹它的数量一致

print(path)
// prints: C:\Users\nick
print(nested)
// prints: 里面写 #" 也没问题
print(greeting)
// prints: 你好，Mia！
```

写正则表达式（第 6 章）、Windows 路径、或者嵌着引号的代码片段时，原始字符串能省掉一整片“反斜杠森林”。需要更多保护层就继续加井号，插值也跟着写成 `\##(...)`。

这些写法都只是词法层面的糖：`0x1F` 就是 `31`，`#"a"#` 就是 `"a"`，运行时的类型一个都没变。

## 15B.4 省掉 `return`：单表达式就是答案

当函数体、闭包、计算属性的 getter 里只有**一个表达式**时，Swift 会把它的结果直接当作返回值，`return` 可以省：

```swift
func double(_ value: Int) -> Int { value * 2 }
let twice: (Int) -> Int = { $0 * 2 }

struct Point {
    var x = 0
    var y = 0
    var magnitudeSquared: Int { x * x + y * y }
}

print(double(3), twice(3), Point(x: 3, y: 4).magnitudeSquared)
// prints: 6 6 25
```

注意“单表达式”这三个字：**多一条语句，`return` 就必须回来**。

```swift
func absolute(_ value: Int) -> Int {
    let sign = value < 0 ? -1 : 1   // 这里多了一句
    return value * sign             // 所以 return 不能省
}
print(absolute(-5))
// prints: 5
```

如果你把最后一行也写成表达式而不加 `return`，编译器不会“猜”你的意思：

```text
error: missing return in global function expected to return 'Int'
```

带 setter 的计算属性，getter 部分同样可以省 `return`；但 `set` 部分永远不产生值，所以“单表达式返回值”这套规则和它无关。

顺带纠正一个流传很广的说法：**“函数体最后是函数调用时，可以省掉圆括号”并不成立。** 能省的只有 `return`，调用处的括号必须留着：

```text
error: function produces expected type 'Int'; did you mean to call it with '()'?
```

反过来倒是有一件容易混淆的事：**不写圆括号时，你拿到的是函数本身，而不是它的返回值**。

```swift
func g() -> Int { 7 }

func f() -> Int { g() }        // 单表达式：省的是 return，括号还在
print(f())
// prints: 7

let value: () -> Int = g       // 这里“不写括号”才正确：传的是函数值
print(value())
// prints: 7
```

所以 `print(g)` 会打印 `(Function)` 而不是 `7`：它把函数当成值打印了出来。把这两件事分开，就不会被“省圆括号”这种说法带偏。

顺便说一句：`return` 写不写都不影响性能，只影响可读性。单表达式函数省掉它是 Swift 社区的普遍写法；分支多、逻辑长的函数还是老实写 `return` 更清楚。

## 15B.5 函数的语法糖

函数声明本身就有不少“能省则省”的地方，从参数标签到返回值写法都算。

**参数标签：`_` 表示调用处不要标签。** 参数标签是 Swift 让调用处“读起来像句子”的设计，`_` 就是主动放弃这句话。

```swift
func move(from start: Int, to end: Int) -> Int { end - start }
func move(_ start: Int, _ end: Int) -> Int { end - start }

print(move(from: 1, to: 4), move(1, 4))
// prints: 3 3
```

**返回 `Void` 可以整个省掉。** `Void` 就是空元组 `()`，所以下面三种写法完全等价：

```swift
func a(_ text: String) { print("a: \(text)") }          // 省略 -> Void
func b(_ text: String) -> Void { print("b: \(text)") }
func c(_ text: String) -> () { print("c: \(text)") }    // () 就是 Void

a("x")
// prints: a: x
b("y")
// prints: b: y
c("z")
// prints: c: z
```

**默认参数和可变参数：用一份声明顶掉一堆重载。**

```swift
func greet(_ name: String, greeting: String = "你好") -> String {
    "\(greeting)，\(name)"
}
print(greet("Mia"))
// prints: 你好，Mia
print(greet("Mia", greeting: "早上好"))
// prints: 早上好，Mia

func total(_ numbers: Int...) -> Int { numbers.reduce(0, +) }
print(total(), total(1), total(1, 2, 3))
// prints: 0 1 6
```

默认参数替你写了“同一个函数的好几个版本”，可变参数替你写了“参数个数不定的那些版本”。两者都别滥用：一份声明里堆三个默认值时，调用处到底传了谁就开始考验读者的记忆力了（第 13.8 节有一组小陷阱）。

**`inout` 的 `&` 是调用处的糖。**

```swift
func doubleInPlace(_ value: inout Int) { value *= 2 }

var n = 21
doubleInPlace(&n)
print(n)
// prints: 42

var x = 1, y = 2
swap(&x, &y)
print(x, y)
// prints: 2 1
```

`&` 不是“取地址”，而是“把这个变量借出去，允许函数改它”。它背后的访问规则属于第 29 章；现在只要记住：能让函数改你的变量，是调用处那个 `&` 在明说。

**方法也是值：能存起来，也能传出去。**

```swift
struct Counter {
    var count = 0
    func described() -> String { "count=\(count)" }
    static func zero() -> Counter { Counter() }
}

let bound: () -> String = Counter(count: 3).described   // 已经绑定到那个实例
print(bound())
// prints: count=3

let make: () -> Counter = Counter.zero                  // 类型方法直接当函数值
print(make().count)
// prints: 0
```

只有“绑定了具体实例”的方法值可以直接拿来用。写成 `Counter.described`（不带实例）会被编译器挡下来：

```text
error: instance member 'described' cannot be used on type 'Counter'
```

**运算符也是一种函数值。**

```swift
func apply(_ value: Int, _ transform: (Int) -> Int) -> Int { transform(value) }
func square(_ value: Int) -> Int { value * value }

print(apply(5, square), apply(5) { $0 + 1 })
// prints: 25 6

let add: (Int, Int) -> Int = (+)     // 运算符当值用，类型必须写全
print(add(1, 2))
// prints: 3
```

`(+)` 这种写法叫运算符函数引用，它和 `Int.init` 一样有个绕不开的点：重载太多，不写类型就没人知道你要哪一个。

```text
error: ambiguous use of operator '+'
```

**“返回多个值”其实是元组的糖。** 函数并没有多返回值这种能力，它返回的是一个元组，只是标签让访问更好读：

```swift
func minMax(_ values: [Int]) -> (min: Int, max: Int) {
    (values.min()!, values.max()!)
}

let result = minMax([3, 1, 2])
print(result.min, result.max, result.0)
// prints: 1 3 1
```

`.0` 和 `.min` 指的是同一个东西——这就是“标签只是元组的标签”的直接证据。

**参数上的 `some P`：泛型参数的糖。** Swift 5.7 起，参数类型写成 `some P` 就等于声明了一个匿名的泛型参数：

```swift
func describe(_ value: some BinaryInteger) -> String { "\(value)" }
print(describe(42), describe(UInt8(7)))
// prints: 42 7

// 上面这个函数和下面这个泛型版本是同一件事
func describeGeneric<T: BinaryInteger>(_ value: T) -> String { "\(value)" }
print(describeGeneric(42), describeGeneric(UInt8(7)))
// prints: 42 7
```

省下的是一个类型参数名，代价是每个 `some P` 参数**各自独立**：

```swift
func pair(_ a: some BinaryInteger, _ b: some BinaryInteger) -> String { "\(a) 和 \(b)" }
print(pair(1, UInt8(2)))          // 一个 Int、一个 UInt8，完全合法
// prints: 1 和 2

func same<T: BinaryInteger>(_ a: T, _ b: T) -> String { "\(a) 与 \(b)" }
print(same(1, 2))
// prints: 1 与 2
```

想让两个参数“必须是同一类型”，就只能退回显式泛型参数 `T`（第 23 章）。

函数相关的其他写法分散在第 13–15 章：嵌套函数（13.5）、`@discardableResult`（13.7）、`@escaping` 与捕获列表（14 章）、尾随闭包与自动闭包（本章 15B.9）。

## 15B.6 结构体的语法糖

结构体的糖主要来自两处：编译器免费送的初始化器，以及属性、方法上的一堆简写。

**逐成员初始化器：你从没写过，但它一直存在。**

```swift
struct User {
    var name: String
    var age: Int
}

let user = User(name: "Mia", age: 30)     // 这个初始化器是编译器写的
print(user.name, user.age)
// prints: Mia 30
```

规则很简单：参数顺序等于属性声明顺序，参数名等于属性名，类型等于属性类型。所以属性的声明顺序变了，调用处也得跟着改——这不是风格问题，而是编译能不能通过的问题。

**初始化器自己也没几样要写的。** 它不带 `static`（它本来就属于类型），不写返回类型，调用它时那句 `Bag(count: 2)` 其实就是 `Bag.init(count: 2)`：

```swift
struct Bag {
    var items: [String] = []
    init(count: Int) {          // 不写 static，也不写返回类型
        items = Array(repeating: "空", count: count)
    }
}

let bag = Bag(count: 2)          // 等于 Bag.init(count: 2)
print(bag.items)
// prints: ["空", "空"]

let make: (Int) -> Bag = Bag.init
print(make(1).items)
// prints: ["空"]
```

`Bag.init` 是一种特殊的函数值写法：类型名点一个 `init`，就能把初始化器当函数传递（第 15B.13 节）。

**属性有初值，参数就有默认值；所有属性都有初值时，`Foo()` 直接可用。**

```swift
struct Options {
    var retries = 3
    var verbose = false
}
print(Options().retries, Options(retries: 5, verbose: true).verbose)
// prints: 3 true

struct Player {
    let name: String              // let 属性同样会进初始化器
    var level = 1
    private(set) var score = 0    // private(set) 不改变初始化器的可见性
}
print(Player(name: "Mia").level)
// prints: 1
print(Player(name: "Bo", level: 9, score: 100).score)
// prints: 100
```

顺便说一句 `private(set)`：它是“读的权限不变、写收紧到当前作用域”的简写，只影响 setter，不影响逐成员初始化器的可见性（第 25 章）。

如果结构体里有 `private` 存储属性，编译器会调整这个初始化器：没有初值的私有属性会让它整体降级为 `private`，跨文件就构造不出来；有初值的私有属性则干脆不出现在参数表里。

```text
error: 'Token' initializer is inaccessible due to 'private' protection level
```

需要精确控制“谁能构造、怎么构造”时，写一个显式 `init` 最省心（第 17.5、20.1 节）。

**只读计算属性：`get` 和 `return` 一起省。**

```swift
struct Circle {
    var radius: Double
    var area: Double { radius * radius * 3.14159 }   // 没有 get，也没有 return
}
print(Circle(radius: 2).area)
// prints: 12.56636
```

一旦需要能写，就得把 `get` 和 `set` 都写出来——只读计算属性才有资格省成一行（第 19.1 节）。

**属性观察器有隐式参数名。**

```swift
struct Score {
    var value = 0 {
        willSet { print("将变成 \(newValue)") }     // newValue 是隐式提供的
        didSet { print("原来是 \(oldValue)") }       // oldValue 也是
    }
}
var score = Score()
score.value = 10
// prints: 将变成 10
// prints: 原来是 0
```

不想用默认名字就自己写参数（`willSet(next)`、`didSet(previous)`）。另外注意 `Score()` 里那次赋值没有触发观察器：**初始化不算“变化”**（第 19.2 节）。

**`mutating`：值类型也能原地改。**

```swift
struct Bank {
    private(set) var balance = 0
    mutating func deposit(_ amount: Int) { balance += amount }
}
var bank = Bank()
bank.deposit(100)
print(bank.balance)
// prints: 100
```

`mutating` 只属于值类型，类的方法不需要它。要是把 `var bank` 写成 `let bank`，`deposit` 立刻失去用武之地——这正是值语义在提醒你“改了就不是原来那一份了”（第 17.2、17.3 节）。

**`Self`：类型内部的“当前类型”。**

```swift
struct Point {
    var x = 0
    static var origin: Self { Self(x: 0) }
    func offset(by delta: Int) -> Self { Self(x: x + delta) }
}
print(Point.origin.x, Point(x: 1).offset(by: 2).x)
// prints: 0 3
```

写 `Self` 而不是 `Point`，类型改名时不用到处替换，子类继承后也自动指向正确的类型。

**属性包装器：一行标注，糖底下长出三个成员。** 第 19.7 节讲过怎么用属性包装器，这里补上“它到底被嚼成了什么”。写下一行 `@Clamped(0...100) var health = 80`，编译器会替你在类型里生成三样东西：一个私有的存储属性 `_health`（类型是包装器 `Clamped`）、一个转发读写到 `_health.wrappedValue` 的计算属性 `health`，以及访问 `$health` 时转发到 `_health.projectedValue` 的入口。

```swift
@propertyWrapper
struct Clamped {
    private var value: Int
    let range: ClosedRange<Int>

    var wrappedValue: Int {
        get { value }
        set { value = min(max(newValue, range.lowerBound), range.upperBound) }
    }
    var projectedValue: String { "允许范围 \(range.lowerBound)...\(range.upperBound)" }

    init(wrappedValue: Int, _ range: ClosedRange<Int>) {
        self.range = range
        self.value = min(max(wrappedValue, range.lowerBound), range.upperBound)
    }
}

struct Player {
    @Clamped(0...100) var health = 80

    func storageValue() -> Int { _health.wrappedValue }   // 同类型内部能看见底层存储
    func limitDescription() -> String { $health }         // $属性 = projectedValue
}

var player = Player()
player.health = 150                    // 走包装器的 setter，被夹到 100
let boosted = Player(health: 120)      // 逐成员初始化器里出现的是包装后的类型 Int
print(player.health, player.storageValue(), boosted.health, player.limitDescription())
// prints: 100 100 100 允许范围 0...100
```

四个容易踩的点：`= 80` 那部分初值会被当作 `wrappedValue` 传给包装器，所以包装器必须提供 `init(wrappedValue:...)`（标注里括号中的参数排在它后面）；`_health` 是 **private** 的，只有同一个类型内部（以及同文件同类型的扩展）能碰；只有包装器定义了 `projectedValue`，`$属性` 才存在；逐成员初始化器给的是外层那个“包装后”的类型，也就是这里的 `Int`，不是 `Clamped`。

**自动遵循也是糖的一种。**

```swift
func require<T: Sendable>(_ value: T) -> String { "\(type(of: value)) 是 Sendable" }
struct Measurement { var value: Double }     // 非 public 结构体自动获得 Sendable
print(require(Measurement(value: 1)))
// prints: Measurement 是 Sendable
```

`Equatable`、`Hashable`、`Codable` 的合成本章 15B.16 节会细说；`Sendable` 的完整规则在第 31 章。这里要记住的是：这些能力大多来自“结构体的成员都满足要求”，而不是你手写了多少代码。

## 15B.7 隐式 `self`：省略是常态，写出来是信号

在类型内部访问自己的属性或方法时，`self.` 通常可以省：

```swift
struct Counter {
    var count = 0
    mutating func bump() { count += 1 }
    func described() -> String { "count=\(count)" }
}
var counter = Counter()
counter.bump()
print(counter.described())
// prints: count=1
```

这个“隐式 `self`”在结构体、枚举、类里都成立。但有两种场合你**必须**把 `self` 写出来。

**第一种：名字被参数或局部变量挡住了。**

```swift
final class Node {
    var value: Int
    init(value: Int) {
        self.value = value          // 不写 self，就是把参数赋给参数
    }
    func matches(_ value: Int) -> Bool { self.value == value }
}
print(Node(value: 1).matches(1))
// prints: true
```

**第二种：闭包会逃逸，编译器要你明确说清“我要捕获这个对象”。**

```swift
final class Box {
    var value = 1
    var stored: (() -> Void)?

    func nonEscaping() {
        [1, 2].forEach { index in
            print("\(index): \(value)")      // 非逃逸闭包：可以省 self
        }
    }

    func escaping() {
        stored = { print(self.value) }        // 逃逸闭包：必须写 self
    }
}

let box = Box()
box.nonEscaping()
// prints: 1: 1
// prints: 2: 1
box.escaping()
box.stored?()
// prints: 1
```

忘了写就会看到这条报错：

```text
error: reference to property 'value' in closure requires explicit use of 'self' to make capture semantics explicit
```

规则背后的意思是：非逃逸闭包一定在函数返回前结束，不会延长 `self` 的生命；逃逸闭包会被存起来，可能让 `self` 活得更久，甚至参与循环引用（第 28 章）。所以编译器要求你在这里露一次面。

一旦你用 `[weak self]` 打破强引用，闭包里的 `self` 就变成了可选值，得先解包：

```swift
final class Loader {
    var name: String
    var onDone: (() -> Void)?
    init(name: String) { self.name = name }

    func start() {
        onDone = { [weak self] in
            guard let self else { return }     // 绑定简写也适用于 self
            print("完成：\(self.name)")
        }
    }
}
let loader = Loader(name: "任务A")
loader.start()
loader.onDone?()
// prints: 完成：任务A
```

`guard let self else { return }` 之后，下面所有代码都可以继续用不带问号的 `self`。这比每处都写 `self?.name` 干净得多，也更容易读。

## 15B.8 可选值的简写：把重复的名字去掉

可选绑定最早的写法要写两遍名字，Swift 5.7 起可以只写一遍：

```swift
struct User { var name: String }

func greet(_ user: User?) -> String {
    if let user {                          // 等于 if let user = user
        return "你好，\(user.name)"
    }
    return "你好，游客"
}
print(greet(User(name: "Mia")), "|", greet(nil))
// prints: 你好，Mia | 你好，游客

func length(_ text: String?) -> Int {
    guard let text else { return -1 }      // guard 同样适用
    return text.count
}
print(length("swift"), length(nil))
// prints: 5 -1
```

简写的前提是“名字正好一样”。想改名或者想拆包得更远处，老写法依然有效：

```swift
func firstLetter(_ text: String?) -> String {
    if let text = text, let first = text.first {   // 可以改名，也可以多个绑定并列
        return String(first)
    }
    return "?"
}
print(firstLetter("swift"), firstLetter(nil))
// prints: s ?
```

多个绑定并列时，任意一个为 `nil` 就整体走 `else`（或 `guard` 的离开路径）。这种写法比一堆嵌套 `if` 清楚得多：

```swift
func sum(_ a: Int?, _ b: Int?) -> Int {
    if let a, let b { return a + b }
    return 0
}
print(sum(1, 2), sum(nil, 2))
// prints: 3 0
```

循环里的可选值也有专门的模式：`while case let top? = stack.popLast()`，只要取出的不是 `nil` 就继续。

```swift
var stack = [1, 2, 3]
var popped: [Int] = []
while case let top? = stack.popLast() {
    popped.append(top)
}
print(popped)
// prints: [3, 2, 1]
```

日常更常见的是它的直系亲属 `while let`——绑定成功就继续，失败就收工：

```swift
var queue = ["a", "b"]
while let next = queue.popLast() {
    print("取到 \(next)")
}
print(queue.count)
// prints: 取到 b
// prints: 取到 a
// prints: 0
```

`while let` 和 `while case let x?` 做的是同一件事，区别只在“匹配的是一个具体的可选值”还是“一段模式”。名字不需要换的情况下，`while let x = x` 也能简写成 `while let x`：

```swift
var maybe: Int? = 3
while let maybe {
    print("值 \(maybe)")
    break                  // 否则会一直循环下去
}
print(maybe as Any)
// prints: 值 3
// prints: Optional(3)
```

最后是两条你每天都在用、但可能没意识到是糖的写法：`?.` 和 `??`。

```swift
struct Person { var name: String; var age: Int }
struct Company { var boss: Person? }

let company = Company(boss: Person(name: "Mia", age: 30))
print(company.boss?.name ?? "没有老板")
// prints: Mia

var maybeCompany: Company? = company
maybeCompany?.boss?.age = 31        // 可选链也能站在赋值号左边
print(maybeCompany?.boss?.age ?? 0)
// prints: 31

let primary: String? = nil
let secondary: String? = nil
print(primary ?? secondary ?? "兜底")   // ?? 可以串成一串
// prints: 兜底
```

`?.` 是“前面的值是 `nil` 就整条链短路，结果是 `nil`”；`??` 是“左边是 `nil` 就用右边”。两者都能串联，也都不会替你做类型转换——`Int?` 和 `Int` 依然是两种类型（第 9 章）。

## 15B.9 闭包与函数值的简写

闭包的简写是 Swift 代码里密度最高的地方。先说最常用的尾随闭包（trailing closure）：只要**最后一个参数是闭包**，就能把它提到圆括号外面。完整规则有四条：

1. 被提前的必须是**最后一个**参数；
2. 提到外面时，它的参数标签一并省略；
3. 如果它是**唯一的实参**，圆括号可以整个不要——`f { }` 就是 `f({ })`；
4. 如果前面还有别的实参，圆括号必须留着——`f(a) { }`。

```swift
func run(_ body: () -> Void) { body() }
run { print("A1") }          // 唯一实参：圆括号整个省掉
// prints: A1
run({ print("A2") })         // 不省也完全合法
// prints: A2

func twice(_ times: Int, _ body: () -> Void) {
    for _ in 0..<times { body() }
}
twice(2) { print("C") }      // 前面还有实参：圆括号必须留
// prints: C
// prints: C

// 带标签的单个闭包参数：尾随写法连标签一起省
func wrap(content: () -> String) -> String { "[\(content())]" }
print(wrap { "B1" }, wrap(content: { "B2" }))
// prints: [B1] [B2]
```

结构体的初始化器适用同一套规则，这正是 SwiftUI 里 `VStack { ... }` 这种写法的由来：

```swift
struct Card {
    var title: String
    var body: () -> String
}
let card = Card(title: "标题") { "正文" }
print(card.title, card.body())
// prints: 标题 正文
```

多个闭包参数时（Swift 5.3 起），第一个尾随闭包不带标签，后面几个带标签；非闭包的实参仍然留在圆括号里：

```swift
func fetch(_ id: Int, success: () -> String, onError: (Int) -> String) -> String {
    success()
}
print(fetch(1) { "ok" } onError: { "err \($0)" })
// prints: ok
print(fetch(1, success: { "ok" }, onError: { "err \($0)" }))
// prints: ok
```

如果闭包很短，参数名也可以省掉，用 `$0`、`$1` 按位置引用：

```swift
let pairs = [(2, 3), (1, 5)]
print(pairs.map { $0.0 * $0.1 })
// prints: [6, 5]
print(pairs.sorted { $0.0 < $1.0 }.map(\.1))
// prints: [5, 3]
```

`$0` 适合一到两行的短闭包。逻辑一旦超过两三行，给它起个名字会比数位置更省脑力。

还有一种反向的糖：`@autoclosure`。它把“传进来的表达式”自动包成闭包，于是调用者写的是值，拿到的却是延迟求值。

```swift
func makeMessage() -> String {
    print("（这次真的算了）")
    return "出错了"
}

func check(_ value: Int, _ message: @autoclosure () -> String) {
    if value < 0 { print(message()) }
}

check(1, makeMessage())     // 条件不成立，参数根本不会被求值
check(-1, makeMessage())    // 条件成立，才真正计算
// prints: （这次真的算了）
// prints: 出错了
```

第一次调用没有任何输出，第二次才打印两行——这就是“惰性求值”的实际手感。`@autoclosure` 用在语义清楚的地方很好，比如标准库里的 `??` 就是这么声明的：右边的默认值只在需要时才计算。用在别处则容易让调用者误判求值时机，这在第 14 章的易错点里已经提醒过。

最后是捕获列表的几种写法。方括号里可以写 `self`、写 `weak` / `unowned`，也可以顺手改名：

```swift
final class Holder {
    var name = "N"

    func make() -> [() -> String] {
        let counter = 0
        return [
            { [self] in name },                       // 显式捕获 self，类型不是可选值
            { [counted = counter] in "\(counted)" },  // 捕获时换个名字
            { [weak self] in self?.name ?? "nil" },   // 弱引用，self 变成可选值
        ]
    }
}
print(Holder().make().map { $0() })
// prints: ["N", "0", "N"]
```

`[self]` 的用处是“我确实要强引用自己，但请让我少写几次 `self.`”；`[weak self]` 与 `[unowned self]` 则是打破循环引用的两把刀，代价和适用场景在第 28 章。

## 15B.10 把运算符和键路径当值传

运算符在 Swift 里也是一种函数，所以可以直接当成值用：

```swift
let numbers = [3, 1, 2]
print(numbers.sorted(by: <))
// prints: [1, 2, 3]
print(numbers.sorted(by: >))
// prints: [3, 2, 1]
print(numbers.reduce(0, +))
// prints: 6
print(numbers.reduce(1, *))
// prints: 6
```

`sorted(by: <)` 比 `sorted { $0 < $1 }` 短，而且不会写错比较顺序。`reduce(0, +)` 同理，是求和最省字的写法。

键路径 `\.属性名` 也能当函数用，而且能一路深入：

```swift
struct Word { var text: String; var length: Int }
let words = [Word(text: "swift", length: 5), Word(text: "go", length: 2)]

print(words.map(\.text))
// prints: ["swift", "go"]
print(words.map(\.length))
// prints: [5, 2]
print(words.map(\.text.count))
// prints: [5, 2]
print([1, 2, 3].map(\.self))     // 键路径也可以只指向自己
// prints: [1, 2, 3]
```

键路径作为函数时是**单参数**的 `(根类型) -> 属性类型`。这一点决定了它的边界：它适合 `map`、`filter` 这类一元场景，但**不能**直接塞进需要两个参数的排序谓词。偷懒先试一下 `sorted(by: \.text)`：

```text
error: cannot infer key path type from context; consider explicitly specifying a root type
```

编译器一眼看出参数对不上，连“根类型是谁”都懒得猜。把根类型写全，它会换成另一句更直白的抱怨：

```swift
print(words.sorted(by: \Word.text))
```

```text
error: cannot convert key path into a multi-argument function type '(Word, Word) throws -> Bool'
```

两句话说的是同一件事：排序谓词要的是 `(元素, 元素) -> Bool`，而键路径只肯给一个参数。

排序用闭包，或者用需要导入 Foundation 的 `sorted(using:)`：

```swift
import Foundation

struct Person: Equatable { var name: String; var age: Int }
let people = [Person(name: "Mia", age: 30), Person(name: "Bo", age: 20)]
print(people.sorted(using: KeyPathComparator(\.age)).map(\.name))
// prints: ["Bo", "Mia"]
```

## 15B.11 模式匹配的简写：`if case`、`for case` 和 `where`

值绑定、区间、元组这些模式不只属于 `switch`（第 12 章已有系统介绍），它们还能直接出现在 `if`、`for`、`while` 里：

```swift
enum Event {
    case key(String)
    case click(x: Int, y: Int)
}
let events: [Event] = [.click(x: 1, y: 1), .key("a"), .key("b")]

if case .key(let k) = events[1] {       // 只关心这一种情况
    print("按键: \(k)")
}
// prints: 按键: a

for case .key(let k) in events {        // 只处理匹配的元素，其余自动跳过
    print("按键: \(k)")
}
// prints: 按键: a
// prints: 按键: b
```

`where` 则给循环或分支追加一个条件，省掉一层 `if`：

```swift
for x in 1...10 where x % 4 == 0 {
    print("where: \(x)")
}
// prints: where: 4
// prints: where: 8

func describe(_ point: (Int, Int)) -> String {
    switch point {
    case let (x, y) where x == y: return "对角线"
    default: return "其他"
    }
}
print(describe((2, 2)), describe((2, 3)))
// prints: 对角线 其他
```

让任意类型都能写进 `case`，靠的是表达式模式运算符 `~=` 的重载：

```swift
struct Even {}
func ~= (pattern: Even, value: Int) -> Bool { value % 2 == 0 }

for n in 3...4 {
    switch n {
    case Even(): print("\(n) 是偶数")
    default: print("\(n) 是奇数")
    }
}
// prints: 3 是奇数
// prints: 4 是偶数
```

一个 `case` 里可以并列多个模式，用逗号隔开：

```swift
func label(_ point: (Int, Int)) -> String {
    switch point {
    case (0, 0), (1, 1): return "特殊点"
    default: return "普通点"
    }
}
print(label((1, 1)), label((5, 5)))
// prints: 特殊点 普通点
```

但并列模式一旦涉及值绑定，**每个模式都必须绑定同一批名字**。否则编译器直接拒绝：

```text
error: 'x' must be bound in every pattern
```

这类写法请优先选择可读性，而不是把三行逻辑压成一行 `case`。

## 15B.12 表达式化的 `if` / `switch`：能出值的分支

第 11 章和第 12 章已经见过 `if` 表达式和 `switch` 表达式，这里补上它们真正的规矩。Swift 5.9 起，`if` 和 `switch` 可以直接产出值：

```swift
let score = 72
let verdict = if score >= 60 { "及格" } else { "不及格" }
print(verdict)
// prints: 及格

let grade = if score >= 90 { "优秀" } else if score >= 60 { "通过" } else { "重修" }
print(grade)
// prints: 通过

let n = -3
let sign = switch n {
case ..<0: "负"
case 0: "零"
default: "正"
}
print(sign)
// prints: 负
```

规矩有三条，每条都值得记住：

**第一，每个分支都要产出同一种类型，且 `if` 必须有 `else`、`switch` 必须穷举。** 这是“表达式必须总能算出值”的直接推论。

**第二，每个分支要么是单个表达式，要么以 `throw`（`switch` 里还可以是 `fallthrough`）结尾。** 想在分支里多写几句再产生值？不行：

```text
error: non-expression branch of 'if' expression may only end with a 'throw'
error: non-expression branch of 'switch' expression may only end with a 'throw' or 'fallthrough'
```

```swift
enum ParseError: Error { case negative }

func absolute(_ value: Int) throws -> Int {
    let result = if value < 0 {
        print("检出负数 \(value)")      // 多了一句，但结尾是 throw，所以成立
        throw ParseError.negative
    } else {
        value
    }
    return result
}

print(try absolute(4))
// prints: 4
do {
    _ = try absolute(-4)
} catch {
    print("被拒绝：\(error)")
}
// prints: 检出负数 -4
// prints: 被拒绝：negative
```

**第三，没有 `do` 表达式。** 需要“先做事、再算出值”的失败路径时，老老实实写成先声明、再赋值：

```swift
enum InputError: Error { case notANumber }

func parse(_ text: String) throws -> Int {
    guard let value = Int(text) else { throw InputError.notANumber }
    return value
}

let parsed: Int
do { parsed = try parse("42") } catch { parsed = -1 }
print(parsed)
// prints: 42
```

最后一条实用建议：分支很短时用 `if` 表达式能让代码更紧凑；分支里要写三句以上逻辑时，`if` 表达式会立刻变得难读，不如写成普通语句加一个 `return`。

## 15B.13 隐式成员与 `.init`：省略类型名

当上下文已经写明类型时，你可以只写点号和成员名，让编译器自己认出类型：

```swift
enum Color: String { case red, green, blue }

struct Style: OptionSet {
    let rawValue: Int
    static let bold = Style(rawValue: 1 << 0)
    static let italic = Style(rawValue: 1 << 1)
}

let c: Color = .red
let palette: [Color] = [.red, .blue]
let styles: Style = [.bold, .italic]
func paint(_ color: Color) -> String { color.rawValue }

print(c.rawValue, palette.map(\.rawValue), styles.contains(.italic))
// prints: red ["red", "blue"] true
print(paint(.green))
// prints: green
```

这种写法叫**隐式成员表达式**。它不只对枚举有效：任何静态成员都可以，包括 `Optional` 的 `.some` / `.none`。

```swift
// 下面两行沿用本节上面的定义，为了单独运行，这里再写一遍
enum Color: String { case red, green, blue }
struct Style: OptionSet {
    let rawValue: Int
    static let bold = Style(rawValue: 1 << 0)
    static let italic = Style(rawValue: 1 << 1)
}

let table: [String: Color] = ["warm": .red, "cool": .green]
print(table["warm"]?.rawValue ?? "nil")
// prints: red

// 从 Swift 5.4 起，隐式成员后面还能继续接成员
let combined: Style = .bold.union(.italic)
print(combined.contains(.italic), combined.rawValue)
// prints: true 3

func maybe(_ flag: Bool) -> Int? { flag ? .some(1) : .none }
print(maybe(true) ?? -1, maybe(false) ?? -1)
// prints: 1 -1
```

构造函数也能当成值来传递。当你需要一个“根据参数造对象”的函数时，不必再写一层闭包：

```swift
enum Color: String { case red, green, blue }

let make = Color.init(rawValue:)
print(make("blue")?.rawValue ?? "nil")
// prints: blue

let makeInt: (String) -> Int? = Int.init      // 这里必须写类型，否则重载无法确定
print(makeInt("42") ?? 0, makeInt("abc") ?? -1)
// prints: 42 -1
```

注意第二段里的类型标注：`Int.init` 有几十个重载，不写清楚要哪一个，编译器就不知道你在指哪个构造函数：

```text
error: ambiguous use of 'init'
```

**歧义出现时，把类型写在变量上**，比硬凑参数更省事。这也是“隐式”的另一面：能省的类型信息都是编译器已经知道的信息，一旦它不知道，就得你补上。

## 15B.14 让自定义类型长出语法：`callAsFunction`、`subscript`、字面量协议

语法糖不只属于标准库。你自己的类型也可以拥有“看起来像语言内置”的写法。第一种：实现了 `callAsFunction` 之后，实例能像函数一样加括号调用。

```swift
struct Multiplier {
    var factor: Int
    func callAsFunction(_ value: Int) -> Int { value * factor }
}
let triple = Multiplier(factor: 3)
print(triple(5), triple(10))
// prints: 15 30
```

第二种：自定义下标，让 `[]` 里的写法由你定义，包括多参数下标。

```swift
struct Matrix {
    let size: Int
    private var storage: [Int]
    init(size: Int) {
        self.size = size
        storage = Array(repeating: 0, count: size * size)
    }
    subscript(row: Int, column: Int) -> Int {
        get { storage[row * size + column] }
        set { storage[row * size + column] = newValue }
    }
}
var matrix = Matrix(size: 2)
matrix[0, 1] = 5
matrix[1, 1] = 7
print(matrix[0, 1], matrix[1, 1], matrix[0, 0])
// prints: 5 7 0
```

第三种：字面量协议。遵循 `ExpressibleByIntegerLiteral`、`ExpressibleByStringLiteral`、`ExpressibleByArrayLiteral`、`ExpressibleByDictionaryLiteral` 等协议后，你的类型也能直接用字面量初始化。

```swift
struct Money: ExpressibleByIntegerLiteral, CustomStringConvertible {
    var cents: Int
    init(integerLiteral value: Int) { cents = value * 100 }
    var description: String { "\(cents / 100) 元 \(cents % 100) 分" }
}
let price: Money = 3          // 字面量 3 被解释成 3 元
print(price)
// prints: 3 元 0 分

struct Route: ExpressibleByArrayLiteral, CustomStringConvertible {
    var stops: [String]
    init(arrayLiteral elements: String...) { stops = elements }
    var description: String { stops.joined(separator: " → ") }
}
let route: Route = ["北京", "上海", "杭州"]
print(route)
// prints: 北京 → 上海 → 杭州
```

字面量协议是把双刃剑。标准库里的 `Set<Int>` 能用 `[1, 2]` 初始化、`Int?` 能直接写 `nil`，都是同一个机制在起作用；你自己的类型也可以照着做，但 `let limit: SomeWeird = 3` 一样会让读者猜不准 `3` 到底代表什么。用之前先问自己：读者看到这个字面量，能不能立刻知道它的含义。

第四种：两个“动态”属性，让编译器在**找不到成员**时改去调用你的方法。`@dynamicMemberLookup` 负责点号后面的名字，`@dynamicCallable` 负责直接加括号调用：

```swift
@dynamicMemberLookup
struct JSON {
    private var storage: [String: String]
    init(_ storage: [String: String]) { self.storage = storage }

    subscript(dynamicMember key: String) -> String? { storage[key] }
}

let document = JSON(["name": "Mia"])
print(document.name ?? "无", document.age ?? "无")
// prints: Mia 无

@dynamicCallable
struct Adder {
    func dynamicallyCall(withArguments args: [Int]) -> Int { args.reduce(0, +) }
}
print(Adder()(1, 2, 3))
// prints: 6
```

这两个标注把“编译期能查出的拼写错误”换成了“运行时才发现是 `nil`”——`document.nmae` 不会报错，只会一路安静地返回 `nil`。所以它们的正经用途是**桥接**：包装 JSON、脚本语言对象、数据库行这类“字段名要到运行时才知道”的东西。日常类型不要用它们，那等于主动放弃编译器这个免费助手。

## 15B.15 自定义运算符与自定义字符串插值

运算符重载让自定义类型也能用 `+`、`-` 这些符号（第 7 章已介绍基础规则）：

```swift
struct Vector: Equatable {
    var x = 0.0
    var y = 0.0
    static func + (lhs: Vector, rhs: Vector) -> Vector {
        Vector(x: lhs.x + rhs.x, y: lhs.y + rhs.y)
    }
    static prefix func - (v: Vector) -> Vector { Vector(x: -v.x, y: -v.y) }
    static func += (lhs: inout Vector, rhs: Vector) { lhs = lhs + rhs }
}

var v = Vector(x: 1, y: 2) + Vector(x: 3, y: 4)
v += Vector(x: 1, y: 1)
print(v, -v)
// prints: Vector(x: 5.0, y: 7.0) Vector(x: -5.0, y: -7.0)
```

想造新符号，先用 `operator` 声明，并给它一个优先级组：

```swift
infix operator <+>: AdditionPrecedence
func <+> (lhs: String, rhs: String) -> String { "\(lhs) \(rhs)" }
print("hello" <+> "world" <+> "again")
// prints: hello world again

prefix operator ^
prefix func ^ (value: Int) -> Int { value * value }
print(^4)
// prints: 16

postfix operator ~
postfix func ~ (value: Int) -> Int { value % 10 }
let lastDigit = 125~      // 后缀运算符要紧贴操作数，不能有空格
print(lastDigit)
// prints: 5
```

字符串插值同样可以扩展。给 `String.StringInterpolation` 加一个方法，`\(...)` 就认识你的类型了：

```swift
struct Temperature {
    var celsius: Double
    var description: String { "\(celsius)℃" }
}

extension String.StringInterpolation {
    enum Style { case celsius, fahrenheit }

    mutating func appendInterpolation(_ value: Temperature, style: Style) {
        switch style {
        case .celsius:
            appendLiteral(value.description)
        case .fahrenheit:
            appendLiteral("\(Int((value.celsius * 9 / 5 + 32).rounded()))℉")
        }
    }
}

let t = Temperature(celsius: 25)
print("今天 \(t, style: .celsius)，也就是 \(t, style: .fahrenheit)")
// prints: 今天 25.0℃，也就是 77℉
```

自定义运算符和自定义插值都属于“**语法层面的 API 设计**”。它们能显著提升可读性（想想矩阵乘法），也能让代码变得只有作者本人看得懂。判断标准只有一条：看代码的人能不能不查文档就猜对含义。

## 15B.16 编译器替你写代码：自动合成与编译期字面量

有些东西你从来没写过，但它确实存在。Swift 会为遵循 `Equatable`、`Hashable`、`Codable`、`CaseIterable` 的类型**自动合成**实现。前提是成员本身也满足要求：所有存储属性都得可比、可哈希、可编解码；`CaseIterable` 的合成只对“没有关联值”的枚举有效。

```swift
import Foundation

// 原始值 + CaseIterable：枚举自己就会列出全部用例
enum Direction: String, CaseIterable {
    case north = "北", south = "南", east = "东", west = "西"
}
print(Direction.allCases.map(\.rawValue))
// prints: ["北", "南", "东", "西"]
print(Direction(rawValue: "东") == .east)
// prints: true

// Equatable / Hashable：逐字段比较、逐字段哈希
struct Coordinate: Equatable, Hashable { var x: Int; var y: Int }
print(Coordinate(x: 1, y: 2) == Coordinate(x: 1, y: 2))
// prints: true
print(Set([Coordinate(x: 1, y: 2), Coordinate(x: 1, y: 2)]).count)
// prints: 1

// Codable：编码和解码代码也是自动生成的（JSONEncoder 把值变成 JSON 数据，JSONDecoder 反过来，见第 24.9 节）
struct Note: Codable, Equatable { var title: String; var pinned: Bool }
let original = Note(title: "糖", pinned: true)
let encoded = try JSONEncoder().encode(original)
print(try JSONDecoder().decode(Note.self, from: encoded) == original)
// prints: true
```

合成的代码**按声明顺序**逐个成员处理，所以只加一个属性就可能改变编码结果的字段，也可能让 `Hashable` 的行为变化。第 16、22、24 章会分别展开这套机制的细节。

还有一条只属于**类**的默认实现：遵循 `Identifiable` 的类不用写 `id`，标准库会把 `ObjectIdentifier(self)` 给它。结构体没有这份待遇，必须自己提供 `id`。

```swift
class Scene: Identifiable {
    let name: String
    init(name: String) { self.name = name }
}

struct Item: Identifiable {
    let name: String
    var id: String { name }     // 结构体没有默认 id，得自己给
}

print(type(of: Scene(name: "客厅").id))
// prints: ObjectIdentifier
print(Item(name: "茶杯").id)
// prints: 茶杯
```

另一类“编译期就写好答案”的糖是 `#` 字面量（第 2 章介绍过它们的语义）：

```swift
func whereAmI() {
    // 下面两个字面量在编译期就被替换成常量
    print("函数名：\(#function)")
    print("行号：\(#line)")
}
whereAmI()
// prints: 函数名：whereAmI()
// prints: 行号：4
```

行号打印出来是 4，因为这条语句就在上面代码块的第四行。`#file`、`#fileID` 同理，它们记录的是“编译器看到的文件”，在 SwiftPM 里通常是模块名加文件名（第 2 章有专门说明）。

## 15B.17 零碎但常见的写法

剩下这些写法往往只在某一类场景出现，但撞见的时候容易愣住，所以集中列一下。

**标签语句**：多层循环里，`break` 和 `continue` 默认只影响最近的一层。加个标签，就能指哪打哪。

```swift
outer: for i in 1...3 {
    for j in 1...3 {
        if i * j == 4 {
            print("跳出 outer: i=\(i), j=\(j)")
            break outer
        }
    }
}
// prints: 跳出 outer: i=2, j=2

rows: for row in 1...3 {
    for column in 1...3 {
        if column == 2 { continue rows }   // 跳过这一行剩下的列，直接进入下一行
        print("\(row)-\(column)")
    }
}
// prints: 1-1
// prints: 2-1
// prints: 3-1
```

**`defer`**：注册一段“离开作用域时再执行”的代码，多个 `defer` 按注册顺序**倒着**执行（第 15 章讲过它在错误处理里的用法）。

```swift
func work(_ name: String) {
    print("打开 \(name)")
    defer { print("关闭 \(name)") }
    defer { print("记录日志 \(name)") }
    print("处理 \(name)")
}
work("文件")
// prints: 打开 文件
// prints: 处理 文件
// prints: 记录日志 文件
// prints: 关闭 文件
```

后注册的先执行，所以“关闭文件”排在“记录日志”后面——这对嵌套资源清理来说正好合适。

**`fallthrough`**：`switch` 默认匹配完就结束，想继续往下走一格，得明说。

```swift
func describe(_ level: Int) -> String {
    var text = ""
    switch level {
    case 1:
        text += "一级"
        fallthrough              // 不检查条件，直接落进下一个分支
    case 2:
        text += "+二级"
    default:
        break
    }
    return text
}
print(describe(1), describe(2))
// prints: 一级+二级 +二级
```

它有一条硬约束：**下一个分支如果绑定了变量，`fallthrough` 就过不去**。理由很直白——落下去的那个分支要用的数据，上一个分支根本没准备：

```swift
switch 1 {
case 1:
    fallthrough            // ❌ 下一个 case 要绑定 n
case let n:
    print(n)
default:
    break
}
```

```text
error: 'fallthrough' from a case which doesn't bind variable 'n'
```

**裸 `do` 块**：`do` 不一定非要配 `catch`，它也可以只是一对作用域括号，用来限制临时变量的范围。

```swift
func describe(_ flag: Bool) -> String {
    let text: String
    do {
        let inner = flag ? "开了" : "关了"   // inner 只在这个 do 块里可见
        text = inner
    }
    return text
}
print(describe(true), describe(false))
// prints: 开了 关了
```

**带标签的 `do` 块**：给 `do` 起个名字，就能用 `break` 从里面提前跳出来——比层层 `if` 更直白。

```swift
func firstEven(_ values: [Int]) -> Int? {
    scan: do {
        for value in values {
            if value % 2 == 0 { return value }
            if value > 10 { break scan }     // 整个 scan 块直接结束
        }
    }
    return nil
}
print(firstEven([1, 3, 5]) as Any, firstEven([1, 4]) as Any)
// prints: nil Optional(4)
```

**枚举本身也是糖的产地**：一行能写多个用例，整数原始值自动递增，字符串原始值默认跟用例同名，带关联值的用例还能当函数用。

```swift
enum Level: Int { case low, medium, high }      // 0, 1, 2
enum Role: String { case admin, editor }        // "admin", "editor"
print(Level.high.rawValue, Role.admin.rawValue)
// prints: 2 admin

enum Event { case key(String) }
let makeKey: (String) -> Event = Event.key      // 带关联值的用例就是函数
print(makeKey("a"))
// prints: key("a")
```

用 `indirect` 让枚举递归地表达树形结构，属于同一类“写法上的便利”，第 16 章有完整例子。

**`_` 通配**：同一个下划线，在三个不同的位置上含义完全不同——**忽略一个值**（`_ = f()`、`let (only, _) = pair`）、**放弃参数标签**（`func f(_ x: Int)`）、**匹配任意值**（模式里的 `_`）。三者的共同点是“这里有个位置，但我不打算给它起名字”，至于“忽略”还是“通配”，得看它站在哪。

```swift
_ = Int("42")                 // 明说“我知道有返回值，故意不要”
for _ in 1...2 { print("重复") }
// prints: 重复
// prints: 重复
let (only, _) = (1, 2)        // 元组解构时丢掉一个
print(only)
// prints: 1
```

**`try?` 会把双层可选压平**：如果函数本来就返回可选值，`try?` 给你的不是“可选的可选”，而是一层（[SE-0230](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0230-flatten-optional-try.md)，Swift 5 起生效）：

```swift
enum LoadError: Error { case bad }

func load(_ flag: Bool) throws -> Int? { flag ? 3 : nil }

let a = try? load(true)          // Int?，不是 Int??
let b = try? load(false)         // 成功但返回 nil，同样是 Int?
print(a as Any, b as Any, type(of: a))
// prints: Optional(3) nil Optional<Int>
```

压平很省心，代价是**“抛错了”和“正常得到 nil”从此分不出来**。需要区分这两种情况时，用 `do-catch` 加普通 `try`（第 15 章）。

**`lazy`**：`lazy var` 的初值在第一次被读取时才计算，之后只算一次。

```swift
struct Heavy {
    lazy var data: String = {
        print("开始计算")
        return "大块数据"
    }()
}
var heavy = Heavy()
print("还没用")
// prints: 还没用
print(heavy.data)
// prints: 开始计算
// prints: 大块数据
print(heavy.data)             // 第二次不会再算
// prints: 大块数据
```

三条边界值得顺手记住：`lazy` 只能挂在 `var` 上，写 `lazy let` 会得到 `'lazy' cannot be used on a let`；它只对结构体和类的**存储属性**有效，而全局变量本来就是惰性的（用到才初始化），所以全局写 `lazy` 会被拒绝：`'lazy' cannot be used on an already-lazy global`；正因为初值只算一次，`lazy` 也很适合放那些“构造一次、之后只读”的重对象。

**字典的默认下标**：`dict[key, default: 0]` 把“取值、是 `nil` 就用默认值、再写回去”三步合成一步。

```swift
var counts: [String: Int] = [:]
counts["a", default: 0] += 1
counts["a", default: 0] += 1
counts["b", default: 0] += 1
print(counts.count, counts.keys.sorted(), counts["a", default: 0])
// prints: 2 ["a", "b"] 2
```

`counts["a", default: 0] += 1` 是典型的“看着像语法、其实是标准库 API”的写法：下标本身可以带参数，`Dictionary` 只是把它用在了很顺手的地方（第 19.6 节讲怎么自己写下标）。

**尾随逗号**：Swift 6.1 起（[SE-0439](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0439-trailing-comma-lists.md)），数组、字典、元组类型、参数列表、实参列表、闭包捕获列表这些“用逗号分隔的清单”都允许在最后一项后面留一个逗号。它换来的不是更短的代码，而是更干净的 diff：加一项、删一项时只动一行，不用顺手改上一行的逗号。这个特性跟着编译器走，不挑语言模式——6.1 及以上的工具链，Swift 5 模式照样认。

```swift
let numbers = [
    1,
    2,
    3,      // 加一项、删一项时，diff 只动一行
]
print(numbers.count)
// prints: 3

func add(_ a: Int, _ b: Int) -> Int { a + b }
print(add(1, 2,))
// prints: 3

let typed: (Int, Int,) = (1, 2,)     // 类型里也能留
print(typed.0 + typed.1)
// prints: 3
```

边界只有一条：**它只对“用逗号分隔的清单”有效**。`enum` 的用例列表虽然也用逗号，但那是声明语法的一部分，末尾多一个逗号会被拒绝：

```text
error: expected identifier after comma in enum 'case' declaration
```

**链式调用与 `mutating` 的边界**：`mutating` 方法返回 `self` 时看起来可以链式调用，实际上不行——因为方法名后面那个值已经是临时值了。

```text
error: cannot use mutating member on immutable value: function call returns immutable value
```

所以“返回自身”的链式风格要么改成不修改原值的 `func ... -> Self`：

```swift
struct Account {
    var balance: Int
    func adding(_ amount: Int) -> Account {     // 不写 mutating
        var copy = self
        copy.balance += amount
        return copy
    }
}
let base = Account(balance: 100)
let after = base.adding(50).adding(25)
print(base.balance, after.balance)
// prints: 100 175
```

要么把 `@discardableResult` 的 `mutating` 方法**一句一句**调用，而不是串成一条链：

```swift
struct Query {
    private(set) var clauses: [String] = []
    @discardableResult
    mutating func select(_ columns: String...) -> Query {
        clauses.append("select \(columns.joined(separator: ", "))")
        return self
    }
    @discardableResult
    mutating func from(_ table: String) -> Query {
        clauses.append("from \(table)")
        return self
    }
}
var query = Query()
query.select("id", "name")     // 返回值不接收，也不会有警告
query.from("users")
print(query.clauses.joined(separator: " "))
// prints: select id, name from users
```

最后留一句关于异步的小糖：`async let` 让你用“像 `let` 一样”的写法并发启动子任务，再用 `await` 收结果。完整的规则和适用场景在第 30 章，这里只展示形状：

```swift
func fetch(_ id: Int) async -> String {
    try? await Task.sleep(for: .milliseconds(10))
    return "结果\(id)"
}

async let first = fetch(1)
async let second = fetch(2)
print(await [first, second].sorted())
// prints: ["结果1", "结果2"]
```

## 15B.18 结果构建器：`@ViewBuilder` 那一类“块状糖”

前面所有的糖都作用在“一行”上：省个名字、省个类型、省个圆括号。这一节讲一种作用在“一整块”上的糖——**结果构建器**（result builder）。它让一个闭包或属性里的一串语句，被编译器悄悄收集成一个值。

写过 SwiftUI 的话，你早就吃过这口糖：

```swift
import SwiftUI

struct Panel: View {
    let on: Bool
    var body: some View {          // 没有写 @ViewBuilder
        VStack {
            Text("面板")
            if on { Text("已开启") } else { Text("已关闭") }
            ForEach(1...2, id: \.self) { i in Text("行 \(i)") }
        }
    }
}

@ViewBuilder
func badge(_ on: Bool) -> some View {
    if on { Text("开") } else { Image(systemName: "xmark") }
}

print(type(of: badge(true)))
// prints: _ConditionalContent<Text, Image>
print(String(describing: type(of: Panel(on: true).body)).hasPrefix("VStack"))
// prints: true
```

`body` 里既没有 `return`，也没有数组或 `+` 拼接，却能并列写视图，还能塞进 `if` 和 `ForEach`。这不是 SwiftUI 的私有语法，而是结果构建器：`View` 协议把 `body` 这个需求声明成了 `@ViewBuilder`，于是所有实现都自动获得这套“块状糖”，自己不必再写一遍标注。`badge` 则把同一套机制用在普通函数上：函数体看着像一串视图，编译器把它们合成一个视图类型。

注意上面 `if` 的两个分支类型并不一样（`Text` 和 `Image`），这在普通函数里根本不算同一个返回值，构建器却能用 `buildEither` 把它们包进一个“二选一”的类型里。这就是 `_ConditionalContent` 的来历，也是 `some View` 能藏住千奇百怪返回类型的原因。

**脱糖之后是什么。** 构建器的本体，就是一个带 `@resultBuilder` 标注的类型；块里的每种写法对应它一个静态方法：

| 块里的写法 | 编译器要调用的方法 |
| --- | --- |
| 单个表达式 | `buildExpression(_:)`（也可以不实现，直接当块的一份子） |
| 并列的多条语句 | `buildBlock(_:)` |
| `if`（没有 `else`） | `buildOptional(_:)` |
| `if` / `else`、`switch` 的分支 | `buildEither(first:)`、`buildEither(second:)` |
| `for` / `while` 循环 | `buildArray(_:)` |
| 逐段累积结果 | `buildPartialBlock(first:)`、`buildPartialBlock(accumulated:next:)` |

不装 SwiftUI 也能亲手验证这件事。下面这个构建器把块里的字符串拼成一段文本，并且支持 `if`、`if / else` 和 `for`：

```swift
@resultBuilder
struct StringBuilder {
    static func buildBlock(_ parts: String...) -> String { parts.joined(separator: "\n") }
    static func buildOptional(_ part: String?) -> String { part ?? "" }
    static func buildEither(first: String) -> String { first }
    static func buildEither(second: String) -> String { second }
    static func buildArray(_ parts: [String]) -> String { parts.joined(separator: "\n") }
}

func text(@StringBuilder _ build: () -> String) -> String { build() }

let inStock = true
let note = text {
    "清单"
    if inStock { "有货" }
    if inStock { "立即发货" } else { "等待补货" }
    for i in 1...2 { "第 \(i) 箱" }
}
print(note.split(separator: "\n").joined(separator: " | "))
// prints: 清单 | 有货 | 立即发货 | 第 1 箱 | 第 2 箱
```

标注可以加在函数、参数、属性和协议需求上。**加在协议需求上时，遵循类型不用重写一遍**——这正是 `body` 不用写 `@ViewBuilder` 的原因：

```swift
@resultBuilder
struct PlusBuilder {
    static func buildBlock(_ parts: String...) -> String { parts.joined(separator: " + ") }
}

protocol Described {
    @PlusBuilder var text: String { get }     // 需求上标注构建器
}

struct Receipt: Described {
    var text: String {                        // 实现里不用再写标注
        "咖啡"
        "面包"
    }
}

print(Receipt().text)
// prints: 咖啡 + 面包
```

**边界与代价。**

- 构建器是纯粹的编译期行为，运行时的代码里找不到它的身影；它改变的是编译器如何把块拼起来，而不是块的语义。
- 只有被标注的地方才有这层糖。普通函数体里并列写两个表达式依然是语法错误，不会自动变成数组。
- 结果构建器不是“更高级的闭包”。它适合描述“一串同构的东西”——视图、HTML 标签、SQL 片段；拿来包装普通业务代码只会让人多读两遍。
- 自己写构建器时，方法的接收类型和返回类型必须自洽。写错时编译器的报错会非常长，读第一条 “cannot convert value of type …” 通常就够了。

## 15B.19 本章小结

| 主题 | 糖 | 边界与代价 |
| --- | --- | --- |
| 类型写法 | `[Int]`、`[K: V]`、`Int?` | 与 `Array`、`Dictionary`、`Optional` 完全等价 |
| 字面量 | `1_000_000`、`0x1F`、`1e6`、多行字符串、`#"..."#` | 只是词法写法，类型不变；原始字符串里插值要写 `\#(...)` |
| 返回值 | 单表达式省 `return` | 多一条语句就得写回来 |
| 函数 | `_` 标签、默认参数、可变参数、`&`、方法当值、`(+)`、`some P` 参数 | 默认值太多会难读；未绑定方法引用不可用；每个 `some P` 各自独立 |
| 结构体 | 逐成员初始化器、`Foo()`、观察器隐式名字、`mutating`、`Self` | `private` 属性会改变初始化器的可见性或参数表 |
| 属性包装器 | `@W var x = v` 同时长出 `_x`、`x`、`$x` 三个成员 | `_x` 是 private；`$x` 取决于 `projectedValue`；初值走 `init(wrappedValue:)` |
| `self` | 隐式 `self` | 名字冲突或逃逸闭包中必须写出 |
| 可选绑定 | `if let x`、`guard let x`、`while let x`、`while case let x?` | 简写要求名字一致；改名用老写法；`try?` 会把双层可选压平 |
| 闭包 | 尾随闭包、`$0`、`@autoclosure`、`[self]`、`[weak self]` | `$0` 只在短闭包里清晰；自动闭包会隐藏求值时机 |
| 函数值 | `sorted(by: <)`、`reduce(0, +)`、`map(\.count)` | 键路径是单参数函数，不能当 `sorted(by:)` 谓词 |
| 模式匹配 | `if case`、`for case`、`where`、自定义 `~=` | 并列模式必须绑定同一批名字 |
| 枚举 | 一行多用例、原始值自动生成、用例当函数值、`indirect` | 关联值、原始值各有规则，见第 16 章 |
| 表达式化控制流 | `if`/`switch` 表达式 | 必须有 `else`/穷举；分支只能是单表达式或以 `throw` 结束；**没有 `do` 表达式** |
| 隐式成员 | `.red`、`.bold.union(.italic)`、`.init` | 上下文缺类型信息时会歧义，需显式标注 |
| 自定义语法 | `callAsFunction`、`subscript`、字面量协议、运算符、插值 | 能力越强越要克制，可读性优先 |
| 动态成员 | `@dynamicMemberLookup`、`@dynamicCallable` | 把拼写错误推迟到运行时，只适合桥接层 |
| 自动合成 | `Equatable`、`Hashable`、`Codable`、`CaseIterable` | 成员顺序会进入合成结果 |
| 结果构建器 | `@resultBuilder`、`@ViewBuilder`、块里的 `if` / `switch` / `for` | 只在被标注的块里生效；分支类型不同会被包进 `_ConditionalContent` 之类的内部类型 |
| 零碎写法 | 标签语句、`defer`、`fallthrough`、`_`、裸 `do`、标签 `do`、`lazy`、`try?`、尾随逗号、字典默认下标 | 各有使用场合，不是“越短越好”；`_` 在三种位置含义不同 |

## 15B.20 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 以为 `[Int]` 和 `Array<Int>` 是两种类型 | 同一个类型，只是写法长短不同 |
| 以为 `1_000_000` 里的下划线会出现在结果里 | 下划线只是写给人看的，值就是 1000000 |
| 在 `#"..."#` 里直接写 `\(name)` | 原始字符串要用 `\#(name)`，井号数量与包裹层一致 |
| 多语句函数体里忘了 `return` | 只有单表达式才允许省略 |
| 以为“函数体最后是函数调用”能省圆括号 | 能省的只有 `return`；`func h() -> Int { g }` 会报 `did you mean to call it with '()'` |
| 以为尾随闭包只在“唯一实参”时可用 | 闭包是最后一个参数就能尾随；圆括号要不要留，取决于前面还有没有别的实参 |
| 以为“返回多个值”是语言特性 | 返回的是元组，标签只是元组的标签 |
| 把 `Counter.described` 当成函数值 | 未绑定方法引用不可用，要传绑定实例的那个值 |
| `let add = (+)` | 运算符重载同样会歧义，必须写出函数类型 |
| 以为所有闭包都能省 `self` | 逃逸闭包必须显式写 `self` |
| `[weak self]` 后仍直接写 `self.name` | `self` 已是可选值，需 `guard let self` 或 `self?` |
| 把 `sorted(by: \.count)` 当成合法写法 | 键路径是单参数函数，双参数谓词要写闭包或用 `sorted(using:)` |
| 以为 `if case`、`for case` 是 `switch` 的替代品 | 它们处理“只关心一种情况”的轻量场景 |
| 在并列 `case` 里只给部分模式绑定名字 | 每个模式都要绑定同一批名字 |
| 在 `if` 表达式分支里写多句语句 | 只允许单表达式，或用 `throw`（`switch` 里可 `fallthrough`）结尾 |
| 期待 `do` 表达式能产出值 | Swift 没有实现它，用普通语句或 `Result` 代替 |
| `let make = Int.init` | 构造函数重载会歧义，把类型标注写出来 |
| 把 `mutating` 方法串成一条链 | 需要可变的左值，链式风格请改成返回新值或分句调用 |
| 忘记后缀运算符要紧贴操作数 | `125~` 合法，`125 ~` 会被解析成别的东西 |
| 到处用自定义运算符和自定义插值 | 糖的目的是更好读，不是更好写 |
| 以为结构体的逐成员初始化器永远能用 | `private` 存储属性会让它降级，或把该属性排除出参数表 |
| 在 `let` 结构体上调用 `mutating` 方法 | 值类型的 `let` 实例不允许被改动 |
| 以为属性包装器的 `$属性` 一定存在 | 只有包装器定义了 `projectedValue` 才有（第 19.7 节） |
| 把包装器的 `_属性` 当成公开接口 | 它是 private 的底层存储，同类型内部才能碰；要对外就靠 `projectedValue` |
| 以为 `try? f()` 会得到“双层可选” | 从 Swift 5 起已经压平；同时也意味着“抛错”和“返回 nil”再也分不出来 |
| 以为 `lazy` 哪儿都能写 | 只能用于结构体/类的存储属性：`lazy let` 和全局变量都会被编译器拒绝 |
| 以为 `fallthrough` 可以去任何分支 | 下一个分支一旦绑定变量就会被拒绝：`'fallthrough' from a case which doesn't bind variable 'n'` |
| 在 `enum` 用例列表末尾也加尾随逗号 | 尾随逗号只对“逗号分隔的清单”生效，声明语法会报 `expected identifier after comma in enum 'case' declaration` |
| 以为可选值必须初始化 | 可选值是唯一的例外，属性、局部变量都自动是 `nil` |
| 以为 `body` 里能并列写视图是 SwiftUI 的“魔法语法” | 那是 `@ViewBuilder` 这个结果构建器的效果，属于 Swift 语言特性 |
| 在没标注 `@resultBuilder` 的函数体里并列写多个表达式 | 普通函数没有这层糖，必须用数组、`+` 或显式收集 |
| 看到 `_ConditionalContent<Text, Image>` 之类类型名就慌 | 那是构建器给“二选一分支”生成的真实类型，`some View` 平时替你藏起来了 |

## 15B.21 下章预告

语言主干的糖已经吃完了。第三篇开始，我们要自己造类型。第一站是枚举：它不只是“一组常量”，而是能携带数据、能递归、能自动合成一批能力的完整类型系统成员——顺便说，你从第 9 章起一直在用的 `Int?`，真身就是它。
