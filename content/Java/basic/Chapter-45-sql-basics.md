+++
title = "第45章 SQL 与数据库基础"
weight = 450
date = "2026-03-30T14:33:56.932+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第四十五章 SQL 与数据库基础

> 在程序员的世界里，有两大终极拷问："我的代码为什么跑不起来"和"我的数据去哪儿了"。前者靠debug，后者靠——你猜对了——数据库。而SQL，就是你和数据库之间的"翻译官"。

## 45.1 SQL 基础

### 什么是SQL？

**SQL（Structured Query Language）**，中文名"结构化查询语言"。别看名字里带"查询"俩字，它可不只是用来查数据的——增删改查，它全包了。SQL是数据库的官方语言，就像Java是JVM上的官方语言一样（这个比喻Java味很浓吧）。

打个比方：如果数据库是一栋大楼，SQL就是进出这栋大楼的钥匙和电梯卡。你可以新建房间（CREATE）、装修房间（UPDATE）、抄家搬空（DELETE）、或者只是趴在门口看看里面住着谁（SELECT）。

### SQL的"门派"之分

江湖上主要有两派SQL方言：

- **MySQL** —— 开源免费，小巧灵活，野路子出身但粉丝众多，互联网公司的最爱
- **Oracle** —— 企业级大佬，稳定可靠，你值得拥有（如果你不差钱的话）
- **PostgreSQL** —— 学霸型选手，功能全面，学术圈和高端项目常客
- **SQL Server** —— 微软嫡系，Windows平台上的企业级首选

我们这套教程的示例，主要跑在MySQL上，因为它最亲民、最常见、最重要的是——免费！

### SQL的基本语法规则

```sql
-- SQL语句以分号结尾（大部分数据库都这样）
SELECT * FROM users;

-- 关键字不区分大小写，但业界习惯大写
select * from users;  -- 能跑，但不推荐
SELECT * FROM users;  -- 规范写法，看着就专业

-- 字符串用单引号包起来
SELECT * FROM users WHERE name = '张三';

-- 注释用 -- 开头，和Java的 // 一样
SELECT * FROM users WHERE id = 1;  -- 查询id为1的用户
```

> 小知识：SQL对大小写不敏感，意味着你可以写成`select SELECT SeLeCt`，数据库都能听懂。但为了代码可读性，请保持大写关键字的习惯。

## 45.2 表操作

### 创建表——给数据建房子

**表（Table）** 是数据库中最基本的数据存储单位，你可以把它想象成一张Excel表格——有行有列，有表头有数据。

```sql
-- 创建一个用户表
CREATE TABLE users (
    id INT,                -- 用户ID，整数类型
    username VARCHAR(50),  -- 用户名，最多50个字符
    email VARCHAR(100),    -- 邮箱
    age INT,               -- 年龄
    created_at DATETIME    -- 注册时间
);
```

建表的时候，你需要告诉数据库：

- 字段叫什么名字
- 字段存什么类型的 data（数据类型）
- 字段能不能为空（NULL）
- 字段要不要唯一（UNIQUE）
- 字段有没有默认值（DEFAULT）

来一个更完善的版本：

```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,  -- 主键：每条记录的唯一身份证
    username VARCHAR(50) NOT NULL,      -- 不能为空
    email VARCHAR(100) UNIQUE,           -- 不能重复
    age INT DEFAULT 18,                 -- 默认18岁
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- 默认当前时间
);
```

### 修改表——装修时间到

表建好了，想加个字段？改个名字？完全OK！

```sql
-- 新增一列：给用户加个"手机号"字段
ALTER TABLE users ADD COLUMN phone VARCHAR(20);

-- 修改字段类型：把手机号改成可变长度
ALTER TABLE users MODIFY COLUMN phone VARCHAR(15);

-- 删除字段：不需要手机号了
ALTER TABLE users DROP COLUMN phone;

-- 表重命名：users太土了，改成registered_users
ALTER TABLE users RENAME TO registered_users;
```

### 删除表——拆迁队来了

```sql
-- 删除整个表，包括数据和结构都没了！
DROP TABLE users;

-- 如果表不存在会报错，加个IF EXISTS更安全
DROP TABLE IF EXISTS users;
```

> 警告：这个操作是**不可逆**的！删表之前请三思三思再三思，必要时先备份。删库到跑路可不是闹着玩的。

## 45.3 查询

终于到了SQL的精髓所在——**查询（SELECT）**！如果说SQL是数据库的钥匙，那SELECT就是钥匙上最亮的那颗钻石。

### 基础查询

