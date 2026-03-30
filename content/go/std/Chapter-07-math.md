+++
title = "第 7 章：数学运算——math、math/big、math/bits、math/cmplx"
weight = 70
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 7 章：数学运算——math、math/big、math/bits、math/cmplx

数学是宇宙的语言，而 Go 的 math 包就是你和这门语言对话的翻译官。从简单的加减乘除到让人头秃的复数运算，Go 标准库提供了全套工具。本章将带你领略 Go 数学工具的魅力，顺便踩踩那些让人欲仙欲死的精度坑。

## 7.1 math 包解决什么问题

math 包是 Go 标准库中处理浮点数数学运算的核心包。它可不是什么"玩具库"，而是实打实的工业级实现——基于 IEEE 754 标准，底层直接调用 CPU 浮点指令。换句话说，当你用 math 包算 sin(π) 的时候，实际上是 CPU 在给你打工。

### 7.1.1 基本的数学计算

加减乘除？不存在的。math 包专注的是"高级"运算——三角函数、对数、开方、幂运算。如果你只是想算 1+1，请左转 basic constants，请勿浪费 math 包的才华。

### 7.1.2 三角函数

math 包提供了完整的三角函数家族：Sin、 Cos、 Tan 及其反函数 Asin、 Acos、 Atan。还记得高数课本上那些令人窒息的公式吗？math 包帮你实现了。

### 7.1.3 对数

自然对数 Log、底数为 10 的 Log10、还有贴心的高精度版本 Log1p（计算 log(1+x)，避免 x 接近 0 时的精度损失）。

### 7.1.4 开方

Sqrt（平方根）是使用最频繁的，毕竟勾股定理谁不爱。Cbrt（立方根）虽然用得少，但关键时刻也能救命。

### 7.1.5 幂运算

Pow(x, y) 计算 x 的 y 次方。看起来简单，但当你知道它内部做了多少优化的时候，你会感激 math 包的存在。

### 7.1.6 浮点数特殊值（无穷大、NaN）

math 包定义了三个"幽灵"值：正无穷大 +Inf、负无穷大 -Inf，以及"不是数字" NaN。它们是 IEEE 754 标准的一部分，理解它们是写出健壮数学代码的前提。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 三角函数：sin(π/2) = 1
	fmt.Println(math.Sin(math.Pi / 2)) // 1

	// 对数
	fmt.Println(math.Log(math.E))    // 1
	fmt.Println(math.Log10(100))     // 2

	// 开方
	fmt.Println(math.Sqrt(16))       // 4
	fmt.Println(math.Cbrt(27))       // 3

	// 幂运算
	fmt.Println(math.Pow(2, 10))     // 1024

	// 特殊值
	fmt.Println(math.Inf(1))         // +Inf
	fmt.Println(math.NaN())           // NaN
}
```

## 7.2 math 核心原理

> **IEEE 754 浮点数的固有限制**
>
> math 包基于 IEEE 754 标准实现浮点数运算。这意味着：浮点数的精度是有限的！你以为的 0.1 + 0.2 = 0.3 在计算机眼里可能是 0.30000000000000004。这不是 bug，是 feature（也是噩梦）。理解这一点，你就能理解为什么比较两个浮点数要用精度阈值，而不是直接用 ==。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 著名的 0.1 + 0.2 问题
	a, b := 0.1, 0.2
	sum := a + b
	fmt.Printf("0.1 + 0.2 = %.20f\n", sum) // 0.30000000000000004441

	// 正确比较方式：使用足够小的误差阈值
	equal := math.Abs(sum-0.3) < 1e-10
	fmt.Println("是否等于 0.3:", equal) // true
}
```

## 7.3 数学常数

math 包贴心地为你准备了一堆数学常数，都是预计算好的float64常量，省去你临时抱佛脚查数学书的麻烦。

### 7.3.1 math.Pi（π≈3.14159...）

圆周率 π，宇宙最重要的常数之一。计算圆面积？先问问 math.Pi。

### 7.3.2 math.E（e≈2.71828...）

自然常数 e，复利公式的核心人物。计算自然指数？找它准没错。

### 7.3.3 math.Sqrt2（√2）

√2 ≈ 1.41421356237，对角线长度计算必备。

### 7.3.4 math.Phi（黄金比例φ≈1.618...）

φ = (1+√5)/2，自然界最神秘的比例，建筑学和艺术家的最爱。

### 7.3.5 math.SqrtE

√e ≈ 1.64872127070，自然常数 e 的平方根。

### 7.3.6 math.Ln2

ln(2) ≈ 0.69314718055，自然对数的经典值。

### 7.3.7 math.Ln10

ln(10) ≈ 2.30258509299，用于对数换底。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Printf("math.Pi    = %.15f\n", math.Pi)    // 3.141592653589793
	fmt.Printf("math.E     = %.15f\n", math.E)     // 2.718281828459045
	fmt.Printf("math.Sqrt2 = %.15f\n", math.Sqrt2) // 1.414213562373095
	fmt.Printf("math.Phi   = %.15f\n", math.Phi)   // 1.618033988749895
	fmt.Printf("math.SqrtE = %.15f\n", math.SqrtE) // 1.648721270700128
	fmt.Printf("math.Ln2   = %.15f\n", math.Ln2)   // 0.693147180559945
	fmt.Printf("math.Ln10  = %.15f\n", math.Ln10)  // 2.302585092994046
}
```

## 7.4 浮点数特殊值

浮点数的世界不只有普通数字，还有三个"幽灵"：正无穷、负无穷、NaN。

### 7.4.1 math.Inf(sign)

返回无穷大。sign > 0 返回正无穷，sign < 0 返回负无穷，sign == 0 你猜？

### 7.4.2 math.NaN()

"Not a Number"，不是数字的数字。它是个"渣男"——既不等于自己，用 == 比较永远返回 false，连 math.NaN() == math.NaN() 都是 false！

### 7.4.3 math.IsInf()

检查一个浮点数是否是无穷大。还能顺便判断是正还是负无穷。

### 7.4.4 math.IsNaN()

检查一个浮点数是否是 NaN。这个函数终于能正确判断 NaN 了，因为 NaN != NaN。

### 7.4.5 正/负无穷大

无穷大不是终点，而是开始。当你除以一个极小的数时，它就会蹦出来。

### 7.4.6 不是数字

NaN 通常在 0.0/0.0 这样的"无效运算"中诞生。它代表了数学上未定义的结果。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 创建特殊值
	posInf := math.Inf(1)   // 正无穷
	negInf := math.Inf(-1)  // 负无穷
	nan := math.NaN()       // NaN

	fmt.Println("正无穷:", posInf)   // +Inf
	fmt.Println("负无穷:", negInf)   // -Inf
	fmt.Println("NaN:", nan)         // NaN

	// 检测特殊值
	fmt.Println("IsInf(posInf):", math.IsInf(posInf, 1)) // true
	fmt.Println("IsNaN(nan):", math.IsNaN(nan))         // true

	// NaN 的奇葩特性
	fmt.Println("NaN == NaN:", nan == nan) // false（永远为 false！）

	// 无穷大的运算
	fmt.Println("1.0 / 0.0 =", 1.0/0.0)   // +Inf
	fmt.Println("-1.0 / 0.0 =", -1.0/0.0) // -Inf
	fmt.Println("math.MaxFloat64 * 2 =", math.MaxFloat64*2) // +Inf
}
```

## 7.5 Inf 和 NaN 的产生

理解这两个"幽灵值"是怎么诞生的，是写出健壮代码的关键。

### 7.5.1 0.0/0.0 = NaN，1.0/0.0 = Inf

这些看似简单的运算，在浮点数世界里有着精确定义：

- 正数 / 0 = +Inf
- 负数 / 0 = -Inf
- 0 / 0 = NaN
- Inf - Inf = NaN
- Inf / Inf = NaN
- sqrt(负数) = NaN

### 7.5.2 了解它们的产生场景，才能调试相关 bug

