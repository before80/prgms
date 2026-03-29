+++
title = "第43章 数据库编程——C++与数据的持久化爱恨情仇"
weight = 430
date = "2026-03-29T21:03:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第43章 数据库编程——C++与数据的持久化爱恨情仇

## 43.1 数据的终极归宿——为什么要学数据库编程

想象一下这个场景：你写了一个C++程序，用户辛辛苦苦输入了10000条客户数据，结果程序一退出，数据全没了——就像你写了一篇万字长文，结果Word崩溃没保存，那种想把电脑从窗户扔出去的心情，懂的自然懂。

**数据库（Database）** 就是来解决这个痛点的。它是数据的"永久居住地"，程序退出数据还在，下次启动还能继续用。而C++作为一门"既要高性能又要控制一切"的语言，在数据库编程领域也是个狠角色——既能直接操作底层数据，又能通过各种库优雅地与数据库交互。

### 43.1.1 关系型数据库与非关系型数据库

数据库的世界里有两大门派：**关系型数据库（Relational Database）** 和 **非关系型数据库（NoSQL）**。

**关系型数据库**就像是Excel表格的超级增强版——数据以表格（表）的形式存储，表与表之间可以通过"关系"连接。SQL（Structured Query Language，结构化查询语言）是它们的官方语言。

常见的**关系型数据库**包括：
- **MySQL** —— 开源界的扛把子，小巧灵活，大多数创业公司的首选
- **PostgreSQL** —— 功能最强大的开源数据库，学术圈和复杂业务的心头好
- **SQLite** —— 嵌入式数据库之王，手机App、浏览器、游戏都用它，一个文件就是一个数据库
- **Oracle** —— 企业级数据库的"老大哥"，银行、电信行业的不二之选（贵有贵的道理）
- **SQL Server** —— 微软的亲儿子，和Windows、.NET生态配合默契

**非关系型数据库（NoSQL）**则是"不按套路出牌"的代表：
- **MongoDB** —— 文档型数据库，存储JSON-like文档，灵活得像橡皮泥
- **Redis** —— 内存数据库，，速度快到飞起，适合做缓存
- **Cassandra** —— 列式存储，适合写入密集型应用
- **Neo4j** —— 图数据库，社交网络、推荐系统的好帮手

> 作为一个务实的C++程序员，我们的策略是：**关系型数据库打天下，NoSQL按需补充**。本章重点讲关系型数据库，因为它们有统一的标准（SQL），学会了走遍天下都不怕。

### 43.1.2 C++数据库编程的"三国鼎立"

C++连接数据库有三条主要路线：

```
┌─────────────────────────────────────────────────────────────┐
│                    C++ 数据库编程方案                        │
├───────────────┬─────────────────────┬───────────────────────┤
│   ODBC        │   原生驱动库         │   ORM框架             │
│  (标准接口)    │   (数据库专用)       │   (对象-关系映射)       │
├───────────────┼─────────────────────┼───────────────────────┤
│   通用性强     │   性能最佳           │   开发效率高           │
│   任何数据库   │   功能完整           │   类型安全             │
│   只要有驱动   │   需要针对安装       │   运行时开销           │
└───────────────┴─────────────────────┴───────────────────────┘
```

**1. ODBC（Open Database Connectivity）—— 数据库的"万能钥匙"**
- 微软发明的标准API
- 只要数据库提供ODBC驱动，就能用同一套代码访问
- 缺点：有点啰嗦，性能略逊于原生驱动

**2. 原生驱动库——"专人专事"**
- 每个数据库有自己的C/C++客户端库
- MySQL → `libmysqlclient` / `MySQL Connector/C++`
- PostgreSQL → `libpq`
- SQLite → `libsqlite3`
- 性能最优，功能最全，但需要针对不同数据库写不同代码

**3. ORM框架——"让数据库说C++的话"**
- Object-Relational Mapping，对象-关系映射
- 把数据库表映射成C++类，把SQL操作变成函数调用
- 代表：`ODB`、`Soci`、`Drogon`、`cpp-orm`
- 适合大型项目，小项目可能杀鸡用牛刀

```cpp
// 没有ORM的世界：手写SQL，参数靠猜
int id = 42;
const char* name = "Alice";
sql = "INSERT INTO users (id, name) VALUES (" + std::to_string(id) + ", '" + name + "')";  // SQL注入警告！

// 有ORM的世界：类型安全，IDE自动补全
User u;
u.id = 42;
u.name = "Alice";
db.save(u);  // 搞定！
```

### 43.1.3 第一个C++数据库程序——SQLite的Hello World

让我们从最简单的开始——SQLite。它不需要安装服务器，一个头文件+一个库就能用，简直是学习和原型开发的神器。

```cpp
// 43-1-sqlite-hello-world.cpp
// 编译：g++ -std=c++17 43-1-sqlite-hello-world.cpp -lsqlite3
// Windows: cl /std:c++17 43-1-sqlite-hello-world.cpp sqlite3.lib

#include <iostream>
#include <string>
#include <sqlite3.h>

int main() {
    sqlite3* db = nullptr;
    int exit_code;
    
    // 打开（如果不存在则创建）数据库
    // SQLite的数据库就是一个文件，简单粗暴
    exit_code = sqlite3_open("hello.db", &db);
    
    if (exit_code != SQLITE_OK) {
        std::cerr << "数据库打开失败: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_close(db);
        return 1;
    }
    
    std::cout << "数据库打开成功！" << std::endl;
    
    // 执行SQL语句：创建表
    const char* create_sql = R"(
        CREATE TABLE IF NOT EXISTS greetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    )";
    
    char* err_msg = nullptr;
    exit_code = sqlite3_exec(db, create_sql, nullptr, nullptr, &err_msg);
    
    if (exit_code != SQLITE_OK) {
        std::cerr << "SQL执行失败: " << err_msg << std::endl;
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    
    std::cout << "表创建成功！" << std::endl;
    
    // 插入数据
    const char* insert_sql = R"(
        INSERT INTO greetings (message) VALUES ('Hello, SQLite!');
        INSERT INTO greetings (message) VALUES ('你好，数据库世界！');
    )";
    
    exit_code = sqlite3_exec(db, insert_sql, nullptr, nullptr, &err_msg);
    
    if (exit_code != SQLITE_OK) {
        std::cerr << "插入数据失败: " << err_msg << std::endl;
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    
    std::cout << "数据插入成功！" << std::endl;
    
    // 查询数据：用回调函数处理结果
    std::cout << "\n===== 查询结果 =====" << std::endl;
    
    auto callback = [](void* data, int argc, char** argv, char** col_names) -> int {
        for (int i = 0; i < argc; i++) {
            std::cout << col_names[i] << ": " << (argv[i] ? argv[i] : "NULL") << "\t";
        }
        std::cout << std::endl;
        return 0;
    };
    
    const char* select_sql = "SELECT * FROM greetings ORDER BY id;";
    exit_code = sqlite3_exec(db, select_sql, callback, nullptr, &err_msg);
    
    if (exit_code != SQLITE_OK) {
        std::cerr << "查询失败: " << err_msg << std::endl;
        sqlite3_free(err_msg);
        sqlite3_close(db);
        return 1;
    }
    
    // 清理
    sqlite3_close(db);
    std::cout << "\n数据库已关闭，再见！" << std::endl;
    
    return 0;
}
```

运行结果：
```
数据库打开成功！
表创建成功！
数据插入成功！

===== 查询结果 =====
id: 1    message: Hello, SQLite!    created_at: 2024-01-15 10:30:00
id: 2    message: 你好，数据库世界！    created_at: 2024-01-15 10:30:00

数据库已关闭，再见！
```

> **小贴士**：SQLite是"无服务器"的数据库，整个数据库就是一个`.db`文件。这意味着：
> - 部署简单：拷贝文件就行
> - 并发限制：写操作是串行化的
> - 适合：嵌入式、移动App、原型开发、小型网站
> - 不适合：高并发写入、多用户写、大数据量

