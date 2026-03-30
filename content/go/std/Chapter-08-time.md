+++
title = "第 8 章：和时间打交道——time 包 ⭐"
weight = 80
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第 8 章：和时间打交道——time 包 ⭐

> "时间是什么？时间是程序员最昂贵的资源，也是最难理解的类型。"
> —— 某位被时区折磨过的 Go 开发者

Go 的 `time` 包是标准库中最"贴心"也最"坑人"的包之一。贴心是因为它设计优雅，API 清晰；坑人是因为时区、格式化字符串、Duration vs Time 的区别，分分钟让你怀疑人生。

这一章，我们来彻底征服它。

---

## 8.1 time 包解决什么问题

程序世界里有三大时间难题：

- **"现在几点？"** —— 服务器在纽约，用户在上海，时区转换让人头秃
- **"暂停 5 秒"** —— 你需要等一个人，但 goroutine 不能干等
- **"5 分钟后超时"** —— 网络请求不能无限等待，到点就走人

`time` 包就是来解决这些问题的。它提供了：
- 获取当前时间
- 构造任意时间点
- 时间段计算
- 定时器和休眠
- 时区转换

简单说，**时间和时间段的表示、计算、格式化、解析**，它全包了。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 问题1：现在几点？
    now := time.Now()
    fmt.Println("当前时间：", now)

    // 问题2：暂停5秒
    fmt.Println("开始暂停5秒...")
    time.Sleep(5 * time.Second) // 暂停5秒
    fmt.Println("5秒过去了！我回来了！")

    // 问题3：5秒后超时（用Timer模拟）
    timer := time.NewTimer(5 * time.Second)
    fmt.Println("设置5秒超时...")
    <-timer.C // 等待timer触发
    fmt.Println("超时了！时间到！")
}

// 当前时间： 2024-01-15 10:30:45.123456 +0800 CST m=+0.000123456
// 开始暂停5秒...
// 5秒过去了！我回来了！
// 设置5秒超时...
// 超时了！时间到！
```

**专业词汇解释：**

- **Timer（定时器）**：单次触发的时间控制器，到点通知一次
- **Ticker（周期定时器）**：反复触发，每隔固定时间通知一次

---

## 8.2 time 核心原理：Time vs Duration

这是 Go time 包最核心的概念，**必须搞清楚**：

| 类型 | 含义 | 类比 |
|------|------|------|
| `time.Time` | 时间**点** | 地图上的一个坐标 |
| `time.Duration` | 时间**段** | 两点之间的距离 |

```
    Time（时间点）                    Duration（时间段）
    ┌─────────┐                       ┌─────────────┐
    │ 10:30   │  ───────(2小时)─────▶ │  12:30      │
    └─────────┘                       └─────────────┘
    "现在是几点"                       "持续多久"
```

**时间点 - 时间点 = 时间段**
```go
t1 := time.Date(2024, 1, 1, 10, 0, 0, 0, time.UTC)
t2 := time.Date(2024, 1, 1, 12, 0, 0, 0, time.UTC)
dur := t2.Sub(t1) // 2小时0分0秒
fmt.Println(dur)  // 2h0m0s
```

**时间点 + 时间段 = 新时间点**
```go
t1 := time.Date(2024, 1, 1, 10, 0, 0, 0, time.UTC)
dur := 2 * time.Hour
t2 := t1.Add(dur)
fmt.Println(t2) // 2024-01-01 12:00:00 +0000 UTC
```

**重要规则：**
- `Time` 和 `Duration` 是**完全不同的类型**，不能直接相加（除非做类型转换）
- `Time - Time = Duration`
- `Time + Duration = Time`
- `Time - Duration = Time`

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // Time + Duration = Time（合法）
    t1 := time.Now()
    t2 := t1.Add(3 * time.Hour)
    fmt.Printf("现在 %v，加上3小时是 %v\n", t1.Format("15:04"), t2.Format("15:04"))

    // Time - Time = Duration（合法）
    diff := t2.Sub(t1)
    fmt.Printf("两者相差：%v\n", diff)

    // Time + Time = ❌ 编译错误！
    // t3 := t1 + t2  // cannot add two time.Time values

    // Duration + Duration = Duration（合法）
    total := 2*time.Hour + 30*time.Minute
    fmt.Printf("总时长：%v\n", total)
}

// 现在 10:30:00，加上3小时是 13:30:00
// 两者相差：3h0m0s
// 总时长：2h30m0s
```

---

## 8.3 time.Time：时间点类型

`time.Time` 是 Go 中表示时间点的结构体，它内部包含：

```
time.Time 结构
├── sec    int64   // 自 1970-01-01 00:00:00 UTC 以来的秒数
├── nsec   int32   // 纳秒部分 (0-999999999)
├── loc    *Location // 时区信息
```

当你打印 `time.Time` 时，它会显示完整的时间信息：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, 7, 15, 14, 30, 45, 123456789, time.UTC)

    fmt.Printf("完整时间：%v\n", t)
    // 2024-07-15 14:30:45.123456789 +0000 UTC

    fmt.Printf("年：%d\n", t.Year())      // 2024
    fmt.Printf("月：%d\n", t.Month())     // July
    fmt.Printf("日：%d\n", t.Day())       // 15
    fmt.Printf("时：%d\n", t.Hour())      // 14
    fmt.Printf("分：%d\n", t.Minute())    // 30
    fmt.Printf("秒：%d\n", t.Second())    // 45
    fmt.Printf("纳秒：%d\n", t.Nanosecond()) // 123456789
    fmt.Printf("时区：%v\n", t.Location())   // UTC

    fmt.Printf("Unix时间戳：%d\n", t.Unix())     // 秒
    fmt.Printf("Unix纳秒：%d\n", t.UnixNano())  // 纳秒
}
```

**专业词汇解释：**

- **time.Time**：Go 标准库中表示时间点的结构体，不可直接修改（是值类型但设计为只读）
- **纳秒（Nanosecond）**：十亿分之一秒（10⁻⁹秒），time.Time 的时间精度
- **Location**：时区信息，决定时间如何显示（+0800 还是 UTC）

---

## 8.4 time.Duration：时间段类型

`time.Duration` 是用**整数类型（int64）** 存储的，单位是**纳秒**。

```go
// Duration 实际上就是 int64 的别名
type Duration int64
```

预定义的时间单位常量：

| 常量 | 值 | 说明 |
|------|-----|------|
| `time.Nanosecond` | 1 | 1 纳秒 |
| `time.Microsecond` | 1000 | 1 微秒 = 1000 纳秒 |
| `time.Millisecond` | 1000000 | 1 毫秒 = 100 万纳秒 |
| `time.Second` | 10⁹ | 1 秒 = 10 亿纳秒 |
| `time.Minute` | 60 × 10⁹ | 1 分钟 = 600 亿纳秒 |
| `time.Hour` | 3600 × 10⁹ | 1 小时 |

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // Duration 的底层值
    fmt.Printf("time.Second = %d 纳秒\n", time.Second)           // 1000000000
    fmt.Printf("time.Minute = %d 纳秒\n", time.Minute)         // 60000000000
    fmt.Printf("time.Hour = %d 纳秒\n", time.Hour)             // 3600000000000

    // Duration 可以直接运算
    dur := time.Hour + 30*time.Minute + 45*time.Second
    fmt.Printf("总时长：%v\n", dur) // 1h30m45s

    // Duration 转其他单位
    fmt.Printf("转秒：%.2f 秒\n", dur.Seconds())               // 5445.00 秒
    fmt.Printf("转分：%.2f 分\n", dur.Minutes())               // 90.75 分
    fmt.Printf("转小时：%.2f 小时\n", dur.Hours())             // 1.5125 小时

    // 字符串解析
    d, _ := time.ParseDuration("2h30m")
    fmt.Printf("解析字符串 '2h30m'：%v\n", d)
}
```

**小技巧：**
- `time.Duration` 是 `int64` 的别名，所以 `1 * time.Second` 实际是 `1000000000`
- 乘法时**必须带单位**，`5 * time.Second` 是 5 秒，`5` 只是个整数 5

---

## 8.5 time.Now()：获取当前时间

这是 `time` 包最常用的函数，返回**当前时间点**。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now()
    fmt.Println("当前时间：", now)
    fmt.Println("类型：", now.Format("2006-01-02 15:04:05.000"))

    // 常用场景：记录开始时间
    start := time.Now()
    fmt.Println("任务开始于：", start)

    // 模拟一些工作
    time.Sleep(100 * time.Millisecond)

    // 计算耗时
    elapsed := time.Since(start)
    fmt.Printf("任务耗时：%v\n", elapsed)
}
```

**扩展：`time.Since()`、`time.Until()`**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    past := time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC)

    // Since(t) = Now().Sub(t)，计算从 t 到现在过了多久
    fmt.Printf("从2024年元旦到现在过了：%v\n", time.Since(past))

    future := time.Date(2025, 1, 1, 0, 0, 0, 0, time.UTC)

    // Until(t) = t.Sub(Now())，计算到现在离 t 还有多久
    fmt.Printf("到2025年元旦还有：%v\n", time.Until(future))
}
```

