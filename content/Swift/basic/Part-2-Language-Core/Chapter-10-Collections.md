+++
title = "第10章 集合：Array、Dictionary 与 Set"
weight = 100
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第十章：集合：Array、Dictionary 与 Set

> 集合是程序的收纳间。数组排好队，字典按名字找，集合负责去重。它们都能装很多东西，但最重要的共同点其实不是“能装”：在 Swift 里，把集合赋给另一个变量，得到的是独立的副本，而不是指向同一堆数据的遥控器。

## 10.1 Array：有顺序的列表

数组用方括号书写，元素类型必须一致：

```swift
var fruits = ["apple", "banana", "cherry"]
print(fruits.count, fruits.first as Any, fruits.last as Any)
// prints: 3 Optional("apple") Optional("cherry")
```

`first` 和 `last` 返回可选值，因为空数组没有首尾元素：

```swift
let empty: [Int] = []
print(empty.first as Any)
// prints: nil
```

下标访问返回非可选值，越界会直接崩溃：

```swift
print(fruits[1])
// prints: banana
```

增删改：

```swift
fruits.append("date")
fruits.insert("avocado", at: 0)
print(fruits)
// prints: ["avocado", "apple", "banana", "cherry", "date"]

fruits[0] = "apricot"
fruits.remove(at: 1)
print(fruits)
// prints: ["apricot", "banana", "cherry", "date"]
```

`removeAll()` 清空，`contains(_:)` 判断存在，`firstIndex(of:)` 找到位置：

```swift
print(fruits.contains("banana"))
// prints: true
print(fruits.firstIndex(of: "cherry") as Any)
// prints: Optional(2)
```

数组的切片类型是 `ArraySlice`，它和 `Substring` 一样会保留原数组的存储：

```swift
let slice = fruits[1...2]
print(slice, type(of: slice))
// prints: ["banana", "cherry"] ArraySlice<String>
```

## 10.2 Dictionary：用键找值

字典存放“键—值”对，键必须遵循 `Hashable`：

```swift
var scores = ["Lin": 90, "Mia": 85]
print(scores["Lin"] as Any)
// prints: Optional(90)
```

下标返回可选值，因为键可能不存在：

```swift
print(scores["Nova"] as Any)
// prints: nil
```

更新和删除：

```swift
scores["Nova"] = 77
scores["Lin"] = 95
print(scores["Lin"] as Any)
// prints: Optional(95)

let removed = scores.removeValue(forKey: "Mia")
print(removed as Any)
// prints: Optional(85)
```

`updateValue(_:forKey:)` 会返回旧值，这也是可选值：

```swift
let old = scores.updateValue(100, forKey: "Nova")
print(old as Any, scores["Nova"] as Any)
// prints: Optional(77) Optional(100)
```

遍历：

```swift
for (name, score) in scores.sorted(by: { $0.key < $1.key }) {
    print("\(name): \(score)")
}
// prints: Lin: 95
// prints: Nova: 100
```

字典本身是无序的，所以想要稳定输出时通常先排序。

## 10.3 Set：只关心“有没有”

集合存放不重复的值，元素必须遵循 `Hashable`：

```swift
var tags: Set<String> = ["swift", "ios", "swift"]
print(tags.count)
// prints: 2
```

集合的典型操作是交、并、差：

```swift
let a: Set = [1, 2, 3, 4]
let b: Set = [3, 4, 5]

print(a.intersection(b).sorted())
// prints: [3, 4]
print(a.union(b).sorted())
// prints: [1, 2, 3, 4, 5]
print(a.subtracting(b).sorted())
// prints: [1, 2]
print(a.symmetricDifference(b).sorted())
// prints: [1, 2, 5]
```

判断包含关系：

```swift
print(a.isSuperset(of: [1, 2]))
// prints: true
print(a.isDisjoint(with: [9, 10]))
// prints: true
```