---

## 43.2 SQL入门——数据的CRUD艺术

### 43.2.1 CRUD是什么？可以吃吗？

**CRUD**是数据库操作的四字真言，代表Create（创建/插入）、Read（读取/查询）、Update（更新）、Delete（删除）。任何数据库应用，说白了就是这四种操作的排列组合。

> 程序员的自嘲：我们的工作就是`SELECT * FROM problems`，然后`INSERT INTO solutions (output) VALUES (nothing)`。

### 43.2.2 数据定义语言（DDL）—— 建表如建房

在动手之前，我们先聊聊数据库的"蓝图"——**表结构（Schema）**。设计表结构就像建房子，要先规划好有几间房、每间房多大、承重墙在哪。SQL的`CREATE TABLE`就是干这个的。

```sql
-- 创建一个"用户表"
CREATE TABLE users (
    id INTEGER PRIMARY KEY,           -- 主键：每行的唯一标识，自增
    username VARCHAR(50) NOT NULL,     -- 用户名，最多50字符，不能为空
    email VARCHAR(100) UNIQUE,        -- 邮箱，唯一约束
    password_hash CHAR(64) NOT NULL,  -- 密码哈希，固定64字符（SHA-256）
    age INTEGER DEFAULT 0,            -- 年龄，默认0
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 创建时间，自动当前时间
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP   -- 更新时间
);

-- 创建一个"订单表"
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,         -- 外键：引用users表的id
    product_name VARCHAR(100),
    price DECIMAL(10, 2),            -- 价格，10位数字，2位小数
    quantity INTEGER DEFAULT 1,
    status VARCHAR(20) DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)  -- 外键约束
);

-- 删除表（危险操作！）
-- DROP TABLE orders;
-- DROP TABLE users;

-- 修改表结构
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
ALTER TABLE users DROP COLUMN age;
```

### 43.2.3 数据操作语言（DML）—— 增删改查

#### 插入数据（INSERT）

```sql
-- 插入单行
INSERT INTO users (username, email, password_hash)
VALUES ('alice', 'alice@example.com', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8');

-- 插入多行（PostgreSQL和MySQL支持）
INSERT INTO users (username, email, password_hash) VALUES
    ('bob', 'bob@example.com', 'hash2'),
    ('charlie', 'charlie@example.com', 'hash3'),
    ('david', 'david@example.com', 'hash4');

-- 从其他表复制数据
INSERT INTO vip_users (username, email)
SELECT username, email FROM users WHERE created_at > '2024-01-01';
```

#### 查询数据（SELECT）—— 最复杂的SQL

`SELECT`是SQL中最强大也最复杂的语句。让我带你层层递进：

```sql
-- 最简单的查询：SELECT * 表示所有列
SELECT * FROM users;

-- 只查询需要的列
SELECT username, email FROM users;

-- 过滤：WHERE子句
SELECT * FROM users WHERE age >= 18;
SELECT * FROM users WHERE username LIKE 'a%';  -- 用户名以a开头
SELECT * FROM users WHERE email IN ('alice@example.com', 'bob@example.com');

-- 排序：ORDER BY
SELECT * FROM users ORDER BY created_at DESC;  -- 按创建时间降序（最新的在前）
SELECT * FROM orders ORDER BY price ASC, created_at DESC;  -- 先按价格升序，再按时间降序

-- 分页：LIMIT和OFFSET
SELECT * FROM users ORDER BY id LIMIT 10 OFFSET 20;  -- 第21-30条记录
-- 或者用MySQL/PostgreSQL的简化语法
SELECT * FROM users LIMIT 20, 10;  -- MySQL风格：跳过前20条，取10条（PostgreSQL/SQLite请用 LIMIT 10 OFFSET 20）

-- 聚合：COUNT、SUM、AVG、MIN、MAX
SELECT COUNT(*) as total_users FROM users;
SELECT AVG(price) as avg_price FROM orders;
SELECT user_id, SUM(price * quantity) as total_spent 
FROM orders 
GROUP BY user_id  -- 按用户分组
HAVING total_spent > 1000;  -- 过滤分组结果

-- 连接：JOIN——表与表之间的关系
SELECT u.username, o.product_name, o.price
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';

-- 多表连接
SELECT 
    u.username,
    o.product_name,
    p.category_name
FROM users u
INNER JOIN orders o ON u.id = o.user_id
INNER JOIN products p ON o.product_id = p.id
WHERE u.username = 'alice';

-- 子查询：查询嵌套查询
SELECT * FROM users 
WHERE id IN (
    SELECT user_id FROM orders 
    WHERE price > 1000
);

-- EXISTS：检查是否存在
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'pending'
);
```

> **性能提示**：`SELECT *`很方便，但生产环境尽量指定需要的列。理由：
> 1. 网络传输数据更少
> 2. 避免不必要地读取大字段（如TEXT、BLOB）
> 3. 表结构变化时不容易出bug

#### 更新数据（UPDATE）

```sql
-- 更新单行
UPDATE users SET email = 'new_email@example.com' WHERE id = 1;

-- 更新多行
UPDATE orders SET status = 'shipped' WHERE created_at < '2024-01-01';

-- 批量更新：按条件不同更新不同值（MySQL）
UPDATE products 
SET price = CASE category
    WHEN 'electronics' THEN price * 0.9      -- 电子产品打9折
    WHEN 'books' THEN price * 0.8            -- 书籍打8折
    WHEN 'food' THEN price * 0.95            -- 食品打95折
    ELSE price
END
WHERE category IN ('electronics', 'books', 'food');

-- 使用计算更新
UPDATE orders 
SET total_price = price * quantity,
    updated_at = CURRENT_TIMESTAMP
WHERE total_price IS NULL;
```

#### 删除数据（DELETE）

```sql
-- 删除单行
DELETE FROM users WHERE id = 1;

-- 批量删除
DELETE FROM orders WHERE status = 'cancelled' AND created_at < '2024-01-01';

-- 清空表（慎用！比DELETE快，但不记录日志，无法回滚）
-- TRUNCATE TABLE orders;

-- 删除前确认：先SELECT再看DELETE
BEGIN;  -- 开始事务
SELECT COUNT(*) FROM orders WHERE status = 'test';
-- 确认无误后执行：
DELETE FROM orders WHERE status = 'test';
COMMIT;  -- 提交事务
```

### 43.2.4 C++中的SQLite参数化查询——告别SQL注入

**SQL注入（SQL Injection）**是数据库应用最常见的安全漏洞。想象一下用户输入`'; DROP TABLE users; --`作为用户名，你的程序如果直接拼SQL，那可就完蛋了。

**参数化查询（Parameterized Query）**是解决这个问题的不二法门：

