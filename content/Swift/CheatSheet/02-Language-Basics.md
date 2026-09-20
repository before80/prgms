+++
title = "02 语言主干"
linkTitle = "02 语言主干"
weight = 20
date = "2026-09-16T11:00:00+08:00"
type = "docs"
description = "常量与变量、运算符优先级、控制流、let 绑定语法全表与模式匹配"
isCJKLanguage = true
draft = false
+++

# 02 语言主干

## 常量与变量

```swift
let pi = 3.14159        // 常量，赋值一次就锁死
var count = 0           // 变量，可以再改
count += 1

let explicit: Double = 1        // 显式类型注解
let a = 1, b = 2, c = 3         // 一行声明多个
var x = 0, y = 0
```

🔥 **默认写 `let`，编译器报"变量从未被修改"时再改成 `var`。** 编译器给出的这条警告是在帮你，不是在烦你。

| 规则 | 说明 |
| --- | --- |
| `let` 绑定的是**值**，不是引用 | 对 `let` 数组不能追加元素，即使数组内容本身是引用类型 |
| 初始化必须在使用之前完成 | `let` 可以延后赋值，但只能赋一次 |
| 作用域结束即销毁 | 没有 `var` 提升之类的历史包袱 |
| 顶层代码 | 只有 `main.swift` 或单文件脚本里能直接写语句 |

## 类型速览

Swift 是**静态强类型**语言：类型在编译期就定死，且**不做隐式数值转换**。

| 类型 | 种类 | 代表 |
| --- | --- | --- |
| `Int` `Double` `Bool` `Character` `String` | 值类型 | 整数默认 `Int`，浮点默认 `Double` |
| `Array` `Dictionary` `Set` | 值类型 | 写时复制，见 [10 内存与值语义]({{< relref "10-Memory-and-Value-Semantics.md" >}}) |
| `struct` `enum` | 值类型 | 自定义类型的主流选择 |
| `class` `actor` `closure` | 引用类型 | 共享状态的场合才需要 |

```swift
let i = 1
let d = 3.0
// let bad = i + d            // 🛑 error: binary operator '+' cannot be applied to operands of type 'Int' and 'Double'
let ok = Double(i) + d        // ✅ 必须显式转换
let truncated = Int(d)        // 3，浮点转整数是截断而非四舍五入

let s = "42"
let parsed = Int(s)           // Int? 而不是 Int —— 转换可能失败
```

⚠️ `Int(d)` 对 `3.9` 得到 `3`（直接砍掉小数）；要四舍五入用 `Int(d.rounded())`。这一步的差异在统计金额时会开出一张很难查的罚单。

## 运算符全表

### 算术与位运算

| 运算符 | 含义 | 示例 |
| --- | --- | --- |
| `+` `-` `*` `/` | 四则运算 | `7 / 2 == 3`，整数除法**向零截断** |
| `%` | 取余 | 结果符号跟**被除数**：`-7 % 3 == -1` |
| `&+` `&-` `&*` | 溢出环绕 | `Int.max &+ 1 == Int.min`，调试时也不崩溃 |
| `<<` `>>` | 移位 | `1 << 4 == 16` |
| `&<<` `&>>` | 环绕移位 | 连**移位量**都按位宽取模：`Int8(1) &<< 8 == 1` |
| `&` `\|` `^` `~` | 按位与 / 或 / 异或 / 取反 | `0b1010 & 0b0110 == 0b0010` |

⚠️ Swift 的 `+` 默认**不**允许溢出，溢出会直接崩溃。这是刻意设计：宁可当场崩，也不要带着错误结果继续跑。真要环绕就用 `&+`。

⚠️ 移位是个例外：`<<` `>>` 自己**不做溢出检查**，顶掉符号位也照样出结果（`Int8(1) << 7 == -128`、`Int8(1) << 8 == 0`）。它们是「聪明移位」，超出位宽时按规则归零或补符号位，而不是取模——这一点和 `&<<` `&>>` 正好相反，后文有专段对比。

```swift
print(Int.max)
// prints: 9223372036854775807
print(Int.max &+ 1)
// prints: -9223372036854775808
print(Int8.max, Int8.min, UInt8.max)
// prints: 127 -128 255
```

### 比较与逻辑

| 运算符 | 说明 |
| --- | --- |
| `==` `!=` | 值相等，要求类型实现 `Equatable` |
| `===` `!==` | 引用相等，只能比 `class` / `actor` 实例；闭包要先 `as AnyObject` 才比得了 |
| `<` `<=` `>` `>=` | 要求 `Comparable`；元组也能比较，逐元素比到分出胜负 |
| `&&` `\|\|` `!` | 短路求值，右操作数可能根本不执行 |
| `? :` | 三元运算符，可以嵌套但别超过一层 |
| `??` | 空合并，见 [06 可选值]({{< relref "06-Optionals.md" >}}) |

```swift
print((1, "b") < (2, "a"))
// prints: true     先比第一个元素，不等就不再往后看
print((1, "b") < (1, "c"))
// prints: true     第一个相等，才继续比第二个
```

⚠️ **Swift 没有"真值"概念。** `if 1 { }` 是编译错误，必须写 `if count > 0 { }`。

顺便记一句：对闭包做引用比较要显式转成对象——`f === g` 会报 `cannot check reference equality of functions`，得写成 `(f as AnyObject) === (g as AnyObject)`。

### `~=`：藏在 `case` 背后的运算符

`switch` 里写 `case 1...10:` 时，编译器其实是在算 `1...10 ~= 你的值`。这个运算符平时看不见，但它是"模式匹配"三个字的实现方式，写 `if case`、`for case` 时用的也是它。

标准库里内置了这么几种：

