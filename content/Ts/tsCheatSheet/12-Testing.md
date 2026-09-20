+++
title = "12 测试"
weight = 112
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "类型断言测试、各测试运行器的类型接入、mock 的类型安全、测试夹具与 CI 中的类型检查"
isCJKLanguage = true
draft = false
+++

# 12 测试

TypeScript 项目的测试有两类**完全不同**的测试目标：

| 目标 | 测什么 | 工具 |
| --- | --- | --- |
| **行为测试** | 运行时行为对不对 | Vitest / Jest / `node:test` / Playwright |
| **类型测试** | 类型推导对不对 | `expectTypeOf` / `tsd` / `expect-type` |

第二类是 TypeScript 特有的，也是最容易被忽略的——**泛型库的类型行为如果不测，重构时悄悄退化你都不会知道**。

> 当前版本参考：Vitest 5.0.1、Jest 30.5.2、`@playwright/test` 1.63.0、`tsd` 0.33.0、`expect-type` 1.4.0。

---

## 类型测试：测「类型」本身

{{< tabpane text=true persist=disabled >}}

{{% tab header="为什么需要" %}}

考虑一个泛型工具类型：

```typescript
export function pick<T extends object, K extends keyof T>(obj: T, keys: K[]): Pick<T, K> {
  const result = {} as Pick<T, K>;
  for (const k of keys) result[k] = obj[k];
  return result;
}
```

**行为测试能过，但类型可能悄悄坏了**：

```typescript
// 行为测试
expect(pick({ a: 1, b: 2 }, ["a"])).toEqual({ a: 1 });   // ✅ 通过

// 但如果有人把返回类型改成 Partial<Pick<T, K>>：
// 行为测试仍然通过！因为运行时行为没变。
// 只有类型测试能发现：
expectTypeOf(pick({ a: 1, b: 2 }, ["a"])).toEqualTypeOf<{ a: number }>();
// ❌ 类型测试失败：实际是 { a?: number }
```

| 只有类型测试能发现的退化 | 例子 |
| --- | --- |
| 返回类型被拓宽 | `{ a: 1 }` → `{ a: number }` |
| 可选性变化 | `{ a: string }` → `{ a?: string }` |
| 收窄丢失 | 联合被合并成宽类型 |
| 推断位置错误 | 泛型参数从错误的位置推断 |
| `readonly` 丢失 | 只读被去掉 |

> 🔥 **判断标准**：如果你的代码里有**泛型、条件类型、工具类型、重载**，就该有类型测试。纯业务代码通常不需要。

**类型测试的运行方式**：

| 方式 | 说明 |
| --- | --- |
| 混在普通测试里 | `expectTypeOf` 写在 `.test.ts` 中，`vitest typecheck` 跑 |
| 独立类型测试文件 | `*.test-d.ts`，由 `tsd` 或 `vitest --typecheck` 处理 |
| 纯编译检查 | 类型测试失败 = 编译失败 |

{{% /tab %}}

{{% tab header="Vitest 的 expectTypeOf" %}}

Vitest 内置类型断言，**无需运行时开销**（只在类型层面校验）。

```typescript
import { expectTypeOf, assertType, test } from "vitest";

test("pick 的类型", () => {
  const result = pick({ a: 1, b: "x" }, ["a"]);

  // 精确相等（最严格）
  expectTypeOf(result).toEqualTypeOf<{ a: number }>();

  // 可赋值性（较宽松）
  expectTypeOf(result).toMatchTypeOf<{ a: number }>();

  // 属性级断言
  expectTypeOf(result.a).toBeNumber();
  expectTypeOf(result).toHaveProperty("a");

  // 函数签名
  expectTypeOf(pick).parameters.toEqualTypeOf<[object, string[]]>();
  expectTypeOf(pick).returns.toEqualTypeOf<object>();
});

test("assertType 简写", () => {
  const n = 1;
  assertType<number>(n);       // ✅
  // assertType<string>(n);    // ❌ 编译失败
});
```

**常用断言方法**：

