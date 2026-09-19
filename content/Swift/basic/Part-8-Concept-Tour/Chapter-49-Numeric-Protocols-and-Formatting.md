+++
title = "第49章 数值协议族与格式化：数字从计算到显示"
weight = 490
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = "Numeric、BinaryInteger、FixedWidthInteger、FloatingPoint 各自保证什么，以及 FormatStyle 怎样把数字变成人看的文字"
isCJKLanguage = true
draft = false
+++

# 第四十九章：数值协议族与格式化：数字从计算到显示

> 第 4 章讲了整数、浮点、溢出；第 38 章又顺手提了一句金额要用 `Decimal`。但中间那层一直没讲：**为什么 `reduce(0, +)` 能同时算 `Int` 和 `Double`？`UInt8.max` 是哪来的？** 这一章补齐数值协议族，顺便把"数字怎么变成给人看的文字"讲清楚——那部分几乎每个项目都会用到，也几乎每个项目都会写歪。

## 49.1 四个协议，各管一件事

| 协议 | 保证什么 | 典型成员 |
| --- | --- | --- |
| `AdditiveArithmetic` | 能加、能减，有零元 | `+`、`-`、`.zero` |
| `Numeric` | 在上面基础上能乘，能比较 | `*`、`isMultiple(of:)` |
| `BinaryInteger` | 整数：能整除取余、能看位宽 | `%`、`bitWidth`、`isSigned` |
| `FixedWidthInteger` | 固定位宽整数：能看边界、能溢出回绕 | `max`、`min`、`&+`、`leadingZeroBitCount` |
| `FloatingPoint` | 浮点：NaN、无穷、精度 | `isNaN`、`infinity`、`nextUp` |

层层叠加的关系可以这样记：**`FixedWidthInteger` 是整数才有的收尾条件，`FloatingPoint` 是浮点那条支线的收尾条件，而 `Numeric` 是两条支线共有的祖先。**

## 49.2 用 `Numeric` 写"对任何数字都成立"的代码

想让一个求和函数同时服务整数和浮点，约束到 `Numeric` 就够了：

```swift
import Foundation

func sum<T: Numeric>(_ values: [T]) -> T {
    values.reduce(.zero) { $0 + $1 }
}

print(sum([1, 2, 3]))
// prints: 6
print(sum([1.5, 2.5]))
// prints: 4.0
print(sum([Decimal(string: "0.1")!, Decimal(string: "0.2")!]))
// prints: 0.3
```

`Decimal` 也能进来，因为它同样遵循 `Numeric`——这就是协议约束的威力：**你不知道 `T` 是什么，但你确定"加法和零元"存在。**

⚠️ 一个常见陷阱：约束到 `Numeric` 时，`.zero` 是唯一能白拿的字面量。想写 `1` 或 `0.5` 会立刻报错，因为 `Numeric` 不保证"从整数字面量构造"这件事——那是 `ExpressibleByIntegerLiteral` 的职责（第 24.12 节）。

## 49.3 位宽与边界：整数独有的信息

只有固定位宽的整数才谈得上"最大能装多少""有多少位"：

```swift
import Foundation

func describe<T: FixedWidthInteger>(_ value: T) -> String {
    "\(value) 占 \(value.bitWidth) 位，前导零 \(value.leadingZeroBitCount) 个"
}

print(describe(UInt8(1)))
// prints: 1 占 8 位，前导零 7 个
print(describe(Int8(-2)))
// prints: -2 占 8 位，前导零 0 个
```

注意第二个结果：`-2` 在补码里是 `1111_1110`，前面一个零都没有，所以前导零是 **0**。这类"和直觉不一样"的细节，正是位运算章节（第 7.5 节）强调过的同一件事：**负数在计算机里不是你眼睛看到的那样。**

`max`、`min` 也是这一族提供的：

```swift
import Foundation

print(UInt8.max, UInt8.min)
// prints: 255 0
print(Int8.max, Int8.min)
// prints: 127 -128
```

## 49.4 溢出：普通运算符会崩，`&` 系列会回绕

第 4 章讲过"整数溢出会崩"，这一族提供了另一套会回绕的运算符：

```swift
import Foundation

print(UInt8.max &+ 1)     // 加过头，从头开始
// prints: 0
print(UInt8.min &- 1)     // 减过头，绕到最大值
// prints: 255
print(UInt8(200) &* 2)
// prints: 144
```

对比一下，同一份运算用普通运算符会直接崩：

```text
Fatal error: Arithmetic overflow
```

什么时候该用 `&+`？几乎是"**当你确实想要模 2ⁿ 的行为**"：哈希、校验和、加密、位图操作。其它场合一律用普通运算符——崩掉总比悄悄算错好。

## 49.5 浮点：`FloatingPoint` 保证的那些"怪事"

浮点这一族的成员都遵守 IEEE 754，所以它们共享一套"反直觉但正确"的行为：

```swift
import Foundation

let samples: [Double] = [.nan, 1.0]
print(samples[0].isNaN, samples[0] == samples[0])
// prints: true false

print((1.0).nextUp, Double.ulpOfOne)
// prints: 1.0000000000000002 2.220446049250313e-16
```

三件事值得逐条记住：

- **NaN 不等于自己**，判断只能用 `isNaN`（第 4 章讲过这个坑）。
- **`nextUp` 是"下一个能表示的浮点数"**，不是"加一"；它让你直观看到浮点的粒度有多粗。
- **`ulpOfOne` 是 1 与下一个双精度浮点数之间的距离**，也就是"双精度在 1 附近的最小分辨率"。比较两个浮点是否"几乎相等"，用的就是它（第 4 章给过 `abs(a-b) < 容差` 的写法）。

