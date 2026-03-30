+++
title = "第37章 Spring Framework——企业级 Java 的基石"
weight = 370
date = "2026-03-30T14:33:56.922+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++
# 第三十七章 Spring Framework——企业级 Java 的基石

> "学 Java 的人，没有不知道 Spring 的。就像学开车的人，没有不知道方向盘的。" —— 某位不愿透露姓名的 Java 程序员

## 37.1 IoC（控制反转）与 DI（依赖注入）

### 37.1.1 什么是 IoC？

**IoC**，全称 **Inversion of Control**，中文叫"控制反转"。听起来高大上，其实原理很简单：

**传统方式**：你是一个勤奋的厨师，你自己去找食材、自己洗菜、自己切菜、自己炒菜。累不累？

**IoC 方式**：你只负责炒菜，食材有人送上门、洗菜有人帮你洗、切菜也有人帮你切。你只管炒！

这就是控制反转——**把对象的创建和管理权交给别人（容器），你自己只负责使用**。这就好比你是老板，雇了个助理帮你处理杂事，你只需要专注核心业务。

### 37.1.2 什么是 DI？

**DI**，全称 **Dependency Injection**，中文叫"依赖注入"。它是 IoC 的一种具体实现方式。

简单来说：依赖注入就是**把对象需要的依赖，在创建对象的时候自动"塞"进去**。

想象一下，你去相亲，对象说"我有车有房，父母健在"，这叫**自我介绍**。但如果是红娘直接把这些条件塞给你，那就叫**依赖注入**。

### 37.1.3 用代码说话

让我们通过一个生动的例子来理解 IoC 和 DI。假设我们要开发一个外卖系统：

```java
// 定义一个接口：送餐服务
public interface DeliveryService {
    String deliver(String orderId);  // 送餐方法
}
```

```java
// 美团送餐实现
public class MeituanDelivery implements DeliveryService {
    @Override
    public String deliver(String orderId) {
        return "美团骑手正在配送订单: " + orderId;
    }
}
```

```java
// 饿了吗送餐实现
public class ElemeDelivery implements DeliveryService {
    @Override
    public String deliver(String orderId) {
        return "饿了么骑手正在配送订单: " + orderId;
    }
}
```

```java
// 餐厅类 - 核心业务逻辑
public class Restaurant {
    // 依赖一个送餐服务
    private DeliveryService deliveryService;

    // 传统方式：自己 new（紧耦合，不推荐）
    public Restaurant() {
        this.deliveryService = new MeituanDelivery();  // 写死了！想换美团还是饿了么？改代码！
    }

    // DI 方式：通过构造函数注入（推荐）
    public Restaurant(DeliveryService deliveryService) {
        this.deliveryService = deliveryService;  // 别人给我什么，我就用什么
    }

    public void placeOrder(String orderId) {
        System.out.println("餐厅收到订单: " + orderId);
        String result = deliveryService.deliver(orderId);
        System.out.println(result);
    }
}
```

```java
public class IoCTest {
    public static void main(String[] args) {
        // 传统方式：餐厅和美团强耦合
        System.out.println("=== 传统方式（紧耦合）===");
        Restaurant restaurant1 = new Restaurant();
        restaurant1.placeOrder("ORDER001");

        // DI 方式：想用美团用美团，想用饿了么用饿了么
        System.out.println("\n=== DI 方式（解耦）===");
        DeliveryService meituan = new MeituanDelivery();
        Restaurant restaurant2 = new Restaurant(meituan);  // 注入美团
        restaurant2.placeOrder("ORDER002");

        DeliveryService ele = new ElemeDelivery();
        Restaurant restaurant3 = new Restaurant(ele);  // 换成饿了么
        restaurant3.placeOrder("ORDER003");
    }
}
```

运行结果：

```
=== 传统方式（紧耦合）===
餐厅收到订单: ORDER001
美团骑手正在配送订单: ORDER001

=== DI 方式（解耦）===
餐厅收到订单: ORDER002
美团骑手正在配送订单: ORDER002

餐厅收到订单: ORDER003
饿了么骑手正在配送订单: ORDER003
```

### 37.1.4 Spring 中的 IoC 容器

Spring 的核心就是一个 **IoC 容器**，它负责管理应用中所有对象的生命周期和依赖关系。

Spring IoC 容器的核心工作流程：

