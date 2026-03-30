+++
title = "第38章 持久化框架——Java 与数据库对话"
weight = 380
date = "2026-03-30T14:33:56.923+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十八章 持久化框架——Java 与数据库对话

> 💡 **前置知识**：本章需要你懂一点 Java 基础（类、对象、接口），懂一点 SQL（SELECT、INSERT 之类的命令）。如果数据库对你来说只是个"存放数据的大仓库"，那本章正是帮你把这个仓库变成一条通畅的高速公路。

想象一下：你写了一个超棒的用户管理系统，用户数据存在数据库里。但问题是——Java 程序和数据库之间，隔着一层"语言不通"的墙。Java 说"我要找一个叫张三的用户"，数据库说"我只听得懂 `SELECT * FROM users WHERE name='张三'`"。

持久化框架，就是来解决这个"鸡同鸭讲"问题的。它们是 Java 和数据库之间的翻译官，只不过这些翻译官有的勤勤恳恳任劳任怨，有的则需要你手把手教它每一个单词。

本章我们就来认识三位翻译官：JDBC（野生翻译，自己查字典）、MyBatis（半驯化，会一些常用语）、JPA/Hibernate（完全驯化，你说个大概它就懂了）。

---

## 38.1 JDBC——自己动手，丰衣足食

### 38.1.1 什么是 JDBC

**JDBC**（Java Database Connectivity）是 Java 官方提供的数据库访问 API。它出现在 JDK 的 `java.sql` 和 `javax.sql` 两个包里，是 Java 与数据库通信的"原生协议"。

你可以把 JDBC 想象成：你拿着一本厚厚的《SQL 字典》，手动把每句中文翻译成 SQL，再把数据库返回的结果手动解析成 Java 对象。没有中间商赚差价，但也没有中间商帮你省事。

### 38.1.2 JDBC 的核心组件

JDBC 有几个你必须记住的核心角色：

- **DriverManager**：负责加载数据库驱动（比如 MySQL 的驱动、Oracle 的驱动），建立数据库连接。
- **Connection**：代表与数据库的一次会话连接，就像打电话建立的一条线路。
- **Statement / PreparedStatement**：负责发送 SQL 语句到数据库。
- **ResultSet**：封装查询结果，像一个游标（cursor）可以在结果集里来回移动。

### 38.1.3 第一个 JDBC 程序

废话少说，先看代码。下面的例子演示了如何用 JDBC 从数据库中查询用户信息：

```java
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

/**
 * JDBC 演示：查询用户信息
 * 使用 PreparedStatement 防止 SQL 注入（security best practice）
 */
public class JdbcDemo {

    // 数据库连接参数
    private static final String URL = "jdbc:mysql://localhost:3306/myapp?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASSWORD = "123456";

    public static void main(String[] args) {
        // SQL 查询语句：根据用户 ID 查询用户名和邮箱
        String sql = "SELECT id, username, email FROM users WHERE id = ?";

        // try-with-resources：自动关闭资源（Connection、PreparedStatement、ResultSet）
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement ps = conn.prepareStatement(sql)) {

            // 设置查询参数
            ps.setInt(1, 1);

            // 执行查询，返回 ResultSet
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("id");
                    String username = rs.getString("username");
                    String email = rs.getString("email");
                    System.out.println("用户ID: " + id + ", 用户名: " + username + ", 邮箱: " + email);
                }
            }

        } catch (SQLException e) {
            // SQL 异常：数据库连接失败、SQL 语法错误、约束冲突等
            System.err.println("数据库操作失败: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

> **小提示**：JDBC 要求你先在项目中放入数据库驱动（MySQL 用 `mysql-connector-java.jar`，Oracle 用 `ojdbc.jar`）。没有驱动，就像打电话却没有信号——什么都传不出去。

### 38.1.4 CRUD 操作演示

CRUD 是 Create（创建）、Read（读取）、Update（更新）、Delete（删除）的缩写。来看一个完整的 CRUD 示例：

```java
import java.sql.*;
import java.util.ArrayList;
import java.util.List;

