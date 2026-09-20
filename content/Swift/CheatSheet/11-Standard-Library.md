+++
title = "11 标准库速查"
linkTitle = "11 标准库"
weight = 110
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "常用协议、格式化、Codable、KeyPath、结果构建器与日期时钟的速查表"
isCJKLanguage = true
draft = false
+++

# 11 标准库速查

## 协议全景

标准库的力量主要来自协议。看到某个类型能做什么，基本就是看它遵守了哪些协议。

| 协议 | 一句话 | 遵守后得到 |
| --- | --- | --- |
| `Equatable` | 能比较相等 | `==` `!=` |
| `Hashable` | 能放进集合 | `Set` `Dictionary` 的键、`hash(into:)` |
| `Comparable` | 能排序 | `<` `<=` `>` `>=`、`sorted()` |
| `Identifiable` | 有稳定身份 | SwiftUI 列表用得上 |
| `Codable` | 能编解码 | `JSONEncoder` / `JSONDecoder` 🔥 |
| `Sequence` | 能遍历 | `for-in`、`map` `filter` `reduce` |
| `Collection` | 能下标访问 | `count`、`indices`、可重复遍历 |
| `BidirectionalCollection` | 能反向走 | `reversed()` |
| `RandomAccessCollection` | 下标 O(1) | `Array`、随机访问算法 |
| `CustomStringConvertible` | 能自定义打印 | `description` |
| `LosslessStringConvertible` | 能从字符串无损还原 | `init?(_:)` 与 `description` 一对 |
| `CaseIterable` | 枚举能列全 | `allCases` |
| `RawRepresentable` | 有原始值 | `init?(rawValue:)`、`rawValue` |
| `ExpressibleBy*Literal` | 能用字面量写 | `let x: MyType = 1` |
| `Sendable` | 能跨并发域传 | 见 [09 错误处理与并发]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `AsyncSequence` | 能 `for await` | 异步数据流 |
| `IteratorProtocol` | 能一步步取值 | `next()`，`Sequence` 的底层 |
| `AdditiveArithmetic` | 只能加、只能减 | `+` `-`（向量、时长这类类型的最小数学要求） |
| `Numeric` | 加上乘法 | `*`、`isMultiple(of:)` |
| `SignedNumeric` | 再带上正负 | 一元 `-`、`negate()` |
| `BinaryInteger` | 整数家族 | `/%`、位运算、`String(x, radix:)` |
| `FixedWidthInteger` | 定长整数 | `&+`、`bitWidth`、`byteSwapped`、溢出报告 |
| `FloatingPoint` | 浮点家族 | `isNaN`、`rounded()`、`nextUp` |
| `Strideable` | 能按步长走 | `stride(from:to:by:)`、`advanced(by:)` |
| `OptionSet` | 位掩码选项集合 | `contains`、`union`、`[.a, .b]` 写法 |
| `Error` | 能当错误抛 | `throw` / `catch`，见 [09 章]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |
| `CustomDebugStringConvertible` | 自定义 `debugPrint` 输出 | `debugDescription` |

🔥 大多数协议的实现编译器能自动合成，前提是所有存储属性也满足条件。`Equatable`、`Hashable`、`Codable`、`CaseIterable` 都属于这一类，手写只是在有特殊需求时才需要。

💭 上面那一串数学协议不是让你背的，而是一把**刻度尺**：写泛型时约束得越松，能接的类型越多。只想要加减就约束 `AdditiveArithmetic`，要乘法再加到 `Numeric`，需要位运算就得写 `FixedWidthInteger`。标准库里的 `Int`、`UInt8`、`Float`、`Double` 分别落在这条链的不同位置上。

## 常用类型

| 类型 | 来自 | 用途 |
| --- | --- | --- |
| `Optional` | 标准库 | 可能没有值 |
| `Result` | 标准库 | 成功 / 失败的容器 |
| `Range` / `ClosedRange` | 标准库 | 区间 |
| `Character` / `String` / `Substring` | 标准库 | 文本 |
| `Array` / `Set` / `Dictionary` | 标准库 | 集合 |
| `KeyPath` / `WritableKeyPath` | 标准库 | 属性路径 |
| `Duration` / `Clock` | 标准库 🆕 | 时间长度与时钟 |
| `Decimal` | Foundation | 十进制定点，算钱用 |
| `Data` | Foundation | 字节缓冲 |
| `Date` / `Calendar` / `TimeZone` | Foundation | 时间与日历 |
| `URL` / `URLComponents` | Foundation | 网址 |
| `JSONEncoder` / `JSONDecoder` | Foundation | JSON 编解码 |
| `UUID` | Foundation | 唯一标识 |

