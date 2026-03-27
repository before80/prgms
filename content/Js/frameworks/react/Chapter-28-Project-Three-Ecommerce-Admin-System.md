+++
title = "第28章 项目三——电商后台管理系统"
weight = 280
date = "2026-03-25T12:56:00+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# Chapter-28 - 项目三——电商后台管理系统

## 28.1 组件库选型

### 28.1.1 Ant Design 入门：开箱即用的企业级组件

Ant Design（简称 AntD）是蚂蚁金服开源的企业级 React 组件库，提供丰富的企业级组件。

```bash
npm install antd @ant-design/icons
```

```jsx
import { Button, Table, Modal, Form, Input, Select } from 'antd'

function ProductList({ products = [] }) {
  const columns = [
    { title: '名称', dataIndex: 'name' },
    { title: '价格', dataIndex: 'price', render: v => `¥${v}` },
    { title: '操作', render: (_, record) => (
      <Button type="link">编辑</Button>
    )}
  ]

  return (
    <Table dataSource={products} columns={columns} rowKey="id" />
  )
}
```

### 28.1.2 shadcn/ui 入门：可定制的高质量组件

shadcn/ui 不是传统意义上的组件库，而是一组"可复制粘贴"的高质量组件代码。

```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button table
```

### 28.1.3 组件库选型对比与决策

| 特性 | Ant Design | shadcn/ui |
|------|-----------|-----------|
| 组件数量 | 70+ | 30+ |
| 定制方式 | CSS 变量覆盖 | 直接修改源码 |
| 包体积 | 较大 | 较小（按需引入）|
| 适用场景 | 企业中后台 | 轻量应用 |

---

## 28.2 表格与表单

### 28.2.1 Ant Design Table：分页、排序、筛选

```jsx
import { Table, Space, Button, Tag } from 'antd'

function ProductTable({ products = [] }) {
  // columns 定义每一列的配置
  // title: 表头文字  dataIndex: 对应数据字段名
  // sorter: true 启用该列的客户端排序
  // filters + onFilter: 启用该列的筛选功能
  const columns = [
    { title: 'ID', dataIndex: 'id', sorter: true },
    {
      title: '名称',
      dataIndex: 'name',
      filters: [
        { text: '产品A', value: '产品A' },
        { text: '产品B', value: '产品B' },
      ],
      // onFilter：决定每行是否通过筛选
      // value 是用户选择的筛选项，record 是当前行数据
      onFilter: (value, record) => record.name.indexOf(value) === 0,
    },
    {
      title: '状态',
      dataIndex: 'status',
      // render：自定义单元格内容，status 是当前单元格的值
      render: status => (
        <Tag color={status === 'active' ? 'green' : 'red'}>
          {status === 'active' ? '上架' : '下架'}
        </Tag>
      )
    },
    {
      title: '操作',
      // render 的第一个参数是整行数据（此处用 _ 占位表示不用）
      // 第二个参数 record 是当前行完整数据对象
      render: (_, record) => (
        <Space>
          <Button size="small" onClick={() => handleEdit(record.id)}>编辑</Button>
          <Button size="small" danger onClick={() => handleDelete(record.id)}>删除</Button>
        </Space>
      )
    }
  ]

  return (
    <Table
      columns={columns}
      dataSource={products}
      rowKey="id"  // 指定每一行的唯一 key（对应数据中的 id 字段）
      // pagination：分页配置
      // pageSize: 每页条数  showSizeChanger: 显示切换每页条数下拉框
      pagination={{ pageSize: 10, showSizeChanger: true }}
      // onChange：分页、排序、筛选变化时触发
      // 参数 pagination / filters / sorter 包含最新状态，可用于请求后端数据
      onChange={(pagination, filters, sorter) => {
        console.log('分页/筛选/排序变化:', pagination, filters, sorter)
        // 实际项目中这里会重新请求后端数据：
        // fetchProducts({ page: pagination.current, pageSize: pagination.pageSize, ...filters })
      }}
    />
  )
}
```

### 28.2.2 可编辑表格

```jsx
import { Table, Input, InputNumber } from 'antd'

// 可编辑单元格的渲染组件
// editing: 当前行是否处于编辑状态（由父组件管理）
// dataIndex: 当前列对应的字段名（用于 Form.Item 的 name）
// record: 当前行完整数据对象
// children: 默认显示内容（非编辑状态时渲染）
const EditableCell = ({ editing, dataIndex, record, children, ...restProps }) => {
  return (
    <td {...restProps}>
      {editing ? (
        // 如果 record.editable 为 true，该单元格可编辑，显示输入框
        // 如果 record.editable 为 false（如 ID 等不允许编辑的字段），仍然显示原始内容
        record.editable ? (
          <Form.Item name={dataIndex} style={{ margin: 0 }}>
            <Input />
          </Form.Item>
        ) : children
      ) : children}
    </td>
  )
}
```

### 28.2.3 高级表单：动态表单项