/**
 * JDBC CRUD 完整演示
 */
public class JdbcCrudDemo {

    private static final String URL = "jdbc:mysql://localhost:3306/myapp?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root";
    private static final String PASSWORD = "123456";

    // ---------- C: 插入数据 ----------
    public int insertUser(String username, String email) {
        String sql = "INSERT INTO users(username, email) VALUES(?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement ps = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, username);
            ps.setString(2, email);
            int rows = ps.executeUpdate();
            if (rows > 0) {
                // 获取自增主键
                try (ResultSet rs = ps.getGeneratedKeys()) {
                    if (rs.next()) {
                        return rs.getInt(1); // 返回新插入记录的主键
                    }
                }
            }
        } catch (SQLException e) {
            System.err.println("插入失败: " + e.getMessage());
        }
        return -1;
    }

    // ---------- R: 查询数据 ----------
    public List<String[]> queryAllUsers() {
        List<String[]> users = new ArrayList<>();
        String sql = "SELECT username, email FROM users";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                users.add(new String[]{rs.getString("username"), rs.getString("email")});
            }
        } catch (SQLException e) {
            System.err.println("查询失败: " + e.getMessage());
        }
        return users;
    }

    // ---------- U: 更新数据 ----------
    public boolean updateUserEmail(int userId, String newEmail) {
        String sql = "UPDATE users SET email = ? WHERE id = ?";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, newEmail);
            ps.setInt(2, userId);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("更新失败: " + e.getMessage());
            return false;
        }
    }

    // ---------- D: 删除数据 ----------
    public boolean deleteUser(int userId) {
        String sql = "DELETE FROM users WHERE id = ?";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASSWORD);
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, userId);
            return ps.executeUpdate() > 0;
        } catch (SQLException e) {
            System.err.println("删除失败: " + e.getMessage());
            return false;
        }
    }
}
```

### 38.1.5 JDBC 的优点与缺点

| 优点 | 缺点 |
|------|------|
| 轻量级，无额外依赖 | 模板代码太多（连接、关闭、异常处理） |
| 完全可控，SQL 优化灵活 | 手动映射结果集到对象（大量 getter/setter） |
| 性能高，无额外开销 | 没有缓存，需要自己管理 SQL |
| 适合复杂业务和极致性能调优 | 数据库移植要改 SQL（因为各数据库 SQL 有差异） |

> **总结**：JDBC 就像自己做饭——可以完全按自己口味来，但每顿饭都要从买菜开始。适合对性能有极致要求、愿意写大量模板代码的开发者。

---

## 38.2 MyBatis——SQL 想怎么写，你说了算

### 38.2.1 什么是 MyBatis

**MyBatis** 是一款优秀的持久层框架，它支持自定义 SQL、存储过程以及高级映射。

如果说 JDBC 是"全手动挡"，那 MyBatis 就是"自动挡 + 手动模式可选"。你依然可以写 SQL（这对喜欢优化 SQL 的工程师来说是福音），但结果的映射工作——把数据库字段变成 Java 对象——MyBatis 帮你自动化了。

MyBatis 之前叫 iBatis，是 Apache 基金会的项目，后来迁移到 Google Code 并更名为 MyBatis。

### 38.2.2 MyBatis 架构图

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│                  (Your Java Code)                         │
└────────────────────────┬────────────────────────────────┘
                         │
                    SqlSession
                         │
          ┌──────────────┼──────────────┐
          │              │              │
      Executor      StatementHandler  ResultHandler
          │              │              │
    ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
    │  Simple   │   │ Prepared  │   │  Result   │
    │  Executor │   │  Statement│   │   Set     │
    │  Reuse    │   │  Handler  │   │  Handler  │
    │  Executor │   │           │   │           │
    └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
          │              │              │
          └──────────────┼──────────────┘
                         │
              ┌──────────┴──────────┐
              │   JDBC (Driver)     │
              │  mysql-connector    │
              └──────────┬──────────┘
                         │
         ┌───────────────┴───────────────┐
         │       MySQL / Oracle / ...   │
         └───────────────────────────────┘
```