## 位掩码：OptionSet

"读 / 写 / 执行"这类开关组合，用 `OptionSet` 比 `Set<Enum>` 更贴底层，也能直接对上 C 的位标志：

```swift
struct Permissions: OptionSet {
    let rawValue: Int
    static let read    = Permissions(rawValue: 1 << 0)
    static let write   = Permissions(rawValue: 1 << 1)
    static let execute = Permissions(rawValue: 1 << 2)
}

let p: Permissions = [.read, .write]          // 组合就是数组字面量
print(p.rawValue, p.contains(.read), p.contains(.execute))
// prints: 3 true false

print(Permissions.write.union(.execute).rawValue)
// prints: 6
print(p.subtracting(.read).rawValue)
// prints: 2
```

| 需求 | 写法 |
| --- | --- |
| 定义 | `struct X: OptionSet { let rawValue: Int; static let a = X(rawValue: 1 << 0) }` |
| 组合 | `[.a, .b]`、`x.union(.b)`、`x.formUnion(.b)` |
| 判断 | `x.contains(.a)` |
| 去掉 | `x.subtracting(.a)`、`x.remove(.a)` |
| 交换 | `x.symmetricDifference(.a)` |
| 空集合 | `X()`，`isEmpty` 为 `true` |
| "全都要" | 标准库没有内建 `all`，自己加一句 `static let all: X = [.a, .b, .c]` |

⚠️ 每个选项必须是 **2 的幂**（`1 << n`），否则位之间会互相串味；`rawValue` 的类型必须是 `FixedWidthInteger`（`Int`、`UInt8` 都行）。

## 格式化：FormatStyle

详细用例见 [03 类型与字符串]({{< relref "03-Types-and-Strings.md" >}})，这里只放最常用的几种：

| 需求 | 写法 |
| --- | --- |
| 千分位整数 | `1234567.formatted()` |
| 两位小数 | `x.formatted(.number.precision(.fractionLength(2)))` |
| 百分比 | `x.formatted(.percent)` |
| 货币 | `x.formatted(.currency(code: "CNY"))` |
| 科学计数 | `x.formatted(.number.notation(.scientific))` |
| 字节数 | `x.formatted(.byteCount(style: .file))` |
| 日期 | `date.formatted(date: .abbreviated, time: .shortened)` |
| 相对时间 | `date.formatted(.relative(presentation: .named))` |
| 时长 | `duration.formatted(.units(allowed: [.minutes, .seconds]))` |
| 列表 | `["a","b","c"].formatted(.list(type: .and))` |
| ISO8601 时间戳 | `date.formatted(.iso8601)` |

## KeyPath

KeyPath 是"指向某个属性的引用"，可以当函数传，也可以动态取值。

```swift
import Foundation   // KeyPathComparator 在 Foundation 里

struct User { let name: String; let age: Int }
let users = [User(name: "Bob", age: 25), User(name: "Alice", age: 30)]

print(users.map(\.name))
// prints: ["Bob", "Alice"]
print(users.sorted(using: KeyPathComparator(\.age)).map(\.name))
// prints: ["Bob", "Alice"]
print(users.sorted { $0.age < $1.age }.map(\.name))
// prints: ["Bob", "Alice"]
```

| 用法 | 写法 |
| --- | --- |
| 当函数 | `users.map(\.name)` 🔥 |
| 取自身 | `a.map(\.self)`，需要 KeyPath 但不想取属性时用 |
| 动态取值 | `user[keyPath: \.name]` |
| 存成变量 | `let kp: KeyPath<User, String> = \User.name` |
| 排序 | `users.sorted(using: KeyPathComparator(\.age))` |
| 求和 | `users.map(\.age).reduce(0, +)` |
| 可写路径（要求属性是 `var`） | `let wk: WritableKeyPath<User, Int> = \User.age` 🝖 |
| 字符串化 | `#keyPath(User.name)`（**只对 `@objc` 属性成立**，见下） |

⚠️ KeyPath **不能**当双参数谓词：`users.sorted(by: \.age)` 是编译错误。要么 `sorted { $0.age < $1.age }`，要么 `sorted(using: KeyPathComparator(\.age))`。

⚠️ `user[keyPath: \.name]`、`users.map(\.name)` 属于标准库，不需要导入；但 `KeyPathComparator` 来自 Foundation。在 Linux 上它会随 swift-corelibs-foundation 一起提供。

