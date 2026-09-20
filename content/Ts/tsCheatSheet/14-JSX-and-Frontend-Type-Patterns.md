+++
title = "14 JSX 与前端类型模式"
weight = 114
date = "2026-03-27T10:00:00+08:00"
type = "docs"
description = "jsx 选项对照、组件与泛型组件写法、事件类型全表、Hook 推断陷阱与 CSS 模块声明"
isCJKLanguage = true
draft = false
+++

# 14 JSX 与前端类型模式

本页只讲**类型层面的模式**——组件签名、事件类型、Hook 推断。框架用法请查框架文档。

> ⚠️ 涉及 React 的具体 API 时，本页基于 React 19 的 `@types/react`。**类型包版本不同，细节可能有差异**，请以你项目里实际安装的 `.d.ts` 为准。

---

## `jsx` 选项

| `jsx` 取值 | 产物 | 需要引入 React | 运行时 |
| --- | --- | --- | --- |
| `preserve` | 保留 JSX 原样 | ❌ | 交给下游（Next.js 等） |
| `react` | `React.createElement(...)` | ✅ | 经典运行时 |
| `react-jsx` | `_jsx(...)` 自动导入 | ❌ | 自动运行时（React 17+）🔥 |
| `react-jsxdev` | 同上 + 调试信息 | ❌ | 开发模式 |
| `react-native` | 保留 JSX | ❌ | React Native |
| `solid` / `preact` 等 | 各自转换 | ❌ | 对应框架 |

```jsonc
// React 项目（生产）
{ "compilerOptions": { "jsx": "react-jsx" } }

// 打包器接管 JSX（Vite / Next.js 常见）
{ "compilerOptions": { "jsx": "preserve" } }

// Preact
{ "compilerOptions": { "jsx": "react-jsx", "jsxImportSource": "preact" } }
```

**TS 6.0 默认 `jsx: "preserve"`**（实测），所以 React 项目**必须显式配置**。

⚠️ **`jsxImportSource` 决定运行时来源**：

```jsonc
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "jsxImportSource": "react"        // 默认就是 react，一般不用写
  }
}
```

文件级覆盖（同一项目混用多个 JSX 运行时）：

```typescript
/** @jsxImportSource preact */
export function Widget() { return <div />; }
```

**经典运行时下的 `React` 作用域问题**（`jsx: "react"` 时的高频错误）：

```typescript
// 🛑 jsx: "react" 但没导入 React
export function Bad() {
  return <div>hi</div>;
}
// ❌ TS2874: This JSX tag requires 'React' to be in scope, but it could not be found.
// ❌ TS7026: JSX element implicitly has type 'any' because no interface
//            'JSX.IntrinsicElements' exists.
```

| 修法 | 做法 |
| --- | --- |
| 换自动运行时 | `jsx: "react-jsx"` ✅ 推荐 🔥 |
| 显式导入 | `import React from "react"` |
| 全局声明 | 不推荐 |

---

## 组件类型

{{< tabpane text=true persist=disabled >}}

{{% tab header="React.FC 的问题" %}}

```typescript
// ⚠️ 现代 React 里不推荐
const Card: React.FC<{ title: string }> = ({ title }) => (
  <div>{title}</div>
);
```

| `React.FC` 带来什么 | 问题 |
| --- | --- |
| 隐式 `children` | ⚠️ **React 18 的类型里已移除**；老类型里有，导致组件「意外接受 children」 |
| 固定返回 `ReactElement \| null` | 返回 `string`、数组、`undefined` 等都不行 ⚠️ |
| 泛型支持差 | 泛型组件写起来很别扭 |
| 增加一层间接 | 错误信息更难读 |

```typescript
// ✅ 推荐：直接写 props 类型
function Card({ title }: { title: string }) {
  return <div>{title}</div>;
}

// ✅ 需要 children 时显式声明
import type { ReactNode } from "react";

function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section><h2>{title}</h2>{children}</section>;
}

// ✅ 需要复用 props 类型时提取出来
interface CardProps { title: string; onSelect?: () => void }
function Card2({ title, onSelect }: CardProps) { /* ... */ }
```

