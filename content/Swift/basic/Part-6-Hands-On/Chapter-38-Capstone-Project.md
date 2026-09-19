+++
title = "第38章 综合实战：支出记录器"
weight = 380
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "把模型、存储、业务规则、异步与测试拼成一个可替换、可测试、可继续长大的小型系统"
isCJKLanguage = true
draft = false
+++

# 第三十八章：综合实战：支出记录器

> 这一章不追求"做一个完整 App"，而是做一个结构正确、可以继续长大的核心：模型清楚、存储可替换、逻辑可测试、错误可读。把支出记录做对，很多业务系统也能照着搭。

## 38.1 需求与边界

先把"要做什么"和"不做什么"同时定下来。不划边界，综合项目最后一定会变成一锅粥。

**要做：**

- 添加一笔支出，包含金额、分类、日期和备注；
- 查询总额、按分类汇总；
- 持久化到 JSON 文件；
- 用协议隔离存储实现，方便替换和测试；
- 所有失败都有明确的错误类型。

**这一章不做：** 界面（第 40 章往后的第七篇专门做）、多币种、账号同步、数据库。不是因为它们难，而是因为**在接口还没稳定之前急着加实现，只会把接口焊死。** 本章的目标是让接口先站住。

有一件事必须现在就决定：金额用 `Decimal`，不用 `Double`。原因是浮点数存不下精确的十进制小数：

```swift
import Foundation

print(0.1 + 0.2)
// prints: 0.30000000000000004

print(0.1 + 0.2 == 0.3)
// prints: false

let a = Decimal(string: "0.1")!
let b = Decimal(string: "0.2")!
print(a + b)
// prints: 0.3

print(a + b == Decimal(string: "0.3")!)
// prints: true
```

一次求和差 0.00000000000000004 看着无所谓，但记账系统的标准动作是"成千上万笔累加"和"两两对账"，误差会累积，更糟的是对不上账时你很难解释为什么。**凡是"钱"、凡是需要精确十进制的地方，默认用 `Decimal`。**

⚠️ 注意上面是用 `Decimal(string:)` 构造的。`Decimal(0.1)` 直接吃一个 `Double` 字面量，等于把浮点误差先请进来再包装一次，白用 `Decimal` 了。需要精确值就永远从字符串或整数走。

## 38.2 模型：只描述数据

这一层的唯一职责是"把一条支出表示清楚"：

```swift
import Foundation

struct Expense: Codable, Identifiable, Equatable {
    let id: UUID
    var amount: Decimal
    var category: String
    var date: Date
    var note: String

    init(
        id: UUID = UUID(),
        amount: Decimal,
        category: String,
        date: Date = .now,
        note: String = ""
    ) {
        self.id = id
        self.amount = amount
        self.category = category
        self.date = date
        self.note = note
    }
}
```

模型的三个自律点：

- **不 import 任何 UI 框架。** 一旦模型里出现 `@State` 或 `Color`，它就没法在命令行、服务端和测试里复用了。
- **不负责读写文件。** 模型不知道自己是存在 JSON、数据库还是内存里。
- **`id` 是 `let`。** 身份不变，这条规矩从第 36 章一直用到第 43 章。

关于 `Decimal` 有一个实战提醒：它**天生支持 `Codable`**，但 JSON 里会以数字形式存储。如果对端系统把这串数字当浮点解析，精度又丢回去了——所以跨系统交换金额时，更稳的做法是存字符串（`"12.50"`），需要时用 `Decimal(string:)` 转回来。

## 38.3 存储协议：先定接口，再定实现

先写协议而不是先写实现，是这一章最重要的一个顺序决定：

```swift
import Foundation

protocol ExpenseStore {
    func load() throws -> [Expense]
    func save(_ expenses: [Expense]) throws
}

struct JSONExpenseStore: ExpenseStore {
    let url: URL

    func load() throws -> [Expense] {
        guard FileManager.default.fileExists(atPath: url.path) else { return [] }
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode([Expense].self, from: data)
    }

    func save(_ expenses: [Expense]) throws {
        let data = try JSONEncoder().encode(expenses)
        try data.write(to: url, options: .atomic)
    }
}
```

协议只有两个方法，这是刻意的：**接口越小，实现越容易替换。** 假如协议里塞进 `sortByDate()`、`sumOfMonth()` 这类查询，那么每换一种存储（JSON → SQLite）都要重新实现一遍这些业务逻辑；放在存储接口里，等于把业务规则绑死在某一种介质上。

测试时换成内存实现，两分钟就能写完：

```swift
import Foundation

final class MemoryExpenseStore: ExpenseStore {
    var expenses: [Expense] = []

    func load() throws -> [Expense] { expenses }
    func save(_ expenses: [Expense]) throws { self.expenses = expenses }
}
```