```
┌─────────────────────────────────────────────────────────┐
│                    Spring IoC 容器                        │
├─────────────────────────────────────────────────────────┤
│  1. 读取配置（XML / 注解 / Java Config）                  │
│                         ↓                                 │
│  2. 解析 Bean 定义（谁负责创建？依赖谁？）                   │
│                         ↓                                 │
│  3. 创建 Bean 实例                                        │
│                         ↓                                 │
│  4. 注入依赖（DI）                                         │
│                         ↓                                 │
│  5. 提供给应用程序使用                                      │
└─────────────────────────────────────────────────────────┘
```

**Bean** 是 Spring 容器管理的对象，你可以把它理解为 Spring 家的"娃"。

## 37.2 Spring Boot

### 37.2.1 为什么需要 Spring Boot？

在 Spring Boot 出现之前，搭建一个 Spring 项目是这样的：

```
1. 添加 Maven/Gradle 依赖（手动配置版本，小心冲突）
2. 配置 web.xml（古老的 XML 配置）
3. 配置 Spring MVC
4. 配置数据源
5. 配置事务
6. 配置日志
7. 部署到 Tomcat
8. 启动...

预计耗时：半天到三天不等，取决于你排错的能力
```

**Spring Boot 的出现，就是为了解决"配置地狱"问题！**

> "Spring Boot 就是让 Spring 项目像泡面一样简单——三分钟搞定，还不用洗碗。" —— 某位被 XML 配置折磨过的开发者

### 37.2.2 Spring Boot 核心特性

Spring Boot 有四大核心特性：

1. **自动配置（Auto-Configuration）**：自动检测你的 classpath，帮你想好该配什么
2. **起步依赖（Starter Dependencies）**：一个依赖包含一整套解决方案
3. **Actuator**：内置监控和健康检查
4. **嵌入式服务器**：不再需要单独安装 Tomcat

### 37.2.3 第一个 Spring Boot 项目

使用 Spring Boot 创建项目简单到令人发指：

```java
// pom.xml 中只需要一个父工程和起步依赖
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- 父工程：定义了常用依赖的版本 -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.2.0</version>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>hello-spring-boot</artifactId>
    <version>1.0.0</version>

    <properties>
        <java.version>17</java.version>
    </properties>

    <!-- Web 开发起步依赖：包含 Spring MVC + Tomcat -->
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Spring Boot 打包插件 -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
```

```java
// 主启动类：一个类搞定一切
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication  // 这个注解等于 @Configuration + @EnableAutoConfiguration + @ComponentScan
public class HelloSpringBootApplication {
    public static void main(String[] args) {
        // 启动 Spring Boot 应用，一行代码！
        SpringApplication.run(HelloSpringBootApplication.class, args);
    }
}
```

```java
// 创建一个 REST 控制器
package com.example.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController  // = @Controller + @ResponseBody（返回 JSON 而不是视图）
public class HelloController {

    @GetMapping("/hello")  // 处理 GET 请求，路径是 /hello
    public String sayHello() {
        return "Hello Spring Boot! 你好，世界！";
    }
}
```

运行效果：

```
.   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::               (v3.2.0)

2026-03-30 21:00:00.001  INFO 1 --- [           main] com.example.HelloSpringBootApplication    : Starting HelloSpringBootApplication...
2026-03-30 21:00:00.123  INFO 1 --- [           main] o.s.b.w.embedded.tomcat.TomcatWebServer    : Tomcat started on port(s): 8080
2026-03-30 21:00:00.456  INFO 1 --- [           main] com.example.HelloSpringBootApplication    : Started HelloSpringBootApplication in 2.5 seconds

访问 http://localhost:8080/hello 会返回：Hello Spring Boot! 你好，世界！
```

### 37.2.4 application.yml 配置文件

Spring Boot 支持两种配置文件格式：`application.properties` 和 `application.yml`。

```yaml
# application.yml 示例
server:
  port: 8080  # 服务器端口

spring:
  application:
    name: hello-spring-boot  # 应用名称
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: 123456
    driver-class-name: com.mysql.cj.jdbc.Driver

# 自定义配置
myapp:
  author: 路人甲
  version: 1.0.0
```

```java
// 读取配置：使用 @Value 注解注入单个值
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class ConfigController {

    @Value("${myapp.author:默认值}")  // 如果没配置，就用"默认值"
    private String author;

    @GetMapping("/author")
    public String getAuthor() {
        return "作者：" + author;
    }
}
```

