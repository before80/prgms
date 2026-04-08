+++
title = "第30章 SQL基础"
weight = 300
date = "2026-04-08T13:22:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第三十章：SQL 基础 —— 数据库界的"普通话"

> 想象一下，如果你去世界各国旅游，每到一个国家就得学一门新语言，那是多么崩溃的一件事。好在数据库界有一位"语言天才"——SQL，它就是数据库世界里的普通话，让你能和 MySQL、PostgreSQL、SQLite 这些"来自不同国家的人"愉快聊天。

## 30.1 数据库基础

### 30.1.1 数据库类型（关系型 vs 非关系型）

在数据库的江湖里，主要分为两大门派：**关系型数据库**（Relational Database）和**非关系型数据库**（NoSQL Database）。

**关系型数据库**就像是Excel表格的"豪华升级版"——数据以**表（Table）**的形式存储，表和表之间可以通过**外键（Foreign Key）**建立关系。比如一个"学生"表和一个"成绩"表，通过学生ID把它们关联起来，这就是关系型数据库的核心思想。

**非关系型数据库**则更加随性自由，数据存储格式灵活多变。常见的类型有：
- **键值存储**（Key-Value）：比如 Redis，像一本超级快的字典
- **文档数据库**（Document）：比如 MongoDB，数据以 JSON 文档形式存储
- **列式数据库**（Column-family）：比如 Cassandra，适合处理海量数据
- **图数据库**（Graph）：比如 Neo4j，专门处理"关系"数据，比如朋友圈的好友关系

```
┌─────────────────────────────────────────────────────────────────┐
│                        数据库的"江湖门派"                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────┐         ┌─────────────────────┐       │
│   │    关系型数据库        │         │    非关系型数据库      │       │
│   │  (Relational DB)     │         │    (NoSQL)          │       │
│   ├─────────────────────┤         ├─────────────────────┤       │
│   │  📊 表格式存储         │         │  📄 文档存储          │       │
│   │  🔗 表间可关联         │         │  🔑 键值对存储        │       │
│   │  ✅ ACID 事务支持      │         │  ⚡ 高性能高并发       │       │
│   │                      │         │  📈 水平扩展方便       │       │
│   │  代表：MySQL          │         │  代表：MongoDB       │       │
│   │       PostgreSQL     │         │         Redis       │       │
│   │       SQLite         │         │         Cassandra   │       │
│   └─────────────────────┘         └─────────────────────┘       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

> **小贴士**：想象关系型数据库是一张精心规划的Excel表，每个格子都有固定的位置；而非关系型数据库更像是一堆随意堆放的JSON文件，灵活性max，但找东西可能得靠"缘分"。

### 30.1.2 MySQL / PostgreSQL / SQLite / MongoDB 介绍

**MySQL** —— 数据库界的"老大哥"
- 诞生于1995年，绝对的"70后"
- 开源免费（被Oracle收购后有社区版）
- 速度快，体积小，是Web开发的首选
- 配上phpMyAdmin，就是新手入门数据库的首选装备
- "我最快！我最轻！！我跑Web最稳！！！"

**PostgreSQL** —— 数据库界的"学院派"
- 号称"世界上最先进的开源关系型数据库"
- 支持面向对象特性（比如自定义类型）
- 支持JSON数据存储（是的，它跨界了！）
- 事务处理能力超强，ACID原则执行得一丝不苟
- "我不只是关系型，我还能面向对象！"

**SQLite** —— 数据库界的"便携小钢炮"
- 整个数据库就是一个`.db`文件，极其轻便
- 零配置，无需安装服务，直接能用
- 手机App内置数据库的首选（你微信的聊天记录就是SQLite存的）
- Python标准库直接内置支持！
- "别看我小，五脏俱全！"

**MongoDB** —— 数据库界的"JSON狂魔"
- 文档型数据库，数据以BSON（类JSON）格式存储
- 表结构灵活到没有结构，想存什么存什么
- 适合快速原型开发和海量数据存储
- "我就是不喜欢被表格束缚！"

```
┌─────────────────────────────────────────────────────────────────┐
│                      四大数据库"门派"各有绝活                        │
├──────────┬────────────┬────────────┬────────────┬──────────────┤
│   特性    │   MySQL    │ PostgreSQL │   SQLite   │   MongoDB    │
├──────────┼────────────┼────────────┼────────────┼──────────────┤
│   类型    │  关系型     │   关系型    │   关系型    │   非关系型    │
│   诞生年   │  1995     │   1996     │   2000     │   2009      │
│   体积    │  中等      │   中等      │   极小     │   中等       │
│   事务    │  支持      │   强力支持  │   支持     │   支持（弱）   │
│   适合场景 │  Web网站   │  企业级/复杂 │  嵌入式/移动 │  大数据/灵活  │
│   学习难度 │  ⭐⭐      │   ⭐⭐⭐    │   ⭐       │   ⭐⭐       │
└──────────┴────────────┴────────────┴────────────┴──────────────┘
```

## 30.2 SQL 基础

> SQL（Structured Query Language）发音通常是"S-Q-L"或者"sequel"。它就是你和数据库"对话"的语言。学会SQL，就像学会了和数据库公主跳舞——你得先伸手（SELECT），她才知道你要干嘛。

### 30.2.1 SELECT / WHERE / ORDER BY

**SELECT** —— 数据库的"点菜"环节
- 作用：从数据库中"挑选"出你想要的数据
- `SELECT *` 表示"给我全部"（星号是万能通配符）
- 可以指定列名，只挑你需要的

**WHERE** —— 数据库的"筛选器"
- 作用：设置条件，只返回符合条件的记录
- 常用运算符：`=`（等于）、`>`（大于）、`<`（小于）、`>=`、`<=`、`!=`（不等于）

**ORDER BY** —— 数据库的"排序功能"
- 作用：对结果进行排序
- `ASC` 升序（从小到大，默认）
- `DESC` 降序（从大到小）

```sql
-- 创建一个"学生成绩表"来练习
CREATE TABLE students (
    id INTEGER PRIMARY KEY,    -- 学号，主键（唯一标识）
    name TEXT,                  -- 姓名
    age INTEGER,                -- 年龄
    score INTEGER                -- 成绩
);

