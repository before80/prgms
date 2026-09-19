+++
title = "04 集合与序列"
linkTitle = "04 集合"
weight = 40
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "数组、字典、集合、元组、区间的全部常用操作，附复杂度与陷阱"
isCJKLanguage = true
draft = false
+++

# 04 集合与序列

## 三种集合，先看怎么选

| | `Array` | `Dictionary` | `Set` |
| --- | --- | --- | --- |
| 顺序 | 保持插入顺序 | **不保证**任何顺序 | **不保证**任何顺序 |
| 查找 | 按索引 O(1)，按值 O(n) | 按键 O(1) | 按值 O(1) |
| 元素要求 | 无 | 键必须 `Hashable` | 元素必须 `Hashable` |
| 典型场景 | 有序列表、频繁按下标访问 | 键值映射、查表 | 去重、成员判断、集合运算 |
| 字面量 | `[1, 2, 3]` | `["a": 1]` | `Set([1, 2])` |

💭 拿不定主意时先写 `Array`。等出现"我要判重"或"按 key 查"的需求，再换成 `Set` 或 `Dictionary`——它们都是值类型，换起来不伤筋动骨。

## 数组

### 创建

```swift
let literal = [1, 2, 3]
let typed: [Int] = []
let repeated = Array(repeating: 0, count: 5)
let fromRange = Array(1...5)
let empty = [String]()

print(repeated, fromRange)
// prints: [0, 0, 0, 0, 0] [1, 2, 3, 4, 5]
```

⚠️ 空数组字面量必须给类型：`let a: [Int] = []` 合法，`let a = []` 是编译错误——编译器没有任何线索猜元素类型。

### 增删改查

| 操作 | 写法 | 复杂度 |
| --- | --- | --- |
| 追加 | `a.append(x)` 或 `a += [x]` | O(1) 摊销 |
| 插入 | `a.insert(x, at: i)` | O(n) |
| 删除指定位置 | `a.remove(at: i)` | O(n) |
| 删除末尾 | `a.removeLast()` / `a.popLast()` | O(1) |
| 按条件删除 | `a.removeAll { $0 < 0 }` | O(n) |
| 全部清空 | `a.removeAll()` | O(n) |
| 按下标读 | `a[0]`、`a.first`、`a.last` | O(1) |
| 按下标写 | `a[0] = 9` | O(1) |
| 交换 | `a.swapAt(i, j)` | O(1) |
| 预分配容量 | `a.reserveCapacity(1000)` | — |
| 是否为空 | `a.isEmpty` | O(1) |
| 元素个数 | `a.count` | O(1) |

```swift
var nums = [3, 1, 4, 1, 5]
nums.append(9)
nums.insert(0, at: 0)
nums.remove(at: 0)
print(nums)
// prints: [3, 1, 4, 1, 5, 9]
```

### 构造与容量：几个少见的 init

除了字面量和 `Array(repeating:count:)`，还有几个构造器值得认识：

```swift
// 从 (键, 值) 序列一次性建字典
let pairs = [("a", 1), ("b", 2)]
print(Dictionary(uniqueKeysWithValues: pairs).keys.sorted())
// prints: ["a", "b"]

print(Dictionary(uniqueKeysWithValues: zip(1..., ["a", "b"]))[2] ?? "?")
// prints: b

// 键可能重复时，得自己定"留谁"的规则
let dup = [("a", 1), ("a", 2)]
print(Dictionary(dup, uniquingKeysWith: { first, _ in first })["a"] ?? -1)
// prints: 1

var arr = [1, 2, 3]
arr.removeAll(keepingCapacity: true)      // 清空元素，但留着已分配的内存
print(arr.isEmpty, arr.capacity >= 3)
// prints: true true
```

| 需求 | 写法 |
| --- | --- |
| 从键值对建字典 | `Dictionary(uniqueKeysWithValues:)`，键重复会**崩** ⚠️ |
| 键重复时自己定规则 | `Dictionary(_:uniquingKeysWith:)` |
| 重复元素只留一个 | `Set(数组)`，或 `Dictionary` 做中间层 |
| 预分配容量 | `a.reserveCapacity(n)`、`d.reserveCapacity(n)` |
| 看已分配多少 | `a.capacity` |
| 清空但保留容量 | `a.removeAll(keepingCapacity: true)` 🝖 |

