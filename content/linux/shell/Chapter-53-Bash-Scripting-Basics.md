+++
title = "第53章：Bash 脚本基础"
weight = 530
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第五十三章：Bash 脚本基础

## 53.1 什么是 Shell 脚本？

想象一下：你每天上班都要做一堆重复的事情——打开电脑、登录微信、打开邮箱、泡杯咖啡（这不是重复，这是仪式感）、检查任务列表……

如果每天都要手动做这些事情，你会想："有没有一种方法，让我告诉电脑'每天早上自动帮我做这些'？"

答案是：**有的，Shell 脚本就是你的私人秘书！**

## 53.2 什么是 Shell？

在讲脚本之前，我们先认识一下 **Shell**。

Shell 是 Linux 的命令行解释器，你可以把它理解为"人和 Linux 内核之间的翻译官"：

```mermaid
graph LR
    A[你] -->|输入命令| B[Shell]
    B -->|翻译| C[Linux内核]
    C -->|执行结果| B
    B -->|翻译成人话| A
```

常见的 Shell 有：
- **bash** (Bourne Again Shell) — Linux 默认主角
- **zsh** (Z Shell) — 终端爱好者的小宝贝
- **fish** (Friendly Interactive Shell) — 新手之友

查看当前使用的 Shell：

```bash
echo $SHELL
# /bin/bash  （或者 /bin/zsh，看你心情）

# 查看系统里有哪些 Shell
cat /etc/shells
# /bin/sh
# /bin/bash
# /usr/bin/zsh
# /usr/bin/fish
```

## 53.3 什么是 Shell 脚本？

简单来说，**Shell 脚本就是把一堆命令写到一个文件里，让电脑自动执行**。

就像写剧本一样——你告诉电脑："先做这个，再做那个，如果出现这种情况，就那样处理。"

### 为什么需要 Shell 脚本？

**场景一：批量处理文件**
```bash
# 手动操作：给100张图片加水印
# "救命，我不想一件一件做啊！"

# 脚本方案：
for img in *.jpg; do
    convert "$img" -quality 85 "compressed_$img"
done
# 一行命令，100张图片搞定！咖啡还没凉~
```

**场景二：自动化部署**
```bash
# 手动部署：git pull → npm install → pm2 restart
# 每次更新都要重复3步，有没有更优雅的方式？

# 脚本方案：写一个 deploy.sh
#!/bin/bash
git pull
npm install
pm2 restart all
echo "部署完成，系统正在运行~"
# 以后只需要执行 ./deploy.sh，完美！
```

**场景三：定时任务**
```bash
# "每天凌晨3点自动备份数据库"
# 手动操作：凌晨3点爬起来？不要命了？

# 脚本 + crontab = 完美解决方案
# 写好脚本，交给 crontab 去调度
# 安心睡觉，第二天上班发现备份已经乖乖躺好了
```

## 53.4 Shell 脚本能做什么？

| 应用场景 | 示例 |
|---------|------|
| 自动化运维 | 批量部署、配置管理、定时任务 |
| 数据处理 | 日志分析、文件整理、格式转换 |
| 系统监控 | 检查服务状态、发送告警通知 |
| 备份恢复 | 自动备份数据库、清理过期文件 |
| 开发辅助 | 编译项目、代码格式化、批量测试 |

## 53.5 第一个 Shell 脚本

让我们写一个"Hello World"脚本，感受一下 Shell 脚本的魅力：

```bash
#!/bin/bash
# 我的第一个脚本：hello_world.sh

echo "Hello World!"
echo "你好，世界！"
echo "今天也是元气满满的一天呢~"
```

**脚本解读：**
- `#!/bin/bash` — **Shebang**（读作 "shee-bang"），告诉系统用 `/bin/bash` 来执行这个脚本
  - `#!` 是特殊的"魔法标记"，`#` 在 shell 中是注释，但 `#!` 组合在一起就是 Shebang
  - 后面的路径 `/bin/bash` 指定了解释器的位置
- `#` 后面的内容是注释，不会被执行
- `echo` 就是打印输出，类似 C 语言的 `printf`，Python 的 `print`