```sql
-- 查询所有用户的所有信息
SELECT * FROM users;

-- 查询指定列
SELECT username, email FROM users;

-- 给列取个中文别名，看着更亲切
SELECT username AS '用户名', email AS '邮箱' FROM users;
```

### 条件查询——WHERE的艺术

```sql
-- 查询年龄大于18的用户
SELECT * FROM users WHERE age > 18;

-- 查询年龄在18到25之间的用户（包含两端）
SELECT * FROM users WHERE age BETWEEN 18 AND 25;

-- 查询邮箱以163结尾的用户（模糊查询）
SELECT * FROM users WHERE email LIKE '%163.com';

-- 查询男性用户（假设有gender字段）
SELECT * FROM users WHERE gender = '男';

-- 多个条件组合：男性 且 年龄大于18
SELECT * FROM users WHERE gender = '男' AND age > 18;

-- 满足任意一个条件就行
SELECT * FROM users WHERE age < 18 OR age > 60;
```

### 排序——谁站C位

```sql
-- 按年龄升序排序（从小到大，数字小的在前）
SELECT * FROM users ORDER BY age ASC;

-- 按年龄降序排序（从大到小）
SELECT * FROM users ORDER BY age DESC;

-- 先按年龄降序，年龄相同的话按用户名升序
SELECT * FROM users ORDER BY age DESC, username ASC;
```

### 分页查询——数据太多了怎么办

```sql
--  LIMIT offset, count
-- 查询第1-10条记录（第一页）
SELECT * FROM users LIMIT 0, 10;

-- 查询第11-20条记录（第二页）
SELECT * FROM users LIMIT 10, 10;

-- MySQL特有的简写：只写数量，默认从0开始
SELECT * FROM users LIMIT 10;  -- 查询前10条
```

### 聚合函数——统计小能手

聚合函数就是对一组数据进行"打包处理"的函数。

```sql
-- 统计用户总数
SELECT COUNT(*) FROM users;

-- 计算平均年龄
SELECT AVG(age) FROM users;

-- 求最大年龄和最小年龄
SELECT MAX(age), MIN(age) FROM users;

-- 计算年龄总和
SELECT SUM(age) FROM users;
```

### 分组查询——物以类聚

```sql
-- 按性别分组，统计每组的人数
SELECT gender, COUNT(*) FROM users GROUP BY gender;

-- 按城市分组，统计每个城市的用户数量，并按数量降序排列
SELECT city, COUNT(*) AS cnt FROM users 
GROUP BY city 
ORDER BY cnt DESC;
```

### HAVING——分组后的过滤

WHERE和HAVING的区别你要搞清楚：

- **WHERE**：过滤**每一行**数据，在分组之前起作用
- **HAVING**：过滤**分组后**的结果，在分组之后起作用

```sql
-- 查询用户数量大于10的城市
SELECT city, COUNT(*) AS cnt 
FROM users 
GROUP BY city 
HAVING cnt > 10;
```

### 多表查询——表亲之间的走动

实际工作中，数据往往分散在多张表里，你需要把它们"连接"起来。

```sql
-- 假设有两张表：users（用户表）和 orders（订单表）
-- users: id, username
-- orders: id, user_id, amount

-- 内连接：只保留有关联的数据
SELECT u.username, o.amount 
FROM users u 
INNER JOIN orders o ON u.id = o.user_id;

-- 左连接：左边表的数据全部保留，右边没有匹配的显示NULL
SELECT u.username, o.amount 
FROM users u 
LEFT JOIN orders o ON u.id = o.user_id;

-- 右连接：右边表的数据全部保留
SELECT u.username, o.amount 
FROM users u 
RIGHT JOIN orders o ON u.id = o.user_id;
```