**架构解读**：

- **SqlSession**：MyBatis 的核心 API，像 JDBC 的 Connection，代表一次数据库会话。
- **Executor**：执行器，负责 SQL 的实际执行，有 Simple（简单执行）、Reuse（重用语句）、Batch（批量执行）三种模式。
- **StatementHandler**：负责处理 JDBC Statement，包括 PreparedStatement 的创建和参数设置。
- **ResultSetHandler**：负责将 ResultSet 映射成 Java 对象。

### 38.2.3 MyBatis 快速上手

假设我们有一个用户表 `users(id, username, email)`，以及一个对应的 Java 实体类：

```java
/**
 * 用户实体类
 * 对应数据库中的 users 表
 */
public class User {
    private Integer id;
    private String username;
    private String email;

    // 无参构造器（MyBatis 需要）
    public User() {}

    public User(String username, String email) {
        this.username = username;
        this.email = email;
    }

    // Getter 和 Setter
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    @Override
    public String toString() {
        return "User{id=" + id + ", username='" + username + "', email='" + email + "'}";
    }
}
```

接下来是 MyBatis 的核心——Mapper 接口和 XML 映射文件：

```java
/**
 * UserMapper 接口
 * MyBatis 会根据这个接口自动生成实现类
 * 方法名和 XML 中 SQL 的 id 对应
 */
public interface UserMapper {

    // 查询所有用户
    List<User> findAll();

    // 根据 ID 查询用户
    User findById(Integer id);

    // 插入用户
    int insertUser(User user);

    // 更新用户邮箱
    int updateEmail(@Param("id") Integer id, @Param("email") String email);

    // 删除用户
    int deleteById(Integer id);
}
```

对应的 XML 映射文件 `UserMapper.xml`：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd">