**运行效果：**
```bash
$ chmod +x hello_world.sh    # 先给脚本加执行权限
$ ./hello_world.sh           # 运行它！
Hello World!
你好，世界！
今天也是元气满满的一天呢~
```

## 53.6 脚本的后缀名重要吗？

技术上讲，**.sh 后缀名只是给人看的**，Linux 不关心这个。重要的是第一行的 `#!/bin/bash`。

但为了可读性，建议：
- 脚本文件用 `.sh` 后缀
- 或者干脆不用后缀，比如 `deploy`、`backup`

```bash
# 这些都能正常运行：
mv hello_world.sh hello_world     # 去掉 .sh
./hello_world                      # 照样执行
```

## 53.7 小结

| 概念 | 说明 |
|------|------|
| Shell | 命令行解释器，人和 Linux 之间的翻译官 |
| Shell 脚本 | 把命令写进文件，让电脑自动执行 |
| Shebang | `#!/bin/bash`，告诉系统用什么解释器 |
| chmod +x | 给脚本加执行权限 |
| echo | 输出命令，类似 print |

---

> 💡 **温馨提示**：
> Shell 脚本看起来简单，但它是 Linux 世界的"瑞士军刀"！熟练掌握后，你可以用几行代码完成原本需要几个小时的工作。说不定隔壁工位的同事看了都会竖起大拇指 👍

---

**本章小结**

本章我们认识了 Shell 脚本这位"私人秘书"：
- Shell 是命令行解释器，bash 是最常用的版本
- Shell 脚本就是"把命令写成文件，让电脑自动执行"
- 它的优势在于自动化——批量处理、定时任务、减少重复劳动
- 简单到 `echo "Hello World"`，复杂到整套自动化部署系统
- 记得 `#!/bin/bash` 和 `chmod +x`，这是脚本的"身份证"

下一章我们将学习如何写一个真正有用的脚本，包括变量、条件判断、循环等。准备好了吗？让我们继续探索 Bash 的魔法世界！ 🚀

---

## 53.2 第一个脚本

光说不练假把式，让我们写一个真正能"干活"的脚本！

### 创建脚本文件

```bash
# 创建脚本文件
vim greeting.sh

# 或者用你喜欢的编辑器
nano greeting.sh
gedit greeting.sh   # 如果在图形界面
code greeting.sh    # 如果装了 VSCode
```

### 编写脚本内容

```bash
#!/bin/bash
# greeting.sh - 我的第一个正经脚本

# 定义变量
name="小明"
date=$(date +%Y年%m月%d日)

# 输出问候语
echo "========================================"
echo "  您好，$name！"
echo "  今天是：$date"
echo "========================================"
echo ""
echo "欢迎来到 Linux 的世界！"
echo "在这里，你就是主宰一切的上帝！"
```

### 运行脚本

```bash
# 方法一：加执行权限后运行（推荐）
chmod +x greeting.sh
./greeting.sh

# 方法二：用 bash 解释器直接运行（不需要加执行权限）
bash greeting.sh

# 方法三：用 sh 运行（POSIX 标准，不保证 bash 特性可用）
sh greeting.sh
```

**运行效果：**
```
========================================
  您好，小明！
  今天是：2026年03月24日
========================================

欢迎来到 Linux 的世界！
在这里，你就是主宰一切的上帝！
```

### 脚本的组成结构

一个完整的脚本通常包含以下部分：

```bash
#!/bin/bash                                    # 1. Shebang（必须！）

# =========================================     # 2. 注释（说明脚本功能）
# 脚本名称：greeting.sh
# 作者：小明
# 日期：2026-03-24
# 描述：一个简单的问候脚本

# =========================================     # 3. 变量定义
NAME="Linux"
VERSION="1.0"

# =========================================     # 4. 主逻辑
echo "Hello, $NAME!"
echo "Version: $VERSION"

# =========================================     # 5. 退出
exit 0                                         # 0 表示正常退出
```

## 53.3 脚本执行

### 执行方式对比

| 方式 | 命令 | 需要执行权限 | 特点 |
|------|------|-------------|------|
| 加权限执行 | `./script.sh` | ✅ 是 | 最标准的方式 |
| bash执行 | `bash script.sh` | ❌ 否 | 跨 Shell 运行 |
| source执行 | `source script.sh` | ❌ 否 | 在当前Shell运行 |