| 方法 | 用途 |
| --- | --- |
| `.toEqualTypeOf<T>()` | **精确相等**，最严格 🔥 |
| `.toMatchTypeOf<T>()` | 可赋值（子类型即可） |
| `.toBeString()` / `.toBeNumber()` / `.toBeBoolean()` | 基础类型 |
| `.toBeAny()` / `.toBeNever()` / `.toBeUnknown()` | 特殊类型 |
| `.toBeNullable()` | 含 `null`/`undefined` |
| `.toHaveProperty("x")` | 有某属性 |
| `.parameter(n)` / `.parameters` | 函数参数 |
| `.returns` | 函数返回值 |
| `.instanceOf<T>()` | 实例类型 |
| `.branded` | 品牌类型 |

```typescript
// 测「不能赋值」也要覆盖
test("错误用法应当编译失败", () => {
  // @ts-expect-error 键不存在
  pick({ a: 1 }, ["typo"]);

  // @ts-expect-error 参数类型不对
  pick({ a: 1 }, [1]);
});
```

⚠️ **必须开 `typecheck`**，否则 `expectTypeOf` 只做运行时空操作：

```bash
npx vitest --typecheck          # 跑类型测试
npx vitest --typecheck.only     # 只跑类型测试
```

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    typecheck: {
      enabled: true,
      include: ["**/*.test-d.ts"],   // 类型测试单独命名
    },
  },
});
```

{{% /tab %}}

{{% tab header="tsd / expect-type（库专用）" %}}

给**发布的库**做类型测试的标准工具。

**`tsd`**（0.33.0）——独立运行，通过编译判断：

```typescript
// test-d/index.test-d.ts
import { expectType, expectError, expectAssignable } from "tsd";
import { pick } from "../src/index.js";

// 精确返回类型
expectType<{ a: number }>(pick({ a: 1, b: 2 }, ["a"]));

// 可赋值
expectAssignable<{ a: number }>(pick({ a: 1 }, ["a"]));

// 断言某个用法应当报错
expectError(pick({ a: 1 }, ["nope"]));

// 测泛型推断位置
expectType<number>(pick({ a: 1 }, ["a"]).a);
```

```jsonc
// package.json
{
  "scripts": { "test:types": "tsd" },
  "tsd": { "directory": "test-d" }
}
```

**`expect-type`**（1.4.0）——不依赖测试框架，纯编译期：

```typescript
import { expectTypeOf } from "expect-type";

expectTypeOf<{ a: number }>().toEqualTypeOf<{ a: number }>();
expectTypeOf(pick({ a: 1 }, ["a"])).toEqualTypeOf<{ a: number }>();
```

| 工具 | 集成方式 | 适合 |
| --- | --- | --- |
| `expectTypeOf`（Vitest） | 已在用 Vitest | 应用项目 🔥 |
| `tsd` | 独立命令 | 发布库的 API 契约 🔥 |
| `expect-type` | 无框架依赖 | 想避免绑定框架 |

> 💡 **发布库强烈建议加 `tsd`**：它能在 CI 里验证「公开 API 的类型行为」——这正是使用者最依赖、又最容易在重构中悄悄破坏的东西。见 [13 发布库]({{< relref "13-Publishing-Libraries-with-Types.md" >}})。

{{% /tab %}}

{{% tab header="手写类型断言（零依赖）" %}}

不想引工具时，用这个经典模式：

```typescript
// 类型相等判断
type Eq<A, B> =
  (<T>() => T extends A ? 1 : 2) extends (<T>() => T extends B ? 1 : 2)
    ? true
    : false;

// 编译期断言：只有为 true 才通过
type Expect<T extends true> = T;

// 用法
type _1 = Expect<Eq<ReturnType<typeof pick<{ a: number }, "a">>, { a: number }>>;
// ✅ 编译通过