当你的程序突然输出 NaN 或 Inf 时，不要慌张。顺着运算链往上找，看看是哪一步"越界"了。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// NaN 的产生场景
	nanOps := []float64{
		0.0 / 0.0,              // 0/0
		math.Inf(0) - math.Inf(0), // Inf - Inf
		math.Inf(0) / math.Inf(0), // Inf / Inf
		math.Sqrt(-1),          // 负数开方
		math.Log(-1),           // 负数取对数
	}

	for i, v := range nanOps {
		fmt.Printf("NaN 场景 %d: %v, IsNaN: %v\n", i+1, v, math.IsNaN(v))
	}

	// Inf 的产生场景
	infOps := []float64{
		1.0 / 0.0,              // 正数/0
		-math.MaxFloat64 * 2,   // 溢出
		math.Log(0),            // log(0) = -Inf
		math.Exp(1000),         // e^1000 溢出
	}

	for i, v := range infOps {
		fmt.Printf("Inf 场景 %d: %v, IsInf: %v\n", i+1, v, math.IsInf(v, 0))
	}
}
```

## 7.6 浮点数精度问题

这是每个 Go 程序员（或任何程序员）都必须面对的残酷现实。

### 7.6.1 0.1 + 0.2 ≠ 0.3

0.1 + 0.2 在浮点数里存储的是近似值，所以结果不等于精确的 0.3。这不是 bug，是 IEEE 754 的固有特性。

### 7.6.2 IEEE 754 双精度浮点数的尾数只有 52 位

float64（64位双精度）的组成：1位符号 + 11位指数 + 52位尾数。尾数决定了精度，所以 0.1 这样的十进制小数在二进制里是无限循环的，只能截断存储。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 著名的 0.1 + 0.2 问题
	a, b := 0.1, 0.2
	c := 0.3

	fmt.Printf("a = %.20f\n", a) // 0.10000000000000000555
	fmt.Printf("b = %.20f\n", b) // 0.20000000000000001110
	fmt.Printf("c = %.20f\n", c) // 0.29999999999999998890

	sum := a + b
	fmt.Printf("a + b = %.20f\n", sum) // 0.30000000000000004441

	// 比较方式
	fmt.Println("\n=== 正确的比较方式 ===")
	fmt.Println("a + b == c:", sum == c)           // false（不要用 ==）
	fmt.Println("math.Abs(a+b-c) < 1e-10:", math.Abs(sum-c) < 1e-10) // true

	// 大数吃小数
	big, small := 1e10, 1e-10
	fmt.Printf("\nbig + small = %.10f\n", big+small)
	fmt.Println("small 被大数吃掉了！精度丢失是真实的。")
}
```

## 7.7 绝对值与取整

math 包提供了全套取整函数，每个都有自己的"性格"。

### 7.7.1 Abs（绝对值）

返回浮点数的绝对值。正数还是正数，负数变正数，0 还是 0。

### 7.7.2 Ceil（向上取整）

"天花板取整"——找到大于等于自己的最小整数。3.1 变 4，-3.1 变 -3。

### 7.7.3 Floor（向下取整）

"地板取整"——找到小于等于自己的最大整数。3.1 变 3，-3.1 变 -4。

### 7.7.4 Trunc（向零取整）

"截断取整"——直接砍掉小数部分。3.1 变 3，-3.1 变 -3。向零看齐，不偏不倚。

### 7.7.5 Round（四舍五入）

标准的四舍五入。3.5 变 4，-3.5 变 -3。注意 Go 1.20 之前的 Round 行为有点怪，现在统一了。

### 7.7.6 RoundToEven（银行家舍入）

"银行家舍入"——奇数舍入，偶数舍入。3.5 变 4，2.5 变 2。这种方式在金融计算中可以减少系统性偏差。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	x := 3.7
	y := -3.7

	fmt.Println("=== Ceil（向上取整）===")
	fmt.Printf("Ceil(%.1f) = %.1f\n", x, math.Ceil(x))   //  4.0
	fmt.Printf("Ceil(%.1f) = %.1f\n", y, math.Ceil(y))   // -3.0

	fmt.Println("\n=== Floor（向下取整）===")
	fmt.Printf("Floor(%.1f) = %.1f\n", x, math.Floor(x))   //  3.0
	fmt.Printf("Floor(%.1f) = %.1f\n", y, math.Floor(y))   // -4.0

	fmt.Println("\n=== Trunc（向零取整）===")
	fmt.Printf("Trunc(%.1f) = %.1f\n", x, math.Trunc(x))   //  3.0
	fmt.Printf("Trunc(%.1f) = %.1f\n", y, math.Trunc(y))   // -3.0

	fmt.Println("\n=== Round（四舍五入）===")
	fmt.Printf("Round(3.5)  = %.1f\n", math.Round(3.5))   //  4.0
	fmt.Printf("Round(2.5)  = %.1f\n", math.Round(2.5))   //  3.0
	fmt.Printf("Round(-3.5) = %.1f\n", math.Round(-3.5))  // -3.0

	fmt.Println("\n=== RoundToEven（银行家舍入）===")
	fmt.Printf("RoundToEven(3.5)  = %.1f\n", math.RoundToEven(3.5))   //  4.0
	fmt.Printf("RoundToEven(2.5)  = %.1f\n", math.RoundToEven(2.5))   //  2.0（银行家舍入）
	fmt.Printf("RoundToEven(1.5)  = %.1f\n", math.RoundToEven(1.5))   //  2.0

	fmt.Println("\n=== Abs（绝对值）===")
	fmt.Printf("Abs(%.1f) = %.1f\n", x, math.Abs(x))   //  3.7
	fmt.Printf("Abs(%.1f) = %.1f\n", y, math.Abs(y))   //  3.7
}
```

## 7.8 三角函数

三角函数是数学里的"老熟人"，在图形计算、物理模拟、信号处理等领域广泛应用。

### 7.8.1 Sin

正弦函数，输入弧度，返回 [-1, 1] 之间的值。

### 7.8.2 Cos

余弦函数，和正弦是"好基友"，总是形影不离。

### 7.8.3 Tan

正切函数，cos 为零时结果是无穷大。

### 7.8.4 Asin

反正弦函数，Sin 的反函数。输入 [-1, 1]，返回弧度。

### 7.8.5 Acos

反余弦函数，返回 [0, π] 之间的弧度。

### 7.8.6 Atan

反正切函数，返回 (-π/2, π/2) 之间的弧度。

### 7.8.7 Atan2

两个参数版本的反正切。atan(y/x) 的问题在于当 x 为负或 x=0 时会出错，atan2(y, x) 完美解决了这个问题，能正确计算任意象限的角度。

### 7.8.8 输入输出都是弧度制，不是角度制

重要的事情说三遍：math 包用的是弧度！弧度！弧度！90° = π/2 弧度，180° = π 弧度。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	// 角度转弧度
	deg90 := 90.0
	rad := deg90 * math.Pi / 180
	fmt.Printf("%f° = %f 弧度\n", deg90, rad) // 1.570796 弧度

	fmt.Println("\n=== 三角函数 ===")
	// Sin, Cos, Tan（输入 π/4 弧度 = 45°）
	angle := math.Pi / 4
	fmt.Printf("Sin(π/4) = %.6f\n", math.Sin(angle)) // 0.707107
	fmt.Printf("Cos(π/4) = %.6f\n", math.Cos(angle)) // 0.707107
	fmt.Printf("Tan(π/4) = %.6f\n", math.Tan(angle)) // 1.000000

	fmt.Println("\n=== 反三角函数 ===")
	// Asin, Acos, Atan
	fmt.Printf("Asin(0.5)  = %.6f 弧度 (%.2f°)\n", math.Asin(0.5), math.Asin(0.5)*180/math.Pi)
	fmt.Printf("Acos(0.5)  = %.6f 弧度 (%.2f°)\n", math.Acos(0.5), math.Acos(0.5)*180/math.Pi)
	fmt.Printf("Atan(1.0)  = %.6f 弧度 (%.2f°)\n", math.Atan(1.0), math.Atan(1.0)*180/math.Pi)

	fmt.Println("\n=== Atan2（推荐使用）===")
	// Atan2 能正确处理所有象限
	fmt.Printf("Atan2(1, 1)   = %.6f 弧度 (%.2f°)\n", math.Atan2(1, 1), math.Atan2(1, 1)*180/math.Pi)   // 45°
	fmt.Printf("Atan2(1, -1)  = %.6f 弧度 (%.2f°)\n", math.Atan2(1, -1), math.Atan2(1, -1)*180/math.Pi)  // 135°
	fmt.Printf("Atan2(-1, -1) = %.6f 弧度 (%.2f°)\n", math.Atan2(-1, -1), math.Atan2(-1, -1)*180/math.Pi) // -135°
	fmt.Printf("Atan2(-1, 1)  = %.6f 弧度 (%.2f°)\n", math.Atan2(-1, 1), math.Atan2(-1, 1)*180/math.Pi)  // -45°

	// 典型应用：计算向量角度
	dx, dy := 3.0, 4.0
	angleVec := math.Atan2(dy, dx)
	fmt.Printf("向量(%.1f, %.1f) 与 X 轴夹角 = %.2f°\n", dx, dy, angleVec*180/math.Pi)
}
```

