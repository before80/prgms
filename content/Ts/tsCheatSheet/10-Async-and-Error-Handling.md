+++
title = "10 异步与错误处理"
weight = 110
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "Promise 与组合子的类型、Awaited、async 函数陷阱、错误类型建模与 using 资源管理"
isCJKLanguage = true
draft = false
+++

# 10 异步与错误处理

异步代码的类型问题集中在两处：**组合子的返回类型**（很多人记不清）和**错误的类型建模**（`catch` 变量为什么是 `unknown`）。

> 组合子返回类型由 `Eq<A, B>` 断言在 TS 6.0.3 实测确认。

---

## Promise 与组合子

{{< tabpane text=true persist=disabled >}}

{{% tab header="返回类型速查" %}}

实测结果，直接抄：

| 表达式 | 返回类型 |
| --- | --- |
| `Promise.all([Promise.resolve(1), Promise.resolve("a")])` | `Promise<[number, string]>` 🔥 **元组** |
| `Promise.all([...] as const)` | `Promise<readonly [number, string]>` |
| `Promise.allSettled([Promise.resolve(1)])` | `Promise<[PromiseSettledResult<number>]>` |
| `Promise.race([Promise.resolve(1), Promise.resolve("a")])` | `Promise<string \| number>` |
| `Promise.any([Promise.resolve(1), Promise.resolve("a")])` | `Promise<string \| number>` |
| `Promise.resolve(1).then((n) => n.toFixed())` | `Promise<string>` |
| `(async () => 1)()` | `Promise<number>` |

**关键差异**：

| 组合子 | 何时 resolve | 何时 reject | 结果类型 |
| --- | --- | --- | --- |
| `all` | **全部**成功 | **任一**失败 | 元组（保位置）🔥 |
| `allSettled` | **总是** | 永不 | 每个元素包成 `PromiseSettledResult` |
| `race` | 第一个 settle（成功或失败） | 第一个失败 | 联合 |
| `any` | 第一个成功 | **全部**失败 | 联合 |

```typescript
// all：类型安全地并行取多个不同数据
const [user, posts] = await Promise.all([
  fetchUser(id),      // Promise<User>
  fetchPosts(id),     // Promise<Post[]>
]);
// user: User，posts: Post[]  ✅ 位置和类型都精确

// allSettled：需要「部分成功」时
const results = await Promise.allSettled([fetchUser(id), fetchPosts(id)]);
for (const r of results) {
  if (r.status === "fulfilled") {
    r.value;    // ✅ 收窄后可访问
  } else {
    r.reason;   // unknown ⚠️ 见下文错误处理
  }
}
```

```typescript
// PromiseSettledResult 的定义（简化）
type PromiseSettledResult<T> =
  | { status: "fulfilled"; value: T }
  | { status: "rejected"; reason: any };   // ⚠️ reason 是 any
```

> ⚠️ `PromiseSettledResult.reason` 的类型是 **`any`**，不是 `unknown`。这是标准库的定义，用的时候要自己当心——见本页「错误的类型建模」。

⚠️ **`Promise.all` 的空数组**：

```typescript
const empty = await Promise.all([]);
// 类型是 []，不是 never[]；运行时是空数组
```

⚠️ **`Promise.all` 混入非 Promise**：TS 会自动包装，但类型仍按原值算：

```typescript
const r = await Promise.all([Promise.resolve(1), 2, "a"]);
// [number, number, string]  ✅ 字面量也能混入
```

{{% /tab %}}

{{% tab header="Awaited 与解包" %}}

`Awaited<T>` 会**递归**解包 Promise 嵌套。

```typescript
type A = Awaited<Promise<string>>;                  // string
type B = Awaited<Promise<Promise<number>>>;         // number  ✅ 递归
type C = Awaited<string>;                           // string（不是 Promise 就原样返回）
type D = Awaited<Promise<string | Promise<number>>>; // string | number
```

**最实用的用法：从异步函数提取返回类型**

```typescript
async function fetchUser() {
  return { id: 1, name: "a" };
}

type FetchedUser = Awaited<ReturnType<typeof fetchUser>>;
// { id: number; name: string }  🔥
```

| 想要 | 写 |
| --- | --- |
| 异步函数的**返回数据类型** | `Awaited<ReturnType<typeof fn>>` 🔥 |
| 异步函数的 `Promise` 类型 | `ReturnType<typeof fn>` |
| 解包任意嵌套 | `Awaited<T>` |

