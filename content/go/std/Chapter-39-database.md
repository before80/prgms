+++
title = "第39章：数据库访问——database/sql"
weight = 390
date = "2026-03-30T13:43:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第39章：数据库访问——database/sql

> "程序员的三大难题：缓存失效、命名、再加一个分布式事务——等等，我忘了我还在学怎么查数据库。" ——某位不愿透露姓名的Gopher

在还没学数据库之前，你的数据可能是这样存储的：

```go
var users = []string{"Alice", "Bob"} // 内存里的数组，关机就没了
```

或者这样：

```go
// 写入到文件
os.WriteFile("data.txt", []byte("Alice\nBob\n"), 0644)
```

这些方案在数据量小、并发低的时候勉强能用。但一旦你的程序需要：

- 存储成千上万条数据
- 多人同时访问
- 根据条件快速查找
- 数据要持久化（程序重启后还在）

你就需要数据库了。而Go语言的标准库 `database/sql` 就是你与数据库之间的"翻译官"。

## 39.1 database/sql包解决什么问题

`database/sql` 是Go语言标准库提供的一个数据库抽象层。它不直接操作数据库，而是提供了一套统一的接口，让你可以用相同的方式访问不同的数据库。

**专业词汇解释：**

- **数据库（Database）**：按照数据结构来组织、存储和管理数据的仓库。常见的数据库有MySQL、PostgreSQL、SQLite等。
- **SQL（Structured Query Language）**：结构化查询语言，用于操作数据库的标准语言。你可以把它理解为"数据库的普通话"。
- **DBMS（Database Management System）**：数据库管理系统，如MySQL、PostgreSQL就是不同的DBMS。

打个比方：`database/sql` 就像是手机的充电接口（USB-C），而MySQL、PostgreSQL等就像是不同的电源插座。不管你用的是哪种插座（数据库），只要插上转接头（驱动），就能用同一根线（`database/sql` API）给手机充电（操作数据）。

**核心功能：**

- 连接管理（创建、复用、关闭连接）
- 执行SQL语句（查询、插入、更新、删除）
- 事务支持（开启、提交、回滚）
- 连接池管理（自动复用连接，提高性能）

## 39.2 database/sql核心原理

`database/sql` 的核心原理可以用两个词概括：**连接池** + **统一接口**。

```
┌─────────────────────────────────────────────────────────────┐
│                        Go 程序                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              database/sql (统一接口)                   │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐          │   │
│  │  │ Conn 1   │  │ Conn 2   │  │ Conn 3   │  ...     │   │
│  │  └──────────┘  └──────────┘  └──────────┘          │   │
│  └─────────────────────────────────────────────────────┘   │
│                          ↕ 连接池                            │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              驱动程序 (匿名导入注册)                   │   │
│  │  mysql / postgres / sqlite3 / ...                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**驱动注册原理：**

```mermaid
graph TD
    A[import _ "github.com/go-sql-driver/mysql"] --> B[驱动包 init 函数执行]
    B --> C[调用 sql.Register 注册自己]
    C --> D[存入全局 map[string]Driver]
    E[sql.Open] --> F[根据驱动名查找驱动]
    F --> G[创建连接]
```

**专业词汇解释：**

- **连接池（Connection Pool）**：预先创建一定数量的数据库连接，放到一个"池子"里。当程序需要操作数据库时，从池子里取一个连接用，用完再放回去，而不是每次都新建连接。这就像租车公司提前准备好车辆，租客来了直接给钥匙，租完还回来，而不是每次都现造一辆车。
- **匿名导入（Anonymous Import）**：使用 `_` 作为别名的导入方式，只执行包的 `init()` 函数，不直接使用包中的符号。
- **统一接口**：无论底层是MySQL还是PostgreSQL，你的代码写法都一样。底层差异由驱动来屏蔽。

## 39.3 驱动的注册与加载

在Go中使用数据库，第一步通常是导入数据库驱动：

```go
import (
    "database/sql"
    _ "github.com/go-sql-driver/mysql"  // 匿名导入，注册MySQL驱动
)
```

**专业词汇解释：**

- **驱动（Driver）**：实现 `database/sql/driver` 接口的包，每个数据库有自己的驱动。MySQL的驱动是 `github.com/go-sql-driver/mysql`，PostgreSQL的驱动是 `github.com/lib/pq`。
- **匿名导入**：用 `_` 导入，只执行包的 `init()` 函数。通常用于注册驱动或导入有副作用的包。
- **init() 函数**：包初始化函数，在包被导入时自动执行。

**为什么用匿名导入？**

因为驱动包只负责"注册自己"，注册完成后你的代码并不需要直接引用它。就像你去酒店办理入住，前台小姐（驱动）帮你登记（注册），之后你直接和酒店系统打交道，不需要再找前台小姐。

```go
package main