> 💭 **判断标准**：`React.FC` 唯一「好处」是省一个类型名。但它在 children、返回类型、泛型三方面都更差。**直接标注 props 类型**是当前社区共识。

**常用 props 类型**：

| 类型 | 含义 |
| --- | --- |
| `ReactNode` | 任何可渲染内容（含 `string`、数组、`null`）🔥 |
| `ReactElement` | 单个 JSX 元素 |
| `JSX.Element` | 同上（全局 JSX 命名空间） |
| `React.ReactNode` | 同 `ReactNode` |
| `CSSProperties` | `style` 属性的类型 |
| `ComponentProps<"button">` | 原生元素的所有属性 🔥 |
| `ComponentProps<typeof Child>` | 另一个组件的 props 🔥 |

```typescript
import type { ComponentProps, ReactNode, CSSProperties } from "react";

// 扩展原生按钮的属性（最常见需求）
interface ButtonProps extends ComponentProps<"button"> {
  variant?: "primary" | "ghost";
}

function Button({ variant = "primary", ...rest }: ButtonProps) {
  return <button data-variant={variant} {...rest} />;
}

// ✅ 透传：onClick、disabled、type 等全都有正确类型
<Button onClick={(e) => e.currentTarget.disabled} type="submit" />;

// 复用另一个组件的 props
type CardProps = ComponentProps<typeof Card> & { footer?: ReactNode };
```

> 🔥 `ComponentProps<"div">` 比 `React.HTMLAttributes<HTMLDivElement>` 更好用：它包含的属性和真实 JSX 完全一致，不会漏也不会多。

{{% /tab %}}

{{% tab header="泛型组件" %}}

```typescript
// ✅ 泛型箭头函数：注意 <T,> 的逗号（避免与 JSX 语法冲突）
interface ListProps<T> {
  items: readonly T[];
  renderItem: (item: T, index: number) => ReactNode;
  keyOf: (item: T) => string | number;
}

function List<T>({ items, renderItem, keyOf }: ListProps<T>) {
  return (
    <ul>
      {items.map((item, i) => (
        <li key={keyOf(item)}>{renderItem(item, i)}</li>
      ))}
    </ul>
  );
}

// 使用：T 自动推断 ✅
<List
  items={users}
  keyOf={(u) => u.id}
  renderItem={(u) => <span>{u.name}</span>}   // ✅ u 是 User
/>;
```

**在 `.tsx` 里写泛型箭头组件的坑**：

```typescript
// 🛑 .tsx 里这会被当成 JSX 标签
const List = <T>(props: ListProps<T>) => <ul />;
//         ~ error TS17008: JSX element 'T' has no corresponding closing tag.

// ✅ 加一个逗号
const List2 = <T,>(props: ListProps<T>) => <ul />;

// ✅ 或加约束（有 extends 时不需要逗号）
const List3 = <T extends object>(props: ListProps<T>) => <ul />;
```

| 写法 | `.tsx` 下 |
| --- | --- |
| `<T>(...)` | ❌ 与 JSX 冲突 |
| `<T,>(...)` | ✅ |
| `<T extends unknown>(...)` | ✅ |
| `<T extends object>(...)` | ✅ |
| `function List<T>(...)` | ✅ 函数声明没问题 |

**多态组件**（`as` prop 模式）：

```typescript
import type { ComponentProps, ElementType } from "react";

type PolymorphicProps<E extends ElementType, P = object> = P & {
  as?: E;
} & Omit<ComponentProps<E>, keyof P | "as">;

function Text<E extends ElementType = "span">({
  as,
  ...rest
}: PolymorphicProps<E, { size?: "sm" | "lg" }>) {
  const Tag = as ?? "span";
  return <Tag {...rest} />;
}

// 使用：不同标签有各自的正确属性 ✅
<Text as="a" href="/x">链接</Text>;      // ✅ href 合法
<Text as="button" onClick={() => {}} />; // ✅ onClick 合法
<Text as="a" onClick={() => {}} />;      // ✅ a 也支持 onClick
<Text as="a" disabled />;                // ❌ disabled 不在 a 上
```

