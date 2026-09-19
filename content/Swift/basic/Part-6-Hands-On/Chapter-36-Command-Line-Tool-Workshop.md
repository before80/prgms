+++
title = "第36章 命令行工具实战：做一个记事本 CLI"
weight = 360
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "从零做一个待办记事本命令行工具：分层结构、参数解析、持久化、错误设计与退出码"
isCJKLanguage = true
draft = false
+++

# 第三十六章：命令行工具实战：做一个记事本 CLI

> 命令行工具是练习 Swift 工程能力的好场地：没有界面可以躲，输入、输出、持久化、错误和退出码都摆在明面上。这一章做一个可以添加、列出和完成待办事项的小工具，把前面的语法、包管理和错误处理串起来。

## 36.1 先把"壳"搭出来

从零开始的好处是你能看清每一层是什么时候被加进去的。第一条命令生成骨架：

```bash
swift package init --type executable --name TodoCLI
```

生成的目标里会自带一个 `main.swift`。我们不打算把它堆成"一个文件写完"，所以先规划好分层，再往里面填文件：

```text
Sources/TodoCLI/
  TodoCLIApp.swift    ← 入口，只负责"把零件装起来"
  TodoItem.swift      ← 模型
  TodoStore.swift     ← 存储
  CommandParser.swift ← 参数解析
```

为什么入口文件叫 `TodoCLIApp.swift` 而不是默认的 `main.swift`？因为下面要用 `@main` 标注入口类型，而**一个名为 `main.swift` 的文件本身就是顶层代码入口，两者不能共存**：

```text
error: 'main' attribute cannot be used in a module that contains top-level code
note: top-level code defined in this source file
```

这个报错只有在"target 里还有别的文件"时才会出现——单文件项目里 `@main` 侥幸能编过，一旦拆成多个文件立刻失败。所以规则记简单一点：**用 `@main` 就别叫 `main.swift`；想叫 `main.swift` 就别用 `@main`。**

## 36.2 数据模型：一行都别多写

模型层只回答一个问题："一条待办长什么样？"

```swift
import Foundation

struct TodoItem: Codable, Identifiable, Equatable {
    let id: UUID
    var title: String
    var isDone: Bool

    init(id: UUID = UUID(), title: String, isDone: Bool = false) {
        self.id = id
        self.title = title
        self.isDone = isDone
    }
}
```

三个协议各有明确分工，不是顺手加的：

| 协议 | 它买到什么 |
| --- | --- |
| `Codable` | 直接读写 JSON，不用手写编解码 |
| `Identifiable` | 拿到稳定的 `id`；将来接 SwiftUI 的 `List` 可以直接用 |
| `Equatable` | 测试里能写 `#expect(item == expected)`，而不是逐字段比对 |

注意 `id` 是 `let`、`title` 和 `isDone` 是 `var`：**身份一旦确定就不再改变**（这正是第 43 章反复强调的那条规则），可变的是内容。

## 36.3 存储层：把"文件"关在一个盒子里

读写文件的代码最容易渗透到项目的每个角落，所以第一件事就是把它关进一个类型里：

```swift
import Foundation

struct TodoStore {
    let fileURL: URL

    init(fileURL: URL) {
        self.fileURL = fileURL
    }

    func load() throws -> [TodoItem] {
        guard FileManager.default.fileExists(atPath: fileURL.path) else {
            return []      // 第一次运行还没有文件，这不是错误
        }
        let data = try Data(contentsOf: fileURL)
        return try JSONDecoder().decode([TodoItem].self, from: data)
    }

    func save(_ items: [TodoItem]) throws {
        let data = try JSONEncoder().encode(items)
        try data.write(to: fileURL, options: .atomic)
    }
}
```

这段代码里有两处刻意的设计：

- **文件不存在返回空数组，而不是抛错。** "还没有数据"和"数据读不出来"是两回事，把它们混成一个错误，会让第一次运行的用户看到一条吓人的报错。
- **写文件用 `.atomic`。** 它先写临时文件、写成之后再替换原文件，所以不会出现"写到一半进程被 Ctrl+C 掉，文件变成半截 JSON"的惨案。

真实项目里还要继续处理三件事：文件权限、多进程并发写、以及数据结构变化后的版本迁移。这三件事本章都会简单提一下写法，但不会全部实现——重要的是你**知道它们存在**。

## 36.4 参数解析：先把字符串变成"命令"