## 7.9 双曲函数

双曲函数是指数函数家族的"近亲"，在神经网络、信号处理、热传导等领域有广泛应用。

### 7.9.1 Sinh

双曲正弦：sinh(x) = (e^x - e^(-x)) / 2

### 7.9.2 Cosh

双曲余弦：cosh(x) = (e^x + e^(-x)) / 2，图像是悬链线形状。

### 7.9.3 Tanh

双曲正切：tanh(x) = sinh(x) / cosh(x)，在神经网络中是著名的激活函数。

### 7.9.4 工程计算（神经网络、信号处理）中常用

tanh 和 sigmoid 是早期神经网络的激活函数宠儿。虽然现在 ReLU 更流行，但双曲函数在 LSTM、GRU 等循环神经网络中仍是核心组件。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	x := 1.0

	fmt.Println("=== 双曲函数 ===")
	fmt.Printf("Sinh(%.1f) = %.6f\n", x, math.Sinh(x))
	fmt.Printf("Cosh(%.1f) = %.6f\n", x, math.Cosh(x))
	fmt.Printf("Tanh(%.1f) = %.6f\n", x, math.Tanh(x))

	// 验证双曲函数恒等式
	fmt.Println("\n=== 验证恒等式 cosh²(x) - sinh²(x) = 1 ===")
	sinhX := math.Sinh(x)
	coshX := math.Cosh(x)
	identity := coshX*coshX - sinhX*sinhX
	fmt.Printf("cosh²(%.1f) - sinh²(%.1f) = %.6f (理论上应该等于 1)\n", x, x, identity)

	// tanh 在神经网络中常用，因为输出在 (-1, 1) 之间且梯度衰减慢
	fmt.Println("\n=== Tanh 在神经网络中 ===")
	 activations := []float64{-2, -1, 0, 1, 2}
	for _, a := range activations {
		fmt.Printf("Tanh(%.1f) = %.6f\n", a, math.Tanh(a))
	}
}
```

## 7.10 对数与指数

对数和指数是数学中的"时间旅行者"，能压缩大数也能膨胀小 数。

### 7.10.1 Log（自然对数）

底数为 e 的对数，ln(x)。数学中的"自然"在这里体现得淋漓尽致。

### 7.10.2 Log1p（log(1+x)，精度更高）

当 x 很小时，直接算 log(1+x) 会有精度损失。Log1p 会先加 1 再取对数，精度更高。这不是吹牛，是数学上的最优解。

### 7.10.3 Log10（10为底）

以 10 为底的对数，用于 pH 值计算、分贝转换等场景。

### 7.10.4 Exp

指数函数 e^x，和 Log 是一对互逆运算。

### 7.10.5 Expm1（e^x-1，精度更高）

当 x 很小时，Exp(x)-1 会有精度损失。Expm1 直接算 e^x-1，精度更高。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("=== 自然对数 Log ===")
	fmt.Printf("Log(1)   = %.6f (ln(1) = 0)\n", math.Log(1))
	fmt.Printf("Log(math.E) = %.6f (ln(e) = 1)\n", math.Log(math.E))

	fmt.Println("\n=== Log1p 高精度版本 ===")
	// 当 x 很小时，Log1p 比 Log(1+x) 更精确
	x := 1e-10
	fmt.Printf("x = %.10f\n", x)
	fmt.Printf("Log(1+x)    = %.20f\n", math.Log(1+x))
	fmt.Printf("Log1p(x)    = %.20f\n", math.Log1p(x))
	fmt.Printf("真实值(约)  = %.20f\n", x) // ln(1+x) ≈ x 当 x 很小时

	fmt.Println("\n=== Log10（10为底） ===")
	fmt.Printf("Log10(100)   = %.1f\n", math.Log10(100))   // 2
	fmt.Printf("Log10(1000)  = %.1f\n", math.Log10(1000))  // 3
	fmt.Printf("Log10(1e-6)  = %.1f\n", math.Log10(1e-6))  // -6

	fmt.Println("\n=== Exp（指数） ===")
	fmt.Printf("Exp(0)   = %.1f\n", math.Exp(0))    // 1
	fmt.Printf("Exp(1)   = %.6f (≈ e)\n", math.Exp(1))

	fmt.Println("\n=== Expm1 高精度版本 ===")
	smallX := 1e-15
	fmt.Printf("x = %.20f\n", smallX)
	fmt.Printf("Exp(x)-1  = %.20f\n", math.Exp(smallX)-1)
	fmt.Printf("Expm1(x)  = %.20f\n", math.Expm1(smallX))
	fmt.Printf("真实值(约) = %.20f\n", smallX)

	fmt.Println("\n=== 对数换底公式 ===")
	// log_a(b) = ln(b) / ln(a)
	base := 2.0
	value := 8.0
	logBase := math.Log(value) / math.Log(base)
	fmt.Printf("log₂(8) = %.1f\n", logBase) // 3
}
```

## 7.11 幂与开方

幂运算和开方是inverse关系，math包贴心地提供了全套工具。

### 7.11.1 Pow（x^y）

计算 x 的 y 次方。x^2 是平方，x^0.5 是开方，x^(-1) 是倒数。

### 7.11.2 Sqrt（√x）

平方根。接受任何非负数，负数会返回 NaN。

### 7.11.3 Cbrt（∛x）

立方根。接受所有实数（包括负数），不像 sqrt 那样矫情。

### 7.11.4 Pow10（10^n）

计算 10 的 n 次方，比 Pow(10, n) 更快更精确。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("=== Pow（幂运算） ===")
	fmt.Printf("Pow(2, 10)   = %.0f (2¹⁰ = 1024)\n", math.Pow(2, 10))
	fmt.Printf("Pow(9, 0.5)  = %.1f (√9)\n", math.Pow(9, 0.5))
	fmt.Printf("Pow(2, -1)   = %.1f (2⁻¹ = 0.5)\n", math.Pow(2, -1))
	fmt.Printf("Pow(-2, 3)   = %.1f ((-2)³ = -8)\n", math.Pow(-2, 3))

	fmt.Println("\n=== Sqrt（平方根） ===")
	fmt.Printf("Sqrt(16)   = %.1f\n", math.Sqrt(16))
	fmt.Printf("Sqrt(2)    = %.10f\n", math.Sqrt(2))
	fmt.Printf("Sqrt(-1)   = %.1f (NaN)\n", math.Sqrt(-1))

	fmt.Println("\n=== Cbrt（立方根） ===")
	fmt.Printf("Cbrt(27)   = %.1f (∛27)\n", math.Cbrt(27))
	fmt.Printf("Cbrt(-8)   = %.1f (∛-8)\n", math.Cbrt(-8))
	fmt.Printf("Cbrt(2)    = %.10f (∛2)\n", math.Cbrt(2))

	fmt.Println("\n=== Pow10（10的幂） ===")
	fmt.Printf("Pow10(3)   = %.0f (10³)\n", math.Pow10(3))
	fmt.Printf("Pow10(-2)  = %.2f (10⁻²)\n", math.Pow10(-2))
	fmt.Printf("Pow10(15)  = %.0e\n", math.Pow10(15))

	fmt.Println("\n=== 勾股定理 ===")
	// c = √(a² + b²)
	a, b := 3.0, 4.0
	c := math.Sqrt(math.Pow(a, 2) + math.Pow(b, 2))
	fmt.Printf("直角三角形 a=%.1f, b=%.1f, 斜边 c=%.1f\n", a, b, c) // 5
}
```

## 7.12 Max、Min

找最大最小值，看似简单，实则暗藏玄机。

### 7.12.1 最值函数

math.Max(a, b) 和 math.Min(a, b) 接受两个 float64，返回较大/较小的那个。

### 7.12.2 注意 Max/Min 对 NaN 的处理

这是重点！如果参数中有 NaN，结果是 NaN。这和直觉不太一样——你可能期望忽略 NaN，但 Go 的设计是"有 NaN 就返回 NaN"。

```go
package main