> ⚠️ 多态组件的类型推导比较脆弱，复杂场景下**可能推断不出 `E`**，需要显式传：`<Text<"button"> as="button" />`。这是类型体操的代价，别为了「完美类型」把组件写得没人能维护。💭

{{% /tab %}}

{{% tab header="children 与组合" %}}

```typescript
import type { ReactNode, PropsWithChildren } from "react";

// 显式声明 children（推荐）
function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section><h2>{title}</h2>{children}</section>;
}

// PropsWithChildren 是语法糖
type PanelProps2 = PropsWithChildren<{ title: string }>;
// 等价于 { title: string; children?: ReactNode }
```

| 类型 | 允许 | 适合 |
| --- | --- | --- |
| `ReactNode` | 元素、字符串、数字、数组、`null`、`undefined`、`boolean` | 通用容器 🔥 |
| `ReactNode`（必需） | 同上，但必须传 | 强制要有内容 |
| `ReactElement` | 单个元素 | 需要 `cloneElement` 时 |
| `(props) => ReactNode` | 函数（render prop） | 渲染逻辑交给调用方 |
| `ReactNode \| (() => ReactNode)` | 两者皆可 | 灵活但类型变复杂 |

**render prop 模式**：

```typescript
interface DataLoaderProps<T> {
  url: string;
  children: (state: { data: T | null; loading: boolean }) => ReactNode;
}

function DataLoader<T>({ url, children }: DataLoaderProps<T>) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  // ... 加载逻辑
  return <>{children({ data, loading })}</>;
}

// 使用：T 从 users 推断 ✅
<DataLoader<{ id: number; name: string }> url="/api">
  {({ data, loading }) => (loading ? <Spinner /> : <div>{data?.name}</div>)}
</DataLoader>;
```

⚠️ **`children` 是函数时不能用 `PropsWithChildren`**——它声明的是 `ReactNode`，函数不是合法的 `ReactNode`。要单独写：

```typescript
// ✅ 函数式 children 要显式声明
type Props = { children: (x: number) => ReactNode };
```

{{% /tab %}}

{{< /tabpane >}}

---

## 事件类型

{{< tabpane text=true persist=disabled >}}

{{% tab header="事件类型全表" %}}

| 事件 | 类型 | 用于元素 |
| --- | --- | --- |
| 点击 | `MouseEvent<T>` | button、div、a |
| 双击 | `MouseEvent<T>` | 同上 |
| 鼠标移动 | `MouseEvent<T>` | 同上 |
| 输入变化 | `ChangeEvent<T>` | input、select、textarea |
| 输入（实时） | `FormEvent<T>` | input |
| 表单提交 | `FormEvent<T>` | form |
| 键盘 | `KeyboardEvent<T>` | 任何可聚焦元素 |
| 聚焦/失焦 | `FocusEvent<T>` | 可聚焦元素 |
| 拖拽 | `DragEvent<T>` | 可拖拽元素 |
| 触摸 | `TouchEvent<T>` | 触摸设备 |
| 滚轮 | `WheelEvent<T>` | 可滚动元素 |
| 剪贴板 | `ClipboardEvent<T>` | input、可编辑元素 |
| 动画 | `AnimationEvent<T>` | 有 CSS 动画的元素 |
| 过渡 | `TransitionEvent<T>` | 有 CSS 过渡的元素 |
| 指针（统一鼠标/触摸/笔） | `PointerEvent<T>` | 现代推荐 🔥 |