最原始的参数来源是 `CommandLine.arguments`，它是个字符串数组，第一个元素是程序路径。解析的目标是把它变成类型化的 `Command`：

```swift
import Foundation

enum Command {
    case add(String)
    case list
    case done(String)
}

func parse(_ arguments: [String]) throws -> Command {
    guard let name = arguments.first else {
        return .list            // 不带任何参数时，默认列出全部
    }

    switch name {
    case "add":
        guard arguments.count >= 2 else { throw CLIError.missingTitle }
        return .add(arguments[1])
    case "list":
        return .list
    case "done":
        guard arguments.count >= 2 else { throw CLIError.missingID }
        return .done(arguments[1])
    default:
        throw CLIError.unknownCommand(name)
    }
}
```

两个值得留意的细节：

- **`guard arguments.count >= 2` 在读取 `arguments[1]` 之前。** 顺序反了就是数组越界崩溃，而崩溃对用户来说是最差的报错方式——他既不知道哪里错了，也拿不到任何提示。
- **`throw` 而不是 `print` 再 `return`。** 解析函数只负责"判断合不合法"，怎么告诉用户是上层的事。这样解析函数可以被测试，也可以被另一个界面（比如 GUI）复用。

错误类型单独定义，并且让它负责"说人话"：

```swift
import Foundation

enum CLIError: Error, CustomStringConvertible {
    case missingTitle
    case missingID
    case unknownCommand(String)
    case notFound(String)

    var description: String {
        switch self {
        case .missingTitle: "请提供标题：todo add \"买牛奶\""
        case .missingID: "请提供 ID：todo done <id>"
        case .unknownCommand(let name): "未知命令：\(name)"
        case .notFound(let id): "找不到项目：\(id)"
        }
    }
}
```

`CustomStringConvertible` 是这里的关键：实现了 `description` 之后，`"\(error)"` 就会输出这句话，主程序里那句 `fputs("error: \(error)\n", stderr)` 不需要写任何 `switch`。**把"错误说什么"放进错误类型自己身上，是 Swift 里最省事的一种分层。**