-- 插入几条测试数据
INSERT INTO students (id, name, age, score) VALUES
    (1, '小明', 18, 95),
    (2, '小红', 17, 88),
    (3, '小强', 19, 72),
    (4, '小华', 18, 91),
    (5, '小李', 20, 85);

-- SELECT：查询所有学生
SELECT * FROM students;

-- SELECT：只查姓名和成绩
SELECT name, score FROM students;

-- WHERE：筛选成绩大于90的学生
SELECT * FROM students WHERE score > 90;

-- WHERE：筛选年龄等于18的学生
SELECT * FROM students WHERE age = 18;

-- ORDER BY：按成绩降序排列
SELECT * FROM students ORDER BY score DESC;

-- 组合技：WHERE + ORDER BY
SELECT name, score FROM students WHERE score >= 85 ORDER BY score DESC;
```

```sql
-- 查询结果示例：

-- SELECT * FROM students;
-- ┌────┬────────┬─────┬───────┐
-- │ id │  name  │ age │ score │
-- ├────┼────────┼─────┼───────┤
-- │  1 │  小明  │  18 │   95  │
-- │  2 │  小红  │  17 │   88  │
-- │  3 │  小强  │  19 │   72  │
-- │  4 │  小华  │  18 │   91  │
-- │  5 │  小李  │  20 │   85  │
-- └────┴────────┴─────┴───────┘

-- SELECT name, score FROM students;
-- ┌────────┬───────┐
-- │  name  │ score │
-- ├────────┼───────┤
-- │  小明  │   95  │
-- │  小红  │   88  │
-- │  小强  │   72  │
-- │  小华  │   91  │
-- │  小李  │   85  │
-- └────────┴───────┘

-- SELECT * FROM students WHERE score > 90;
-- ┌────┬────────┬─────┬───────┐
-- │ id │  name  │ age │ score │
-- ├────┼────────┼─────┼───────┤
-- │  1 │  小明  │  18 │   95  │
-- │  4 │  小华  │  18 │   91  │
-- └────┴────────┴─────┴───────┘

-- SELECT name, score FROM students WHERE score >= 85 ORDER BY score DESC;
-- ┌────────┬───────┐
-- │  name  │ score │
-- ├────────┼───────┤
-- │  小明  │   95  │
-- │  小华  │   91  │
-- │  小红  │   88  │
-- │  小李  │   85  │
-- └────────┴───────┘
```

### 30.2.2 DISTINCT / LIMIT

**DISTINCT** —— 数据库的"去重神器"
- 作用：去除查询结果中的重复记录
- 就像你妈让你去超市买"不重复"的菜一样

**LIMIT** —— 数据库的"截断小能手"
- 作用：限制返回记录的数量
- 分页查询的必备神器

```sql
-- 先插入一些重复数据来演示
INSERT INTO students (name, age, score) VALUES
    ('小王', 18, 85),
    ('小张', 18, 92);

-- DISTINCT：查询所有不重复的年龄
SELECT DISTINCT age FROM students;

-- DISTINCT：查询不重复的(年龄, 成绩)组合
SELECT DISTINCT age, score FROM students;

-- LIMIT：查询成绩前三名的学生
SELECT * FROM students ORDER BY score DESC LIMIT 3;

-- LIMIT + OFFSET：跳过前2条，取接下来的3条（分页第二页）
SELECT * FROM students ORDER BY id LIMIT 3 OFFSET 2;
```

```sql
-- 查询结果示例：

-- SELECT DISTINCT age FROM students;
-- ┌─────┐
-- │ age │
-- ├─────┤
-- │  17 │
-- │  18 │
-- │  19 │
-- │  20 │
-- └─────┘

