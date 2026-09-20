+++
title = "16 血泪速查：最容易写错的地方"
linkTitle = "16 常见坑"
weight = 160
date = "2026-09-20T10:30:00+08:00"
type = "docs"
description = "一份按症状索引的速查表：每一条都写清「你会怎么写」「实际发生什么」「正确写法」，全部在本机 Swift 6.4 实跑过"
isCJKLanguage = true
draft = false
+++

# 16 血泪速查：最容易写错的地方

前面 15 章是按**知识结构**组织的，这一章按**症状**组织——你遇到了怪事，来这里对号入座。

每一条都严格写成三行：

- **你会怎么写**：看起来完全合理、甚至别的语言里就是对的写法。
- **实际发生什么**：编译器/运行期真的做了什么（不是"理论上可能"）。
- **正确写法**：照抄就能过。

> ⚠️ 本章所有"实际发生什么"都是在 **Swift 6.4、`-swift-version 6`** 下真跑出来的，包括崩溃信息和退出码。看到 `rc=133` 就是进程被 SIGTRAP 干掉——Swift 的 `Fatal error` 家族统一是这个退出码。

---

## 1. 整数：不是数学

### 1.1 溢出会崩，不是回绕

| | |
| --- | --- |
| **你会怎么写** | `var x = Int.max; x += 1` |
| **实际发生什么** | `Fatal error: arithmetic overflow`，进程收 SIGTRAP、退出码 **133** |
| **正确写法** | 想回绕就写 `x &+= 1`（`&+` `&-` `&*` 同理）；想安全就问 `x.addingReportingOverflow(1).overflow` |

### 1.2 除法向零截断，`%` 跟着被除数

| | |
| --- | --- |
| **你会怎么写** | 以为 `-7 / 2 == -3.5` 会四舍五入，或以为 `-7 % 3 == 2` |
| **实际发生什么** | `-7 / 2` 是 `-3`（朝零砍掉），`-7 % 3` 是 `-1`（符号跟**被除数**）——和 Python 的 `-7 % 3 == 2` **不一样** |
| **正确写法** | 要"向下取整的除法"自己写：`let q = Int(floor(Double(a) / Double(b)))`；要数学取模用 `((a % b) + b) % b` |

```swift
print(-7 / 2, 7 / -2)      // prints: -3 -3
print(-7 % 3, 7 % -3)      // prints: -1 1
```

### 1.3 整数相除得到整数

| | |
| --- | --- |
| **你会怎么写** | `let avg = sum / count` |
| **实际发生什么** | 两个 `Int` 相除还是 `Int`，小数被丢掉；算平均分、比率时静默失精 |
| **正确写法** | 先转浮点：`Double(sum) / Double(count)`。算钱就别用Double，见 [03 章]({{< relref "03-Types-and-Strings.md" >}}) |

### 1.4 `UInt` 不是"更安全的 `Int`"

| | |
| --- | --- |
| **你会怎么写** | 觉得负数没意义，于是把计数写成 `UInt` |
| **实际发生什么** | `UInt(0) - 1` **直接崩**；`UInt(5) &- 7` 给你 `18446744073709551614`——一个看起来非常体面的巨大数字，bug 从这里开始 |
| **正确写法** | 除非在写二进制协议或对接 C，一律用 `Int`。`count`、`index` 这些 API 返回的也都是 `Int` |

---

## 2. 浮点：`==` 不是你以为的那个

### 2.1 `0.1 + 0.2 != 0.3`

| | |
| --- | --- |
| **你会怎么写** | `if 0.1 + 0.2 == 0.3 { }` |
| **实际发生什么** | 假。差值是 `5.551115123125783e-17` |
| **正确写法** | 比较用容差：`abs(a - b) < 1e-9`；金额用整数分单位或 `Decimal` |

### 2.2 `NaN` 连自己都不等于自己