⚠️ 这里用 `final class` 而不是 `struct`，因为测试需要"写进去的内容下一次读得到"。如果写成 `struct`，`save` 改的是一份副本，测试会看到数据凭空消失——这是第 17 章值语义最容易在实战中咬人的地方。当然也可以写 `struct` + `inout`，但那样协议签名就要跟着变，得不偿失。

## 38.4 业务规则：服务层只做判断和聚合

模型不知道规则，存储不知道规则，那么规则住在哪？答案是单独一个服务类型。

```swift
import Foundation

enum ExpenseError: Error, Equatable {
    case invalidAmount
    case emptyCategory
}

struct ExpenseService {
    let store: ExpenseStore

    func add(amount: Decimal, category: String) throws {
        guard amount > 0 else { throw ExpenseError.invalidAmount }
        guard !category.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
            throw ExpenseError.emptyCategory
        }
        var expenses = try store.load()
        expenses.append(Expense(amount: amount, category: category))
        try store.save(expenses)
    }

    func total() throws -> Decimal {
        try store.load().reduce(0) { $0 + $1.amount }
    }

    func totalByCategory() throws -> [String: Decimal] {
        try store.load().reduce(into: [:]) { result, expense in
            result[expense.category, default: 0] += expense.amount
        }
    }
}
```

逐点解释这段"看起来平平无奇但很关键"的代码：

- **`store` 是协议类型，不是具体类型。** 服务从不知道数据存在哪，这正是不用改一行业务代码就能把 JSON 换成 SQLite 的原因。
- **校验写在写之前。** 先判断再落盘，避免"写坏了再回滚"这种复杂操作。
- **`category.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty`**：只判 `isEmpty` 会放过一个纯空格的分类名——这是真实项目里最常见的"看起来校验了其实没校验"。
- **`reduce(into: [:])` 做分组求和**，比手写 `for` 更短也更不容易写错初始值。
- **错误用 `enum` 而不是字符串**：调用方能 `catch ExpenseError.invalidAmount` 做精确处理，测试里也能直接比较（所以它遵循 `Equatable`）。

## 38.5 异步版本：当存储变成"会慢"的东西

接口现在都是同步的。一旦存储换成数据库、网络或者云盘，同步接口就变成了性能杀手：每次 `load()` 都会卡住调用它的线程。把接口升级成异步，同时用 `actor` 保护共享文件：

```swift
import Foundation

protocol AsyncExpenseStore: Sendable {
    func load() async throws -> [Expense]
    func save(_ expenses: [Expense]) async throws
}

actor FileExpenseStore: AsyncExpenseStore {
    private let url: URL
    init(url: URL) { self.url = url }

    func load() async throws -> [Expense] {
        try JSONExpenseStore(url: url).load()
    }

    func save(_ expenses: [Expense]) async throws {
        try JSONExpenseStore(url: url).save(expenses)
    }
}
```

三点说明：

- **`actor` 保证同一时刻只有一段代码碰这个存储。** 两个任务同时 `load → 改 → save` 时，如果没有 actor，后写的那次会把先写的覆盖掉；有了它，两次操作被排成队列，各自都基于最新的数据。
- **`protocol AsyncExpenseStore: Sendable`**：这个约束是必须的。异步接口意味着实现会被跨隔离域传递，编译器会要求它可安全传递（第 31 章）。写 `Sendable` 比后面被一串并发报错追着改容易得多。
- **真正的文件 I/O 还可以再往下挪一层。** `actor` 解决的是"不要同时写"，不解决"别阻塞线程"。在服务端或大文件场景，可以把实际读写放进专门的任务或执行器。本章为了短小不做这一步，但你应该知道它存在。

## 38.6 测试：把"我试过没问题"变成证据

前面把存储抽成协议，代价是多写几行；回报就在这里——整套业务规则可以离线、毫秒级地验证：

```swift
import Foundation
import Testing

@Test
func addingExpenseUpdatesTotal() throws {
    let store = MemoryExpenseStore()
    let service = ExpenseService(store: store)

    try service.add(amount: 12.5, category: "餐饮")
    try service.add(amount: 7.5, category: "交通")

    #expect(try service.total() == 20)
}

@Test
func invalidAmountThrows() {
    let service = ExpenseService(store: MemoryExpenseStore())
    #expect(throws: ExpenseError.invalidAmount) {
        try service.add(amount: 0, category: "餐饮")
    }
}

@Test
func blankCategoryIsRejected() {
    let service = ExpenseService(store: MemoryExpenseStore())
    #expect(throws: ExpenseError.emptyCategory) {
        try service.add(amount: 10, category: "   ")
    }
}

@Test
func totalGroupsByCategory() throws {
    let service = ExpenseService(store: MemoryExpenseStore())
    try service.add(amount: 10, category: "餐饮")
    try service.add(amount: 5, category: "餐饮")
    try service.add(amount: 3, category: "交通")

    #expect(try service.totalByCategory() == ["餐饮": 15, "交通": 3])
}
```