### source vs bash 的区别

这个区别**超级重要**，很多新手都会在这里翻车！

```bash
# 创建一个脚本 test_env.sh
#!/bin/bash
export MY_VAR="Hello from script"

# 用 bash 运行
bash test_env.sh
echo $MY_VAR      # 输出为空！变量不存在！

# 用 source 运行
source test_env.sh
echo $MY_VAR      # 输出：Hello from script
```

**解释：**
- `bash script.sh` — 在**子 Shell** 中运行，环境隔离
- `source script.sh` — 在**当前 Shell** 中运行，环境共享

### 什么时候用哪种？

```bash
# 场景一：运行独立脚本
./my_script.sh              # 用 ./ ，子 shell 运行

# 场景二：加载环境变量
source /etc/profile         # 让环境变量生效
source ~/.bashrc            # 重新加载 bash 配置

# 场景三：调试脚本
bash -x script.sh           # 调试模式运行
```

### 管道执行

```bash
# 把脚本输出通过管道传给其他命令
./script.sh | grep "error"

# Here Document 方式
./script.sh << EOF
input1
input2
EOF
```

## 53.4 变量

终于到了变量部分！这是脚本的"记忆单元"，让你的脚本不再"金鱼脑"。

### 变量定义

```bash
# 基本赋值（等号两边不能有空格！）
name="Linux"           # 字符串
version=1.0            # 数字（其实还是字符串）
is_awesome=true       # 布尔值（习惯用法）
empty_var=             # 空值

# 定义常量（习惯上用大写）
readonly PI=3.14159
MAX_RETRIES=3
```

### 变量使用

```bash
# 使用变量时要加 $
echo $name
echo "Hello, $name"
echo "Hello, ${name}"    # 加花括号更规范

# 字符串拼接
greeting="Hello, "$name"!"
echo $greeting           # Hello, Linux!

# 双引号里可以解析变量，单引号不会
echo "$name is best"     # Linux is best
echo '$name is best'     # $name is best（字面量）
```

### 系统变量

| 变量 | 说明 | 示例 |
|------|------|------|
| `$0` | 脚本名 | `greeting.sh` |
| `$1-$9` | 第1-9个参数 | `$1` 第一个参数 |
| `$#` | 参数个数 | `3` |
| `$@` | 所有参数 | `"$1" "$2" "$3"` |
| `$$` | 当前进程ID | `12345` |
| `$?` | 上个命令退出状态 | `0` 表示成功 |
| `$USER` | 当前用户名 | `linux` |
| `$HOME` | 家目录 | `/home/linux` |
| `$PWD` | 当前目录 | `/home/linux/scripts` |
| `$RANDOM` | 随机数 | `4823` |

### 命令替换

把命令输出赋值给变量：

```bash
# 方法一：反引号（老派）
current_date=`date +%Y-%m-%d`

# 方法二：$()（现代派，推荐！）
current_time=$(date +%H:%M:%S)
disk_usage=$(df -h / | tail -1)
file_count=$(ls | wc -l)

# 嵌套使用
echo "Today is $(date +%Y年%m月%d日)"
```

### 数组变量

```bash
# 定义数组
colors=("红色" "绿色" "蓝色" "黄色")

# 访问数组元素
echo ${colors[0]}    # 红色
echo ${colors[1]}    # 绿色

# 获取所有元素
echo ${colors[@]}    # 红色 绿色 蓝色 黄色

# 获取数组长度
echo ${#colors[@]}  # 4

# 获取某个元素的长度
echo ${#colors[0]}   # 2（"红色"两个字符）
```

### 只读变量

```bash
readonly CONST_VAR="这个变量不能改"
CONST_VAR="试试改一下"   # 报错！
```

### 删除变量

```bash
name="Linux"
echo $name      # Linux
unset name
echo $name      # 空，什么都没有了
```

## 53.5 引号

引号在 Shell 中可不是随便用的，它们有各自的"性格"。

### 单引号 vs 双引号