⚠️ `Dictionary(uniqueKeysWithValues:)` 碰到重复键**直接崩**（实测 `Fatal error: Duplicate values for key: 'a'`），它不负责替你决定留哪一个。数据来自外部（解析结果、用户输入）时，用 `uniquingKeysWith:` 版本把规则写清楚。

💭 还有一个冷门兄弟 `ContiguousArray<Element>`：它保证元素在一块连续内存里。元素是**类**或 `@objc` 协议类型时，它可能比 `Array` 少一层桥接开销；其他情况直接用 `Array`，别没事换类型。🝖

### 排序与变形

```swift
let nums = [3, 1, 4, 1, 5]

print(nums.sorted())
// prints: [1, 1, 3, 4, 5]
print(nums.sorted(by: >))
// prints: [5, 4, 3, 1, 1]
print(nums.reversed().map { $0 })
// prints: [5, 1, 4, 1, 3]

var mutable = nums
mutable.sort()          // 原地排序，要求元素可比较
print(mutable)
// prints: [1, 1, 3, 4, 5]
```

⚠️ `sorted()` 返回新数组，`sort()` 原地改。看到没有 `ed` 后缀，就说明它在改你自己。这条规矩对 `reversed` / `shuffled` 也一样：`shuffled()` 返回新数组，`shuffle()` 打乱自己。

🔥 **排序是稳定的**：两个"相等"的元素会保持原来的相对顺序。这一点在按多个字段排序时特别有用——先按次要字段排一次，再按主要字段排一次，前一次的成果不会被打乱。

```swift
struct Player { let first: String; let last: String }

// 已经按姓氏排好
var roster = [
    Player(first: "Sam", last: "Coffey"),
    Player(first: "Ashley", last: "Hatch"),
    Player(first: "Kristie", last: "Mewis"),
    Player(first: "Ashley", last: "Sanchez"),
]

roster.sort { $0.first < $1.first }      // 再按名字排
print(roster.map(\.last))
// prints: ["Hatch", "Sanchez", "Mewis", "Coffey"]
// 两个 Ashley 的先后没变：Hatch 还在 Sanchez 前面
```