**专业词汇解释：**

- **`time.Now()`**：返回本地时区的当前时间，包含.monotonic（单调时钟）部分
- **`time.Since(t)`**：快捷函数，相当于 `time.Now().Sub(t)`
- **`time.Until(t)`**：快捷函数，相当于 `t.Sub(time.Now())`

---

## 8.6 time.Date：构造指定时间点

`time.Date()` 创建一个精确的 Time 值，所有组件都明确指定。

```go
func Date(year int, month Month, day, hour, min, sec, nsec int, loc *Location) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 构造一个时间：2024年7月15日 14:30:45 + 北京时区
    t := time.Date(2024, time.July, 15, 14, 30, 45, 0, time.FixedZone("CST", 8*3600))

    fmt.Println("构造的时间：", t)
    fmt.Printf("格式化：%s\n", t.Format("2006-01-02 15:04:05"))

    // 构造当前时间的"今天凌晨"
    today := time.Date(time.Now().Year(), time.Now().Month(), time.Now().Day(), 0, 0, 0, 0, time.Local)
    fmt.Println("今天凌晨：", today)

    // 构造"下个月今天"
    nextMonth := time.Now().AddDate(1, 0, 0)
    fmt.Println("下个月今天：", nextMonth.Format("2006-01-02"))
}
```

**注意事项：**
- `month` 参数是 `time.Month` 类型（1-12 的别名），可以用 `time.July` 或直接写 `7`
- `day` 从 1 开始，不是从 0
- 不合法的时间（如 2月30日）会自动溢出到下个月

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 2月没有30日，自动溢出到3月2日
    invalid := time.Date(2024, time.February, 30, 12, 0, 0, 0, time.UTC)
    fmt.Printf("2月30日？自动变成：%s\n", invalid.Format("2006-01-02"))

    // 2024是闰年，2月29日是合法日期
    leapDay := time.Date(2024, time.February, 29, 12, 0, 0, 0, time.UTC)
    fmt.Printf("闰年2月29日：%s 是合法的\n", leapDay.Format("2006-01-02"))

    // 2023年2月29日？不存在！
    invalid2 := time.Date(2023, time.February, 29, 12, 0, 0, 0, time.UTC)
    fmt.Printf("2023年2月29日？自动变成：%s\n", invalid2.Format("2006-01-02"))
}
```

---

## 8.7 Unix 时间戳

Unix 时间戳是自 **1970-01-01 00:00:00 UTC** 以来经过的**秒数**。

> 很多同学问：为什么是 1970 年 1 月 1 日？因为这是 Unix 系统的"生日"！计算机行业有很多"历史遗留问题"，这个算是一个。

```
        Unix 纪元 (1970-01-01 00:00:00 UTC)
              │
              │───────────►───────────│
              0          1700000000   (2023-11-15)
              │           (十位数)     (现在的时间戳)
              ▼
         负数方向 ←───────────│
         (1970年之前的时间)
```

Go 提供了四个函数获取不同精度的时间戳：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now()

    // Unix 时间戳（秒）
    fmt.Printf("Unix 秒：%d\n", now.Unix())

    // Unix 时间戳（毫秒）
    fmt.Printf("Unix 毫秒：%d\n", now.UnixMilli())

    // Unix 时间戳（微秒）
    fmt.Printf("Unix 微秒：%d\n", now.UnixMicro())

    // Unix 时间戳（纳秒）
    fmt.Printf("Unix 纳秒：%d\n", now.UnixNano())

    // 特殊时间点的时间戳
    epoch := time.Date(1970, 1, 1, 0, 0, 0, 0, time.UTC)
    fmt.Printf("1970-01-01 00:00:00 UTC = %d 秒\n", epoch.Unix())

    // 时间戳转回时间
    ts := 1700000000
    t := time.Unix(ts, 0)
    fmt.Printf("时间戳 %d = %s\n", ts, t.Format("2006-01-02 15:04:05"))
}
```

**常见场景：**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 场景1：日志中使用时间戳
    now := time.Now()
    fmt.Printf("[%d] 系统启动\n", now.Unix())

    // 场景2：缓存过期时间（相对时间戳）
    cacheExpiry := now.Add(24 * time.Hour).Unix()
    fmt.Printf("缓存过期时间戳：%d\n", cacheExpiry)

    // 场景3：数据库存储（MySQL 5.6+ 支持毫秒）
    // INSERT INTO logs (created_at) VALUES (FROM_UNIXTIME(1700000000))
    fmt.Printf("存储到数据库：%d\n", now.UnixMilli())

    // 场景4：JWT 令牌过期判断
    claims := map[string]interface{}{
        "exp": now.Add(7 * 24 * time.Hour).Unix(), // 7天后过期
    }
    fmt.Printf("JWT过期时间戳：%d\n", claims["exp"])
}
```

**专业词汇解释：**

- **Unix 纪元（Epoch）**：1970-01-01 00:00:00 UTC，是所有 Unix 时间测量的起点
- **时间戳（Timestamp）**：用一个整数表示时间，方便存储和计算

---

## 8.8 time.Unix：纳秒时间戳转 Time

`time.Unix()` 将 Unix 时间戳（秒 + 纳秒）转换回 `time.Time`。

```go
func Unix(sec int64, nsec int64) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 从时间戳创建时间
    t1 := time.Unix(1700000000, 0)
    fmt.Println("从Unix秒创建：", t1)

    // 带纳秒
    t2 := time.Unix(1700000000, 123456789)
    fmt.Println("带纳秒：", t2)

    // 时间戳互相转换
    now := time.Now()
    ts := now.Unix()
    recovered := time.Unix(ts, 0)
    fmt.Printf("原始时间：%v\n", now)
    fmt.Printf("时间戳：%d\n", ts)
    fmt.Printf("恢复时间：%v（丢失了毫秒精度）\n", recovered)

    // 保留毫秒的正确做法
    tsMilli := now.UnixMilli()
    recoveredMilli := time.UnixMilli(tsMilli)
    fmt.Printf("保留毫秒：%v\n", recoveredMilli)
}
```

**时间戳精度对比：**

| 函数 | 精度 | 用途 |
|------|------|------|
| `Unix()` | 秒 | 通用场景，数据库存储 |
| `UnixMilli()` | 毫秒 | Web API，缓存 |
| `UnixMicro()` | 微秒 | 日志，高精度日志 |
| `UnixNano()` | 纳秒 | 性能分析，科学研究 |

---

## 8.9 time.Parse：把字符串解析成时间

`time.Parse()` 是将**格式化的时间字符串**转换为 `time.Time` 的函数。

```go
func Parse(layout, value string) (Time, error)
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 解析常见格式
    layouts := []string{
        "2006-01-02",                    // 日期
        "15:04:05",                      // 时间
        "2006-01-02 15:04:05",           // 日期+时间
        "2006/01/02 15:04:05",           // 斜杠分隔
        "02 Jan 2006 15:04:05",          // DD Mon YYYY
    }

    for _, layout := range layouts {
        value := "2024-07-15 14:30:45"
        // 用对应的 layout
        t, err := time.Parse(layout, value[:len(layout)])
        if err == nil {
            fmt.Printf("Layout %q -> %v\n", layout, t)
        }
    }

    // 实际解析
    t, err := time.Parse("2006-01-02 15:04:05", "2024-07-15 14:30:45")
    if err != nil {
        panic(err)
    }
    fmt.Println("解析结果：", t)
}
```

**但是！这里有个大坑：**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 问题：假设你在北京，想解析一个字符串时间
    s := "2024-07-15 14:30:00"

    // 用 time.Parse 解析（没有时区信息）
    t, _ := time.Parse("2006-01-02 15:04:05", s)
    fmt.Println("解析结果：", t)
    fmt.Println("时区：", t.Location())

    // 问题来了！这个时间是 UTC 还是本地时间？
    // 答案是：不知道！Parse 默认假设是 UTC！
    // 实际上它会显示为 UTC，但时间值本身没有时区语义
}
```

> **8.10 节会讲到：Go 使用一种独特的参考时间来定义格式化字符串。**

---

## 8.10 Go 独特的参考时间

Go 的时间格式化是**反人类直觉**的！大多数语言用占位符（如 `%Y-%m-%d`），但 Go 用**一个具体的参考时间**来定义格式。

**参考时间：**

```
Mon Jan 2 15:04:05 -0700 MST 2006
```

拆解开来：

| 位置 | 值 | 含义 |
|------|-----|------|
| Mon | Monday | 星期几（缩写） |
| Jan | January | 月份（缩写） |
| 2 | 2 | 一个月中的第几天 |
| 15 | 3 PM | 24小时制小时 |
| 04 | 4 | 分钟 |
| 05 | 5 | 秒 |
| -0700 | -0700 | 时区偏移量 |
| MST | Mountain Standard Time | 时区名称 |
| 2006 | 2006 | 年份 |