| 写法 | 走的是哪条 | 例子 |
| --- | --- | --- |
| `值 ~= 值` | 两个 `Equatable` 相等比较 | `3 ~= 3` → `true` |
| `区间 ~= 值` | `RangeExpression` 判断落在区间里 | `1...10 ~= 7` → `true` |
| `Substring ~= String` | 字符串片段与字符串比较 | `"abc".dropFirst() ~= "bc"` → `true` |
| 自定义类型 | 你自己写重载 | 见下 |

```swift
let n = 7

print(3 ~= 3)          // prints: true
print(1...10 ~= n)     // prints: true
print(0..<5 ~= n)      // prints: false

switch n {
case 1...10: print("命中区间")    // 等价于 if 1...10 ~= n
default:     print("没命中")
}
// prints: 命中区间
```

🔥 真正的威力在于**你可以给它加重载**，从而让 `switch` 认识你自己的"形状"：

```swift
struct MultipleOf { let base: Int }

// 参数顺序是 (模式, 待匹配的值)
func ~= (pattern: MultipleOf, value: Int) -> Bool {
    value % pattern.base == 0
}

switch 9 {
case MultipleOf(base: 3): print("3 的倍数")
case MultipleOf(base: 2): print("2 的倍数")
default:                  print("都不是")
}
// prints: 3 的倍数

print(MultipleOf(base: 3) ~= 9)
// prints: true
```

⚠️ 三个容易想歪的点，都实测过：

1. **没有"函数版"重载。** 有人以为 `case isEven:` 能拿一个 `(Int) -> Bool` 当模式，实测报的是 `expression pattern of type '(Int) -> Bool' cannot match values of type 'Int'`——`~=` 要求模式值本身能被"比较"，闭包不在其列。要按条件筛，用 `case let x where isEven(x):`。
2. **`~=` 可以直接调用**，不必写在 `switch` 里：`if 1...10 ~= x { }` 是合法写法。
3. **元组模式是逐元素匹配的**：`case (1, 2):` 相当于两个元素各走一次 `~=`（相等比较也是它的一个重载）。所以自定义模式照样能塞进元组——实测 `case (MultipleOf(base: 3), 4):` 能命中。

### 赋值运算符

`=` 这一族全是右结合、优先级最低，结果是 **`Void` 而不是被赋的那个值**——这点和 C 不一样：`a = b = 1` 在 C 里是链式赋值，在 Swift 里直接报 `cannot assign value of type '()' to type 'Int'`。顺带一提，`let x = (y = 1)` 能编过，但 `x` 的类型是 `()`，编译器会警告 `constant 'x' inferred to have type '()', which may be unexpected`。

| 一类 | 运算符 |
| --- | --- |
| 基本赋值 | `=` |
| 算术复合 | `+=` `-=` `*=` `/=` `%=` |
| 位运算复合 | `<<=` `>>=` `&=` `\|=` `^=` |
| 环绕复合（溢出不崩） | `&+=` `&-=` `&*=` `&<<=` `&>>=` |

环绕复合那五个运算符，一个都别猜，下面全是跑出来的：

```swift
var x = Int.max
x &+= 1
print(x)
// prints: -9223372036854775808     加到顶了，从最小那头绕回来

var y = Int.min
y &-= 1
print(y)
// prints: 9223372036854775807     减到底了，从最大那头绕回来

var z = Int.max
z &*= 2
print(z)
// prints: -2                       0x7FFF...FF × 2 只留低 64 位，符号位成了 1
```

把上面三个例子里的 `&` 去掉、换成普通的 `+=` `-=` `*=`，程序当场就崩：`Fatal error: arithmetic overflow`，进程收 SIGTRAP、退出码 133。`&` 前缀的意思就是「我知道会溢出，别管我」，等于签字画押放弃检查。

```swift
var flags: UInt8 = 0b0000_1111
flags <<= 4
flags |= 0b0000_0001
print(flags, flags >> 4)
// prints: 241 15
```

💭 第二段是位标志的典型动作，逐步拆开就是：`0000_1111` 左移 4 位 → `1111_0000`（240）→ 再按位或上最低位 → `1111_0001`（241）→ 右移 4 位把高 4 位挪回来 → 15。`<<=`、`|=` 和 `+=` 是同一类简写，含义都是"算完再赋回自己"。

#### `&<<=` `&>>=` 和 `<<=` `>>=` 差在哪

平时看不出差别：

```swift
var a: Int8 = 100
a <<= 3
var b: Int8 = 100
b &<<= 3
print(a, b)
// prints: 32 32                    没移过头时，两者完全一样
```

分岔点在**移位量本身超出位宽**的时候。普通 `<<` `>>` 是「聪明移位」（smart shift）：移位量太大时不做取模，而是直接给个兜底结果——左移归 `0`，右移一路补符号位。`&<<` `&>>` 反过来，先把移位量按位宽取模（8 位宽就是 `& 7`），再死板地移那么多位。

```swift
var c: Int8 = 1
c <<= 8
print(c)
// prints: 0                        移过头了，聪明移位给个 0

var d: Int8 = 1
d &<<= 8
print(d)
// prints: 1                        8 & 7 = 0，等于原地没动

var e: Int8 = 1
e &<<= 9
print(e)
// prints: 2                        9 & 7 = 1，只左移 1 位

var f: Int8 = -4
f >>= 9
print(f)
// prints: -1                       右移补符号位，负数最后被填成 -1

var g: Int8 = -4
g &>>= 9
print(g)
// prints: -2                       9 & 7 = 1，等价于 >> 1
```