> 💡 `ReturnType<typeof fetchUser>` 得到的是 `Promise<{...}>`，**直接用会错**。这是最常见的错误之一——记住外面套 `Awaited`。

**`async` 函数返回 `Promise<T>` 时不要重复包**：

```typescript
// ✅ 正确
async function a(): Promise<number> { return 1; }

// ⚠️ 合法但多余（TS 会自动展平）
async function b(): Promise<Promise<number>> { return Promise.resolve(1); }

// 🛑 常见错误：手动 new Promise 却没写 async 语义
function c(): Promise<number> {
  return 1;   // ❌ TS2322: Type 'number' is not assignable to type 'Promise<number>'.
}
```

**`async` 函数的返回类型标注规则**：

| 标注 | 实际返回 |
| --- | --- |
| `async function f(): Promise<number>` | ✅ 应写这个 |
| `async function f(): number` | ❌ `TS1064`: 返回值必须是 `Promise<T>` |
| `function f(): Promise<number>`（无 async） | 必须自己返回 Promise |

{{% /tab %}}

{{% tab header="类型安全的解包模式" %}}

`try/catch` 会丢失类型收窄，用判别联合替代更好。

```typescript
// 🛑 传统 try/catch：catch 里拿不到「成功值」的类型
async function bad() {
  try {
    const user = await fetchUser();
    const posts = await fetchPosts(user.id);
    return { user, posts };            // 类型能推出来
  } catch (e) {
    return { error: e };               // ⚠️ 返回值变成联合，调用方难处理
  }
}
```

```typescript
// ✅ Result 类型：把错误变成返回值的一部分
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

async function safeAsync<T>(p: Promise<T>): Promise<Result<T>> {
  try {
    return { ok: true, value: await p };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e : new Error(String(e)) };
  }
}

const r = await safeAsync(fetchUser());
if (r.ok) {
  r.value;    // ✅ 收窄到成功分支，类型完整
} else {
  r.error;    // Error
}
```

| 方案 | 优点 | 缺点 |
| --- | --- | --- |
| `try/catch` | 语言原生，直观 | 调用方容易忘；错误类型丢失 |
| Result 类型 | 类型完整，强制处理 🔥 | 代码略啰嗦 |
| 让异常冒泡到边界 | 简单 | 需要全局错误处理 |

```typescript
// 并行 + 逐个报告失败
async function settleAll<T extends readonly unknown[]>(
  promises: { [K in keyof T]: Promise<T[K]> },
): Promise<{ [K in keyof T]: Result<T[K]> }> {
  const results = await Promise.allSettled(promises);
  return results.map((r) =>
    r.status === "fulfilled"
      ? { ok: true as const, value: r.value }
      : { ok: false as const, error: r.reason }
  ) as never;
}
```

> 💭 **什么时候用 Result 而不是异常**：可预期的业务失败（校验不通过、资源不存在）用 Result；不可预期的意外（网络断了、bug）用异常冒泡到边界统一处理。全都用 Result 会让代码很啰嗦。

{{% /tab %}}

{{% tab header="取消与超时" %}}

`AbortController` / `AbortSignal` 是标准的取消机制。

```typescript
async function fetchWithTimeout(url: string, ms: number): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timer);       // ✅ 一定要清理，否则计时器泄漏
  }
}
```

| 类型 | 作用 |
| --- | --- |
| `AbortController` | 拥有 `signal`，调用 `abort()` 触发取消 |
| `AbortSignal` | 传给 API，被监听 |
| `AbortSignal.timeout(ms)` | 直接创建超时信号的静态方法 🆕 |
| `AbortSignal.any([...])` | 合并多个信号 🆕 |

```typescript
// 更简洁的超时写法（较新的运行时支持）
await fetch(url, { signal: AbortSignal.timeout(5000) });

// 合并用户取消 + 超时
await fetch(url, {
  signal: AbortSignal.any([userSignal, AbortSignal.timeout(5000)]),
});
```

⚠️ **`setTimeout` 的返回类型因环境而异**——这是跨平台代码的经典坑：

| `lib` 配置 | `setTimeout` 返回 |
| --- | --- |
| `["dom"]` | `number` |
| `["node"]`（`@types/node`） | `NodeJS.Timeout` |