注意第三个测试：它专门验证"纯空格分类"会被拒绝。**测试最有价值的部分往往不是主流程，而是这些边界。** 主流程你手点一遍就发现了，边界只有写下来才不会在半年后悄悄回归。

在 SwiftPM 项目里放进 `Tests/` 目录，运行 `swift test`，四个用例都会通过：

```text
Test run started.
addingExpenseUpdatesTotal() passed
invalidAmountThrows() passed
blankCategoryIsRejected() passed
totalGroupsByCategory() passed
```

## 38.7 如果今天就要接界面

这套核心可以直接喂给 SwiftUI，而且不需要改任何业务代码：

```swift
import SwiftUI
import Observation

@Observable
final class ExpenseListModel {
    private let service: ExpenseService
    private(set) var total: Decimal = 0
    private(set) var message: String?

    init(service: ExpenseService) {
        self.service = service
    }

    func refresh() {
        do {
            total = try service.total()
            message = nil
        } catch {
            message = "读取失败：\(error)"
        }
    }

    func add(amountText: String, category: String) {
        guard let amount = Decimal(string: amountText) else {
            message = "金额必须是数字"
            return
        }
        do {
            try service.add(amount: amount, category: category)
            refresh()
        } catch {
            message = "\(error)"
        }
    }
}

// 界面效果：模型暴露 total 与 message，视图只管显示；
// 想深入界面写法请看第七篇（第 40 章起）
```

这段代码其实是一次"分层检验"：如果模型层写得干净，接线只需要几十行；如果需要把文件读写、校验和界面揉在一起才能跑起来，说明前面某一层的位置放错了。

## 38.8 继续扩展

- 增加删除和编辑功能（注意：金额与分类的校验要复用，不要复制）；
- 用 `Decimal.FormatStyle` 格式化金额，例如 `total.formatted(.currency(code: "CNY"))`；
- 用 SwiftUI + Charts 展示分类占比（第七篇 + 官方 Charts）；
- 用 SQLite/GRDB 替换 JSON 存储，验证"接口真的可替换"；
- 增加导入导出、预算与周期统计；
- 给存储加版本号，实现数据结构迁移。

综合项目的价值不在功能数量，而在**每一层都能单独替换、单独测试**。这样的代码才经得起下一轮需求——因为下一轮需求一定会来，而且大概率会问你"能不能加一个……"。

## 38.9 本章小结

| 层 | 职责 | 关键决定 |
| --- | --- | --- |
| 模型 | 纯数据与编码能力 | 用 `Decimal` 存金额；不 import UI |
| 存储协议 | 隔离持久化实现 | 接口越小越好；`Sendable` 便于并发 |
| 业务服务 | 校验和聚合逻辑 | 错误用枚举；trim 后再判空 |
| actor 存储 | 串行保护共享文件 | 防止并发覆盖写 |
| 测试 | 用内存实现验证业务规则 | 边界用例比主流程更重要 |
| 界面模型 | 把服务包装成可观察对象 | 不写业务规则，只做适配 |

## 38.10 本章易错点速查

| 易错点 | 正确认识 |
| --- | --- |
| 金额使用 `Double` | 货币计算优先 `Decimal`，且从字符串构造 |
| `Decimal(0.1)` 当精确值用 | 那等于先引入浮点误差；用 `Decimal(string:)` |
| 模型直接读写文件或引用 UI 类型 | 模型保持纯粹，才能复用与测试 |
| 业务逻辑散在界面和存储中 | 集中到 service，才测得动 |
| 内存存储写成 `struct` | `save` 改的是副本，测试会"丢数据"；用 `class` 或 `inout` |
| 只判 `isEmpty` 就算校验了分类 | 纯空格能溜过去；先 `trimmingCharacters` |
| 测试依赖真实文件路径 | 用内存 store 或临时目录 |
| 多个任务同时写同一文件 | 用 actor 保护，否则后写覆盖先写 |
| 异步存储协议不标 `Sendable` | 后面会被一串并发报错追着改 |
| 接口没稳定就引入数据库 | 先让模型和接口站住，再换实现 |

## 38.11 下章预告

最后一章是选读：服务端 Swift。你会看到同一套语言如何编写 HTTP 服务、异步路由、数据库访问和部署配置。