💭 这条保证是从 Swift 5.8 起明确写进官方文档的（[SE-0372](https://github.com/swiftlang/swift-evolution/blob/main/proposals/0372-document-sorting-as-stable.md)）。老教程说"Swift 的排序不稳定"，那是很久以前的信息。

### 切片

```swift
let nums = [3, 1, 4, 1, 5, 9]

print(nums.prefix(2), nums.suffix(2))
// prints: [3, 1] [5, 9]
print(nums.dropFirst(2), nums.dropLast(2))
// prints: [4, 1, 5, 9] [3, 1, 4, 1]
```

⚠️ 切片返回的是 `ArraySlice`，它**保留原来的下标**。这意味着：

```swift
let nums = [3, 1, 4, 1, 5, 9]

let slice = nums[2...4]
print(slice[0])
// 🛑 崩溃：下标越界
print(slice[slice.startIndex])
// prints: 4        ✅ 必须用切片的 startIndex
```

要恢复正常下标就 `Array(slice)`。这个坑每年都有一批人栽进去。

## 字典

```swift
var ages = ["Alice": 30, "Bob": 25]

ages["Carol"] = 28                 // 新增
ages["Alice"] = 31                 // 覆盖
ages["Bob"] = nil                  // 删除
print(ages.keys.sorted())
// prints: ["Alice", "Carol"]

print(ages["nobody", default: 0])
// prints: 0

ages["Dave", default: 0] += 1      // 不存在就先用默认值起手
print(ages["Dave"] ?? -1)
// prints: 1
```

| 操作 | 写法 | 备注 |
| --- | --- | --- |
| 取值 | `d[key]` | 返回 `Value?`，键不存在就是 `nil` |
| 带默认值取值 | `d[key, default: 0]` | 返回非可选值，🔥 常配合 `+=` 计数；只读不会写入，`+=` 会顺手插入这个键 |
| 写入 | `d[key] = value` | 键已存在则覆盖 |
| 删除 | `d[key] = nil` 或 `d.removeValue(forKey: key)` | 后者返回被删掉的值 |
| 更新并取旧值 | `d.updateValue(v, forKey: k)` | 返回旧值 `Value?` |
| 遍历 | `for (k, v) in d` | 顺序不保证 |
| 只取键 / 值 | `d.keys` / `d.values` | 都是视图，不复制 |
| 变换值 | `d.mapValues { $0 * 2 }` | 保留键类型 |
| 筛选 | `d.filter { $0.value > 26 }` | 返回新字典 |
| 合并 | `d.merging(other) { old, new in new }` | 冲突时由闭包决定留谁 |
| 分组 | `Dictionary(grouping: items, by: { $0.kind })` | 一行完成分组统计 🔥 |

```swift
let words = ["apple", "avocado", "banana", "blueberry", "cherry"]
let grouped = Dictionary(grouping: words) { $0.first! }
print(grouped["a"] ?? [])
// prints: ["apple", "avocado"]

let counts = words.reduce(into: [Character: Int]()) { result, word in
    result[word.first!, default: 0] += 1
}
print(counts["b"] ?? 0)
// prints: 2
```

## 集合

```swift
var seen: Set<Int> = [1, 2, 3]
seen.insert(4)
seen.insert(4)                 // 重复插入无效果
print(seen.count)
// prints: 4
print(seen.contains(3))
// prints: true
```

| 运算 | 写法 | 含义 |
| --- | --- | --- |
| 并集 | `a.union(b)` | 两边的元素合起来（自动去重） |
| 交集 | `a.intersection(b)` | 两边都有的 |
| 差集 | `a.subtracting(b)` | 在 a 不在 b |
| 对称差 | `a.symmetricDifference(b)` | 只在一侧出现 |
| 子集 | `a.isSubset(of: b)` | 参数可以是任何序列 |
| 超集 | `a.isSuperset(of: b)` | |
| 无交集 | `a.isDisjoint(with: b)` | |
| 原地版本 | `a.formUnion(b)` 等 | 直接改 `a`，避免复制 🝖 |

```swift
let a: Set = [1, 2, 3, 4]
print(a.union([5, 6]).sorted())
// prints: [1, 2, 3, 4, 5, 6]
print(a.subtracting([1, 2]).sorted())
// prints: [3, 4]
print(a.symmetricDifference([3, 9]).sorted())
// prints: [1, 2, 4, 9]
```

🔥 判断"两个数组有没有重复元素"时，把其中一个转成 `Set` 再 `isDisjoint`，比双层循环快得多。

⚠️ `Set` 里的元素必须实现 `Hashable`。自定义类型加上 `Hashable` 后，编译器通常能自动合成实现——但如果你的类型有 `Double` 字段，别用它当哈希依据，`NaN` 会让集合行为变得不可预测。

### 固定长度与"只看不抄"：`InlineArray` 和 `Span` 🆕

`Array` 的元素放在堆上，长度随时可变。Swift 6.2 带来了两个"反着来"的兄弟：

- **`InlineArray<N, T>`**：长度写在类型里，元素直接内联存放，没有堆分配。
- **`Span<T>`**：一段**借来**的只读视图，拿到它不拷贝任何数据。

```swift
var buffer: InlineArray<3, Int> = [1, 2, 3]
buffer[0] = 9
print(buffer.count, buffer[0])
// prints: 3 9

let numbers = [10, 20, 30]
print(numbers.span[1], numbers.span.count)     // 借出来看一眼，不复制
// prints: 20 3
```

⚠️ 两个实测会碰到的限制：

| 你想写的 | 结果 |
| --- | --- |
| `for x in buffer`（遍历 `InlineArray`） | `for-in loop requires 'InlineArray<3, Int>' to conform to 'Iterable', which is only available in macOS 27.0 or newer` |
| `let v = buffer.span` 然后拿去别处用 | `lifetime-dependent value escapes its scope` —— `Span` 只能在借用范围内用 |

💭 这两个类型是给性能敏感代码准备的（省掉堆分配、也能天然避免数据竞争）。日常业务照旧用 `Array`；读到它们时，知道是"更快但更受限的数组"就够。

## 元组

元组是"临时打包几个值"的轻量工具，没有命名类型，也不能实现协议。

```swift
let pair = (name: "Alice", age: 30)
print(pair.name, pair.1)
// prints: Alice 30

let (n, a) = pair          // 解构
print(n, a)
// prints: Alice 30

let (_, onlyAge) = pair    // 用 _ 忽略不需要的部分
print(onlyAge)
// prints: 30
```

| 能做 | 不能做 |
| --- | --- |
| 带标签或按位置访问 | 不能遵守协议（除了有限的比较） |
| 作为函数返回值返回多个值 | 不能加方法或属性 |
| 逐元素比较（最多 6 个元素） | 不能递归包含自身 |
| `swap(&a, &b)` 交换两个变量 | 元素超过 6 个就无法比较大小 |

```swift
print((1, "b") < (2, "a"))
// prints: true
print((1, 2) < (1, 3))
// prints: true
```

💭 元组适合"就地返回两三个值"，一旦发现这个组合要传给多个函数，就该升级成 `struct`——有名字的类型比 `(String, Int, Bool)` 好懂得多。

## 区间与序列

```swift
print(Array(1...5))
// prints: [1, 2, 3, 4, 5]
print((1...5).map { $0 * $0 })
// prints: [1, 4, 9, 16, 25]
print(Array(stride(from: 0, to: 10, by: 3)))
// prints: [0, 3, 6, 9]
print(Array((1...5).reversed()))
// prints: [5, 4, 3, 2, 1]
```

`..<` 是半开区间 `Range`，`...` 是闭区间 `ClosedRange`。`Range` 可以表示空区间（`5..<5`），`ClosedRange` 不行。

标准库还提供了两个"按规律生成序列"的函数，写算法题和爬格子时很好用：

```swift
// sequence(first:next:)：从第一个值开始，靠闭包推出下一个；返回 nil 就结束
let powers = sequence(first: 1, next: { $0 < 100 ? $0 * 2 : nil })
print(Array(powers))
// prints: [1, 2, 4, 8, 16, 32, 64, 128]

// sequence(state:next:)：状态自带，适合递推
let fib = sequence(state: (0, 1)) { (pair: inout (Int, Int)) -> Int? in
    defer { pair = (pair.1, pair.0 + pair.1) }
    return pair.0
}
print(Array(fib.prefix(7)))
// prints: [0, 1, 1, 2, 3, 5, 8]

print(Array(repeatElement("x", count: 3)))
// prints: ["x", "x", "x"]
```

💭 它们是**惰性**的：不 `prefix`、不 `Array(...)` 就不会真的算下去。拿不到终止条件时记得自己截断，否则会一直生成下去。

## 自己造一个序列：IteratorProtocol

标准库的 `Sequence` 不是魔法，它只要求一件事：能给出一个"下一个值"。你的类型只要实现 `next()`，就能用上 `map`、`filter`、`reduce`、`for-in` 全套工具：

```swift
struct Countdown: Sequence, IteratorProtocol {
    var current: Int

    mutating func next() -> Int? {
        guard current > 0 else { return nil }   // 返回 nil 表示"没有了"
        defer { current -= 1 }
        return current
    }
}

print(Array(Countdown(current: 3)))
// prints: [3, 2, 1]
print(Countdown(current: 4).map { $0 * 10 })
// prints: [40, 30, 20, 10]
for x in Countdown(current: 2) { print(x) }
// prints:
//   2
//   1
```

两个协议的分工：

| 协议 | 要求 | 你能得到 |
| --- | --- | --- |
| `IteratorProtocol` | `mutating func next() -> Element?` | 一个能一步步取值的东西 |
| `Sequence` | `makeIterator()` | `for-in`、`map`、`filter`、`reduce`、`contains`… 全套免费 |

💭 当类型**自己就是**迭代器（同时遵守两个协议）时，标准库会用默认实现替你写 `makeIterator()`，所以上面只写了 `next()`。这就是"遵守一个协议，白拿一整套算法"的最好例子。

想临时凑一个序列、又不想专门定义类型时，用 `AnyIterator` 和 `AnySequence`：

```swift
var i = 0
let counter = AnyIterator { () -> Int? in
    i += 1
    return i <= 3 ? i : nil
}
print(Array(counter))
// prints: [1, 2, 3]

// 承接上文：Countdown 已定义
let seq = AnySequence(Countdown(current: 3))
print(seq.reduce(0, +))
// prints: 6
```

| 类型 | 用途 |
| --- | --- |
| `AnyIterator` | 用一个闭包当场造出迭代器 |
| `AnySequence` | 把任意序列包起来，藏掉具体类型（类型擦除） |
| `sequence(first:next:)` / `sequence(state:next:)` | 连类型都不用定义，见上一节 |

⚠️ `Sequence` 有一个出了名的特性：**它不保证能被遍历两次**。如果序列是"一次性"的（比如网络流、文件句柄），第一次 `for-in` 之后第二次就没数据了。需要重复遍历就遵守 `Collection`，或者先 `Array(seq)` 存下来。

## 高阶函数速查

这张表是 Swift 写起来最爽的部分，值得整块记住。

| 函数 | 作用 | 示例 → 结果 |
| --- | --- | --- |
| `map` | 一对一变换 | `[1,2].map { $0 * 2 }` → `[2, 4]` |
| `compactMap` | 变换并丢掉 `nil` | `["1","x"].compactMap(Int.init)` → `[1]` |
| `flatMap` | 展平一层嵌套 | `[[1,2],[3]].flatMap { $0 }` → `[1, 2, 3]` |
| `filter` | 保留满足条件的 | `[1,2,3].filter { $0 > 1 }` → `[2, 3]` |
| `reduce` | 折叠成一个值 | `[1,2,3].reduce(0, +)` → `6` |
| `reduce(into:)` | 折叠进可变容器 | 见上面的词频统计 |
| `sorted(by:)` | 自定义排序 | `[3,1].sorted(by: >)` → `[3, 1]` |
| `first(where:)` | 第一个满足条件的 | `[1,2].first { $0 > 1 }` → `2` |
| `allSatisfy` | 是否全部满足 | `[2,4].allSatisfy { $0.isMultiple(of: 2) }` → `true` |
| `contains(where:)` | 是否存在满足的 | `[1,2].contains { $0 > 1 }` → `true` |
| `min()` / `max()` | 最小 / 最大 | `[3,1].min()` → `1` |
| `min(by:)` / `max(by:)` | 用自定义规则找极值 | `[3,1].min(by: >)` → `3`（"按 `>` 排最前"就是最大那个） |
| `firstIndex(of:)` / `firstIndex(where:)` | 找位置，找不到给 `nil` | `[3,1,4].firstIndex(of: 4)` → `2` |
| `lastIndex(of:)` / `lastIndex(where:)` | 从后往前找 | `[1,2,1].lastIndex(of: 1)` → `2` |
| `prefix` / `suffix` | 前 / 后 N 个 | `[1,2,3].prefix(2)` → `[1, 2]` |
| `dropFirst` / `dropLast` | 丢掉前 / 后 N 个 | `[1,2,3].dropFirst()` → `[2, 3]` |
| `zip` | 拉链式配对 | `zip([1,2], ["a","b"])` → `[(1,"a"), (2,"b")]` |
| `enumerated` | 带下标 | `["a"].enumerated()` → `[(0, "a")]` |
| `joined` | 拼接 | `["a","b"].joined(separator: "-")` → `"a-b"` |
| `shuffled` / `randomElement` | 随机 | `[1,2].randomElement()` → 随机一个或 `nil` |

### 同一个任务，三种写法

统计一段文本里每个单词出现的次数——这是最常遇到的小需求，也是最能看出风格差异的地方。

{{< tabpane text=true persist=disabled >}}

{{% tab header="reduce(into:)（推荐）" %}}

```swift
let words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

let counts = words.reduce(into: [String: Int]()) { result, word in
    result[word, default: 0] += 1
}

print(counts["apple"] ?? 0)
// prints: 3
```

一次遍历、不产生中间数组，`result[word, default: 0] += 1` 这个写法本身也足够清楚。🔥

{{% /tab %}}

{{% tab header="map + 分组" %}}

```swift
let words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

let groups = Dictionary(grouping: words) { $0 }
let counts = groups.mapValues(\.count)

print(counts["apple"] ?? 0)
// prints: 3
```

思路更直白："先按自己分组，再数每组的数量"，代价是多存了一份分组数据。

{{% /tab %}}

{{% tab header="for-in（最笨但最清楚）" %}}

```swift
let words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

var counts: [String: Int] = [:]
for word in words {
    if let n = counts[word] {
        counts[word] = n + 1
    } else {
        counts[word] = 1
    }
}

print(counts["apple"] ?? 0)
// prints: 3
```

毫无技巧，也毫无误解空间。团队风格保守时它反而是最好的选择。

{{% /tab %}}

{{< /tabpane >}}

## 序列、集合、惰性

Swift 的集合协议是一条链，理解它能解释很多"为什么这里能用那里不能用"。

| 协议 | 提供的能力 | 谁遵守 |
| --- | --- | --- |
| `Sequence` | 能 `for-in`，能 `map` / `filter` | 几乎所有容器 |
| `Collection` | 上面全部 + 下标、`count`、可多次遍历 | `Array` `Dictionary` `Set` `String` |
| `BidirectionalCollection` | 还能从后往前 | `Array` `String` |
| `RandomAccessCollection` | 索引移动是 O(1) | `Array` |

`Sequence` 只有一次机会：如果某个序列是"单遍"的（比如从网络读流），遍历两次会出问题：

```swift
let s = [1, 2, 3].lazy.map { $0 * 2 }
print(s.first ?? 0)
// prints: 2
```

⚠️ `.lazy` 会把变换推迟到真正取值时才发生。链式操作很长时它能省掉中间数组。但它只是**包装**：底层是可多次遍历的集合（`Array`、`Range`）时，遍历几遍都没事；底层本身是单遍序列（读流、通道）时，第二遍就是空的——这才是那个经典 bug。

## 复杂度速查

| 操作 | Array | Dictionary / Set |
| --- | --- | --- |
| 按下标 / 键访问 | O(1) | O(1) 平均 |
| 追加 / 插入 | 末尾 O(1) 摊销，中间 O(n) | O(1) 平均（可能触发扩容重哈希） |
| 删除 | 末尾 O(1)，中间 O(n) | O(1) 平均 |
| 按值查找 | O(n) | O(1) 平均 |
| 是否包含 | O(n) | O(1) 平均 |
| 遍历 | O(n) | O(n) |

## 陷阱速查

| 陷阱 | 说明 |
| --- | --- |
| 越界访问 | `a[i]` 不检查，越界直接崩溃；用 `a.indices.contains(i)` 或 `a.first` |
| `ArraySlice` 下标 | 切片保留原数组下标，用 `startIndex` 而不是 `0` |
| 边遍历边改 | `for x in a` 迭代的是取值那一刻的快照，循环里改 `a` 不会崩但结果容易想错；真正会崩的是按下标一边走一边删（`for i in a.indices { a.remove(at: i) }` → `Fatal error: Index out of range`），要先收集下标再删 |
| 字典顺序 | 遍历字典的顺序不保证，需要稳定顺序就 `sorted()` |
| `first` 返回可选值 | `a.first` 是 `Element?`，空数组得到 `nil` |
| `contains` 用在 `Set` 上更快 | `[Int]` 上判重是 O(n)，`Set` 上是 O(1) |
| 大数组用 `+=` 单个元素 | 用 `append`，`+=` 每次都会构造数组字面量 |