-- SELECT * FROM students ORDER BY score DESC LIMIT 3;
-- ┌────┬────────┬─────┬───────┐
-- │ id │  name  │ age │ score │
-- ├────┼────────┼─────┼───────┤
-- │  1 │  小明  │  18 │   95  │
-- │  7 │  小张  │  18 │   92  │  （假设小张id=7）
-- │  4 │  小华  │  18 │   91  │
-- └────┴────────┴─────┴───────┘

-- SELECT * FROM students ORDER BY id LIMIT 3 OFFSET 2;
-- ┌────┬────────┬─────┬───────┐
-- │ id │  name  │ age │ score │
-- ├────┼────────┼─────┼───────┤
-- │  3 │  小强  │  19 │   72  │
-- │  4 │  小华  │  18 │   91  │
-- │  5 │  小李  │  20 │   85  │
-- └────┴────────┴─────┴───────┘
-- （跳过前2条，从第3条开始取3条，即 id=3,4,5 的记录）
```

> **趣味记忆**：DISTINCT 就是"我只要独一无二的你"，LIMIT 就是"适可而止，见好就收"。

### 30.2.3 INSERT / UPDATE / DELETE

这三位是数据库的"写操作三剑客"——增删改，都是危险动作！现实数据库中，**删除操作一定要三思而后行**，否则"删库到跑路"可不是开玩笑的。

**INSERT** —— 插入新数据
- 方式1：指定列名插入
- 方式2：批量插入

**UPDATE** —— 更新数据
- **必须配合 WHERE 条件！** 否则会把整张表都更新了！
- 这是新手最容易踩的坑

**DELETE** —— 删除数据
- **必须配合 WHERE 条件！** 否则会清空整张表！
- 删除的数据"理论上"可以恢复（如果有备份），但别抱太大希望

```sql
-- INSERT：插入一条新学生记录
INSERT INTO students (name, age, score) VALUES ('小刘', 19, 78);

-- INSERT：一次性插入多条记录（批量插入）
INSERT INTO students (name, age, score) VALUES
    ('小陈', 20, 82),
    ('小周', 18, 90),
    ('小吴', 17, 76);

-- UPDATE：把"小刘"的成绩更新为80
UPDATE students SET score = 80 WHERE name = '小刘';

-- UPDATE：把18岁学生的成绩都加5分（危险操作！没有WHERE试试？）
UPDATE students SET score = score + 5 WHERE age = 18;

-- DELETE：删除成绩低于75的学生
DELETE FROM students WHERE score < 75;

-- DELETE：删除所有数据（超级危险！千万别在生产库执行！）
-- DELETE FROM students;  -- 此处暂不执行，否则后续示例将无数据可查
```

```sql
-- 查询结果示例：

-- INSERT INTO students (name, age, score) VALUES ('小刘', 19, 78);
-- 执行成功，返回：1 row affected

-- UPDATE students SET score = 80 WHERE name = '小刘';
-- 执行成功，返回：1 row affected

-- UPDATE students SET score = score + 5 WHERE age = 18;
-- 执行成功，返回：3 rows affected（假设有3个18岁的学生）

-- DELETE FROM students WHERE score < 75;
-- 执行成功，返回：2 rows deleted
```

> **血的教训**：有一次我写 `UPDATE students SET score = 0` 忘了加 WHERE，结果...那天的午饭突然就不香了。所以，**写 UPDATE 和 DELETE 之前，先用 SELECT 确认影响范围**！

## 30.3 聚合与分组

> 聚合函数就像是Excel里的SUM、COUNT、AVG那些函数，只不过SQL版的更专业、更强大。

### 30.3.1 COUNT / SUM / AVG / MAX / MIN

**COUNT()** —— 数数有几条
- `COUNT(*)`：计算所有记录数，包括NULL
- `COUNT(列名)`：计算该列非空记录数

**SUM()** —— 求和
- 计算某列数值的总和

**AVG()** —— 求平均值
- 计算某列的平均值

**MAX() / MIN()** —— 最大值/最小值
- 找出某列的最大值或最小值

```sql
-- 先看看原始数据
SELECT * FROM students;

-- COUNT：统计学生总数
SELECT COUNT(*) FROM students;

-- COUNT：统计有成绩的学生数量
SELECT COUNT(score) FROM students;

-- SUM：计算所有学生成绩的总和
SELECT SUM(score) FROM students;

-- AVG：计算学生成绩的平均值
SELECT AVG(score) FROM students;

-- MAX：找出最高分
SELECT MAX(score) FROM students;

-- MIN：找出最低分
SELECT MIN(score) FROM students;

-- 组合使用：同时查看平均分、最高分、最低分
SELECT 
    COUNT(*) as 学生总数,
    AVG(score) as 平均分,
    MAX(score) as 最高分,
    MIN(score) as 最低分
FROM students;
```

```sql
-- 查询结果示例：

