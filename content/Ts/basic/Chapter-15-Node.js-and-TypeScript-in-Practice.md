+++
title = "第15章 Node.js + TypeScript 实战"
weight = 150
date = "2026-03-26T21:05:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++

# 第 15 章 Node.js + TypeScript 实战

> 写 TypeScript 只会在浏览器里玩？那你只解锁了这门语言 20% 的成就。Node.js + TypeScript 才是真正的完全体——后端 API、数据库操作、文件系统、命令行工具，统统拿下。本章就是你的"全栈 TypeScript 修炼手册"。

## 15.1 项目初始化

### 15.1.1 tsconfig 配置与环境变量类型扩展

当你终于决定用 TypeScript 写后端的那一刻，恭喜你——你已经比 90% 的 Node.js 开发者高了一个段位。但革命尚未成功，配置先搞好。

初始化一个 Node.js + TypeScript 项目，只需要几步：

```bash
mkdir my-backend && cd my-backend
npm init -y
npm install -D typescript @types/node ts-node
npx tsc --init
```

执行完 `npx tsc --init` 之后，你会看到目录里多了一个 `tsconfig.json`。但别高兴太早——默认配置是给浏览器用的，想写后端还得折腾一番。

一个标准的 Node.js 后端 `tsconfig.json` 长这样：

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "outDir": "./dist",
        "rootDir": "./src",
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true,
        "forceConsistentCasingInFileNames": true,
        "resolveJsonModule": true,
        "declaration": true,
        "declarationMap": true,
        "sourceMap": true
    },
    "include": ["src/**/*"],
    "exclude": ["node_modules", "dist"]
}
```

来，逐个解释这些配置都是干嘛的：

- **`target: "ES2022"`**：编译目标定为 ES2022，也就是现代 Node.js（v18+）支持的语法版本。别再用 `"ES5"` 了，都 2026 年了，你还在兼容 IE6 吗？

- **`module: "NodeNext"`**：`NodeNext` 是 Node.js 官方的模块系统，支持 ESM 和 CJS 混搭。如果你想在 Node.js 里用 `import`/`export` 语法，这个选项必须开。

- **`moduleResolution: "NodeNext"`**：和 `module` 配套，告诉 TypeScript 按照 Node.js 的模块解析规则去找模块。

- **`strict: true`**：开启所有严格类型检查。后端代码不比前端，不需要考虑浏览器兼容问题，直接开最严格的模式就对了。

- **`esModuleInterop: true`**：让 `import fs from 'fs'` 这样的语句能正常工作（不开启的话，CJS 模块的默认导入会有问题）。

- **`skipLibCheck: true`**：跳过对 `@types/*` 包的类型检查。开启这个可以大大加快编译速度，那些第三方库的类型声明文件里的破事儿就不用管了。

- **`resolveJsonModule: true`**：允许直接 `import` JSON 文件。这个在读取配置文件（`package.json`、`config.json`）的时候特别有用。

- **`declaration: true`** 和 **`declarationMap: true`**：生成 `.d.ts` 类型声明文件和它的 source map，让其他项目引用你的包时能获得完整的类型提示。

- **`sourceMap: true`**：生成 source map，方便调试。当你的 TypeScript 代码报错时，source map 能让错误信息指向原始的 `.ts` 文件，而不是编译后的 `.js` 文件。

**敲黑板**：后端 TypeScript 项目的 `tsconfig.json` 和前端（Vite/Webpack 项目）完全不同，别混用！

配置好 `tsconfig.json` 之后，你的项目目录结构应该是这样的：

```
my-backend/
├── src/
│   └── index.ts          # 入口文件
├── dist/                  # 编译输出目录（不要手动修改）
├── node_modules/
├── tsconfig.json
└── package.json
```

接下来，在 `package.json` 的 `scripts` 里加上几个常用的命令：

```json
{
    "scripts": {
        "dev": "tsx watch src/index.ts",
        "build": "tsc",
        "start": "node dist/index.js",
        "typecheck": "tsc --noEmit"
    }
}
```

`npm run dev` 用于开发阶段热重载，`npm run build` 用于生产环境编译，`npm run typecheck` 用于在不编译的情况下检查类型错误。

**环境变量类型扩展**——这是后端 TypeScript 项目里最容易翻车的环节之一。

我们在后端项目里几乎都要用 `process.env` 来读取环境变量，但 `process.env` 的类型定义默认只有 `string | undefined`，你读取一个 `PORT` 环境变量得到的是 `string | undefined`，想转成 `number` 还得手动断言：

```typescript
const port = process.env.PORT; // 类型是 string | undefined
const portNumber = port as unknown as number; // 太粗暴了！
```

更优雅的做法是用 `zod` 或者 `dotenv` 配合类型推导。不过在讲解具体方案之前，先说说为什么环境变量需要"类型扩展"。

Node.js 原生的 `process.env` 类型定义是这样的：

```typescript
declare namespace NodeJS {
    interface ProcessEnv {
        [key: string]: string | undefined;
    }
}

declare var process: {
    env: ProcessEnv;
};
```

也就是说，`process.env` 上任何不存在的属性，类型都是 `string | undefined`。但实际上，我们的环境变量是有具体类型的——比如 `PORT` 应该是 `number`，`DATABASE_URL` 应该是 `string`，`DEBUG_MODE` 应该是 `boolean`。

怎么让 TypeScript 知道这一点？答案是**类型声明合并**（第11章讲过）：

```typescript
// src/types/env.d.ts
declare global {
    namespace NodeJS {
        interface ProcessEnv {
            PORT: string;           // 环境变量是字符串，运行时 Node.js 就是这么存的
            DATABASE_URL: string;
            NODE_ENV: "development" | "production" | "test";
            DEBUG_MODE: "true" | "false"; // 环境变量永远是字符串，没有布尔类型
            API_TIMEOUT: string;
        }
    }
}

export {}; // 这是 d.ts 文件的"保命符"，防止类型合并污染全局
```

加上这段类型声明之后，TypeScript 就知道：
- `process.env.PORT` 是 `string`，不是 `string | undefined`
- `process.env.NODE_ENV` 是 `"development" | "production" | "test"`，不是 `string`
- `process.env.DEBUG_MODE` 是 `"true" | "false"`，不是 `string | undefined`

不过请注意：**环境变量在操作系统层面永远是字符串**。所以 `DEBUG_MODE: "true" | "false"` 而不是 `boolean`，这很合理——你需要在代码里自己做转换：

```typescript
const isDebug = process.env.DEBUG_MODE === "true";
console.log(isDebug); // true 或 false（取决于环境变量值）
```

---

## 15.2 Express / Fastify 类型化

### 15.2.1 请求响应类型定义

终于要写后端 API 了！假设你已经选好了框架——要么是老牌的 **Express**，要么是新贵 **Fastify**。不管选哪个，TypeScript 都能给你完整的类型安全。

先从最经典的 Express 开始。

Express 的请求（Request）和响应（Response）对象原来是没有泛型参数的，你想拿到一个带类型的 `req.body`，得自己 cast：

```typescript
// 没有类型的时候
app.post("/user", (req, res) => {
    const name = req.body.name; // 类型是 any，瞎眼！
    const age = req.body.age;  // any again！
    // ...
});
```

有了 TypeScript，我们需要先给 `req.body` 定义一个类型：

```typescript
// 定义请求体的类型
interface CreateUserBody {
    name: string;
    email: string;
    age: number;
}

app.post<{ Body: CreateUserBody }>("/user", (req, res) => {
    // 现在 req.body 的类型是 CreateUserBody
    const { name, email, age } = req.body;

    if (!name || !email) {
        res.status(400).json({ error: "name 和 email 是必填的" });
        return;
    }

    console.log(`收到创建用户请求: ${name}, ${email}, ${age}`);
    // 后续调用数据库等操作
    res.status(201).json({ id: 1, name, email, age });
});
```

Express 的路由泛型参数格式是 `app.METHOD<ReqParams, ResBody, ReqQuery, ReqBody>(path, handler)`。我们来逐一拆解：

- **`ReqParams`**：URL 参数的类型，比如 `/user/:id` 中的 `id`
- **`ResBody`**：响应的 JSON body 类型
- **`ReqQuery`**：查询字符串（`?key=value`）的类型
- **`ReqBody`**：请求体的类型

一个完整的类型化 Express 接口：

```typescript
interface UserParams {
    id: string;
}

interface UserQuery {
    includeStats?: "true" | "false";
    page?: string;
}

interface User {
    id: number;
    name: string;
    email: string;
    createdAt: string;
}

app.get<{ Params: UserParams; Query: UserQuery; Reply: User | User[] }>(
    "/user/:id",
    (req, res) => {
        const { id } = req.params;     // string（自动类型收窄）
        const includeStats = req.query.includeStats === "true";
        const page = req.query.page ? parseInt(req.query.page, 10) : 1;

        console.log(`查询用户 ID: ${id}, includeStats: ${includeStats}, page: ${page}`);

        // 模拟数据库查询
        const user: User = {
            id: parseInt(id, 10),
            name: "张三",
            email: "zhangsan@example.com",
            createdAt: new Date().toISOString(),
        };

        res.json(user);
    }
);
```

### 15.2.2 中间件函数类型签名

Express 的中间件（Middleware）是它的灵魂——请求在到达处理函数之前，会经过一连串的中间件"安检"。但中间件的 TypeScript 类型签名是一个重灾区，很多人写着写着就变成了 `any`。

先来看中间件的基本签名：

```typescript
// Express 中间件的标准类型签名
type ExpressMiddleware = (
    req: Request,
    res: Response,
    next: NextFunction
) => void | Promise<void>;
```

一个简单的日志中间件：

```typescript
function loggerMiddleware(
    req: Request,
    res: Response,
    next: NextFunction
): void {
    const start = Date.now();
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);

    // 在响应结束后打印耗时
    res.on("finish", () => {
        const duration = Date.now() - start;
        console.log(`请求完成: ${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
    });

    next();
}

// 注册中间件
app.use(loggerMiddleware);
```

一个认证中间件，返回的是错误或者继续往下走：

```typescript
import { Request, Response, NextFunction } from "express";

// 定义认证失败时抛出的错误类型
class UnauthorizedError extends Error {
    statusCode = 401;
    constructor(message = "未授权访问") {
        super(message);
        this.name = "UnauthorizedError";
    }
}

interface AuthRequest extends Request {
    userId?: number;
    userRole?: "admin" | "user";
}

function authMiddleware(
    req: Request,
    res: Response,
    next: NextFunction
): void {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith("Bearer ")) {
        next(new UnauthorizedError("缺少有效的 Authorization header"));
        return;
    }

    const token = authHeader.slice(7); // 去掉 "Bearer " 前缀

    // 这里应该是 JWT 验证的逻辑，简化演示
    try {
        // 假设验证通过，注入 userId 和 userRole 到 req
        (req as AuthRequest).userId = 1;
        (req as AuthRequest).userRole = "admin";
        next();
    } catch {
        next(new UnauthorizedError("无效的 Token"));
    }
}

// 使用中间件
app.get("/admin", authMiddleware, (req, res) => {
    const authReq = req as AuthRequest;
    console.log(`管理员访问: userId=${authReq.userId}, role=${authReq.userRole}`);
    res.json({ message: "欢迎来到管理员后台！" });
});
```

**敲黑板**：中间件的参数类型最好显式声明，不要偷懒用 `any`。一旦用了 `any`，TypeScript 就无法帮你检查 `req`、`res`、`next` 的使用是否正确了。

### 15.2.3 Schema 的类型推断（Fastify）

说完 Express，来看它的强劲对手——**Fastify**。

Fastify 号称"最快的 Node.js Web 框架"，它的最大亮点就是**Schema First**——你写一个 JSON Schema，Fastify 自动给你生成类型定义，不需要手动写接口。

先安装依赖：

```bash
npm install fastify
npm install -D @fastify/type-provider-typebox tsx
```

**敲黑板**：要用 TypeBox 做 Fastify 类型推断，安装的是 `@fastify/type-provider-typebox`，不是 `@fastify/type-provider-json-schema`——别问我怎么知道的，这是无数人踩过的坑。

一个完整的类型化 Fastify API（Fastify v5 + TypeBox）：

```typescript
import Fastify from "fastify";
import { Type, Static } from "@sinclair/typebox";
import type { FastifyPluginAsync } from "fastify";

// 用 TypeBox 定义 schema（同时也是类型）
const UserSchema = Type.Object({
    id: Type.Number(),
    name: Type.String(),
    email: Type.String({ format: "email" }),
    age: Type.Optional(Type.Number()),
});

// 从 schema 推断出 TypeScript 类型
type User = Static<typeof UserSchema>;

// 创建用户请求体的 schema
const CreateUserSchema = Type.Object({
    name: Type.String({ minLength: 1 }),
    email: Type.String({ format: "email" }),
    age: Type.Optional(Type.Number({ minimum: 0 })),
});

// 用 FastifyPluginAsync 包装插件，获取完整的类型推导
const userRoutes: FastifyPluginAsync = async (fastify) => {
    fastify.post("/user", async (request, reply) => {
        // request.body 的类型由 schema 自动推导，不需要手动写泛型
        const { name, email, age } = request.body as Static<typeof CreateUserSchema>;

        // 模拟数据库插入
        const newUser: User = {
            id: Math.floor(Math.random() * 10000),
            name,
            email,
            age,
        };

        console.log(`创建用户: ${name} (${email})`);
        reply.code(201);
        return newUser;
    });

    // 查询单个用户
    fastify.get("/user/:id", async (request) => {
        const { id } = request.params as { id: string };
        console.log(`查询用户 ID: ${id}`);

        // 模拟数据库查询
        const user: User = {
            id: parseInt(id, 10),
            name: "张三",
            email: "zhangsan@example.com",
            age: 25,
        };

        return user;
    });
};

const server = Fastify();

server.register(userRoutes);

server.listen({ port: 3000 }, (err, address) => {
    if (err) {
        console.error(err);
        process.exit(1);
    }
    console.log(`服务器启动在 ${address}`);
});
```

这段代码的精妙之处在于：**`CreateUserBody` 和 `User` 类型都是从 JSON Schema 自动推断出来的**，你不需要写两遍类型定义。`as Static<...>` 只是一个显式的类型标注，让代码意图更清晰。

`TypeBox` 是一个用 TypeScript 写的库，它的类型系统在**运行时是真实的 JSON Schema**，在**编译时是 TypeScript 类型**——两全其美。

```bash
# 开发阶段运行（tsx 支持 ESM 和热重载，比 ts-node 更现代）
npm install -D tsx
npm run dev

# 生产阶段编译
npm run build
```

---

## 15.3 数据库类型化

### 15.3.1 Prisma ORM 与 TypeScript 的集成

说到后端，数据库是永远绕不开的话题。**Prisma** 是目前 TypeScript 生态里最时髦的 ORM，它最大的卖点就是：**数据库 schema 就是类型定义**。

安装 Prisma：

```bash
npm install prisma @prisma/client
npx prisma init
```

安装完成后，目录里会多出一个 `prisma/schema.prisma` 文件。这个文件就是 Prisma 的 schema——你在这里定义数据模型，Prisma 自动生成 TypeScript 类型。

编辑 `prisma/schema.prisma`：

```prisma
// prisma/schema.prisma

generator client {
    provider = "prisma-client-js"
}

datasource db {
    provider = "postgresql"
    url      = env("DATABASE_URL")
}

model User {
    id        Int      @id @default(autoincrement())
    email     String   @unique
    name      String
    age       Int?
    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt

    posts     Post[]   // 一对多关系：一个用户可以有多篇文章
}

model Post {
    id        Int      @id @default(autoincrement())
    title     String
    content   String?
    published Boolean  @default(false)
    authorId  Int

    author    User     @relation(fields: [authorId], references: [id])

    createdAt DateTime @default(now())
    updatedAt DateTime @updatedAt
}
```

定义好 schema 之后，运行 `npx prisma generate`，Prisma 就会在 `node_modules/.prisma/client` 里生成完整的 TypeScript 类型。

生成的类型是什么样的？可以直接看 `node_modules/.prisma/client/index.d.ts`，或者直接用：

```typescript
import { PrismaClient } from "@prisma/client";

const prisma = new PrismaClient();

// Prisma 自动知道 User 类型的完整结构
const user = await prisma.user.findUnique({
    where: { id: 1 },
    include: { posts: true },
});

// user.name 的类型是 string
// user.posts 是 Post[] 类型
// user.posts[0].title 的类型是 string
console.log(user?.name); // 张三
console.log(user?.posts[0]?.title); // 我的第一篇文章
```

这就是 Prisma 的魔力——**不需要你手动定义类型，类型从 schema 里自动长出来**。

### 15.3.2 Prisma Client 类型化查询

Prisma Client 的查询是**完全类型安全**的——不仅返回值是类型化的，连查询参数也会做类型检查。

```typescript
import { PrismaClient, Prisma } from "@prisma/client";

const prisma = new PrismaClient();

// Prisma 会检查 where 参数是否符合 schema
// 如果你写了不存在的字段，TypeScript 直接报错
const activeUsers = await prisma.user.findMany({
    where: {
        age: { gte: 18 }, // gte = greater than or equal
        posts: {
            some: {
                published: true, // 只查询有已发布文章的用户
            },
        },
    },
    orderBy: { createdAt: "desc" },
    take: 10,
});

// activeUsers 的类型是 User[]，完全类型安全
console.log(activeUsers[0]?.name);
```

**关联查询**也完全类型化：

```typescript
// 查询某个用户及其所有已发布的文章，并统计文章数量
async function getUserWithPublishedPosts(userId: number) {
    const result = await prisma.user.findUnique({
        where: { id: userId },
        include: {
            posts: {
                where: { published: true },
                select: {
                    id: true,
                    title: true,
                    createdAt: true,
                },
                orderBy: { createdAt: "desc" },
            },
            _count: {
                select: { posts: true }, // 统计文章总数
            },
        },
    });

    if (!result) {
        console.log("用户不存在");
        return null;
    }

    console.log(`用户: ${result.name}`);
    console.log(`已发布文章数: ${result._count.posts}`);
    result.posts.forEach((post) => {
        console.log(`  - ${post.title}`);
    });

    return result;
}

getUserWithPublishedPosts(1);
```

---

## 15.4 错误处理

### 15.4.1 自定义错误类的类型继承体系

后端服务最怕什么？**线上崩了没人知道原因**。一个好的错误处理体系，应该能让错误信息精确到"哪一行代码出了问题"。

在 TypeScript 后端里，建议用**自定义错误类继承体系**来处理错误：

```typescript
// src/errors/AppError.ts

// 基类错误
class AppError extends Error {
    constructor(
        public message: string,
        public statusCode: number = 500,
        public code: string = "INTERNAL_ERROR",
        public details?: unknown
    ) {
        super(message);
        this.name = this.constructor.name;
        Error.captureStackTrace(this, this.constructor);
    }
}

// 400 - 客户端请求有问题
class BadRequestError extends AppError {
    constructor(message: string, details?: unknown) {
        super(message, 400, "BAD_REQUEST", details);
    }
}

// 401 - 未认证
class UnauthorizedError extends AppError {
    constructor(message: string = "需要登录", details?: unknown) {
        super(message, 401, "UNAUTHORIZED", details);
    }
}

// 403 - 无权限
class ForbiddenError extends AppError {
    constructor(message: string = "权限不足", details?: unknown) {
        super(message, 403, "FORBIDDEN", details);
    }
}

// 404 - 资源不存在
class NotFoundError extends AppError {
    constructor(resource: string, id?: number | string) {
        const message = id !== undefined
            ? `${resource} with id ${id} not found`
            : `${resource} not found`;
        super(message, 404, "NOT_FOUND");
    }
}

// 409 - 资源冲突（比如唯一键重复）
class ConflictError extends AppError {
    constructor(message: string, details?: unknown) {
        super(message, 409, "CONFLICT", details);
    }
}

// 500 - 服务器内部错误
class InternalError extends AppError {
    constructor(message: string = "服务器内部错误", details?: unknown) {
        super(message, 500, "INTERNAL_ERROR", details);
    }
}

export {
    AppError,
    BadRequestError,
    UnauthorizedError,
    ForbiddenError,
    NotFoundError,
    ConflictError,
    InternalError,
};
```

使用这些错误类：

```typescript
import { NotFoundError, BadRequestError, ConflictError } from "./errors/AppError";

async function getUser(id: number) {
    const user = await prisma.user.findUnique({ where: { id } });

    if (!user) {
        throw new NotFoundError("User", id); // "User with id 1 not found"
    }

    return user;
}

async function createUser(email: string, name: string) {
    // 检查 email 是否已被使用
    const existing = await prisma.user.findUnique({ where: { email } });

    if (existing) {
        throw new ConflictError(`Email ${email} already in use`);
    }

    if (!name || name.trim().length === 0) {
        throw new BadRequestError("name cannot be empty");
    }

    return prisma.user.create({
        data: { email, name: name.trim() },
    });
}
```

然后写一个**全局错误处理中间件**，把所有错误统一格式化成 JSON 响应：

```typescript
import { Request, Response, NextFunction } from "express";
import { AppError } from "./errors/AppError";

function errorHandler(
    err: Error,
    req: Request,
    res: Response,
    _next: NextFunction
): void {
    console.error(`[ERROR] ${err.name}: ${err.message}`);
    if (process.env.NODE_ENV === "development") {
        console.error(err.stack);
    }

    if (err instanceof AppError) {
        // 自定义应用错误：按 statusCode 返回
        res.status(err.statusCode).json({
            error: {
                code: err.code,
                message: err.message,
                details: err.details,
            },
        });
    } else {
        // 未知错误：统一返回 500
        res.status(500).json({
            error: {
                code: "INTERNAL_ERROR",
                message: "An unexpected error occurred",
            },
        });
    }
}

// 注册全局错误处理中间件（必须放在所有路由之后）
app.use(errorHandler);
```

### 15.4.2 Result 类型模式在后端的实现

还记得第9章讲的 Result 类型模式吗？它在前端和后端都很有用，但在后端尤其重要——因为后端的错误往往需要传播到多个层次（数据库层 → 服务层 → 控制器层 → 中间件层），Result 类型让这个传播变得类型安全。

```typescript
// src/utils/result.ts

type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

// 构造器函数
function ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}

// 辅助函数：unwrap（安全地取值，失败则抛异常）
function unwrap<T>(result: Result<T>): T {
    if (!result.ok) throw result.error;
    return result.value;
}

// 辅助函数：map（对 ok 的值做变换，err 不变）
function map<T, U, E>(
    result: Result<T, E>,
    fn: (value: T) => U
): Result<U, E> {
    if (result.ok) {
        return ok(fn(result.value));
    }
    return result;
}

// 辅助函数：flatMap（链式调用）
function flatMap<T, U, E>(
    result: Result<T, E>,
    fn: (value: T) => Result<U, E>
): Result<U, E> {
    if (result.ok) {
        return fn(result.value);
    }
    return result;
}
```

在服务层使用 Result 类型：

```typescript
// src/services/UserService.ts

import { Result, ok, err } from "../utils/result";
import { PrismaClient } from "@prisma/client";
import { NotFoundError, ConflictError } from "../errors/AppError";

const prisma = new PrismaClient();

interface UserDTO {
    id: number;
    name: string;
    email: string;
}

async function findUserById(id: number): Promise<Result<UserDTO, NotFoundError>> {
    const user = await prisma.user.findUnique({ where: { id } });

    if (!user) {
        return err(new NotFoundError("User", id));
    }

    return ok({
        id: user.id,
        name: user.name,
        email: user.email,
    });
}

async function createUser(
    name: string,
    email: string
): Promise<Result<UserDTO, NotFoundError | ConflictError>> {
    const existing = await prisma.user.findUnique({ where: { email } });

    if (existing) {
        return err(new ConflictError(`Email ${email} already exists`));
    }

    const user = await prisma.user.create({ data: { name, email } });

    return ok({
        id: user.id,
        name: user.name,
        email: user.email,
    });
}

// 链式调用示例
async function getUserFullInfo(id: number) {
    const result = await findUserById(id);

    // flatMap：只有在 ok 的情况下才调用后续逻辑
    return flatMap(result, async (user) => {
        // 假设这里还要查用户的文章数
        const posts = await prisma.post.count({ where: { authorId: user.id } });
        return ok({ ...user, postsCount: posts });
    });
}
```

在控制器层处理 Result：

```typescript
// src/controllers/userController.ts

app.get("/user/:id", async (req, res) => {
    const id = parseInt(req.params.id, 10);

    if (isNaN(id)) {
        res.status(400).json({ error: "Invalid user id" });
        return;
    }

    const result = await findUserById(id);

    if (!result.ok) {
        res.status(result.error.statusCode).json({
            error: {
                code: result.error.code,
                message: result.error.message,
            },
        });
        return;
    }

    res.json(result.value);
});
```

---

## 15.5 单元测试

### 15.5.1 Vitest / Jest 与 TypeScript 配置

写后端不写测试？那你的代码就是"裸奔跑高速公路"。后端测试的主流工具是 **Vitest**（更快、更现代）或 **Jest**（更成熟、更普遍）。这里推荐 Vitest，因为它用 Vite 构建，测试运行速度比 Jest 快一个数量级。

安装 Vitest：

```bash
npm install -D vitest
```

配置 `vitest.config.ts`：

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
    test: {
        globals: true,             // 全局注入 test/expect，不用每次 import
        environment: "node",     // Node.js 环境（不是浏览器）
        coverage: {
            provider: "v8",
            reporter: ["text", "json", "html"],
            exclude: [
                "node_modules/",
                "dist/",
                "**/*.d.ts",
                "**/*.config.ts",
                "**/index.ts",
            ],
        },
        testTimeout: 10000,       // 单个测试的超时时间（毫秒）
    },
});
```

在 `package.json` 里加测试脚本：

```json
{
    "scripts": {
        "test": "vitest",
        "test:run": "vitest run",    // 单次运行（CI 友好）
        "coverage": "vitest run --coverage"
    }
}
```

写一个测试试试水：

```typescript
// src/utils/__tests__/result.test.ts