import (
    "database/sql"
    "fmt"
    // 匿名导入执行驱动注册
    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // 此时mysql驱动已经注册，可以使用了
    db, err := sql.Open("mysql", "user:password@tcp(localhost:3306)/testdb")
    if err != nil {
        fmt.Println("打开数据库失败:", err)
        return
    }
    defer db.Close()
    fmt.Println("数据库连接已创建（实际连接可能尚未建立）")
}
```

## 39.4 sql.Open：创建数据库连接，不立刻建立连接

`sql.Open` 是创建数据库连接的入口，但它有点"懒"，不会立刻建立真正的网络连接。

```go
func main() {
    // DSN: Data Source Name，数据库连接字符串
    dsn := "user:password@tcp(localhost:3306)/testdb?charset=utf8mb4"
    
    // sql.Open 返回 *DB 对象，此时并没有真正连接数据库
    db, err := sql.Open("mysql", dsn)
    if err != nil {
        fmt.Println("打开数据库失败:", err)
        return
    }
    defer db.Close()
    
    fmt.Println("DB对象已创建，实际网络连接尚未建立")
    fmt.Println("真正的连接会在第一次执行Query/Exec时建立")
}
```

**专业词汇解释：**

- **DSN（Data Source Name）**：数据源名称，就是数据库的连接字符串，包含了用户名、密码、主机、端口、数据库名等信息。不同数据库的DSN格式可能不同。
- **懒连接（Lazy Connection）**：`sql.Open` 只是创建了一个 `*DB` 对象和配置，实际的TCP连接是在第一次执行SQL时才建立的。这是一种"按需连接"的策略。

**为什么设计成这样？**

想象你开了一家餐厅，`sql.Open` 就相当于你拿到了餐厅的会员卡（有了进入的资格），但你还没真正走进餐厅坐下。只有当你点菜（执行Query/Exec）时，服务员才会带你入座（建立真实连接）。

```go
// 常见的DSN格式
// MySQL: "user:password@tcp(localhost:3306)/dbname?charset=utf8mb4"
// PostgreSQL: "host=localhost port=5432 user=postgres password=secret dbname=test"
// SQLite: "test.db"  // 文件路径即可
```

## 39.5 DB.Ping：检查连接是否有效

`DB.Ping` 用来检查数据库连接是否有效。如果连接已经断开，它会尝试重连。

```go
func main() {
    dsn := "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4"
    db, err := sql.Open("mysql", dsn)
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // Ping 检查连接是否可用
    if err := db.Ping(); err != nil {
        fmt.Println("数据库连接失败:", err)
        return
    }
    fmt.Println("数据库连接正常！")
}
```

**专业词汇解释：**

- **Ping**：原本是网络术语（发送ICMP回显请求），在这里比喻为"戳一下看对方有没有回应"。数据库的Ping就是向数据库服务器发送一个小请求，看它能不能正常响应。
- **连接健康检查**：在生产环境中，定期Ping可以及时发现断开的连接，避免在执行重要操作时才发现问题。

**使用场景：**

- 应用启动时检查数据库是否可用
- 定期检查连接是否存活
- 在执行重要操作前确认连接状态

```go
// 实际项目中可以这样用
func checkDB(db *sql.DB) error {
    if err := db.Ping(); err != nil {
        // 记录日志并告警
        return fmt.Errorf("数据库连接异常: %w", err)
    }
    return nil
}
```

## 39.6 DB.SetMaxOpenConns：最大并发连接数

`SetMaxOpenConns` 设置最大打开（正在使用）的连接数。如果设置为0（默认），表示不限制。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 设置最大打开连接数为10
    // 超过10个并发请求时，第11个会等待前面的释放连接
    db.SetMaxOpenConns(10)
    
    fmt.Println("最大并发连接数已设置为10")
}
```

**专业词汇解释：**

- **最大打开连接数**：同一时刻最多有多少个连接正在被使用。如果设置为10，意味着同一时刻最多只有10个并发数据库操作。
- **连接限制的原因**：数据库服务器本身有连接数上限，设置过大会导致数据库拒绝连接。另外，连接数太多也会消耗系统资源。

**为什么要限制？**

这就像你去游乐园的热门项目，如果不限流，大家一起冲进去可能会发生踩踏事故。限制最大连接数就是为了"防止踩踏"，保护数据库服务器不被突如其来的大量请求冲垮。

## 39.7 DB.SetMaxIdleConns：最大空闲连接数

`SetMaxIdleConns` 设置连接池中最大空闲连接数。空闲连接是已经建立但当前没有使用的连接。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 设置最大空闲连接数为5
    // 当连接用完归还后，池子里最多保留5个空闲连接
    db.SetMaxIdleConns(5)
    
    // 设置空闲连接的最大存活时间（后面会讲）
    db.SetConnMaxLifetime(5 * time.Minute)
}
```

**专业词汇解释：**

- **空闲连接（Idle Connection）**：已经和数据库建立连接，但当前没有执行任何SQL操作的连接。它们在连接池里"待命"，等待下次被使用。
- **连接复用**：复用空闲连接比每次都新建连接要快得多，因为省去了建立TCP连接和数据库认证的时间。

**调优建议：**

- 如果你的应用并发量很高，空闲连接数应该设置得大一些（比如和最大并发连接数相同）
- 如果你的应用并发量很低，可以设置小一些，节省数据库资源
- 如果设置为0，则不保留任何空闲连接，每次用完都关闭
- 如果设置为-1，则不限制空闲连接数（不推荐）

## 39.8 DB.SetConnMaxLifetime：连接最大生命周期

`SetConnMaxLifetime` 设置连接的最大存活时间。超过这个时间的连接会被关闭。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 设置连接最大存活时间为1小时
    // 任何连接存活超过1小时后都会被关闭
    db.SetConnMaxLifetime(1 * time.Hour)
    
    fmt.Println("连接最大生命周期设置为1小时")
}
```

**专业词汇解释：**

- **连接生命周期（Connection Lifetime）**：连接从创建到被关闭的整个存活时间。
- **为什么需要过期机制**：数据库服务器为了节省资源，会在一段时间后自动关闭空闲连接。如果客户端还把这些连接当作有效的，就会出问题。设置合理的生命周期可以避免这个问题。

**一个常见的坑：**

```go
// 错误示例：设置了MaxLifetime但没有设置MaxIdleConns
db.SetConnMaxLifetime(5 * time.Minute)
// 如果MaxIdleConns是默认值2，创建5分钟后这两个连接会过期
// 下次请求时会创建新连接，导致连接数翻倍
```

**调优建议：**