-- SELECT COUNT(*) FROM students;
-- ┌──────────┐
-- │ COUNT(*) │
-- ├──────────┤
-- │    10    │   （假设有10个学生）
-- └──────────┘

-- SELECT AVG(score) FROM students;
-- ┌────────────┐
-- │ AVG(score) │
-- ├────────────┤
-- │   85.4     │
-- └────────────┘

-- SELECT COUNT(*) as 学生总数, AVG(score) as 平均分, MAX(score) as 最高分, MIN(score) as 最低分 FROM students;
-- ┌──────────┬──────────┬──────────┬──────────┐
-- │ 学生总数  │  平均分   │  最高分   │  最低分   │
-- ├──────────┼──────────┼──────────┼──────────┤
-- │    10    │   85.4   │    98    │    65    │
-- └──────────┴──────────┴──────────┴──────────┘
```

### 30.3.2 GROUP BY / HAVING

**GROUP BY** —— 分组大师
- 作用：把数据按某个字段分组
- 通常配合聚合函数使用

**HAVING** —— 分组后的筛选器
- WHERE 是筛选"原始数据"
- HAVING 是筛选"分组后的结果"
- HAVING 必须和 GROUP BY 一起用

```sql
-- GROUP BY：按年龄分组，统计每个年龄的学生数量和平均分
SELECT 
    age as 年龄,
    COUNT(*) as 人数,
    AVG(score) as 平均分
FROM students
GROUP BY age;

-- GROUP BY + HAVING：筛选平均分大于85的年龄组
SELECT 
    age as 年龄,
    COUNT(*) as 人数,
    AVG(score) as 平均分
FROM students
GROUP BY age
HAVING AVG(score) > 85;

-- 完整的聚合查询模板
SELECT 
    列1,
    聚合函数(列2) as 别名
FROM 表名
WHERE 条件          -- 筛选原始数据
GROUP BY 列1        -- 按列1分组
HAVING 聚合条件      -- 筛选分组结果
ORDER BY 列3 DESC;  -- 排序
```

```sql
-- 查询结果示例：

-- SELECT age, COUNT(*), AVG(score) FROM students GROUP BY age;
-- ┌──────┬──────────┬────────────┐
-- │ age  │ COUNT(*) │ AVG(score) │
-- ├──────┼──────────┼────────────┤
-- │  17  │    2     │   82.0     │
-- │  18  │    4     │   89.5     │
-- │  19  │    2     │   78.5     │
-- │  20  │    2     │   84.0     │
-- └──────┴──────────┴────────────┘

-- SELECT age, COUNT(*), AVG(score) FROM students GROUP BY age HAVING AVG(score) > 85;
-- ┌──────┬──────────┬────────────┐
-- │ age  │ COUNT(*) │ AVG(score) │
-- ├──────┼──────────┼────────────┤
-- │  18  │    4     │   89.5     │
-- └──────┴──────────┴────────────┘
```

> **记忆口诀**：WHERE是"先筛选后分组"，HAVING是"先分组后筛选"。就像你妈让你"先洗碗再吃饭"和"先吃饭再洗碗"，顺序不同，结果完全不同！

## 30.4 表连接

> 表连接是SQL的精髓所在！想象一下，你有两张表：一张是"学生表"（有姓名和班级ID），一张是"班级表"（有班级名和教室号）。连接就是把它们"拼"在一起，让你看到"小明在哪个教室上课"这种信息。

```
┌─────────────────────────────────────────────────────────────────┐
│                    表连接的"拼图游戏"                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   学生表                          班级表                         │
│  ┌────┬────────┬─────┐      ┌────┬────────┬────────┐           │
│  │ id │  name  │cls_id│     │cls_id│cls_name│ room  │           │
│  ├────┼────────┼─────┤      ├────┼────────┼────────┤           │
│  │ 1  │  小明  │ 101  │◄────►│ 101 │  1班   │  A101  │           │
│  │ 2  │  小红  │ 102  │◄────►│ 102 │  2班   │  A102  │           │
│  │ 3  │  小强  │ 101  │◄────►│ 103 │  3班   │  A103  │           │
│  └────┴────────┴─────┘      └────┴────────┴────────┘           │
│         │                           │                          │
│         └─────────── JOIN ───────────┘                          │
│                        │                                        │
│                        ▼                                        │
│               ┌────────────────┐                                 │
│               │  连接的表结果    │                                 │
│               └────────────────┘                                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 30.4.1 INNER JOIN

**INNER JOIN（内连接）** —— 最常见的连接方式
- 只返回两个表中**匹配成功**的记录
- 一边有、一边没有的数据，直接"丢掉"