**记住口诀：1-2-3-4-5-6-7**

```
1 = 1（一个月中的第几天，1-31）
2 = 2（一年的第几个月，1-12）
3 = 3（小时，0-23 或 1-12）
4 = 4（分钟，0-59）
5 = 5（秒，0-59）
6 = 6（年份的后两位或全部）
7 = 7（时区偏移量如 -0700）
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 14, 30, 45, 123456789, time.FixedZone("CST", 8*3600))

    // 常见格式化输出
    fmt.Printf("日期：%s\n", t.Format("2006-01-02"))
    fmt.Printf("时间：%s\n", t.Format("15:04:05"))
    fmt.Printf("日期时间：%s\n", t.Format("2006-01-02 15:04:05"))
    fmt.Printf("带毫秒：%s\n", t.Format("15:04:05.000"))
    fmt.Printf("中文友好：%s\n", t.Format("2006年01月02日 15时04分05秒"))

    // 时区显示
    fmt.Printf("UTC偏移：%s\n", t.Format("-0700"))
    fmt.Printf("时区名：%s\n", t.Format("MST"))

    // 完整格式
    fmt.Printf("RFC1123Z：%s\n", t.Format("Mon, 02 Jan 2006 15:04:05 -0700"))

    // 反过来：解析时也需要用同样的参考时间
    parsed, _ := time.Parse("2006-01-02", "2024-07-15")
    fmt.Printf("解析结果：%v\n", parsed)
}
```

```
日期：2024-07-15
时间：14:30:45
日期时间：2024-07-15 14:30:45
带毫秒：14:30:45.123
中文友好：2024年07月15日 14时30分45秒
UTC偏移：+0800
时区名：CST
RFC1123Z：Mon, 15 Jul 2024 14:30:45 +0800
解析结果：2024-07-15 00:00:00 +0000 UTC
```

**小技巧：**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 常用格式化模板
    const (
        DateOnly     = "2006-01-02"
        TimeOnly     = "15:04:05"
        DateTime     = "2006-01-02 15:04:05"
        ISO8601      = "2006-01-02T15:04:05Z07:00"
        RFC1123      = "Mon, 02 Jan 2006 15:04:05 MST"
        ChineseStyle = "2006年01月02日 15:04:05"
    )

    t := time.Now()

    fmt.Println("DateOnly:", t.Format(DateOnly))
    fmt.Println("DateTime:", t.Format(DateTime))
    fmt.Println("Chinese:", t.Format(ChineseStyle))
}
```

---

## 8.11 常用格式化常量

Go 预定义了一些常用的格式化常量：

| 常量 | 值 | 说明 |
|------|-----|------|
| `time.ANSIC` | `"Mon Jan _2 15:04:05 2006"` | Unix date 格式 |
| `time.UnixDate` | `"Mon Jan _2 15:04:05 MST 2006"` | 带时区的 Unix date |
| `time.RFC3339` | `"2006-01-02T15:04:05Z07:00"` | ISO 8601 标准 |
| `time.RFC3339Nano` | `"2006-01-02T15:04:05.999999999Z07:00"` | 纳秒精度的 RFC3339 |

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 14, 30, 45, 123456789, time.UTC)

    fmt.Println("ANSIC:")
    fmt.Println("    ", t.Format(time.ANSIC))

    fmt.Println("UnixDate:")
    fmt.Println("    ", t.Format(time.UnixDate))

    fmt.Println("RFC3339:")
    fmt.Println("    ", t.Format(time.RFC3339))

    fmt.Println("RFC3339Nano:")
    fmt.Println("    ", t.Format(time.RFC3339Nano))

    // JSON 序列化常用
    fmt.Println("JSON 日期格式:", t.Format(time.RFC3339))

    // HTTP Header 格式（RFC 7231）
    fmt.Println("HTTP Date:", t.Format("Mon, 02 Jan 2006 15:04:05 GMT"))
}
```

```
ANSIC:
     Mon Jul 15 14:30:45 2024

UnixDate:
     Mon Jul 15 14:30:45 UTC 2024

RFC3339:
     2024-07-15T14:30:45Z

RFC3339Nano:
     2024-07-15T14:30:45.123456789Z

JSON 日期格式: 2024-07-15T14:30:45Z
HTTP Date: Mon, 15 Jul 2024 14:30:45 GMT
```

**专业词汇解释：**

- **RFC3339**：ISO 8601 的一个配置文件，互联网标准日期格式，JSON、API 最常用
- **ISO 8601**：国际标准化组织的时间格式标准，格式如 `2024-07-15T14:30:45Z`

---

## 8.12 time.LoadLocation：加载时区

`time.LoadLocation()` 根据时区名称（如 `"Asia/Shanghai"`）加载 `*Location`。

```go
func LoadLocation(name string) (*Location, error)
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 加载常见时区
    locations := []string{
        "Asia/Shanghai",      // 中国标准时间
        "America/New_York",   // 美国东部时间
        "Europe/London",      // 伦敦时间
        "Asia/Tokyo",         // 日本时间
        "America/Los_Angeles", // 太平洋时间
        "UTC",                // 世界标准时间
    }

    for _, name := range locations {
        loc, err := time.LoadLocation(name)
        if err != nil {
            fmt.Printf("加载 %s 失败: %v\n", name, err)
            continue
        }
        now := time.Now().In(loc)
        fmt.Printf("%-25s -> %s\n", name, now.Format("15:04:05 (MST)"))
    }
}
```

```
Asia/Shanghai              -> 22:30:45 (CST)
America/New_York           -> 09:30:45 (EST)
Europe/London              -> 14:30:45 (GMT)
Asia/Tokyo                 -> 23:30:45 (JST)
America/Los_Angeles        -> 06:30:45 (PST)
UTC                        -> 14:30:45 (UTC)
```

**时区名称怎么记？**

| 地区 | 格式 | 示例 |
|------|------|------|
| 洲/城市 | `Continent/City` | `Asia/Shanghai` |
| 国家/城市 | `Country/City` | `America/New_York` |
| 缩写 | 如 `UTC` | `UTC` |

**常见时区速查：**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 北京时间 vs 纽约时间
    shanghai, _ := time.LoadLocation("Asia/Shanghai")
    newYork, _ := time.LoadLocation("America/New_York")

    now := time.Now()

    fmt.Printf("北京时间：%s\n", now.In(shanghai).Format("2006-01-02 15:04:05"))
    fmt.Printf("纽约时间：%s\n", now.In(newYork).Format("2006-01-02 15:04:05"))

    // 计算时差
    diff := 8 - 5 // 北京 UTC+8，纽约 UTC-5（冬令时可能-4）
    fmt.Printf("时差：%d 小时\n", diff)
}
```

**注意：** `time.LoadLocation` 依赖系统的时区数据库。在 Windows 上可能需要安装。

---

## 8.13 time.FixedZone：创建固定偏移时区

当你没有标准时区名称时（如 `"UTC+8"` 这种），可以用 `time.FixedZone()` 创建一个固定偏移量的时区。

```go
func FixedZone(name string, offset int) *Location
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 创建 UTC+8 的固定时区（类似中国标准时间，但没有夏令时）
    cst := time.FixedZone("CST", 8*3600) // 8小时 = 8*3600秒

    t := time.Date(2024, time.July, 15, 14, 30, 0, 0, cst)
    fmt.Println("使用固定时区：", t)
    fmt.Println("格式化：", t.Format("2006-01-02 15:04:05 -0700"))

    // 创建 UTC-5 的固定时区
    est := time.FixedZone("EST", -5*3600)
    t2 := time.Date(2024, time.July, 15, 14, 30, 0, 0, est)
    fmt.Println("EST 时区：", t2.Format("2006-01-02 15:04:05 -0700"))

    // 模拟不同地区的时区偏移
    offsets := []struct {
        name   string
        offset int
    }{
        {"UTC+9", 9 * 3600},    // 日本
        {"UTC+5:30", 5*3600 + 30*60}, // 印度
        {"UTC-8", -8 * 3600},   // 太平洋
    }

    for _, o := range offsets {
        loc := time.FixedZone(o.name, o.offset)
        now := time.Now().In(loc)
        fmt.Printf("%s -> %s\n", o.name, now.Format("15:04:05"))
    }
}
```

```
使用固定时区： 2024-07-15 14:30:00 +0800 CST
格式化： 2024-07-15 14:30:00 +0800 CST
EST 时区： 2024-07-15 14:30:00 -0500 EST
UTC+9 -> 23:30:45
UTC+5:30 -> 19:00:45
UTC-8 -> 06:30:45
```

**使用场景：**
- 数据库存储的是"服务器本地时间"，但你知道偏移量
- 解析没有时区名称的时间字符串
- 模拟任意时区进行测试

---

## 8.14 time.In：把时间转换到指定时区

`time.In()` 将一个时间点转换到指定的时区。

```go
func (t Time) In(loc *Location) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 假设这是某个航班从北京起飞的时间
    departure := time.Date(2024, 7, 15, 14, 30, 0, 0, time.UTC)

    // 转换到不同时区显示
    locations := []*time.Location{
        time.UTC,
        mustLoadLocation("Asia/Shanghai"),
        mustLoadLocation("America/New_York"),
        mustLoadLocation("Europe/London"),
    }

    fmt.Println("航班 2024-07-15 14:30 UTC 起飞")
    fmt.Println("各地时间：")
    for _, loc := range locations {
        localTime := departure.In(loc)
        fmt.Printf("  %-20s: %s\n", loc.String(), localTime.Format("2006-01-02 15:04:05 (MST)"))
    }
}