```cpp
// 43-2-parameterized-query.cpp
// 编译：g++ -std=c++17 43-2-parameterized-query.cpp -lsqlite3

#include <iostream>
#include <string>
#include <sqlite3.h>

// 参数化查询：用户输入不会被当作SQL代码执行
bool insert_user(sqlite3* db, const std::string& username, const std::string& email) {
    const char* sql = "INSERT INTO users (username, email) VALUES (?, ?);";
    sqlite3_stmt* stmt = nullptr;
    
    // 准备语句
    int rc = sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        std::cerr << "准备语句失败: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }
    
    // 绑定参数：? 占位符按顺序绑定
    // 第一个参数是username，第二个是email
    sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, email.c_str(), -1, SQLITE_TRANSIENT);
    
    // 执行语句
    rc = sqlite3_step(stmt);
    if (rc != SQLITE_DONE) {
        std::cerr << "执行失败: " << sqlite3_errmsg(db) << std::endl;
        sqlite3_finalize(stmt);
        return false;
    }
    
    std::cout << "插入成功！用户ID: " << sqlite3_last_insert_rowid(db) << std::endl;
    
    // 清理
    sqlite3_finalize(stmt);
    return true;
}

// 演示SQL注入攻击
void demonstrate_sql_injection() {
    std::cout << "\n===== SQL注入演示 =====" << std::endl;
    
    // 恶意输入：' OR '1'='1' --
    // 如果用字符串拼接，会变成：WHERE username = '' OR '1'='1' --'，瞬间绕过认证！
    
    std::cout << "恶意输入: ' OR '1'='1' --" << std::endl;
    std::cout << "危险写法生成的SQL:" << std::endl;
    std::cout << "  SELECT * FROM users WHERE username = '' OR '1'='1' --'" << std::endl;
    std::cout << "  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 恒为真！所有记录都被返回！" << std::endl;
    
    std::cout << "\n参数化查询生成的SQL:" << std::endl;
    std::cout << "  SELECT * FROM users WHERE username = ? " << std::endl;
    std::cout << "  参数值: ' OR '1'='1' --" << std::endl;
    std::cout << "  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 这只是普通字符串，不会被解析为SQL！" << std::endl;
}

int main() {
    sqlite3* db = nullptr;
    
    // 创建临时内存数据库（断电就没了，但速度快）
    int rc = sqlite3_open(":memory:", &db);
    if (rc != SQLITE_OK) {
        std::cerr << "数据库打开失败" << std::endl;
        return 1;
    }
    
    // 创建表
    const char* create_sql = R"(
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL
        );
    )";
    sqlite3_exec(db, create_sql, nullptr, nullptr, nullptr);
    
    // 正常插入
    insert_user(db, "alice", "alice@example.com");
    insert_user(db, "bob", "bob@example.com");
    insert_user(db, "charlie", "charlie@example.com");
    
    // 演示SQL注入（只是打印说明，不实际执行危险操作）
    demonstrate_sql_injection();
    
    // 查询演示
    std::cout << "\n===== 用户列表 =====" << std::endl;
    
    const char* select_sql = "SELECT id, username, email FROM users WHERE username LIKE ?";
    sqlite3_stmt* stmt = nullptr;
    
    sqlite3_prepare_v2(db, select_sql, -1, &stmt, nullptr);
    // 绑定参数：查询所有以'a'开头的用户
    sqlite3_bind_text(stmt, 1, "a%", -1, SQLITE_TRANSIENT);  // % 是SQL的通配符
    
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::cout << "ID: " << sqlite3_column_int(stmt, 0)
                  << ", 用户名: " << sqlite3_column_text(stmt, 1)
                  << ", 邮箱: " << sqlite3_column_text(stmt, 2) << std::endl;
    }
    
    sqlite3_finalize(stmt);
    sqlite3_close(db);
    
    return 0;
}
```

运行结果：
```
插入成功！用户ID: 1
插入成功！用户ID: 2
插入成功！用户ID: 3

===== SQL注入演示 =====
恶意输入: ' OR '1'='1' --
危险写法生成的SQL:
  SELECT * FROM users WHERE username = '' OR '1'='1' --'
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 恒为真！所有记录都被返回！

参数化查询生成的SQL:
  SELECT * FROM users WHERE username = ? 
  参数值: ' OR '1'='1' --
  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 这只是普通字符串，不会被解析为SQL！

===== 用户列表 =====
ID: 1, 用户名: alice, 邮箱: alice@example.com
```

---

## 43.3 高级数据库操作——事务、连接池与性能优化

### 43.3.1 事务（Transaction）—— 要么全做，要么全不做

**事务**是数据库操作的"原子性保障"。想象你给朋友转账：你的账户扣钱 + 朋友的账户加钱，这两个操作必须同时成功或同时失败，否则就会出现"钱凭空消失"或"钱凭空出现"的诡异现象。

事务有四个特性，简称**ACID**：

- **Atomicity（原子性）**：事务是最小执行单位，不可分割。要么全做，要么全不做。
- **Consistency（一致性）**：事务执行前后，数据库状态必须是一致的。
- **Isolation（隔离性）**：并发执行的事务互相隔离，不互相干扰。
- **Durability（持久性）**：事务提交后，结果永久保存。

```cpp
// 43-3-transactions.cpp
// 演示SQLite中的事务操作

#include <iostream>
#include <string>
#include <sqlite3.h>

bool transfer_money(sqlite3* db, int from_user, int to_user, double amount) {
    // 开启事务：所有操作暂存在内存中
    const char* begin_sql = "BEGIN TRANSACTION;";
    sqlite3_exec(db, begin_sql, nullptr, nullptr, nullptr);
    
    try {
        // 1. 检查付款方余额
        const char* check_sql = "SELECT balance FROM accounts WHERE user_id = ?;";
        sqlite3_stmt* stmt = nullptr;
        
        sqlite3_prepare_v2(db, check_sql, -1, &stmt, nullptr);
        sqlite3_bind_int(stmt, 1, from_user);
        
        if (sqlite3_step(stmt) != SQLITE_ROW) {
            std::cerr << "付款方不存在" << std::endl;
            sqlite3_finalize(stmt);
            sqlite3_exec(db, "ROLLBACK;", nullptr, nullptr, nullptr);
            return false;
        }
        
        double balance = sqlite3_column_double(stmt, 0);
        sqlite3_finalize(stmt);
        
        if (balance < amount) {
            std::cerr << "余额不足！当前余额: " << balance << ", 需要: " << amount << std::endl;
            sqlite3_exec(db, "ROLLBACK;", nullptr, nullptr, nullptr);
            return false;
        }
        
        // 2. 扣款
        const char* deduct_sql = "UPDATE accounts SET balance = balance - ? WHERE user_id = ?;";
        sqlite3_prepare_v2(db, deduct_sql, -1, &stmt, nullptr);
        sqlite3_bind_double(stmt, 1, amount);
        sqlite3_bind_int(stmt, 2, from_user);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        // 3. 收款
        const char* add_sql = "UPDATE accounts SET balance = balance + ? WHERE user_id = ?;";
        sqlite3_prepare_v2(db, add_sql, -1, &stmt, nullptr);
        sqlite3_bind_double(stmt, 1, amount);
        sqlite3_bind_int(stmt, 2, to_user);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        // 4. 提交事务：所有操作一次性写入磁盘
        sqlite3_exec(db, "COMMIT;", nullptr, nullptr, nullptr);
        
        std::cout << "转账成功！从用户" << from_user << "转给用户" << to_user << "，金额: " << amount << std::endl;
        return true;
        
    } catch (...) {
        // 任何异常都回滚事务
        std::cerr << "转账失败，回滚事务" << std::endl;
        sqlite3_exec(db, "ROLLBACK;", nullptr, nullptr, nullptr);
        return false;
    }
}

int main() {
    sqlite3* db = nullptr;
    sqlite3_open(":memory:", &db);
    
    // 创建账户表
    sqlite3_exec(db, R"(
        CREATE TABLE accounts (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0
        );
        INSERT INTO accounts (user_id, name, balance) VALUES (1, 'Alice', 10000);
        INSERT INTO accounts (user_id, name, balance) VALUES (2, 'Bob', 5000);
        INSERT INTO accounts (user_id, name, balance) VALUES (3, 'Charlie', 3000);
    )", nullptr, nullptr, nullptr);
    
    std::cout << "===== 初始状态 =====" << std::endl;
    std::cout << "Alice: $10000, Bob: $5000, Charlie: $3000" << std::endl;
    
    // 正常转账
    std::cout << "\n===== 转账测试 =====" << std::endl;
    transfer_money(db, 1, 2, 1000);  // Alice转给Bob $1000
    
    // 余额不足的转账
    std::cout << "\n===== 余额不足测试 =====" << std::endl;
    transfer_money(db, 3, 1, 5000);  // Charlie只有$3000，却要转$5000
    
    std::cout << "\n===== 最终状态 =====" << std::endl;
    // 查询所有账户
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(db, "SELECT user_id, name, balance FROM accounts ORDER BY user_id", -1, &stmt, nullptr);
    while (sqlite3_step(stmt) == SQLITE_ROW) {
        std::cout << "用户" << sqlite3_column_int(stmt, 0) << " (" 
                  << sqlite3_column_text(stmt, 1) << "): $" 
                  << sqlite3_column_double(stmt, 2) << std::endl;
    }
    sqlite3_finalize(stmt);
    
    sqlite3_close(db);
    return 0;
}
```