```typescript
// 🛑 只在浏览器对，Node 下报错
const timer: number = setTimeout(() => {}, 0);

// ✅ 跨平台安全：不要标注类型
const timer = setTimeout(() => {}, 0);
clearTimeout(timer);

// ✅ 或显式用对应环境的类型
const t2: ReturnType<typeof setTimeout> = setTimeout(() => {}, 0);
```

> 🔥 `ReturnType<typeof setTimeout>` 是**跨平台写计时器类型的标准手法**。既能在浏览器用，也能在 Node 用，还不用引 `@types/node`。

{{% /tab %}}

{{< /tabpane >}}

---

## 错误的类型建模

{{< tabpane text=true persist=disabled >}}

{{% tab header="catch 变量为什么是 unknown" %}}

`useUnknownInCatchVariables`（随 `strict` 默认开启）让 `catch` 变量类型是 `unknown`。

```typescript
try {
  risky();
} catch (e) {
  e.message;
  // ~ ❌ TS18046: 'e' is of type 'unknown'.
}
```

**为什么改成 `unknown`**：JavaScript 里 `throw` 可以抛**任何值**，不只是 `Error`。

```typescript
throw "字符串";        // ✅ 合法
throw 42;             // ✅ 合法
throw { code: 1 };    // ✅ 合法
throw null;           // ✅ 合法
```

所以 `catch (e)` 里 `e` 声称是 `Error` 是**撒谎**。改成 `unknown` 强迫你处理。

**标准处理模板**：

```typescript
function toError(e: unknown): Error {
  if (e instanceof Error) return e;
  if (typeof e === "string") return new Error(e);
  return new Error(`未知错误: ${JSON.stringify(e)}`);
}

try {
  risky();
} catch (e) {
  const err = toError(e);    // ✅ 现在有完整的 Error 类型
  logger.error(err.message, { stack: err.stack });
}
```

| 收窄手段 | 适用 |
| --- | --- |
| `e instanceof Error` | 最常见的标准错误 ✅ |
| `e instanceof AppError` | 自定义错误类 |
| `typeof e === "string"` | 有人抛字符串 |
| 鸭子类型 `"message" in e` | 跨 realm 的 Error（`instanceof` 会失效）⚠️ |

```typescript
// 跨 realm 安全的判断（iframe、Worker 传来的 Error）
function isErrorLike(e: unknown): e is { message: string; stack?: string } {
  return typeof e === "object" && e !== null && "message" in e
    && typeof (e as { message: unknown }).message === "string";
}
```

{{% /tab %}}

{{% tab header="自定义错误类" %}}

```typescript
class AppError extends Error {
  constructor(
    message: string,
    readonly code: string,
    readonly statusCode = 500,
    options?: { cause?: unknown },
  ) {
    super(message, options);
    this.name = "AppError";
    // 修正原型链（target 低于 ES2015 时必需；现代 target 可省）
    Object.setPrototypeOf(this, AppError.prototype);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} 不存在`, "NOT_FOUND", 404);
    this.name = "NotFoundError";
  }
}

class ValidationError extends AppError {
  constructor(readonly issues: string[]) {
    super("校验失败", "VALIDATION", 400);
    this.name = "ValidationError";
  }
}
```

**用 `instanceof` 精确分发**（需要判别联合时是这样写）：

```typescript
function handle(e: unknown): Response {
  if (e instanceof ValidationError) {
    return json({ issues: e.issues }, e.statusCode);   // ✅ e.issues 可访问
  }
  if (e instanceof NotFoundError) {
    return json({ message: e.message }, e.statusCode);
  }
  if (e instanceof AppError) {
    return json({ code: e.code }, e.statusCode);
  }
  return json({ message: "内部错误" }, 500);
}
```

⚠️ **继承链顺序很重要**：`instanceof` 检查要**从最具体到最一般**。把 `AppError` 放在 `NotFoundError` 前面会把所有子类都吃掉。

**用 `cause` 保留原始错误**（ES2022）：

```typescript
try {
  await db.query(sql);
} catch (e) {
  throw new AppError("查询失败", "DB_ERROR", 500, { cause: e });
  // 原始错误保留在 err.cause 里
}