import (
	"fmt"
	"math"
)

func main() {
	fmt.Println("=== 基本用法 ===")
	fmt.Printf("Max(3, 7)   = %.1f\n", math.Max(3, 7))
	fmt.Printf("Min(3, 7)   = %.1f\n", math.Min(3, 7))
	fmt.Printf("Max(-5, -2) = %.1f\n", math.Max(-5, -2))

	// 注意：Max/Min 的参数顺序不影响结果
	fmt.Printf("Max(1, 2, 3) 需要用其他方式\n")

	fmt.Println("\n=== NaN 处理（重点！） ===")
	nan := math.NaN()
	fmt.Printf("Max(1.0, NaN) = %.1f\n", math.Max(1.0, nan)) // NaN
	fmt.Printf("Min(NaN, 2.0) = %.1f\n", math.Min(nan, 2.0)) // NaN
	fmt.Println("只要有 NaN，结果就是 NaN！")

	fmt.Println("\n=== 实际应用 ===")
	// 限制数值范围
	value := 150.0
	minVal, maxVal := 0.0, 100.0
	clamped := math.Max(minVal, math.Min(maxVal, value))
	fmt.Printf("将 %.1f 限制在 [%.1f, %.1f] 范围内 = %.1f\n", value, minVal, maxVal, clamped)

	// 找出数组中的最大最小值（用循环）
	values := []float64{3.14, 2.71, 1.41, 1.73, 0.57}
	maxVal = values[0]
	minVal = values[0]
	for _, v := range values[1:] {
		maxVal = math.Max(maxVal, v)
		minVal = math.Min(minVal, v)
	}
	fmt.Printf("数组中最大值 = %.2f, 最小值 = %.2f\n", maxVal, minVal)
}
```

## 7.13 math/big 包解决什么问题

int64 的范围是 ±9×10¹⁸，超出这个范围的计算怎么办？比如计算 100!（100的阶乘）或者 2 的 1000 次方？math/big 就是来解决这个问题的——它提供了任意精度的大数运算，让你能计算"老天文学家才能算出来"的数字。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// int64 的范围限制
	var i64 int64 = 1<<63 - 1
	fmt.Printf("int64 最大值: %d\n", i64)

	// 试试 100!
	fmt.Println("\n=== 100! (阶乘) ===")
	// 用 math/big
	result := new(big.Int)
	result.SetString("1", 10)
	for i := 2; i <= 100; i++ {
		result.Mul(result, big.NewInt(int64(i)))
	}
	fmt.Printf("100! = %d\n", result)
	fmt.Printf("位数: %d 位\n", len(result.String()))

	// 2 的 1000 次方
	fmt.Println("\n=== 2^1000 ===")
	powResult := new(big.Int)
	powResult.Exp(big.NewInt(2), big.NewInt(1000), nil)
	fmt.Printf("2^1000 = %d\n", powResult)
}
```

## 7.14 math/big 核心原理

big 包提供了三种大数类型，各有专长。

### 7.14.1 big.Int（整数精确）

整数运算，永远精确。没有精度问题，没有舍入误差。整数界的"完美主义者"。

### 7.14.2 big.Float（浮点可设精度）

浮点数运算，但精度可以自己设定。精度越高越精确，但运算越慢、占用内存越多。这是速度与精度的权衡。

### 7.14.3 big.Rat（分数精确）

有理数，分子分母分别存储。1/3 就是 1/3，不会变成 0.333333...。数学老师的最爱。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	fmt.Println("=== 三种大数类型 ===")

	// big.Int: 整数精确运算
	i := new(big.Int)
	i.SetString("123456789012345678901234567890", 10)
	fmt.Printf("big.Int:  %s\n", i)

	// big.Float: 浮点可设精度
	f := new(big.Float).SetPrec(100) // 100 位精度
	f.SetString("3.14159265358979323846264338327950288419716939937510")
	fmt.Printf("big.Float (100位精度): %.50f...\n", f)

	// big.Rat: 分数精确
	r := new(big.Rat)
	r.SetString("1/3")
	fmt.Printf("big.Rat:  %s (精确！不是 0.333...)\n", r)
	fmt.Printf("big.Rat to Float: %.20f\n", r.Float64())

	// 对比：1/3 在 float64 中丢失精度
	var f64 float64 = 1.0 / 3.0
	fmt.Printf("float64:  %.20f (精度丢失)\n", f64)
}
```

## 7.15 big.Int 的创建

big.Int 的创建方式有多种，最常用的是 NewInt 和 SetString。

### 7.15.1 NewInt

从 int64 创建一个 big.Int。简单直接。

### 7.15.2 Add

加法。big.Int 是immutable的，Add 返回一个新的 big.Int。

### 7.15.3 Sub

减法。

### 7.15.4 Mul

乘法。

### 7.15.5 Div

除法。整数除法，不保留小数部分。

### 7.15.6 基本算术运算，返回新对象，原对象不变

重要特性！big.Int 是 immutable 的。所有运算都返回新的 big.Int，原始对象不变。这和 strings.Builder 的模式类似。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// 创建 big.Int
	a := big.NewInt(123)
	b := big.NewInt(456)

	fmt.Println("=== 基本算术运算 ===")
	// 注意：所有运算都返回新的 big.Int
	sum := new(big.Int).Add(a, b)
	diff := new(big.Int).Sub(a, b)
	prod := new(big.Int).Mul(a, b)
	quot := new(big.Int).Div(a, b)
	rem := new(big.Int).Rem(a, b)

	fmt.Printf("%d + %d = %d\n", a, b, sum)
	fmt.Printf("%d - %d = %d\n", a, b, diff)
	fmt.Printf("%d × %d = %d\n", a, b, prod)
	fmt.Printf("%d ÷ %d = %d, 余数 = %d\n", a, b, quot, rem)

	fmt.Println("\n=== 大数运算 ===")
	// 计算 Fibonacci 数列的超大值
	fib := make([]*big.Int, 100)
	fib[0] = big.NewInt(0)
	fib[1] = big.NewInt(1)
	for i := 2; i < 100; i++ {
		fib[i] = new(big.Int).Add(fib[i-1], fib[i-2])
	}
	fmt.Printf("F(99) = %d\n", fib[99])
	fmt.Printf("F(99) 的位数: %d 位\n", len(fib[99].String()))
}
```

## 7.16 big.Int 的比较

big.Int 的比较使用的是 Cmp 方法，而不是 ==。

### 7.16.1 Cmp

Compare 方法。返回值有三 种情况。

### 7.16.2 返回 -1

当第一个数小于第二个数时。

### 7.16.3 返回 0

当两个数相等时。

### 7.16.4 返回 1