| 类型 | 特点 | 示例 |
|------|------|------|
| 单引号 `' '` | 原样输出，不解析任何特殊字符 | `'$name'` → `$name` |
| 双引号 `" "` | 解析变量和某些转义字符 | `"$name"` → `Linux` |
| 反引号 \` \` | 执行命令（已过时） | `` `date` `` |

### 实战演示

```bash
name="Linux"

# 单引号：所见即所得
echo '$name'           # 输出：$name
echo 'Hello\nWorld'    # 输出：Hello\nWorld（不转义）

# 双引号：解析变量和特殊字符
echo "$name"           # 输出：Linux
echo "Hello\nWorld"    # 输出：Hello（换行）

# 变量和字符串拼接
echo "Hello, $name!"   # 输出：Hello, Linux!
echo "Version: ${version:-1.0}"  # 默认值语法

# 转义字符
echo "Path: \$HOME"    # 输出：Path: $HOME
echo "He said \"Hi\""  # 输出：He said "Hi"
```

### Here Document

用于输入多行文本给命令：

```bash
# 基本语法
command << EOF
第一行内容
第二行内容
$variable（可解析变量）
EOF

# 实例：多行字符串
cat << EOF
=================================
    用户信息报表
=================================
用户名：$USER
日期：$(date +%Y-%m-%d)
主机：$HOSTNAME
=================================
EOF
```

### Here String

```bash
# 把字符串作为输入
cat <<< "Hello World"

# 等价于
echo "Hello World" | cat
```

## 53.6 运算符

Shell 脚本虽然不是计算器，但基本的数学运算还是得会的！

### 算术运算符

```bash
# 方法一：$[表达式]（已过时）
result=$[1 + 2]
echo $result    # 3

# 方法二：$((表达式))（推荐！）
result=$((1 + 2))
echo $result    # 3

a=10
b=3

echo $((a + b))    # 13
echo $((a - b))    # 7
echo $((a * b))    # 30
echo $((a / b))    # 3（整数除法）
echo $((a % b))    # 1（取余）

# 复合运算
echo $((a += 5))   # 15
echo $((a -= 3))   # 12
echo $((a *= 2))   # 24
```

### 关系运算符

```bash
x=10
y=20

# 比较（返回 true 或 false）
[ $x -eq $y ]   # 等于
[ $x -ne $y ]   # 不等于
[ $x -gt $y ]   # 大于
[ $x -lt $y ]   # 小于
[ $x -ge $y ]   # 大于等于
[ $x -le $y ]   # 小于等于

# 字符串比较
[ "$str1" = "$str2" ]   # 等于
[ "$str1" != "$str2" ]  # 不等于
[ -z "$str" ]           # 字符串为空
[ -n "$str" ]           # 字符串非空
```

### 逻辑运算符

```bash
# 逻辑与
[ $x -gt 5 ] && [ $x -lt 20 ]

# 逻辑或
[ $x -lt 5 ] || [ $x -gt 20 ]

# 逻辑非
[ ! $x -eq 10 ]

# 组合条件
if [ $x -gt 5 ] && [ $x -lt 20 ]; then
    echo "x 在 5 和 20 之间"
fi
```

### 文件测试运算符

```bash
file="/path/to/file"

# 文件类型测试
[ -e $file ]   # 文件存在
[ -f $file ]   # 普通文件
[ -d $file ]   # 目录
[ -L $file ]   # 符号链接
[ -r $file ]   # 可读
[ -w $file ]   # 可写
[ -x $file ]   # 可执行

# 文件属性比较
[ file1 -nt file2 ]   # file1 比 file2 新
[ file1 -ot file2 ]   # file1 比 file2 旧
```

## 53.7 条件判断

程序员的三大法宝：**顺序、选择、循环**。现在我们学"选择"！

### 基本语法

```bash
# 单分支
if [ 条件 ]; then
    # 条件成立时执行
fi

# 双分支
if [ 条件 ]; then
    # 条件成立
else
    # 条件不成立
fi

# 多分支
if [ 条件1 ]; then
    # 条件1成立
elif [ 条件2 ]; then
    # 条件2成立
else
    # 都不成立
fi
```

### 实战例子

```bash
#!/bin/bash
# check_number.sh - 判断数字大小