func mustLoadLocation(name string) *time.Location {
    loc, err := time.LoadLocation(name)
    if err != nil {
        panic(err)
    }
    return loc
}
```

```
航班 2024-07-15 14:30 UTC 起飞
各地时间：
  UTC                : 2024-07-15 14:30:00 UTC
  Asia/Shanghai      : 2024-07-15 22:30:00 CST
  America/New_York   : 2024-07-15 10:30:00 EDT
  Europe/London      : 2024-07-15 15:30:00 BST
```

**注意：** `In()` 返回一个新的 `Time`，不会修改原时间！

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Now()
    fmt.Println("原始时间：", t.Format("15:04:05"))

    // In() 不修改原时间
    utc := t.In(time.UTC)
    fmt.Println("UTC时间：", utc.Format("15:04:05"))

    // t 本身没变
    fmt.Println("原时间还是：", t.Format("15:04:05 (MST)"))
}
```

---

## 8.15 time.Local、time.UTC：本地时区和世界标准时间

Go 提供了两个预定义的 `*Location`：

- `time.Local` —— 本地时区（自动检测系统设置）
- `time.UTC` —— 世界标准时间

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now()

    // 本地时间
    fmt.Println("本地时间：", now.In(time.Local).Format("2006-01-02 15:04:05 (MST)"))

    // UTC 时间
    fmt.Println("UTC 时间：", now.In(time.UTC).Format("2006-01-02 15:04:05 (MST)"))

    // 两者对比
    local := now.In(time.Local)
    utc := now.In(time.UTC)
    fmt.Printf("相差：%.2f 小时\n", local.Sub(utc).Hours())

    // 注意：time.Local 是一个全局变量
    fmt.Printf("time.Local 类型：%T\n", time.Local)
    fmt.Printf("time.UTC 类型：%T\n", time.UTC)
}
```

```
本地时间： 2024-07-15 22:30:45 (CST)
UTC 时间： 2024-07-15 14:30:45 (UTC)
相差：8.00 小时
time.Local 类型：*time.Location
time.UTC 类型：*time.Location
```

**警告：** `time.Local` 是一个全局变量，**不要**在 `time.Time` 中长期存储它！

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 错误示例：把 Local 存到结构体中
    type Event struct {
        Time     time.Time
        Timezone *time.Location // 不要这样做！
    }

    // 正确做法：存储 UTC 时间，或者存储时区名称
    type EventFixed struct {
        Time        time.Time // 存储 UTC
        TimezoneName string   // 存储 "Asia/Shanghai"
    }

    e := EventFixed{
        Time:         time.Now().UTC(),
        TimezoneName: "Asia/Shanghai",
    }
    fmt.Printf("事件时间（UTC）：%s\n", e.Time.Format(time.RFC3339))
}
```

---

## 8.16 时间组件提取

从 `time.Time` 中可以提取出各个时间组件：

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 14, 30, 45, 123456789, time.UTC)

    fmt.Println("=== 时间组件提取 ===")
    fmt.Printf("年：%d\n", t.Year())           // 2024
    fmt.Printf("月：%d (%s)\n", t.Month(), t.Month()) // 7 (July)
    fmt.Printf("日：%d\n", t.Day())            // 15
    fmt.Printf("时：%d\n", t.Hour())            // 14
    fmt.Printf("分：%d\n", t.Minute())          // 30
    fmt.Printf("秒：%d\n", t.Second())          // 45
    fmt.Printf("纳秒：%d\n", t.Nanosecond())   // 123456789

    // 日期组件一次性获取
    year, month, day := t.Date()
    fmt.Printf("\n用 Date() 一次性获取：%d年%d月%d日\n", year, month, day)

    // 时分秒一次性获取
    hour, min, sec := t.Clock()
    fmt.Printf("用 Clock() 一次性获取：%d时%d分%d秒\n", hour, min, sec)

    // UTC 偏移量
    _, offset := t.Zone()
    fmt.Printf("\nUTC 偏移：%d 秒 (%d 小时)\n", offset, offset/3600)
}
```

```
=== 时间组件提取 ===
年：2024
月：7 (July)
日：15
时：14
分：30
秒：45
纳秒：123456789

用 Date() 一次性获取：2024年7月15日
用 Clock() 一次性获取：14时30分45秒

UTC 偏移：0 秒 (0 小时)
```

**实用技巧：**

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    now := time.Now()

    // 判断是不是今天
    today := time.Date(now.Year(), now.Month(), now.Day(), 0, 0, 0, 0, now.Location())
    tomorrow := today.Add(24 * time.Hour)
    isToday := now.After(today) && now.Before(tomorrow)
    fmt.Printf("是不是今天：%v\n", isToday)

    // 判断是不是周末
    weekday := now.Weekday()
    isWeekend := weekday == time.Saturday || weekday == time.Sunday
    fmt.Printf("是不是周末：%v (%s)\n", isWeekend, weekday)

    // 判断是不是闰年
    year := now.Year()
    isLeapYear := (year%4 == 0 && year%100 != 0) || (year%400 == 0)
    fmt.Printf("%d 年是不是闰年：%v\n", year, isLeapYear)
}
```

---

## 8.17 Weekday、ISOWeek、YearDay

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 0, 0, 0, 0, time.UTC)

    // Weekday：星期几
    fmt.Println("=== Weekday ===")
    fmt.Printf("今天是：%s\n", t.Weekday())      // Monday
    fmt.Printf("数值：%d (0=周日，6=周六)\n", t.Weekday())

    // 枚举比较
    if t.Weekday() == time.Monday {
        fmt.Println("是周一，新的一周开始了！")
    }

    // ISOWeek：ISO 8601 标准的一年中的第几周
    fmt.Println("\n=== ISOWeek ===")
    year, week := t.ISOWeek()
    fmt.Printf("2024年7月15日是 ISO 第 %d 周\n", week)

    // ISO 周的计算方式：周一是一周的第一天
    // 2024年7月15日是周一，所以是第 29 周的第 1 天
    fmt.Printf("ISO 年：%d，周：%d\n", year, week)

    // YearDay：一年中的第几天
    fmt.Println("\n=== YearDay ===")
    fmt.Printf("7月15日是一年中的第 %d 天\n", t.YearDay())

    // 特殊日期
    dates := []time.Time{
        time.Date(2024, 1, 1, 0, 0, 0, 0, time.UTC),  // 元旦
        time.Date(2024, 12, 31, 0, 0, 0, 0, time.UTC), // 跨年
        time.Date(2024, 2, 29, 0, 0, 0, 0, time.UTC),  // 闰年2月29日
    }

    for _, d := range dates {
        fmt.Printf("%s 是 %s，ISO第%d周，一年第%d天\n",
            d.Format("2006-01-02"),
            d.Weekday(),
            d.ISOWeek().Week,
            d.YearDay())
    }
}
```

```
=== Weekday ===
今天是：Monday
数值：1 (0=周日，6=周六)

=== ISOWeek ===
2024年7月15日是 ISO 第 29 周
ISO 年：2024，周：29

=== YearDay ===
7月15日是一年中的第 197 天

2024-01-01 是 Monday，ISO第1周，一年第1天
2024-12-31 是 Tuesday，ISO第1周，一年第366天
2024-02-29 是 Thursday，ISO第9周，一年第60天
```

**专业词汇解释：**

- **Weekday**：星期几，值域 `time.Sunday` 到 `time.Saturday`
- **ISOWeek**：ISO 8601 标准，规定每周从周一开始，第 1 周是包含 1 月 4 日的那一周
- **YearDay**：一年中的第几天，闰年 1-366，非闰年 1-365

---

## 8.18 time.Add：加 Duration 得到新时间点

```go
func (t Time) Add(d Duration) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 基准时间
    start := time.Date(2024, time.July, 15, 14, 30, 0, 0, time.UTC)
    fmt.Println("基准时间：", start.Format("2006-01-02 15:04:05"))

    // 加上各种时间段
    durations := []time.Duration{
        1 * time.Hour,
        30 * time.Minute,
        90 * time.Second,
        2*time.Hour + 15*time.Minute + 30*time.Second,
        -1 * time.Hour, // 也可以是负的！
    }

    for _, d := range durations {
        result := start.Add(d)
        sign := "+"
        if d < 0 {
            sign = ""
        }
        fmt.Printf("  %s %s = %s\n", start.Format("15:04:05"), sign+d.String(), result.Format("15:04:05"))
    }

    // 实际场景：计算超时时间
    fmt.Println("\n=== 实际场景：订单超时 ===")
    orderTime := time.Now()
    timeout := 30 * time.Minute
    expireTime := orderTime.Add(timeout)
    fmt.Printf("订单时间：%s\n", orderTime.Format("15:04:05"))
    fmt.Printf("30分钟后：%s\n", expireTime.Format("15:04:05"))
    fmt.Printf("还剩：%v\n", time.Until(expireTime))
}
```

```
基准时间： 2024-07-15 14:30:00
  14:30:00 + 1h0m0s = 15:30:00
  14:30:00 + 30m0s = 15:00:00
  14:30:00 + 1m30s = 15:31:30
  14:30:00 + 2h15m30s = 16:45:30
  14:30:00 + -1h0m0s = 13:30:00