```java
// 读取配置：使用 @ConfigurationProperties 绑定一组配置
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

@Component  // 让 Spring 扫描到这个组件
@ConfigurationProperties(prefix = "myapp")  // 绑定以 myapp 开头的配置
public class MyAppProperties {
    private String author;
    private String version;

    // getter 和 setter 是必须的
    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }
}
```

## 37.3 Spring MVC

### 37.3.1 什么是 MVC？

**MVC** 是 **Model-View-Controller** 的缩写，是一种软件设计模式：

- **Model（模型）**：数据模型，负责业务逻辑和数据处理
- **View（视图）**：展示层，负责渲染页面（HTML、JSP、Thymeleaf 等）
- **Controller（控制器）**：控制层，负责接收请求、调用模型、返回视图

想象你去餐厅吃饭：

- **你**（用户）跟服务员说：我要一份宫保鸡丁
- **服务员**（Controller）接收你的请求，告诉厨房
- **厨房**（Model）做好菜
- **服务员**（Controller）把菜端回来给你
- **盘子**（View）装着菜展示给你

### 37.3.2 Spring MVC 请求处理流程

```
┌─────────┐     ┌───────────┐     ┌──────────┐     ┌─────────┐     ┌────────┐
│  用户   │ ──→ │  DispatcherServlet  │ ──→ │ HandlerMapping      │ ──→ │ Controller       │
│  发送请求│     │  （前端控制器）     │     │ （处理器映射器）     │     │ （控制器）       │
└─────────┘     └───────────┘     └──────────┘     └─────────┘     └────────┘
                                                                      │
                   ┌───────────┐     ┌──────────┐     ┌─────────┐     ↓
                   │  用户看到  │ ←── │ ViewResolver     │ ──← │ ModelAndView        │
                   │  响应页面  │     │ （视图解析器）     │     │（模型和视图）       │
                   └───────────┘     └──────────┘     └─────────┘
```

流程解释：

1. **DispatcherServlet** 是 Spring MVC 的"门卫"，所有请求都先经过它
2. **HandlerMapping** 找到对应的 Controller 方法
3. **Controller** 处理业务逻辑，返回 ModelAndView
4. **ViewResolver** 解析视图模板
5. **渲染**后的页面返回给用户

### 37.3.3 完整示例

```java
// 实体类 - Model
package com.example.model;

public class User {
    private Long id;
    private String name;
    private String email;

    public User() {}

    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    // getter 和 setter
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

```java
// Controller - 处理用户请求
package com.example.controller;

import com.example.model.User;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;  // 用于传递数据给视图
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/users")  // 类上的路由：/users
public class UserController {

    // GET 请求：查询所有用户
    // 访问路径：/users 或 /users/list
    @GetMapping({"/", "/list"})
    public String listUsers(Model model) {
        List<User> users = new ArrayList<>();
        users.add(new User(1L, "张三", "zhangsan@example.com"));
        users.add(new User(2L, "李四", "lisi@example.com"));
        users.add(new User(3L, "王五", "wangwu@example.com"));

        model.addAttribute("users", users);  // 把数据传递给视图
        return "user/list";  // 返回视图名（由 ViewResolver 解析）
    }

    // GET 请求：查看单个用户
    // 访问路径：/users/1
    @GetMapping("/{id}")
    public String getUser(@PathVariable Long id, Model model) {
        // 假装从数据库查询
        User user = new User(id, "用户" + id, "user" + id + "@example.com");
        model.addAttribute("user", user);
        return "user/detail";
    }

    // GET 请求：显示创建用户的表单
    @GetMapping("/create")
    public String showCreateForm() {
        return "user/create";
    }

    // POST 请求：创建用户
    @PostMapping("/create")
    public String createUser(@RequestParam String name,
                             @RequestParam String email) {
        // 假装保存到数据库
        System.out.println("创建用户：name=" + name + ", email=" + email);
        // 重定向到用户列表
        return "redirect:/users/list";
    }

    // DELETE 请求：删除用户
    @DeleteMapping("/{id}")
    @ResponseBody  // 直接返回 JSON，不走视图
    public String deleteUser(@PathVariable Long id) {
        System.out.println("删除用户：" + id);
        return "{\"message\": \"删除成功，用户ID：" + id + "\"}";
    }
}
```

```java
// RESTful API Controller - 返回 JSON
package com.example.controller;