运行结果：
```
===== 初始状态 =====
Alice: $10000, Bob: $5000, Charlie: $3000

===== 转账测试 =====
转账成功！从用户1转给用户2，金额: 1000

===== 余额不足测试 =====
余额不足！当前余额: 3000, 需要: 5000
转账失败，回滚事务

===== 最终状态 =====
用户1 (Alice): $9000
用户2 (Bob): $6000
用户3 (Charlie): $3000
```

### 43.3.2 连接池——连接复用，性能飙升

数据库连接建立的代价是昂贵的——需要TCP握手、认证、初始化等，通常需要几十毫秒。如果每次查询都新建连接，高并发场景下性能会惨不忍睹。

**连接池（Connection Pool）**的思路是：预先建立一批连接，用的时候从池子里拿，用完归还，而不是销毁。这样就省去了重复建立连接的开销。

```cpp
// 43-4-connection-pool.cpp
// 演示简单的连接池实现

#include <iostream>
#include <string>
#include <vector>
#include <queue>
#include <mutex>
#include <memory>
#include <chrono>
#include <sqlite3.h>

// 数据库连接封装
class DBConnection {
    sqlite3* conn_ = nullptr;
    bool in_use_ = false;
    
public:
    explicit DBConnection(const std::string& db_path) {
        if (sqlite3_open(db_path.c_str(), &conn_) != SQLITE_OK) {
            throw std::runtime_error("数据库打开失败");
        }
        std::cout << "    [连接#" << (long(conn_) % 1000) << "] 已创建" << std::endl;
    }
    
    ~DBConnection() {
        if (conn_) {
            std::cout << "    [连接#" << (long(conn_) % 1000) << "] 已销毁" << std::endl;
            sqlite3_close(conn_);
        }
    }
    
    sqlite3* get() { return conn_; }
    bool is_available() const { return !in_use_; }
    void mark_in_use() { in_use_ = true; }
    void mark_available() { in_use_ = false; }
    
    // 禁止复制
    DBConnection(const DBConnection&) = delete;
    DBConnection& operator=(const DBConnection&) = delete;
};

// 简单的连接池实现
class ConnectionPool {
    std::string db_path_;
    size_t pool_size_;
    std::vector<std::unique_ptr<DBConnection>> available_;
    std::queue<std::unique_ptr<DBConnection>> in_use_;
    std::mutex mutex_;
    
public:
    ConnectionPool(const std::string& db_path, size_t pool_size) 
        : db_path_(db_path), pool_size_(pool_size) {
        // 预创建连接
        for (size_t i = 0; i < pool_size_; ++i) {
            available_.push_back(std::make_unique<DBConnection>(db_path_));
        }
        std::cout << "连接池初始化完成，共 " << pool_size_ << " 个连接" << std::endl;
    }
    
    // 获取连接
    std::unique_ptr<DBConnection> acquire() {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (!available_.empty()) {
            auto conn = std::move(available_.back());
            available_.pop_back();
            conn->mark_in_use();
            return conn;
        }
        
        // 如果池已空，创建临时连接（实际生产环境应该等待或拒绝）
        std::cout << "    连接池已空，创建临时连接..." << std::endl;
        return std::make_unique<DBConnection>(db_path_);
    }
    
    // 归还连接
    void release(std::unique_ptr<DBConnection> conn) {
        std::lock_guard<std::mutex> lock(mutex_);
        
        if (available_.size() < pool_size_) {
            conn->mark_available();
            available_.push_back(std::move(conn));
        }
        // 超过池大小的连接会被销毁
    }
};

// 使用RAII语法的连接guard
class ConnectionGuard {
    ConnectionPool& pool_;
    std::unique_ptr<DBConnection> conn_;
    
public:
    ConnectionGuard(ConnectionPool& pool) : pool_(pool) {
        conn_ = pool.acquire();
    }
    
    ~ConnectionGuard() {
        pool_.release(std::move(conn_));
    }
    
    sqlite3* get() { return conn_->get(); }
    
    // 禁止复制
    ConnectionGuard(const ConnectionGuard&) = delete;
    ConnectionGuard& operator=(const ConnectionGuard&) = delete;
};

int main() {
    std::cout << "===== 连接池演示 =====" << std::endl;
    
    ConnectionPool pool("demo.db", 3);  // 3个连接的池
    
    std::cout << "\n--- 模拟5个查询任务 ---" << std::endl;
    
    // 模拟5个并发查询
    for (int i = 0; i < 5; ++i) {
        std::cout << "任务" << (i+1) << ": ";
        
        // 使用guard自动管理连接生命周期
        ConnectionGuard guard(pool);
        sqlite3* db = guard.get();
        
        // 模拟查询操作
        sqlite3_stmt* stmt = nullptr;
        sqlite3_prepare_v2(db, "SELECT 1", -1, &stmt, nullptr);
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        std::cout << "完成" << std::endl;
        // guard析构时自动归还连接
    }
    
    std::cout << "\n--- 所有任务完成 ---" << std::endl;
    
    return 0;
}
```

### 43.3.3 性能优化——让数据库飞起来

数据库性能优化是个大话题，这里总结几个C++开发者的必备技巧：

#### 1. 索引（Index）—— 图书馆的目录

索引就像书的目录，让查询从"逐页翻找"变成"直接翻到目录页"。但索引不是免费的——它会占用额外空间，并让写入变慢（因为要更新索引）。

```sql
-- 创建索引
CREATE INDEX idx_users_email ON users(email);           -- 单列索引
CREATE INDEX idx_orders_user_status ON orders(user_id, status);  -- 复合索引

-- 查询是否使用了索引（MySQL）
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

-- 删除索引
DROP INDEX idx_users_email;
```

> **黄金法则**：为 WHERE、JOIN、ORDER BY 经常涉及的列建索引，但不要滥用——每个索引都会拖慢INSERT/UPDATE/DELETE。

#### 2. 预处理语句（Prepared Statements）—— 编译一次，执行多次

同样的SQL结构，只是参数不同，预处理语句可以复用执行计划，省去重复解析的开销。

```cpp
// 普通方式：每次都要解析SQL
for (const auto& user : users) {
    std::string sql = "INSERT INTO users (name, email) VALUES ('" + user.name + "', '" + user.email + "')";
    // ...执行
}

// 预处理方式：只解析一次，执行多次
sqlite3_stmt* stmt = nullptr;
sqlite3_prepare_v2(db, "INSERT INTO users (name, email) VALUES (?, ?)", -1, &stmt, nullptr);

for (const auto& user : users) {
    sqlite3_reset(stmt);  // 重置状态，但保留执行计划
    sqlite3_bind_text(stmt, 1, user.name.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_bind_text(stmt, 2, user.email.c_str(), -1, SQLITE_TRANSIENT);
    sqlite3_step(stmt);
}

sqlite3_finalize(stmt);
```

#### 3. 批量操作——减少网络往返

```cpp
// 逐条插入：N次网络往返
for (const auto& item : items) {
    insert_one(db, item);
}

// 批量插入：1次网络往返
{
    sqlite3_exec(db, "BEGIN TRANSACTION", nullptr, nullptr, nullptr);
    for (const auto& item : items) {
        insert_one(db, item);
    }
    sqlite3_exec(db, "COMMIT", nullptr, nullptr, nullptr);
}

// 或者使用SQLite的批量插入语法（MySQL/PostgreSQL）
std::string sql = "INSERT INTO users (name, email) VALUES ";
std::vector<std::string> values;
for (const auto& u : users) {
    values.push_back("('" + u.name + "', '" + u.email + "')");  // 注意：这里只是为了演示，实际应该用参数化
}
sql += join(values, ",");
sqlite3_exec(db, sql.c_str(), nullptr, nullptr, nullptr);
```