⚠️ **`#keyPath` 和 `\.age` 不是同一件事**，这是 KeyPath 这一节最容易混的地方：

| 写法 | 是什么 | 要求 |
| --- | --- | --- |
| `\User.age` | Swift 的 KeyPath 字面量，**真正的类型** | 无。属性是 `let` 就是 `KeyPath`，是 `var` 才是 `WritableKeyPath` |
| `#keyPath(User.age)` | 把属性名变成**字符串**，只给 Objective-C 的 KVC 用 | 类型得是 `NSObject` 子类、属性得标 `@objc`，且属性是 `var` |

```swift
import Foundation

struct User { let name: String; let age: Int }   // 纯 Swift 结构体
// print(#keyPath(User.name))
// 🛑 error: argument of '#keyPath' refers to non-'@objc' property 'name'

final class ObjcUser: NSObject {
    @objc var name: String = "x"
}
print(#keyPath(ObjcUser.name))
// prints: name
```

顺手记一句：上面那张表里 `WritableKeyPath<User, Int>` 只能指向 `var`。如果 `User` 的属性是 `let`，写 `let wk: WritableKeyPath<User, Int> = \User.age` 会报 `cannot convert key path type 'any KeyPath<User, Int> & Sendable' to contextual type 'WritableKeyPath<User, Int>'`——`let` 属性只配得到 `KeyPath`。

## Codable

```swift
import Foundation

struct Config: Codable, Equatable {
    var name: String
    var timeout: Int

    enum CodingKeys: String, CodingKey {
        case name = "app_name"     // 映射到 JSON 里的另一个键名
        case timeout
    }
}

let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
let data = try encoder.encode(Config(name: "demo", timeout: 30))
print(String(decoding: data, as: UTF8.self))
// prints: {
//           "app_name" : "demo",
//           "timeout" : 30
//         }

print(try JSONDecoder().decode(Config.self, from: data))
// prints: Config(name: "demo", timeout: 30)
```

| 需求 | 写法 |
| --- | --- |
| 改键名 | 自定义 `CodingKeys` 枚举 |
| 日期格式 | `encoder.dateEncodingStrategy = .iso8601` |
| 输出可读 | `outputFormatting = [.prettyPrinted, .sortedKeys]` |
| 忽略某个字段 | 不放进 `CodingKeys`——但该属性必须**是可选值，或者有默认值**，否则解码直接失败（见下） |
| 缺失字段用默认值 | 自己写 `init(from:)`，用 `decodeIfPresent` |
| 嵌套容器 | 用 `nestedContainer(keyedBy:forKey:)` 🝖 |
| 非 JSON 编码 | `PropertyListEncoder`、自定义 `Encoder` |

```swift
import Foundation

struct Event: Codable { var title: String; var date: Date }

let iso = JSONEncoder()
iso.dateEncodingStrategy = .iso8601
iso.outputFormatting = [.sortedKeys]      // 不写这行，键的顺序每次都可能不一样
let payload = try iso.encode(Event(title: "发布", date: Date(timeIntervalSince1970: 0)))
print(String(decoding: payload, as: UTF8.self))
// prints: {"date":"1970-01-01T00:00:00Z","title":"发布"}
```

⚠️ `JSONEncoder` **不保证键的顺序**：它按底层字典的哈希顺序输出，同一个程序连跑五次可能给出两种结果。要稳定的输出（做 diff、写测试、存快照）就必须加 `.sortedKeys`。上面 `Config` 那个例子能稳定显示 `app_name` 在 `timeout` 之前，正是因为设了它。

⚠️ `Codable` 合成出来的解码器**不会**为缺失字段兜底：字段少了就抛错，而不是用属性的默认值。想宽容一点，必须手写 `init(from:)`。

合成与手写的差别，看这两种写法就清楚了：

{{< tabpane text=true persist=disabled >}}

{{% tab header="自动合成（默认）" %}}

```swift
import Foundation   // Data / JSONDecoder 都在这里

struct StrictConfig: Codable {
    var name: String
    var timeout: Int
}

let partial = Data(#"{"name":"demo"}"#.utf8)
let strict = try? JSONDecoder().decode(StrictConfig.self, from: partial)
print(strict as Any)
// prints: nil        少了 timeout，直接解码失败
```

字段一个都不能少，键名也必须对得上（除非用 `CodingKeys` 做映射）。

{{% /tab %}}