当第一个数大于第二个数时。类似 strings.Compare。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	a := big.NewInt(100)
	b := big.NewInt(50)
	c := big.NewInt(100)

	fmt.Println("=== Cmp 比较 ===")
	fmt.Printf("%d vs %d: Cmp = %d\n", a, b, a.Cmp(b)) // 1  (a > b)
	fmt.Printf("%d vs %d: Cmp = %d\n", b, a, b.Cmp(a)) // -1 (b < a)
	fmt.Printf("%d vs %d: Cmp = %d\n", a, c, a.Cmp(c)) // 0  (a == c)

	fmt.Println("\n=== 封装成易用的比较函数 ===")
	isLess := func(x, y *big.Int) bool { return x.Cmp(y) < 0 }
	isGreater := func(x, y *big.Int) bool { return x.Cmp(y) > 0 }
	isEqual := func(x, y *big.Int) bool { return x.Cmp(y) == 0 }

	fmt.Printf("%d < %d: %v\n", b, a, isLess(b, a))
	fmt.Printf("%d > %d: %v\n", a, b, isGreater(a, b))
	fmt.Printf("%d == %d: %v\n", a, c, isEqual(a, c))
}
```

## 7.17 big.Int 的位操作

big.Int 虽然是"大数"，但同样支持位运算。这在密码学和算法优化中很有用。

### 7.17.1 And

按位与。

### 7.17.2 Or

按位或。

### 7.17.3 Xor

按位异或。

### 7.17.4 Not

按位取反。

### 7.17.5 Lsh

左移，相当于乘以 2^n。

### 7.17.6 Rsh

右移，相当于除以 2^n（向下取整）。

### 7.17.7 位运算，用于大数算法

位运算在大数算法（如 RSA 加密）中经常用到。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// 创建两个 big.Int 进行位运算
	x := big.NewInt(0b110101) // 53 in decimal
	y := big.NewInt(0b101011) // 43 in decimal

	fmt.Printf("x = %d (二进制: %s)\n", x, fmt.Sprintf("%b", x.Int64()))
	fmt.Printf("y = %d (二进制: %s)\n", y, fmt.Sprintf("%b", y.Int64()))

	fmt.Println("\n=== 位运算 ===")
	and := new(big.Int).And(x, y)
	or := new(big.Int).Or(x, y)
	xor := new(big.Int).Xor(x, y)
	not := new(big.Int).Not(x)

	fmt.Printf("x & y  = %d\n", and) // 001001 = 9
	fmt.Printf("x | y  = %d\n", or)  // 111111 = 63
	fmt.Printf("x ^ y  = %d\n", xor) // 110110 = 54
	fmt.Printf("^x     = %d\n", not) // 反码

	fmt.Println("\n=== 移位运算 ===")
	lsh := new(big.Int).Lsh(x, 3) // x * 2^3
	rsh := new(big.Int).Rsh(x, 2) // x / 2^2
	fmt.Printf("x << 3 = %d (原值 × 8)\n", lsh)
	fmt.Printf("x >> 2 = %d (原值 ÷ 4)\n", rsh)
}
```

## 7.18 big.Int 的字符串转换

big.Int 和字符串之间的转换是大数处理的基础。

### 7.18.1 SetString

从字符串解析 big.Int。第二个参数指定进制（2-36）。

### 7.18.2 从字符串解析，支持不同进制（第二个参数指定进制）

进制支持从 2（二进制）到 36（数字+字母）。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	fmt.Println("=== 字符串解析 ===")

	// 二进制
	bin := new(big.Int)
	bin.SetString("1010", 2)
	fmt.Printf("二进制 1010 = %d\n", bin)

	// 八进制
	oct := new(big.Int)
	oct.SetString("777", 8)
	fmt.Printf("八进制 777 = %d\n", oct)

	// 十六进制
	hex := new(big.Int)
	hex.SetString("FF", 16)
	fmt.Printf("十六进制 FF = %d\n", hex)

	// 36 进制（最大支持）
	base36 := new(big.Int)
	base36.SetString("Z", 36)
	fmt.Printf("36进制 Z = %d\n", base36) // 35

	fmt.Println("\n=== 常用进制转换 ===")
	num := big.NewInt(255)

	// Text 方法：将大整数转为指定进制的字符串
	fmt.Printf("十进制: %s\n", num.Text(10))
	fmt.Printf("二进制: %s\n", num.Text(2))
	fmt.Printf("十六进制: %s\n", num.Text(16))
}
```

## 7.19 big.Float

big.Float 提供了任意精度的浮点数运算。

### 7.19.1 精度控制

big.Float 的精度是可配置的，通过 SetPrec 方法设置。

### 7.19.2 SetPrec 设置精度，精度越高结果越精确但运算越慢

精度以二进制位为单位。float64 对应 53 位精度。精度越高，计算越慢、内存占用越大。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	fmt.Println("=== big.Float 精度控制 ===")

	// 默认精度（53 位，约 16 位十进制）
	f1 := new(big.Float).SetPrec(53)
	f1.SetString("3.141592653589793238462643383279")
	fmt.Printf("53 位精度: %.20f\n", f1)

	// 高精度（100 位）
	f2 := new(big.Float).SetPrec(100)
	f2.SetString("3.141592653589793238462643383279502884197169399375105820974944592307")
	fmt.Printf("100 位精度: %.50f\n", f2)

	// 对比 float64
	var f64 float64 = 3.141592653589793
	fmt.Printf("float64:   %.20f\n", f64)

	fmt.Println("\n=== 精度影响示例 ===")
	// 计算 0.1 + 0.2
	bf := new(big.Float).SetPrec(100)
	bf.SetString("0.1")
	bf.Add(bf, new(big.Float).SetPrec(100).SetString("0.2"))
	fmt.Printf("big.Float: 0.1 + 0.2 = %.20f\n", bf)
	fmt.Printf("float64:   0.1 + 0.2 = %.20f\n", 0.1+0.2)
}
```

## 7.20 big.Float 的方法

big.Float 的算术方法与 big.Int 类似，但处理浮点数。

### 7.20.1 Add

浮点数加法。

### 7.20.2 Sub

浮点数减法。

### 7.20.3 Mul

浮点数乘法。

### 7.20.4 Div

浮点数除法。

### 7.20.5 Sqrt

平方根。

### 7.20.6 和 Int 类似，但处理浮点数

同样的 immutable 模式，同样的方法链风格。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// 创建 big.Float
	a := new(big.Float).SetPrec(100).SetString("10.5")
	b := new(big.Float).SetPrec(100).SetString("3.2")

	fmt.Println("=== big.Float 算术运算 ===")
	sum := new(big.Float).Add(a, b)
	diff := new(big.Float).Sub(a, b)
	prod := new(big.Float).Mul(a, b)
	quot := new(big.Float).Quo(a, b)

	fmt.Printf("%.2f + %.2f = %.4f\n", a, b, sum)
	fmt.Printf("%.2f - %.2f = %.4f\n", a, b, diff)
	fmt.Printf("%.2f × %.2f = %.4f\n", a, b, prod)
	fmt.Printf("%.2f ÷ %.2f = %.4f\n", a, b, quot)

	fmt.Println("\n=== Sqrt ===")
	c := new(big.Float).SetPrec(100).SetString("2")
	sqrtC := new(big.Float).Sqrt(c)
	fmt.Printf("√2 = %.50f\n", sqrtC)
}
```

## 7.21 big.Rat

big.Rat 存储精确的有理数，永远不会丢失精度。

### 7.21.1 有理数

分子分母分别存储，1/3 就是 1/3，不是 0.333...

### 7.21.2 分子分母分别存储，1/3 不会丢失精度，SetString 解析 "3/7" 这样的字符串

你可以直接用字符串 "3/7" 创建一个有理数。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	fmt.Println("=== big.Rat 有理数 ===")

	// 从字符串创建
	r1 := new(big.Rat).SetString("1/3")
	r2 := new(big.Rat).SetString("2/7")

	fmt.Printf("r1 = %s\n", r1)
	fmt.Printf("r2 = %s\n", r2)

	// 加法
	sum := new(big.Rat).Add(r1, r2)
	fmt.Printf("%s + %s = %s\n", r1, r2, sum)

	// 乘法
	prod := new(big.Rat).Mul(r1, r2)
	fmt.Printf("%s × %s = %s\n", r1, r2, prod)

	// 转为浮点数
	f, _ := sum.Float64()
	fmt.Printf("和的浮点值: %.10f\n", f)

	fmt.Println("\n=== 对比 float64 ===")
	var f1, f2 float64 = 1.0/3.0, 2.0/7.0
	sumFloat := f1 + f2
	prodFloat := f1 * f2
	fmt.Printf("float64: 1/3 + 2/7 = %.10f\n", sumFloat)
	fmt.Printf("float64: 1/3 × 2/7 = %.10f\n", prodFloat)

	// 精确值应该是多少？
	fmt.Println("\n精确结果 1/3 + 2/7 = 13/21 ≈ 0.619047619...")
}
```