number=15

if [ $number -gt 20 ]; then
    echo "$number 比 20 大"
elif [ $number -gt 10 ]; then
    echo "$number 比 10 大，比 20 小"
else
    echo "$number 不超过 10"
fi

# 输出：15 比 10 大，比 20 小
```

## 53.8 if 语句

if 语句是条件判断的核心，让我们深入了解一下。

### 嵌套 if

```bash
age=25
income=50000

if [ $age -ge 18 ]; then
    echo "已成年"
    
    if [ $income -gt 100000 ]; then
        echo "高收入人群"
    else
        echo "普通收入"
    fi
    
else
    echo "未成年"
fi
```

### 多个条件

```bash
# 并且 &&
if [ $age -ge 18 ] && [ $age -lt 65 ]; then
    echo "劳动力人口"
fi

# 或者 ||
if [ $status == "admin" ] || [ $status == "root" ]; then
    echo "管理员权限"
fi
```

### test 命令

`[ ]` 其实是 `test` 命令的简写：

```bash
# 这两个等价：
test $x -eq $y
[ $x -eq $y ]

# test 命令可以直接在命令行使用
test -f /etc/passwd && echo "文件存在"
```

## 53.9 case 语句

当有很多分支时，`case` 比 `if...elif...elif...` 优雅得多！

### 基本语法

```bash
case 变量 in
模式1)
    # 匹配模式1时执行
    ;;
模式2)
    # 匹配模式2时执行
    ;;
*)
    # 默认情况（类似 else）
    ;;
esac
```

### 实战例子

```bash
#!/bin/bash
# menu.sh - 简单的菜单选择

echo "请选择你喜欢的操作系统："
echo "1) Linux"
echo "2) macOS"
echo "3) Windows"
echo ""

read choice

case $choice in
    1)
        echo "明智的选择！Linux 最棒！"
        ;;
    2)
        echo "macOS 也很不错，设计优美"
        ;;
    3)
        echo "Windows...呃，好吧"
        ;;
    *)
        echo "无效选择，请输入 1-3"
        ;;
esac
```

### 模式匹配

```bash
# 数字范围
case $score in
    9[0-9]|100)
        echo "优秀"
        ;;
    [7-8][0-9])
        echo "良好"
        ;;
    6[0-9])
        echo "及格"
        ;;
    *)
        echo "需要努力"
        ;;
esac

# 字符串模式
case $filename in
    *.jpg|*.png)
        echo "图片文件"
        ;;
    *.txt)
        echo "文本文件"
        ;;
    *.sh)
        echo "Shell 脚本"
        ;;
    *)
        echo "未知类型"
        ;;
esac
```

## 53.10 for 循环

for 循环是批量处理的利器！

### 基本语法

```bash
# 形式一：遍历列表
for 变量 in 值1 值2 值3
do
    # 循环体
done

# 形式二：C 语言风格
for (( i=0; i<5; i++ ))
do
    # 循环体
done
```

### 实战例子

```bash
#!/bin/bash
# 遍历文件
for file in *.txt
do
    echo "处理文件: $file"
done

# 遍历数字
for i in {1..5}
do
    echo "第 $i 次迭代"
done

# C 语言风格
for (( i=1; i<=5; i++ ))
do
    echo "计数: $i"
done

# 遍历命令输出
for line in $(cat users.txt)
do
    echo "用户: $line"
done

# 遍历数组
colors=("红" "绿" "蓝")
for color in "${colors[@]}"
do
    echo "颜色: $color"
done
```

### 批量重命名

```bash
# 给所有 .txt 文件加上 .bak 后缀
for file in *.txt; do
    mv "$file" "${file}.bak"
done

# 批量转换文件名
for img in *.JPG; do
    newname=$(basename "$img" .JPG).jpg
    mv "$img" "$newname"
done
```

## 53.11 while 循环

while 循环当条件满足时一直执行。

### 基本语法

```bash
while [ 条件 ]
do
    # 循环体
done
```

### 实战例子

```bash
#!/bin/bash
# 计数器示例
count=1

while [ $count -le 5 ]
do
    echo "计数: $count"
    count=$((count + 1))