{{% tab header="手写 init(from:)（宽容）" %}}

```swift
import Foundation

struct LooseConfig: Codable {
    var name: String
    var timeout: Int

    enum CodingKeys: String, CodingKey { case name, timeout }

    init(from decoder: any Decoder) throws {
        let c = try decoder.container(keyedBy: CodingKeys.self)
        name = try c.decodeIfPresent(String.self, forKey: .name) ?? "未命名"
        timeout = try c.decodeIfPresent(Int.self, forKey: .timeout) ?? 30
    }
}

let partial = Data(#"{"name":"demo"}"#.utf8)
print(try JSONDecoder().decode(LooseConfig.self, from: partial))
// prints: LooseConfig(name: "demo", timeout: 30)
```

`decodeIfPresent` 让缺失字段回落到默认值，代价是必须自己维护 `init(from:)`。

{{% /tab %}}

{{< /tabpane >}}

## 日期、时长与时钟

```swift
import Foundation

let now = Date()
print(now.formatted(date: .abbreviated, time: .shortened))

let duration = Duration.seconds(90)
print(duration.formatted(.units(allowed: [.minutes, .seconds])))
// prints: 1分钟30秒

let clock = ContinuousClock()
let elapsed = clock.measure { _ = (1...10_000).reduce(0, +) }
print(elapsed > .zero)
// prints: true
```

| 需求 | 写法 |
| --- | --- |
| 当前时间 | `Date.now` / `Date()` |
| 时间戳 | `date.timeIntervalSince1970` |
| 从时间戳构造 | `Date(timeIntervalSince1970:)` |
| 只要年月日 | `Calendar.current.dateComponents([.year, .month, .day], from: date)` |
| 加一天 | `Calendar.current.date(byAdding: .day, value: 1, to: date)` |
| 自定义格式串（老写法） | `DateFormatter().dateFormat = "yyyy-MM-dd"`，然后 `formatter.string(from: date)` 🝖 |
| 时长运算 | `Duration.seconds(1) + .milliseconds(500)` |
| 测耗时 | `ContinuousClock().measure { ... }` 🔥 |
| 异步等待 | `try await Task.sleep(for: .seconds(1))` |

⚠️ **"不放进 `CodingKeys`" ≠ "这个字段可以随便缺"**，这两件事经常被当成一件。把一个属性从 `CodingKeys` 里去掉，只是让它不参与编解码，但类型仍然必须满足 `Codable` 的合成条件：

| 被排除的属性长什么样 | 结果 |
| --- | --- |
| `var b: Int`（非可选、无默认值） | ❌ 合成失败：`type 'A' does not conform to protocol 'Decodable'`，附一句 `'b' does not have a matching CodingKey and does not have a default value` |
| `var b: Int = 0`（有默认值） | ✅ 解码时保持默认值，JSON 里的 `b` 被忽略 |
| `var b: Int?`（可选值） | ✅ 解码成 `nil` |

```swift
import Foundation

struct A: Codable {
    var a: Int
    var b: Int = 0                            // 有默认值，才敢从 CodingKeys 里去掉
    enum CodingKeys: String, CodingKey { case a }
}

let data = Data(#"{"a":1,"b":2}"#.utf8)
print(try JSONDecoder().decode(A.self, from: data))
// prints: A(a: 1, b: 0)       JSON 里的 b 被整个忽略，留下的 0 是属性默认值
```

⚠️ 测耗时用 `ContinuousClock`，不要用 `Date()` 相减：系统时间会被调整（NTP 校时、用户手动改、闰秒），挂起也会污染结果。💭 顺带澄清一个常被夸大的点：**时区本身不影响相减**——`timeIntervalSince` 数的是绝对时间差，把 `TZ` 换成哪个时区，两次 `Date()` 之差都一样。`Date()` 真正的毛病是"挂钟"性质，不是时区。

## 结果构建器

SwiftUI 的 `@ViewBuilder` 背后就是结果构建器。它让你能在"本该是一条表达式"的地方写若干行，由编译器收集起来：

```swift
@resultBuilder
struct ArrayBuilder {
    static func buildBlock(_ parts: [Int]...) -> [Int] { parts.flatMap { $0 } }
    static func buildOptional(_ part: [Int]?) -> [Int] { part ?? [] }
}

func collect(@ArrayBuilder _ body: () -> [Int]) -> [Int] { body() }

let flag = false
let built = collect {
    [1, 2]
    if flag { [99] }      // 条件分支也能写进来
    [3]
}
print(built)
// prints: [1, 2, 3]
```