```sql
-- 创建学生表和班级表
CREATE TABLE classes (
    cls_id INTEGER PRIMARY KEY,
    cls_name TEXT,
    room TEXT
);

INSERT INTO classes (cls_id, cls_name, room) VALUES
    (101, 'Python入门班', 'A101'),
    (102, 'Web开发班', 'A102'),
    (103, '数据分析班', 'B201'),
    (104, 'UI设计班', 'B301');

CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    cls_id INTEGER
);

INSERT INTO students (id, name, cls_id) VALUES
    (1, '小明', 101),
    (2, '小红', 102),
    (3, '小强', 101),
    (4, '小华', 104),      -- 注意：104不在classes表中！
    (5, '小李', 103);

-- INNER JOIN：只返回两边都有的记录
SELECT 
    students.name as 学生姓名,
    classes.cls_name as 班级名称,
    classes.room as 教室
FROM students
INNER JOIN classes ON students.cls_id = classes.cls_id;

-- 简写形式（用逗号分隔表，用WHERE指定连接条件）
SELECT 
    s.name as 学生姓名,
    c.cls_name as 班级名称,
    c.room as 教室
FROM students s, classes c
WHERE s.cls_id = c.cls_id;
```

```sql
-- 查询结果示例：

-- SELECT students.name, classes.cls_name, classes.room FROM students INNER JOIN classes ON students.cls_id = classes.cls_id;
-- ┌────────────┬──────────────┬────────┐
-- │ 学生姓名   │   班级名称     │  教室  │
-- ├────────────┼──────────────┼────────┤
-- │   小明     │  Python入门班  │  A101  │
-- │   小红     │   Web开发班    │  A102  │
-- │   小强     │  Python入门班  │  A101  │
-- │   小华     │   UI设计班    │  B301  │
-- │   小李     │   数据分析班   │  B201  │
-- └────────────┴──────────────┴────────┘
```

### 30.4.2 LEFT JOIN / RIGHT JOIN / FULL JOIN

**LEFT JOIN（左连接）** —— 左边表的数据"全保留"
- 即使右表没有匹配，也返回左表的全部记录
- 右表没匹配上的显示NULL（空）

**RIGHT JOIN（右连接）** —— 右边表的数据"全保留"
- 即使左表没有匹配，也返回右表的全部记录

**FULL JOIN（全连接）** —— 两边都保留
- 相当于 LEFT JOIN + RIGHT JOIN
- 任何一边没匹配上的都用NULL填充

```sql
-- LEFT JOIN：保留所有学生，即使他没有班级
SELECT 
    students.name as 学生姓名,
    classes.cls_name as 班级名称,
    classes.room as 教室
FROM students
LEFT JOIN classes ON students.cls_id = classes.cls_id;

-- RIGHT JOIN：保留所有班级，即使没有学生
SELECT 
    students.name as 学生姓名,
    classes.cls_name as 班级名称,
    classes.room as 教室
FROM students
RIGHT JOIN classes ON students.cls_id = classes.cls_id;

-- FULL JOIN：两边都保留
SELECT 
    students.name as 学生姓名,
    classes.cls_name as 班级名称,
    classes.room as 教室
FROM students
FULL JOIN classes ON students.cls_id = classes.cls_id;
```

```sql
-- 查询结果示例：

-- LEFT JOIN 结果：
-- ┌────────────┬──────────────┬────────┐
-- │ 学生姓名   │   班级名称     │  教室  │
-- ├────────────┼──────────────┼────────┤
-- │   小明     │  Python入门班  │  A101  │
-- │   小红     │   Web开发班    │  A102  │
-- │   小强     │  Python入门班  │  A101  │
-- │   小华     │   UI设计班    │  B301  │
-- │   小李     │   数据分析班   │  B201  │
-- └────────────┴──────────────┴────────┘

-- RIGHT JOIN 结果：
-- ┌────────────┬──────────────┬────────┐
-- │ 学生姓名   │   班级名称     │  教室  │
-- ├────────────┼──────────────┼────────┤
-- │   小明     │  Python入门班  │  A101  │
-- │   小红     │   Web开发班    │  A102  │
-- │   小强     │  Python入门班  │  A101  │
-- │   小华     │   UI设计班    │  B301  │
-- │   小李     │   数据分析班   │  B201  │
-- └────────────┴──────────────┴────────┘
```

> **记忆小技巧**：LEFT JOIN 就像左撇子坚持用左手——"不管右边有没有，我都保留左边"。

### 30.4.3 CROSS JOIN

**CROSS JOIN（交叉连接）** —— 笛卡尔积
- 左表的每一行都和右表的每一行组合
- 结果数量 = 左表行数 × 右表行数
- 相亲网站的"全员匹配"模式！

```sql
-- CROSS JOIN：所有学生和所有班级的组合
SELECT 
    students.name as 学生姓名,
    classes.cls_name as 班级名称
FROM students
CROSS JOIN classes;
```