done

# 读取文件行
while read line
do
    echo "行内容: $line"
done < /etc/hostname

# 无限循环（Ctrl+C 停止）
while true
do
    echo "按 Ctrl+C 停止..."
    sleep 1
done
```

### until 循环

until 和 while 相反，条件**不满足**时继续执行：

```bash
#!/bin/bash
# until 示例：倒计时

count=5

until [ $count -eq 0 ]
do
    echo "倒计时: $count"
    sleep 1
    count=$((count - 1))
done

echo "发射！🚀"
```

## 53.12 until 循环

until 循环是 while 的"反义词"——当条件为 false 时继续执行。

```bash
#!/bin/bash
# until 示例：等待服务启动

port=3306

until nc -z localhost $port 2>/dev/null
do
    echo "MySQL 还未启动，等待中..."
    sleep 2
done

echo "MySQL 已就绪！"
```

## 53.13 函数

函数是代码复用的神器！

### 定义函数

```bash
# 形式一：function 关键字
function greet {
    echo "你好！"
}

# 形式二：直接定义（更简洁）
greet() {
    echo "你好！"
}

# 调用函数
greet
```

### 函数参数

```bash
#!/bin/bash

# 带参数的函数
greet_user() {
    name=$1           # 第一个参数
    age=$2            # 第二个参数
    echo "你好，$name！你 $age 岁了。"
    
    # 返回值
    return 0
}

# 调用并传递参数
greet_user "小明" "25"

# 使用 $? 获取返回值
echo "函数返回状态: $?"
```

### 函数返回值

```bash
# return 用于返回状态码（0-255）
check_file() {
    if [ -f "$1" ]; then
        return 0    # 成功
    else
        return 1    # 失败
    fi
}

if check_file "/etc/passwd"; then
    echo "文件存在"
else
    echo "文件不存在"
fi

# 如果要返回数据，用 echo
get_date() {
    echo $(date +%Y-%m-%d)
}

today=$(get_date)
echo "今天是: $today"
```

### 局部变量

```bash
#!/bin/bash

counter() {
    local count=0    # local 关键字定义局部变量
    count=$((count + 1))
    echo "函数内 count: $count"
}

count=100
counter
echo "函数外 count: $count"   # 仍然是 100，函数内的改动不影响外部
```

### 函数库

把常用函数写到一个文件里，需要时 source 加载：

```bash
# 创建文件 common.sh
#!/bin/bash

# 颜色输出函数
red() { echo -e "\033[31m$*\033[0m"; }
green() { echo -e "\033[32m$*\033[0m"; }
yellow() { echo -e "\033[33m$*\033[0m"; }

# 日志函数
log() {
    echo "[$(date +%H:%M:%S)] $*"
}

# 在其他脚本中使用
#!/bin/bash
source common.sh

green "操作成功！"
log "开始处理..."
```

## 53.14 数组

数组让你能存储和操作一组数据。

### 定义数组

```bash
# 方式一：直接赋值
fruits=("苹果" "香蕉" "橙子" "葡萄")

# 方式二：按索引赋值
colors[0]="红色"
colors[1]="绿色"
colors[2]="蓝色"

# 方式三：稀疏数组
sparse[0]="第一"
sparse[5]="第六"    # 中间跳过了

# 方式四：从命令输出创建
files=($(ls *.txt))
```

### 访问数组

```bash
fruits=("苹果" "香蕉" "橙子" "葡萄")

# 访问单个元素
echo ${fruits[0]}    # 苹果
echo ${fruits[2]}    # 橙子

# 访问所有元素
echo ${fruits[@]}    # 苹果 香蕉 橙子 葡萄
echo ${fruits[*]}    # 苹果 香蕉 橙子 葡萄