import { describe, it, expect } from "vitest";
import { ok, err, map, unwrap } from "../../utils/result";

describe("Result 类型", () => {
    it("ok() 应该创建成功结果", () => {
        const result = ok(42);
        expect(result.ok).toBe(true);
        expect(result.value).toBe(42);
    });

    it("err() 应该创建失败结果", () => {
        const error = new Error("oops");
        const result = err(error);
        expect(result.ok).toBe(false);
        expect(result.error).toBe(error);
    });

    it("map() 应该对 ok 的值做变换", () => {
        const doubled = map(ok(5), (n) => n * 2);
        expect(unwrap(doubled)).toBe(10);

        const errResult = err<number, Error>(new Error("fail"));
        const mapped = map(errResult, (n) => n * 2);
        expect(mapped.ok).toBe(false);
    });

    it("unwrap() 在 err 时应该抛出错误", () => {
        const result = err<never, Error>(new Error("test error"));
        expect(() => unwrap(result)).toThrow("test error");
    });
});
```

运行测试：

```bash
npm run test:run
# 输出：
#  ✓ src/utils/__tests__/result.test.ts (4 tests)
#   Result 类型
#     ✓ ok() 应该创建成功结果
#     ✓ err() 应该创建失败结果
#     ✓ map() 应该对 ok 的值做变换
#     ✓ unwrap() 在 err 时应该抛出错误
#
# Test Files  1 passed (1)
# Tests       4 passed (4)
```

### 15.5.2 Mock 函数的类型化

测试里最难搞的部分就是**外部依赖**——数据库、第三方 API、文件系统，这些都不应该在单元测试里真实调用，而是用 Mock（模拟对象）来替代。

Vitest 提供了 `vi.fn()` 来创建 Mock 函数：

```typescript
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";