=== 实际场景：订单超时 ===
订单时间：22:30:45
30分钟后：23:00:45
还剩：29m59.8s
```

---

## 8.19 time.Sub：两个时间点相减得到 Duration

```go
func (t Time) Sub(u Time) Duration
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t1 := time.Date(2024, time.July, 15, 9, 0, 0, 0, time.UTC)
    t2 := time.Date(2024, time.July, 15, 17, 30, 0, 0, time.UTC)

    // 正常相减
    duration := t2.Sub(t1)
    fmt.Printf("从 %s 到 %s\n", t1.Format("15:04"), t2.Format("15:04"))
    fmt.Printf("相差：%v\n", duration)
    fmt.Printf("转成小时：%.2f 小时\n", duration.Hours())
    fmt.Printf("转成分钟：%.0f 分钟\n", duration.Minutes())

    // 负数情况（t1 在 t2 之后）
    t3 := time.Date(2024, time.July, 15, 20, 0, 0, 0, time.UTC)
    negDuration := t3.Sub(t2)
    fmt.Printf("\n如果反过来（t3 - t2）：%v\n", negDuration)

    // 实际场景：API 响应时间
    fmt.Println("\n=== 实际场景：API 响应时间 ===")
    start := time.Now()
    // 模拟 API 调用
    time.Sleep(150 * time.Millisecond)
    end := time.Now()

    latency := end.Sub(start)
    fmt.Printf("API 延迟：%v\n", latency)
    fmt.Printf("毫秒：%.2f ms\n", float64(latency.Milliseconds()))

    // 格式化输出
    fmt.Printf("格式化：%s\n", latency.String()) // 152.234ms
}
```

```
从 09:00 到 17:30
相差：8h30m0s
转成小时：8.50 小时
转成分钟：510 分钟

如果反过来（t3 - t2）：2h30m0s

=== 实际场景：API 响应时间 ===
API 延迟：150.234ms
毫秒：150.00 ms
格式化：150.234ms
```

---

## 8.20 time.AddDate：加年、月、日，自动处理闰年

```go
func (t Time) AddDate(years, months, days int) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    start := time.Date(2024, time.February, 29, 14, 30, 0, 0, time.UTC)
    fmt.Println("闰年2月29日：", start.Format("2006-01-02"))

    // 加1年，自动处理闰年问题
    oneYearLater := start.AddDate(1, 0, 0)
    fmt.Printf("加1年：%s（2月29日 -> 2月28日，因为2025年不是闰年）\n", oneYearLater.Format("2006-01-02"))

    // 减1年
    oneYearAgo := start.AddDate(-1, 0, 0)
    fmt.Printf("减1年：%s（非闰年，没有2月29日）\n", oneYearAgo.Format("2006-01-02"))

    // 加月份
    fmt.Println("\n=== 月份计算 ===")
    dates := []time.Time{
        time.Date(2024, 1, 31, 0, 0, 0, 0, time.UTC), // 1月31日
        time.Date(2024, 1, 31, 0, 0, 0, 0, time.UTC),
        time.Date(2024, 1, 31, 0, 0, 0, 0, time.UTC),
    }

    for i, d := range dates {
        result := d.AddDate(0, i+1, 0) // 分别加1、2、3个月
        fmt.Printf("1月31日 + %d个月 = %s\n", i+1, result.Format("2006-01-02"))
    }

    // 实用场景：订阅到期日
    fmt.Println("\n=== 实用场景：订阅计算 ===")
    subscribeDate := time.Now()
    durations := []int{1, 3, 6, 12} // 月数

    for _, months := range durations {
        expire := subscribeDate.AddDate(0, months, 0)
        fmt.Printf("订阅 %d 个月，到期日：%s\n", months, expire.Format("2006-01-02"))
    }
}
```

```
闰年2月29日： 2024-02-29
加1年：2025-02-28（2月29日 -> 2月28日，因为2025年不是闰年）
减1年：2023-02-28（非闰年，没有2月29日）

=== 月份计算 ===
1月31日 + 1个月 = 2024-03-01  （没有2月31日）
1月31日 + 2个月 = 2024-04-01  （没有3月31日？等等）
1月31日 + 3个月 = 2024-05-01

=== 实用场景：订阅计算 ===
订阅 1 个月，到期日：2024-08-29
订阅 3 个月，到期日：2024-10-29
订阅 6 个月，到期日：2025-01-29
订阅 12 个月，到期日：2025-07-29
```

**重要规则：**
- `AddDate` 自动处理溢出（如 1月31日 + 1个月 = 3月1日；2月29日 + 1年 = 2月28日，因为目标年份不是闰年）
- 年、月、日是**分别**加上的，不是直接加总天数

---

## 8.21 time.Before、time.After、time.Equal：时间点比较

```go
func (t Time) Before(u Time) bool
func (t Time) After(u Time) bool
func (t Time) Equal(u Time) bool
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t1 := time.Date(2024, time.July, 15, 10, 0, 0, 0, time.UTC)
    t2 := time.Date(2024, time.July, 15, 14, 0, 0, 0, time.UTC)
    t3 := time.Date(2024, time.July, 15, 10, 0, 0, 0, time.UTC) // 和 t1 相同

    // Before
    fmt.Println("=== Before ===")
    fmt.Printf("t1(%s) before t2(%s)? %v\n",
        t1.Format("15:04"), t2.Format("15:04"), t1.Before(t2))

    // After
    fmt.Println("\n=== After ===")
    fmt.Printf("t2(%s) after t1(%s)? %v\n",
        t2.Format("15:04"), t1.Format("15:04"), t2.After(t1))

    // Equal（比较的是时刻，不是字符串）
    fmt.Println("\n=== Equal ===")
    fmt.Printf("t1 == t3? %v\n", t1.Equal(t3))
    fmt.Printf("t1 == t2? %v\n", t1.Equal(t2))

    // 实际场景：检查缓存是否过期
    fmt.Println("\n=== 实际场景：缓存过期检查 ===")
    cacheTime := time.Now().Add(-10 * time.Minute)
    expiry := 30 * time.Minute

    isExpired := time.Now().After(cacheTime.Add(expiry))
    remaining := cacheTime.Add(expiry).Sub(time.Now())

    fmt.Printf("缓存创建时间：%s\n", cacheTime.Format("15:04"))
    fmt.Printf("过期时间：%s\n", cacheTime.Add(expiry).Format("15:04"))
    fmt.Printf("是否已过期：%v\n", isExpired)
    fmt.Printf("剩余时间：%v\n", remaining)
}
```

```
=== Before ===
t1(10:00) before t2(14:00)? true

=== After ===
t2(14:00) after t1(10:00)? true

=== Equal ===
t1 == t3? true
t1 == t2? false

=== 实际场景：缓存过期检查 ===
缓存创建时间：22:20:45
过期时间：22:50:45
是否已过期：false
剩余时间：19m14.8s
```

**注意：**
- `Equal` 比较的是**时刻**是否相同，会自动处理时区
- `t1.Equal(t2)` 等价于 `t1.Sub(t2) == 0`
- **不要用 `==` 比较两个 `time.Time`**，因为它们可能有不同的 Location 或单调时钟

---

## 8.22 time.Truncate：截断到指定精度

`Truncate` 将时间截断到指定的精度，向下取整。

```go
func (t Time) Truncate(d Duration) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 14, 32, 45, 123456789, time.UTC)

    fmt.Println("原始时间：", t.Format("15:04:05.999999999"))

    // 截断到不同精度
    truncations := []time.Duration{
        time.Second,
        time.Minute,
        5 * time.Minute,
        time.Hour,
        6 * time.Hour,
    }

    for _, d := range truncations {
        truncated := t.Truncate(d)
        fmt.Printf("截断到 %-10s -> %s\n", d.String(), truncated.Format("15:04:05"))
    }

    // 实际场景：取整到小时
    fmt.Println("\n=== 实际场景：日志聚合 ===")
    logTime := time.Now()
    hourStart := logTime.Truncate(time.Hour)

    fmt.Printf("日志时间：%s\n", logTime.Format("15:04:05"))
    fmt.Printf("所属小时开始：%s\n", hourStart.Format("15:04:05"))
    fmt.Printf("到这个小时结束还剩：%v\n", hourStart.Add(time.Hour).Sub(logTime))
}
```

```
原始时间： 14:32:45.123456789
截断到 1s         -> 14:32:45.000000000
截断到 1m0s       -> 14:32:00.000000000
截断到 5m0s       -> 14:30:00.000000000
截断到 1h0m0s     -> 14:00:00.000000000
截断到 6h0m0s     -> 12:00:00.000000000