type _2 = Expect<Eq<ReturnType<typeof pick<{ a: number }, "a">>, { a?: number }>>;
// ❌ TS2344: Type 'false' does not satisfy the constraint 'true'.
```

（此模式已在 TS 6.0.3 实测：正确断言通过，错误断言报 `TS2344`。）

| 要点 | 说明 |
| --- | --- |
| 用 `type _1 = ...` | 以类型别名形式触发检查 |
| 下划线前缀 | 表明「只为检查而存在」 |
| `Eq` 而非 `extends` | `extends` 判不出 `any`，`Eq` 才能精确判断 |
| 断言写在哪里 | 紧挨实现，或单独 `types.test-d.ts` |

⚠️ **手写断言不会运行**——它们只在类型检查时生效。所以要确保这些文件**在 `tsc --noEmit` 的范围内**（在 `include` 里）。

{{% /tab %}}

{{< /tabpane >}}

---

## 测试工程的类型配置

{{< tabpane text=true persist=disabled >}}

{{% tab header="tsconfig 怎么组织" %}}

**问题**：测试文件的类型需求和源码往往不同（需要测试框架全局、可能需要 DOM、有时候比源码宽松）。

| 方案 | 做法 | 适合 |
| --- | --- | --- |
| 单一 tsconfig | `include` 同时含 `src` 和 `tests` | 小项目 ✅ 简单 |
| 分离 tsconfig | `tsconfig.json` + `tsconfig.test.json` | 需要不同 `types`/`lib` |
| 项目引用 | `references` 指向测试项目 | monorepo 🔥 |

**方案一：单一配置**（最简单）

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "types": ["node", "vitest/globals"],
    "rootDir": ".",
    "noEmit": true
  },
  "include": ["src", "tests"]
}
```

**方案二：分离配置**（测试需要更宽的类型时）

```jsonc
// tsconfig.json —— 只管源码
{
  "compilerOptions": {
    "strict": true,
    "types": ["node"],
    "rootDir": "./src",
    "outDir": "./dist"
  },
  "include": ["src"]
}
```

```jsonc
// tsconfig.test.json —— 覆盖测试目录
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    "types": ["node", "vitest/globals"],
    "noEmit": true,
    "rootDir": "."
  },
  "include": ["src", "tests"]
}
```

```jsonc
// package.json
{
  "scripts": {
    "typecheck": "tsc --noEmit -p tsconfig.json",
    "test": "vitest",
    "test:types": "tsc --noEmit -p tsconfig.test.json"
  }
}
```

> 🔥 **CI 里两个都要跑**：`tsconfig.json` 保证产物类型正确，`tsconfig.test.json` 保证测试代码本身类型正确。只跑一个会漏。

⚠️ **常见坑**：测试文件被包含进**产物编译**，导致 `dist` 里出现 `*.test.js`。修法：

```jsonc
{
  "exclude": ["**/*.test.ts", "**/*.spec.ts", "tests"]
}
```

{{% /tab %}}

{{% tab header="测试框架的全局类型" %}}

6.0 的 `types` 默认为 `[]`，**测试框架的全局不再自动可用**。

| 框架 | 全局注入方式 | `types` 写法 |
| --- | --- | --- |
| **Vitest**（开 `globals: true`） | `types: ["vitest/globals"]` | `["vitest/globals"]` |
| **Vitest**（不开 globals） | 从 `vitest` 显式 import | 不需要 |
| **Jest** | `@types/jest` | `["jest"]` |
| **Jest**（`@jest/globals`） | 显式 import | 不需要 |
| **`node:test`** | 显式 import | `["node"]` |
| **Playwright** | 显式 import | 不需要 |

```typescript
// ❌ 报 Cannot find name 'describe'
describe("x", () => { it("y", () => {}); });
```

```jsonc
// ✅ Vitest 开 globals 的配置
{ "compilerOptions": { "types": ["vitest/globals"] } }
```

```typescript
// ✅ 更推荐：显式导入，不依赖全局
import { describe, it, expect, vi } from "vitest";
```

```typescript
// ✅ Jest 的显式导入形式
import { describe, it, expect, jest } from "@jest/globals";
```

```typescript
// ✅ node:test（Node 内置，无需框架）
import { test, describe, it, before, beforeEach, mock } from "node:test";
import assert from "node:assert/strict";

describe("suite", () => {
  beforeEach(() => { /* 准备 */ });

  it("基本断言", () => {
    assert.equal(1 + 1, 2);
  });

  test("mock 用法", () => {
    const fn = mock.fn((x: number) => x * 2);
    fn(2);
    assert.equal(fn.mock.callCount(), 1);
    assert.equal(fn.mock.calls[0]?.arguments[0], 2);   // ⚠️ 注意 ?. 
  });
});
```