import com.example.model.User;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ConcurrentHashMap;

@RestController  // 所有方法都返回 JSON
@RequestMapping("/api/users")
public class UserApiController {

    // 模拟数据库
    private final ConcurrentHashMap<Long, User> userDb = new ConcurrentHashMap<>();

    public UserApiController() {
        userDb.put(1L, new User(1L, "张三", "zhangsan@example.com"));
        userDb.put(2L, new User(2L, "李四", "lisi@example.com"));
    }

    // GET /api/users - 获取所有用户
    @GetMapping
    public List<User> getAllUsers() {
        return new ArrayList<>(userDb.values());
    }

    // GET /api/users/1 - 获取单个用户
    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        User user = userDb.get(id);
        if (user == null) {
            throw new UserNotFoundException("用户不存在，ID：" + id);
        }
        return user;
    }

    // POST /api/users - 创建用户
    @PostMapping
    public User createUser(@RequestBody User user) {
        Long newId = userDb.size() + 1L;
        user.setId(newId);
        userDb.put(newId, user);
        return user;
    }

    // PUT /api/users/1 - 更新用户
    @PutMapping("/{id}")
    public User updateUser(@PathVariable Long id, @RequestBody User user) {
        user.setId(id);
        userDb.put(id, user);
        return user;
    }

    // DELETE /api/users/1 - 删除用户
    @DeleteMapping("/{id}")
    public void deleteUser(@PathVariable Long id) {
        userDb.remove(id);
    }

    // 自定义异常
    static class UserNotFoundException extends RuntimeException {
        public UserNotFoundException(String message) {
            super(message);
        }
    }
}
```

### 37.3.4 处理请求参数

Spring MVC 提供了多种接收请求参数的方式：

```java
@Controller
@RequestMapping("/params")
public class ParamController {

    // 1. 路径变量：/params/user/123
    @GetMapping("/user/{id}")
    public String pathVar(@PathVariable Long id) {
        return "路径参数，ID：" + id;
    }

    // 2. 查询参数：/params/search?name=张三&age=25
    @GetMapping("/search")
    public String search(@RequestParam String name,
                         @RequestParam(defaultValue = "0") int age) {
        return "查询参数，姓名：" + name + "，年龄：" + age;
    }

    // 3. 请求头：获取请求头中的值
    @GetMapping("/header")
    public String header(@RequestHeader("User-Agent") String userAgent,
                         @RequestHeader(value = "Accept-Language", defaultValue = "zh-CN") String language) {
        return "User-Agent：" + userAgent + "<br>语言：" + language;
    }

    // 4. Cookie：获取 Cookie 值
    @GetMapping("/cookie")
    public String cookie(@CookieValue(value = "session_id", required = false) String sessionId) {
        return "Session ID：" + sessionId;
    }

    // 5. 请求体：接收 JSON 请求体
    @PostMapping("/body")
    @ResponseBody
    public String body(@RequestBody User user) {
        return "请求体数据：" + user.getName() + "，" + user.getEmail();
    }

    // 6. 表单提交：接收表单数据
    @PostMapping("/form")
    public String form(@RequestParam String username,
                       @RequestParam String password) {
        return "表单数据：用户名=" + username + "，密码=" + password;
    }
}
```

## 37.4 Spring 常用注解

### 37.4.1 核心注解

Spring 的注解就像武侠小说里的"武功秘籍"，学会了就能四两拨千斤。

| 注解 | 说明 | 类比 |
|------|------|------|
| `@Component` | 通用组件注解，Spring 会扫描并管理此类 | "不管你是啥，先纳入管理" |
| `@Service` | 业务层组件注解 | "这是服务层，专注业务逻辑" |
| `@Repository` | 数据访问层组件注解 | "这是数据仓库，负责 CRUD" |
| `@Controller` | 控制器注解 | "这是控制器，接收用户请求" |
| `@RestController` | RESTful 控制器（=@Controller + @ResponseBody）| "直接返回数据，不走视图" |

```java
// 一个典型的 Spring 分层架构

// 数据层：专门跟数据库打交道
@Repository
public class UserDao {
    public User findById(Long id) {
        // 假装查询数据库
        return new User(id, "用户" + id, "user" + id + "@example.com");
    }
}