```sql
-- 查询结果示例：
-- （5个学生 × 4个班级 = 20条记录）
-- ┌────────────┬──────────────┐
-- │ 学生姓名   │   班级名称    │
-- ├────────────┼──────────────┤
-- │   小明     │  Python入门班 │
-- │   小明     │   Web开发班   │
-- │   小明     │   数据分析班  │
-- │   小红     │  Python入门班  │
-- │   小红     │   Web开发班   │
-- │   小红     │   数据分析班  │
-- │   小强     │  Python入门班  │
-- │   小强     │   Web开发班   │
-- │   小强     │   数据分析班  │
-- │   ...      │     ...      │
-- └────────────┴──────────────┘
-- 小明可以同时上所有课！（当然，这只是理论上的）
```

> **警告**：CROSS JOIN 在小表上是无害的"实验"，但在大表上可能是"灾难"——两个10万行的表做CROSS JOIN会生成10亿行数据！

## 30.5 子查询与视图

> 子查询就是"查询里的查询"，就像俄罗斯套娃，一层套一层。视图则是数据库的"美颜滤镜"，把复杂的查询封装起来，随时调用。

### 30.5.1 标量子查询

**标量子查询** —— 返回单个值的子查询
- 出现在 SELECT、WHERE 等需要单个值的地方
- 必须返回且只能返回一行一列

```sql
-- 查询比平均分高的学生
SELECT name, score 
FROM students 
WHERE score > (SELECT AVG(score) FROM students);

-- 查询成绩最高的学生姓名
SELECT name 
FROM students 
WHERE score = (SELECT MAX(score) FROM students);

-- 查询每个学生与平均分的差值
SELECT 
    name,
    score,
    score - (SELECT AVG(score) FROM students) as 与平均分差值
FROM students;
```

```sql
-- 查询结果示例：

-- SELECT name, score FROM students WHERE score > (SELECT AVG(score) FROM students);
-- ┌────────┬───────┐
-- │  name  │ score │
-- ├────────┼───────┤
-- │  小明  │   95  │
-- │  小华  │   91  │
-- └────────┴───────┘

-- SELECT name, score, score - (SELECT AVG(score) FROM students) as 与平均分差值 FROM students;
-- ┌────────┬───────┬──────────────┐
-- │  name  │ score │ 与平均分差值   │
-- ├────────┼───────┼──────────────┤
-- │  小明  │   95  │    +9.6      │
-- │  小红  │   88  │    +2.6      │
-- │  小强  │   72  │   -13.4      │
-- │  小华  │   91  │    +5.6      │
-- │  小李  │   85  │    -0.4      │
-- └────────┴───────┴──────────────┘
```

### 30.5.2 表子查询

**表子查询** —— 返回整张表的子查询
- 放在 FROM 后面作为临时表
- 放在 IN/EXISTS 后面作为条件

```sql
-- 查询成绩大于85分的学生（作为临时表）
SELECT * FROM (
    SELECT name, score FROM students WHERE score > 85
) AS high_scores;

-- 查询报了"Python入门班"的学生姓名（用IN）
SELECT name FROM students 
WHERE cls_id IN (
    SELECT cls_id FROM classes WHERE cls_name = 'Python入门班'
);

-- 查询与"小明"同班的学生
SELECT name FROM students 
WHERE cls_id IN (
    SELECT cls_id FROM students WHERE name = '小明'
);
```

```sql
-- 查询结果示例：

-- SELECT name FROM students WHERE cls_id IN (SELECT cls_id FROM classes WHERE cls_name = 'Python入门班');
-- ┌────────┐
-- │  name  │
-- ├────────┤
-- │  小明  │
-- │  小强  │
-- └────────┘
```

### 30.5.3 视图

**视图（View）** —— 虚拟表
- 基于真实表的查询结果"保存"为一个"虚拟表"
- 不存储真实数据，每次查询视图时实时计算
- 可以像操作表一样查询视图

```sql
-- 创建视图：成绩优秀的学生
CREATE VIEW excellent_students AS
SELECT 
    students.name,
    students.score,
    classes.cls_name
FROM students
INNER JOIN classes ON students.cls_id = classes.cls_id
WHERE students.score >= 90;

-- 查询视图（和查询表一样）
SELECT * FROM excellent_students;

-- 查看成绩优秀学生的人数
SELECT COUNT(*) FROM excellent_students;

-- 删除视图
DROP VIEW excellent_students;
```

```sql
-- 查询结果示例：

-- SELECT * FROM excellent_students;
-- ┌────────┬───────┬──────────────┐
-- │  name  │ score │  cls_name    │
-- ├────────┼───────┼──────────────┤
-- │  小明  │   95  │  Python入门班 │
-- │  小华  │   91  │  UI设计班    │
-- └────────┴───────┴──────────────┘
```

> **视图的优点**：
> 1. **简化复杂查询**：把100行的复杂SQL封装成视图，以后只需3行
> 2. **数据安全**：只暴露需要的列，不暴露敏感字段
> 3. **代码复用**：多处使用同一个查询逻辑，一改全改

## 30.6 Python 数据库操作

终于到Python环节了！学会了SQL，我们来看看怎么用Python操作数据库。