| 表达式 | 移位量怎么算 | 结果 |
| --- | --- | --- |
| `Int8(1) << 8` | 超过位宽 → 兜底归零 | `0` |
| `Int8(1) &<< 8` | `8 & 7 = 0` | `1` |
| `Int8(1) &<< 9` | `9 & 7 = 1` | `2` |
| `Int8(1) &<< -1` | `-1 & 7 = 7` | `-128` |
| `Int8(-4) >> 9` | 超过位宽 → 一路补符号位 | `-1` |
| `Int8(-4) &>> 9` | `9 & 7 = 1`，即 `>> 1` | `-2` |

⚠️ 顺带纠正一个常见误解：普通 `<<` **并不是安全的那一个**。它不做溢出检查，顶掉符号位照样出结果——`Int8(1) << 7 == -128`，`Int8(64) << 1 == -128`。要精确摆布每一位时，这两个数得在脑子里过一遍。

⚠️ **Swift 里没有这些东西**，别照着别的语言写（报错原文都是实测的）：

| 你写的 | 报什么 |
| --- | --- |
| `i++` / `i--` | `cannot find operator '++' in scope; did you mean '+= 1'?` |
| `2 ** 3` | `cannot find operator '**' in scope`（要么自己定义，要么 `pow`） |
| `x ??= 1` | `cannot find operator '??=' in scope` |
| `x &/= 2` | `cannot find operator '&/=' in scope` |
| `x &%= 2` | `cannot find operator '&%=' in scope`——环绕族只覆盖加、减、乘和移位 |

### 同一个符号，好几种身份

Swift 的符号是复用的。看不清一行代码时，先问"这个符号此刻是哪个身份"：

| 符号 | 身份 |
| --- | --- |
| `&` | 按位与 / 取地址（`f(&x)` 的 `inout`）/ 协议组合（`any A & B`） |
| `?` | 可选类型 `Int?` / 可选链 `a?.b` / 三元 `a ? b : c` / `try?` `as?` |
| `!` | 逻辑非 / 强制解包 `a!` / 隐式解包类型 `Int!` / `try!` `as!` |
| `...` | 闭区间 `1...5` / 前缀区间 `1...` / 可变参数 `Int...` / 模式 `case 1...5:` |
| `..<` | 半开区间 `1..<5` / 模式 `case ..<5:` |
| `.` | 成员访问 / 前导点简写 `.some`（原理见 [06 可选值]({{< relref "06-Optionals.md" >}})）/ 小数 |
| `\` | KeyPath 字面量 `\.name`，见 [11 标准库]({{< relref "11-Standard-Library.md" >}}) |
| `$` | 隐式闭包参数 `$0` `$1`（见 [05 章]({{< relref "05-Functions-and-Closures.md" >}})）/ 属性包装器的投影值 `$name` |
| `:` | 类型标注 / 字典 / 继承列表 / `case` 标签 / 三元的一部分 |
| `_` | 忽略值（`for _ in`、`_ = f()`）/ 省略参数标签 `func f(_ x: Int)` |
| `#` | 编译期指令与自由宏，见 [15 章]({{< relref "15-Macros-and-Debugging.md" >}}) |
| `@` | 声明上的属性，见 [15 章]({{< relref "15-Macros-and-Debugging.md" >}}) |

💭 记忆方式：**符号本身没有含义，位置才有。** 同一个 `&` 出现在表达式里是按位与，出现在调用点的实参前是"把这个变量按引用传进去"，出现在类型位置是"同时满足两个协议"。

### 优先级

从高到低，记住这张表就不用加括号猜了：

| 官方组名（写在 `higherThan:` 里的就是它们） | 运算符 |
| --- | --- |
| `BitwiseShiftPrecedence` | `<<` `>>` `&<<` `&>>` |
| `MultiplicationPrecedence` | `*` `/` `%` `&*` `&` |
| `AdditionPrecedence` | `+` `-` `&+` `&-` `\|` `^` |
| `RangeFormationPrecedence` | `..<` `...` |
| `CastingPrecedence` | `is` `as` `as?` `as!` |
| `NilCoalescingPrecedence` | `??` |
| `ComparisonPrecedence` | `==` `!=` `<` `<=` `>` `>=` `===` `!==` |
| `LogicalConjunctionPrecedence` | `&&` |
| `LogicalDisjunctionPrecedence` | `\|\|` |
| `DefaultPrecedence` | 自定义运算符不指定组时的落脚点，比三元紧 |
| `TernaryPrecedence` | `? :` |
| `FunctionArrowPrecedence` | `->`（只在声明里出现，省得记它排哪儿） |
| `AssignmentPrecedence` | `=` 及其全部复合形式 |

⚠️ 官方组名要写对：`is` / `as` 那一组叫 `CastingPrecedence`，写成 `CastPrecedence` 会报 `unknown precedence group 'CastPrecedence'`（实测）。

```swift
print(2 + 3 * 4)          // prints: 14
print(1 | 2 & 4)          // prints: 1      & 比 | 高
print(1 << 2 + 3)         // prints: 7      移位比加法高
print(true || false && false)   // prints: true   && 比 || 高

let nothing: Int? = nil
print(nothing ?? 0 + 1)   // prints: 1      ?? 比 + 低，右边先算完
```

### 自定义运算符

```swift
import Foundation

infix operator **: MultiplicationPrecedence

func ** (base: Double, exp: Double) -> Double {
    pow(base, exp)
}

print(2 ** 10)
// prints: 1024.0
```

⚠️ 自定义运算符只在自己模块内可见（除非显式 `public`），而且会显著增加代码阅读成本。除非是矩阵、向量这类数学库，建议直接用普通函数名。💭

前缀、后缀运算符要**分开声明**，而且函数名前面必须带上那个关键字：