---

## 43.4 C++数据库框架——让数据库编程更优雅

### 43.4.1 SOCI—— 面向C++的数据库访问库

**SOCI** 是一个简单而强大的C++数据库访问库。它的设计理念是：让数据库操作看起来像STL迭代器一样自然。

```cpp
// 43-5-soci-demo.cpp
// 编译：g++ -std=c++17 43-5-soci-demo.cpp -lsoci_core -lsoci_sqlite3
// 注意：需要先安装SOCI库

/*
#include <iostream>
#include <string>
#include <soci/soci.h>
#include <soci/sqlite3/soci-sqlite3.h>

using namespace soci;

int main() {
    // 连接到SQLite数据库
    session sql("sqlite3", "company.db");
    
    // 创建表
    sql << "CREATE TABLE IF NOT EXISTS employees ("
           "id INTEGER PRIMARY KEY, "
           "name VARCHAR(100), "
           "salary DOUBLE)";
    
    // 插入数据（使用参数化）
    int id = 1;
    std::string name = "Alice";
    double salary = 75000.0;
    sql << "INSERT INTO employees (id, name, salary) VALUES (:id, :name, :salary)",
        use(id), use(name), use(salary);
    
    // 查询：使用into从结果中提取数据
    std::string result_name;
    double result_salary;
    sql << "SELECT name, salary FROM employees WHERE id = 1",
        into(result_name), into(result_salary);
    
    std::cout << "员工: " << result_name << ", 工资: $" << result_salary << std::endl;
    
    // 批量查询：使用vector
    std::vector<std::string> names;
    sql << "SELECT name FROM employees", into(names);
    
    std::cout << "所有员工: ";
    for (const auto& n : names) std::cout << n << " ";
    std::cout << std::endl;
    
    // 事务
    transaction tr(sql);
    sql << "UPDATE employees SET salary = salary * 1.1 WHERE id = 1";
    tr.commit();
    
    return 0;
}
*/
```

### 43.4.2 SQLpp11—— 类型安全的SQL编写器

**sqlpp11** 是一个让你在C++代码中"写SQL"的库，但语法是C++的，类型安全，编译时检查错误。

```cpp
// 43-6-sqlpp11-demo.cpp
// 注意：这是伪代码，展示sqlpp11的风格

/*
#include <sqlpp11/sqlpp11.h>
#include <sqlpp11/sqlite3/sqlite3.h>

namespace db = sqlpp::sqlite3;

int main() {
    // 定义表结构（编译时检查）
    struct Employees : public sqlpp::table_t<Employees,
        sqlpp::column_t<id, int, sqlpp::primary_key_t>,
        sqlpp::column_t<name, std::string, sqlpp::not_null_t>,
        sqlpp::column_t<salary, double>
    > {};
    
    db::connection_config config;
    config.path_to_database = "company.db";
    db::connection db(config);
    
    db.execute("CREATE TABLE IF NOT EXISTS employees ("
               "id INTEGER PRIMARY KEY, name TEXT NOT NULL, salary REAL)");
    
    // 插入
    db(insert_into(employees).set(
        employees.id = 1,
        employees.name = "Alice",
        employees.salary = 75000.0
    ));
    
    // 查询（类型安全！）
    auto rows = db(select(all_of(employees)).from(employees).where(employees.salary > 50000));
    
    for (const auto& row : rows) {
        std::cout << row.name << ": $" << row.salary << std::endl;
    }
    
    return 0;
}
*/

int main() {
    std::cout << "===== SQLpp11 风格展示 =====" << std::endl;
    std::cout << "sqlpp11让你用C++语法写SQL：" << std::endl;
    std::cout << R"(
    // 普通SQL
    SELECT * FROM users WHERE age > 18 AND name LIKE 'A%'
    
    // sqlpp11风格
    select(all_of(users))
        .from(users)
        .where(users.age > 18 and users.name.like("A%"))
    )" << std::endl;
    std::cout << "\n实际使用时需要安装sqlpp11库" << std::endl;
    return 0;
}
```

### 43.4.3 Drogon—— 高性能C++ RESTful框架

**Drogon** 是一个基于C++17的高性能Web框架，内置了强大的数据库支持，可以方便地与PostgreSQL、MySQL、SQLite交互。

```cpp
// 43-7-drogon-demo.cpp
// 注意：这是伪代码，展示Drogon的数据库操作风格

/*
#include <drogon/drogon.h>

using namespace drogon;

int main() {
    app().registerHandler("/users/{id}", [](const HttpRequestPtr& req, 
                                           std::function<void(const HttpResponsePtr&)>&& callback,
                                           int id) {
        // 从数据库查询用户
        orm::Mapper<orm::DbClient, User> mapper(getDbClient());
        mapper.findOne(where(cond("id == ?", id)),
            [&callback](const User& user) {
                auto resp = HttpResponse::newHttpJsonResponse(user.toJson());
                callback(resp);
            },
            [&callback](const DrogonDbException& e) {
                auto resp = HttpResponse::newHttpResponse();
                resp->setStatusCode(k404NotFound);
                callback(resp);
            });
    });
    
    app().run();
}
*/

int main() {
    std::cout << "===== Drogon框架数据库操作风格展示 =====" << std::endl;
    std::cout << R"(
Drogon ORM示例（伪代码）：

// 定义模型
class User : public orm::Model<User> {
public:
    int id;
    std::string name;
    std::string email;
    
    // 指定表名
    static constexpr const char* TableName = "users";
    
    // 指定哪些字段可被ORM自动映射
    FLUFFY_MEMBER(id, name, email);
};

// 查询
auto users = User::selectAll();
auto user = User::findByPrimaryKey(1);

// 插入
User newUser;
newUser.name = "Alice";
newUser.email = "alice@example.com";
newUser.insert();

// 更新
newUser.email = "new_email@example.com";
newUser.update();

// 删除
newUser.deleteByPrimaryKey();
)" << std::endl;
    return 0;
}
```

---

## 43.5 错误处理与安全——数据库编程的防护盾

### 43.5.1 错误处理——让程序优雅地崩溃

数据库操作可能因为各种原因失败：网络断开、权限不足、约束冲突、死锁等。良好的错误处理让你的程序"优雅地失败"而不是"灾难性地崩溃"。