（`node:test` 上述用法已在 Node v24.20.0 + `@types/node` 实测编译通过。）

> 💭 **显式 import 优于全局类型**：编译更快、依赖清晰、不同测试框架可以共存、不污染全局。只有为了少写几行 import 才用 globals。

{{% /tab %}}

{{% tab header="E2E 与浏览器测试" %}}

```typescript
// Playwright：类型从 @playwright/test 显式导入
import { test, expect, type Page } from "@playwright/test";

test("登录流程", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("邮箱").fill("a@b.c");
  await page.getByRole("button", { name: "登录" }).click();

  await expect(page.getByRole("heading")).toHaveText("欢迎");
});
```

| 要点 | 说明 |
| --- | --- |
| 用 `getByRole` / `getByLabel` | 语义定位，比 CSS 选择器稳定 |
| `expect` 来自 `@playwright/test` | ⚠️ 不是 Vitest 的 `expect`，别混用 |
| `type Page` 显式导入 | 抽 page object 时用 |
| 自动等待 | Playwright 的断言自带重试，不需要手写 `waitFor` |

**Page Object 模式 + 类型**：

```typescript
import { type Page, type Locator, expect } from "@playwright/test";

export class LoginPage {
  readonly email: Locator;
  readonly password: Locator;
  readonly submit: Locator;

  constructor(private readonly page: Page) {
    this.email = page.getByLabel("邮箱");
    this.password = page.getByLabel("密码");
    this.submit = page.getByRole("button", { name: "登录" });
  }

  async login(email: string, password: string): Promise<void> {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submit.click();
  }

  async expectError(msg: string): Promise<void> {
    await expect(this.page.getByRole("alert")).toHaveText(msg);
  }
}
```

> ⚠️ **`private readonly page: Page` 是参数属性**，会生成运行时代码，因此**不能**通过 `erasableSyntaxOnly`。若开了该选项或在写 Playwright（它自己转译 TS），需要手写字段：

```typescript
export class LoginPage {
  readonly email: Locator;
  private readonly page: Page;

  constructor(page: Page) {
    this.page = page;
    this.email = page.getByLabel("邮箱");
  }
}
```

{{% /tab %}}

{{< /tabpane >}}

---

## Mock 的类型安全

Mock 是**类型最容易失守**的地方——因为大家习惯用 `as any` 糊过去。

{{< tabpane text=true persist=disabled >}}

{{% tab header="函数 mock" %}}

```typescript
import { vi, expect, test } from "vitest";

// ✅ 带类型参数的 mock：参数和返回值都受约束
const add = vi.fn((a: number, b: number): number => a + b);

add(1, 2);        // ✅
add("1", 2);      // ❌ TS2345: 参数类型不符 —— mock 也有类型检查！
const r: number = add(1, 2);   // ✅ 返回值类型正确

// ✅ jest 等价写法
import { jest } from "@jest/globals";
const addJest = jest.fn((a: number, b: number): number => a + b);
```

| 需求 | Vitest | Jest |
| --- | --- | --- |
| 创建 mock | `vi.fn(impl)` | `jest.fn(impl)` |
| 控制返回值 | `mockReturnValue(v)` | 同 |
| 一次性返回 | `mockReturnValueOnce(v)` | 同 |
| 模拟实现 | `mockImplementation(fn)` | 同 |
| 断言调用 | `expect(fn).toHaveBeenCalledWith(...)` | 同 |
| 断言次数 | `expect(fn).toHaveBeenCalledTimes(n)` | 同 |

> 🔥 **关键**：`vi.fn` / `jest.fn` **会保留实现的类型**。只要你不写 `as any`，mock 的参数和返回值都会被检查。**mock 也需要正确**。

**mock 依赖对象的方法**（`vi.mocked`）：

```typescript
import { vi, expect, test } from "vitest";
import * as api from "./api";

// mock 整个模块
vi.mock("./api");

test("使用 mock 后的模块", () => {
  // ✅ vi.mocked 让被 mock 的函数保留原签名
  vi.mocked(api.fetchUser).mockResolvedValue({ id: 1, name: "a", email: "a@b.c" });

  // ❌ 若返回的数据不符合 User，这里会报错
  // vi.mocked(api.fetchUser).mockResolvedValue({ id: "1" });
});
```