=== 实际场景：日志聚合 ===
日志时间：22:32:45
所属小时开始：22:00:00
到这个小时结束还剩：27m14.8s
```

---

## 8.23 time.Round：四舍五入到指定精度

`Round` 将时间四舍五入到指定的精度。

```go
func (t Time) Round(d Duration) Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    t := time.Date(2024, time.July, 15, 14, 32, 45, 0, time.UTC)

    fmt.Println("原始时间：", t.Format("15:04:05"))

    // 四舍五入到不同精度
    roundings := []time.Duration{
        time.Second,
        time.Minute,
        5 * time.Minute,
        time.Hour,
        6 * time.Hour,
    }

    for _, d := range roundings {
        rounded := t.Round(d)
        fmt.Printf("四舍五入到 %-10s -> %s\n", d.String(), rounded.Format("15:04:05"))
    }

    // Truncate vs Round 对比
    fmt.Println("\n=== Truncate vs Round ===")
    t2 := time.Date(2024, time.July, 15, 14, 32, 45, 0, time.UTC)
    for _, d := range []time.Duration{time.Minute, 5 * time.Minute, time.Hour} {
        fmt.Printf("%-10s: Truncate=%s, Round=%s\n",
            d.String(),
            t2.Truncate(d).Format("15:04"),
            t2.Round(d).Format("15:04"))
    }

    // 实际场景：取整到最接近的15分钟
    fmt.Println("\n=== 实际场景：会议室预定 ===")
    meetingTime := time.Date(2024, time.July, 15, 14, 38, 0, 0, time.UTC)
    roundedMeeting := meetingTime.Round(15 * time.Minute)
    fmt.Printf("原定时间：%s\n", meetingTime.Format("15:04"))
    fmt.Printf("四舍五入到最近的15分钟：%s\n", roundedMeeting.Format("15:04"))
}
```

```
原始时间： 14:32:45

截断到 1s         -> 14:32:45
截断到 1m0s       -> 14:32:00
截断到 5m0s       -> 14:30:00
截断到 1h0m0s     -> 14:00:00
截断到 6h0m0s     -> 12:00:00

=== Truncate vs Round ===
1m0s       : Truncate=14:32, Round=14:33
5m0s       : Truncate=14:30, Round=14:35
1h0m0s     : Truncate=14:00, Round=15:00

=== 实际场景：会议室预定 ===
原定时间：14:38:00
四舍五入到最近的15分钟：14:45:00
```

---

## 8.24 time.Sleep：goroutine 暂停

`time.Sleep()` 让当前 goroutine 暂停指定的时间段。

```go
func Sleep(d Duration)
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("开始睡觉...")
    start := time.Now()

    time.Sleep(2 * time.Second) // 睡2秒

    fmt.Printf("醒了！睡了 %v\n", time.Since(start))

    // 不同单位的睡眠
    fmt.Println("\n=== 不同单位的睡眠 ===")
    sleeps := []time.Duration{
        100 * time.Millisecond,
        500 * time.Millisecond,
        1 * time.Second,
    }

    for _, s := range sleeps {
        start := time.Now()
        time.Sleep(s)
        fmt.Printf("Sleep(%v) 实际睡了 %v\n", s, time.Since(start))
    }
}
```

```
开始睡觉...
醒了！睡了 2.001234s

=== 不同单位的睡眠 ===
Sleep(100ms) 实际睡了 100.123ms
Sleep(500ms) 实际睡了 500.089ms
Sleep(1s) 实际睡了 1.000234s
```

**重要特性：**
- `Sleep` **不消耗 CPU**，goroutine 在睡眠期间被挂起
- 睡眠时间**不保证精确**，可能稍微多一点点
- 可以用 `context.WithTimeout` 来实现**可取消的睡眠**

```go
package main

import (
    "context"
    "fmt"
    "time"
)

func main() {
    // 可取消的睡眠
    ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
    defer cancel()

    fmt.Println("开始可取消的睡眠...")

    select {
    case <-time.After(5 * time.Second):
        fmt.Println("5秒到了（不应该出现）")
    case <-ctx.Done():
        fmt.Printf("被取消了：%v\n", ctx.Err())
    }
}
```

---

## 8.25 time.NewTimer：单次定时器

`time.NewTimer()` 创建一个定时器，指定时间后触发一次。

```go
func NewTimer(d Duration) *Timer
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("创建一个3秒后触发的定时器...")

    // 创建定时器
    timer := time.NewTimer(3 * time.Second)

    // 等待定时器触发
    fmt.Printf("等待中... %s\n", time.Now().Format("15:04:05"))

    // <-timer.C 会阻塞，直到定时器触发
    t := <-timer.C
    fmt.Printf("定时器触发了！%s\n", t.Format("15:04:05"))

    // 定时器触发后，timer.C 会被关闭
}
```

```
创建一个3秒后触发的定时器...
等待中... 22:30:45
定时器触发了！22:30:48
```

**Timer 的结构：**

```go
type Timer struct {
    C <-chan Time  // 触发时发送当前时间
    r runtimeTimer
}
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    timer := time.NewTimer(2 * time.Second)

    go func() {
        t := <-timer.C
        fmt.Printf("定时器在 goroutine 中触发：%s\n", t.Format("15:04:05"))
    }()

    // 主 goroutine 继续做其他事
    fmt.Println("主 goroutine 继续执行...")
    time.Sleep(1 * time.Second)
    fmt.Println("1秒后...")

    // 等待 goroutine 完成
    time.Sleep(2 * time.Second)
}
```

---

## 8.26 time.NewTicker：周期定时器

`time.NewTicker()` 创建一个周期定时器，每隔固定时间触发一次。

```go
func NewTicker(d Duration) *Ticker
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 创建一个每500毫秒触发一次的 ticker
    ticker := time.NewTicker(500 * time.Millisecond)
    defer ticker.Stop() // 记得停止！

    fmt.Println("开始周期定时器，每500ms触发一次")

    count := 0
    for t := range ticker.C {
        count++
        fmt.Printf("[%s] 第 %d 次触发\n", t.Format("15:04:05.000"), count)

        if count >= 5 {
            fmt.Println("够了，停止定时器")
            ticker.Stop()
            break
        }
    }

    fmt.Println("定时器已停止")
}
```

```
开始周期定时器，每500ms触发一次
[22:30:45.123] 第 1 次触发
[22:30:45.623] 第 2 次触发
[22:30:46.123] 第 3 次触发
[22:30:46.623] 第 4 次触发
[22:30:47.123] 第 5 次触发
够了，停止定时器
定时器已停止
```

**Timer vs Ticker：**

| 类型 | 触发次数 | 典型用途 |
|------|----------|----------|
| `Timer` | 单次 | 超时控制、延迟执行 |
| `Ticker` | 无限循环 | 定期检查、心跳 |

---

## 8.27 time.After 的陷阱

`time.After(d)` 返回一个 channel，在 d 时间后发送当前时间。**但每次调用都会创建一个新的定时器！**

```go
func After(d Duration) <-chan Time
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 错误用法：在循环中使用 time.After
    fmt.Println("=== time.After 的陷阱 ===")
    fmt.Println("在循环中反复调用 time.After 会导致内存泄漏！")

    // 模拟错误用法
    for i := 0; i < 3; i++ {
        select {
        case <-time.After(1 * time.Second):
            fmt.Printf("第 %d 次完成\n", i+1)
        }
    }

    // 问题在于：每次循环都创建了一个新的定时器
    // 虽然最终它们会触发并被 GC 回收，但如果循环很快，
    // 会积累大量定时器

    fmt.Println("\n=== 正确做法：用 defer 或 reuse ===")

    // 正确做法1：在循环外创建 Timer
    timer := time.NewTimer(1 * time.Second)
    defer timer.Stop()

    for i := 0; i < 3; i++ {
        timer.Reset(1 * time.Second) // 重置而不是创建新的
        <-timer.C
        fmt.Printf("第 %d 次完成（复用定时器）\n", i+1)
    }

    // 正确做法2：用 Ticker
    fmt.Println("\n=== 正确做法：用 Ticker ===")
    ticker := time.NewTicker(1 * time.Second)
    defer ticker.Stop()

    for i := 0; i < 3; i++ {
        <-ticker.C
        fmt.Printf("第 %d 次完成（用 Ticker）\n", i+1)
    }
}
```

```
=== time.After 的陷阱 ===
第 1 次完成
第 2 次完成
第 3 次完成