```typescript
import type { ChangeEvent, MouseEvent, FormEvent, KeyboardEvent, FocusEvent } from "react";

function Form() {
  const onChange = (e: ChangeEvent<HTMLInputElement>) => {
    console.log(e.target.value);          // ✅ string
  };
  const onClick = (e: MouseEvent<HTMLButtonElement>) => {
    console.log(e.currentTarget.disabled); // ✅ boolean
  };
  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();                    // ✅ 存在
  };
  const onKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") { /* ... */ }   // ✅ e.key 有字面量联合类型
  };
  const onBlur = (e: FocusEvent<HTMLInputElement>) => {
    console.log(e.target.value);           // ✅
  };

  return (
    <form onSubmit={onSubmit}>
      <input onChange={onChange} onKeyDown={onKeyDown} onBlur={onBlur} />
      <button onClick={onClick}>提交</button>
    </form>
  );
}
```

**更省事的做法：内联箭头函数**——类型自动推断，不用手写标注 🔥

```typescript
// ✅ 推荐：让 TS 从 JSX 属性位置推断事件类型
<input onChange={(e) => setValue(e.target.value)} />

// ⚠️ 抽出去就需要手写类型
const handleChange = (e: ChangeEvent<HTMLInputElement>) => setValue(e.target.value);
<input onChange={handleChange} />
```

{{% /tab %}}

{{% tab header="target vs currentTarget" %}}

**这是事件处理里最容易写错的一处。**

| 属性 | 类型 | 指向 |
| --- | --- | --- |
| `currentTarget` | 泛型参数 `T` | **绑定处理器的元素** ✅ 精确 |
| `target` | `EventTarget`（需按 `T` 假设） | **实际触发事件的元素** ⚠️ 可能是子元素 |

```typescript
function Bad({ onClick }: { onClick: (e: React.MouseEvent<HTMLButtonElement>) => void }) {
  const handler = (e: React.MouseEvent<HTMLButtonElement>) => {
    // 🛑 target 是 EventTarget，没有 disabled
    e.target.disabled;
    //       ~~~~~~~~ error TS2339: Property 'disabled' does not exist on type 'EventTarget'.
  };
  return <button onClick={handler} />;
}
```

```typescript
// ✅ 用 currentTarget
const handler = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.currentTarget.disabled;   // ✅ 类型精确
};

// ✅ 或收窄 target（当确实需要触发元素时）
const handler2 = (e: React.MouseEvent<HTMLButtonElement>) => {
  if (e.target instanceof HTMLButtonElement) {
    e.target.disabled;        // ✅ 收窄后可用
  }
};
```

**为什么 `target` 类型这么宽**：因为事件会冒泡。你在 `<div>` 上监听点击，实际点到的可能是里面的 `<span>`：

```typescript
// 委托场景：确实需要 target
function List({ items }: { items: string[] }) {
  const onClick = (e: React.MouseEvent<HTMLUListElement>) => {
    // target 才是被点的那个 li，currentTarget 永远是 ul
    if (e.target instanceof HTMLLIElement) {
      console.log(e.target.dataset.id);   // ✅ 收窄后安全
    }
  };
  return <ul onClick={onClick}>{/* ... */}</ul>;
}
```

| 场景 | 用哪个 |
| --- | --- |
| 表单元素读值 | `currentTarget` 🔥 |
| 读绑定元素属性 | `currentTarget` 🔥 |
| 事件委托 | `target` + `instanceof` 收窄 |
| 一般情况 | `currentTarget` 更安全 |

> 💭 **默认用 `currentTarget`**。只有当你在做事件委托、确实关心「哪个子元素被点了」时才用 `target`，并且一定要 `instanceof` 收窄。

**表单读值的标准写法**：

```typescript
// ✅ 受控组件：推荐用 currentTarget
<input value={name} onChange={(e) => setName(e.currentTarget.value)} />

// ✅ 非受控：用 FormData
function onSubmit(e: FormEvent<HTMLFormElement>) {
  e.preventDefault();
  const data = new FormData(e.currentTarget);   // ✅ currentTarget 是 form
  const email = data.get("email");              // FormDataEntryValue | null
  if (typeof email === "string") { /* ... */ }
}
```

{{% /tab %}}

{{% tab header="事件处理器类型" %}}