```swift
import Foundation

prefix operator √
prefix func √ (x: Double) -> Double { x.squareRoot() }

postfix operator °
postfix func ° (x: Double) -> Double { x * .pi / 180 }

print(√16.0, 180.0°)
// prints: 4.0 3.141592653589793
```

💭 声明和定义必须对上：只写了 `prefix operator √` 却把函数定义成 `func √`，实测报 `prefix unary operator missing 'prefix' modifier`。

#### 名字不是想取就能取

运算符名只能用符号，而且有几条硬规矩（下面每一条的报错都是实测原文）：

| 你想写的 | 结果 |
| --- | --- |
| `infix operator **`、`≈`、`⊂`、`§`、`&&&`、`..+` | ✅ 都能声明 |
| `infix operator add`、`a+b`、`€` | ❌ `'add' is considered an identifier and must not appear within an operator name` |
| `infix operator @+` | ❌ `'@' is not allowed in operator names` |
| `infix operator =`、`prefix operator =` | ❌ `cannot declare a custom 'infix' '=' operator`（写 `prefix` 时消息里对应换成 `'prefix'`） |
| `infix operator ?` | ❌ `cannot declare a custom 'infix' '?' operator` |
| `postfix operator ?`、`postfix operator !` | ❌ `postfix operator names starting with '?' or '!' are disallowed to avoid collisions with built-in unwrapping operators` |

💭 一句话总结：**运算符名里不能出现字母数字和 `@`，`=` 与 `?` 不能自定义，后缀运算符不能用 `?` / `!` 开头**——最后这条就是为了不和你天天写的 `value!`、`value?` 打架。

### 自定义优先级组

挂个 `MultiplicationPrecedence` 不总是你要的效果。想让"幂运算"比乘法更紧、而且是右结合，得自己声明一个优先级组：

```swift
precedencegroup PowerPrecedence {
    higherThan: MultiplicationPrecedence   // 比乘法更紧
    associativity: right                   // 右结合
}

infix operator **: PowerPrecedence

func ** (base: Int, exp: Int) -> Int {
    var result = 1
    for _ in 0..<exp { result *= base }
    return result
}

print(2 ** 3 ** 2)
// prints: 512     右结合，等于 2 ** (3 ** 2)
print(2 * 3 ** 2)
// prints: 18      比乘法紧，等于 2 * (3 ** 2)
```

| 键 | 能写什么 | 说明 |
| --- | --- | --- |
| `higherThan` / `lowerThan` | 别的优先级组 | 和已有运算符比高低，可以并列写多个 |
| `associativity` | `left` / `right` / `none` | 同级怎么结合；`none` 的运算符必须加括号 |
| `assignment` | `true` | 声明"赋值类"运算符，天生右结合、优先级最低 |

⚠️ 写了 `assignment: true` 就不能再写 `associativity`——实测直接报语法错误 `expected operator attribute identifier in precedence group body`。

## 区间

| 写法 | 名称 | 包含 |
| --- | --- | --- |
| `1...5` | `ClosedRange` | 1, 2, 3, 4, 5 |
| `1..<5` | `Range` | 1, 2, 3, 4 |
| `1...` | `PartialRangeFrom` | 1 到无限，只能用于取下标或模式 |
| `...5` | `PartialRangeThrough` | 从起点到 5 |
| `..<5` | `PartialRangeUpTo` | 起点到 4 |

```swift
let nums = [10, 20, 30, 40, 50]
print(nums[2...])         // prints: [30, 40, 50]
print(nums[...2])         // prints: [10, 20, 30]
print(nums[..<2])         // prints: [10, 20]
print((1...10).contains(7))   // prints: true

print(Array(stride(from: 0, to: 10, by: 3)))
// prints: [0, 3, 6, 9]
print(Array(stride(from: 10, through: 0, by: -3)))
// prints: [10, 7, 4, 1]
```

💭 `stride` 的 `to:` **不含**终点、`through:` **含**终点，跟 `..<` / `...` 是一套逻辑。步长可以是负数，但方向得和行程一致：`stride(from: 0, to: 10, by: -3)` 得到的是**空序列**，它不会自作主张倒着走。另外 `stride` 本身不是集合，所以要先 `Array(...)` 一下才好直接打印。

⚠️ 区间本身是值，可以反转但不能用 `.reversed()` 当集合：`(1...5).reversed()` 得到的是 `ReversedCollection`，`Array((1...5).reversed())` 才是你要的数组。

⚠️ 还有一件常踩的事：上面 `nums[2...]` 的结果**不是 `Array`，而是 `ArraySlice`**，它保留原数组的下标——切片里的第一项下标是 `2`，所以 `nums[2...][0]` 会直接 `Fatal error: Index out of bounds`（实测）。要拿第一项就写 `slice.startIndex`，想彻底回到"从 0 开始"的普通数组就套一层 `Array(slice)`。展开见 [04 集合与序列]({{< relref "04-Collections.md" >}})。

## 控制流

### if / else if / else

```swift
let score = 87

if score >= 90 {
    print("A")
} else if score >= 80 {
    print("B")
} else {
    print("C")
}
// prints: B
```

### guard：提前退出

`guard` 的语义是"这里必须成立，否则滚出去"。它的 `else` 分支**必须**离开当前作用域（`return` / `break` / `continue` / `throw` / `fatalError()`），而成功绑定出来的变量在后续代码里一直有效——这正是它比嵌套 `if` 好用的原因。

```swift
func process(_ input: String?) {
    guard let text = input, !text.isEmpty else {
        print("输入无效")
        return
    }
    // 从这里开始 text 是非可选 String，不用再解包
    print(text.count)
}
```

### switch：穷尽匹配