### 30.6.1 sqlite3（标准库）

Python的`sqlite3`是内置标准库，**无需安装任何第三方库**就能操作SQLite数据库！这就是"免费而且还送到家门口"的服务。

```python
import sqlite3

# 连接数据库（如果不存在会自动创建）
conn = sqlite3.connect('school.db')

# 创建游标（用于执行SQL语句）
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,      -- NOT NULL 表示不能为空
        age INTEGER,
        score INTEGER
    )
''')

# 插入数据
cursor.execute(
    'INSERT INTO students (name, age, score) VALUES (?, ?, ?)',
    ('小明', 18, 95)             # 使用参数化查询，防止SQL注入！
)
cursor.executemany(              # 批量插入
    'INSERT INTO students (name, age, score) VALUES (?, ?, ?)',
    [('小红', 17, 88), ('小强', 19, 72), ('小华', 18, 91)]
)

# 查询数据
cursor.execute('SELECT * FROM students')
rows = cursor.fetchall()         # 获取所有结果
for row in rows:
    print(f"学号: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 成绩: {row[3]}")

# 带参数的查询
cursor.execute('SELECT name, score FROM students WHERE score > ?', (85,))
results = cursor.fetchall()
print("成绩大于85的学生:", results)

# 更新数据
cursor.execute('UPDATE students SET score = ? WHERE name = ?', (90, '小强'))

# 删除数据
cursor.execute('DELETE FROM students WHERE score < ?', (80,))

# 提交事务（重要！不提交数据不会保存）
conn.commit()

# 关闭连接
conn.close()

# 打印结果
# 学号: 1, 姓名: 小明, 年龄: 18, 成绩: 95
# 学号: 2, 姓名: 小红, 年龄: 17, 成绩: 88
# 学号: 3, 姓名: 小强, 年龄: 19, 成绩: 72
# 学号: 4, 姓名: 小华, 年龄: 18, 成绩: 91
# 成绩大于85的学生: [('小明', 95), ('小红', 88), ('小华', 91)]
```

> **重要提醒**：Python操作数据库时，**一定要用参数化查询**（用`?`占位符），而不是字符串拼接！否则会被SQL注入攻击打得满地找牙。

### 30.6.2 SQLAlchemy（ORM）

**SQLAlchemy**是Python中最流行的ORM（Object Relational Mapping，对象关系映射）库。简单来说，它让你可以用**操作Python对象的方式**来操作数据库，而不用写SQL语句。

> **ORM是什么？** 想象一下，你是个不会说外语的人，但你有一个人肉翻译（ORM），你跟翻译说"给我来份宫保鸡丁"，翻译就帮你跟厨师说"来份宫保鸡丁"。ORM就是把Python语言"翻译"成SQL语言。

```python
# 安装：pip install sqlalchemy

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# 创建数据库连接（SQLite）
engine = create_engine('sqlite:///school.db', echo=True)
# echo=True 会打印所有SQL语句，方便调试

# 创建基类
Base = declarative_base()

# 定义模型类（就像定义Python类一样定义表）
class Student(Base):
    __tablename__ = 'students'          # 对应的表名
    
    id = Column(Integer, primary_key=True)      # 主键
    name = Column(String(50), nullable=False)   # 姓名，不能为空
    age = Column(Integer)                        # 年龄
    score = Column(Float)                        # 成绩
    
    def __repr__(self):
        return f"<Student(name='{self.name}', age={self.age}, score={self.score})>"

# 创建表（如果表已存在会报错，可以用 create_all）
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
session = Session()

# 插入数据
student1 = Student(name='小明', age=18, score=95.0)
student2 = Student(name='小红', age=17, score=88.0)
session.add(student1)        # 添加一个
session.add_all([student2])  # 批量添加
session.commit()             # 提交

# 查询数据（不用写SQL！）
# 查所有
all_students = session.query(Student).all()
for s in all_students:
    print(s)

# 条件查询
high_scorers = session.query(Student).filter(Student.score > 85).all()
print("高分学生:", high_scorers)

# 按分数排序
ordered = session.query(Student).order_by(Student.score.desc()).all()
print("按分数排序:", ordered)

# 更新数据
student = session.query(Student).filter(Student.name == '小明').first()
student.score = 96.0
session.commit()

# 删除数据
student = session.query(Student).filter(Student.name == '小红').first()
session.delete(student)
session.commit()

# 关闭会话
session.close()

# 打印结果
# <Student(name='小明', age=18, score=95.0)>
# <Student(name='小红', age=17, score=88.0)>
# 高分学生: [<Student(name='小明', age=18, score=95.0)>]
```

### 30.6.3 PyMySQL（MySQL 驱动）

**PyMySQL**是纯Python实现的MySQL驱动，特点是**纯Python实现**（不需要编译），安装简单，兼容性好。

> 如果你想连接MySQL数据库（比如阿里云、腾讯云的MySQL服务），PyMySQL是经典选择。