- 建议设置为比数据库服务端的"空闲超时时间"短一些，确保客户端先于服务端关闭连接
- MySQL的默认空闲超时是 `wait_timeout`，通常8小时，可以据此设置客户端的MaxLifetime

## 39.9 连接池耗尽：所有连接都在使用中，新请求会等待

当所有连接都被占用，新的请求会等待。这是连接池的核心机制之一。

```
┌─────────────────────────────────────────────────────────────┐
│                      连接池耗尽示意图                          │
│                                                             │
│  请求1 ──▶ [连接A] 正在使用                                   │
│  请求2 ──▶ [连接B] 正在使用                                   │
│  请求3 ──▶ [连接C] 正在使用                                   │
│  请求4 ──▶ [连接D] 正在使用 ──▶ 等待...                        │
│  请求5 ──▶ [连接E] 正在使用 ──▶ 等待...                        │
│              ↑                                              │
│         最大10个连接                                          │
└─────────────────────────────────────────────────────────────┘
```

**代码模拟连接池耗尽：**

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 设置最大连接数为2，用于演示
    db.SetMaxOpenConns(2)
    db.SetMaxIdleConns(2)
    
    // 模拟3个请求
    var wg sync.WaitGroup
    for i := 1; i <= 3; i++ {
        wg.Add(1)
        go func(id int) {
            defer wg.Done()
            start := time.Now()
            
            // 从连接池获取连接（最多等30秒）
            ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
            defer cancel()
            
            // 假设执行一个耗时查询
            rows, err := db.QueryContext(ctx, "SELECT SLEEP(3)")
            if err != nil {
                fmt.Printf("请求%d: 获取连接失败: %v\n", id, err)
                return
            }
            rows.Close()
            
            fmt.Printf("请求%d: 耗时 %v\n", id, time.Since(start))
        }(i)
    }
    
    wg.Wait()
    fmt.Println("所有请求完成")
}
```

**专业词汇解释：**

- **连接池耗尽**：所有连接都在使用中，新的请求必须等待。这是正常现象，说明你的应用并发量较高。
- **连接等待**：等待时间过长会导致请求超时，需要合理设置超时时间。
- **死锁（Deadlock）**：虽然不是连接池耗尽直接导致的，但如果多个事务互相等待对方的锁，就会形成死锁，导致连接被长期占用。

**如何处理连接池耗尽：**

1. **增加最大连接数**（如果数据库允许）
2. **优化SQL查询**，减少每个操作占用连接的时间
3. **使用缓存**，减少数据库访问次数
4. **设置合理的超时时间**，避免无限等待

```go
// 给每个数据库操作设置超时
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

rows, err := db.QueryContext(ctx, "SELECT * FROM users WHERE id = ?", userID)
```

## 39.10 DB.Query：查询多行，返回 *Rows

`DB.Query` 用于执行查询语句，返回多行结果。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // Query 执行查询，返回 *Rows
    rows, err := db.Query("SELECT id, name, age FROM users WHERE age > ?", 18)
    if err != nil {
        panic(err)
    }
    defer rows.Close()  // 重要：关闭rows释放连接
    
    // 遍历结果
    for rows.Next() {
        var id int
        var name string
        var age int
        
        // Scan 将当前行的数据扫描到变量中
        if err := rows.Scan(&id, &name, &age); err != nil {
            panic(err)
        }
        fmt.Printf("用户: ID=%d, 姓名=%s, 年龄=%d\n", id, name, age)
    }
    
    // 检查遍历是否有错误
    if err := rows.Err(); err != nil {
        panic(err)
    }
}
```

**专业词汇解释：**

- **Query**：查询方法，用于执行SELECT语句，返回多行数据。
- **\*Rows**：游标对象，代表一个查询结果集。通过遍历Rows获取每一行数据。
- **游标（Cursor）**：可以理解为"结果的当前位置指针"，初始指向第一行之前，每调用一次Next()向下移动一行。

**Query的执行流程：**

```
1. db.Query()        → 从连接池获取连接，发起查询
2. 返回 *Rows        → 结果集游标，初始位置在第一行之前
3. rows.Next()       → 移动到下一行，返回true表示有数据
4. rows.Scan()       → 读取当前行数据到变量
5. rows.Close()      → 关闭游标，释放连接回连接池
```

## 39.11 DB.QueryRow：查询单行，返回 *Row

`DB.QueryRow` 用于查询最多一行数据，比Query更轻量。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // QueryRow 查询单行，返回 *Row
    var name string
    var age int
    
    // 查询ID为1的用户
    err := db.QueryRow("SELECT name, age FROM users WHERE id = ?", 1).Scan(&name, &age)
    if err != nil {
        if err == sql.ErrNoRows {
            fmt.Println("没找到这个用户")
        } else {
            panic(err)
        }
        return
    }
    
    fmt.Printf("查到的用户: 姓名=%s, 年龄=%d\n", name, age)
}
```

**专业词汇解释：**

- **QueryRow**：专门用于查询最多一行的场景，比Query更简洁，不需要手动遍历。
- **\*Row**：`QueryRow` 的返回值类型，它只有一个方法 `Scan()`。
- **自动关闭**：`*Row` 不需要手动关闭，底层会自动处理。

**QueryRow vs Query：**

| 特性 | QueryRow | Query |
|------|----------|-------|
| 返回类型 | *Row | *Rows |
| 遍历 | 不需要 | 需要 Next() 遍历 |
| 关闭 | 自动关闭 | 必须手动 Close() |
| 多行 | 只返回第一行 | 返回所有行 |
| 空结果 | 返回 sql.ErrNoRows | 遍历0次 |

## 39.12 Rows.Scan：扫描结果到变量，按列顺序对应

`Rows.Scan` 将当前行的数据按列顺序扫描到变量中。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    rows, err := db.Query("SELECT id, name, email, created_at FROM users LIMIT 1")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    
    if rows.Next() {
        var (
            id        int
            name      string
            email     sql.NullString  // 允许NULL的字段
            createdAt time.Time
        )
        
        // Scan 按列顺序将数据扫描到变量
        // 顺序必须和SELECT的列顺序一致！
        err := rows.Scan(&id, &name, &email, &createdAt)
        if err != nil {
            panic(err)
        }
        
        fmt.Printf("ID: %d\n", id)
        fmt.Printf("姓名: %s\n", name)
        fmt.Printf("邮箱: %v (Valid=%v)\n", email.String, email.Valid)
        fmt.Printf("创建时间: %v\n", createdAt)
    }
}
```