| | |
| --- | --- |
| **你会怎么写** | `if x == .nan { }`，或者在 `Set<Double>` 里去重 |
| **实际发生什么** | `Double.nan == Double.nan` 是 **`false`**；`Set` 里的 `NaN` 行为不可预测（`NaN` 不满足 `Equatable` 的语义假设） |
| **正确写法** | 判 NaN 用 `x.isNaN`；别拿可能含 `NaN` 的 `Double` 当哈希依据 |

### 2.3 `Int(d)` 对 NaN / 无穷 / 超大值会崩

| | |
| --- | --- |
| **你会怎么写** | 从 JSON 里读到一个数是 `Double`，直接 `Int(d)` |
| **实际发生什么** | `Int(Double.nan)` 报 `Fatal error: Double value cannot be converted to Int because it is either infinite or NaN`；`Int(1e300)` 报 `invalid conversion: '1e300' overflows 'Int'` |
| **正确写法** | 处理外部数据用 `Int(exactly: d)`（返回 `Int?`），或者自己先检查 `d.isFinite && d >= -9.2e18 && d <= 9.2e18` |

---

## 3. 字符串：索引不是整数

### 3.1 `s[0]` 永远不合法

| | |
| --- | --- |
| **你会怎么写** | `let first = s[0]`（C++/Python/JS 的习惯） |
| **实际发生什么** | 编译错误。`String.Index` 不是整数，因为 UTF-8 字节 / Unicode 标量 / 扩展字形簇是三套不同的计数单位 |
| **正确写法** | `s.first`、`s.startIndex`、`s[s.index(s.startIndex, offsetBy: 3)]` |

### 3.2 `count` 数的是"字"，不是"字节"

| | |
| --- | --- |
| **你会怎么写** | 用 `s.count` 判断"这个字符串占多少字节"，好分配缓冲区 |
| **实际发生什么** | `"Hello, 世界".count` 是 **9**，`utf8.count` 是 **13**——"世界"各占 3 个字节 |
| **正确写法** | 要字节数就 `Array(s.utf8)` 或 `s.utf8.count`；要交给 C 就先转成 `[CChar]` |

### 3.3 切片长期持有会拖住整个原字符串

| | |
| --- | --- |
| **你会怎么写** | 从几 MB 的日志里 `prefix(20)` 取出一个 `Substring` 存进数组，长期留着 |
| **实际发生什么** | `Substring` 与原字符串**共享内存**，那几 MB 一直不释放。切片不复制数据是把双刃剑 |
| **正确写法** | 长期持有就 `String(slice)` 拷一份 |

### 3.4 按索引逐个取字符是 O(n²)

| | |
| --- | --- |
| **你会怎么写** | `for i in 0..<s.count { let c = s[s.index(s.startIndex, offsetBy: i)] }` |
| **实际发生什么** | 每次 `index(offsetBy:)` 都要从头数字形簇，整个循环变成 O(n²)，长文本上慢得离谱 |
| **正确写法** | `for c in s`；真要随机访问就先 `Array(s)` |

---

## 4. 可选值：`!` 是最贵的一个字符

### 4.1 字典取值永远是可选值

| | |
| --- | --- |
| **你会怎么写** | `let n = dict["count"]! + 1` |
| **实际发生什么** | 键不存在就崩。而且如果**元素类型本身是可选的**（`[String: Int?]`），`dict[key]` 是 `Int??`——你得解两层 |
| **正确写法** | `let n = (dict["count"] ?? 0) + 1`；嵌套可选用 `dict[key] ?? nil` 压平一层 |

### 4.2 `Int("...")` 不认前后空白

| | |
| --- | --- |
| **你会怎么写** | `Int(userInput)`，以为它会自动 trim |
| **实际发生什么** | `Int(" 42 ")` 是 **`nil`**——前后有空白就是解析失败 |
| **正确写法** | 先 `userInput.trimmingCharacters(in: .whitespacesAndNewlines)` 再转 |

### 4.3 可选值插进字符串会带上 `Optional(...)`

| | |
| --- | --- |
| **你会怎么写** | `print("值是 \(maybeInt)")` |
| **实际发生什么** | 打印出 `值是 Optional(5)`，日志里到处是这个字符串，看起来像 bug 又不像 |
| **正确写法** | `"值是 \(maybeInt ?? 0)"`，或者先用 `if let` 解包 |

