+++
title = "第54章：Bash 脚本进阶"
weight = 540
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第五十四章：Bash 脚本进阶

## 54.1 字符串处理

Shell 脚本中最常用的数据类型就是字符串，让我们来掌握各种处理技巧！

### 字符串基础操作

```bash
str="Hello World"

# 获取字符串长度
echo ${#str}    # 11

# 截取子串
echo ${str:0:5}       # Hello（从索引0开始，截取5个字符）
echo ${str:6}         # World（从索引6到末尾）
echo ${str:(-5)}      # World（负数索引，用括号更清晰）
# 或者: echo ${str: -5}  # 注意冒号后有空格，容易混淆

# 字符串拼接
str1="Hello"
str2="World"
result="$str1 $str2"
echo $result    # Hello World
```

### 字符串替换

```bash
str="Hello World"

# 替换第一个匹配
echo ${str/World/Linux}    # Hello Linux

# 替换所有匹配
echo ${str//o/O}           # HellO WOrld

# 替换开头匹配
echo ${str/#Hello/Hi}      # Hi World

# 替换结尾匹配
echo ${str/%World/Universe}  # Hello Universe

# 删除子串
echo ${str/World}          # Hello （删除第一个 World）
echo ${str//o}             # Hell Wrld（删除所有 o）
```

### 字符串大小写

```bash
str="Hello World"

# 转为大写（bash 4.0+）
echo ${str^^}              # HELLO WORLD

# 转为小写
echo ${str,,}             # hello world

# 首字母大写
echo ${str^}               # Hello world

# 模式转换
echo ${str^^[aeiou]}       # HEllO WOrld（只转换元音）
```

### 字符串分割

```bash
# 按分隔符分割
email="user@example.com"
IFS='@' read -r user domain <<< "$email"
echo "用户: $user"    # user
echo "域名: $domain"  # example.com

# 分割路径
path="/home/user/documents/file.txt"
IFS='/' read -ra parts <<< "$path"
echo "${parts[-1]}"   # file.txt（最后一部分）
echo "${parts[-2]}"  # documents

# 读取每一行
echo -e "line1\nline2\nline3" | while read -r line; do
    echo "行: $line"
done
```

### 字符串去空白

```bash
str="   前后有空格   "

# 去开头空格
echo "${str#"${str%%[![:space:]]*}"}"   # "前后有空格   "

# 去结尾空格
echo "${str%"${str##*[![:space:]]}"}"    # "   前后有空格"

# 去两端空格（bash 内置）
echo "$str" | xargs

# 使用 trim 函数
trim() {
    local var="$*"
    var="${var#"${var%%[![:space:]]*}"}"
    var="${var%"${var##*[![:space:]]}"}"
    echo -n "$var"
}
```

## 54.2 正则表达式

正则表达式是文本处理的"瑞士军刀"，在 Shell 中经常配合 grep、sed、awk 使用。

### 正则基础

```bash
# 基本元字符
^        # 行首
$        # 行尾
.        # 任意单个字符
*        # 前一个字符零次或多次
+        # 前一个字符一次或多次（扩展正则）
?        # 前一个字符零次或一次
[abc]    # 字符集，匹配 a、b 或 c
[^abc]   # 否定字符集，匹配除了 a、b、c 之外
[a-z]    # 范围，匹配小写字母
```

### 扩展正则表达式

```bash
# 使用 egrep 或 grep -E
grep -E "^[0-9]+$" file.txt      # 纯数字行
grep -E "^[a-zA-Z]+$" file.txt  # 纯字母行
egrep "^hello|world$" file.txt  # hello 开头或 world 结尾

# 其他扩展元字符
|         # 或
()        # 分组
{n}       # 精确重复 n 次
{n,}      # 至少 n 次
{n,m}     # n 到 m 次
```

### 常用正则实例

```bash
# 邮箱验证
email="user@example.com"
if [[ $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "邮箱格式正确"
fi

# IP 地址验证
ip="192.168.1.1"
if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
    echo "IP 格式正确"
fi

# 手机号验证（中国大陆）
phone="13812345678"
if [[ $phone =~ ^1[3-9][0-9]{9}$ ]]; then
    echo "手机号格式正确"
fi
```

### Bash 中的正则匹配