**专业词汇解释：**

- **Scan**：将游标当前位置的行数据复制到变量中。
- **按顺序对应**：Scan的变量顺序必须和SELECT语句中的列顺序一致，而不是列名。
- **类型匹配**：变量的类型必须和数据库列类型匹配，比如整数字段用int或int64，字符串用string，时间用time.Time。

**类型对应表：**

| 数据库类型 | Go类型 |
|-----------|--------|
| INT | int, int32, int64 |
| BIGINT | int64 |
| VARCHAR, TEXT | string |
| DATETIME, TIMESTAMP | time.Time |
| FLOAT, DOUBLE | float32, float64 |
| DECIMAL | github.com/shopspring/decimal.Decimal |
| NULL值 | sql.NullString, sql.NullInt64等 |

## 39.13 Rows.Next：移动到下一行

`Rows.Next` 将游标移动到下一行，返回是否有更多数据。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    rows, err := db.Query("SELECT id, name FROM users LIMIT 5")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    
    // Next 返回true表示有下一行数据
    // 返回false表示已经遍历完所有行
    for rowNum := 1; rows.Next(); rowNum++ {
        var id int
        var name string
        
        if err := rows.Scan(&id, &name); err != nil {
            panic(err)
        }
        fmt.Printf("第%d行: ID=%d, 姓名=%s\n", rowNum, id, name)
    }
    
    // 重要：检查遍历过程中是否有错误
    if err := rows.Err(); err != nil {
        panic(err)
    }
}
```

**专业词汇解释：**

- **Next**：移动游标到下一行。如果返回true，说明成功移动到一行，可以调用Scan；如果返回false，说明已经没有更多行了。
- **遍历结束**：可能是因为没有数据，也可能是查询出错了。调用 `rows.Err()` 可以确认。

**常见错误：**

```go
// 错误示例：没有检查Next的返回值
rows, _ := db.Query("SELECT id FROM users")
for {
    var id int
    rows.Scan(&id)  // 可能扫描到空行或出错
    fmt.Println(id)
    if !rows.Next() {
        break
    }
}

// 正确写法：for循环直接使用Next作为条件
rows, _ := db.Query("SELECT id FROM users")
for rows.Next() {
    var id int
    rows.Scan(&id)
    fmt.Println(id)
}
```

## 39.14 Rows.Close：关闭游标

`Rows.Close` 关闭游标，释放占用的连接回连接池。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    rows, err := db.Query("SELECT name FROM users")
    if err != nil {
        panic(err)
    }
    
    // defer rows.Close() 是最佳实践
    // 确保无论函数怎么退出，连接都会被释放
    defer rows.Close()
    
    for rows.Next() {
        var name string
        rows.Scan(&name)
        fmt.Println(name)
    }
}
```

**专业词汇解释：**

- **关闭游标**：关闭游标意味着"我不需要这个结果集了"，底层会将连接释放回连接池，供其他请求使用。
- **为什么要关闭**：如果忘记关闭，而连接池已经满了，新的查询会一直等待，导致程序卡死。

**不关闭的后果：**

```go
// 这段代码有内存泄漏风险
func badQuery() {
    db, _ := sql.Open("mysql", "dsn")
    
    for {
        rows, _ := db.Query("SELECT ...")  // 不关闭
        // 处理rows...
        // 连接永远不会被释放！
    }
}
```

**最佳实践：**

```go
rows, err := db.Query("SELECT ...")
if err != nil {
    return err
}
defer rows.Close()  // defer是Go的"保险"机制

// 使用rows...
```

## 39.15 sql.ErrNoRows：QueryRow 没查到记录的错误