### 4.4 `try?` 会把嵌套可选压平一层

| | |
| --- | --- |
| **你会怎么写** | 以为 `try? f()` 在 `f` 返回 `T?` 时给你 `T??`，好区分"抛错了"和"返回 nil" |
| **实际发生什么** | SE-0230 之后只给 `T?`，两种失败**糊在一起分不出来** |
| **正确写法** | 要区分就用 `do/catch` + `try`；要区分"空"和"错"就返回 `Result` |

### 4.5 `!` 在没有亲手指认过的地方

| | |
| --- | --- |
| **你会怎么写** | `let name = user.profile!.name`——"这里肯定有值" |
| **实际发生什么** | 一旦不是，`Fatal error: Unexpectedly found nil while unwrapping an Optional value`，线上就是这么炸的 |
| **正确写法** | `guard let profile = user.profile else { return }`。`!` 只留给"刚刚亲手检查过"和单元测试 |

---

## 5. 集合：值语义的边界在哪

### 5.1 遍历时删元素会崩

| | |
| --- | --- |
| **你会怎么写** | `for i in a.indices { if a[i] % 2 == 0 { a.remove(at: i) } }` |
| **实际发生什么** | 数组缩短了，`indices` 还是老的，报 `Fatal error: Index out of range` |
| **正确写法** | `a.removeAll { $0 % 2 == 0 }`；或者倒着遍历 `for i in a.indices.reversed()`；或者先 `filter` 再赋值 |

### 5.2 数组里装引用类型，值语义名存实亡

| | |
| --- | --- |
| **你会怎么写** | `var copy = arr`，然后改副本里那个元素的属性，以为原数组不受影响 |
| **实际发生什么** | 数组本身确实复制了，但**元素是引用**，两个数组指向同一批对象，改一个两个都变 |
| **正确写法** | 元素类型改用 `struct`；确实要独立副本就做深拷贝（例如让元素实现 `copy()` 或走 `Codable`） |

```swift
final class Marker { var x: Int; init(_ v: Int) { x = v } }
let markers = [Marker(1)]
let copy = markers
copy[0].x = 99
print(markers[0].x, copy[0].x)
// prints: 99 99      拷贝的是指针，不是对象
```

### 5.3 字典 / 集合的顺序不保证

| | |
| --- | --- |
| **你会怎么写** | 依赖 `dict.keys` 的遍历顺序，或者断言"输出一定是 `a b c`" |
| **实际发生什么** | 顺序由哈希决定，**同一个程序连跑六次能给你六种排法**（本机实测：`eabcd`、`ebdac`、`adceb`…） |
| **正确写法** | 要稳定顺序就 `dict.keys.sorted()`；测试里别断言未排序的集合字面量 |

### 5.4 `Array(repeating:count:)` 对引用类型只建一个对象

| | |
| --- | --- |
| **你会怎么写** | `let rows = Array(repeating: Row(), count: 3)`，以为拿到三行独立的数据 |
| **实际发生什么** | 拿到的是**同一个对象的三份引用**，改一行三行全变 |

```swift
final class Row { var v = 0 }
let rows = Array(repeating: Row(), count: 3)
rows[0].v = 9
print(rows.map(\.v))
// prints: [9, 9, 9]
```

| | |
| --- | --- |
| **正确写法** | `let rows = (0..<3).map { _ in Row() }`——用 `map` 每次新建 |

### 5.5 `sorted` 不保证稳定

| | |
| --- | --- |
| **你会怎么写** | 按某字段排序，指望相等的元素保持原顺序 |
| **实际发生什么** | Swift 的 `sorted(by:)` **不承诺稳定**。实测 `[(1,"b"),(0,"a"),(1,"a"),(0,"b")]` 按第一个元素排序得到 `["a", "b", "b", "a"]` |
| **正确写法** | 比较器里把"第二关键字"一起写进去，让顺序完全由你决定 |

---