```typescript
// Jest 等价：jest.mocked
import { jest } from "@jest/globals";
jest.mock("./api");
jest.mocked(api.fetchUser).mockResolvedValue({ id: 1, name: "a", email: "a@b.c" });
```

⚠️ **`vi.mock` 的路径必须与 import 路径一致**，否则 mock 不生效——这是最常见的 mock 问题（`vi.mock` 会被提升到文件顶部）。

{{% /tab %}}

{{% tab header="部分 mock 与 spy" %}}

**只替换对象的一个方法，保留其余**：

```typescript
import { vi, expect, test } from "vitest";

test("部分 mock", () => {
  const logger = {
    info: vi.fn(),
    error: vi.fn(),
    debug: (msg: string) => console.debug(msg),   // 保留真实实现
  };

  doWork(logger);

  expect(logger.info).toHaveBeenCalled();
  expect(logger.error).not.toHaveBeenCalled();
});
```

**Spy 真实对象**（调用真实实现，同时记录）：

```typescript
import { vi, expect, test, afterEach } from "vitest";

test("spy 会调用真实实现", () => {
  const spy = vi.spyOn(console, "warn").mockImplementation(() => {});   // 静音
  riskyOperation();
  expect(spy).toHaveBeenCalledWith(expect.stringContaining("deprecated"));
  spy.mockRestore();      // ✅ 必须还原！
});
```

| 手段 | 是否调用真实实现 | 用途 |
| --- | --- | --- |
| `vi.fn()` | ❌ 不调用 | 完全替代 |
| `vi.spyOn(obj, "m")` | ✅ **调用** | 观察真实行为 |
| `vi.spyOn(...).mockImplementation()` | ❌ 替换 | 观察 + 替换 |
| `vi.mocked(fn)` | 取决于 `vi.mock` | 类型安全地访问 mock |

> ⚠️ **`vi.spyOn` 会污染全局对象**，测试之间会互相影响。用 `afterEach(() => vi.restoreAllMocks())` 或配置 `restoreMocks: true`。

**用 `satisfies` 构造类型安全的 mock 对象**：

```typescript
import { expect, test } from "vitest";

interface Logger {
  info(msg: string): void;
  error(msg: string, err?: unknown): void;
}

test("部分 mock 的对象", () => {
  // ✅ satisfies 保证 mock 对象符合接口，同时保留 mock 的具体类型
  const logger = {
    info: vi.fn(),
    error: vi.fn(),
  } satisfies Logger;

  doWork(logger);

  expect(logger.info).toHaveBeenCalledWith("started");
  // logger.info 仍是 Mock 类型，有 toHaveBeenCalledWith ✅
});
```

> 🔥 `satisfies` 在这里是**最理想的工具**：既校验 mock 覆盖了接口（少写一个方法就报错），又**不拓宽**类型（还能访问 mock 专用方法）。用 `: Logger` 注解会把 mock 方法擦掉。

{{% /tab %}}

{{% tab header="避免 as any 的替代方案" %}}

```typescript
// 🛑 常见但危险：mock 与真实类型脱节，接口改了测试还能过
const mockRepo = {
  findById: vi.fn().mockResolvedValue({ id: 1 } as any),
} as any as Repository;
```

```typescript
// ✅ 方案 1：satisfies + 明确返回值类型
import { vi } from "vitest";

const mockRepo = {
  findById: vi.fn(async (id: string): Promise<User | null> => ({ id, name: "a", email: "a@b.c" })),
  save: vi.fn(async (u: User): Promise<void> => {}),
} satisfies Repository;
```

```typescript
// ✅ 方案 2：用测试数据工厂，保证数据符合类型
function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: 1,
    name: "测试用户",
    email: "test@example.com",
    ...overrides,     // ✅ 覆盖也是类型安全的
  };
}

const u = makeUser({ name: "自定义" });      // ✅
const bad = makeUser({ nmae: "拼错" });      // ❌ TS2353: 拼写错误被抓到
```