`FloatingPoint` 还有一个实用能力：`isFinite`、`isInfinite`、`sign`。处理来自外部的数值（用户输入、JSON、传感器）时，先判 `isFinite` 再往下算，能挡掉一批"NaN 传染整条计算链"的问题。

## 49.6 `Decimal`：钱的正确容器

第 38 章已经给过结论，这里补上它和数值协议族的关系：`Decimal` 同样遵循 `Numeric`，所以求和、比较这些代码对它一样适用；区别只在精度语义——它是十进制小数，不是二进制。

```swift
import Foundation

let a = Decimal(string: "0.1")!
let b = Decimal(string: "0.2")!
print(a + b == Decimal(string: "0.3")!)
// prints: true
print(a + b)
// prints: 0.3
```

对比 `Double` 的 `0.1 + 0.2 == 0.3` 会得到 `false`。**"钱"、"税率"、"账单分摊"这类必须和人对上账的数字，默认用 `Decimal`，并且从字符串构造**（`Decimal(0.1)` 会把浮点误差先请进门）。

## 49.7 格式化：`FormatStyle` 是唯一的正解

把数字变成文字，历史上有很多做法：`String(format:)`、手写拼接、`NumberFormatter`。前两种会写出难读又难本地化的代码，第三种啰嗦到没人愿意用。现在统一用 **`FormatStyle`**：

```swift
import Foundation

print(1234.5678.formatted(.number.precision(.fractionLength(2))))
// prints: 1,234.57
print(0.256.formatted(.percent.precision(.fractionLength(1))))
// prints: 25.6%
print(Decimal(string: "1234.5")!.formatted(.currency(code: "CNY")))
// prints: ¥1,234.50
print(3.14159.formatted(.number.precision(.significantDigits(3))))
// prints: 3.14
```

日期也走同一套思路：

```swift
import Foundation

let day = Date(timeIntervalSince1970: 0)
print(day.formatted(.iso8601.year().month().day()))
// prints: 1970-01-01
```

`FormatStyle` 的好处有三个，值得逐条对照旧写法看：

1. **能组合。** `.number.precision(...)`、`.currency(code:)`、`.percent` 都是可拼接的积木，而不是一串格式符。
2. **本地化是默认行为。** 同一个 `.currency(code: "CNY")` 在不同区域会给出符合当地习惯的写法（千分位、符号位置），不用你手写 `if locale ==`。
3. **可逆。** `.formatted()` 负责显示，解析时用 `ParseStrategy`（如 `IntegerParseStrategy`）把文字读回数字——这是 `String(format:)` 永远做不到的。

在自己的类型上，也可以直接借用这套：

```swift
import Foundation

struct Reading: CustomStringConvertible {
    var celsius: Double

    var description: String {
        "\(celsius.formatted(.number.precision(.fractionLength(1))))°C"
    }
}

print(Reading(celsius: 21.456))
// prints: 21.5°C
```

`CustomStringConvertible` 会让字符串插值自动走你的 `description`，这一条在第 52 章还会展开。

## 49.8 带单位的数字：`Measurement`

物理量（长度、重量、温度）最容易被"数字 + 字符串单位"糊过去："3 km"、"3000 m" 混着存，换算全靠手写常数。标准库的 `Measurement` 把数值和单位绑在一起：

```swift
import Foundation

let distance = Measurement(value: 3, unit: UnitLength.kilometers)
let inMeters = distance.converted(to: .meters)
print(inMeters.value)
// prints: 3000.0
print(distance + Measurement(value: 500, unit: UnitLength.meters))
// prints: 3500.0 m
```

单位换算由系统负责，`formatted()` 还能按用途挑写法（例如导航场景会自动选合适的单位）。**当你的数据带物理量时,"数值 + 单位字符串"几乎总是错的。**

## 49.9 本章小结

| 概念 | 关键结论 |
| --- | --- |
| `AdditiveArithmetic` / `Numeric` | 加减（含零元）/ 再乘；泛型数值算法的入口 |
| `BinaryInteger` | 整数语义：整除取余、位宽、有无符号 |
| `FixedWidthInteger` | 固定位宽：`max`/`min`、前导零、`&+` 回绕 |
| `FloatingPoint` | IEEE 754 行为：NaN、无穷、`nextUp`、`ulp` |
| `Decimal` | 十进制精确运算，钱的默认选择 |
| `FormatStyle` | 显示数字/日期/百分比/货币的统一接口，自带本地化 |
| `Measurement` | 带单位的物理量，换算交给系统 |

## 49.10 本章易错点速查

| 容易踩的地方 | 正确认识 |
| --- | --- |
| 约束 `T: Numeric` 后写 `1` 或 `0.5` | `Numeric` 不保证字面量构造；用 `.zero` 或换更具体的约束 |
| 以为 `Int` 和 `UInt8` 能直接混算 | 不同位宽/符号类型要显式转换，且注意范围 |
| 用 `&+` 图"省一次检查" | 它换来的是一次静默的错误结果；只在确实需要回绕时用 |
| 判断 NaN 用 `==` | 永远为 false；用 `isNaN` |
| 用 `abs(a - b) < 0.0001` 比浮点 | 容差应基于量级；至少知道 `ulpOfOne` 的存在 |
| 货币用 `Double` 或 `Decimal(0.1)` | 用 `Decimal(string:)` 构造 |
| 手写 `String(format:)` 做货币/百分比 | 用 `FormatStyle`，本地化和边界都替你处理了 |
| 把距离存成 `"3"` + `"km"` 两个字段 | 用 `Measurement`，换算不会错 |

## 49.11 下章预告

数值家族补齐了。下一章做一次"家族盘点"：把散落在第 19 章、第 15B 章、第 21 章里的**属性**与**下标**的每一种形态收进一张图，包括静态下标、协议里的下标、以及让点语法接住任意名字的动态成员查找。