```swift
let point = (x: 2, y: 0)

switch point {
case (0, 0):
    print("原点")
case (let x, 0):
    print("在 x 轴上，x = \(x)")
case (0, let y):
    print("在 y 轴上，y = \(y)")
case let (x, y) where x == y:
    print("对角线")
case let (x, y):
    print("普通点 (\(x), \(y))")
}
// prints: 在 x 轴上，x = 2
```

switch 的规则和别的语言不太一样，值得单列一张表：

| 规则 | 说明 |
| --- | --- |
| 必须穷尽 | 少写分支编译器直接报错，除非有 `default` |
| 不穿透 | 匹配到一个 `case` 就结束，不需要 `break` |
| `fallthrough` | 想穿透必须显式写；但**不能穿进**一个会绑值的 `case`（报 `'fallthrough' from a case which doesn't bind variable 'x'`），自己这层带绑定没问题 |
| 值绑定 | `case let (x, y)` 或 `case (let x, 0)` |
| `where` 过滤 | `case let x where x > 0:` |
| 复合 case | `case 1, 3, 5:` 用逗号并列 |
| 区间作为模式 | `case 1...10:` 走的是 `~=` 运算符，见本章「`~=`：藏在 `case` 背后的运算符」 |
| `@unknown default` | 对系统枚举写默认分支，未来新增 case 时给出警告 🔥 |

```swift
let score = 87

switch score {
case 90...:      print("A")
case 80..<90:    print("B")
case 60..<80:    print("C")
default:         print("F")
}
// prints: B
```

### if / switch 作为表达式 🆕

从 Swift 5.9 起，`if` 和 `switch` 可以直接产出值，不用再写"先声明变量再在分支里赋值"那套。

```swift
let n = 5
let parity = if n.isMultiple(of: 2) { "偶数" } else { "奇数" }
print(parity)
// prints: 奇数

let grade = 87
let letter = switch grade {
case 90...:   "A"
case 80..<90: "B"
default:      "C"
}
print(letter)
// prints: B
```

⚠️ 作为表达式时，每个分支都必须产出同一种类型的值，且所有分支都要覆盖到——`switch` 少一个分支，这里就直接报错。

### for-in

```swift
for i in 0..<3 { print(i) }         // 0 1 2
for (index, value) in [10, 20].enumerated() { print(index, value) }
for (key, value) in ["a": 1, "b": 2] { print(key, value) }   // 字典顺序不保证
for _ in 0..<3 { print("重复三次") }  // _ 表示不关心这个值
for c in "abc" { print(c) }          // Character
```

⚠️ `.enumerated()` 发的是**从 0 开始重新数的偏移量**，不是原集合的下标——`[10, 20, 30][1...].enumerated()` 得到的是 `(0, 20), (1, 30)`，而不是 `(1, 20), (2, 30)`（实测）。只有当被遍历的正好是整个数组时，这两个概念才碰巧重合。

### while / repeat-while

```swift
var i = 0
while i < 3 { i += 1 }         // 先判断，可能一次都不执行

var j = 0
repeat { j += 1 } while j < 3  // 至少执行一次
```

### break / continue / 标签

```swift
outer: for i in 1...3 {
    for j in 1...3 {
        if j == 2 { continue }      // 跳过本次内层循环
        if i == 3 { break outer }   // 直接跳出外层循环
        print(i, j)
    }
}
// prints:
//   1 1
//   1 3
//   2 1
//   2 3
```

不带标签的 `break` 只跳出当前这一层；想一次跳出多层就得给循环起名字，这是 Swift 里少数必须用到标签的场景。

标签其实能贴在**任何语句**上，不只是循环。`break 标签` 的含义是"立刻离开这个被标记的块"：

| 标签贴在哪 | `break label` 的效果 |
| --- | --- |
| `for` / `while` / `repeat` | 结束整个循环（`continue label` 则是跳到下一轮） |
| `if` | 提前跳出这个分支块 |
| `do { }` | 提前跳出这个块，剩下的语句都不执行 |
| `switch` | 从嵌套的循环里直接结束整个 `switch` |

```swift
let values = [1, 2, 3]

outer: if values.count == 3 {
    for v in values {
        if v == 2 { break outer }      // 直接跳出整个 if 块
        print("处理", v)
    }
    print("不会到这里")
}
// prints: 处理 1
print("继续后面的代码")
// prints: 继续后面的代码
```

💭 贴了标签的 `do { }` 是 Swift 里最接近"goto 一小步"的写法：块尾放一句 `break block`，就能从块中间提前撤出来（比如做完校验就跳过后续步骤），比套一层 `if` 更直白。

```swift
block: do {
    print("第一步")
    break block                      // 想提前收工时把它放在中间
    // print("这行不会执行")
}
// prints: 第一步
```

💭 **Swift 里没有 `goto`**，它连关键字都不是：写 `goto next` 时编译器会把 `goto` 和 `next` 当成两个相邻的标识符，报的是 `consecutive statements on a line must be separated by ';'`（实测）。最接近"跳一下"的三件工具全在上面：贴标签的 `do { }` + `break 标签`（往前跳一段）、`continue 标签`（回到指定循环的下一轮）、`fallthrough`（在 `switch` 里往下穿一格，只能往下，且不能穿进带值绑定的 `case`）。真要写任意跳转的状态机，标准做法是 `while` + `switch` 的状态循环。

## 绑定语法全表：`let` 的搭档们

`let` 单独出现是**声明**；跟在别的关键字后面就变成**绑定（binding）**——"匹配上了就取个名字，匹配不上就走另一条路"。Swift 里能这么写的位置一共就下面这些，一张表看全：