| 想表达 | 类型 |
| --- | --- |
| 「某个元素的某事件处理器」 | `React.MouseEventHandler<T>` |
| 「任意事件处理器」 | `React.EventHandler<React.SyntheticEvent>` |
| 自定义组件的回调 | 自己定义签名 |

```typescript
import type { MouseEventHandler, ChangeEventHandler, ReactNode } from "react";

interface ButtonProps {
  onClick?: MouseEventHandler<HTMLButtonElement>;   // ✅ 比手写函数类型简洁
  children: ReactNode;
}

// 等价于
interface ButtonProps2 {
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
}
```

**自定义组件的回调应该「接收数据」而不是「接收事件」**：

```typescript
// 🛑 把 DOM 事件泄漏到组件 API 里
interface BadSelectProps {
  onSelect: (e: React.MouseEvent<HTMLLIElement>) => void;
}

// ✅ 组件内部消化事件，对外暴露语义化回调
interface SelectProps<T> {
  options: readonly T[];
  onSelect: (value: T) => void;
  getLabel: (value: T) => string;
}

function Select<T>({ options, onSelect, getLabel }: SelectProps<T>) {
  return (
    <ul>
      {options.map((o) => (
        <li key={getLabel(o)} onClick={() => onSelect(o)}>{getLabel(o)}</li>
      ))}
    </ul>
  );
}
```

> 🔥 **判断标准**：如果调用方需要 `e.currentTarget.dataset.xxx` 才能拿到有用信息，说明你的组件 API 设计有问题——应该直接回调**业务数据**。

{{% /tab %}}

{{< /tabpane >}}

---

## Hook 的类型推断陷阱

{{< tabpane text=true persist=disabled >}}

{{% tab header="useState" %}}

```typescript
// ✅ 从初始值推断
const [n, setN] = useState(0);              // number
const [s, setS] = useState("");             // string

// ⚠️ 陷阱 1：初始值是 null 时推断成 null，之后无法赋值
const [user, setUser] = useState(null);
setUser({ name: "a" });
// ❌ TS2345: Argument of type '{ name: string; }' is not assignable to 'null'.
```

```typescript
// ✅ 显式给联合类型
const [user, setUser] = useState<User | null>(null);
setUser({ name: "a" });                     // ✅

// ✅ 或者给一个合理的初始值
const [user, setUser] = useState<User | undefined>(undefined);
```

```typescript
// ⚠️ 陷阱 2：字面量被推断成宽类型
const [mode, setMode] = useState("light");
//                             ~~~~~~~ string（不是 "light"）
setMode("typo");        // ✅ 不报错 🛑
```

```typescript
// ✅ 用泛型参数或 as const
const [mode, setMode] = useState<"light" | "dark">("light");
setMode("typo");        // ❌ TS2345: '"typo"' is not assignable to '"light" | "dark"'

// ✅ 或者从常量推导
const MODES = ["light", "dark"] as const;
type Mode = (typeof MODES)[number];
const [mode2, setMode2] = useState<Mode>("light");
```

| 初始值 | 推断结果 | 处理 |
| --- | --- | --- |
| `useState(0)` | `number` | ✅ |
| `useState("")` | `string` | ✅ |
| `useState(null)` | `null` ⚠️ | 显式给联合 |
| `useState([])` | `never[]` ⚠️ | `useState<Item[]>([])` |
| `useState({})` | `{}` ⚠️ | 显式给类型 |

```typescript
// 🛑 空数组的经典坑
const [items, setItems] = useState([]);
setItems([{ id: 1 }]);
// ❌ TS2345: Argument of type '{ id: number; }[]' is not assignable to 'never[]'.

// ✅ 
const [items, setItems] = useState<{ id: number }[]>([]);
```

**`setState` 的函数式更新**：

```typescript
const [count, setCount] = useState(0);

// ✅ 基于旧值更新（并发安全）
setCount((c) => c + 1);      // c 推断为 number ✅

// ⚠️ 直接依赖旧值可能丢更新
setCount(count + 1);
```