## 7.22 big.Int 的进制转换

big.Int 提供了 Text 方法将大整数转换为各种进制的字符串。

```go
package main

import (
	"fmt"
	"math/big"
)

func main() {
	// 创建一个很大的整数
	n := new(big.Int)
	// 2^100
	n.Exp(big.NewInt(2), big.NewInt(100), nil)

	fmt.Printf("2^100 = %d\n", n)
	fmt.Printf("十进制: %s\n", n.Text(10))
	fmt.Printf("十六进制: %s\n", n.Text(16))
	fmt.Printf("二进制长度: %d 位\n", n.BitLen())

	// 解析十六进制字符串
	hexStr := "FFFFFFFFFFFFFFFF"
	n2 := new(big.Int)
	n2.SetString(hexStr, 16)
	fmt.Printf("\n十六进制 %s = %d\n", hexStr, n2)
}
```

## 7.23 math/bits 包解决什么问题

math/bits 提供了 CPU 指令级别的位运算函数，是算法优化的利器。

### 7.23.1 位运算是算法优化的基础

位运算在底层无处不在：排序、搜索、加密、压缩......掌握 bits 包，让你的算法飞起来。

### 7.23.2 PopCount（统计1的个数）

统计一个数字的二进制表示中有多少个 1。这是 CPU 指令级别的操作，O(1) 复杂度。

### 7.23.3 Len（最高位位置）

返回最高有效位的位置。对于算法中的缩放和分区很有用。

### 7.23.4 RotateLeft（循环移位）

数据循环移入移出，在密码学和图像处理中常用。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	// PopCount: 统计 1 的个数
	x := 0b10101010 // 170
	fmt.Printf("%d (二进制 %s) 有 %d 个 1\n", x, fmt.Sprintf("%b", x), bits.PopCount(uint(x)))

	// Len: 最高有效位的位置
	fmt.Printf("Len(%d) = %d (因为 %d = %s)\n", 16, bits.Len(16), 16, fmt.Sprintf("%b", 16))

	// RotateLeft: 循环左移
	y := uint8(0b00011111)
	rotated := bits.RotateLeft8(y, 2)
	fmt.Printf("RotateLeft8(%08b, 2) = %08b\n", y, rotated)
}
```

## 7.24 math/bits 核心原理

> **CPU 指令级别的位运算**
>
> math/bits 的函数直接对应 CPU 指令，O(1) 时间复杂度。PopCount 在某些 CPU 上是一条指令（POPCNT），Len 是 BSR 指令。这意味着用 bits 包比自己写循环快 10-100 倍。

```go
package main

import (
	"fmt"
	"math/bits"
	"time"
)

func main() {
	// 对比 bits 包 vs 循环实现
	n := uint(0xFFFFFFFF)

	// bits.PopCount
	start := time.Now()
	for i := 0; i < 1e7; i++ {
		bits.PopCount(n)
	}
	bitsTime := time.Since(start)

	// 循环实现
	start = time.Now()
	for i := 0; i < 1e7; i++ {
		count := 0
		for ; n > 0; n >>= 1 {
			count += int(n & 1)
		}
	}
	loopTime := time.Since(start)

	fmt.Printf("bits.PopCount 耗时: %v\n", bitsTime)
	fmt.Printf("循环实现  耗时: %v\n", loopTime)
	fmt.Printf("bits 快约 %d 倍\n", loopTime/bitsTime+1)
}
```

## 7.25 OnesCount 系列

统计二进制中 1 的个数。

### 7.25.1 PopCount

最常用的函数。统计 uint 中 1 的个数。

### 7.25.2 计算二进制中有多少个 1，是 CPU 指令，O(1)

一条 POPCNT 指令就搞定了，比任何循环都快。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	testCases := []uint{
		0,             // 0000
		1,             // 0001
		0xFF,          // 11111111
		0x5555,        // 0101010101010101
		0xAAAA,        // 1010101010101010
		0xFFFFFFFF,    // 32 个 1
	}

	fmt.Println("=== PopCount ===")
	for _, n := range testCases {
		fmt.Printf("PopCount(%032b) = %d\n", n, bits.PopCount(n))
	}

	// 奇偶性判断：PopCount 的应用
	fmt.Println("\n=== 应用：判断奇偶 ===")
	for _, n := range []uint{1, 2, 3, 4} {
		if bits.PopCount(n)%2 == 0 {
			fmt.Printf("%d 有偶数个 1（偶数）\n", n)
		} else {
			fmt.Printf("%d 有奇数个 1（奇数）\n", n)
		}
	}
}
```

## 7.26 Len 系列

返回最高有效位的位置。

### 7.26.1 Len

返回最高有效位的位置（从 1 开始）。

### 7.26.2 返回最高有效位的位置，Len(16) = 5，因为 16=10000b

注意：Len 返回的是位置（从1开始），不是索引（从0开始）。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== Len 系列 ===")
	testCases := []uint{1, 2, 3, 4, 7, 8, 15, 16, 17, 255, 256}

	for _, n := range testCases {
		fmt.Printf("Len(%d) = %d  (%s)\n", n, bits.Len(n), fmt.Sprintf("%b", n))
	}

	fmt.Println("\n=== 应用 ===")
	// 快速估算数字需要的位数
	n := uint(1000)
	fmt.Printf("数字 %d 需要 %d 位二进制表示\n", n, bits.Len(n))

	// 快速幂运算优化：知道指数的位数可以提前分配空间
	exp := 100
	fmt.Printf("2^%d 需要大约 %d 位二进制\n", exp, bits.Len(1<<exp))
}
```

## 7.27 RotateLeft

循环移位，数据从一端移出又从另一端移入。

### 7.27.1 循环移位

所有移出的位从另一端移入，形成"循环"。

### 7.27.2 数据循环移入移出

在密码学（如 DES）和图像处理（如位图旋转）中常用。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== RotateLeft ===")

	// 8 位循环左移
	for _, shift := range []int{0, 1, 2, 4, 8} {
		x := uint8(0b10110011)
		rotated := bits.RotateLeft8(x, shift)
		fmt.Printf("RotateLeft8(%08b, %2d) = %08b\n", x, shift, rotated)
	}

	fmt.Println("\n=== RotateRight ===")
	x := uint8(0b10110011)
	for _, shift := range []int{1, 2, 4} {
		rotated := bits.RotateLeft8(x, -shift) // 负数是右移
		fmt.Printf("RotateRight8(%08b, %d) = %08b\n", x, shift, rotated)
	}

	fmt.Println("\n=== 16位和32位版本 ===")
	y16 := uint16(0b1111000011110000)
	y32 := uint32(0b11110000111100001111000011110000)

	fmt.Printf("RotateLeft16(%016b, 4) = %016b\n", y16, bits.RotateLeft16(y16, 4))
	fmt.Printf("RotateLeft32(%032b, 8) = %032b\n", y32, bits.RotateLeft32(y32, 8))
}
```

## 7.28 Reverse 系列

比特位反转。

### 7.28.1 比特位反转