## 6. 值语义与初始化

### 6.1 `let` 锁的是引用，不是对象内部

| | |
| --- | --- |
| **你会怎么写** | 以为 `let user = User()` 之后 `user.name` 也不能改 |
| **实际发生什么** | 类的 `var` 属性照样能改——`let` 锁的是"这个变量指向谁" |
| **正确写法** | 想真的不可变，就把属性写成 `let`，或者用 `struct` + `private(set) var` |

### 6.2 在 `extension` 里加 `init` 能保住成员逐一初始化器

| | |
| --- | --- |
| **你会怎么写** | 在结构体**声明体内**加了个 `init`，发现编译器白送的 `Point(x:y:)` 没了 |
| **实际发生什么** | 只要在类型体内写了任何 `init`，成员逐一初始化器就不再合成；写进 `extension` 则两者都有 |
| **正确写法** | 新初始化器放 `extension`；但**同签名**的放哪都会报 `invalid redeclaration of synthesized memberwise 'init(x:y:)'` |

### 6.3 属性观察器在初始化期间不触发

| | |
| --- | --- |
| **你会怎么写** | 在 `init` 里给属性赋值，指望 `didSet` 跑一遍做校验 |
| **实际发生什么** | 初始化器里的赋值**不触发** `willSet` / `didSet`——刻意设计，避免初始化期间乱响 |
| **正确写法** | 校验逻辑抽成一个方法，在 `init` 里显式调用；或者放进属性的 `set` 里 |

### 6.4 父类的便利初始化器可能"悄悄没了"

| | |
| --- | --- |
| **你会怎么写** | 父类有 `convenience init()`，子类写了自己的指定初始化器，然后 `Child()` |
| **实际发生什么** | 只有当子类把父类**所有**指定初始化器都实现（覆写也算）时，便利初始化器才继续继承；落下一个就报 `missing argument for parameter ...` |
| **正确写法** | 见 [07 章]({{< relref "07-Custom-Types.md" >}})"初始化器的继承"一节 |

---

## 7. 协议与泛型

### 7.1 默认实现没进协议要求 → `any` 上走静态派发

| | |
| --- | --- |
| **你会怎么写** | 只写在 `extension` 里，然后用 `any P` 调用，以为会走具体类型的实现 |
| **实际发生什么** | 走的是扩展里的那份。实测：具体类型调用给 `结构体里的实现`，`any P` 调用给 `扩展里的实现` |
| **正确写法** | 把方法同时写进**协议要求**里 |

### 7.2 `any` 会让关联类型退化成 `Any`

| | |
| --- | --- |
| **你会怎么写** | `let s: any Sequence = [1, 2, 3]`，然后 `s.contains(2)` |
| **实际发生什么** | 元素变成 `Any`，`Any` 不是 `Equatable`，报 `missing argument label 'where:' in call`。`map` / `filter` 还能跑，`contains(_:)` 这类"按值找"的不行 |
| **正确写法** | 写全主关联类型 `any Sequence<Int>`，或者改用泛型 / `some` |

### 7.3 `Equatable` 不会为"带关联值的枚举"凭空出现

| | |
| --- | --- |
| **你会怎么写** | `enum E { case a(Int); case b }` 然后 `E.a(1) == E.a(1)` |
| **实际发生什么** | 报 `referencing operator function '==' on 'Equatable' requires that 'E' conform to 'Equatable'`——**必须显式声明 `: Equatable`**，编译器才帮你合成 |
| **正确写法** | `enum E: Equatable { ... }`；关联值类型本身也得是 `Equatable` |

### 7.4 `CaseIterable` 只有枚举能用

| | |
| --- | --- |
| **你会怎么写** | 给结构体加 `CaseIterable` 想拿到一组预设值 |
| **实际发生什么** | `error: type 'S' does not conform to protocol 'CaseIterable'`——它是枚举专属的，而且要求**没有关联值** |
| **正确写法** | 结构体用 `static let all: [S] = [...]` 自己列 |

---

## 8. 内存与所有权