当 `QueryRow` 查询不到任何记录时，会返回 `sql.ErrNoRows` 错误。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    var name string
    // 查询一个不存在的用户
    err := db.QueryRow("SELECT name FROM users WHERE id = ?", 99999).Scan(&name)
    
    if err != nil {
        if err == sql.ErrNoRows {
            // QueryRow 没查到任何记录
            fmt.Println("用户不存在（没有找到匹配的记录）")
        } else {
            // 其他错误（数据库连接失败等）
            fmt.Println("查询出错:", err)
        }
        return
    }
    
    fmt.Println("查到的用户:", name)
}
```

**专业词汇解释：**

- **sql.ErrNoRows**：Go标准库定义的错误变量，表示"没有找到任何行"。这是 `QueryRow` 特有的，因为QueryRow只关心一行，没有查到就是异常情况。
- **为什么Query需要特殊处理**：Query返回多个结果，即使没有行也只是"空结果集"，不算错误。但QueryRow只查一行，没有结果就是"查了个寂寞"。

**最佳实践：**

```go
func getUserName(db *sql.DB, id int) (string, error) {
    var name string
    err := db.QueryRow("SELECT name FROM users WHERE id = ?", id).Scan(&name)
    
    if err != nil {
        if err == sql.ErrNoRows {
            return "", fmt.Errorf("用户%d不存在", id)
        }
        return "", fmt.Errorf("查询用户%d失败: %w", id, err)
    }
    
    return name, nil
}
```

## 39.16 DB.Exec：执行 SQL，INSERT、UPDATE、DELETE

`DB.Exec` 用于执行不需要返回结果集的SQL语句，如INSERT、UPDATE、DELETE。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 执行INSERT
    result, err := db.Exec(
        "INSERT INTO users (name, age, email) VALUES (?, ?, ?)",
        "张三", 25, "zhangsan@example.com",
    )
    if err != nil {
        panic(err)
    }
    
    // 获取插入的ID和影响行数（后面会详细讲）
    id, _ := result.LastInsertId()
    fmt.Printf("插入成功，ID=%d\n", id)
    
    // 执行UPDATE
    affected, _ := result.RowsAffected()
    fmt.Printf("受影响行数=%d\n", affected)
    
    // 执行UPDATE
    result, err = db.Exec(
        "UPDATE users SET age = ? WHERE name = ?",
        26, "张三",
    )
    if err != nil {
        panic(err)
    }
    rowsAffected, _ := result.RowsAffected()
    fmt.Printf("更新了%d行\n", rowsAffected)
    
    // 执行DELETE
    result, err = db.Exec("DELETE FROM users WHERE name = ?", "张三")
    if err != nil {
        panic(err)
    }
    rowsAffected, _ = result.RowsAffected()
    fmt.Printf("删除了%d行\n", rowsAffected)
}
```

**专业词汇解释：**

- **Exec**：Execute的缩写，用于执行INSERT、UPDATE、DELETE等不返回结果集的SQL语句。
- **INSERT**：插入语句，向表中添加新记录。
- **UPDATE**：更新语句，修改已存在的记录。
- **DELETE**：删除语句，删除记录。

**Query vs Exec：**

| 方法 | 用途 | 返回值 |
|------|------|--------|
| Query | SELECT查询 | *Rows（多行） |
| QueryRow | SELECT查询 | *Row（单行） |
| Exec | INSERT/UPDATE/DELETE | Result |

## 39.17 Result.LastInsertId、Result.RowsAffected：获取插入 ID 或影响行数

`Exec` 返回一个 `Result` 对象，可以通过它获取插入的ID或影响的行数。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 先创建一个测试表
    db.Exec("CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))")
    
    // INSERT - 获取自增ID
    result, err := db.Exec("INSERT INTO products (name) VALUES (?)", "手机")
    if err != nil {
        panic(err)
    }
    
    // LastInsertId 返回插入的自增ID
    // 注意：只有自增ID的INSERT才能获取到
    id, err := result.LastInsertId()
    if err != nil {
        panic(err)
    }
    fmt.Printf("插入的产品ID: %d\n", id)
    
    // UPDATE/DELETE - 获取影响行数
    result, err = db.Exec("UPDATE products SET name = ? WHERE id = ?", "智能手机", id)
    if err != nil {
        panic(err)
    }
    
    // RowsAffected 返回受影响的行数
    affected, err := result.RowsAffected()
    if err != nil {
        panic(err)
    }
    fmt.Printf("更新了%d行\n", affected)
    
    // 再次更新（内容没变）
    result, err = db.Exec("UPDATE products SET name = ? WHERE id = ?", "智能手机", id)
    affected, _ = result.RowsAffected()
    fmt.Printf("再次更新（无变化），受影响行数: %d\n", affected)  // 仍然是1，因为WHERE条件仍匹配
    
    // 清理测试表
    db.Exec("DROP TABLE products")
}
```

**专业词汇解释：**

- **LastInsertId**：插入操作返回的自增ID。用于获取AUTO_INCREMENT字段的值。
- **RowsAffected**：受影响的行数。UPDATE和DELETE语句返回匹配并被修改/删除的行数。
- **AUTO_INCREMENT**：MySQL的自增主键机制，插入记录时不需要指定ID，数据库会自动递增。

**注意事项：**

```go
// LastInsertId 可能返回0或错误，如果：
// 1. 插入的表没有自增主键
// 2. 使用的是批量插入（只有第一个ID会被返回）
// 3. 驱动不支持该功能

// RowsAffected 可能和预期不符，如果：
// 1. UPDATE的WHERE条件没有匹配到任何行（返回0）
// 2. UPDATE前后值一样（MySQL可能返回0，因为没有实际修改）
```

## 39.18 DB.Prepare：预编译语句，一次编译多次执行

`Prepare` 创建预编译语句，适合执行多次相同结构的SQL。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 创建预编译语句
    // ? 是占位符，会在执行时替换
    stmt, err := db.Prepare("INSERT INTO users (name, age) VALUES (?, ?)")
    if err != nil {
        panic(err)
    }
    defer stmt.Close()  // 记得关闭预编译语句
    
    // 多次执行同一语句，每次传入不同的参数
    users := [][2]interface{}{
        {"Alice", 20},
        {"Bob", 25},
        {"Charlie", 30},
    }
    
    for _, user := range users {
        result, err := stmt.Exec(user[0], user[1])
        if err != nil {
            panic(err)
        }
        id, _ := result.LastInsertId()
        fmt.Printf("插入用户 %s，ID=%d\n", user[0], id)
    }
    
    // 清理
    db.Exec("DELETE FROM users WHERE name IN (?, ?, ?)", "Alice", "Bob", "Charlie")
}
```

**专业词汇解释：**

- **预编译语句（Prepared Statement）**：先编译SQL语句的结构，再传入参数执行。数据库服务器只需编译一次，之后每次传入不同参数即可执行。
- **占位符（Placeholder）**：SQL中的 `?` 或 `$1` 等，用于表示将来会填入的值。
- **性能优势**：预编译语句避免了每次执行时重新解析SQL字符串，适合执行多次相同结构的SQL。