{{% /tab %}}

{{% tab header="useRef 的三种形态" %}}

`useRef` 的重载决定了返回类型的可变性——**这是 React 类型里最容易混淆的地方**。

| 写法 | 返回类型 | `.current` 可写 |
| --- | --- | --- |
| `useRef<T>(init: T)` | `RefObject<T>`（React 19） | ✅ |
| `useRef<T>(null)` | `RefObject<T \| null>` | ✅ |
| `useRef<T>(null)` 且传给 `ref=` | 只读 `RefObject<T \| null>` | ❌ 由 React 管理 |

```typescript
// 形态 1：可变容器（存任意值，不参与渲染）
const renderCount = useRef(0);
renderCount.current += 1;              // ✅ 可写

// 形态 2：DOM 引用（初始 null）
const inputRef = useRef<HTMLInputElement>(null);
// inputRef.current 类型：HTMLInputElement | null
<input ref={inputRef} />;
inputRef.current?.focus();             // ✅ 必须判空 🔥

// 形态 3：定时器 id
const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
timerRef.current = setTimeout(() => {}, 1000);
```

⚠️ **`useRef` 忘了判空是最常见的运行时错误**：

```typescript
const el = useRef<HTMLDivElement>(null);
useEffect(() => {
  el.current.scrollIntoView();
  //       ~~~~~~~~~ ❌ TS18047: 'el.current' is possibly 'null'.
}, []);
```

```typescript
useEffect(() => {
  el.current?.scrollIntoView();        // ✅ 可选链
  // 或者
  if (el.current) el.current.scrollIntoView();
}, []);
```

**两种「可变容器」的语义区别**：

```typescript
// ✅ 想「跨渲染保持可变值」→ 初始值给具体值
const cache = useRef(new Map<string, number>());
cache.current.set("a", 1);             // ✅ 不用判空

// ⚠️ 如果写成 useRef<Map<...>>(null)，每次都要判空，很烦
```

> 💡 **`ref` 传给 JSX 后由 React 赋值**，你的代码不应该写它。React 19 里这类 ref 的类型是只读的 `RefObject`，想写会报错——这是有意的保护。

{{% /tab %}}

{{% tab header="useMemo / useCallback / useEffect" %}}

```typescript
// ✅ 返回类型自动推断
const sorted = useMemo(() => [...items].sort(cmp), [items]);
// sorted: Item[]

// ✅ 回调类型自动推断
const handleClick = useCallback((id: string) => { /* ... */ }, []);
// handleClick: (id: string) => void
```

⚠️ **显式泛型通常不必要，且容易写错**：

```typescript
// 🛑 手写泛型反而可能引入错误
const sorted = useMemo<Item[]>(() => [...items].sort(cmp), [items]);

// ✅ 让 TS 推断，只在推断失败时才标注
const sorted = useMemo(() => [...items].sort(cmp), [items]);
```

**`useEffect` 的清理函数类型**：

```typescript
useEffect(() => {
  const timer = setInterval(tick, 1000);
  // ✅ 返回清理函数（返回 void 或 () => void 都可以）
  return () => clearInterval(timer);
}, []);

// ⚠️ 不要在 effect 里返回非函数
useEffect(() => {
  return 42;
  // ❌ TS2322: Type 'number' is not assignable to type 'void | Destructor'.
}, []);
```

**依赖数组**：

| 写法 | 类型 |
| --- | --- |
| `useEffect(fn, [])` | `DependencyList` |
| `useEffect(fn)` | 每次渲染都跑 |
| `useEffect(fn, [a, b])` | 依赖变化时跑 |

> ⚠️ **TypeScript 不检查依赖数组是否完整**。漏依赖是运行时 bug（陈旧闭包），不是类型错误。这类问题靠 ESLint 的 `react-hooks/exhaustive-deps` 规则，**不是类型系统的能力范围**。

**自定义 Hook 的写法**：