将字节或字的位顺序反转。00000001 变成 10000000。

### 7.28.2 字节内位序反转，用于 FFT 等算法

FFT（快速傅里叶变换）需要位反转索引。bit reversal 是 FFT 的基础步骤。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== Reverse 系列 ===")

	testCases := []uint8{1, 2, 3, 4, 5, 10, 128, 255}

	for _, n := range testCases {
		rev := bits.Reverse8(n)
		fmt.Printf("Reverse8(%08b) = %08b\n", n, rev)
	}

	fmt.Println("\n=== 16位和32位 ===")
	x16 := uint16(0x00FF)
	x32 := uint32(0x00FF00FF)

	fmt.Printf("Reverse16(%016b) = %016b\n", x16, bits.Reverse16(x16))
	fmt.Printf("Reverse32(%032b) = %032b\n", x32, bits.Reverse32(x32))

	// FFT 位反转示例
	fmt.Println("\n=== FFT 位反转应用 ===")
	N := 8 // 8 点 FFT
	for i := 0; i < N; i++ {
		rev := bits.Reverse8(uint8(i)) & 7 // 只取低 3 位（&7 等价于保留后3位）
		fmt.Printf("FFT 索引 %d -> 位反转 %d\n", i, rev)
	}
}
```

## 7.29 Add、Sub、Mul、Div

位级算术运算。

### 7.29.1 加减乘除的位级实现

这些函数返回进位或余数，适合底层算法实现。

### 7.29.2 返回进位或余数

Add 返回进位，Div 返回商和余数。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== Add ===")
	a, b := uint(10), uint(20)
	sum, carry := bits.Add(a, b)
	fmt.Printf("%d + %d = %d, 进位 = %d\n", a, b, sum, carry)

	// 溢出示例
	max := uint(^uint(0)) // 最大 uint
	sumOverflow, carryOverflow := bits.Add(max, 1)
	fmt.Printf("%d + 1 = %d, 进位 = %d (溢出检测)\n", max, sumOverflow, carryOverflow)

	fmt.Println("\n=== Sub ===")
	diff, borrow := bits.Sub(20, 8)
	fmt.Printf("20 - 8 = %d, 借位 = %d\n", diff, borrow)

	// 借位示例（20 - 30）
	diffBorrow, borrowBorrow := bits.Sub(20, 30)
	fmt.Printf("20 - 30 = %d, 借位 = %d (负数结果)\n", diffBorrow, borrowBorrow)

	fmt.Println("\n=== Mul ===")
	hi, lo := bits.Mul(6, 7)
	result := (uint64(hi) << 64) | uint64(lo)
	fmt.Printf("6 × 7 = %d (hi=%d, lo=%d)\n", result, hi, lo)

	// 大数乘法
	bigA := uint64(0xFFFFFFFF)
	bigB := uint64(0xFFFFFFFF)
	hiBig, loBig := bits.Mul(bigA, bigB)
	fmt.Printf("0xFFFFFFFF × 0xFFFFFFFF = 0x%X%X\n", hiBig, loBig)

	fmt.Println("\n=== Div ===")
	quo, rem := bits.Div(100, 7)
	fmt.Printf("100 ÷ 7 = %d, 余数 = %d\n", quo, rem)
}
```

## 7.30 LeadingZeros、TrailingZeros

前导零和末尾零计数。

### 7.30.1 前导零和末尾零计数

LeadingZeros 计算前面有多少个 0，TrailingZeros 计算末尾有多少个 0。

### 7.30.2 快速找到第一个/最后一个 1

这在算法中很有用，比如快速找到二进制表示中最左/最右的 1。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== LeadingZeros（前导零）===")
	testCases := []uint{1, 2, 4, 128, 255, 0}
	for _, n := range testCases {
		lz := bits.LeadingZeros(n)
		fmt.Printf("LeadingZeros(%d) = %d (32-%d=%d位有效位)\n", n, lz, lz, 32-lz)
	}

	fmt.Println("\n=== TrailingZeros（末尾零）===")
	tzCases := []uint{8, 16, 24, 32, 0}
	for _, n := range tzCases {
		tz := bits.TrailingZeros(n)
		fmt.Printf("TrailingZeros(%d) = %d (能被 2^%d 整除)\n", n, tz, tz)
	}

	fmt.Println("\n=== 应用 ===")
	// 快速判断是否是 2 的幂
	isPowerOf2 := func(n uint) bool {
		return n != 0 && bits.TrailingZeros(n) == bits.Len(n)-1
	}

	for _, n := range []uint{1, 2, 3, 4, 8, 16, 15} {
		fmt.Printf("%d 是 2 的幂: %v\n", n, isPowerOf2(n))
	}
}
```

## 7.31 Add32、Add64、Sub32、Sub64、Mul32、Mul64：带溢出的加减乘

这些函数是 Add、Sub、Div 的变体，操作特定宽度的整数。

```go
package main

import (
	"fmt"
	"math/bits"
)

func main() {
	fmt.Println("=== 32位运算 ===")

	// Add32
	sum, carry := bits.Add32(1, 2, 0)
	fmt.Printf("Add32(1, 2, 0) = %d, 进位 = %d\n", sum, carry)

	// Sub32
	diff, borrow := bits.Sub32(5, 3, 0)
	fmt.Printf("Sub32(5, 3, 0) = %d, 借位 = %d\n", diff, borrow)

	// Mul32
	hi, lo := bits.Mul32(12345, 6789)
	fmt.Printf("Mul32(12345, 6789) = hi=%d, lo=%d\n", hi, lo)

	fmt.Println("\n=== 溢出示例 ===")
	// 计算 0xFFFFFFFF + 1
	sumOverflow, carryOverflow := bits.Add32(0xFFFFFFFF, 1, 0)
	fmt.Printf("Add32(0xFFFFFFFF, 1, 0) = %d (0x%08X), 进位 = %d\n", sumOverflow, sumOverflow, carryOverflow)

	// 验证
	fmt.Printf("实际结果: 0x%08X (溢出！)\n", uint32(sumOverflow))
}
```

## 7.32 math/cmplx 包解决什么问题

math/cmplx 提供了复数运算支持。

### 7.32.1 复数运算

Go 原生支持 complex 类型，math/cmplx 提供了复数版本的数学函数。

### 7.32.2 复数的加减乘除，三角函数

复数也有自己的 sin、cos、log、pow。

### 7.32.3 对数

复数对数是多值函数，cmplx.Log 返回主值。

### 7.32.4 幂

复数幂运算。

```go
package main

import (
	"fmt"
	"math/cmplx"
)

func main() {
	// 创建复数 3 + 4i
	c := complex(3, 4)
	fmt.Printf("复数: %v\n", c)
	fmt.Printf("模长: %.1f\n", cmplx.Abs(c))

	// 复数运算
	c1 := complex(1, 2)
	c2 := complex(3, 4)

	fmt.Println("\n=== 复数基本运算 ===")
	fmt.Printf("%v + %v = %v\n", c1, c2, c1+c2)
	fmt.Printf("%v - %v = %v\n", c1, c2, c1-c2)
	fmt.Printf("%v × %v = %v\n", c1, c2, c1*c2)
	fmt.Printf("%v ÷ %v = %v\n", c1, c2, c1/c2)

	// 复数三角函数
	fmt.Println("\n=== 复数三角函数 ===")
	z := complex(0, 0)
	fmt.Printf("Sin(%v) = %v\n", z, cmplx.Sin(z))
	fmt.Printf("Cos(%v) = %v\n", z, cmplx.Cos(z))

	// 复数对数
	fmt.Println("\n=== 复数对数 ===")
	fmt.Printf("Log(1+0i) = %v\n", cmplx.Log(complex(1, 0)))
	fmt.Printf("Log(i)    = %v\n", cmplx.Log(complex(0, 1)))
}
```

## 7.33 math/cmplx 核心原理

> **complex128 与 complex64**
>
> Go 支持两种复数类型：complex64（实部虚部各32位）和 complex128（实部虚部各64位）。complex 函数从实部和虚部构造复数。

```go
package main