// 读取
if (e instanceof AppError && e.cause instanceof Error) {
  logger.debug("根因", e.cause.message);
}
```

| 要点 | 说明 |
| --- | --- |
| `this.name = "X"` | 不设的话序列化后全是 `"Error"` |
| `Object.setPrototypeOf` | 现代 `target` 下通常不需要 |
| `cause` | 保留原始错误链 🔥 |
| `readonly` 字段 | 参数属性顺带声明，简洁 |
| `instanceof` 顺序 | 具体在前，一般在后 |

{{% /tab %}}

{{% tab header="用判别联合替代错误类" %}}

错误类适合「用异常」，判别联合适合「用返回值」。

```typescript
// 判别联合建模错误
type ApiError =
  | { kind: "network"; cause: unknown }
  | { kind: "notFound"; resource: string }
  | { kind: "validation"; issues: string[] }
  | { kind: "server"; status: number; message: string };

type ApiResult<T> = { ok: true; data: T } | { ok: false; error: ApiError };

function describe(e: ApiError): string {
  switch (e.kind) {
    case "network":    return "网络错误";
    case "notFound":   return `${e.resource} 不存在`;     // ✅ e.resource 可访问
    case "validation": return `校验失败: ${e.issues.join(", ")}`;
    case "server":     return `服务端错误 ${e.status}`;
    default: {
      const _exhaustive: never = e;   // ✅ 新增错误类型时编译报错 🔥
      return _exhaustive;
    }
  }
}
```

**两种风格对比**：

| | 错误类 + `instanceof` | 判别联合 |
| --- | --- | --- |
| 新增错误类型 | ⚠️ 容易漏处理，运行时才发现 | ✅ `never` 检查强制处理 |
| 携带数据 | ✅ 类字段 | ✅ 每个分支自定义 |
| 序列化 | ⚠️ `Error` 序列化会丢信息 | ✅ 就是普通对象 |
| 可跨进程/网络传递 | ❌ | ✅ |
| 心智负担 | 熟悉异常的人更自然 | 更「函数式」 |

> 💭 **推荐组合**：**边界层用判别联合**（需要序列化、需要穷尽处理），**内部深层用异常**（省去层层传递 Result 的啰嗦），在边界处把异常转成联合。这也是很多成熟后端代码库的做法。

**`Error` 序列化的坑**：

```typescript
JSON.stringify(new Error("出错了"));
// "{}"  ⚠️ message、stack 全都丢了！因为它们是不可枚举属性

// ✅ 手动序列化
function serializeError(e: unknown) {
  if (e instanceof Error) {
    return { name: e.name, message: e.message, stack: e.stack };
  }
  return { name: "Unknown", message: String(e) };
}
```

{{% /tab %}}

{{< /tabpane >}}

---

## 资源管理与 `using` 🆕

TS 5.2 引入的**显式资源管理**，配合 `Symbol.dispose`。

```typescript
class FileHandle {
  constructor(readonly path: string) {}

  read() { return "文件内容"; }

  // 实现 Symbol.dispose，作用域结束时自动调用
  [Symbol.dispose]() {
    console.log(`关闭 ${this.path}`);
  }
}

function process() {
  using file = new FileHandle("./data.txt");
  return file.read();
  // 作用域退出时自动调用 file[Symbol.dispose]()  ✅
}
```

**同步与异步两种**：

| 语法 | 要求 | 何时调用 |
| --- | --- | --- |
| `using x = ...` | `Symbol.dispose` | 同步作用域退出 |
| `await using x = ...` | `Symbol.asyncDispose` | 异步作用域退出（可 await） |

```typescript
class DbConnection {
  async connect() {}
  async [Symbol.asyncDispose]() {
    await this.close();     // ✅ 支持异步清理
  }
}

async function query() {
  await using conn = new DbConnection();
  await conn.connect();
  return "结果";
  // 自动 await conn[Symbol.asyncDispose]()
}
```

**配套类型**（需要 `lib` 包含 `esnext.disposable` 或 `esnext`）：

```typescript
declare function getRes(): Disposable;
function f() {
  using r = getRes();     // ✅ 需 lib 含 Disposable 类型
  return r;
}
```

⚠️ **常见报错**：`Cannot find global type 'Disposable'`

```text
error TS2318: Cannot find global type 'Disposable'.
```

修法：`lib` 里加入 `esnext` 或 `esnext.disposable`：

```jsonc
{ "compilerOptions": { "lib": ["ES2023", "ESNext.Disposable", "DOM"] } }
```

| 特性 | 说明 |
| --- | --- |
| 自动清理 | 比 `try/finally` 更简洁，且**忘不了** 🔥 |
| 支持异步 | `await using` + `Symbol.asyncDispose` |
| 可用 `DisposableStack` | 组合多个资源，集中清理 |
| 需要 Node 24+ / 现代浏览器 | 运行时也要支持（TS 会降级辅助函数） |
| ⚠️ 与 `erasableSyntaxOnly` | `using` 是**擦除式语法**，可以共存 ✅ |

```typescript
// DisposableStack：一次管理多个资源
function multi() {
  using stack = new DisposableStack();
  const a = stack.use(new FileHandle("a"));
  const b = stack.use(new FileHandle("b"));
  return `${a.read()}${b.read()}`;
  // 退出时按 LIFO 顺序清理 ✅
}
```

> 💡 `using` 最大的价值是**异常安全**：即使中间抛异常，清理也一定执行，而且不需要你记得写 `finally`。

---

## 实战模式

### 带重试的异步调用

```typescript
type RetryOptions = {
  retries?: number;
  delayMs?: number;
  signal?: AbortSignal;
};