```typescript
import { useState, useEffect } from "react";

function useDebounced<T>(value: T, delayMs: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debounced;      // ✅ 返回类型 T，泛型正确传递
}

// 使用：类型自动保留
const q = useDebounced(searchText, 300);   // q: string
```

**返回元组的自定义 Hook**（用 `as const` 保持元组类型）：

```typescript
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = useCallback(() => setOn((v) => !v), []);
  const set = useCallback((v: boolean) => setOn(v), []);

  return [on, { toggle, set }] as const;   // ✅ as const 保证是元组
}

const [isOpen, { toggle }] = useToggle();  // ✅ 解构类型正确
```

> ⚠️ **没有 `as const` 会返回数组而不是元组**，解构时类型会退化成联合：
>
> ```typescript
> // 🛑 返回 (boolean | { toggle: ... })[]，解构出来的类型很难用
> return [on, { toggle, set }];
> ```

{{% /tab %}}

{{< /tabpane >}}

---

## CSS 模块与资源声明

```typescript
// src/types/assets.d.ts ——必须是「不含顶层 import/export 的脚本文件」
declare module "*.module.css" {
  const classes: Readonly<Record<string, string>>;
  export default classes;
}

declare module "*.css" {
  const content: string;
  export default content;
}

declare module "*.svg" {
  const url: string;
  export default url;
}

declare module "*.png" {
  const url: string;
  export default url;
}
```

```typescript
// 使用
import styles from "./Button.module.css";

// ✅ 有类型：string
<div className={styles.primary} />;
```

⚠️ **`Record<string, string>` 的类型太宽**——拼错的类名不会报错：

```typescript
<div className={styles.primry} />;   // ⚠️ 不报错，运行时得到 undefined
```

**想要类名也有类型**，需要用工具生成声明：

| 方案 | 做法 |
| --- | --- |
| `typed-css-modules` | 为每个 `.module.css` 生成 `.d.ts` |
| `vite-plugin-sass-dts` 等 | 构建时生成 |
| CSS-in-JS（vanilla-extract 等） | 类型从 TS 代码来 🔥 |

```typescript
// vanilla-extract 风格：样式本身就是 TS，类名有精确类型
import { style } from "@vanilla-extract/css";

export const button = style({ padding: 8 });
// button 的类型是 string，但由 TS 生成，改名会被重构工具追踪 ✅
```

**其它资源的声明**：

```typescript
declare module "*.json" {
  const value: unknown;      // ⚠️ 或者开 resolveJsonModule 让 TS 推断结构
  export default value;
}

declare module "*?raw" {
  const content: string;
  export default content;
}

declare module "*?url" {
  const url: string;
  export default url;
}
```

> 💡 **Vite 项目别忘了 `types: ["vite/client"]`**，它已经内置了这些资源声明，不用自己写。

---

## 常见陷阱小结

| 陷阱 | 症状 | 正确做法 |
| --- | --- | --- |
| `.tsx` 里泛型箭头没加逗号 | `TS17008` | `<T,>` 或 `<T extends unknown>` |
| 用 `e.target` 读表单值 | `TS2339` EventTarget 没该属性 | 用 `e.currentTarget` 🔥 |
| `useState(null)` | 推断成 `null`，无法赋值 | `useState<T \| null>(null)` |
| `useState([])` | 推断成 `never[]` | `useState<Item[]>([])` |
| `useRef` 不判空 | `TS18047` | `ref.current?.method()` |
| 自定义 Hook 返回数组 | 类型退化成联合 | 加 `as const` |
| `React.FC` 隐式 children | children 行为意外 | 直接标注 props |
| `jsx: "react"` 忘了导入 | `TS2874` / `TS7026` | 用 `react-jsx` |
| effect 返回非函数 | `TS2322` | 只返回清理函数或 void |
| 以为 TS 检查 Hook 依赖 | 陈旧闭包 bug | 用 ESLint 规则 |
| CSS 类名拼错 | 不报错 | 用生成类型的方案 |
| 给 `*.module.css` 写 `any` | 失去全部保护 | 用 `Record<string, string>` 起步 |