```jsx
import { Form, Input, Button, Space } from 'antd'

function DynamicForm() {
  // useForm()：获取 antd 表单实例，用于编程式操作表单
  const [form] = Form.useForm()

  return (
    <Form form={form}>
      {/* Form.List：专门处理动态表单项（数组形式）
          name="users"：对应表单数据中 users 数组字段
          fields：当前已有的表单项数组，每个项有 key（唯一标识）和 name（在数组中的索引）
          add / remove：Form.List 提供的添加/删除表单项的回调函数 */}
      <Form.List name="users">
        {(fields, { add, remove }) => (
          <>
            {fields.map(({ key, name, ...restField }) => (
              // name 是该表单项在数组中的索引
              // name={[name, 'name']} 表示 users[name].name（嵌套字段路径）
              // restField 包含一些内部需要的 props，要透传给 Form.Item
              <Space key={key} align="center">
                <Form.Item {...restField} name={[name, 'name']}>
                  <Input placeholder="姓名" />
                </Form.Item>
                <Form.Item {...restField} name={[name, 'email']}>
                  <Input placeholder="邮箱" />
                </Form.Item>
                {/* remove 接收数组索引 name，直接删除对应项 */}
                <Button onClick={() => remove(name)}>删除</Button>
              </Space>
            ))}
            <Button type="dashed" onClick={add} block>
              添加一行
            </Button>
          </>
        )}
      </Form.List>
    </Form>
  )
}
```

---

## 28.3 权限管理

### 28.3.1 基于角色的权限控制（RBAC）

RBAC（Role-Based Access Control）是后台管理系统的标配——不同角色的用户看到的功能不同：admin 可以做任何操作，editor 只能读写，viewer 只能看。

实现思路很简单：**在用户登录时把角色信息存到全局状态，然后每个需要权限判断的地方查一下这个角色**。权限判断可以是简单的函数，也可以抽成 HOC/权限组件。

```jsx
// 权限配置
const permissions = {
  admin: ['read', 'write', 'delete', 'manage'],
  editor: ['read', 'write'],
  viewer: ['read']
}

// 权限检查
function can(role, action) {
  return permissions[role]?.includes(action) || false
}
```

### 28.3.2 路由级权限

```jsx
import { Navigate } from 'react-router-dom'

function PermissionRoute({ action, children }) {
  const { user } = useAuthStore()
  if (!can(user.role, action)) {
    return <Navigate to="/403" replace />
  }
  return children
}

<Route path="/users" element={
  <PermissionRoute action="read">
    <UserManagement />
  </PermissionRoute>
} />
```

### 28.3.3 按钮级权限

```jsx
function PermissionButton({ action, children, ...props }) {
  const { user } = useAuthStore()

  if (!can(user.role, action)) return null

  return <Button {...props}>{children}</Button>
}

// 使用
<PermissionButton action="delete" danger onClick={handleDelete}>
  删除
</PermissionButton>
```

---

## 28.4 数据可视化

仪表盘（Dashboard）是后台管理系统的"门面"，数据可视化的质量直接影响用户体验。电商后台最常见的图表是折线图（销售额趋势）、柱状图（分类对比）和饼图（流量来源）。

**Recharts** 是 React 生态里最流行的图表库之一——API 简洁、TypeScript 支持好、组件化程度高，和 React 的理念一拍即合。

### 28.4.1 Recharts 基础图表

```bash
npm install recharts
```

```jsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

function SalesChart({ data }) {
  return (
    <LineChart data={data}>
      {/* CartesianGrid：背景网格线，strokeDasharray="3 3" 表示虚线效果 */}
      <CartesianGrid strokeDasharray="3 3" />
      {/* XAxis/YAxis：坐标轴，dataKey 指定取数据的哪个字段作为坐标值 */}
      <XAxis dataKey="month" />
      <YAxis />
      {/* Tooltip：鼠标悬停时显示详细数据 */}
      <Tooltip />
      {/* Legend：图例，说明每条线代表什么 */}
      <Legend />
      {/* Line：折线图
          type="monotone" 让线条平滑（还有 "linear" 折线模式）
          dataKey 指定取数据的哪个字段作为 Y 轴值
          stroke 是线条颜色 */}
      <Line type="monotone" dataKey="sales" stroke="#4CAF50" />
      <Line type="monotone" dataKey="profit" stroke="#2196F3" />
    </LineChart>
  )
}
```

### 28.4.2 仪表盘（Dashboard）设计

Dashboard 的布局设计讲究"重点优先"——最关键的数据（销售额、订单数）放在左上角，次要数据放右边或下方。Grid 布局是标配，`grid-cols-4` 是常见选择（桌面端 4 列，移动端自动变成 1-2 列）。

每个 StatCard（统计卡片）通常包含：指标名称、数值、同比/环比趋势（↑ +12% 或 ↓ -3%）。趋势用颜色区分：绿色表示增长，红色表示下降。好的 Dashboard 让管理者 30 秒内就能了解整体状况。

```jsx
function Dashboard() {
  return (
    <div className="grid grid-cols-4 gap-4">
      <StatCard title="总销售额" value="¥1,234,567" trend="+12%" />
      <StatCard title="订单数" value="8,888" trend="+8%" />
      <StatCard title="访问量" value="45,678" trend="-2%" />
      <StatCard title="转化率" value="3.21%" trend="+5%" />
    </div>
  )
}
```

---

## 本章小结

本章我们完成了电商后台管理系统的核心功能：

- **组件库选型**：Ant Design 企业级组件 vs shadcn/ui 可定制组件
- **表格与表单**：AntD Table 的分页排序筛选、可编辑表格、动态表单项
- **权限管理**：RBAC 权限控制、路由级权限、按钮级权限
- **数据可视化**：Recharts 基础图表、仪表盘设计

从 Todo App 到社交应用再到后台管理系统，三个项目覆盖了 React 开发的主流场景！接下来我们将深入 React 内部原理！⚙️