```bash
# [[ ]] 中的 =~ 操作符
str="Hello123World"

if [[ $str =~ ^Hello[0-9]+World$ ]]; then
    echo "匹配成功！"
fi

# 捕获分组
if [[ $str =~ ^([A-Za-z]+)([0-9]+)([A-Za-z]+)$ ]]; then
    echo "全部: ${BASH_REMATCH[0]}"
    echo "第一组: ${BASH_REMATCH[1]}"
    echo "第二组: ${BASH_REMATCH[2]}"
    echo "第三组: ${BASH_REMATCH[3]}"
fi
```

## 54.3 sed

sed 是流编辑器，专治"文本替换困难症"！

### 基本语法

```bash
sed [选项] '命令' 文件
```

### 替换命令

```bash
# 基本替换：s/原内容/新内容/
sed 's/old/new/' file.txt           # 替换每行第一个 old
sed 's/old/new/g' file.txt          # 替换所有 old（g 表示全局）
sed 's/old/new/2' file.txt          # 替换每行第二个 old

# 分隔符可以自定义（当内容包含 / 时）
sed 's|/bin/bash|/bin/sh|' file.txt

# 替换特定行
sed '3s/old/new/' file.txt          # 只替换第3行
sed '1,5s/old/new/g' file.txt        # 替换1-5行
sed '/pattern/s/old/new/g' file.txt  # 只在匹配的行替换

# 多个替换
sed -e 's/old1/new1/' -e 's/old2/new2/' file.txt
sed 's/old1/new1/; s/old2/new2/' file.txt
```

### sed 高级操作

```bash
# 删除行
sed '/^$/d' file.txt                # 删除空行
sed '/^\s*#/d' file.txt             # 删除注释行
sed '1,10d' file.txt                # 删除1-10行

# 插入和追加
sed '3i\新行内容' file.txt          # 在第3行前插入
sed '3a\新行内容' file.txt          # 在第3行后追加
sed '1a\第一行后\n第二行' file.txt  # 多行追加

# 替换整行
sed '/pattern/c\替换后的整行内容' file.txt

# 反向引用
sed 's/\([0-9]\+\)/\1/p' file.txt   # 保留带数字的行
sed 's/\b\(.\)\b/\1\1/g' file.txt   # 每个字符重复一次

# 大小写转换
sed 's/[a-z]/\U&/g' file.txt         # 转大写
sed 's/[A-Z]/\L&/g' file.txt         # 转小写
```

### sed 实战例子

```bash
# 1. 批量替换文件名（在文件内容中）
sed -i 's/旧路径/新路径/g' *.txt     # -i 表示直接修改文件

# 2. 提取 IP 地址
ifconfig | sed -n '/inet /p' | sed 's/inet.*://' | sed 's/ .*//'

# 3. 清理日志（保留最近100行）
sed -i '1,$(($(wc -l<file.log)-100))d' file.log

# 4. 在每行前后加引号
sed 's/.*/"&"/' file.txt            # "每一行"
sed 's/.*/"&"/' file.txt            # "每一行"
```

## 54.4 awk

awk 是更强大的文本分析工具，适合处理结构化文本。

### 基本语法

```bash
awk 'pattern { action }' 文件
```

### 字段操作

```bash
# 默认按空格分割字段
echo "John 25 male Beijing" | awk '{print $1, $3}'
# 输出：John male

# 修改分隔符
echo "192.168.1.1" | awk -F'.' '{print $1"."$2"."$3".0"}'

# 使用多个分隔符
echo "user@email.com,123456" | awk -F'[@,]' '{print $1, $3}'

# 内置变量
# NF: 字段数
# NR: 行号
# $0: 整行
# $n: 第 n 个字段
```

### 实战例子

```bash
# 1. 打印文件内容（带行号）
awk '{print NR, $0}' file.txt

# 2. 计算文件大小总和
ls -l *.txt | awk '{sum+=$5} END {print "Total:", sum, "bytes"}'

# 3. 找最高内存占用进程
ps aux | awk 'NR>1 {print $6" "$11}' | sort -rn | head -5

# 4. 格式化输出
awk '{printf "%-10s %5d\n", $1, $2}' file.txt

# 5. 条件过滤
awk '/error/ {print $0}' log.txt           # 包含 error 的行
awk '$3 > 100 {print $1, $3}' file.txt     # 第3字段大于100的行

# 6. 统计访问日志
awk '{print $4}' access.log | sort | uniq -c | sort -rn | head -10
```