### 8.1 `weak` 的限制是"指向的类型"，不是"写在哪"

| | |
| --- | --- |
| **你会怎么写** | 听说"`weak` 只能写在类里"，于是放弃在 struct 里打断引用环 |
| **实际发生什么** | `struct Holder { weak var c: C? }` **完全合法**，而且确实是弱引用（实测 `deinit` 会触发、之后变成 `nil`）。真正的限制是**被指向的类型必须是类** |
| **正确写法** | 值类型里放 `weak` 正是打断"类 → 结构体 → 类"引用环的标准手法。反过来，`weak var p: Point?` 会报 `'weak' may only be applied to class and class-bound protocol types` |

### 8.2 同一个变量传进两个 `inout` 参数

| | |
| --- | --- |
| **你会怎么写** | `balance(&p.health, &p.energy)`，觉得两个属性互不相干 |
| **实际发生什么** | 取决于 `p` 是**局部变量**还是**全局变量**：局部变量编译器能静态证明互不相干，放行；全局变量编译通过但**运行期崩**：`Simultaneous accesses to 0x..., but modification requires exclusive access.`（元组的两个元素同理） |
| **正确写法** | 先抄到局部变量：`let h = p.health; balance(&p.health, &p.energy)`；或者把整个结构体一次性传进去 |

### 8.3 `withoutActuallyEscaping` 是一句承诺

| | |
| --- | --- |
| **你会怎么写** | 为了让"非逃逸闭包"能传给 `@escaping` 参数，套一层 `withoutActuallyEscaping`，然后那个闭包其实被存下来了 |
| **实际发生什么** | 编译期完全不报，运行期是未定义行为——崩溃点可能在几个文件之外 |
| **正确写法** | 拿不准就把函数签名改成 `@escaping`，别用这个函数 |

### 8.4 指针不能逃出 `withUnsafe...` 闭包

| | |
| --- | --- |
| **你会怎么写** | 在 `withUnsafeBufferPointer { $0.baseAddress }` 里把指针存下来，闭包外再用 |
| **实际发生什么** | 指向的内存可能已经被回收或搬走，表现为"偶尔算错一个数"，极难定位 |
| **正确写法** | 所有使用都在闭包内完成；确实要逃逸就手工 `allocate` 并配对 `deallocate` |

---

## 9. 并发：编译通过 ≠ 逻辑正确

### 9.1 actor 是可重入的

| | |
| --- | --- |
| **你会怎么写** | 把状态和方法都塞进 `actor`，以为从此安全 |
| **实际发生什么** | actor 只保证"同一时刻一个任务在跑"，**不保证方法不被打断**。每个 `await` 都是让别的任务插进来的口子：两个任务同时从余额 100 各取 100，错误写法实测**两个都成功、余额 -100** |
| **正确写法** | 挂起之后**重新检查**状态，且"检查 → 修改"之间不能再有 `await`；细节见 [09 章]({{< relref "09-Error-Handling-and-Concurrency.md" >}}) |

### 9.2 `@unchecked Sendable` 是承诺，不是检查

| | |
| --- | --- |
| **你会怎么写** | 编译器抱怨类型不是 `Sendable`，加个 `@unchecked Sendable` 让它闭嘴 |
| **实际发生什么** | 编译期从此不再检查，数据竞争留到运行期——而且往往在高负载下才出现 |
| **正确写法** | 先问"它真的线程安全吗"。要共享可变状态就用 `Mutex` 保护起来，或者干脆换成 `actor` / 值类型 |

### 9.3 `Task { }` 里的错误会被静默吞掉

| | |
| --- | --- |
| **你会怎么写** | `Task { try await upload() }`，忘了 `await` 那个 task 的 `.value` |
| **实际发生什么** | 任务照常执行，抛出的错误**没人接**，只是静默失败 |
| **正确写法** | `Task { do { try await upload() } catch { logger.error(...) } }`，或者把值 `await` 出来 |

### 9.4 取消是协作式的