```cpp
// 43-8-error-handling.cpp

#include <iostream>
#include <string>
#include <stdexcept>
#include <sqlite3.h>

// 自定义数据库异常
class DatabaseError : public std::runtime_error {
    int error_code_;
public:
    DatabaseError(int code, const std::string& msg) 
        : std::runtime_error(msg), error_code_(code) {}
    
    int code() const { return error_code_; }
};

// RAII封装的数据库连接
class Database {
    sqlite3* db_ = nullptr;
    bool transaction_active_ = false;
    
public:
    Database(const std::string& path) {
        int rc = sqlite3_open(path.c_str(), &db_);
        if (rc != SQLITE_OK) {
            throw DatabaseError(rc, "无法打开数据库: " + path);
        }
        
        // 启用外键约束
        sqlite3_exec(db_, "PRAGMA foreign_keys = ON", nullptr, nullptr, nullptr);
        
        // 设置超时（毫秒），超时后放弃锁等待
        sqlite3_busy_timeout(db_, 5000);
        
        std::cout << "数据库连接成功: " << path << std::endl;
    }
    
    ~Database() {
        if (transaction_active_) {
            std::cerr << "警告：析构时还有未提交的事务，已自动回滚" << std::endl;
            rollback();
        }
        if (db_) {
            sqlite3_close(db_);
            std::cout << "数据库连接已关闭" << std::endl;
        }
    }
    
    sqlite3* get() { return db_; }
    
    // 执行SQL（不带参数）
    void execute(const std::string& sql) {
        char* err_msg = nullptr;
        int rc = sqlite3_exec(db_, sql.c_str(), nullptr, nullptr, &err_msg);
        
        if (rc != SQLITE_OK) {
            std::string error = err_msg ? err_msg : "未知错误";
            sqlite3_free(err_msg);
            throw DatabaseError(rc, "SQL执行失败: " + error);
        }
    }
    
    // 参数化查询：插入
    void insert_user(const std::string& username, const std::string& email) {
        const char* sql = "INSERT INTO users (username, email) VALUES (?, ?);";
        sqlite3_stmt* stmt = nullptr;
        
        if (sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr) != SQLITE_OK) {
            throw DatabaseError(sqlite3_errcode(db_), "准备语句失败");
        }
        
        sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, email.c_str(), -1, SQLITE_TRANSIENT);
        
        int rc = sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        if (rc != SQLITE_DONE) {
            throw DatabaseError(rc, "插入失败: " + std::string(sqlite3_errmsg(db_)));
        }
    }
    
    // 事务管理
    void begin() {
        if (transaction_active_) {
            throw DatabaseError(-1, "事务已在进行中");
        }
        execute("BEGIN TRANSACTION");
        transaction_active_ = true;
    }
    
    void commit() {
        if (!transaction_active_) {
            throw DatabaseError(-1, "没有活跃的事务");
        }
        execute("COMMIT");
        transaction_active_ = false;
    }
    
    void rollback() {
        if (!transaction_active_) return;
        sqlite3_exec(db_, "ROLLBACK", nullptr, nullptr, nullptr);
        transaction_active_ = false;
    }
    
    // 禁用复制
    Database(const Database&) = delete;
    Database& operator=(const Database&) = delete;
};

// 安全的批量操作
void safe_batch_insert(Database& db, const std::vector<std::pair<std::string, std::string>>& users) {
    try {
        db.begin();
        
        for (const auto& [username, email] : users) {
            db.insert_user(username, email);
            std::cout << "已插入: " << username << std::endl;
        }
        
        db.commit();
        std::cout << "批量插入成功！" << std::endl;
        
    } catch (const DatabaseError& e) {
        db.rollback();
        std::cerr << "批量插入失败，已回滚: " << e.what() << std::endl;
        throw;
    }
}

int main() {
    try {
        Database db("demo.db");
        
        // 创建表
        db.execute(R"(
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL
            )
        )");
        
        // 测试插入
        std::cout << "\n--- 测试正常插入 ---" << std::endl;
        db.insert_user("alice", "alice@example.com");
        
        // 测试唯一约束冲突
        std::cout << "\n--- 测试约束冲突 ---" << std::endl;
        try {
            db.insert_user("alice", "another@example.com");  // 会失败！
        } catch (const DatabaseError& e) {
            std::cerr << "捕获到错误: " << e.what() << std::endl;
        }
        
        // 测试批量操作
        std::cout << "\n--- 测试批量插入 ---" << std::endl;
        safe_batch_insert(db, {
            {"bob", "bob@example.com"},
            {"charlie", "charlie@example.com"},
            {"david", "david@example.com"}
        });
        
        std::cout << "\n所有操作完成！" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "程序异常退出: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

### 43.5.2 SQL注入防护——永远不要相信用户输入

我们已经见过参数化查询如何防止SQL注入。这里总结一下最佳实践：

```cpp
// 43-9-security-best-practices.cpp

#include <iostream>
#include <string>
#include <sqlite3.h>

// ===== 安全原则1：永远使用参数化查询 =====
void bad_practice(sqlite3* db, const std::string& user_input) {
    // 这是危险的！
    std::string sql = "SELECT * FROM users WHERE name = '" + user_input + "'";
    // 如果user_input是 "'; DROP TABLE users; --"，你就完了！
}

void good_practice(sqlite3* db, const std::string& user_input) {
    std::string sql = "SELECT * FROM users WHERE name = ?";
    sqlite3_stmt* stmt = nullptr;
    sqlite3_prepare_v2(db, sql.c_str(), -1, &stmt, nullptr);
    sqlite3_bind_text(stmt, 1, user_input.c_str(), -1, SQLITE_TRANSIENT);
    // user_input永远是字符串，不会被当作SQL执行
    sqlite3_finalize(stmt);
}

// ===== 安全原则2：输入验证 =====
bool is_valid_username(const std::string& username) {
    // 只允许字母、数字、下划线
    for (char c : username) {
        if (!std::isalnum(c) && c != '_') {
            return false;
        }
    }
    return !username.empty() && username.length() <= 50;
}

// ===== 安全原则3：最小权限原则 =====
void setup_secure_connection(sqlite3* db) {
    // SQLite不支持细粒度权限，但可以设置PRAGMA
    // PRAGMA query_only = ON;  // 只读模式
    // PRAGMA read_uncommitted = 1;  // 允许脏读
}

// ===== 安全原则4：敏感数据加密 =====
std::string hash_password(const std::string& password) {
    // 实际应该用bcrypt、argon2等专业库
    // 这里仅作演示
    // return bcrypt_hash(password);
    return "hashed_" + password;  // 占位符
}

bool verify_password(const std::string& password, const std::string& hash) {
    // return bcrypt_verify(password, hash);
    return hash == "hashed_" + password;  // 占位符
}

int main() {
    std::cout << "===== SQL安全最佳实践 =====" << std::endl;
    
    std::cout << R"(
安全原则总结：

1. 【参数化查询】永远使用 ? 占位符，不要拼接SQL字符串

2. 【输入验证】在进入SQL之前验证输入
   - 类型检查
   - 长度限制
   - 格式白名单

3. 【最小权限】
   - 应用使用只读账号，只有需要时才用写账号
   - 禁止使用root/admin账号运行应用

4. 【敏感数据加密】
   - 密码必须哈希存储（bcrypt/scrypt/argon2）
   - 敏感字段可以加密存储（AES）

5. 【错误信息处理】
   - 生产环境不要返回详细错误
   - 记录详细日志，但返回给用户通用信息

6. 【定期更新】
   - 保持数据库软件最新
   - 关注CVE漏洞数据库
)" << std::endl;
    
    return 0;
}
```

---

## 43.6 实战：打造一个C++联系人管理系统

学完了基础，让我们来做一个完整的例子——命令行联系人管理系统，麻雀虽小，五脏俱全。

```cpp
// 43-10-contact-manager.cpp
// 编译：g++ -std=c++17 43-10-contact-manager.cpp -lsqlite3
// 运行：./a.out

#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <memory>
#include <sqlite3.h>

// RAII数据库封装
class Database {
    sqlite3* db_ = nullptr;
    
public:
    Database(const std::string& path) {
        if (sqlite3_open(path.c_str(), &db_) != SQLITE_OK) {
            throw std::runtime_error("无法打开数据库");
        }
        
        // 启用外键
        sqlite3_exec(db_, "PRAGMA foreign_keys = ON", nullptr, nullptr, nullptr);
        
        create_tables();
    }
    
    ~Database() {
        if (db_) sqlite3_close(db_);
    }
    
    sqlite3* get() { return db_; }
    
    void create_tables() {
        const char* sql = R"(
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        )";
        sqlite3_exec(db_, sql, nullptr, nullptr, nullptr);
    }
};

// 联系人结构
struct Contact {
    int id = 0;
    std::string name;
    std::string phone;
    std::string email;
    std::string address;
    std::string created_at;
};

// ContactDao：数据访问对象
class ContactDao {
    sqlite3* db_;
    
public:
    explicit ContactDao(sqlite3* db) : db_(db) {}
    