// 业务层：专注业务逻辑
@Service
public class UserService {
    // 注入 DAO（依赖注入）
    private final UserDao userDao;

    public UserService(UserDao userDao) {
        this.userDao = userDao;
    }

    public User getUser(Long id) {
        if (id == null || id <= 0) {
            throw new IllegalArgumentException("无效的用户ID");
        }
        return userDao.findById(id);
    }
}

// 控制层：接收请求，返回响应
@RestController
@RequestMapping("/api/users")
public class UserApi {
    private final UserService userService;

    public UserApi(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/{id}")
    public User getUser(@PathVariable Long id) {
        return userService.getUser(id);
    }
}
```

### 37.4.2 依赖注入注解

| 注解 | 说明 | 使用场景 |
|------|------|----------|
| `@Autowired` | 按类型自动注入（Spring 专用）| 字段、构造函数、setter |
| `@Inject` | 按类型自动注入（Java 标准）| 同 @Autowired |
| `@Resource` | 按名称注入（Java 标准）| 字段、setter |
| `@Qualifier` | 指定注入哪个 Bean | 多个同类型 Bean 时 |
| `@Primary` | 指定优先使用的 Bean | 多个同类型 Bean 时 |

```java
@Service
public class NotificationService {

    // 方式1：构造函数注入（推荐，最正式）
    private final EmailService emailService;
    private final SmsService smsService;

    public NotificationService(EmailService emailService, SmsService smsService) {
        this.emailService = emailService;
        this.smsService = smsService;
    }

    // 方式2：字段注入（简洁但不推荐）
    @Autowired
    private PushService pushService;

    // 方式3：setter 注入
    private WechatService wechatService;

    @Autowired
    public void setWechatService(WechatService wechatService) {
        this.wechatService = wechatService;
    }
}
```

```java
// 当有多个同类型 Bean 时，使用 @Qualifier 或 @Primary

// 接口
public interface Payment {
    void pay(double amount);
}

// 微信支付实现
@Service("wechatPay")
public class WechatPayment implements Payment {
    @Override
    public void pay(double amount) {
        System.out.println("微信支付：" + amount + "元");
    }
}

// 支付宝支付实现
@Service("aliPay")
public class AlipayPayment implements Payment {
    @Override
    public void pay(double amount) {
        System.out.println("支付宝支付：" + amount + "元");
    }
}

// 银行卡支付实现
@Service
@Primary  // 默认使用的实现
public class CardPayment implements Payment {
    @Override
    public void pay(double amount) {
        System.out.println("银行卡支付：" + amount + "元");
    }
}
```

```java
// 使用 @Qualifier 指定注入哪个
@RestController
public class OrderController {

    private final Payment payment;

    // 指定使用微信支付
    @Autowired
    public OrderController(@Qualifier("wechatPay") Payment payment) {
        this.payment = payment;
    }

    public void createOrder(double amount) {
        payment.pay(amount);
    }
}
```

### 37.4.3 请求处理注解

| 注解 | 说明 |
|------|------|
| `@GetMapping` | 处理 GET 请求 |
| `@PostMapping` | 处理 POST 请求 |
| `@PutMapping` | 处理 PUT 请求 |
| `@DeleteMapping` | 处理 DELETE 请求 |
| `@PatchMapping` | 处理 PATCH 请求 |
| `@RequestMapping` | 通用的请求映射 |

```java
@RestController
@RequestMapping("/api/products")
public class ProductController {

    // GET /api/products
    @GetMapping
    public List<Product> list() { /*...*/ }

    // GET /api/products/123
    @GetMapping("/{id}")
    public Product get(@PathVariable Long id) { /*...*/ }

    // POST /api/products
    @PostMapping
    public Product create(@RequestBody Product product) { /*...*/ }

    // PUT /api/products/123
    @PutMapping("/{id}")
    public Product update(@PathVariable Long id, @RequestBody Product product) { /*...*/ }

    // DELETE /api/products/123
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) { /*...*/ }
}
```

### 37.4.4 常用配置注解

| 注解 | 说明 |
|------|------|
| `@Configuration` | 标识这是一个配置类 |
| `@Bean` | 声明一个 Bean（替代 XML 配置）|
| `@ComponentScan` | 指定要扫描的包 |
| `@PropertySource` | 引入外部配置文件 |
| `@Value` | 注入配置值 |

```java
@Configuration  // 声明这是一个配置类
public class AppConfig {