| 方法 | 支持什么写法 |
| --- | --- |
| `buildBlock` | 顺序排列多条语句 |
| `buildOptional` | `if` 没有 `else` |
| `buildEither` | `if / else`、`switch` |
| `buildArray` | `for-in` 循环 |
| `buildExpression` | 单条表达式 |
| `buildFinalResult` | 最后统一加工 |

💭 结果构建器是"库作者的工具"。日常开发里你是它的使用者（`@ViewBuilder`、`@resultBuilder` 定义的 DSL），而不是它的作者。

## 集合算法补充

前面 [04 集合与序列]({{< relref "04-Collections.md" >}}) 已经列过主力函数，这里补几个容易被忽略的：

| 需求 | 写法 |
| --- | --- |
| 判断是否全等 | `a.elementsEqual(b)` |
| 按条件切分 | `a.partition(by: { $0 < 0 })`（原地重排，返回分界下标） |
| 找最长前缀 | `a.prefix(while: { $0 < 5 })` |
| 找最长后缀 | 标准库没有 `suffix(while:)`，翻个面再来：`Array(a.reversed().prefix(while: { $0 < 5 }).reversed())` |
| 丢掉前缀 | `a.drop(while: { $0 < 5 })` |
| 分块 | `stride(from: 0, to: a.count, by: 3).map { Array(a[$0..<min($0+3, a.count)]) }` |
| 找最值及其位置 | `a.enumerated().max { $0.element < $1.element }` |
| 累加（前缀和） | `a.reduce(into: []) { $0.append(($0.last ?? 0) + $1) }` |
| 交错 | `zip(a, b).flatMap { [$0, $1] }` |
| 去重且保序 | `a.reduce(into: [Int]()) { seen, x in if !seen.contains(x) { seen.append(x) } }` ⚠️ 累加器的类型必须写出来，`into: []` 推不出来 |
| 随机抽样 | `a.shuffled().prefix(3)` |
| 可复现的随机 | 自己实现 `RandomNumberGenerator`，再用 `a.randomElement(using: &rng)`、`Int.random(in:using:)` |
| 定长内联数组 | `InlineArray<N, T>`，见 [04 集合]({{< relref "04-Collections.md" >}}) 🆕 |

```swift
let numbers = [3, 1, 4, 1, 5, 9, 2, 6]
print(numbers.prefix(while: { $0 > 2 }).map { $0 })
// prints: [3]

var mutable = [3, 1, 4, 1, 5]
let pivot = mutable.partition(by: { $0 >= 4 })
print(mutable, pivot)
// prints: [3, 1, 1, 4, 5] 3
// pivot 是分界下标：前半段都不满足条件，后半段都满足，但**组内顺序不作保证**

// zip 的长度以较短的那个为准
print(Array(zip(1..., ["a", "b", "c"])))
// prints: [(1, "a"), (2, "b"), (3, "c")]
```

## 观察与状态

Swift 5.9 起标准库外多了一个 `Observation` 模块，`@Observable` 取代了 `ObservableObject` + `@Published` 的组合：

| 场景 | 现代写法 | 老写法 |
| --- | --- | --- |
| 可观察模型 | `@Observable final class Model` 🆕 | `class Model: ObservableObject` + `@Published` |
| 视图持有 | `@State private var model = Model()` | `@StateObject` |
| 视图接收 | `let model: Model`（自动追踪） | `@ObservedObject` |
| 环境注入 | `.environment(model)` + `@Environment(Model.self)` | `@EnvironmentObject` |

💭 `@Observable` 只追踪**真正被读到的**属性，不再一改全刷新，也不用再纠结 `@StateObject` 和 `@ObservedObject` 的区别。SwiftUI 的细节见教程部分的 SwiftUI 篇。

```swift
import Observation

@Observable
final class Model {
    var name = ""                                  // 被观察
    @ObservationIgnored var cache = 0              // 改了也不通知视图
}

let m = Model()
m.name = "x"
print(m.name, m.cache)
// prints: x 0
```

💭 什么时候该用 `@ObservationIgnored`：那些"改了不需要刷新界面"的内部缓存、统计计数、委托对象。少观察一个属性，就少一次无谓的刷新。

## Foundation 日常工具箱

除了 `Date`、`Data`、`URL` 这些"数据型"类型，Foundation 里还有几个天天见面但很少有人系统看过的工具：

