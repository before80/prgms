+++
title = "第15章 错误处理：throws、do-catch 与类型化抛出"
weight = 150
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十五章：错误处理：`throws`、`do-catch` 与类型化抛出

> 错误处理不是给代码贴创可贴，而是把“这件事可能失败”写进函数签名。Swift 用 `throws` 明确标出风险，用 `do-catch` 强迫调用者面对风险。到了 Swift 6，你还可以把失败类型收窄，让编译器和你一起守住错误边界。

## 15.1 定义错误类型

错误类型遵循 `Error` 协议。枚举最常用，因为每个失败原因都能有清楚的名字：

```swift
enum LoginError: Error {
    case emptyUsername
    case wrongPassword
    case locked(until: Int)
}
```

错误类型和普通类型一样，可以有属性、方法和关联值。关联值适合携带“为什么失败”的细节。

## 15.2 `throw` 与 `throws`

可能失败的函数在参数列表后写 `throws`：

```swift
func login(username: String, password: String) throws -> String {
    guard !username.isEmpty else {
        throw LoginError.emptyUsername
    }
    guard password == "swift" else {
        throw LoginError.wrongPassword
    }
    return "欢迎，\(username)"
}
```

调用可能抛错的函数时，必须写 `try`：

```swift
do {
    let message = try login(username: "Mia", password: "swift")
    print(message)
    // prints: 欢迎，Mia
} catch {
    print("登录失败：\(error)")
}
```

`do` 块负责尝试，`catch` 负责接住。`catch` 不会自动把错误变成 `nil`，而是给你一个明确的失败出口。

## 15.3 分类捕获

可以按错误类型或枚举分支捕获：

```swift
do {
    _ = try login(username: "", password: "swift")
} catch LoginError.emptyUsername {
    print("用户名不能为空")
    // prints: 用户名不能为空
} catch LoginError.wrongPassword {
    print("密码错误")
} catch {
    print("其他错误：\(error)")
}
```

最后一个 `catch` 是兜底，写法就像一个隐式的 `let error` 绑定。只要前面的分支没有覆盖所有错误，编译器就允许这个兜底存在。

关联值也可以匹配：

```swift
do {
    throw LoginError.locked(until: 1_800_000_000)
} catch LoginError.locked(let until) {
    print("锁定到 \(until)")
    // prints: 锁定到 1800000000
} catch {
    print(error)
}
```

## 15.4 `try?` 与 `try!`

`try?` 把成功结果包成可选值，失败变成 `nil`：

```swift
let message = try? login(username: "Mia", password: "wrong")
print(message as Any)
// prints: nil
```

`try?` 适合“失败不影响流程，只想得到有没有值”的场景。它会把具体错误信息丢掉；如果需要分类处理，必须用 `do-catch`。

`try!` 表示“失败就崩溃”，只能用于你愿意承担崩溃后果的位置：

```swift
let ok = try! login(username: "Mia", password: "swift")
print(ok)
// prints: 欢迎，Mia
```

库代码、用户输入、网络响应几乎都不应该使用 `try!`。

## 15.5 `defer`：无论成败都收尾

`defer` 在离开当前作用域时执行，成功、失败和提前 `return` 都会触发：

```swift
func readFile(name: String) throws {
    print("打开 \(name)")
    defer { print("关闭 \(name)") }
    throw LoginError.wrongPassword
}

do {
    try readFile(name: "data.txt")
} catch {
    print("处理错误：\(error)")
}
// prints: 打开 data.txt
// prints: 关闭 data.txt
// prints: 处理错误：wrongPassword
```

同一作用域里多个 `defer` 按后进先出执行。它不负责“吞掉”错误，只负责收尾。

## 15.6 `Result`：把成功或失败当作值

`Result<Success, Failure>` 是一个枚举，只有 `.success` 和 `.failure` 两种情况：

```swift
let result: Result<String, Error> = Result {
    try login(username: "Mia", password: "swift")
}

switch result {
case .success(let message):
    print(message)
    // prints: 欢迎，Mia
case .failure(let error):
    print("失败：\(error)")
}
```

`Result` 适合异步回调、任务结果或需要把错误继续传递的场景。它和 `throws` 不是竞争关系：能在函数签名中直接表达失败时，`throws` 通常更自然；需要把结果当数据存储或传递时，`Result` 更方便。

## 15.7 类型化抛出

Swift 6 允许把抛出的错误类型写进签名：

```swift
enum ParseError: Error, Equatable {
    case empty
    case notANumber(String)
}

func parse(_ text: String) throws(ParseError) -> Int {
    guard !text.isEmpty else { throw .empty }
    guard let value = Int(text) else { throw .notANumber(text) }
    return value
}

do {
    print(try parse("42"))
    // prints: 42
} catch {
    print("解析失败：\(error)")
}
```

在 `throws(ParseError)` 函数里，`catch` 的 `error` 已知类型是 `ParseError`，不需要再转换。类型化抛出让错误边界更精确，但也会让签名更强绑定；公共 API 需要谨慎选择。

类型化抛出可以配合 `catch` 的穷尽匹配：

```swift
do {
    _ = try parse("")
} catch .empty {
    print("输入为空")
    // prints: 输入为空
} catch .notANumber(let text) {
    print("不是数字：\(text)")
}
```

错误类型也可以顺着调用链往上走，中间层不需要写 `do-catch`：