async function withRetry<T>(
  fn: () => Promise<T>,
  { retries = 3, delayMs = 1000, signal }: RetryOptions = {},
): Promise<T> {
  let lastError: unknown;
  for (let i = 0; i <= retries; i++) {
    try {
      return await fn();
    } catch (e) {
      lastError = e;
      if (i === retries) break;
      if (signal?.aborted) throw e;              // ✅ 取消优先
      await new Promise((r) => setTimeout(r, delayMs * 2 ** i));
    }
  }
  throw toError(lastError);
}
```

### 并发限流

```typescript
async function mapLimit<T, R>(
  items: readonly T[],
  limit: number,
  fn: (item: T, index: number) => Promise<R>,
): Promise<R[]> {
  const results = new Array<R>(items.length);
  let cursor = 0;

  async function worker(): Promise<void> {
    while (cursor < items.length) {
      const i = cursor++;
      const item = items[i];
      if (item === undefined) continue;   // ✅ noUncheckedIndexedAccess 下必需
      results[i] = await fn(item, i);
    }
  }

  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, () => worker()),
  );
  return results;
}
```

> ⚠️ 注意上面 `items[i]` 的 `undefined` 判断——这是 `noUncheckedIndexedAccess` 开启后的必然写法。**这不是麻烦，而是在提醒你索引可能越界**。

### 异步迭代

```typescript
async function* paginate<T>(
  fetchPage: (cursor?: string) => Promise<{ items: T[]; next?: string }>,
): AsyncGenerator<T, void, undefined> {
  let cursor: string | undefined;
  do {
    const page = await fetchPage(cursor);
    yield* page.items;
    cursor = page.next;
  } while (cursor);
}

// 消费
for await (const item of paginate(fetchPage)) {
  console.log(item);
}
```

| 类型 | 用途 |
| --- | --- |
| `AsyncGenerator<T, TReturn, TNext>` | `async function*` 的返回类型 |
| `AsyncIterable<T>` | 可被 `for await` 消费 |
| `for await (const x of it)` | 异步迭代语法 |

> ⚠️ `for await` 只接受 `AsyncIterable`。普通数组用不了——但**同步可迭代对象**可以在 `async` 函数里用普通 `for...of`。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 忘了 `Awaited` | 拿到 `Promise<T>` 而非 `T` | `Awaited<ReturnType<typeof fn>>` |
| `catch` 里直接用 `e.message` | `TS18046` | 先 `instanceof Error` 收窄 |
| 以为 `throw` 只能抛 Error | 类型撒谎 | 用 `toError` 归一化 |
| `Error` 直接 JSON 序列化 | 得到 `{}` | 手动提取 `message`/`stack` |
| `instanceof` 顺序反了 | 子类错误被父类吃掉 | 具体在前 |
| `setTimeout` 标注 `number` | Node 下报错 | `ReturnType<typeof setTimeout>` |
| 忘了 `clearTimeout` | 计时器泄漏 | `finally` 里清理 |
| 以为 `allSettled.reason` 是 `Error` | 实际是 `any` ⚠️ | 自己收窄 |
| `Promise.all` 空数组 | — | 类型是 `[]`，注意后续访问 |
| 异步函数忘了 `async` | `TS2322` 返回类型不符 | 加 `async` 或手动返回 Promise |
| `Symbol.dispose` 找不到类型 | `TS2318` | `lib` 加 `ESNext.Disposable` |
| 深层传递 Result | 代码啰嗦 | 内部用异常，边界转联合 |