| | |
| --- | --- |
| **你会怎么写** | `task.cancel()`，以为它立刻停下 |
| **实际发生什么** | 只是设了个标志。正在跑的循环不会自己停，只有调用了 `Task.checkCancellation()` / 会抛 `CancellationError` 的 API 才会响应 |
| **正确写法** | 长循环里定期 `try Task.checkCancellation()`；`await` 后的收尾逻辑要能处理"中途被取消" |

### 9.5 在 `async` 函数里阻塞线程

| | |
| --- | --- |
| **你会怎么写** | 在 `async` 函数里用 `DispatchSemaphore.wait()` 或 `Thread.sleep` 等一个结果 |
| **实际发生什么** | 线程池的线程数有限（通常等于核数），阻塞几个就可能让整个并发系统卡死，且极难复现 |
| **正确写法** | `try await Task.sleep(for:)`；要等别的东西就把它也变成 `async` |

---

## 10. 语言细节：看起来对，其实不对

### 10.1 `if x = 1` 不是赋值

| | |
| --- | --- |
| **你会怎么写** | 把 C 的写法带过来 |
| **实际发生什么** | `error: use of '=' in a boolean context, did you mean '=='?`——Swift 明确拦下 |
| **正确写法** | 要比较写 `==`；想"赋值并判断"就用 `if let` / `while let` 这类绑定 |

### 10.2 `Bool?` 不能当条件用

| | |
| --- | --- |
| **你会怎么写** | `let b: Bool? = ...; if b { }` |
| **实际发生什么** | `error: value of optional type 'Bool?' must be unwrapped to a value of type 'Bool'`——Swift 没有真值转换，可选值也不算 |
| **正确写法** | `if b == true { }`，或者 `if let b, b { }` |

### 10.3 `let` 结构体不能调 `mutating` 方法

| | |
| --- | --- |
| **你会怎么写** | `let s = Counter(); s.increment()` |
| **实际发生什么** | `error: cannot use mutating member on immutable value: 's' is a 'let' constant`——值类型的 `let` 是**彻底的**只读 |
| **正确写法** | 改成 `var`；或者让方法返回新值（`func incremented() -> Self`） |

### 10.4 元组下标从 `.0` 开始，标签和位置可以混用

| | |
| --- | --- |
| **你会怎么写** | `let t = (x: 1, y: 2)` 之后写 `t.1` 或 `t["y"]` |
| **实际发生什么** | `t.1` 合法（给的是 `2`）；`t["y"]` 不合法——元组不是字典 |
| **正确写法** | 用位置或标签：`t.0` / `t.x`。要按名字查就改用 `struct` 或字典 |

### 10.5 元组最多 6 个元素能比较

| | |
| --- | --- |
| **你会怎么写** | 拿一个 7 元组写 `a < b` |
| **实际发生什么** | `error: binary operator '<' cannot be applied to two '(Int /* ... repeated 7 times ... */)' operands`——标准库只为 ≤6 元组提供了比较重载 |
| **正确写法** | 超过 6 个就用 `struct`，顺便给它加 `Comparable` |

### 10.6 闭包不能遵守协议

| | |
| --- | --- |
| **你会怎么写** | 想让一个闭包去满足 `protocol Delegate { func didTap() }` |
| **实际发生什么** | 编译不过。函数类型不是具名类型，不能声明协议遵守 |
| **正确写法** | 包一层 `struct` 把闭包存成属性，由结构体去遵守协议 |

### 10.7 字符串插值里写元组要包一层

| | |
| --- | --- |
| **你会怎么写** | `print("坐标 \(x, y)")`（旧教程里的写法） |
| **实际发生什么** | 不是"能跑但不推荐"，而是**编译失败**：编译器把它解析成标准库的 `appendInterpolation(_:default:)`，两个 `Int` 时报 `instance method 'appendInterpolation(_:default:)' requires that 'Int' conform to 'StringProtocol'` |
| **正确写法** | `"坐标 (\(x), \(y))"`，或者 `"坐标 \(String(describing: (x, y)))"` |

---

## 11. 工具链：看着成功，其实没跑

### 11.1 `swiftc -typecheck` 会漏诊断