### awk 脚本文件

```bash
# 创建 awk 脚本 report.awk
BEGIN {
    FS=":"
    print "=== 用户报告 ==="
}

{
    print "用户: " $1
    print "Shell: " $7
    print "---"
}

END {
    print "=== 报告结束 ==="
}

# 运行
awk -f report.awk /etc/passwd
```

### awk 数组

```bash
# 1. 统计单词出现频率
{ for (i=1; i<=NF; i++) words[$i]++ }
END { for (w in words) print w, words[w] }'

# 2. 按字段分组统计
awk '{sum[$1]+=$2} END {for (k in sum) print k, sum[k]}' data.txt

# 3. 二维数组
awk 'BEGIN {
    array[1,1]="a"; array[1,2]="b"
    array[2,1]="c"; array[2,2]="d"
    for (i=1; i<=2; i++)
        for (j=1; j<=2; j++)
            print i","j":", array[i,j]
}'
```

## 54.5 进程处理

### 查看进程

```bash
# 查看当前终端的进程
ps

# 查看所有进程
ps aux
ps -ef

# 查看特定进程
ps aux | grep nginx

# 实时监控（top 的简化版）
top -bn1 | head -20
```

### 进程控制

```bash
# 后台运行
./script.sh &

# 查看后台任务
jobs

# 把前台任务放到后台（暂停）
Ctrl+Z

# 恢复后台运行
bg

# 恢复到前台
fg

# 杀死进程
kill PID              # 正常终止
kill -9 PID           # 强制杀死
killall process_name  # 按名字杀
```

### 进程等待

```bash
#!/bin/bash
# 启动后台进程
./long_task.sh &
pid=$!

# 做其他事情
echo "正在等待后台任务完成..."

# 等待进程结束
wait $pid

echo "任务完成！"
```

### 进程信息

```bash
# 获取进程 ID
echo $$

# 获取父进程 ID
echo $PPID

# 查看进程树
pstree
pstree -p username

# 查看打开的文件
lsof -p PID

# 查看进程状态
cat /proc/PID/status
```

## 54.6 信号处理

信号是进程间通信的一种方式，Ctrl+C、kill 命令都是发信号。

### 常用信号

| 信号 | 编号 | 说明 |
|------|------|------|
| SIGHUP | 1 | 挂起 |
| SIGINT | 2 | 中断（Ctrl+C） |
| SIGQUIT | 3 | 退出（Ctrl+\） |
| SIGKILL | 9 | 强制杀死 |
| SIGTERM | 15 | 正常终止 |
| SIGUSR1 | 10 | 用户自定义 |
| SIGUSR2 | 12 | 用户自定义 |

### trap 命令

```bash
#!/bin/bash
# trap_demo.sh

# 捕获 Ctrl+C (SIGINT)
trap 'echo "别按 Ctrl+C，没用的！" ' SIGINT

# 捕获退出信号
trap 'echo "脚本退出中..."; exit 0' EXIT

# 捕获自定义信号
trap 'echo "收到 USR1 信号"' SIGUSR1

echo "按 Ctrl+C 试试？"
echo "PID: $$"

# 无限循环
while true; do
    sleep 1
done
```

### 发送信号

```bash
# 给进程发送信号
kill -SIGTERM PID
kill -15 PID
kill -SIGUSR1 PID

# 发送自定义信号给当前脚本
kill -SIGUSR1 $$

# 发送信号给进程组
kill -SIGTERM -PGID
```

## 54.7 管道与子Shell

### 管道

管道连接多个命令，数据从左到右流动：

```bash
# 基本管道
cat file.txt | grep "error" | sort | uniq

# 管道 tee（同时写文件）
cat file.txt | tee output.txt | grep "pattern"

# 管道 xargs（把管道输入转为命令行参数）
cat users.txt | xargs -I {} echo "处理用户: {}"

# 管道组
{ cmd1; cmd2; } | cmd3
```

### 子Shell

```bash
# 在子Shell中执行（环境隔离）
(cd /tmp; ls)        # 不会改变当前目录
pwd                   # 还是在原目录

# 子Shell 变量隔离
var=100
( var=200; echo "子Shell: $var" )
echo "父Shell: $var"  # 还是 100

# 进程替换
while read -r line; do
    echo "行: $line"
done < <(grep "pattern" file.txt)
```