=== 正确做法：用 defer 或 reuse ===

第 1 次完成（复用定时器）
第 2 次完成（复用定时器）
第 3 次完成（复用定时器）

=== 正确做法：用 Ticker ===

第 1 次完成（用 Ticker）
第 2 次完成（用 Ticker）
第 3 次完成（用 Ticker）
```

**内存泄漏示例：**

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func badPattern() {
    // 错误：每次都创建新定时器
    for {
        select {
        case <-time.After(1 * time.Hour): // ← 每次循环创建新定时器！
            fmt.Println("不应该执行到这里")
        case <-time.After(1 * time.Second):
            fmt.Println("处理...")
        }
    }
}

func goodPattern() {
    // 正确：复用定时器
    timer := time.NewTimer(1 * time.Hour)
    defer timer.Stop()

    for {
        timer.Reset(1 * time.Hour)
        select {
        case <-timer.C:
            fmt.Println("超时！")
        case <-time.After(1 * time.Second):
            fmt.Println("处理...")
        }
    }
}

func main() {
    var m1, m2 runtime.MemStats

    // 测量不好的模式
    runtime.GC()
    runtime.ReadMemStats(&m1)
    fmt.Printf("初始： Alloc=%d MB\n", m1.Alloc/1024/1024)

    // 注意：在生产环境中使用 badPattern 会导致内存持续增长
    // 这里只是演示
    _ = badPattern
    _ = goodPattern

    runtime.ReadMemStats(&m2)
    fmt.Printf("运行后： Alloc=%d MB\n", m2.Alloc/1024/1024)
}
```

---

## 8.28 Timer/Ticker 的 Stop：停止定时器释放资源

```go
func (t *Timer) Stop() bool
func (t *Ticker) Stop()
```

**Timer.Stop() 返回值：**
- `true`：定时器还没触发就被停止了
- `false`：定时器已经触发过了

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 停止 Timer
    fmt.Println("=== Timer.Stop ===")
    timer := time.NewTimer(5 * time.Second)

    // 模拟一些工作
    time.Sleep(2 * time.Second)

    // 提前停止
    stopped := timer.Stop()
    fmt.Printf("timer.Stop() 返回：%v\n", stopped)

    // 检查 channel 是否还有值
    select {
    case t, ok := <-timer.C:
        fmt.Printf("Channel 状态：%v, 时间=%v\n", ok, t)
    default:
        fmt.Println("Channel 没有值（已被停止）")
    }

    // 停止已经触发的 Timer
    fmt.Println("\n=== 停止已触发的 Timer ===")
    timer2 := time.NewTimer(1 * time.Second)
    time.Sleep(2 * time.Second) // 等它触发
    stopped2 := timer2.Stop()
    fmt.Printf("timer.Stop() 返回：%v（已经触发了）\n", stopped2)

    // 停止 Ticker
    fmt.Println("\n=== Ticker.Stop ===")
    ticker := time.NewTicker(100 * time.Millisecond)
    go func() {
        for range ticker.C {
            fmt.Println("这不应该出现")
        }
    }()

    time.Sleep(350 * time.Millisecond)
    ticker.Stop()
    fmt.Println("Ticker 已停止，不再接收消息")
}
```

```
=== Timer.Stop ===
timer.Stop() 返回：true
Channel 没有值（已被停止）

=== 停止已触发的 Timer ===
timer.Stop() 返回：false（已经触发了）

=== Ticker.Stop ===
Ticker 已停止，不再接收消息
```

**重要原则：**
- 创建 Timer/Ticker 后，**一定要在不再需要时调用 Stop()**
- 可以在 `defer` 中调用，确保函数退出时资源被释放

---

## 8.29 Timer.Reset：重置定时器

`Timer.Reset()` 重新设置定时器的过期时间。

```go
func (t *Timer) Reset(d Duration)
```

**使用场景：** 复用 Timer，避免反复创建新定时器。

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    // 模拟：处理请求，超时控制
    fmt.Println("=== Timer.Reset 用法 ===")

    // 创建超时定时器
    timer := time.NewTimer(5 * time.Second)

    // 模拟处理3个请求
    requests := []int{1, 2, 3}
    for i, req := range requests {
        // 模拟每个请求处理时间
        processTime := time.Duration(2+i) * time.Second

        fmt.Printf("请求 %d：开始处理（预计 %v）...\n", req, processTime)

        // 重置定时器到新的超时时间
        timer.Reset(5 * time.Second)

        // 模拟处理中...
        time.Sleep(processTime)

        // 检查是否超时
        select {
        case <-timer.C:
            fmt.Printf("请求 %d：超时！\n", req)
        default:
            fmt.Printf("请求 %d：处理完成\n", req)
        }
    }

    timer.Stop() // 清理

    // 更常见的场景：心跳检测
    fmt.Println("\n=== 场景：心跳检测 ===")
    heartbeat := time.NewTimer(2 * time.Second)
    defer heartbeat.Stop()

    for i := 0; i < 5; i++ {
        // 模拟收到心跳响应
        if i < 4 {
            fmt.Printf("第 %d 次心跳：收到响应，重置定时器\n", i+1)
            heartbeat.Reset(2 * time.Second)
        }

        select {
        case <-heartbeat.C:
            fmt.Printf("第 %d 次心跳：超时！连接可能断开\n", i+1)
            heartbeat.Reset(2 * time.Second)
        case <-time.After(500 * time.Millisecond):
            // 模拟 500ms 后收到下一个心跳
        }
    }
}
```

```
=== Timer.Reset 用法 ===
请求 1：开始处理（预计 2s）...
请求 1：处理完成
请求 2：开始处理（预计 3s）...
请求 2：处理完成
请求 3：开始处理（预计 4s）...
请求 3：处理完成

=== 场景：心跳检测 ===
第 1 次心跳：收到响应，重置定时器
第 2 次心跳：收到响应，重置定时器
第 3 次心跳：收到响应，重置定时器
第 4 次心跳：收到响应，重置定时器
第 5 次心跳：超时！连接可能断开
```

**Timer.Reset 注意事项：**
1. **只能在 Timer 未触发时调用**（或者触发后手动 drain channel）
2. 如果 Timer 已经触发，`Reset` 前需要先消费掉 `timer.C` 中的值
3. 多 goroutine 环境下需要注意同步

---

## 8.30 Monotonic Clock：防止系统时钟回拨的保护机制

Go 的 `time.Time` 内部包含两个时间：
- **Wall clock（挂钟时间）**：与系统时钟同步，可能回拨或跳跃
- **Monotonic clock（单调时钟）**：只能前进，不会后退

```go
type Time struct {
    // wall: 挂钟时间（秒 + 纳秒）
    // ext:  单调时钟（纳秒，只在内部使用）
    // loc:  时区
}
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("=== Monotonic Clock 演示 ===")

    // time.Since 和 time.Until 使用单调时钟
    start := time.Now()

    // 模拟一些耗时操作
    time.Sleep(100 * time.Millisecond)

    elapsed := time.Since(start)
    fmt.Printf("经过的时间（使用单调时钟）：%v\n", elapsed)

    // 重要：比较两个 Time 是否"相等"时
    t1 := time.Now()
    time.Sleep(10 * time.Millisecond)
    t2 := time.Now()

    // t1 和 t2 的 Wall clock 不同
    fmt.Printf("t1 = %v\n", t1)
    fmt.Printf("t2 = %v\n", t2)
    fmt.Printf("t2.Sub(t1) = %v\n", t2.Sub(t1))

    // 但 Equal 比较的是 Wall clock
    fmt.Printf("t1.Equal(t2) = %v\n", t1.Equal(t2))

    // 注意：Format 方法会丢弃单调时钟信息
    fmt.Printf("t1.Format = %s\n", t1.Format("15:04:05.000000000"))
    fmt.Printf("t2.Format = %s\n", t2.Format("15:04:05.000000000"))
}
```

```
=== Monotonic Clock 演示 ===
经过的时间（使用单调时钟）：100.234ms
t1 = 2024-07-15 22:30:45.123456789 +0800 CST m=+0.000123456
t2 = 2024-07-15 22:30:45.133456789 +0800 CST m=+0.010123456
t2.Sub(t1) = 10ms
t1.Equal(t2) = false
t1.Format = 22:30:45.123456789
t2.Format = 22:30:45.133456789
```

**m=+0.000123456 是什么？**

这就是单调时钟的偏移量。Go 在内部使用它来确保 `time.Since(t)` 的准确性，即使系统时钟回拨。

**为什么需要单调时钟？**

```
系统时间：12:00 → 12:05 → 12:03 (回拨!) → 12:06
真实时间：00:00 → 00:05 → 00:06 → 00:07

如果用系统时钟计算"经过的时间"：
12:00 到 12:06 = 6分钟
但实际上只过了 7 分钟吗？不对！

单调时钟：只能前进，不受系统时钟回拨影响
```