**预编译的优势：**

```
普通SQL执行过程：
  解析SQL字符串 → 编译执行计划 → 执行 → 返回结果
  解析SQL字符串 → 编译执行计划 → 执行 → 返回结果  (重复)
  
预编译SQL执行过程：
  [预编译] 解析SQL字符串 → 编译执行计划 → 保存编译结果
  [执行1] 传入参数 → 使用已编译计划 → 返回结果
  [执行2] 传入参数 → 使用已编译计划 → 返回结果  (复用)
  [执行3] 传入参数 → 使用已编译计划 → 返回结果
```

**安全性：**

预编译语句还能防止SQL注入攻击，因为参数是分开传输的，攻击者无法通过参数篡改SQL结构。

## 39.19 DB.Begin、DB.BeginTx：开启事务

事务是一组原子性的SQL操作，要么全部成功，要么全部失败。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 开启事务
    tx, err := db.Begin()
    if err != nil {
        panic(err)
    }
    
    // 在事务中执行操作
    _, err = tx.Exec("INSERT INTO accounts (name, balance) VALUES (?, ?)", "张三", 1000)
    if err != nil {
        // 出错了，回滚事务
        tx.Rollback()
        panic(err)
    }
    
    _, err = tx.Exec("INSERT INTO accounts (name, balance) VALUES (?, ?)", "李四", 500)
    if err != nil {
        tx.Rollback()
        panic(err)
    }
    
    // 所有操作成功，提交事务
    err = tx.Commit()
    if err != nil {
        panic(err)
    }
    
    fmt.Println("事务提交成功！")
}
```

**专业词汇解释：**

- **事务（Transaction）**：一组原子性的数据库操作集合。事务内的所有操作要么全部成功，要么全部失败回滚。
- **Begin**：开始一个事务，返回 `*Tx` 对象。
- **BeginTx**：`Begin` 的增强版，支持设置事务选项（如隔离级别）。

```go
// BeginTx 支持更多选项
tx, err := db.BeginTx(
    context.Background(),
    &sql.TxOptions{
        Isolation: sql.LevelRepeatableRead,  // 设置隔离级别
        ReadOnly: false,                     // 是否只读
    },
)
```

**事务的ACID特性：**

- **Atomicity（原子性）**：事务是最小执行单位，不可分割
- **Consistency（一致性）**：事务执行前后，数据库状态保持一致
- **Isolation（隔离性）**：并发执行的事务互相隔离，不互相干扰
- **Durability（持久性）**：事务提交后，结果永久保存

## 39.20 Tx.Commit、Tx.Rollback：提交或回滚事务

`Commit` 提交事务，使所有操作永久生效；`Rollback` 回滚事务，撤销所有操作。

```go
func transferMoney(db *sql.DB, from string, to string, amount float64) error {
    // 开启事务
    tx, err := db.Begin()
    if err != nil {
        return fmt.Errorf("开启事务失败: %w", err)
    }
    
    // 标记一个退出点，任何错误都会触发回滚
    var success bool
    defer func() {
        if !success {
            tx.Rollback()  // 即使.Commit()失败，Rollback()也是安全的
        }
    }()
    
    // 扣钱
    result, err := tx.Exec("UPDATE accounts SET balance = balance - ? WHERE name = ?", amount, from)
    if err != nil {
        return fmt.Errorf("扣款失败: %w", err)
    }
    if affected, _ := result.RowsAffected(); affected == 0 {
        return fmt.Errorf("付款账户不存在或余额不足")
    }
    
    // 加钱
    _, err = tx.Exec("UPDATE accounts SET balance = balance + ? WHERE name = ?", amount, to)
    if err != nil {
        return fmt.Errorf("收款失败: %w", err)
    }
    
    // 提交事务
    if err := tx.Commit(); err != nil {
        return fmt.Errorf("提交事务失败: %w", err)
    }
    
    success = true  // 标记事务成功
    return nil
}
```

**专业词汇解释：**

- **Commit**：提交事务，将所有操作永久写入数据库。
- **Rollback**：回滚事务，撤销所有未提交的操作。
- **保存点（Savepoint）**：可以在事务中设置保存点，支持部分回滚。

**为什么要defer Rollback？**

```go
// 常见陷阱：忘记回滚
func badExample() {
    tx, _ := db.Begin()
    // ... 执行操作 ...
    if someError {
        tx.Rollback()  // 这里return了就不会Commit
        return
    }
    tx.Commit()  // 如果上面没回滚，这里会Commit
}

// 推荐写法：defer自动处理
func goodExample() {
    tx, _ := db.Begin()
    defer func() {
        if r := recover(); r != nil {
            tx.Rollback()
            panic(r)  // 重新抛出panic
        }
    }()
    // ... 执行操作 ...
    tx.Commit()
}
```

## 39.21 隔离级别：ReadUncommitted、ReadCommitted、RepeatableRead、Serializable

事务隔离级别定义了事务之间的隔离程度，越高的级别越安全，但性能也越差。

```
┌─────────────────────────────────────────────────────────────────┐
│                    隔离级别金字塔                                  │
│                                                                 │
│                         Serializable                            │
│                        /            \                            │
│              RepeatableRead        ReadCommitted                  │
│               /        \          /        \                     │
│      ReadUncommitted                                    (越往下隔离越弱)│
└─────────────────────────────────────────────────────────────────┘
```

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // ReadUncommitted - 最低级别，可能读到未提交的数据（脏读）
    tx1, _ := db.BeginTx(context.Background(), &sql.TxOptions{
        Isolation: sql.LevelReadUncommitted,
    })
    
    // ReadCommitted - 只有提交后的数据才能被读到（防止脏读，但可能有不可重复读）
    tx2, _ := db.BeginTx(context.Background(), &sql.TxOptions{
        Isolation: sql.LevelReadCommitted,
    })
    
    // RepeatableRead - 保证同一事务中多次读取结果一致（防止不可重复读）
    tx3, _ := db.BeginTx(context.Background(), &sql.TxOptions{
        Isolation: sql.LevelRepeatableRead,
    })
    
    // Serializable - 最高级别，完全串行化（防止幻读，但性能最差）
    tx4, _ := db.BeginTx(context.Background(), &sql.TxOptions{
        Isolation: sql.LevelSerializable,
    })
    
    // 使用完关闭事务
    tx1.Rollback()
    tx2.Rollback()
    tx3.Rollback()
    tx4.Rollback()
}
```