![SQL表关系图](https://via.placeholder.com/800x400?text=SQL+Table+Relationships+Diagram)

> 图示说明：用户表（users）和订单表（orders）通过user_id关联。一个用户可以有多个订单（1对多关系），这是数据库设计中最常见的关系模式。

### 子查询——查询里面套查询

```sql
-- 查询比平均年龄大的用户
SELECT * FROM users 
WHERE age > (SELECT AVG(age) FROM users);

-- 查询订单金额大于100的用户
SELECT * FROM users 
WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);
```

## 45.4 函数

SQL不仅能做数据筛选和计算，还内置了大量**函数**来处理数据。下面介绍几个最常用的。

### 字符串函数

```sql
-- 拼接字符串
SELECT CONCAT(username, '-', email) FROM users;

-- 计算字符串长度
SELECT username, LENGTH(username) FROM users;

-- 截取字符串（从第1个字符开始，截取5个）
SELECT SUBSTRING(username, 1, 5) FROM users;

-- 转大写/小写
SELECT UPPER(username), LOWER(email) FROM users;

-- 去除首尾空格
SELECT TRIM('  hello  ');
```

### 数值函数

```sql
-- 四舍五入
SELECT ROUND(3.14159, 2);  -- 结果：3.14

-- 向上取整
SELECT CEIL(3.14);  -- 结果：4

-- 向下取整
SELECT FLOOR(3.14);  -- 结果：3

-- 绝对值
SELECT ABS(-100);  -- 结果：100

-- 随机数（0-1之间）
SELECT RAND();
```

### 日期函数

```sql
-- 获取当前日期时间
SELECT NOW();

-- 获取当前日期
SELECT CURDATE();

-- 获取当前时间
SELECT CURTIME();

-- 提取日期的某个部分
SELECT YEAR(NOW());   -- 年
SELECT MONTH(NOW());  -- 月
SELECT DAY(NOW());    -- 日

-- 日期加减
SELECT DATE_ADD(NOW(), INTERVAL 1 DAY);      -- 明天
SELECT DATE_SUB(NOW(), INTERVAL 1 MONTH);    -- 上个月今天

-- 日期格式化
SELECT DATE_FORMAT(NOW(), '%Y年%m月%d日 %H:%i:%s');
```

### 条件函数

```sql
-- IF函数：类似Java的三元运算符
SELECT username, IF(age >= 18, '成年人', '未成年人') AS '身份' FROM users;

-- IFNULL函数：如果值为NULL就替换成指定值
SELECT IFNULL(email, '未填写') FROM users;

-- CASE WHEN：多条件判断
SELECT 
    username,
    CASE 
        WHEN age < 18 THEN '未成年'
        WHEN age < 30 THEN '青年'
        WHEN age < 60 THEN '中年'
        ELSE '老年'
    END AS '年龄段'
FROM users;
```

## 45.5 索引

### 什么是索引？

**索引（Index）** 是数据库为了加快查询速度而建立的数据结构。你可以把它想象成一本书的目录——没有目录你要翻完整本书才能找到想看的内容，有了目录直接翻到对应页码。

### 索引的工作原理

当你对一个字段建立索引后，数据库会为这个字段的值单独维护一个数据结构（通常是B+树），这个结构里的值是排序好的，并且每个值都指向对应的数据行。

查询的时候，数据库先在索引树里快速定位，然后直接跳转到目标数据行——不用一行一行去扫描了。

### 创建索引

```sql
-- 直接创建索引
CREATE INDEX idx_username ON users(username);

-- 给username和email建立联合索引
CREATE INDEX idx_user_info ON users(username, email);

-- 给email字段加唯一索引（既约束了唯一性，又提升了查询速度）
CREATE UNIQUE INDEX idx_email ON users(email);

-- 建表的时候直接指定索引
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    INDEX idx_username (username)  -- 在建表时创建索引
);
```

### 删除索引

```sql
DROP INDEX idx_username ON users;
```

### 索引的代价

天下没有免费的午餐，索引虽好，但也有代价：

1. **占用空间**：索引本身要占用磁盘空间
2. **拖慢写入**：INSERT、UPDATE、DELETE时要同时维护索引
3. **过度索引**：字段太少、数据量太小的时候，索引反而是累赘

> 最佳实践：只为**查询频繁**、**数据量大**、**区分度高**的字段建立索引。

### 何时使用索引？

```sql
-- 适合建索引的情况
SELECT * FROM users WHERE username = '张三';        -- 等值查询
SELECT * FROM users WHERE age > 18;                -- 范围查询
SELECT * FROM users WHERE username LIKE '张%';     -- 前缀模糊查询

-- 不适合建索引的情况
SELECT * FROM users WHERE email LIKE '%163.com';   -- 后缀模糊查询（用不上索引）
SELECT * FROM users WHERE gender = '男';           -- 区分度太低的字段
```

## 45.6 事务

### 什么是事务？

**事务（Transaction）** 是数据库管理系统执行过程中的一个逻辑单位，由一系列操作组成。一个事务内的所有操作要么全部成功，要么全部失败——没有中间状态。

打个比方：你去银行转账，从A账户转100块到B账户。这个过程实际上是两步：

1. A账户减100
2. B账户加100

如果第一步成功了但第二步失败了怎么办？A账户平白无故少了100块，这肯定不行！这时候就需要事务来保证：要么两步都成功，要么两步都回滚（撤销）。

### 事务的四大特性（ACID）

- **A**tomicity（原子性）：事务是最小执行单位，不可分割。要么全做，要么全不做。
- **C**onsistency（一致性）：事务执行前后，数据库状态必须保持一致。
- **I**solation（隔离性）：并发执行的事务相互隔离，不能互相干扰。
- **D**urability（持久性）：事务一旦提交，对数据库的改变就是永久性的。

### 事务的基本操作

```sql
-- 开启事务
START TRANSACTION;
-- 或者
BEGIN;

-- 执行操作
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- A账户减100
UPDATE accounts SET balance = balance + 100 WHERE id = 2;  -- B账户加100

-- 提交事务（所有操作正式生效）
COMMIT;

-- 回滚事务（撤销所有操作）
ROLLBACK;
```

### 并发问题与隔离级别

当多个事务同时操作同一批数据时，会产生各种问题：

| 问题 | 说明 |
|------|------|
| 脏读 | 读取到了其他事务未提交的数据 |
| 不可重复读 | 同一个事务中，两次读取同一行数据结果不同 |
| 幻读 | 同一个事务中，两次查询结果集不一致（多了或少了行） |

为了解决这些问题，SQL标准定义了4个隔离级别：

```sql
-- 查看当前隔离级别
SELECT @@tx_isolation;

-- 设置隔离级别
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|------------|------|
| READ UNCOMMITTED | 可能 | 可能 | 可能 |
| READ COMMITTED | 不可能 | 可能 | 可能 |
| REPEATABLE READ（MySQL默认） | 不可能 | 不可能 | 可能 |
| SERIALIZABLE | 不可能 | 不可能 | 不可能 |

> MySQL的InnoDB引擎在REPEATABLE READ级别下，通过MVCC（多版本并发控制）基本解决了幻读问题，所以通常不用把隔离级别调到最高的SERIALIZABLE。

### 实战例子

```sql
-- 模拟转账操作
START TRANSACTION;

UPDATE account SET balance = balance - 1000 WHERE id = 1 AND balance >= 1000;

-- 检查影响行数，如果为0说明余额不足
-- 这里用一个存储过程或者应用逻辑来检查
UPDATE account SET balance = balance + 1000 WHERE id = 2;

-- 两条UPDATE都成功了，提交
COMMIT;
-- 如果任何一步失败，执行ROLLBACK
```

## 45.7 JDBC编程步骤

终于到了Java和数据库"牵手"的时候了！**JDBC（Java Database Connectivity）** 是Java提供的数据库连接技术，是Java程序操作数据库的标准API。

### JDBC工作原理

JDBC采用**驱动管理器 + 数据库驱动**的模式。应用程序只需要调用JDBC API，而具体的数据库操作由对应的数据库驱动来完成。

```
Java程序 → JDBC API → JDBC驱动管理器 → 数据库驱动 → 数据库
```

### JDBC编程七步曲

#### 第一步：加载驱动

```java
// 方式一：手动加载驱动类（老派写法）
Class.forName("com.mysql.cj.jdbc.Driver");

// 方式二：从JDBC 4.0开始，MySQL驱动支持自动加载
// 只需要把驱动jar包放到classpath里就行
```

#### 第二步：建立连接

```java
// 数据库连接地址
String url = "jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=Asia/Shanghai";
String username = "root";
String password = "123456";

// 建立连接
Connection conn = DriverManager.getConnection(url, username, password);
```

#### 第三步：创建语句对象

```java
// 创建普通SQL语句对象
Statement stmt = conn.createStatement();

// 创建预编译SQL语句对象（推荐，防止SQL注入）
String sql = "SELECT * FROM users WHERE id = ?";
PreparedStatement pstmt = conn.prepareStatement(sql);
pstmt.setInt(1, 1);  // 第一个问号的值设为1
```

#### 第四步：执行SQL

```java
// 执行查询，返回ResultSet
ResultSet rs = pstmt.executeQuery();

// 执行增删改，返回影响的行数
int rows = stmt.executeUpdate("INSERT INTO users (username) VALUES ('张三')");
```

#### 第五步：处理结果

```java
// 遍历ResultSet
while (rs.next()) {
    int id = rs.getInt("id");           // 按列名获取
    String name = rs.getString(2);      // 按列索引获取（从1开始）
    
    System.out.println("用户ID: " + id + ", 用户名: " + name);
}
```

#### 第六步：关闭资源

```java
// 按照后创建先关闭的原则，依次关闭
if (rs != null) rs.close();
if (stmt != null) stmt.close();
if (conn != null) conn.close();
```

### 完整示例

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class JdbcDemo {
    
    public static void main(String[] args) {
        // 数据库配置
        String url = "jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=Asia/Shanghai";
        String user = "root";
        String password = "123456";
        
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        
        try {
            // 第一步：加载驱动（MySQL 8.x）
            Class.forName("com.mysql.cj.jdbc.Driver");
            
            // 第二步：建立连接
            conn = DriverManager.getConnection(url, user, password);
            System.out.println("数据库连接成功！");
            
            // 第三步：创建预编译SQL语句
            String sql = "SELECT * FROM users WHERE age > ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setInt(1, 18);  // 查询18岁以上的用户
            
            // 第四步：执行查询
            rs = pstmt.executeQuery();
            
            // 第五步：处理结果
            System.out.println("查询结果：");
            while (rs.next()) {
                int id = rs.getInt("id");
                String username = rs.getString("username");
                String email = rs.getString("email");
                int age = rs.getInt("age");
                System.out.printf("ID: %d, 用户名: %s, 邮箱: %s, 年龄: %d%n", 
                                  id, username, email, age);
            }
            
        } catch (ClassNotFoundException e) {
            System.out.println("驱动类找不到！" + e.getMessage());
        } catch (SQLException e) {
            System.out.println("数据库操作出错！" + e.getMessage());
        } finally {
            // 第六步：关闭资源（重要！防止连接泄漏）
            try {
                if (rs != null) rs.close();
                if (pstmt != null) pstmt.close();
                if (conn != null) conn.close();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### 使用try-with-resources简化关闭操作

从Java 7开始，你可以用try-with-resources来自动关闭资源：

```java
String url = "jdbc:mysql://localhost:3306/mydb?useSSL=false&serverTimezone=Asia/Shanghai";
String sql = "SELECT * FROM users WHERE age > ?";

try (Connection conn = DriverManager.getConnection(url, "root", "123456");
     PreparedStatement pstmt = conn.prepareStatement(sql)) {
    
    pstmt.setInt(1, 18);
    
    try (ResultSet rs = pstmt.executeQuery()) {
        while (rs.next()) {
            System.out.println(rs.getString("username"));
        }
    }
    
} catch (SQLException e) {
    e.printStackTrace();
}
// 无需手动关闭，资源会自动释放
```

### 增删改操作示例

```java
// 插入数据
public int insertUser(String username, String email, int age) {
    String sql = "INSERT INTO users (username, email, age) VALUES (?, ?, ?)";
    
    try (Connection conn = getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {
        
        pstmt.setString(1, username);
        pstmt.setString(2, email);
        pstmt.setInt(3, age);
        
        return pstmt.executeUpdate();  // 返回影响的行数
        
    } catch (SQLException e) {
        e.printStackTrace();
        return 0;
    }
}

// 更新数据
public int updateUserAge(int id, int newAge) {
    String sql = "UPDATE users SET age = ? WHERE id = ?";
    
    try (Connection conn = getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {
        
        pstmt.setInt(1, newAge);
        pstmt.setInt(2, id);
        
        return pstmt.executeUpdate();
        
    } catch (SQLException e) {
        e.printStackTrace();
        return 0;
    }
}

// 删除数据
public int deleteUser(int id) {
    String sql = "DELETE FROM users WHERE id = ?";
    
    try (Connection conn = getConnection();
         PreparedStatement pstmt = conn.prepareStatement(sql)) {
        
        pstmt.setInt(1, id);
        return pstmt.executeUpdate();
        
    } catch (SQLException e) {
        e.printStackTrace();
        return 0;
    }
}
```

---

## 本章小结

本章我们学习了SQL与数据库的基础知识，主要包括：

1. **SQL基础**：了解了SQL是什么、它的门派分支（MySQL、Oracle等），以及基本的语法规则。
2. **表操作**：掌握了CREATE TABLE创建表、ALTER TABLE修改表、DROP TABLE删除表的用法，以及主键、唯一约束、默认值等概念。
3. **查询**：深入学习了SELECT的各种用法，包括条件查询、排序、分页、聚合函数、分组查询、多表连接和子查询。
4. **函数**：了解了字符串函数、数值函数、日期函数和条件函数的使用。
5. **索引**：理解了索引的工作原理、创建与删除方法，以及索引的适用场景和注意事项。
6. **事务**：掌握了事务的ACID特性、开启/提交/回滚操作，以及并发问题和隔离级别。
7. **JDBC编程**：学习了Java通过JDBC操作数据库的完整步骤，包括加载驱动、建立连接、创建语句、执行SQL、处理结果和关闭资源。

数据库是现代软件开发不可或缺的一部分。无论是Web应用、企业系统还是移动后台，都离不开数据的存储与管理。学好SQL和JDBC，就等于掌握了与数据打交道的基本功。

> 记住：程序员的三大浪漫——操作系统、编译原理、数据库。你已经解锁了第三项，接下来继续加油吧！