### 子Shell 常用场景

```bash
# 1. 临时切换目录
(cd /tmp && do_something)

# 2. 设置临时环境
(env_var=value command)

# 3. 并行执行
./task1.sh &
./task2.sh &
./task3.sh &
wait  # 等待所有后台任务完成

# 4. 避免污染当前环境
(export PATH=/new/path:$PATH; ./script.sh)
```

## 54.8 实战脚本

让我们综合运用所学知识，写几个真正有用的脚本！

### 脚本一：日志分析器

```bash
#!/bin/bash
# log_analyzer.sh - 日志分析工具

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 检查参数
if [ $# -eq 0 ]; then
    echo "用法: $0 <日志文件>"
    exit 1
fi

LOG_FILE="$1"

if [ ! -f "$LOG_FILE" ]; then
    echo -e "${RED}错误: 文件不存在${NC}"
    exit 1
fi

echo "========================================"
echo "         日志分析报告"
echo "========================================"
echo "文件: $LOG_FILE"
echo "分析时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 总行数
total_lines=$(wc -l < "$LOG_FILE")
echo -e "${GREEN}总行数: $total_lines${NC}"

# 错误统计
error_count=$(grep -c -i "error" "$LOG_FILE" 2>/dev/null || echo 0)
echo -e "${RED}错误 (ERROR): $error_count${NC}"

# 警告统计
warning_count=$(grep -c -i "warn" "$LOG_FILE" 2>/dev/null || echo 0)
echo -e "${YELLOW}警告 (WARN): $warning_count${NC}"

# 成功统计
success_count=$(grep -c -i "success\|ok" "$LOG_FILE" 2>/dev/null || echo 0)
echo -e "${GREEN}成功 (SUCCESS/OK): $success_count${NC}"

# 错误类型分布
echo ""
echo "错误类型分布:"
grep -i "error" "$LOG_FILE" | sed 's/.*\[ERROR\]//' | awk '{print $1}' | sort | uniq -c | sort -rn | head -5

# 最近10条错误
echo ""
echo "最近10条错误:"
grep -i "error" "$LOG_FILE" | tail -10

echo ""
echo "========================================"
```

### 脚本二：系统状态监控

```bash
#!/bin/bash
# system_monitor.sh - 系统状态监控

# 设置阈值
CPU_THRESHOLD=80
MEM_THRESHOLD=80
DISK_THRESHOLD=90

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================"
echo "         系统状态监控"
echo "========================================"
echo "监控时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# CPU 使用率
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
echo -n "CPU 使用率: "
if [ "${cpu_usage%.*}" -gt $CPU_THRESHOLD ]; then
    echo -e "${RED}${cpu_usage}%${NC} [警告: 超过 ${CPU_THRESHOLD}%]"
else
    echo -e "${GREEN}${cpu_usage}%${NC} [正常]"
fi

# 内存使用率
mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
echo -n "内存使用率: "
if [ "$mem_usage" -gt $MEM_THRESHOLD ]; then
    echo -e "${RED}${mem_usage}%${NC} [警告: 超过 ${MEM_THRESHOLD}%]"
else
    echo -e "${GREEN}${mem_usage}%${NC} [正常]"
fi

# 磁盘使用率
disk_usage=$(df -h / | tail -1 | awk '{print $5}' | cut -d'%' -f1)
echo -n "磁盘使用率: "
if [ "$disk_usage" -gt $DISK_THRESHOLD ]; then
    echo -e "${RED}${disk_usage}%${NC} [警告: 超过 ${DISK_THRESHOLD}%]"
else
    echo -e "${GREEN}${disk_usage}%${NC} [正常]"
fi

# 负载
load_avg=$(uptime | awk -F'load average:' '{print $2}')
echo "系统负载: $load_avg"

# 在线用户
user_count=$(who | wc -l)
echo "在线用户: $user_count"

# TOP 5 CPU 进程
echo ""
echo "TOP 5 CPU 进程:"
ps aux --sort=-%cpu | head -6 | tail -5 | awk '{print $11, $3"% CPU"}'

# TOP 5 内存进程
echo ""
echo "TOP 5 内存进程:"
ps aux --sort=-%mem | head -6 | tail -5 | awk '{print $11, $4"% MEM"}'

echo "========================================"
```