| 写法 | 问的是什么问题 | 匹配不上时 | 完整例子 |
| --- | --- | --- | --- |
| `if let x = opt { }` | 可选值里有值吗 | 走 `else`（可以省略） | 见 [`if let`](#if-let最常用的那一个) |
| `if let x { }`（Swift 5.7 简写） | 同上，变量同名时可省右边 | 同上 | 见 [`if let`](#if-let最常用的那一个) |
| `guard let x = opt else { ... }` | 没值就立刻收摊 | **必须**离开当前作用域 | 见 [`guard let`](#guard-let没值就早点走) |
| `while let x = seq.next()` | 下一个还有吗 | 结束循环 | 见 [`while let`](#while-let一直取到没有为止) |
| `if var x = opt` / `guard var x = opt` | 同上，但要的是**可改的副本** | 同 `if let` / `guard let` | 见 [`if var` / `guard var`](#if-var--guard-var解出来的是副本) |
| `if case let .ok(code) = value` | 它是这个形状吗 | 走 `else` | 见 [`case let`](#case-let让绑定跟着模式走) |
| `if case let x? = opt` | 有值吗（模式写法） | 走 `else` | 见 [`case let`](#case-let让绑定跟着模式走) |
| `for case let x? in list` | 这一项有值吗 | 跳过这一项 | 见 [`case let`](#case-let让绑定跟着模式走) |
| `case let (x, y)` / `case .some(let v)` | `switch` 里的分支绑定 | 换下一个 `case` | 见 [`case let`](#case-let让绑定跟着模式走) |
| `catch let e as MyError` | 是这个具体错误类型吗 | 漏给下一个 `catch` | 见 [`catch let`](#catch-let按类型接住错误) |
| `if let a, let b, a < b` | 一串条件全成立吗 | 任何一段失败就整体短路 | 见 [逗号就是"而且"](#逗号就是而且多段绑定的求值顺序) |

### `if let`：最常用的那一个

问"这个可选值里有东西吗"，有就取出来用，没有就走 `else`：

```swift
let rawInput: String? = "42"

if let value = Int(rawInput ?? "") {
    print("解析成功：\(value)")
} else {
    print("解析失败")
}
// prints: 解析成功：42
```

Swift 5.7 起，**要解包的东西和取出来的名字一样**时可以只写一遍：

```swift
let nickname: String? = "小龟"

if let nickname {          // 等价于 if let nickname = nickname
    print("你好，\(nickname)")
}
// prints: 你好，小龟
```

⚠️ 简写只认"同名"这一种情况：要解的是 `nickname`，就只能写 `if let nickname`，不能写 `if let name`。想换名字还是得写全 `if let name = nickname`。

### `guard let`：没值就早点走

`guard let` 和 `if let` 解的是同一个包，区别在**解出来的值能活多久**：

```swift
func greet(_ name: String?) -> String {
    guard let name else { return "没有名字" }   // 没值就立刻离开当前作用域
    return "你好，\(name)"                     // 从这里往下，name 已经是 String，不用再解包
}

print(greet("Swift"), greet(nil))
// prints: 你好，Swift 没有名字
```

💭 怎么选不用犹豫：**解包后只在接下来几行里用 → `if let`；解包后要在后面一大段代码里用 → `guard let`。** `guard` 的 `else` 分支必须真的离开当前作用域，`return`、`break`、`continue`、`throw`、`fatalError()` 都行，忘了写编译器会拦你。

### `while let`：一直取到没有为止

`popLast()` 返回 `Int?`，栈空了就是 `nil`，循环自然结束——这是"边消耗边处理"最干净的写法：

```swift
var stack = [1, 2, 3]
while let top = stack.popLast() {
    print(top)
}
// prints:
//   3
//   2
//   1
```

后面同样可以接逗号条件，边解包边判断：

```swift
var head: Int? = 3
while let h = head, h > 0 {
    print(h)
    head = h - 1
}
// prints:
//   3
//   2
//   1
```

### `if var` / `guard var`：解出来的是副本

```swift
let settings: [String: Int]? = ["port": 80]

if var s = settings {          // s 是解包出来的副本
    s["port"] = 8080
    print(s["port"] ?? 0, settings?["port"] ?? 0)
}
// prints: 8080 80
```

🔥 `if var` 改的永远是**副本**——值类型语义在这里一样成立，原可选值纹丝不动。要改回原处，得让原变量自己参与赋值。

```swift
func double(_ input: Int?) -> Int {
    guard var x = input else { return -1 }
    x *= 2
    return x
}
print(double(21), double(nil))
// prints: 42 -1
```

### 逗号就是"而且"：多段绑定的求值顺序

```swift
let a: Int? = 1
let b: Int? = nil

if let a, let b, a < b {
    print("a < b")
} else {
    print("前两段有一个是 nil，第三段根本没机会执行")
}
// prints: 前两段有一个是 nil，第三段根本没机会执行
```

⚠️ 逗号连接的每一段**从左往右求值，一旦失败就整体短路**。所以后面的条件可以放心依赖前面解出来的变量——不用嵌套 `if`，也不用担心它是空的。这就是 `if let` 比"层层嵌套"强的关键。

它还能和 `#available` 这类条件混着写——而且**顺序绝对不能反**：

```swift
@available(macOS 13, *)
func modern() -> Int { 9 }

if #available(macOS 13, *), let v = Optional(modern()) {
    print(v)
}
// prints: 9
```

这段里有两套长得像、作用完全不同的"版本检查"，先分清：

| 写法 | 是什么 | 谁在管 |
| --- | --- | --- |
| `@available(macOS 13, *)` 贴在 `func` 上 | **声明**：这个函数只有 macOS 13 起才存在 | 编译期。从此在低版本上下文里点名调用它就是错误 |
| `#available(macOS 13, *)` 写在 `if` 里 | **检查**：眼下这台机器够格吗 | 运行期求值；同时它还是编译器放行 `modern()` 的**通行证** |

末尾那个 `*` 省不得，它表示"其他平台（iOS、Linux……）不设版本要求"。少写它，报错原文是 `must handle potential future platforms with '*'`。

⚠️ 把绑定挪到 `#available` 前面，编译直接不过：

```text
if let v = Optional(modern()), #available(macOS 13, *) {
   🛑 error: 'modern()' is only available in macOS 13 or newer
      note: add 'if #available' version check
}
```

原因就是上面那句"逗号从左往右求值"：`#available` 先立住，后面的 `modern()` 才有资格露面。整条 `if` 的实际执行顺序是——**先问系统版本 → 版本够，才去算 `modern()` 并包成 `Int?` → 解包成 `v` → 进花括号打印**。

💭 中间那层 `Optional(modern())` 是刻意绕的一下：`modern()` 本来就返回非可选的 `Int`，把它塞进 `Optional` 只是为了凑出一个"可选绑定"，好演示 availability 检查和可选绑定能挤在同一串条件里。真实代码里直接写 `let v = modern()` 就行。

💭 顺带一提：如果 App 的部署目标本来就是 macOS 13 或更高，这个检查恒为真，写了不报错，只是多余。

### `case let`：让绑定跟着模式走

```swift
enum Status { case ok(Int), failed }
let s = Status.ok(200)

if case let .ok(code) = s {
    print("code", code)
}
// prints: code 200
```

可选值也能写成模式，加一个后缀 `?` 就表示"有值才匹配"——效果和 `if let` 一样，但它能和其他模式拼在一起：

```swift
let maybe: Int? = 7

if case let x? = maybe {          // 等价于 if case .some(let x) = maybe
    print("有值：\(x)")
}
// prints: 有值：7
```

同一套模式放进 `for`，就变成"只处理有值的那几项"，其余的直接跳过：

```swift
let row: [Int?] = [1, nil, 3]
var picked: [Int] = []

for case let x? in row { picked.append(x) }
print(picked)
// prints: [1, 3]
```

写进 `switch` 时，绑定可以落在元组的某个位置上，也可以只关心"有值没值"：

```swift
func describe(_ pair: (Int, Int)) -> String {
    switch pair {
    case let (x, y) where x < y: "升序 \(x) \(y)"
    case let (x, y) where x > y: "降序 \(x) \(y)"
    default:                     "相等"
    }
}
print(describe((1, 2)), describe((3, 1)), describe((2, 2)))
// prints: 升序 1 2 降序 3 1 相等

func name(of code: Int?) -> String {
    switch code {
    case let v?: "有值：\(v)"      // 有值就绑定到 v
    case nil:    "没有值"
    }
}
print(name(of: 404), name(of: nil))
// prints: 有值：404 没有值
```

`if case`、`for case let`、`while case`、`switch` 里的 `case let` 是同一套东西的不同用法，`while case` 与 `guard case` 见下一节，`case is` / `case let x as T` 这种带类型筛选的写法见 [14 章的模式转换]({{< relref "14-Type-Casting-and-Interop.md" >}})。

### `catch let`：按类型接住错误

```swift
enum NetworkError: Error { case timeout(Int) }

do {
    throw NetworkError.timeout(30)
} catch let e as NetworkError {
    print(e)
} catch {
    print("其他错误")
}
// prints: timeout(30)
```

不写 `as` 的 `catch let e` 拿到的是 `any Error`；加上 `as 具体类型` 就顺手完成了类型筛选。

⚠️ 三条容易混的：

1. `if let x = y` 里的 `x` 是**新的常量**，和外面的同名变量互不干扰；要改就写 `if var x`。
2. `if let` 只能问"有没有值"，问不了"是不是某个 `case`"——后者是 `if case` 的活儿。
3. 5.7 的简写 `if let x` 要求右边那个变量也叫 `x`；`if var x`、`guard var x` 同样支持简写。

💭 一张表记不住也没关系，记住一句话就行：**`let` 前面跟的是谁，就等于在问谁的问题。** `if` 问"有值吗"，`guard` 问"没值就撤吗"，`while` 问"还有下一个吗"，`case` 问"是这个形状吗"。

## `case` 的搭档们

`case` 同样不只在 `switch` 里工作。它的搭档和 `let` 那套是平行的：

| 写法 | 用在哪 | 匹配不上时 |
| --- | --- | --- |
| `if case <模式> = 值 { }` | 只想判断一个形状 | 走 `else` |
| `guard case <模式> = 值 else { }` | 不匹配就提前退出 | 必须离开作用域 |
| `while case <模式> = 值 { }` | 只要还匹配就一直转 | 结束循环 |
| `for case <模式> in 序列 { }` | 只处理匹配的那些元素 | 跳过这一项 |
| `for case <模式> in 序列 where 条件` | 再叠一层过滤 | 跳过这一项 |
| `switch` 里的 `case` | 多分支、且必须穷尽 | 不会发生，编译器盯着 |
| `case let x` / `case .some(let v)` | 分支里顺手绑定 | — |
| `case is T` / `case let x as T` | 判断类型、顺手转型（见 [14 章]({{< relref "14-Type-Casting-and-Interop.md" >}})） | — |
| `case let x where x > 0` | 分支里再加过滤 | 换下一个分支 |
| `@unknown default` | 系统枚举的兜底 | — |

`while case` 是里面最不常见、但偶尔能救场的一个——"只要还处于某种状态就继续"：

```swift
enum Step { case next(Int), done }
let steps: [Step] = [.next(1), .next(2), .next(3), .done]

var i = 0
while case .next(let n) = steps[i] {    // 只要这一项还是 .next 就继续
    print(n)
    i += 1
}
print("停在 \(steps[i])")
// prints:
//   1
//   2
//   3
//   停在 done
```

⚠️ 这个循环是拿 `.done` 当刹车片的：判断条件里 `steps[i]` **先取值、再问形状**。所以序列里一旦没有兜底的 `.done`，`i` 会一路加下去，运行时报 `Fatal error: Index out of range`（实测）。真实代码里要么保证有终止项，要么把边界条件一起写进判断，比如 `i < steps.count, case .next(let n) = steps[i]`。

`guard case` 则是同一件事的"提前退出"版本：

```swift
func check(_ v: Int?) -> String {
    guard case let v? = v else { return "空" }
    return "有 \(v)"
}
print(check(5), check(nil))
// prints: 有 5 空
```

## `where` 的搭档们

`where` 是 Swift 里"到处打补丁"的那个词，它贴在不同位置干的是同一件事：**再加一条必须成立的条件**。

| 贴在哪 | 写法 | 作用 |
| --- | --- | --- |
| `case` 后面 | `case let x where x > 0:` | 分支匹配后再过滤 |
| `for` 后面 | `for x in list where x > 0` | 遍历时过滤，相当于 `continue` |
| `catch` 后面 | `catch let e where e is FileError` | 按条件挑错误 |
| 泛型参数 | `func f<T>() where T: Hashable` | 约束类型参数（见 [08 章]({{< relref "08-Protocols-and-Generics.md" >}})） |
| 泛型参数 | `func f<A, B>(_ a: A, _ b: B) where A.Element == B.Element` | 多条件、精确匹配 |
| 扩展上 | `extension Array where Element: Comparable` | 只在这个条件下才有这些成员 |
| 关联类型 | `associatedtype Item where Item: Hashable` | 约束关联类型 |

```swift
enum FileError: Error { case missing(String), denied(String) }

do {
    throw FileError.missing("a.txt")
} catch let e where e is FileError {
    print("带 where 的 catch:", e)
} catch {
    print("其他")
}
// prints: 带 where 的 catch: missing("a.txt")
```

⚠️ `for ... where` 只是"看着像过滤"，它和 `filter` 有个区别：`where` 里的条件在**每一轮**都重新求值，而 `filter` 会先把所有元素过一遍。数据量大又只想要前面几个时，`for ... where { ...; break }` 更省。

## 模式匹配的非主流用法

模式匹配不只在 `switch` 里能用，`if` / `guard` / `for` / `while` 都能接 `case`：

```swift
enum Status { case ok, failed(code: Int) }

let s = Status.failed(code: 500)

if case .failed(let code) = s, code >= 500 {
    print("服务端错误 \(code)")
}
// prints: 服务端错误 500

func mustBeOK(_ s: Status) {
    guard case .ok = s else { return }
    print("一切正常")
}

let list: [Int?] = [1, nil, 3]
for case let value? in list {      // 只处理非 nil 的元素
    print(value)
}
// prints:
//   1
//   3
```

## 收尾清理：defer

`defer` 里的代码在离开当前作用域时执行，无论正常返回还是抛错，而且**后进先出**。适合成对资源的收尾。

```swift
func work() {
    defer { print("第二个执行") }
    defer { print("第一个执行") }
    print("主体")
}
work()
// prints:
//   主体
//   第一个执行
//   第二个执行
```

⚠️ `defer` 不会在进程被杀、`fatalError`、`exit()` 时执行——它管的是作用域，不是进程生命周期。

## 写起来最舒服的几种遍历

同一件事，Swift 有至少四种写法。选哪种看你想表达什么。

{{< tabpane text=true persist=disabled >}}

{{% tab header="for-in（最直白）" %}}

```swift
var total = 0
for value in [1, 2, 3, 4] {
    total += value * 2
}
print(total)
// prints: 20
```

副作用明确、可读性最好，有 `break` / `continue` 需求时只有它合适。

{{% /tab %}}

{{% tab header="map / filter（表达转换）" %}}

```swift
let total = [1, 2, 3, 4].map { $0 * 2 }.reduce(0, +)
print(total)
// prints: 20

let evens = [1, 2, 3, 4].filter { $0.isMultiple(of: 2) }
print(evens)
// prints: [2, 4]
```

没有副作用，写成一条链反而更容易看懂"数据是怎么变的"。

{{% /tab %}}

{{% tab header="forEach（只为副作用）" %}}

```swift
[1, 2, 3].forEach { print($0) }
// prints:
//   1
//   2
//   3
```

⚠️ `forEach` 里的 `return` 只结束当前这一轮，相当于 `continue`，**不能**当 `break` 用。需要提前退出就老老实实写 `for-in`。

{{% /tab %}}

{{% tab header="for case / where（过滤 + 遍历）" %}}

```swift
let nums: [Int?] = [1, nil, 3, 4]

for case let n? in nums where n > 1 {
    print(n)
}
// prints:
//   3
//   4
```

一次性把"解包 + 过滤 + 遍历"写在一行，比在循环体里嵌两层 `if` 清爽。

{{% /tab %}}

{{< /tabpane >}}

## 风格约定

| 事项 | 惯例 |
| --- | --- |
| 类型名 | `UpperCamelCase` |
| 变量、函数 | `lowerCamelCase` |
| 常量 | 也是 `lowerCamelCase`，**不用**全大写 |
| 枚举成员 | `lowerCamelCase`：`case notFound` |
| 布尔 | 读起来像断言：`isEmpty`、`canRetry` |
| 分号 | 不需要，一行一句时省略；一行多句才用 |
| 大括号 | 左括号跟在同一行，这是官方风格 |