| 需求 | 写法 | 备注 |
| --- | --- | --- |
| 小量偏好设置 | `UserDefaults.standard.set(_:forKey:)` / `.integer(forKey:)` | 只适合存开关、计数一类的小数据 |
| 广播 / 订阅事件 | `NotificationCenter.default.post` / `.addObserver` | 订阅完记得 `removeObserver`，否则会泄漏 |
| 读 App 自身信息 | `Bundle.main.infoDictionary`、`Bundle.main.executablePath` | 在 App 包里才有意义 |
| 写日志 | `Logger(subsystem:category:)`（`import os`） | 比 `print` 强：有级别、能过滤、性能好；输出要去 Console.app 或 `log stream` 里看 |
| 读写文件、临时目录 | `FileManager.default` | 用例见 [13 工具链]({{< relref "13-Tooling.md" >}}) |
| 命令行参数、环境变量 | `CommandLine` / `ProcessInfo` | 同上，见 [13 工具链]({{< relref "13-Tooling.md" >}}) |
| 编解码 base64 | `data.base64EncodedString()` / `Data(base64Encoded:)` | 接口传图片、凭证时常用 |
| 哈希摘要 | `SHA256.hash(data:)`（`import CryptoKit`） | 只在 Apple 平台；跨平台项目用 swift-crypto |
| 网络请求 | `URLSession.shared.data(from:)` | 配合 `async/await`，一行拿到 `(Data, URLResponse)` |
| 读文件 | `try Data(contentsOf: url)`、`try String(contentsOf:encoding:)` | 大文件要流式读，别整个塞进内存 |
| 写文件 | `try data.write(to: url, options: .atomic)` | `.atomic` 先写临时文件再替换，断电不会留半个文件 |
| 目录操作 | `FileManager.default.createDirectory(at:withIntermediateDirectories:)`、`removeItem(at:)`、`copyItem(at:to:)` | 更多用例见 [13 章]({{< relref "13-Tooling.md" >}}) |
| 区域、日历、时区 | `Locale.current`、`Calendar.current`、`TimeZone.current` | 格式化输出会跟着它们变，写测试时要小心 |

```swift
import Foundation

UserDefaults.standard.set(42, forKey: "launchCount")
print(UserDefaults.standard.integer(forKey: "launchCount"))
// prints: 42

let note = Notification.Name("demo")
let token = NotificationCenter.default.addObserver(forName: note, object: nil, queue: nil) { n in
    print("收到通知:", n.userInfo?["k"] ?? "-")
}
NotificationCenter.default.post(name: note, object: nil, userInfo: ["k": 7])
// prints: 收到通知: 7
NotificationCenter.default.removeObserver(token)

print(Bundle.main.executablePath != nil)
// prints: true
```

```swift
import CryptoKit
import Foundation

let data = Data("你好".utf8)
let base64 = data.base64EncodedString()
print(base64, String(data: Data(base64Encoded: base64)!, encoding: .utf8)!)
// prints: 5L2g5aW9 你好

print(SHA256.hash(data: Data("abc".utf8)).map { String(format: "%02x", $0) }.joined())
// prints: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
```

⚠️ 几点经验：

1. **`UserDefaults` 不是数据库。** 存大数组或二进制数据会让启动变慢，那种数据该进文件或数据库。
2. **通知是广播，不带类型信息。** `userInfo` 是个 `[AnyHashable: Any]`，取的时候要自己转型——能用直接回调和 `async` 序列的地方就别用通知。
3. **`Logger` 的字符串插值有讲究**：`logger.log("用户 \(userId)")` 里的数字、字符串会按隐私规则处理，默认不显示个人数据。想看到具体值要写 `logger.log("用户 \(userId, privacy: .public)")`。

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| `sorted(by: \.age)` | 编译不过，KeyPath 不是双参数谓词 |
| 以为 `Codable` 会用属性默认值 | 缺失字段直接抛错，需要 `decodeIfPresent` |
| 用 `Date` 测耗时 | 用 `ContinuousClock`，系统时间会被改 |
| 用 `Double` 算钱 | 用整数分单位或 `Decimal` |
| `formatted()` 写进测试断言 | 输出依赖区域设置 |
| `zip` 后长度不一致 | 以**短的那个**为准，多余部分被静默丢弃 ⚠️ |
| 滥用 `@resultBuilder` 做业务逻辑 | 它适合描述结构，不适合藏控制流 |
| 对非常大的集合用 `first(where:)` 循环 | 需要频繁查找时先建 `Dictionary` / `Set` |