<!-- namespace 指向 Mapper 接口 -->
<mapper namespace="com.example.mapper.UserMapper">

    <!-- resultMap：定义结果集如何映射到 Java 对象 -->
    <resultMap id="UserResultMap" type="com.example.entity.User">
        <id property="id" column="id"/>
        <result property="username" column="username"/>
        <result property="email" column="email"/>
    </resultMap>

    <!-- 查询所有用户 -->
    <select id="findAll" resultMap="UserResultMap">
        SELECT id, username, email FROM users
    </select>

    <!-- 根据 ID 查询 -->
    <select id="findById" resultMap="UserResultMap">
        SELECT id, username, email FROM users WHERE id = #{id}
    </select>

    <!-- 插入用户，useGeneratedKeys 获取自增主键 -->
    <insert id="insertUser" parameterType="com.example.entity.User"
            useGeneratedKeys="true" keyProperty="id">
        INSERT INTO users(username, email) VALUES(#{username}, #{email})
    </insert>

    <!-- 更新邮箱 -->
    <update id="updateEmail">
        UPDATE users SET email = #{email} WHERE id = #{id}
    </update>

    <!-- 删除 -->
    <delete id="deleteById">
        DELETE FROM users WHERE id = #{id}
    </delete>

</mapper>
```

最后是 MyBatis 配置文件 `mybatis-config.xml`：

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE configuration PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://localhost:3306/myapp?useSSL=false&amp;serverTimezone=UTC"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
        <!-- 注册 Mapper XML 文件 -->
        <mapper resource="mappers/UserMapper.xml"/>
    </mappers>
</configuration>
```

以及启动代码：

```java
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

import java.io.InputStream;
import java.util.List;

/**
 * MyBatis 快速入门演示
 */
public class MyBatisDemo {

    public static void main(String[] args) {
        // 加载 MyBatis 配置文件
        String resource = "mybatis-config.xml";
        try (InputStream inputStream = org.apache.ibatis.io.Resources.getResourceAsStream(resource)) {
            // 构建 SqlSessionFactory（会话工厂）
            SqlSessionFactory sqlSessionFactory = new SqlSessionFactoryBuilder().build(inputStream);

            // 打开一个会话（try-with-resources 自动关闭）
            try (SqlSession session = sqlSessionFactory.openSession()) {
                // 获取 Mapper（MyBatis 动态代理实现）
                UserMapper mapper = session.getMapper(UserMapper.class);

                // 查询
                User user = mapper.findById(1);
                System.out.println("查询结果: " + user);

                // 插入
                User newUser = new User("lisi", "lisi@example.com");
                int affected = mapper.insertUser(newUser);
                System.out.println("插入影响行数: " + affected + ", 新用户ID: " + newUser.getId());
                session.commit(); // 注意：MyBatis 默认不自动提交，需要手动 commit

                // 查询所有
                List<User> allUsers = mapper.findAll();
                allUsers.forEach(System.out::println);
            }

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 38.2.4 MyBatis 的动态 SQL

MyBatis 的一大杀器是**动态 SQL**——可以根据条件动态生成 SQL 语句。比如拼接查询条件：

```xml
<select id="findByConditions" resultMap="UserResultMap">
    SELECT id, username, email FROM users
    <where>
        <if test="username != null">
            AND username LIKE #{username}
        </if>
        <if test="email != null">
            AND email = #{email}
        </if>
    </where>
</select>
```

这样就不用写一堆 if 判断来拼接 SQL 了，MyBatis 帮你搞定。

### 38.2.5 MyBatis 注解版（不用 XML）

如果你不想写 XML，MyBatis 也支持注解方式直接在接口上写 SQL：

```java
public interface UserMapper {

    @Select("SELECT * FROM users WHERE id = #{id}")
    User findById(Integer id);

    @Insert("INSERT INTO users(username, email) VALUES(#{username}, #{email})")
    @Options(useGeneratedKeys = true, keyProperty = "id")
    int insert(User user);

    @Update("UPDATE users SET email = #{email} WHERE id = #{id}")
    int updateEmail(@Param("id") Integer id, @Param("email") String email);

    @Delete("DELETE FROM users WHERE id = #{id}")
    int deleteById(Integer id);
}
```

### 38.2.6 MyBatis 优缺点总结

| 优点 | 缺点 |
|------|------|
| SQL 完全可控，方便优化 | 需要手写 SQL（对某些人来说这是缺点） |
| 自动映射结果集，不用手动 set | XML 或注解配置有一定学习成本 |
| 动态 SQL 强大，条件拼接方便 | 关联查询（JOIN）配置相对繁琐 |
| 轻量级，没有太多魔法 | |

> **总结**：MyBatis 是那个"给你自由但不放弃你"的选择。你写 SQL，它负责其他脏活累活。特别适合国内业务场景——复杂查询多、SQL 优化是刚需。

---

## 38.3 JPA / Hibernate——你说需求，它来翻译

### 38.3.1 什么是 JPA

**JPA**（Java Persistence API）是 Java 官方提供的持久化规范标准。它不是具体实现，而是一套接口规范，类似于 JDBC 是规范、而 MySQL Connector 是实现的关系。

JPA 的主要实现包括：

- **Hibernate**：最流行的 JPA 实现，功能最全面
- **EclipseLink**：Oracle 官方的 JPA 实现
- **Spring Data JPA**：Spring 生态对 JPA 的封装和增强

### 38.3.2 什么是 Hibernate

**Hibernate** 是 JPA 规范的具体实现，它的核心思想是：**ORM**（Object-Relational Mapping，对象-关系映射）。

ORM 是什么？就是把你数据库里的表映射成 Java 类，表里的每一行映射成对象，表里的每一个字段映射成对象的属性。你操作对象，Hibernate 自动生成对应的 SQL。

打个比方：

- **JDBC** = 你拿着地图自己找路
- **MyBatis** = 你说目的地，它帮你规划路线但你还是坐在驾驶座
- **Hibernate** = 你说"我要去故宫"，它直接把车开到门口还帮你开门

### 38.3.3 Hibernate / JPA 架构图

```
┌─────────────────────────────────────────────────────────┐
│                   Application Code                       │
│              UserDao / UserService                       │
└────────────────────────┬────────────────────────────────┘
                         │
              ┌──────────┴──────────┐
              │    JPA Interface     │  ← Java Persistence API（规范）
              │  EntityManager       │
              └──────────┬──────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
  ┌──────┴──────┐ ┌──────┴──────┐ ┌──────┴──────┐
  │ Hibernate  │ │ EclipseLink │ │  OpenJPA    │
  │ (实现)      │ │ (实现)       │ │  (实现)     │
  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
              ┌──────────┴──────────┐
              │      JDBC Layer     │
              │  DriverManager      │
              └──────────┬──────────┘
                         │
         ┌───────────────┴───────────────┐
         │        Database               │
         │   MySQL / Oracle / PostgreSQL │
         └───────────────────────────────┘
```

### 38.3.4 第一个 JPA / Hibernate 程序

JPA 的核心概念是**实体（Entity）**——用 `@Entity` 注解标记的类对应数据库中的一张表。

首先，实体类：

```java
import jakarta.persistence.*;  // JPA 2.2+ 使用 jakarta.persistence（Java 9 之后）
// 如果用 javax.persistence 则为旧版 Java EE

/**
 * 用户实体类
 * @Entity 标记为 JPA 实体
 * @Table 指定对应的数据库表名
 */
@Entity
@Table(name = "users")
public class User {

    /**
     * @Id 标记主键
     * @GeneratedValue 主键生成策略
     *    - IDENTITY：自增长（MySQL）
     *    - SEQUENCE：序列（Oracle、PostgreSQL）
     *    - TABLE：表生成器（通用）
     *    - AUTO：由 JPA 自动选择（默认）
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    /**
     * @Column 映射列，可指定列名、长度、是否可空
     */
    @Column(name = "username", nullable = false, length = 50)
    private String username;

    @Column(name = "email", length = 100)
    private String email;

    // 无参构造器（JPA 必须）
    public User() {}

    public User(String username, String email) {
        this.username = username;
        this.email = email;
    }

    // Getter / Setter
    public Integer getId() { return id; }
    public void setId(Integer id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    @Override
    public String toString() {
        return "User{id=" + id + ", username='" + username + "', email='" + email + "'}";
    }
}
```

然后是 JPA 配置文件 `persistence.xml`（放在 `META-INF` 目录下）：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<persistence xmlns="https://jakarta.ee/xml/ns/persistence"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence
             https://jakarta.ee/xml/ns/persistence/persistence.xsd"
             version="3.0">

    <!-- persistence-unit 的名称，代码中通过这个名称获取 EntityManagerFactory -->
    <persistence-unit name="myapp" transaction-type="RESOURCE_LOCAL">

        <!-- 实体类 -->
        <class>com.example.entity.User</class>

        <!-- 数据库连接属性 -->
        <properties>
            <!-- Hibernate 作为 JPA 实现 -->
            <property name="jakarta.persistence.jdbc.driver" value="com.mysql.cj.jdbc.Driver"/>
            <property name="jakarta.persistence.jdbc.url"
                      value="jdbc:mysql://localhost:3306/myapp?useSSL=false&amp;serverTimezone=UTC"/>
            <property name="jakarta.persistence.jdbc.user" value="root"/>
            <property name="jakarta.persistence.jdbc.password" value="123456"/>

            <!-- Hibernate 特有配置：显示 SQL -->
            <property name="hibernate.show_sql" value="true"/>
            <property name="hibernate.format_sql" value="true"/>
            <!-- Hibernate 自动创建表（开发时用，生产环境建议用 migrations） -->
            <property name="hibernate.hbm2ddl.auto" value="update"/>
            <!-- MySQL 方言 -->
            <property name="hibernate.dialect" value="org.hibernate.dialect.MySQLDialect"/>
        </properties>
    </persistence-unit>
</persistence>
```

最后是 CRUD 操作：

```java
import jakarta.persistence.*;
import java.util.List;

/**
 * JPA / Hibernate CRUD 演示
 */
public class JpaDemo {

    // 创建 EntityManagerFactory（相当于 SqlSessionFactory，可复用）
    private static final EntityManagerFactory emf =
            Persistence.createEntityManagerFactory("myapp");

    public static void main(String[] args) {
        JpaDemo demo = new JpaDemo();

        // 插入
        User user = demo.insertUser("zhangsan", "zhangsan@example.com");
        System.out.println("插入: " + user);

        // 查询
        User found = demo.findById(user.getId());
        System.out.println("查询: " + found);

        // 更新
        demo.updateEmail(user.getId(), "newemail@example.com");
        System.out.println("更新后查询: " + demo.findById(user.getId()));

        // 查询所有
        List<User> all = demo.findAll();
        all.forEach(System.out::println);

        // 删除
        demo.deleteById(user.getId());
        System.out.println("删除后查询: " + demo.findById(user.getId()));

        // 关闭工厂
        emf.close();
    }

    // ---------- C: 创建 ----------
    public User insertUser(String username, String email) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction(); // JPA 默认不自动提交
        tx.begin();
        try {
            User user = new User(username, email);
            em.persist(user); // 插入到数据库
            tx.commit();
            return user;
        } catch (Exception e) {
            tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    // ---------- R: 读取 ----------
    public User findById(Integer id) {
        EntityManager em = emf.createEntityManager();
        try {
            // find 方法：先查一级缓存，没有则查数据库
            return em.find(User.class, id);
        } finally {
            em.close();
        }
    }

    // 使用 JPQL 查询（类似 SQL，但操作的是实体对象）
    public List<User> findAll() {
        EntityManager em = emf.createEntityManager();
        try {
            TypedQuery<User> query = em.createQuery("SELECT u FROM User u", User.class);
            return query.getResultList();
        } finally {
            em.close();
        }
    }

    // ---------- U: 更新 ----------
    public void updateEmail(Integer id, String newEmail) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();
        try {
            User user = em.find(User.class, id);
            if (user != null) {
                user.setEmail(newEmail);
                em.merge(user); // 更新（merge 类似 saveOrUpdate）
            }
            tx.commit();
        } catch (Exception e) {
            tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    // ---------- D: 删除 ----------
    public void deleteById(Integer id) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        tx.begin();
        try {
            User user = em.find(User.class, id);
            if (user != null) {
                em.remove(user); // 删除
            }
            tx.commit();
        } catch (Exception e) {
            tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }
}
```

### 38.3.5 一对多和多对一关系映射

实际业务中，用户和订单的关系是"一个用户有多个订单"。来看 JPA 如何处理这种**关联关系**：

```java
// Order 实体（多方）
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    private String orderNo;      // 订单号
    private Double totalPrice;  // 订单总金额

    /**
     * @ManyToOne：多对一关系（多个订单属于同一个用户）
     * @JoinColumn：指定外键列名
     */
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    public Order() {}

    public Order(String orderNo, Double totalPrice, User user) {
        this.orderNo = orderNo;
        this.totalPrice = totalPrice;
        this.user = user;
    }

    // Getter / Setter
    public Integer getId() { return id; }
    public String getOrderNo() { return orderNo; }
    public Double getTotalPrice() { return totalPrice; }
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
}
```

```java
// User 实体（一方）
@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(nullable = false)
    private String username;

    /**
     * @OneToMany：一对多关系（一个用户有多个订单）
     * mappedBy：表示在 Order 那边维护外键（放弃关系维护权）
     * cascade：级联操作（级联删除、级联持久化等）
     */
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Order> orders = new ArrayList<>();

    public User() {}
    public User(String username) { this.username = username; }

    public Integer getId() { return id; }
    public String getUsername() { return username; }
    public List<Order> getOrders() { return orders; }
    public void addOrder(Order order) {
        orders.add(order);
        order.setUser(this); // 维护双向关系
    }
}
```

### 38.3.6 Spring Data JPA——更简洁的 JPA

如果你的项目用 Spring Boot，**Spring Data JPA** 可以让你几乎不写 SQL。它的工作方式是：你只需要定义一个继承 `JpaRepository` 的接口，剩下的 CRUD 操作 Spring Data JPA 帮你自动实现。

```java
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

/**
 * UserRepository 接口
 * 继承 JpaRepository<实体类型, 主键类型>
 * 常用的 CRUD 方法已经自动实现了
 */
@Repository
public interface UserRepository extends JpaRepository<User, Integer> {

    // Spring Data JPA 会根据方法名自动推断 SQL
    // findByUsername：SELECT * FROM users WHERE username = ?
    List<User> findByUsername(String username);

    // findByEmailContaining：SELECT * FROM users WHERE email LIKE '%xxx%'
    List<User> findByEmailContaining(String emailKeyword);

    // 复杂查询也可以用 @Query 注解自定义 JPQL
    // @Query("SELECT u FROM User u WHERE u.username = :name")
    // User findByName(@Param("name") String name);
}
```

然后在 Service 层直接注入使用：

```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public List<User> findByUsername(String username) {
        return userRepository.findByUsername(username);
    }

    /**
     * @Transactional：Spring 自动管理事务
     * 如果抛出异常则自动回滚，否则自动提交
     */
    @Transactional
    public User save(User user) {
        return userRepository.save(user);
    }
}
```

### 38.3.7 JPA / Hibernate 的优点与缺点

| 优点 | 缺点 |
|------|------|
| 完全对象化，你只关心 Java 对象 | 复杂查询（多表 JOIN）性能不如手写 SQL |
| 告别 SQL，代码更简洁（尤其是 Spring Data JPA） | SQL 不透明，调优困难（"黑盒"问题） |
| 天然支持一级缓存（session 缓存）、二级缓存 | 学习曲线陡峭，注解众多 |
| 数据库移植性好（换数据库基本不换代码） | 懒加载导致的 N+1 查询问题 |
| 生态丰富（与 Spring 集成良好） | 批量操作性能不如 JDBC |

> **总结**：JPA/Hibernate 是那个"你想偷懒，它帮你搞定一切"的选择。但记住——偷懒是有代价的。当你的 SQL 变得复杂时，你可能会花更多时间去理解 Hibernate 生成的 SQL 到底在干什么。

---

## 本章小结

本章我们介绍了 Java 生态中三种主流的持久化方案，从"全手动挡"到"全自动驾驶"：

1. **JDBC**：Java 数据库通信的基石。你完全掌控 SQL，也完全负责所有细节——连接管理、异常处理、结果集映射。适合对性能有极致要求、愿意写大量模板代码的场景。

2. **MyBatis**：SQL 想怎么写你说了算，结果集自动映射，动态 SQL 强大。国内互联网公司宠爱有加，因为业务复杂查询多，SQL 优化是刚需。上手简单，进阶需要理解它的运行机制。

3. **JPA / Hibernate**：对象即一切。你操作对象，框架生成 SQL。Spring Data JPA 更是把"约定优于配置"发挥到极致。但当你需要写复杂查询时，"黑盒"生成的 SQL 可能让你抓狂。

没有最好的框架，只有最适合的选择。小项目快速开发选 JPA/Spring Data JPA；中等复杂度需要 SQL 控制力选 MyBatis；极致性能和完全可控选 JDBC。当然，实际项目中很多人是"脚踩两条船"——核心业务用 MyBatis，简单的 CRUD 用 Spring Data JPA。

持久化是后端开发的基石，学好这一章，你和数据库之间的"对话"就算是入门了！