**专业词汇解释：**

- **ReadUncommitted（读未提交）**：最低隔离级别，事务可以读到其他事务未提交的数据。可能产生脏读。
- **ReadCommitted（读已提交）**：只能读到已提交的数据，防止脏读，但可能出现不可重复读。
- **RepeatableRead（可重复读）**：同一事务中多次读取同一数据，结果一致，防止不可重复读。MySQL默认级别。
- **Serializable（串行化）**：最高隔离级别，事务完全串行执行，完全防止幻读，但性能最差。

**隔离级别导致的问题：**

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|---------|------|-----------|------|
| ReadUncommitted | 可能 | 可能 | 可能 |
| ReadCommitted | 不可能 | 可能 | 可能 |
| RepeatableRead | 不可能 | 不可能 | 可能 |
| Serializable | 不可能 | 不可能 | 不可能 |

- **脏读（Dirty Read）**：读到了其他事务未提交的数据
- **不可重复读（Non-repeatable Read）**：同一事务中，两次读取同一行数据结果不同
- **幻读（Phantom Read）**：同一事务中，两次查询返回的行数不同（因为其他事务插入了新行）

## 39.22 NullInt64、NullString、NullTime：空值处理

数据库中的NULL表示"未知"或"空"，Go的原生类型不能直接表示NULL，需要用 `database/sql` 提供的特殊类型。

```go
func main() {
    db, err := sql.Open("mysql", "root:root@tcp(localhost:3306)/testdb?charset=utf8mb4")
    if err != nil {
        panic(err)
    }
    defer db.Close()
    
    // 创建测试表，其中email允许NULL
    db.Exec("CREATE TABLE IF NOT EXISTS users (id INT, name VARCHAR(50), email VARCHAR(50))")
    db.Exec("DELETE FROM users")
    db.Exec("INSERT INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    db.Exec("INSERT INTO users (id, name, email) VALUES (2, 'Bob', NULL)")           // NULL
    db.Exec("INSERT INTO users (id, name, email) VALUES (3, 'Charlie', 'charlie@example.com')")
    
    rows, err := db.Query("SELECT id, name, email FROM users ORDER BY id")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    
    fmt.Println("用户列表：")
    for rows.Next() {
        var (
            id    int
            name  string
            email sql.NullString  // 专门处理NULL的类型
        )
        
        rows.Scan(&id, &name, &email)
        
        // 检查是否为NULL
        if email.Valid {
            fmt.Printf("ID=%d, 姓名=%s, 邮箱=%s\n", id, name, email.String)
        } else {
            fmt.Printf("ID=%d, 姓名=%s, 邮箱=<未填写>\n", id, name)
        }
    }
    
    // 其他可空类型
    var nullInt sql.NullInt64       // 相当于 Go的 int64?（可空）
    var nullBool sql.NullBool       // 相当于 Go的 bool?
    var nullFloat sql.NullFloat64   // 相当于 Go的 float64?
    var nullTime sql.NullTime       // 相当于 Go的 time.Time?
    var nullByte sql.NullByte       // 相当于 Go的 byte?
    
    _ = nullInt
    _ = nullBool
    _ = nullFloat
    _ = nullTime
    _ = nullByte
    
    // 清理测试表
    db.Exec("DROP TABLE users")
}
```

**专业词汇解释：**

- **NULL**：数据库中的特殊值，表示"未知"或"不存在"。它不等于空字符串，也不等于0。
- **NullString**：对应可能为NULL的VARCHAR或TEXT列。
- **NullInt64**：对应可能为NULL的BIGINT或INT列。
- **NullTime**：对应可能为NULL的DATETIME或TIMESTAMP列。

**为什么需要Null类型？**

```go
// 如果直接用string扫描NULL列
var email string
rows.Scan(&email)  // 会出错！因为Go的string不能是nil

// 使用NullString
var email sql.NullString
rows.Scan(&email)  // OK
if email.Valid {
    fmt.Println(email.String)  // 有值
} else {
    fmt.Println("NULL")        // 空值
}
```

## 39.23 database/sql/driver：驱动接口定义

`database/sql/driver` 定义了驱动需要实现的接口。了解这些接口可以更深入理解 `database/sql` 的工作原理。

```go
/*
driver包的核心接口定义（简化版）

// Driver 是数据库驱动必须实现的接口
type Driver interface {
    Open(name string) (Conn, error)  // 打开一个新连接
}

// Conn 代表一个数据库连接
type Conn interface {
    Prepare(query string) (Stmt, error)      // 准备预编译语句
    Close() error                             // 关闭连接
    Begin() (Tx, error)                       // 开始事务
}

// Stmt 代表一个预编译语句
type Stmt interface {
    Close() error                      // 关闭语句
    NumInput() int                     // 返回占位符数量
    Exec(args []Value) (Result, error) // 执行（INSERT/UPDATE/DELETE）
    Query(args []Value) (Rows, error)  // 查询（SELECT）
}

// Tx 代表一个事务
type Tx interface {
    Commit() error       // 提交
    Rollback() error     // 回滚
}

// Rows 代表查询结果集
type Rows interface {
    Columns() []string   // 返回列名
    Close() error        // 关闭游标
    Next(dest []Value) error  // 移动到下一行
}

// Result 是执行INSERT/UPDATE/DELETE的结果
type Result interface {
    LastInsertId() (int64, error)    // 插入的ID
    RowsAffected() (int64, error)    // 影响的行数
}
*/
```

