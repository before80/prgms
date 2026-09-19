+++
title = "第34章 测试：Swift Testing 与 XCTest"
weight = 340
date = "2026-09-14T22:30:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十四章：测试：Swift Testing 与 XCTest

> 测试不是给代码上保险，而是把“我期待它怎样工作”写成可重复执行的证据。Swift Testing 提供了现代化的宏和结构化用例，XCTest 仍然是大量现有项目的基础。两者都值得会，重点不是框架名字，而是测什么、怎么让测试稳定。

## 34.1 Swift Testing：`@Test` 与 `#expect`

Swift 6 时代的测试写起来像在给代码写备注：函数加一个 `@Test` 就是测试，断言写成 `#expect`。

```swift
import Testing

func add(_ a: Int, _ b: Int) -> Int {
    a + b
}

@Test
func addition() {
    #expect(add(2, 3) == 5)
}
```

`@Test` 登记测试函数，`#expect` 检查条件。失败时它会报告表达式、实际值和源码位置，比普通 `assert` 更容易定位。

测试命名建议描述行为，而不是复述函数名：

```swift
@Test
func addingTwoPositiveNumbersReturnsSum() {
    #expect(add(2, 3) == 5)
}
```

## 34.2 `#require`：先拿到必要条件

`#require` 用来解包可选值或中断当前测试：

```swift
@Test
func firstElementIsValid() throws {
    let values = [1, 2, 3]
    let first = try #require(values.first)
    #expect(first == 1)
}
```

如果 `values.first` 是 `nil`，测试立即失败，后面的断言不会在一个无效值上继续乱跑。`#expect` 记录失败但继续，`#require` 是“没有它就没法继续”。

## 34.3 测试抛错与异步代码

会被测出错的代码，测试里就得把“出错”也当成一种预期结果来检查：

```swift
enum CalculatorError: Error, Equatable { case divisionByZero }

func divide(_ a: Int, _ b: Int) throws -> Int {
    guard b != 0 else { throw CalculatorError.divisionByZero }
    return a / b
}

@Test
func dividingByZeroThrows() {
    #expect(throws: CalculatorError.divisionByZero) {
        try divide(1, 0)
    }
}
```

异步测试直接写 `async`：

```swift
@Test
func loadingReturnsValue() async throws {
    let value = try await loadValue()
    #expect(value > 0)
}
```

测试中的异步代码必须可重复、可等待。不要靠 `sleep` 猜时间；能注入假时钟或协议依赖时，就不要把测试建立在真实时钟上。

## 34.4 参数化测试

同一套逻辑可以用多组输入：

```swift
@Test(arguments: [1, 2, 3, 4])
func numberIsPositive(_ value: Int) {
    #expect(value > 0)
}
```

也可以传入元组：

```swift
@Test(arguments: [(2, 3, 5), (4, 5, 9)])
func addition(_ a: Int, _ b: Int, expected: Int) {
    #expect(add(a, b) == expected)
}
```

参数化测试适合边界值、输入输出表和多种格式，不要把彼此无关的场景硬塞进同一个测试。

## 34.5 `@Suite` 与测试组织

`@Suite` 把相关测试归组：

```swift
@Suite("整数运算")
struct IntegerMathTests {
    @Test func addition() { #expect(add(1, 2) == 3) }
}
```

共享初始化逻辑可以放在 suite 的属性和初始化器里。测试之间应尽量独立，不要依赖执行顺序，也不要把一个测试的结果留给另一个测试使用。

## 34.6 XCTest：现有项目的主力

老项目里更常见的是 XCTest——继承 `XCTestCase`，方法名以 `test` 开头：

```swift
import XCTest

final class MathTests: XCTestCase {
    func testAddition() {
        XCTAssertEqual(add(2, 3), 5)
    }

    func testDivisionByZero() {
        XCTAssertThrowsError(try divide(1, 0))
    }
}
```

常用断言包括 `XCTAssertEqual`、`XCTAssertTrue`、`XCTAssertNil`、`XCTAssertThrowsError`。异步 XCTest 可以写 `func testLoad() async throws`。

性能测试使用 `measure`：

```swift
func testPerformance() {
    measure {
        _ = (0..<10_000).reduce(0, +)
    }
}
```

性能数字受机器、调试/发布构建和后台负载影响。不要把一次本机结果当成永久基线。

## 34.7 好测试的共同特征

- 一个测试只验证一个清晰行为。
- 失败信息能告诉你期望什么、实际什么。
- 不依赖真实网络、真实时间、当前时区或执行顺序。
- 能独立运行，也能整体运行。
- 覆盖正常路径、边界值和错误路径。
- 被测对象通过协议或参数注入外部依赖，方便替换。

测试不是越多越好。重复验证同一个细节的测试只会拖慢构建，并让重构时修改面变大。

## 34.8 本章小结

| 工具 | 用途 |
| --- | --- |
| `@Test` | 声明 Swift Testing 测试 |
| `#expect` | 检查条件并记录失败 |
| `#require` | 取得继续测试所必需的值 |
| 参数化测试 | 用多组输入覆盖同一逻辑 |
| `@Suite` | 组织相关测试 |
| XCTest | 现有项目常用的测试框架 |
| `measure` | XCTest 的性能测量 |

## 34.9 本章易错点速查

| 易错点 | 正确理解 |
| --- | --- |
| 用 `sleep` 等异步结果 | 测试会慢且不稳定，改用可靠等待或注入时钟 |
| 测试互相依赖执行顺序 | 每个测试应能单独运行 |
| 只测正常路径 | 边界和错误路径通常更容易藏 bug |
| `#expect` 失败后继续访问无效值 | 必要前置条件用 `#require` |
| 把性能测试当绝对标准 | 结果受环境和构建模式影响 |
| 一个测试塞入十几个无关断言 | 失败定位困难，拆分测试 |

## 34.10 下章预告

测试保证行为，调试和性能分析保证你能找到问题。下一章讲断言策略、日志、断点、计时、优化属性以及如何避免“凭感觉优化”。