```typescript
// ✅ 方案 3：只 mock 用到的部分，用 unknown 过渡而不是 any
function fakeResponse<T>(data: T): Response {
  return {
    ok: true,
    status: 200,
    json: async () => data,
  } as unknown as Response;      // ⚠️ 这里仍需要断言，但被限制在一个地方
}
```

| 反模式 | 问题 | 替代 |
| --- | --- | --- |
| `as any` 造 mock | 接口变化时测试静默通过 | `satisfies` 🔥 |
| 复制一份接口定义 | 会与真实接口脱节 | 直接用真实类型 |
| mock 所有方法 | 冗余且易过时 | 只 mock 用到的 |
| 测试里硬编码大对象 | 难维护 | 数据工厂函数 |
| `@ts-ignore` 在测试里 | 积累技术债 | `@ts-expect-error` + 说明 |

> 💭 **测试代码的类型严格度不应低于源码**。很多人觉得「反正是测试」就放松要求，结果是**接口改了、测试还绿**——测试失去了保护作用。上面 `satisfies` 的写法成本极低，收益很大。

{{% /tab %}}

{{< /tabpane >}}

---

## 测试夹具与数据工厂

```typescript
import { test, expect } from "vitest";

interface User {
  id: string;
  name: string;
  email: string;
  role: "admin" | "user";
  createdAt: Date;
}

// 基础工厂：所有字段有合理默认值
function makeUser(overrides: Partial<User> = {}): User {
  return {
    id: crypto.randomUUID(),
    name: "测试用户",
    email: "test@example.com",
    role: "user",
    createdAt: new Date("2026-01-01"),
    ...overrides,
  };
}

// 派生工厂：预设特定状态
const makeAdmin = (o: Partial<User> = {}) => makeUser({ role: "admin", ...o });

// 用法
test("管理员有额外权限", () => {
  const admin = makeAdmin({ name: "管理员" });
  expect(can(admin, "delete")).toBe(true);
});
```

**工厂模式的价值**：

| 好处 | 说明 |
| --- | --- |
| 新增字段只改一处 | 不用改几十个测试 🔥 |
| `Partial` + `satisfies` 保证类型 | 拼错字段名会报错 |
| 测试意图清晰 | 只写「与本测试相关的字段」 |
| 减少硬编码噪音 | 默认值集中管理 |

**用 `satisfies` 做测试数据表**：

```typescript
test.each([
  { input: "", expected: false, desc: "空字符串" },
  { input: "a@b.c", expected: true, desc: "合法邮箱" },
  { input: "no-at", expected: false, desc: "缺 @" },
] satisfies { input: string; expected: boolean; desc: string }[])(
  "$desc: $input -> $expected",
  ({ input, expected }) => {
    expect(isValidEmail(input)).toBe(expected);
  },
);
```

> 💡 `satisfies` 让 `test.each` 的表**也有类型检查**——写错字段名或类型会立刻报错，而不是运行时才发现 `expected` 是 `undefined`。

**测异步错误**：

```typescript
import { test, expect } from "vitest";

test("缺少参数时抛错", async () => {
  // ✅ 断言 Promise reject
  await expect(fetchUser("")).rejects.toThrow("id 不能为空");

  // ✅ 断言错误类型（配合自定义错误类）
  await expect(fetchUser("x")).rejects.toBeInstanceOf(NotFoundError);

  // ⚠️ 检查错误对象的具体属性
  await expect(fetchUser("x")).rejects.toMatchObject({ code: "NOT_FOUND" });
});

test("同步抛错", () => {
  expect(() => parse("bad")).toThrow(SyntaxError);

  // 拿到错误实例做进一步断言
  try {
    parse("bad");
    expect.unreachable("应当抛错");      // ✅ 没抛错就让测试失败
  } catch (e) {
    expect(e).toBeInstanceOf(SyntaxError);
    expect((e as SyntaxError).message).toContain("unexpected");
  }
});
```

