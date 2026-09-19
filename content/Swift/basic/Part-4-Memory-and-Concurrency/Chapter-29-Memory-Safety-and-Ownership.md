+++
title = "第29章 内存安全与所有权：borrowing、consuming 与不可复制类型"
weight = 290
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第二十九章：内存安全与所有权：`borrowing`、`consuming` 与不可复制类型

> Swift 的内存安全不只靠 ARC，还靠独占访问和所有权规则。到了最新 Swift，类型可以明确表示“只能借出去”“可以被消费掉”“根本不能复制”。这些能力让高性能代码不必在安全和效率之间二选一。

## 29.1 独占访问：同一时间只能有一个写手

`inout` 参数在调用期间拥有独占访问权：

```swift
func modify(_ value: inout Int) {
    value += 1
}

var number = 1
modify(&number)
print(number)
// prints: 2
```

下面这种把同一个变量同时以两个 `inout` 传入的写法不允许——编译器直接拒收，因为两个"写手"谁都不知道对方在改什么：

```swift
func swap2(_ a: inout Int, _ b: inout Int) {}

var number = 1
swap2(&number, &number)
```

```text
error: inout arguments are not allowed to alias each other
```

独占访问也适用于属性、下标和 `mutating` 方法。编译器会尽量在编译期发现冲突，某些动态情况下则在运行时检查：比如函数正在写某个变量，代码又去读同一个变量，程序会当场停下并打印

```text
Simultaneous accesses to 0x..., but modification requires exclusive access.
```

宁可崩掉，也不让两个访问悄悄破坏数据——这就是"独占"两个字的全部含义。

## 29.2 `borrowing`：只借不改，也可能不复制

参数可以声明为 `borrowing`，表示函数只读取调用者的值，不需要取得所有权：

```swift
struct Config: ~Copyable {
    var name: String
}

func readName(_ config: borrowing Config) -> String {
    config.name
}

func test() {
    let config = Config(name: "app")
    print(readName(config))
}
test()
// prints: app
```

对普通可复制类型，`borrowing` 更多是优化和语义提示；对不可复制类型，它决定调用后原值是否还能使用。

## 29.3 `consuming`：把值交给函数

`consuming` 参数表示函数取得值的所有权，调用后原值可能不再可用：

```swift
struct Token: ~Copyable {
    var value: Int
}

func take(_ token: consuming Token) -> Int {
    token.value
}

func test() {
    let token = Token(value: 7)
    print(take(token))
}
test()
// prints: 7
```

在 `test()` 之后，`token` 的所有权已经交给 `take`，不能在后面继续使用。编译器会在你需要时阻止“已经消费过的值再次出场”。

“阻止”不是一句空话，它由编译器的所有权检查兜底。把 `consuming` 用在方法上，效果一样，只是语法更贴近类型设计：

```swift
struct Wallet: ~Copyable {
    var balance: Int

    borrowing func peek() -> Int { balance }        // 只看不动，原值仍然可用

    consuming func spend(_ amount: Int) -> Int {    // 花掉之后，钱包本身被消费
        balance - amount
    }
}

func demo() {
    let wallet = Wallet(balance: 100)
    print(wallet.peek())        // 借用：wallet 还在
    // prints: 100
    print(wallet.spend(30))     // 消费：wallet 在这里被吃掉，返回值是剩余额度
    // prints: 70
}
demo()
```

如果 `demo()` 里在 `spend` 之后再写一句 `print(wallet.peek())`，编译直接失败：

```text
error: 'wallet' used after consume
  note: consumed here
  note: used here
```

`borrowing` 和 `consuming` 不只是给 `~Copyable` 用的。普通可复制类型也可以声明它们，用来向调用方和编译器表达“我不会拿走你的值”或“这个值交给我了”。

## 29.4 `~Copyable`：不可复制类型

普通类型默认遵循 `Copyable`。写成 `~Copyable` 就明确关闭复制能力：

```swift
struct FileDescriptor: ~Copyable {
    let fd: Int

    init(fd: Int) { self.fd = fd }

    deinit {
        print("关闭文件描述符 \(fd)")
    }
}

func use() {
    let fd = FileDescriptor(fd: 3)
    print("使用 \(fd.fd)")
}

use()
// prints: 使用 3
// prints: 关闭文件描述符 3
```

不可复制类型适合资源句柄、唯一所有权对象和性能敏感结构。它通常配合 `borrowing`、`consuming` 参数与 `deinit` 使用，确保资源只被释放一次。

## 29.5 `consume` 与 `copy`：在调用点控制值

除了参数修饰，Swift 还给了两个**表达式级**的关键字，让你在调用点直接说明意图：

```swift
func demo() {
    let text = "hello"          // 局部常量
    let moved = consume text    // 提前结束 text 的生命周期，把值整体搬给 moved
    print(moved, moved.count)
    // prints: hello 5
}
demo()
```