**实际影响：**

- `time.Since()`、`time.Until()`、`time.Sub()` 使用单调时钟
- `Time.Equal()` **不**使用单调时钟，只比较时刻
- `Time.Before()`、`Time.After()` 使用单调时钟
- 序列化（JSON/Marshal）时会**丢失单调时钟**信息

---

## 8.31 time.ParseInLocation：解析时间（指定时区）

`time.ParseInLocation()` 相当于 `time.Parse()` + 指定时区。

```go
func ParseInLocation(layout, value string, loc *Location) (Time, error)
```

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("=== Parse vs ParseInLocation ===")

    // 时间字符串（假设这是北京时间）
    dateStr := "2024-07-15 14:30:00"

    // Parse：假设字符串是 UTC，解析结果也是 UTC
    t1, _ := time.Parse("2006-01-02 15:04:05", dateStr)
    fmt.Printf("Parse 结果：%v（时区=%s）\n", t1, t1.Location())

    // ParseInLocation：指定解析为北京时间
    loc, _ := time.LoadLocation("Asia/Shanghai")
    t2, _ := time.ParseInLocation("2006-01-02 15:04:05", dateStr, loc)
    fmt.Printf("ParseInLocation 结果：%v（时区=%s）\n", t2, t2.Location())

    // 两者的时间值相同，但时区不同
    fmt.Printf("时间值相同？%v\n", t1.Equal(t2))

    // 转换到 UTC 看看
    fmt.Printf("\n转换为 UTC：\n")
    fmt.Printf("  Parse 的 UTC：%s\n", t1.UTC().Format("15:04:05"))
    fmt.Printf("  ParseInLocation 的 UTC：%s\n", t2.UTC().Format("15:04:05"))

    // 实际场景：从 API 解析时间字符串
    fmt.Println("\n=== 实际场景：API 响应解析 ===")

    // 模拟 API 返回的时间（通常是 UTC）
    apiResponse := `{"timestamp": "2024-07-15T14:30:00Z"}`
    fmt.Printf("API 返回：%s\n", apiResponse)

    // 解析为本地时间
    apiTime, _ := time.Parse(time.RFC3339, "2024-07-15T14:30:00Z")
    localTime := apiTime.In(time.Local)

    fmt.Printf("转换为本地时间：%s\n", localTime.Format("2006-01-02 15:04:05 (MST)"))
}
```

```
=== Parse vs ParseInLocation ===
Parse 结果：2024-07-15 14:30:00 +0000 UTC（时区=UTC）
ParseInLocation 结果：2024-07-15 14:30:00 +0800 CST（时区=Asia/Shanghai）
时间值相同？true

转换为 UTC：
  Parse 的 UTC：14:30:00
  ParseInLocation 的 UTC：06:30:00

=== 实际场景：API 响应解析 ===
API 返回：{"timestamp": "2024-07-15T14:30:00Z"}
转换为本地时间：22:30:45 (CST)
```

**重要规则：**
- 如果时间字符串**包含时区信息**（如 `Z`、`+0800`），直接用 `Parse` 即可
- 如果时间字符串**没有时区信息**，用 `ParseInLocation` 明确指定
- 服务器之间的 API 通信，**建议始终使用 UTC**

---

## 8.32 Duration 的单位常量

`time.Duration` 的预定义常量：

| 常量 | 值（纳秒） | 可读形式 |
|------|-----------|---------|
| `time.Nanosecond` | 1 | 1ns |
| `time.Microsecond` | 1000 | 1µs |
| `time.Millisecond` | 1,000,000 | 1ms |
| `time.Second` | 1,000,000,000 | 1s |
| `time.Minute` | 60,000,000,000 | 1m |
| `time.Hour` | 3,600,000,000,000 | 1h |

```go
package main

import (
    "fmt"
    "time"
)

func main() {
    fmt.Println("=== Duration 单位常量 ===")

    // 打印各单位的值
    fmt.Printf("time.Nanosecond  = %d\n", time.Nanosecond)    // 1
    fmt.Printf("time.Microsecond = %d\n", time.Microsecond)  // 1000
    fmt.Printf("time.Millisecond = %d\n", time.Millisecond)  // 1000000
    fmt.Printf("time.Second      = %d\n", time.Second)      // 1000000000
    fmt.Printf("time.Minute      = %d\n", time.Minute)      // 60000000000
    fmt.Printf("time.Hour        = %d\n", time.Hour)        // 3600000000000

    // 组合使用
    dur := 2*time.Hour + 30*time.Minute + 45*time.Second + 500*time.Millisecond
    fmt.Printf("\n组合：%v\n", dur)

    // 转换为不同单位
    fmt.Printf("转纳秒：%d\n", dur.Nanoseconds())
    fmt.Printf("转微秒：%d\n", dur.Microseconds())
    fmt.Printf("转毫秒：%d\n", dur.Milliseconds())
    fmt.Printf("转秒：%.3f\n", dur.Seconds())
    fmt.Printf("转分：%.3f\n", dur.Minutes())
    fmt.Printf("转小时：%.3f\n", dur.Hours())

    // 字符串解析
    durations := []string{
        "1s",
        "2m30s",
        "1h30m",
        "1h30m45s",
        "100ms",
        "1.5h",
    }

    fmt.Println("\n=== ParseDuration ===")
    for _, s := range durations {
        d, err := time.ParseDuration(s)
        if err != nil {
            fmt.Printf("解析 '%s' 失败：%v\n", s, err)
        } else {
            fmt.Printf("'%s' = %v\n", s, d)
        }
    }
}
```

```
=== Duration 单位常量 ===
time.Nanosecond  = 1
time.Microsecond = 1000
time.Millisecond = 1000000
time.Second      = 1000000000
time.Minute      = 600000000000
time.Hour        = 3600000000000

组合：2h30m45.5s

转纳秒：9045500000000
转微秒：9045500000
转毫秒：9045500
转秒：9045.500
转分：150.750
转小时：2.512

=== ParseDuration ===
'1s' = 1s
'2m30s' = 2m30s
'1h30m' = 1h30m
'1h30m45s' = 1h30m45s
'100ms' = 100ms
'1.5h' = 1h30m0s
```

---

## 本章小结

本章我们深入学习了 Go 标准库的 `time` 包，这是日常开发中使用频率最高的包之一。

### 核心概念

| 概念 | 说明 |
|------|------|
| **time.Time** | 时间**点**，不可变，包含年、月、日、时、分、秒、纳秒、时区 |
| **time.Duration** | 时间**段**，以纳秒为单位，可累加 |
| **Time vs Duration** | Time + Duration = Time，Time - Time = Duration |

### 常用操作

**获取和构造时间：**
```go
time.Now()                    // 获取当前时间
time.Date(2024, 7, 15, 14, 30, 0, 0, loc)  // 构造指定时间
time.Unix(1700000000, 0)     // 时间戳转 Time
time.Parse(layout, str)       // 字符串解析
```

**时间组件提取：**
```go
t.Year(), t.Month(), t.Day()           // 年、月、日
t.Hour(), t.Minute(), t.Second()      // 时、分、秒
t.Weekday(), t.YearDay(), t.ISOWeek() // 星期、年内天数、ISO周
```

**时间计算：**
```go
t.Add(d)               // 加时间段
t.Sub(u)               // 两时间相减
t.AddDate(1, 2, 3)     // 加年、月、日
t.Before(u), t.After(u), t.Equal(u)  // 比较
t.Truncate(d), t.Round(d)             // 截断/四舍五入
```

**定时器：**
```go
time.Sleep(d)                  // 休眠
time.NewTimer(d)               // 单次定时器
time.NewTicker(d)               // 周期定时器
timer.Reset(d), timer.Stop()    // 重置/停止
```

### 时区处理

- **time.LoadLocation(name)**：加载标准时区
- **time.FixedZone(name, offset)**：创建固定偏移时区
- **time.In(loc)**：转换时区
- **time.ParseInLocation(layout, value, loc)**：解析时指定时区

### 常见陷阱

1. **time.After 的内存泄漏**：循环中反复调用 `time.After` 会创建大量定时器
2. **Parse 默认 UTC**：字符串解析不会自动使用本地时区
3. **时区偏移量**：夏令时导致同一时区在不同时刻偏移量不同
4. **Monotonic Clock**：`time.Time` 序列化时会丢失单调时钟信息

### 时间格式化口诀

**记住：1-2-3-4-5-6-7**

```
1 = 一个月中的第几天
2 = 月份
3 = 小时
4 = 分钟
5 = 秒
6 = 年份
7 = 时区偏移
```

**常用格式：**
```go
"2006-01-02"                  // 日期
"2006-01-02 15:04:05"         // 日期时间
time.RFC3339                  // ISO 8601 标准
time.RFC3339Nano              // 带纳秒
```

---

> "和时间打交道，耐心比代码更重要。"
> —— Go 语言之父 Rob Pike（大概说过）