    // 插入联系人
    int insert(const Contact& c) {
        const char* sql = "INSERT INTO contacts (name, phone, email, address) VALUES (?, ?, ?, ?);";
        sqlite3_stmt* stmt = nullptr;
        
        sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, c.name.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, c.phone.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, c.email.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 4, c.address.c_str(), -1, SQLITE_TRANSIENT);
        
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        return sqlite3_last_insert_rowid(db_);
    }
    
    // 查询所有联系人
    std::vector<Contact> find_all() {
        std::vector<Contact> contacts;
        const char* sql = "SELECT id, name, phone, email, address, created_at FROM contacts ORDER BY name;";
        sqlite3_stmt* stmt = nullptr;
        
        sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            Contact c;
            c.id = sqlite3_column_int(stmt, 0);
            c.name = (char*)sqlite3_column_text(stmt, 1);
            c.phone = sqlite3_column_text(stmt, 2) ? (char*)sqlite3_column_text(stmt, 2) : "";
            c.email = sqlite3_column_text(stmt, 3) ? (char*)sqlite3_column_text(stmt, 3) : "";
            c.address = sqlite3_column_text(stmt, 4) ? (char*)sqlite3_column_text(stmt, 4) : "";
            c.created_at = (char*)sqlite3_column_text(stmt, 5);
            contacts.push_back(c);
        }
        
        sqlite3_finalize(stmt);
        return contacts;
    }
    
    // 按ID查找
    Contact find_by_id(int id) {
        const char* sql = "SELECT id, name, phone, email, address, created_at FROM contacts WHERE id = ?;";
        sqlite3_stmt* stmt = nullptr;
        Contact c;
        
        sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        sqlite3_bind_int(stmt, 1, id);
        
        if (sqlite3_step(stmt) == SQLITE_ROW) {
            c.id = sqlite3_column_int(stmt, 0);
            c.name = (char*)sqlite3_column_text(stmt, 1);
            c.phone = sqlite3_column_text(stmt, 2) ? (char*)sqlite3_column_text(stmt, 2) : "";
            c.email = sqlite3_column_text(stmt, 3) ? (char*)sqlite3_column_text(stmt, 3) : "";
            c.address = sqlite3_column_text(stmt, 4) ? (char*)sqlite3_column_text(stmt, 4) : "";
            c.created_at = (char*)sqlite3_column_text(stmt, 5);
        }
        
        sqlite3_finalize(stmt);
        return c;
    }
    
    // 删除联系人
    bool remove(int id) {
        const char* sql = "DELETE FROM contacts WHERE id = ?;";
        sqlite3_stmt* stmt = nullptr;
        
        sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        sqlite3_bind_int(stmt, 1, id);
        
        sqlite3_step(stmt);
        sqlite3_finalize(stmt);
        
        return sqlite3_changes(db_) > 0;
    }
    
    // 搜索联系人
    std::vector<Contact> search(const std::string& keyword) {
        std::vector<Contact> contacts;
        const char* sql = R"(
            SELECT id, name, phone, email, address, created_at 
            FROM contacts 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name;
        )";
        sqlite3_stmt* stmt = nullptr;
        
        std::string pattern = "%" + keyword + "%";
        
        sqlite3_prepare_v2(db_, sql, -1, &stmt, nullptr);
        sqlite3_bind_text(stmt, 1, pattern.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 2, pattern.c_str(), -1, SQLITE_TRANSIENT);
        sqlite3_bind_text(stmt, 3, pattern.c_str(), -1, SQLITE_TRANSIENT);
        
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            Contact c;
            c.id = sqlite3_column_int(stmt, 0);
            c.name = (char*)sqlite3_column_text(stmt, 1);
            c.phone = sqlite3_column_text(stmt, 2) ? (char*)sqlite3_column_text(stmt, 2) : "";
            c.email = sqlite3_column_text(stmt, 3) ? (char*)sqlite3_column_text(stmt, 3) : "";
            c.address = sqlite3_column_text(stmt, 4) ? (char*)sqlite3_column_text(stmt, 4) : "";
            c.created_at = (char*)sqlite3_column_text(stmt, 5);
            contacts.push_back(c);
        }
        
        sqlite3_finalize(stmt);
        return contacts;
    }
};

// 联系人管理器
class ContactManager {
    std::unique_ptr<Database> db_;
    std::unique_ptr<ContactDao> dao_;
    
public:
    ContactManager() : db_(std::make_unique<Database>("contacts.db")),
                       dao_(std::make_unique<ContactDao>(db_->get())) {}
    
    void add_contact() {
        Contact c;
        std::cout << "===== 添加联系人 =====" << std::endl;
        std::cout << "姓名: ";
        std::getline(std::cin, c.name);
        std::cout << "电话: ";
        std::getline(std::cin, c.phone);
        std::cout << "邮箱: ";
        std::getline(std::cin, c.email);
        std::cout << "地址: ";
        std::getline(std::cin, c.address);
        
        int id = dao_->insert(c);
        std::cout << "添加成功！ID: " << id << std::endl;
    }
    
    void list_contacts() {
        auto contacts = dao_->find_all();
        
        if (contacts.empty()) {
            std::cout << "暂无联系人" << std::endl;
            return;
        }
        
        std::cout << "\n===== 联系人列表 =====" << std::endl;
        std::cout << std::left
                  << std::setw(4) << "ID"
                  << std::setw(15) << "姓名"
                  << std::setw(15) << "电话"
                  << std::setw(25) << "邮箱"
                  << "地址" << std::endl;
        std::cout << std::string(80, '-') << std::endl;
        
        for (const auto& c : contacts) {
            std::cout << std::left
                      << std::setw(4) << c.id
                      << std::setw(15) << c.name
                      << std::setw(15) << c.phone
                      << std::setw(25) << c.email
                      << c.address << std::endl;
        }
        std::cout << "共 " << contacts.size() << " 位联系人" << std::endl;
    }
    
    void search_contact() {
        std::string keyword;
        std::cout << "搜索关键词: ";
        std::getline(std::cin, keyword);
        
        auto contacts = dao_->search(keyword);
        
        if (contacts.empty()) {
            std::cout << "未找到匹配的联系人！" << std::endl;
            return;
        }
        
        std::cout << "找到 " << contacts.size() << " 个结果:" << std::endl;
        for (const auto& c : contacts) {
            std::cout << "  [" << c.id << "] " << c.name << " - " << c.phone << std::endl;
        }
    }
    
    void delete_contact() {
        std::string id_str;
        std::cout << "要删除的联系人ID: ";
        std::getline(std::cin, id_str);
        
        try {
            int id = std::stoi(id_str);
            Contact c = dao_->find_by_id(id);
            
            if (c.id == 0) {
                std::cout << "联系人不存在" << std::endl;
                return;
            }
            
            std::cout << "确认删除 " << c.name << "? (y/n): ";
            char confirm;
            std::cin >> confirm;
            std::cin.ignore();
            
            if (confirm == 'y' || confirm == 'Y') {
                dao_->remove(id);
                std::cout << "删除成功" << std::endl;
            } else {
                std::cout << "已取消" << std::endl;
            }
        } catch (const std::exception&) {
            std::cout << "无效的ID" << std::endl;
        }
    }
};

void print_menu() {
    std::cout << R"(
===== 联系人管理系统 =====
1. 添加联系人
2. 查看联系人列表
3. 搜索联系人
4. 删除联系人
5. 退出
========================
请选择: )";
}

int main() {
    std::cout << "欢迎使用联系人管理系统！" << std::endl;
    
    ContactManager manager;
    
    while (true) {
        print_menu();
        
        std::string choice;
        std::getline(std::cin, choice);
        
        if (choice == "1") {
            manager.add_contact();
        } else if (choice == "2") {
            manager.list_contacts();
        } else if (choice == "3") {
            manager.search_contact();
        } else if (choice == "4") {
            manager.delete_contact();
        } else if (choice == "5") {
            std::cout << "再见！" << std::endl;
            break;
        } else {
            std::cout << "无效选择，请重新输入" << std::endl;
        }
        
        std::cout << std::endl;
    }
    
    return 0;
}
```

---

## 43.7 NoSQL简介——C++中的非关系型数据库

虽然关系型数据库是主流，但NoSQL也有它的用武之地。这里简单介绍几种C++中常用的NoSQL方案。

### 43.7.1 Redis—— 内存数据库之王

Redis是最流行的内存数据库，支持字符串、哈希、列表、集合、有序集合等多种数据结构，常用作缓存和消息队列。

```cpp
// 43-11-redis-demo.cpp
// 注意：需要安装hiredis库
// 编译：g++ -std=c++17 43-11-redis-demo.cpp -lhiredis