**自定义驱动的简单示例：**

虽然一般不推荐自己写驱动，但了解接口有助于理解工作原理：

```go
package mydriver

import (
    "database/sql"
    "database/sql/driver"
    "fmt"
)

// 注册驱动（驱动包init函数会自动调用）
func init() {
    sql.Register("mydriver", &MyDriver{})
}

// 实现Driver接口
type MyDriver struct{}

func (d *MyDriver) Open(dsn string) (driver.Conn, error) {
    fmt.Printf("连接数据库: %s\n", dsn)
    return &MyConn{}, nil
}

// 实现Conn接口
type MyConn struct{}

func (c *MyConn) Prepare(query string) (driver.Stmt, error) {
    return &MyStmt{query: query}, nil
}

func (c *MyConn) Close() error {
    return nil
}

func (c *MyConn) Begin() (driver.Tx, error) {
    return &MyTx{}, nil
}

// 实现Stmt接口
type MyStmt struct {
    query string
}

func (s *MyStmt) Close() error { return nil }
func (s *MyStmt) NumInput() int { return 0 }
func (s *MyStmt) Exec(args []driver.Value) (driver.Result, error) {
    return &MyResult{}, nil
}
func (s *MyStmt) Query(args []driver.Value) (driver.Rows, error) {
    return &MyRows{}, nil
}

// 实现Tx接口
type MyTx struct{}

func (t *MyTx) Commit() error { return nil }
func (t *MyTx) Rollback() error { return nil }

// 实现Result接口
type MyResult struct{}

func (r *MyResult) LastInsertId() (int64, error) { return 1, nil }
func (r *MyResult) RowsAffected() (int64, error) { return 1, nil }

// 实现Rows接口
type MyRows struct{}

func (r *MyRows) Columns() []string { return nil }
func (r *MyRows) Close() error { return nil }
func (r *MyRows) Next(dest []driver.Value) error { return nil }

// 使用自定义驱动
func ExampleUsage() {
    // import _ "mydriver"
    // db, _ := sql.Open("mydriver", "dsn")
    fmt.Println("驱动已注册，可通过 sql.Open 使用")
}
```

**专业词汇解释：**

- **interface{}（Go 1.17前）/ any（Go 1.18+）**：空接口，所有类型都实现了它。
- **driver.Value**：驱动和数据库之间传递的值类型，可以是 `int64`、`float64`、`bool`、`[]byte`、`string`、`time.Time`。
- **注册机制**：驱动的 `init()` 函数调用 `sql.Register()` 将自己注册到全局 map 中，之后 `sql.Open` 就能找到它了。

---

## 本章小结

本章我们学习了Go语言标准库 `database/sql`，这是Go程序访问数据库的主要方式。以下是本章的核心要点：

### 连接管理

| 方法 | 作用 |
|------|------|
| `sql.Open()` | 创建数据库连接（懒连接，不立刻建立网络连接） |
| `DB.Ping()` | 检查连接是否有效 |
| `DB.SetMaxOpenConns()` | 设置最大并发连接数 |
| `DB.SetMaxIdleConns()` | 设置最大空闲连接数 |
| `DB.SetConnMaxLifetime()` | 设置连接最大生命周期 |

### 查询与执行

| 方法 | 作用 | 返回值 |
|------|------|--------|
| `DB.Query()` | 查询多行 | `*Rows` |
| `DB.QueryRow()` | 查询单行 | `*Row` |
| `DB.Exec()` | 执行INSERT/UPDATE/DELETE | `Result` |
| `DB.Prepare()` | 创建预编译语句 | `*Stmt` |

### Rows遍历模式

```go
rows, err := db.Query("SELECT ...")
if err != nil {
    return err
}
defer rows.Close()

for rows.Next() {
    // 处理当前行
    rows.Scan(&var1, &var2)
}
// 记得检查Err
if err := rows.Err(); err != nil {
    return err
}
```

### 事务处理

```go
tx, err := db.Begin()
if err != nil {
    return err
}

// 执行操作
_, err = tx.Exec("INSERT ...", ...)
if err != nil {
    tx.Rollback()
    return err
}

err = tx.Commit()
```

### 特殊值处理

- `sql.ErrNoRows`：`QueryRow` 没查到记录时的错误
- `sql.NullString`、`sql.NullInt64`、`sql.NullTime` 等：处理数据库NULL值

### 驱动注册

```go
import _ "github.com/go-sql-driver/mysql"
```

驱动通过匿名导入自动注册，`sql.Open("mysql", dsn)` 时会找到已注册的驱动。

### 常见错误与最佳实践

1. **永远 defer rows.Close()**：防止连接泄漏
2. **使用 QueryContext/ExecContext**：支持超时控制
3. **合理设置连接池参数**：根据业务负载调整
4. **事务中记得 Rollback**：异常时自动回滚
5. **使用预编译语句**：提高性能，防止SQL注入

> "学会了database/sql，你就是那个能让程序和数据仓库无缝对话的魔法师。虽然不能像哈利波特那样骑着扫帚飞，但至少能骑着SQL查询从数据库里取出你要的数据。" —— 某位刚写完本章的Gopher