名字都取得很直白，对着结果读一遍就记住了：`intersection` 是交集，`union` 是并集，`subtracting` 是"从左边那份里剔掉右边也有的元素"，`symmetricDifference` 是"只出现在其中一边"的对称差；`isSuperset(of:)` 问"我是不是包含它全部"，`isDisjoint(with:)` 问"我们有没有交集"。集合运算背后是哈希表，所以这些操作通常比用数组手写循环快得多，也不会产生重复元素。

## 10.4 值语义：复制的是内容，不是地址

数组、字典和集合都是**值类型**：

```swift
var original = [1, 2, 3]
var copy = original
copy.append(4)

print(original)
// prints: [1, 2, 3]
print(copy)
// prints: [1, 2, 3, 4]
```

这里的“复制”不是立刻把所有元素抄一遍。Swift 使用写时复制（Copy-on-Write）：只有某一方真正修改时，底层存储才会分离。第 27 章会拆开这套机制，现在先记住结论：**每次赋值在语义上都是独立副本，性能通常在幕后优化。**

字典和集合同理：

```swift
var d1 = ["a": 1]
var d2 = d1
d2["b"] = 2
print(d1.count, d2.count)
// prints: 1 2
```

这里没有直接打印两个字典，因为**字典是无序的**，打印出来的键顺序不保证稳定，不适合写进“预期输出”。要比内容，用 `==`；要稳定地展示，先 `sorted()`。

## 10.5 遍历、筛选与变换

数组、字典、集合都能用 `for-in` 遍历：

```swift
for fruit in ["apple", "pear"] {
    print(fruit)
}
// prints: apple
// prints: pear
```

`map` 变换每个元素，`filter` 保留满足条件的元素，`reduce` 把元素合成一个结果：

```swift
let numbers = [1, 2, 3, 4, 5]
print(numbers.map { $0 * 2 })
// prints: [2, 4, 6, 8, 10]
print(numbers.filter { $0.isMultiple(of: 2) })
// prints: [2, 4]
print(numbers.reduce(0, +))
// prints: 15
```

`reduce(0, +)` 里的 `+` 是“运算符当函数传”的写法，第 15B.10 节会专门讲它以及其他函数值的简写。

`compactMap` 会丢掉变换产生的 `nil`：

```swift
let texts = ["1", "two", "3"]
print(texts.compactMap(Int.init))
// prints: [1, 3]
```

遍历数组时向其中增删元素会出问题，因为迭代器依赖稳定的结构。需要修改时先收集待处理项，循环结束后再统一处理：

```swift
var values = [1, 2, 3]
var shouldRemove: [Int] = []
for value in values where value.isMultiple(of: 2) {
    shouldRemove.append(value)
}
values.removeAll { shouldRemove.contains($0) }
print(values)
// prints: [1, 3]
```

## 10.6 本章小结

| 集合 | 有序 | 可重复 | 查找方式 | 适合场景 |
| --- | --- | --- | --- | --- |
| `Array` | 是 | 是 | 下标、遍历 | 顺序列表 |
| `Dictionary` | 否 | 键唯一 | 键 | 按名字查数据 |
| `Set` | 否 | 否 | 包含判断、集合运算 | 去重与成员关系 |

## 10.7 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 用越界下标“试试看” | 越界会崩溃，不能靠它判断存在 |
| 把字典下标当成一定有值 | 字典下标返回可选值 |
| 认为数组赋值后共享修改 | 值语义下两者独立 |
| 把不可哈希的值塞进 `Set` | 元素必须遵循 `Hashable` |
| 期待字典遍历顺序固定 | 字典无序，需要顺序就排序 |
| 边遍历边修改数组 | 先记录待处理项，循环结束后统一修改 |
| 忘记 `compactMap` | `map` 会产生 `[Int?]`，成对过滤解包用 `compactMap` |

## 10.8 下章预告

数据有了容器，接下来就要让程序做决定。第十一章从 `if`、`for`、`while` 讲起，把控制流的骨架搭好；第十二章再进入 Swift 的 `switch`——那不是普通的 `switch`，而是一套模式匹配系统。