```swift
func sum(_ items: [String]) throws(ParseError) -> Int {
    var total = 0
    for item in items {
        total += try parse(item)   // 出错就原样往上传，签名承诺了只会是 ParseError
    }
    return total
}

print(try sum(["1", "2", "3"]))
// prints: 6
```

如果某个函数披着 `throws` 的外衣，但永远不会真的抛错，可以写成 `throws(Never)`。此时连 `try` 都不用写：

```swift
func alwaysOK() throws(Never) -> Int { 7 }

print(alwaysOK())
// prints: 7
```

反过来，硬要给它加 `try` 会得到警告 `no calls to throwing functions occur within 'try' expression`——编译器在提醒你这句话是多余的。`throws(Never)` 主要出现在泛型代码里，用来表示“这个函数确实声明了可能抛错，但具体到这个类型就不会抛”。

一个容易踩的坑是 `Result` 与类型化抛出的配合。`Result { try ... }` 会把错误类型擦成 `any Error`：

```swift
let erased = Result { try parse("42") }
print(type(of: erased))
// prints: Result<Int, Error>
```

想保住 `ParseError`，就在 `do-catch` 里手动构造。这类 `catch` 里的 `error` 已知是 `ParseError`，所以能直接塞进 `Result`：

```swift
func parseResult(_ text: String) -> Result<Int, ParseError> {
    do {
        return .success(try parse(text))
    } catch {
        return .failure(error)      // error 的类型是 ParseError，不是 any Error
    }
}

switch parseResult("") {
case .success(let value): print("成功 \(value)")
case .failure(let error): print("失败 \(error)")
}
// prints: 失败 empty
```

## 15.8 `rethrows`：把错误原样转交

有些高阶函数自己不产生错误，只是把可能抛错的闭包执行一遍。这时可以用 `rethrows`：

```swift
func transform<T, U>(_ value: T, using body: (T) throws -> U) rethrows -> U {
    try body(value)
}

print(try transform(3) { $0 * 2 })
// prints: 6
```

`rethrows` 的意思是：闭包不抛错，函数就不会抛；闭包抛错，函数才把错误继续抛出去。这样调用者仍然需要使用 `try`，但编译器知道真正的错误来源是那个闭包。

```swift
enum WorkError: Error { case failed }

do {
    _ = try transform(3) { _ in throw WorkError.failed }
} catch {
    print("收到错误")
    // prints: 收到错误
}
```

`rethrows` 只适用于接受抛出闭包的函数；不能拿它包装任意 `throws` 操作，也不能和 `async` 混着滥用来假装处理了错误。

## 15.9 `LocalizedError`：给用户看的错误

`LocalizedError` 来自 `Foundation`（不在标准库里），可以补充错误描述、失败原因和恢复建议：

```swift
import Foundation

struct DiskError: LocalizedError {
    let path: String

    var errorDescription: String? {
        "无法读取文件：\(path)"
    }

    var recoverySuggestion: String? {
        "请检查文件是否存在，以及是否有读取权限。"
    }
}

let error = DiskError(path: "/tmp/data")
print(error.errorDescription ?? "")
// prints: 无法读取文件：/tmp/data
print(error.recoverySuggestion ?? "")
// prints: 请检查文件是否存在，以及是否有读取权限。
```

面向用户的错误应该解释“发生了什么”和“下一步怎么办”，不要把内部堆栈或敏感信息直接展示出去。

## 15.10 本章小结

| 主题 | 关键结论 |
| --- | --- |
| `Error` | 自定义错误通常用枚举并遵循该协议 |
| `throw` | 主动抛出错误，立即退出当前路径 |
| `throws` | 写进函数签名，调用者必须处理 |
| `do-catch` | 分类捕获，最后一个 `catch` 可兜底 |
| `try?` | 失败转为 `nil`，丢失具体错误 |
| `try!` | 失败即崩溃，只适合确定不会失败处 |
| `defer` | 离开作用域时执行，成功失败都触发 |
| `Result` | 把成功和失败包装成值 |
| `throws(E)` | 类型化抛出，错误类型更精确 |

## 15.11 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 调用 `throws` 函数忘记 `try` | 编译器会直接报错 |
| 用 `try?` 后又想知道失败原因 | 具体错误已被丢弃，需用 `do-catch` |
| 在库代码里使用 `try!` | 调用者可能让你的整个进程崩溃 |
| 只在成功路径释放资源 | 把释放逻辑交给 `defer` 更可靠 |
| 认为 `Result` 一定比 `throws` 好 | 看错误是否需要被当作数据保存和传递 |
| 类型化抛出签名过窄 | 之后新增一种错误就会造成破坏性修改 |
| 把内部错误直接展示给用户 | 应转换成可理解、可行动的信息 |

## 15.12 下章预告

到这里，语言的主干已经搭好。但在进入自定义类型之前，还有一批“写法上的糖”值得单独收拢一次：单表达式省 `return`、隐式 `self`、`if let` 简写、键路径当函数、`if`/`switch` 表达式、`.init` 当值……下一章把它们集中起来讲清边界，顺便纠正几个想当然的猜测（比如 Swift 并没有 `do` 表达式）。

再往后，第三篇从枚举开始进入“自定义类型的世界”。第一个要揭开的秘密，就是你从第 9 章起一直使用的可选值：`Int?` 的真身其实是一个枚举。