# 获取数组长度
echo ${#fruits[@]}   # 4
echo ${#fruits[*]}   # 4

# 获取某个元素的长度
echo ${#fruits[0]}   # 2（"苹果"两个字符）
```

### 数组切片

```bash
fruits=("苹果" "香蕉" "橙子" "葡萄" "西瓜")

# 切片：从索引 1 开始，取 3 个
echo ${fruits[@]:1:3}   # 香蕉 橙子 西瓜

# 从索引 2 开始到末尾
echo ${fruits[@]:2}     # 橙子 葡萄 西瓜
```

### 数组操作

```bash
# 添加元素
fruits=("苹果" "香蕉")
fruits+=("橙子")         # 追加
fruits=("${fruits[@]}" "葡萄")  # 另一种方式

# 删除元素
unset fruits[1]          # 删除索引 1 的元素

# 删除整个数组
unset fruits

# 关联数组（需要 bash 4+）
declare -A person
person["name"]="小明"
person["age"]=25
person["city]="北京"

echo ${person["name"]}   # 小明
echo ${!person[@]}        # name age city（所有键）
```

### 遍历数组

```bash
# 遍历值
for fruit in "${fruits[@]}"; do
    echo "水果: $fruit"
done

# 遍历索引
for i in "${!fruits[@]}"; do
    echo "索引 $i: ${fruits[$i]}"
done
```

## 53.15 脚本调试

调试是发现和修复问题的过程，Shell 提供了多种调试工具。

### 调试选项

| 选项 | 作用 |
|------|------|
| `-n` | 检查语法错误，不执行 |
| `-v` | 显示读取的每一行 |
| `-x` | 显示执行的每一行（追踪） |

### 使用方法

```bash
# 检查语法
bash -n script.sh

# 显示执行过程
bash -x script.sh

# 组合使用
bash -vn script.sh
```

### 在脚本中启用调试

```bash
#!/bin/bash

# 在需要调试的位置开启
set -x    # 开启调试
echo "这行会被追踪"
set +x    # 关闭调试

echo "这行不会"
```

### 常见调试技巧

```bash
#!/bin/bash
# debug_demo.sh

# 1. 打印变量值
echo "DEBUG: x = $x"

# 2. 在可疑位置加日志
log_debug() {
    echo "[$(date +%T)] DEBUG: $*"
}

# 3. 捕获错误
set -e    # 遇错误就退出
set -u    # 使用未定义变量时报错
set -o pipefail   # 管道中任何一个失败就算失败

# 4. 调试函数
debug_func() {
    echo "Entering: ${FUNCNAME[1]}"
    echo "Arguments: $*"
}
```

### trap 信号捕获

```bash
#!/bin/bash
# trap_demo.sh

# 脚本退出时执行清理
cleanup() {
    echo "脚本退出，清理临时文件..."
    rm -f /tmp/tmp_*.txt
}

trap cleanup EXIT

# 脚本主体
echo "开始执行..."
# ...
```

### 常用调试命令

```bash
# 查看命令的 help
help set

# 列出所有函数及其定义
declare -F

# 查看函数定义
declare -f function_name

# 跟踪变量赋值
bash -x script.sh 2>&1 | grep variable_name
```

## 本章小结

本章我们学习了 Bash 脚本的基础知识：

| 知识点 | 内容 |
|--------|------|
| Shell 脚本 | 把命令写成文件，让电脑自动执行 |
| Shebang | `#!/bin/bash`，告诉系统用什么解释器 |
| 变量 | 存储数据的"容器"，用 `$` 访问 |
| 引号 | 单引号原样输出，双引号解析变量 |
| 运算符 | 算术、关系、逻辑、文件测试 |
| 条件判断 | `if...then...fi` |
| 多分支 | `case...in...esac` |
| 循环 | `for`、`while`、`until` |
| 函数 | 代码复用，`function name()` 或 `name()` |
| 数组 | 存储多个值，`${array[@]}` 访问 |
| 调试 | `bash -x`、`set -x`、`trap` |

Shell 脚本是 Linux 运维的基石。掌握好这些基础知识，你就能写出强大的自动化脚本，让电脑乖乖为你打工！

---

> 💡 **温馨提示**：
> 写 Shell 脚本最重要的是多练！建议把本章的每个例子都亲手敲一遍，感受一下"让电脑听话"的乐趣。下一个脚本大师，就是你！

---

**下一章预告**：53.2-53.15 节已更新完毕！第五十四章我们将学习 Bash 脚本进阶，包括字符串处理、正则表达式、sed、awk 等强大工具。敬请期待！ 🚀