import (
	"fmt"
	"math/cmplx"
)

func main() {
	// 创建复数
	c64 := complex(1, 2)  // 自动推断为 complex128
	c128 := complex(1.5, 2.5)

	fmt.Printf("c64:  %T = %v\n", c64, c64)
	fmt.Printf("c128: %T = %v\n", c128, c128)

	// 从实部虚部构造
	realPart := 3.0
	imagPart := 4.0
	c := cmplx.Rect(5, 0.9273) // 模长 5，角度约 53.13° ≈ arctan(4/3)
	fmt.Printf("构造的复数: %v (模长=%.1f, 角度=%.2f°)\n", c, cmplx.Abs(c), cmplx.Phase(c)*180/cmplx.Abs(cmplx.Exp(complex(0, 1))))
}
```

## 7.34 real、imag：提取复数的实部和虚部

复数由实部和虚部组成，可以单独提取。

```go
package main

import (
	"fmt"
	"math/cmplx"
)

func main() {
	c := complex(3, 4)

	fmt.Printf("复数: %v\n", c)
	fmt.Printf("实部 (real): %.1f\n", real(c))
	fmt.Printf("虚部 (imag): %.1f\n", imag(c))

	// 也可用 cmplx 包的版本
	fmt.Printf("cmplx.Real: %.1f\n", cmplx.Real(c))
	fmt.Printf("cmplx.Imag: %.1f\n", cmplx.Imag(c))

	// 验证：a + bi = complex(a, b)
	a, b := real(c), imag(c)
	c2 := complex(a, b)
	fmt.Printf("\n重新构造: complex(%.1f, %.1f) = %v\n", a, b, c2)
}
```

## 7.35 基本运算

复数的加减乘除和共轭。

### 7.35.1 加减乘除

Go 的复数运算符原生支持这些运算。

### 7.35.2 共轭（Conj）

复数的共轭是把虚部取反。a + bi 的共轭是 a - bi。

### 7.35.3 复数的共轭是把虚部取反

共轭复数在复变函数论和信号处理中很重要。

```go
package main

import (
	"fmt"
	"math/cmplx"
)

func main() {
	c := complex(3, 4)

	fmt.Printf("复数: %v\n", c)
	fmt.Printf("共轭 (Conj): %v\n", cmplx.Conj(c))

	// 验证：z * Conj(z) = |z|²
	product := c * cmplx.Conj(c)
	absSquared := cmplx.Abs(c) * cmplx.Abs(c)
	fmt.Printf("z × Conj(z) = %v\n", product)
	fmt.Printf("|z|² = %.1f\n", absSquared)
	fmt.Printf("相等: %v\n", product == complex(absSquared, 0))
}
```

## 7.36 Abs、Phase、Polar

复数的模长、相角和极坐标转换。

### 7.36.1 模长

复数的模长是从原点到该点的距离。

### 7.36.2 相角

复数与实轴正方向的夹角。

### 7.36.3 极坐标转换

复数可以用笛卡尔坐标 (a, b) 或极坐标 (r, θ) 表示。

### 7.36.4 复数可以用模长和相角表示

z = r(cos θ + i sin θ) = r·e^(iθ)

```go
package main

import (
	"fmt"
	"math"
	"math/cmplx"
)

func main() {
	c := complex(3, 4)

	fmt.Printf("复数: %v\n", c)

	// 模长
	abs := cmplx.Abs(c)
	fmt.Printf("模长 (Abs): %.1f\n", abs)

	// 相角（弧度）
	phase := cmplx.Phase(c)
	fmt.Printf("相角 (Phase): %.4f 弧度\n", phase)
	fmt.Printf("相角: %.2f°\n", phase*180/math.Pi)

	// 极坐标
	r, theta := cmplx.Polar(c)
	fmt.Printf("极坐标: r=%.1f, θ=%.4f rad\n", r, theta)

	// 从极坐标恢复笛卡尔坐标
	cartesian := cmplx.Rect(r, theta)
	fmt.Printf("从极坐标恢复: %v\n", cartesian)

	// 验证欧拉公式
	euler := cmplx.Exp(complex(0, phase)) * r
	fmt.Printf("欧拉公式验证: r×e^(iθ) = %v\n", euler)
}
```

## 7.37 指数、对数、幂、三角函数

复数版本的 math 函数。

### 7.37.1 复数版本的 math 函数

math 包的所有数学函数都有复数版本。

### 7.37.2 Sin

复数正弦。sin(z) = sin(x)cosh(y) + i cos(x)sinh(y)

### 7.37.3 Log

复数对数。Log(z) = ln|z| + i Arg(z)

### 7.37.4 Pow 等

复数幂运算。Pow(z1, z2) = exp(z2 × Log(z1))

```go
package main

import (
	"fmt"
	"math/cmplx"
)

func main() {
	z := complex(1, 1)

	fmt.Printf("复数 z = %v\n", z)

	fmt.Println("\n=== 指数和对数 ===")
	fmt.Printf("Exp(z) = %v\n", cmplx.Exp(z))
	fmt.Printf("Log(z) = %v\n", cmplx.Log(z))

	fmt.Println("\n=== 三角函数 ===")
	fmt.Printf("Sin(z) = %v\n", cmplx.Sin(z))
	fmt.Printf("Cos(z) = %v\n", cmplx.Cos(z))
	fmt.Printf("Tan(z) = %v\n", cmplx.Tan(z))

	fmt.Println("\n=== 反三角函数 ===")
	fmt.Printf("Asin(z) = %v\n", cmplx.Asin(z))
	fmt.Printf("Acos(z) = %v\n", cmplx.Acos(z))
	fmt.Printf("Atan(z) = %v\n", cmplx.Atan(z))

	fmt.Println("\n=== 双曲函数 ===")
	fmt.Printf("Sinh(z) = %v\n", cmplx.Sinh(z))
	fmt.Printf("Cosh(z) = %v\n", cmplx.Cosh(z))
	fmt.Printf("Tanh(z) = %v\n", cmplx.Tanh(z))

	fmt.Println("\n=== 幂运算 ===")
	// z^2
	fmt.Printf("z² = %v\n", cmplx.Pow(z, 2))
	// 2^z
	fmt.Printf("2^z = %v\n", cmplx.Pow(2, z))
	// z 的 z 次方
	fmt.Printf("z^z = %v\n", cmplx.Pow(z, z))

	fmt.Println("\n=== 特殊值 ===")
	// i 的 i 次方（结果是实数！）
	iPowerI := cmplx.Pow(complex(0, 1), complex(0, 1))
	fmt.Printf("i^i = %v (是实数！约等于 %.4f)\n", iPowerI, real(iPowerI))
}
```

---

## 本章小结

本章探索了 Go 标准库中的数学工具家族：

| 包 | 用途 | 关键类型 |
|---|---|---|
| **math** | 基础浮点数学运算 | float64 |
| **math/big** | 任意精度大数运算 | big.Int, big.Float, big.Rat |
| **math/bits** | CPU 级别位运算 | uint, 无类型整数 |
| **math/cmplx** | 复数运算 | complex64, complex128 |

### 核心要点

1. **浮点数精度问题**：0.1 + 0.2 ≠ 0.3 是 IEEE 754 的固有特性，不是 bug。比较浮点数要用误差阈值。

2. **特殊值**：Inf 和 NaN 是浮点数的"幽灵"，理解它们的产生场景是调试数学代码的基础。

3. **大数运算**：当 int64 不够用时，big.Int 提供精确整数运算，big.Float 提供可配置精度的浮点运算，big.Rat 提供精确有理数运算。

4. **位运算优化**：math/bits 包的函数直接对应 CPU 指令，O(1) 复杂度，是算法优化的利器。

5. **复数运算**：math/cmplx 提供了完整的复数数学函数库，从三角函数到指数对数，应有尽有。

> **数学第一法则**：永远不要用 == 比较两个浮点数，除非你确定它们是同一个值直接比较的结果。