| 断言 | 用途 |
| --- | --- |
| `.rejects.toThrow(msg)` | 异步抛错及消息 |
| `.rejects.toBeInstanceOf(Cls)` | 错误类型 |
| `.rejects.toMatchObject({...})` | 错误的部分属性 |
| `expect.unreachable()` | 断言「不该走到这里」 |
| `.resolves.toEqual(...)` | 异步成功值 |

⚠️ **不要忘记 `await`**——`expect(promise).rejects` 不 `await` 的话断言不会执行，测试**永远是绿的**：

```typescript
// 🛑 永远通过（漏了 await）
test("坏测试", () => {
  expect(fetchUser("")).rejects.toThrow();
});

// ✅ 正确
test("好测试", async () => {
  await expect(fetchUser("")).rejects.toThrow();
});
```

> 🔥 这类 bug 极其隐蔽。可以开 ESLint 规则 `@typescript-eslint/no-floating-promises` 来兜住——它依赖类型信息，正好是 TS 生态独有的能力。

---

## CI 中的类型检查

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: npm
      - run: npm ci

      # 🔥 类型检查（打包器/测试框架都不做这件事）
      - run: npx tsc --noEmit

      # 测试代码的类型
      - run: npx tsc --noEmit -p tsconfig.test.json

      # 类型测试（如果用 tsd）
      - run: npx tsd

      # 行为测试
      - run: npm test
```

| 步骤 | 为什么必须有 |
| --- | --- |
| `tsc --noEmit` | 打包器（esbuild/SWC/Vite）**不做类型检查** 🔥 |
| 测试代码类型检查 | 测试代码也是代码 |
| `tsd` / 类型测试 | 保证公开 API 类型不退化 |
| 测试运行 | 行为正确性 |

**`@ts-expect-error` 的自动化治理**：

```bash
# 统计数量，作为技术债指标
grep -rn "@ts-expect-error" src --include="*.ts" --include="*.tsx" | wc -l

# 检查是否有「未使用的 expect-error」（TS 会报 TS2578，CI 里自然会被抓到）
npx tsc --noEmit
```

```typescript
// ✅ @ts-expect-error 的好处：上游修好后会自动变成错误，提醒你删掉
// @ts-expect-error 库的类型定义缺少该重载，见 issue #123
legacyCall(x);
```

⚠️ `@ts-expect-error` **没有用处时**会报错：

```text
error TS2578: Unused '@ts-expect-error' directive.
```

这是**特性而不是麻烦**——它保证每条抑制指令都对应一个真实的类型问题，不会无限堆积。

**覆盖率与类型的关系**：

| 指标 | 测什么 | 类型能替代吗 |
| --- | --- | --- |
| 语句覆盖率 | 代码是否被执行 | ❌ 不能 |
| 类型检查 | 类型是否自洽 | ❌ 不能替代测试 |
| 类型测试 | 类型推导是否符合预期 | ✅ 独有价值 🔥 |

> 💭 **类型检查和测试是互补的，不是替代关系**。类型检查能排除一整类错误（拼写、结构不符、漏处理分支），但**不能证明逻辑正确**。100% 类型安全 + 0 个测试 = 一运行就错。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| 忘了 `await expect(...).rejects` | 测试永远通过 🛑 | 加 `await` |
| `as any` 造 mock | 接口改了测试还绿 | 用 `satisfies` |
| 用 `: Interface` 注解 mock 对象 | mock 方法类型被擦掉 | 用 `satisfies Interface` |
| 测试文件进了产物 | `dist` 里有 `.test.js` | `exclude` 测试文件 |
| 6.0 下 `describe` 找不到 | `types` 默认 `[]` | `["vitest/globals"]` |
| 没开 `--typecheck` | `expectTypeOf` 是空操作 | 开 `vitest --typecheck` |
| 类型测试文件不在 `include` | 断言不生效 | 确保被 `tsc` 覆盖 |
| `vi.spyOn` 没还原 | 测试互相污染 | `restoreMocks: true` |
| 手写断言用 `extends` 判 `any` | 永远为真 | 用 `Eq<A, B>` |
| 只跑框架测试不跑 `tsc` | 类型错误漏进主干 | CI 里两个都跑 🔥 |
| 参数属性在 `erasableSyntaxOnly` 下报错 | `TS1294` | 手写字段赋值 |