// 假设我们有一个 UserService，依赖 Prisma Client
interface UserServiceDeps {
    prisma: {
        user: {
            findUnique: (args: { where: { id: number } }) => Promise<unknown>;
            create: (args: { data: { name: string; email: string } }) => Promise<unknown>;
        };
    };
}

function createUserService(deps: UserServiceDeps) {
    return {
        async getUserById(id: number) {
            return deps.prisma.user.findUnique({ where: { id } });
        },

        async createUser(name: string, email: string) {
            return deps.prisma.user.create({
                data: { name, email },
            });
        },
    };
}

describe("UserService", () => {
    // 创建一个 mock 的 prisma client
    const mockPrisma = {
        user: {
            findUnique: vi.fn(),
            create: vi.fn(),
        },
    };

    const userService = createUserService({ prisma: mockPrisma });

    beforeEach(() => {
        // 每个测试前清空所有 mock 调用记录
        vi.clearAllMocks();
    });

    afterEach(() => {
        // 每个测试后重置 mock 状态
        vi.resetAllMocks();
    });

    it("getUserById 应该返回用户数据", async () => {
        const mockUser = { id: 1, name: "张三", email: "zhangsan@example.com" };
        mockPrisma.user.findUnique.mockResolvedValue(mockUser);

        const result = await userService.getUserById(1);

        expect(result).toEqual(mockUser);
        expect(mockPrisma.user.findUnique).toHaveBeenCalledWith({ where: { id: 1 } });
        expect(mockPrisma.user.findUnique).toHaveBeenCalledTimes(1);
    });

    it("getUserById 在用户不存在时应该返回 null", async () => {
        mockPrisma.user.findUnique.mockResolvedValue(null);

        const result = await userService.getUserById(999);

        expect(result).toBeNull();
    });

    it("createUser 应该调用 prisma.create 并返回创建的用户", async () => {
        const newUser = { id: 2, name: "李四", email: "lisi@example.com" };
        mockPrisma.user.create.mockResolvedValue(newUser);

        const result = await userService.createUser("李四", "lisi@example.com");

        expect(result).toEqual(newUser);
        expect(mockPrisma.user.create).toHaveBeenCalledWith({
            data: { name: "李四", email: "lisi@example.com" },
        });
    });
});
```

**Mock 函数的类型安全**：如果你在 `vi.fn()` 上调用了 `mockResolvedValue`，TypeScript 会记住这个 mock 函数的返回类型，在 `await` 调用时会自动推断为对应的类型。

---

## 本章小结

本章完成了从零搭建一个 TypeScript 后端项目的全部流程。

### 项目初始化

`tsconfig.json` 的后端配置和前端完全不同，重点关注 `module: "NodeNext"`、`moduleResolution: "NodeNext"`、`strict: true`。环境变量用类型声明合并（d.ts 文件里的 `declare global`）来扩展 `process.env` 的类型。

### Express 与 Fastify 类型化

Express 通过路由泛型参数 `app.get<{ Params, Query, Reply }>()` 实现请求/响应类型化。Fastify 更进一步，用 **TypeBox** 从 JSON Schema 自动推断 TypeScript 类型，schema 即类型定义，两全其美。

### Prisma ORM

Prisma 的 schema 就是类型定义——写好 `schema.prisma`，运行 `prisma generate`，类型自动生成。查询参数和返回值全部类型化，是目前 TypeScript 生态里类型安全度最高的 ORM。

### 错误处理

自定义错误类继承体系 + 全局错误处理中间件，是后端错误处理的最佳实践。Result 类型模式让错误的传播和消费都变得类型安全，特别适合服务层→控制器层的错误传递。

### 单元测试

Vitest 是目前最推荐的后端测试框架，比 Jest 快很多。Mock 函数 `vi.fn()` 完全类型化，配合 `mockResolvedValue` / `mockRejectedValue` 可以优雅地模拟外部依赖。

> 写后端不用 TypeScript，就像骑电动车不戴头盔——不是不能骑，是出事了代价很大。