参数再多一些（子命令嵌套、`--help`、补全），手写就该淘汰了，换成官方的 [`swift-argument-parser`](https://github.com/apple/swift-argument-parser)。判断时机很简单：**当你开始为"解析"写测试、或者开始复制粘贴解析代码时。**

## 36.5 主程序：把零件装起来

入口只做三件事：准备零件、分发命令、兜住错误。

```swift
import Foundation

@main
struct TodoCLI {
    static func main() {
        do {
            let home = FileManager.default.homeDirectoryForCurrentUser
            let store = TodoStore(fileURL: home.appending(path: ".todo.json"))
            var items = try store.load()
            let command = try parse(Array(CommandLine.arguments.dropFirst()))

            switch command {
            case .add(let title):
                let item = TodoItem(title: title)
                items.append(item)
                try store.save(items)
                print("added: \(item.title)")

            case .list:
                for item in items {
                    let mark = item.isDone ? "x" : " "
                    print("[\(mark)] \(item.title)  \(item.id)")
                }

            case .done(let id):
                guard let index = items.firstIndex(where: { $0.id.uuidString == id }) else {
                    throw CLIError.notFound(id)
                }
                items[index].isDone = true
                try store.save(items)
                print("done: \(items[index].title)")
            }
        } catch {
            fputs("error: \(error)\n", stderr)
            exit(1)
        }
    }
}
```

三个值得逐句解释的地方：

- **`CommandLine.arguments.dropFirst()`**：数组第一个元素是程序自身的路径（比如 `.build/debug/TodoCLI`），解析时必须丢掉，否则每个命令都会被当成 `unknownCommand`。
- **`items[index].isDone = true`**：`TodoItem` 是结构体，所以这里是"替换数组里的那个值"，而不是"改一个共享对象"。这正是第 17 章值语义在实战里的样子。
- **`do { } catch { }` 包住整个流程**：任何一步抛错都会落到同一个出口，不会出现"某处忘了处理错误，程序带着半截状态继续跑"。

跑起来是这样：

```bash
$ swift run TodoCLI add "写 Swift 教程"
added: 写 Swift 教程

$ swift run TodoCLI list
[ ] 写 Swift 教程  1A2B3C4D-...

$ swift run TodoCLI done 1A2B3C4D-...
done: 写 Swift 教程
```

## 36.6 退出码与输出流：UNIX 世界的礼貌

最后这段 `fputs(...) + exit(1)` 看起来不起眼，却是命令行工具能不能进入脚本流水线的分水岭。它遵守两条约定：

| 约定 | 做法 | 好处 |
| --- | --- | --- |
| 正常结果走标准输出，错误走标准错误 | `print` 对比 `fputs(..., stderr)` | `todo list > out.txt` 不会把错误信息也写进结果文件 |
| 成功退出码 0，失败非 0 | 正常结束默认 0；出错 `exit(1)` | 脚本里可以写 `todo add x && echo ok` |

试试把这两条破坏掉会怎样：如果错误也 `print` 到标准输出，那么 `todo list > list.txt` 在出错时会往 `list.txt` 里写一行 `error: ...`，下游脚本会把这句话当成一条待办——错误的代价从"看得见"变成"藏起来"。

退出码还可以更精确一点，用不同的数字区分不同失败原因：

```swift
import Foundation

enum ExitCode: Int32 {
    case ok = 0
    case usage = 64      // 参数用法错误
    case data = 65       // 数据读不出来
    case notFound = 66   // 找不到目标
}

// 用法：exit(ExitCode.notFound.rawValue)
```

`64`、`65`、`66` 来自 BSD 的 `sysexits.h` 约定（`EX_USAGE` / `EX_DATAERR` / `EX_NOINPUT`）。这不是必须的，但当你的工具会被别人的脚本调用时，明确的退出码能让调用方区分"我参数写错了"和"数据坏了"。

## 36.7 可以继续升级的方向

一个能跑的小工具和一个好用的工具之间，通常隔着这几步：

- 用 `swift-argument-parser` 提供 `--help`、子命令、自动补全和参数校验；
- 增加 `remove`、`clear`、按状态 `filter`、以及优先级；
- 把 `TodoStore` 抽成协议，加一个内存实现专门给测试用（第 38 章就是这个套路）；
- 大文件改用 `FileHandle` 或流式写入，避免一次性读进内存；
- 用 Swift Testing 覆盖解析、存储和完成状态三块逻辑（第 34 章）；
- 给存储加一层"带锁的 actor"，允许多个进程安全写入（第 31 章）。

命令行工具的威力在于可组合：它不需要窗口，却可以被脚本、CI、快捷键和自动化平台反复调用。这也意味着它的"接口"（参数、输出、退出码）比界面更需要稳定。

## 36.8 本章小结

| 层 | 职责 | 出错时的表现 |
| --- | --- | --- |
| 模型 | 表示数据并支持编码 | 编译期就不会错 |
| 存储 | 负责读写和持久化策略 | 抛 `FileManager` / `Codable` 的错误 |
| 解析 | 把参数变成命令 | 抛 `CLIError`，信息面向用户 |
| 主程序 | 组织流程、输出结果、处理错误 | 统一 `catch`，写 stderr 并给退出码 |
| 错误类型 | 自己携带 `description` | 主程序不用 `switch` 就能打印 |

## 36.9 本章易错点速查

| 易错点 | 正确认识 |
| --- | --- |
| 把 `@main` 写进 `main.swift`，同时又拆了其他文件 | 报 `'main' attribute cannot be used...`；入口文件改名或去掉 `@main` |
| 忘记 `dropFirst()` | 程序路径会被当成第一个参数，所有命令都变成"未知命令" |
| 先读 `arguments[1]` 再判长度 | 参数缺失时数组越界崩溃，用户什么提示都看不到 |
| 错误只打印到标准输出 | 错误写标准错误，并返回非零退出码 |
| 直接覆盖写文件 | 用 `.atomic` 或临时文件，避免半截文件 |
| 文件不存在时抛错 | 返回空数组；"没数据"和"读失败"要分开 |
| 所有逻辑塞进入口文件 | 模型、存储、解析分层，才能单独测试 |
| 只用真实用户目录测试 | 测试注入临时目录或内存存储 |
| 手动解析越来越复杂还硬撑 | 该上 `swift-argument-parser` 时就上 |

## 36.10 下章预告

下一章进入 SwiftUI：用声明式代码描述界面。你会看到 `View`、`@State`、`@Binding`、`@Observable` 和旧式 `ObservableObject` 的关系，以及为什么 SwiftUI 的视图是值类型。