`consume` 对局部变量和参数有效，用在全局变量上会报 `error: 'consume' cannot be applied to globals`——全局值是整个程序共享的，不能被你单方面搬走。

`copy` 是它的反向操作，用来显式复制一个值。它的限制正好说明了 `~Copyable` 的含义：

```text
error: 'copy' cannot be applied to noncopyable types
```

两个关键字的判断标准很朴素：**想让值提前消失用 `consume`，想强调“这里是故意复制，不是共享”用 `copy`。** 日常业务代码几乎用不到它们，但在性能敏感的循环和资源句柄代码里，它们能把“我到底把值怎么了”写在纸面上。

## 29.6 `~Escapable` 与 `Span`

有些值只允许在有限作用域内存在，不能逃逸到外部保存。这类类型使用 `~Escapable`：

```swift
let array = [1, 2, 3]
let span = array.span
print(span.count, span[0], span[span.count - 1])
// prints: 3 1 3

func total(_ span: Span<Int>) -> Int {
    var sum = 0
    for i in 0..<span.count {   // 用下标访问；越界照样当场崩，不会读到你没打算读的内存
        sum += span[i]
    }
    return sum
}

print(total(span))
// prints: 6
```

`Span` 不会复制数组，而是提供一段安全、只读的连续内存视图。它的生命周期受原数组约束——这不是“建议”，而是编译器强制的规则。两条经典报错都来自“想让视图活过被看的数据”：

```swift
func makeSpan() -> Span<Int> {
    let array = [1, 2, 3]
    return array.span       // ❌ 返回后 array 就没了，span 会指着一片空地
}
```

```text
error: a function cannot return a ~Escapable result
```

临时值同样不行，数组字面量活不过那一行：

```swift
let bytes: Span<UInt8> = [1, 2, 3].span   // ❌ 数组字面量是临时的
```

```text
error: lifetime-dependent value escapes its scope
```

想看原始字节，用 `bytes` 属性拿一个 `RawSpan`：

```swift
let numbers = [1, 2, 3]
let raw = numbers.span.bytes
print(raw.byteCount)
// prints: 24
```

三个 `Int` 占 24 字节——`RawSpan` 不问元素类型，只按字节算。`Span` 与 `RawSpan` 适合性能敏感的解析、序列化和底层互操作，不适合作为普通业务数据的默认容器。

## 29.7 `InlineArray`：固定大小、避免堆分配

`InlineArray` 用类型参数记录长度，把元素直接放进值内部：

```swift
var values = InlineArray<4, Int>(repeating: 0)
values[0] = 10
values[3] = 20
print(values.count, values[0], values[3])
// prints: 4 10 20
```

它适合长度在编译期已知、希望避免堆分配的场景，例如矩阵、图形数据和小型缓冲区。长度不再是运行时属性，而是类型的一部分。

## 29.8 所有权不是“越新越要用”

所有权特性很强大，但会提高 API 复杂度：

- `borrowing` 适合只读或不需要取得所有权的参数。
- `consuming` 适合明确转移所有权的参数。
- `~Copyable` 适合不能随意复制的资源。
- `~Escapable` 适合生命周期受限的视图。

如果普通结构体和 ARC 已经足够清楚，就不要为了“使用新语法”而把接口复杂化。所有权工具应该让资源规则更明确，而不是让调用者猜谜。

## 29.9 本章小结

| 概念 | 含义 |
| --- | --- |
| 独占访问 | 同一时间只允许一个写访问 |
| `borrowing` | 借用参数，不取得所有权 |
| `consuming` | 取得参数所有权，值可能被消费 |
| `~Copyable` | 类型不可复制，适合唯一资源 |
| `consume` / `copy` | 在调用点提前搬走值 / 显式复制值 |
| `~Escapable` | 值不能逃逸出受限生命周期 |
| `Span` | 安全、只读的连续内存视图 |
| `InlineArray` | 编译期固定大小、内联存储的数组 |

## 29.10 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 把 `borrowing` 当成引用传递的同义词 | 它表达借用语义，不保证一定无复制 |
| 消费后继续使用原值 | 编译器会阻止已消费值的使用 |
| 对全局变量写 `consume` | 全局值属于整个程序，只能消费局部值 |
| 对 `~Copyable` 类型写 `copy` | 报 `'copy' cannot be applied to noncopyable types` |
| 给普通模型加 `~Copyable` | 只在确实不能复制时使用 |
| 把 `Span` 保存到原数据生命周期之外 | `~Escapable` 会阻止这种逃逸 |
| 认为 `InlineArray` 能动态增长 | 长度是类型的一部分，固定不变 |
| 为了新语法牺牲可读性 | 所有权是精确表达工具，不是炫技 |

## 29.11 下章预告

内存与所有权的部分到此完成，接下来正式进入并发。第三十章从 `async/await`、`Task`、结构化并发和取消讲起，先把异步执行的基本节奏跑通。