| | |
| --- | --- |
| **你会怎么写** | 用 `swiftc -typecheck` 当"快速编译"来把关，绿灯就以为能编过 |
| **实际发生什么** | 少数诊断它看不到。实测两个例子：**`missing return`**（只给一句 `expression of type 'String' is unused` 的警告）和**逃逸闭包捕获 `inout` 参数**（一路绿灯）。真编一次才报 |
| **正确写法** | `-typecheck` 用来换即时反馈没问题，**发版前必须跑完整编译**（`swift build` / `swiftc` 不带 `-typecheck`） |

### 11.2 `swift(>=6.0)` 判断的是语言模式

| | |
| --- | --- |
| **你会怎么写** | `#if swift(>=6.0)` 来判断"工具链够不够新" |
| **实际发生什么** | 用 Swift 6.4 的工具链、但不加 `-swift-version 6` 时，它是**假**的——它看的是语言模式 |
| **正确写法** | 判断工具链用 `compiler(>=6.0)`，判断语言模式才用 `swift(>=6.0)` |

### 11.3 `assert` 在发布版本里被整个删掉

| | |
| --- | --- |
| **你会怎么写** | `assert(cleanup())`，或者用 `assert` 校验用户输入 |
| **实际发生什么** | `assert` 的条件表达式在 `-O` 下**根本不会被求值**，副作用一起消失；`-Ounchecked` 下更彻底（连同数组越界检查都没了） |
| **正确写法** | 有副作用的调用单独写一行；校验外部输入用 `precondition` 或正经的错误处理。⚠️ 但要"任何构建都拦得住"，只有 `preconditionFailure` 和 `fatalError` 靠得住——详见 [15 章]({{< relref "15-Macros-and-Debugging.md" >}}) 那张实测表 |

### 11.4 `@_cdecl` 导出的函数忘了 `public`

| | |
| --- | --- |
| **你会怎么写** | 写了 `@_cdecl("swift_add") func swiftAdd(...)`，直接编译成库给 C 用 |
| **实际发生什么** | 符号还在二进制里（`nm libadd.dylib` 能看到小写 `t _swift_add`），但**不在导出表**里（`nm -gU` 为空），链接时报 `Undefined symbols: _swift_add` |
| **正确写法** | 加上 `public`，`nm -gU` 里就变成大写 `T _swift_add` |

### 11.5 格式化输出依赖区域设置

| | |
| --- | --- |
| **你会怎么写** | 测试里断言 `XCTAssertEqual("\(1234.5.formatted())", "1,234.5")` |
| **实际发生什么** | 换一个 `Locale` 就是另一种千分位/小数点，CI 和本地结果不一致 |
| **正确写法** | 断言数值本身，或者给 `FormatStyle` 显式指定 `.locale(Locale(identifier: "en_US"))` |

---

## 收尾：怎么用这一章

这张表的价值不在"看完记住"，而在**出事时能对上号**。真遇到怪问题，先按症状在下面三处里找：

| 症状 | 先看 |
| --- | --- |
| 程序**崩**了，退出码 133 | 第 1 节（溢出）、第 4.5 节（`!`）、第 5.1 节（遍历时删）、第 8.2 节（`inout` 冲突）、第 15 章（断言家族） |
| 结果**静默错**了，不崩 | 第 1.2 / 1.3 节（整数除法取余）、第 2 节（浮点）、第 5.2 / 5.4 节（引用语义）、第 9.1 节（actor 重入） |
| 编译**不过**，但我觉得没错 | 第 3.1 节（`s[0]`）、第 7.2 节（`any` + 关联类型）、第 10.1 / 10.2 节（`=` 与 `Bool?`）、第 10.5 节（7 元组） |

💭 最后一句真心话：这份速查表里最省时间的从来不是"正确写法"那一列，而是**"实际发生什么"那一列**。编译器说的话往往和你想问的不是一回事——它说 `Index out of range`，你以为是数组越界，其实是遍历时把数组改短了。能读懂它的原话，比记住任何一条语法都值钱。