    // 相当于 <bean id="userService" class="com.example.UserService"/>
    @Bean
    public UserService userService() {
        return new UserService();
    }

    // 带依赖的 Bean
    @Bean
    public OrderService orderService(UserService userService) {
        // Spring 会自动注入 UserService
        return new OrderService(userService);
    }
}
```

```java
@Configuration
@ComponentScan(basePackages = "com.example")  // 扫描 com.example 包
@PropertySource("classpath:app.properties")   // 引入配置文件
public class AutoConfig {
    // 配置类的内容
}
```

### 37.4.5 AOP 相关注解

**AOP**（Aspect-Oriented Programming，面向切面编程）是一种编程范式，用于将**横切关注点**（如日志、事务、安全）与业务逻辑分离。

```java
// 定义切面
@Aspect  // 声明这是一个切面
@Component  // 让 Spring 管理
public class LoggingAspect {

    // 切入点：拦截所有 Controller 的方法
    @Pointcut("execution(* com.example.controller..*.*(..))")
    public void controllerPointcut() {}

    // 前置通知
    @Before("controllerPointcut()")
    public void before(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[前置] 准备执行方法：" + methodName);
    }

    // 后置通知
    @After("controllerPointcut()")
    public void after(JoinPoint joinPoint) {
        String methodName = joinPoint.getSignature().getName();
        System.out.println("[后置] 方法执行完成：" + methodName);
    }

    // 返回通知
    @AfterReturning(pointcut = "controllerPointcut()", returning = "result")
    public void afterReturning(JoinPoint joinPoint, Object result) {
        System.out.println("[返回] 方法返回：" + result);
    }

    // 异常通知
    @AfterThrowing(pointcut = "controllerPointcut()", throwing = "e")
    public void afterThrowing(JoinPoint joinPoint, Exception e) {
        System.out.println("[异常] 方法抛出异常：" + e.getMessage());
    }
}
```

## Spring 架构图

```
┌────────────────────────────────────────────────────────────────────────┐
│                         Spring 全家桶架构图                              │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                        Spring Boot                               │  │
│  │   自动配置 + 起步依赖 + Actuator + 嵌入式服务器                    │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    ↑                                    │
│                                    │                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      Spring Framework                            │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────┐  │  │
│  │  │   Core      │  │   Web       │  │   Data      │  │  AOP    │  │  │
│  │  │  IoC/DI     │  │  Web MVC    │  │  Access     │  │  Aspect │  │  │
│  │  │  容器       │  │  REST       │  │  JDBC       │  │  切面   │  │  │
│  │  │             │  │  WebFlux    │  │  ORM        │  │  编程  │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐               │  │
│  │  │   Testing   │  │   Integration│  │  Messaging  │               │  │
│  │  │  单元测试   │  │  集成测试    │  │  消息队列  │               │  │
│  │  │  Mock对象   │  │  JMS/AMQP   │  │  RabbitMQ   │               │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘               │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                    ↑                                    │
│                                    │                                    │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                      运行环境                                      │  │
│  │         Tomcat / Jetty / Undertow / Netty                         │  │
│  │         JDK 17+ / JVM                                             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

## 本章小结

本章我们学习了 Java 企业级开发的基石——Spring Framework，主要内容包括：

1. **IoC 与 DI**：理解了控制反转和依赖注入的核心概念，通过将对象创建和依赖管理交给 Spring 容器，实现了代码的松耦合。

2. **Spring Boot**：掌握了 Spring Boot 的核心特性，包括自动配置、起步依赖、内嵌服务器等，能够快速搭建生产级别的 Spring 应用。

3. **Spring MVC**：理解了 MVC 设计模式，熟悉了请求处理流程，掌握了 RESTful API 的开发方式。

4. **Spring 常用注解**：学习了@Component、@Service、@Repository、@Controller、@Autowired、@GetMapping 等核心注解的用法。

> "Spring 不是银弹，但它是 Java 企业开发中最接近银弹的存在。" —— Rod Johnson（Spring 之父）

下一章我们将深入学习 Spring Boot 的更多高级特性，敬请期待！

---

*_"Talk is cheap, show me the code." —— Linus Torvalds_*