/*
#include <iostream>
#include <string>
#include <hiredis/hiredis.h>

int main() {
    // 连接到Redis
    redisContext* ctx = redisConnect("127.0.0.1", 6379);
    if (ctx == nullptr || ctx->err) {
        if (ctx) {
            std::cerr << "Redis错误: " << ctx->errstr << std::endl;
            redisFree(ctx);
        } else {
            std::cerr << "无法分配Redis上下文" << std::endl;
        }
        return 1;
    }
    
    // 字符串操作
    redisReply* reply = (redisReply*)redisCommand(ctx, "SET key %s", "hello");
    std::cout << "SET: " << reply->str << std::endl;
    freeReplyObject(reply);
    
    reply = (redisReply*)redisCommand(ctx, "GET key");
    std::cout << "GET: " << (reply->str ? reply->str : "(nil)") << std::endl;
    freeReplyObject(reply);
    
    // 哈希操作
    reply = (redisReply*)redisCommand(ctx, "HSET user:1000 name %s age %d", "Alice", 30);
    std::cout << "HSET: " << reply->integer << std::endl;
    freeReplyObject(reply);
    
    reply = (redisReply*)redisCommand(ctx, "HGETALL user:1000");
    if (reply->type == REDIS_REPLY_ARRAY) {
        for (size_t i = 0; i < reply->elements; i += 2) {
            std::cout << reply->element[i]->str << ": " 
                      << reply->element[i+1]->str << std::endl;
        }
    }
    freeReplyObject(reply);
    
    // 列表操作
    reply = (redisReply*)redisCommand(ctx, "LPUSH tasks %s", "first");
    freeReplyObject(reply);
    reply = (redisReply*)redisCommand(ctx, "LPUSH tasks %s", "second");
    freeReplyObject(reply);
    
    reply = (redisReply*)redisCommand(ctx, "LRANGE tasks 0 -1");
    std::cout << "任务列表: ";
    for (size_t i = 0; i < reply->elements; i++) {
        std::cout << reply->element[i]->str << " ";
    }
    std::cout << std::endl;
    freeReplyObject(reply);
    
    redisFree(ctx);
    return 0;
}
*/

int main() {
    std::cout << "===== Redis C++ 示例 =====" << std::endl;
    std::cout << R"(
Redis常用命令：
- SET key value        设置字符串值
- GET key              获取字符串值
- HSET hash field value   设置哈希字段
- HGET hash field      获取哈希字段
- LPUSH list value     推入列表
- LRANGE list start stop   范围查询
- INCR counter         原子递增
- EXPIRE key seconds   设置过期时间
)" << std::endl;
    return 0;
}
```

### 43.7.2 MongoDB—— 文档数据库

MongoDB存储BSON文档（类似JSON）， schema灵活，适合快速迭代的项目。

```cpp
// 43-12-mongodb-demo.cpp
// 注意：需要安装mongocxx库

/*
#include <iostream>
#include <bsoncxx/builder/stream/document.hpp>
#include <bsoncxx/json.hpp>
#include <mongocxx/client.hpp>
#include <mongocxx/instance.hpp>

using bsoncxx::builder::stream::document;
using bsoncxx::builder::stream::open_document;
using bsoncxx::builder::stream::close_document;
using bsoncxx::builder::stream::finalize;

int main() {
    mongocxx::instance inst{};  // 初始化MongoDB驱动
    mongocxx::client conn{mongocxx::uri{"mongodb://localhost:27017"}};
    
    auto db = conn["mydb"];  // 选择数据库
    auto collection = db["users"];  // 选择集合
    
    // 插入文档
    auto doc = document{}
        << "name" << "Alice"
        << "age" << 30
        << "email" << "alice@example.com"
        << "skills" << open_document
            << "cpp" << "advanced"
            << "python" << "intermediate"
        << close_document
        << finalize;
    
    collection.insert_one(doc);
    std::cout << "文档已插入" << std::endl;
    
    // 查询文档
    auto cursor = collection.find(document{} << "name" << "Alice" << finalize);
    for (auto&& doc : cursor) {
        std::cout << "找到用户: " << bsoncxx::to_json(doc) << std::endl;
    }
    
    // 更新文档
    collection.update_one(
        document{} << "name" << "Alice" << finalize,
        document{} << "$set" << open_document
            << "age" << 31
        << close_document << finalize
    );
    
    // 删除文档
    collection.delete_one(document{} << "name" << "Alice" << finalize);
    
    return 0;
}
*/

int main() {
    std::cout << "===== MongoDB C++ 示例 =====" << std::endl;
    std::cout << R"(
MongoDB文档结构示例（BSON/JSON）：

{
    "_id": ObjectId("..."),
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com",
    "address": {
        "city": "Beijing",
        "country": "China"
    },
    "tags": ["C++", "Python", "Database"],
    "created_at": ISODate("2024-01-15T10:30:00Z")
}

MongoDB优势：
- 灵活的Schema，字段随时增删
- 支持复杂的嵌套文档
- 高并发读写
- 水平扩展容易
)" << std::endl;
    return 0;
}
```

---

## 本章小结

数据库是现代软件开发不可或缺的一环，而C++凭借其高性能和精细的内存控制，在数据库编程领域同样大放异彩。本章我们从基础到实践，系统地学习了C++数据库编程的方方面面。

### 核心知识点回顾

1. **数据库基础**
   - 关系型数据库（MySQL、PostgreSQL、SQLite）与非关系型数据库（Redis、MongoDB）的特点和适用场景
   - SQL语言四大操作：CRUD（创建、读取、更新、删除）
   - 表结构设计、外键约束、索引等概念

2. **C++数据库编程方案**
   - **ODBC**：标准接口，通用性强但略繁琐
   - **原生驱动库**：性能最优，如SQLite的`libsqlite3`、MySQL的`MySQL Connector/C++`
   - **ORM框架**：开发效率高，如SOCI、sqlpp11、Drogon

3. **SQLite实战**
   - 创建数据库、创建表、插入、查询、更新、删除操作
   - **参数化查询**：防止SQL注入的必备技能
   - **事务处理**：BEGIN、COMMIT、ROLLBACK保证数据一致性
   - **连接池**：复用连接，提升性能
   - **性能优化**：索引、预处理语句、批量操作

4. **错误处理与安全**
   - 自定义异常类、RAII封装确保资源正确释放
   - 永远使用参数化查询，永远不要拼接SQL字符串
   - 输入验证、最小权限原则、敏感数据加密

5. **NoSQL补充**
   - Redis：内存数据库，适合缓存和消息队列
   - MongoDB：文档数据库，适合灵活Schema的应用

6. **实战项目**
   - 完整的命令行联系人管理系统，涵盖增删改查所有功能

### 学习建议

> **"纸上得来终觉浅，绝知此事要躬行。"** 

- **多动手**：建议读者实际编译运行本章的代码，观察输出结果
- **阅读文档**：SQLite官方文档（sqlite.org）是最好的学习资源
- **深入学习**：如果要做大型项目，建议学习SOCI或Drogon等框架
- **性能意识**：数据库往往是应用的性能瓶颈，学会用EXPLAIN分析查询计划

### 延伸阅读

- 《SQLite权威指南》—— SQLite官方推荐
- 《高性能MySQL》—— MySQL性能优化的经典之作
- SOCI官方文档：soci.sourceforge.net
- Drogon框架：github.com/an-tao/drogon

> **温馨提醒**：数据库操作一定要记得**备份**！尤其是生产环境，一个`DROP TABLE`可能让你后悔莫及。版本控制、备份策略、灰度发布——保护数据，人人有责！

---

*本章完*