### 脚本三：批量文件处理

```bash
#!/bin/bash
# batch_process.sh - 批量文件处理工具

# 配置
INPUT_DIR="./input"
OUTPUT_DIR="./output"
BACKUP_DIR="./backup"
LOG_FILE="batch_process.log"

# 创建目录
mkdir -p "$OUTPUT_DIR" "$BACKUP_DIR"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 处理单个文件
process_file() {
    local file="$1"
    local filename=$(basename "$file")
    
    log "处理文件: $filename"
    
    # 备份原文件
    cp "$file" "$BACKUP_DIR/$filename"
    
    # 处理逻辑（这里示例：转大写 + 行号）
    line_count=$(wc -l < "$file")
    sed -n "1p" "$file" > "$OUTPUT_DIR/$filename"
    sed -n "2,$line_count p" "$file" | \
        sed '/^$/d' | \
        awk '{print NR": "$0}' >> "$OUTPUT_DIR/$filename"
    
    log "完成: $filename -> $OUTPUT_DIR/$filename"
}

# 主逻辑
main() {
    log "========================================"
    log "批量处理开始"
    
    if [ ! -d "$INPUT_DIR" ]; then
        log "错误: 输入目录不存在"
        exit 1
    fi
    
    file_count=0
    for file in "$INPUT_DIR"/*; do
        if [ -f "$file" ]; then
            process_file "$file"
            ((file_count++))
        fi
    done
    
    log "批量处理完成，共处理 $file_count 个文件"
    log "========================================"
}

main "$@"
```

### 脚本四：MySQL 数据库备份

```bash
#!/bin/bash
# mysql_backup.sh - MySQL 数据库备份

# 配置
DB_HOST="localhost"
DB_USER="root"
DB_PASS="your_password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=7

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# 备份函数
backup_database() {
    local db_name="$1"
    local backup_file="$BACKUP_DIR/${db_name}_${DATE}.sql.gz"
    
    log "开始备份数据库: $db_name"
    
    # 执行备份
    mysqldump -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" \
        --single-transaction --routines --triggers \
        "$db_name" | gzip > "$backup_file"
    
    if [ $? -eq 0 ]; then
        log "备份成功: $backup_file"
    else
        log "备份失败: $db_name"
        return 1
    fi
}

# 清理旧备份
cleanup_old_backups() {
    log "清理 ${KEEP_DAYS} 天前的备份..."
    find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete
    log "清理完成"
}

# 主逻辑
main() {
    log "========================================"
    log "MySQL 数据库备份开始"
    
    # 获取所有数据库
    databases=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" \
        -e "SHOW DATABASES;" | grep -v Database | grep -v information_schema)
    
    for db in $databases; do
        backup_database "$db"
    done
    
    cleanup_old_backups
    
    # 显示备份文件
    log "当前备份文件:"
    ls -lh "$BACKUP_DIR"
    
    log "========================================"
    log "备份完成"
}

main "$@"
```

## 本章小结

本章我们学习了 Bash 脚本的进阶内容：

| 知识点 | 说明 |
|--------|------|
| 字符串处理 | 截取、替换、大小写、分割、去空白 |
| 正则表达式 | 模式匹配、验证、文本提取 |
| sed | 流编辑器，文本替换、删除、插入 |
| awk | 文本分析工具，字段处理、统计 |
| 进程处理 | 查看、控制、等待、信号 |
| 信号处理 | trap 捕获，自定义信号处理 |
| 管道与子Shell | 命令组合、环境隔离 |
| 实战脚本 | 日志分析、系统监控、批处理、备份 |

掌握这些技能后，你的 Shell 脚本能力将提升到一个新境界！能够处理复杂的文本分析、自动化运维等任务。

---

> 💡 **温馨提示**：
> 正则表达式和 sed/awk 是 Linux 文本处理的三剑客。它们看起来复杂，但用多了就熟练了。建议找一些日志文件多加练习，你会感受到"原来文本处理可以这么快！"

---

**第五十四章：Bash 脚本进阶 — 完结！** 🎉

下一章我们将进入"版本控制"的世界，学习 Git 版本管理系统。敬请期待！ 🚀