```python
# 安装：pip install pymysql

import pymysql

# 连接MySQL数据库
conn = pymysql.connect(
    host='localhost',           # 数据库地址
    port=3306,                  # 端口（默认3306）
    user='root',                # 用户名
    password='your_password',   # 密码（换成你的！）
    database='school',          # 数据库名
    charset='utf8mb4'           # 字符集（支持emoji）
)

# 创建游标
cursor = conn.cursor()

# 执行SQL（和sqlite3一样）
cursor.execute('SELECT VERSION()')
version = cursor.fetchone()
print(f"MySQL版本: {version[0]}")

# 插入数据
sql = 'INSERT INTO students (name, age, score) VALUES (%s, %s, %s)'
cursor.execute(sql, ('小王', 20, 85))
conn.commit()
print(f"插入成功，ID: {cursor.lastrowid}")

# 批量插入
data = [
    ('小赵', 19, 78),
    ('小钱', 18, 92),
    ('小孙', 20, 86)
]
cursor.executemany(sql, data)
conn.commit()
print(f"批量插入成功，影响行数: {cursor.rowcount}")

# 查询数据
cursor.execute('SELECT * FROM students WHERE score > %s', (80,))
results = cursor.fetchall()
for row in results:
    print(f"ID: {row[0]}, 姓名: {row[1]}, 年龄: {row[2]}, 成绩: {row[3]}")

# 关闭连接
cursor.close()
conn.close()

# 打印结果
# MySQL版本: 8.0.32
# 插入成功，ID: 1
# 批量插入成功，影响行数: 3
# ID: 1, 姓名: 小王, 年龄: 20, 成绩: 85.0
# ID: 3, 姓名: 小钱, 年龄: 18, 成绩: 92.0
```

> **连接池优化**：生产环境中，通常不会每次请求都创建新连接，而是使用**连接池**（Connection Pool）。PyMySQL本身不提供连接池，但可以配合`DBUtils`或`sqlalchemy`的连接池使用。

```
┌─────────────────────────────────────────────────────────────────┐
│                    Python数据库操作"三剑客"对比                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌───────────┬─────────────────────────────────────────────┐   │
│   │  sqlite3  │  ✅ Python内置，无需安装                      │   │
│   │           │  ✅ 零配置，直接可用                           │   │
│   │           │  ✅ 轻量级，适合学习和小型项目                   │   │
│   │           │  ❌ 不适合高并发                               │   │
│   ├───────────┼─────────────────────────────────────────────┤   │
│   │ SQLAlchemy│  ✅ ORM方式，代码优雅                          │   │
│   │           │  ✅ 支持多种数据库                              │   │
│   │           │  ✅ 防止SQL注入（自动转义）                      │   │
│   │           │  ⚠️ 有一定学习成本                              │   │
│   ├───────────┼─────────────────────────────────────────────┤   │
│   │  PyMySQL  │  ✅ 纯Python实现，安装简单                      │   │
│   │           │  ✅ 适合连接远程MySQL                           │   │
│   │           │  ❌ 需要配合连接池使用（生产环境）               │   │
│   └───────────┴─────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 本章小结

### 核心概念回顾

| 概念 | 说明 |
|------|------|
| **关系型数据库** | 数据以表格形式存储，表与表之间通过外键关联 |
| **SQL** | 数据库的"普通话"，用于与数据库交互 |
| **SELECT** | 查询数据，支持 WHERE 条件、ORDER BY 排序 |
| **聚合函数** | COUNT、SUM、AVG、MAX、MIN 用于统计计算 |
| **GROUP BY** | 分组，配合聚合函数使用，HAVING 筛选分组结果 |
| **JOIN** | 表连接，INNER JOIN 只保留匹配、LEFT/RIGHT JOIN 全保留某表 |
| **子查询** | 查询中的查询，分为标量子查询和表子查询 |
| **视图** | 虚拟表，基于真实表的查询封装 |

### 重点语法速记

```sql
-- 查询模板
SELECT 列 FROM 表 WHERE 条件 GROUP BY 列 HAVING 聚合条件 ORDER BY 列 LIMIT;

-- 连接模板
SELECT * FROM 表1 JOIN 表2 ON 连接条件;

-- Python操作数据库
import sqlite3
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()
cursor.execute('SELECT * FROM table')
conn.commit()
conn.close()
```

### 实战建议

1. **先 SELECT 确认，再 UPDATE/DELETE** —— 养成习惯，避免删库跑路
2. **使用参数化查询** —— 防止 SQL 注入攻击
3. **善用 LIMIT 分页** —— 大数据量查询一定要分页
4. **理解 JOIN 而非死记** —— 画个维恩图，连接类型就清楚了

> 恭喜你！读完本章，你已经掌握了数据库的核心技能。从增删改查到表连接，从子查询到视图，你已经是个"SQL小能手"了！接下来，继续在实践中打怪升级吧！ 🎉
