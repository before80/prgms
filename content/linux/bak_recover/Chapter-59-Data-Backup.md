+++
title = "第59章：数据备份"
weight = 590
date = "2026-03-24T13:18:28+08:00"
type = "docs"
description = ""
isCJKLanguage = true
draft = false
+++


# 第五十九章：数据备份

## 59.1 tar/rsync 备份

### 备份的重要性

> "数据丢失的那一天，你才会意识到备份有多重要。"
> —— 每一个经历过数据丢失的人

```mermaid
graph LR
    A[数据] --> B{有备份?}
    B -->|是| C[恢复数据]
    B -->|否| D[欲哭无泪]
    C --> E[继续工作]
    D --> F[重新开始?]
```

### tar 打包

tar 是 Linux 下最常用的打包工具，"tar" = "tape archive"（磁带归档）。

```bash
# 基本打包
tar -cvf archive.tar /path/to/dir

# 选项说明：
# -c: 创建档案
# -v: 显示详情
# -f: 指定文件名

# 打包并压缩
tar -czvf archive.tar.gz /path/to/dir      # gzip 压缩
tar -cjvf archive.tar.bz2 /path/to/dir    # bzip2 压缩
tar -cJvf archive.tar.xz /path/to/dir     # xz 压缩
```

### tar 解包

```bash
# 解包到当前目录
tar -xvf archive.tar

# 解包到指定目录
tar -xvf archive.tar -C /target/directory

# 解压 .tar.gz
tar -xzvf archive.tar.gz

# 解压 .tar.bz2
tar -xjvf archive.tar.bz2

# 解压 .tar.xz
tar -xJvf archive.tar.xz
```

### tar 高级用法

```bash
# 打包时排除文件
tar -czvf backup.tar.gz /data \
  --exclude='*.log' \
  --exclude='*.tmp' \
  --exclude='node_modules'

# 打包时包含特定文件
tar -czvf backup.tar.gz -T include.txt

# 查看包内容（不解压）
tar -tvf archive.tar

# 追加文件到已有包
tar -rvf archive.tar newfile.txt

# 打包时显示差异
tar -czvf backup.tar.gz -g snapshot.snar /data
```

### rsync 同步

rsync 是强大的文件同步工具，支持增量备份。

```bash
# 基本同步
rsync -av /source/ /destination/

# 选项说明：
# -a: 归档模式（保留权限、时间等）
# -v: 显示详情
# -z: 压缩传输
# -P: 显示进度并支持断点续传

# 远程同步
rsync -avz /local/path/ user@remote:/remote/path/

# SSH 传输
rsync -avz -e ssh /local/ user@remote:/remote/

# 排除文件
rsync -avz --exclude='*.log' --exclude='tmp/' /source/ /dest/
```

### rsync 增量备份

```bash
# 使用 rsync 实现增量备份
rsync -av --delete /data/ /backup/data/

# 硬链接备份（节省空间）
rsync -av --link-dest=/backup/day-1 /data/ /backup/day-2/

# 创建快照目录
backup_dir="/backup/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"
rsync -av /data/ "$backup_dir/"

# 清理旧备份（保留最近7天）
find /backup -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
```

### 备份脚本示例

```bash
#!/bin/bash
# backup.sh - 增量备份脚本

# 配置
SOURCE="/data"
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d_%H%M%S)
LOG_FILE="/var/log/backup.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 开始备份
log "========== 开始备份 =========="
log "源目录: $SOURCE"
log "目标目录: $BACKUP_DIR"

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 执行备份
if rsync -av --delete \
    --exclude='*.tmp' \
    --exclude='*.log' \
    --exclude='node_modules' \
    "$SOURCE/" "$BACKUP_DIR/latest/"; then
    
    # 创建带时间戳的快照
    cp -al "$BACKUP_DIR/latest" "$BACKUP_DIR/$DATE"
    
    log "备份成功: $DATE"
else
    log "备份失败！"
    exit 1
fi

# 清理旧备份
find "$BACKUP_DIR" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

log "========== 备份完成 =========="
```

## 59.2 数据库备份

### MySQL/MariaDB 备份

```bash
# 安装 MySQL 客户端
sudo apt install mysql-client

# 基本备份
mysqldump -u root -p database_name > backup.sql

# 备份所有数据库
mysqldump -u root -p --all-databases > all_databases.sql

# 压缩备份
mysqldldump -u root -p database_name | gzip > backup.sql.gz

# 备份特定表
mysqldump -u root -p database_name users orders > tables.sql

# 远程备份
mysqldump -h remote_host -u root -p database_name > backup.sql
```

### mysqldump 高级选项

```bash
# 完整备份（包含存储过程、触发器等）
mysqldump -u root -p \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    --master-data=2 \
    database_name > backup.sql

# 选项说明：
# --single-transaction: 事务级别备份（InnoDB）
# --routines: 存储过程和函数
# --triggers: 触发器
# --events: 事件调度器
# --master-data: 记录备份时的 binlog 位置
```

### MySQL 备份脚本

```bash
#!/bin/bash
# mysql_backup.sh

# 配置
DB_HOST="localhost"
DB_USER="root"
DB_PASS="your_password"
BACKUP_DIR="/backup/mysql"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=7

# 创建备份目录
mkdir -p "$BACKUP_DIR"

# 备份函数
backup_db() {
    local db=$1
    local backup_file="$BACKUP_DIR/${db}_${DATE}.sql.gz"
    
    echo "备份数据库: $db"
    mysqldump -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" \
        --single-transaction \
        --routines \
        --triggers \
        "$db" | gzip > "$backup_file"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ 成功: $backup_file"
    else
        echo "  ✗ 失败: $db"
        return 1
    fi
}

# 获取所有数据库
databases=$(mysql -h"$DB_HOST" -u"$DB_USER" -p"$DB_PASS" \
    -e "SHOW DATABASES;" | grep -v Database | grep -v information_schema)

# 备份每个数据库
for db in $databases; do
    backup_db "$db"
done

# 清理旧备份
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete

echo "备份完成！"
ls -lh "$BACKUP_DIR"
```

### PostgreSQL 备份

```bash
# 安装 PostgreSQL 客户端
sudo apt install postgresql-client

# 基本备份
pg_dump -U postgres database_name > backup.sql

# 压缩备份
pg_dump -U postgres database_name | gzip > backup.sql.gz

# 备份所有数据库
pg_dumpall -U postgres > all_databases.sql

# 自定义格式备份
pg_dump -U postgres -Fc database_name > backup.dump

# 远程备份
pg_dump -h remote_host -U postgres database_name > backup.sql
```

### PostgreSQL 备份脚本

```bash
#!/bin/bash
# postgresql_backup.sh

# 配置
PG_HOST="localhost"
PG_USER="postgres"
PG_PASS="your_password"
BACKUP_DIR="/backup/postgresql"
DATE=$(date +%Y%m%d_%H%M%S)
KEEP_DAYS=7

export PGPASSWORD="$PG_PASS"

mkdir -p "$BACKUP_DIR"

# 备份函数
backup_db() {
    local db=$1
    local backup_file="$BACKUP_DIR/${db}_${DATE}.sql.gz"
    
    echo "备份数据库: $db"
    pg_dump -h "$PG_HOST" -U "$PG_USER" "$db" | gzip > "$backup_file"
    
    if [ $? -eq 0 ]; then
        echo "  ✓ 成功: $backup_file"
    else
        echo "  ✗ 失败: $db"
    fi
}

# 获取所有数据库
databases=$(psql -h "$PG_HOST" -U "$PG_USER" -lqt -d postgres | cut -d \| -f 1 | sed -e 's/^//' -e 's/$//' | grep -v '^$')

# 备份
for db in $databases; do
    backup_db "$db"
done

# 清理旧备份
find "$BACKUP_DIR" -name "*.sql.gz" -mtime +$KEEP_DAYS -delete

echo "备份完成！"
```

### Redis 备份

```bash
# RDB 快照备份
redis-cli SAVE

# 后台异步备份
redis-cli BGSAVE

# 复制 rdb 文件
cp /var/lib/redis/dump.rdb /backup/redis_$(date +%Y%m%d).rdb

# AOF 备份
cp /var/lib/redis/appendonly.aof /backup/redis_$(date +%Y%m%d).aof
```

### MongoDB 备份

```bash
# 安装 mongodump
# mongodump --uri="mongodb://user:pass@host:27017"

# 基本备份
mongodump --db database_name --out /backup/mongo/

# 压缩备份
mongodump --db database_name --gzip --archive=/backup/mongo.gz

# 恢复
mongorestore --db database_name /backup/mongo/database_name/
```

## 59.3 定时备份

### cron 定时任务

```bash
# 编辑 crontab
crontab -e

# 格式：
# * * * * * command
# │ │ │ │ │
# │ │ │ │ └─── 星期 (0-7, 0和7都是周日)
# │ │ │ └───── 月份 (1-12)
# │ │ └─────── 日期 (1-31)
# │ └───────── 小时 (0-23)
# └─────────── 分钟 (0-59)
```

### 定时备份示例

```bash
# crontab -e

# 每天凌晨2点执行备份
0 2 * * * /scripts/backup.sh >> /var/log/backup.log 2>&1

# 每天凌晨2点，每小时执行一次增量备份
0 */1 * * * /scripts/incremental_backup.sh

# 每周日凌晨3点执行完整备份
0 3 * * 0 /scripts/full_backup.sh

# 每天凌晨2点MySQL备份
0 2 * * * /scripts/mysql_backup.sh

# 每月1日凌晨3点备份
0 3 1 * * /scripts/monthly_backup.sh

# 每15分钟执行一次
*/15 * * * * /scripts/check_backup_status.sh
```

### systemd 定时器

```bash
# 创建备份服务
sudo nano /etc/systemd/system/backup.service

[Unit]
Description=Data Backup Service

[Service]
Type=oneshot
ExecStart=/scripts/backup.sh
User=root

# 创建定时器
sudo nano /etc/systemd/system/backup.timer

[Unit]
Description=Backup Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target

# 启用定时器
sudo systemctl daemon-reload
sudo systemctl enable backup.timer
sudo systemctl start backup.timer

# 查看状态
systemctl list-timers
```

### 备份验证

```bash
#!/bin/bash
# verify_backup.sh - 验证备份完整性

BACKUP_DIR="/backup"
LOG_FILE="/var/log/backup_verify.log"

echo "[$(date)] 开始验证备份..." >> "$LOG_FILE"

# 检查备份文件是否存在
latest_backup=$(ls -t "$BACKUP_DIR"/*.sql.gz 2>/dev/null | head -1)

if [ -z "$latest_backup" ]; then
    echo "错误: 未找到备份文件！" >> "$LOG_FILE"
    exit 1
fi

# 验证压缩文件完整性
if gzip -t "$latest_backup" 2>/dev/null; then
    echo "✓ 备份文件完整: $latest_backup" >> "$LOG_FILE"
else
    echo "✗ 备份文件损坏: $latest_backup" >> "$LOG_FILE"
    # 发送告警
    mail -s "备份验证失败" admin@example.com << EOF
备份文件 $latest_backup 验证失败！
EOF
fi
```

## 59.4 云端备份

### AWS S3 备份

```bash
# 安装 AWS CLI
pip install awscli

# 配置
aws configure

# 基本命令
aws s3 cp backup.tar.gz s3://my-bucket/backups/
aws s3 sync /data s3://my-bucket/data/
aws s3 ls s3://my-bucket/

# 加密备份
aws s3 cp backup.tar.gz s3://my-bucket/backups/ --sse AES256

# 设置生命周期
aws s3api put-bucket-lifecycle-configuration \
    --bucket my-bucket \
    --lifecycle-configuration file://lifecycle.json
```

### S3 备份脚本

```bash
#!/bin/bash
# s3_backup.sh

BUCKET="my-backup-bucket"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="/tmp/backup_${DATE}.tar.gz"

# 创建备份
tar -czvf "$BACKUP_FILE" /data

# 上传到 S3
aws s3 cp "$BACKUP_FILE" "s3://${BUCKET}/backups/"

# 清理本地临时文件
rm -f "$BACKUP_FILE"

# 列出 S3 上的备份
aws s3 ls "s3://${BUCKET}/backups/"
```

### rclone 备份

rclone 支持多种云存储，非常适合 Linux 备份：

```bash
# 安装
curl https://rclone.org/install.sh | sudo bash

# 配置存储
rclone config

# 支持的存储类型：
# Google Drive, Dropbox, OneDrive, S3, SFTP, etc.

# 常用命令
rclone copy /local/path remote:bucket/path
rclone sync /local/path remote:bucket/path
rclone mount remote:bucket /mnt/point

# 备份到 Google Drive
rclone sync /data gdrive:backups \
    --exclude '*.tmp' \
    --exclude 'node_modules/' \
    --transfers 10 \
    --progress

# 备份到 S3
rclone sync /data s3backup:my-bucket/data \
    --s3-storage-class GLACIER
```

### rclone 定时备份

```bash
#!/bin/bash
# rclone_backup.sh

REMOTE="gdrive"
SOURCE="/data"
DEST="backups/$(hostname)/"

# 执行同步
rclone sync "$SOURCE" "${REMOTE}:${DEST}" \
    --delete-before \
    --exclude '*.tmp' \
    --exclude '.cache/**' \
    --log-file /var/log/rclone_backup.log \
    --log-level INFO

# 检查结果
if [ $? -eq 0 ]; then
    echo "备份成功！"
else
    echo "备份失败！"
fi
```

### 增量备份方案

```bash
#!/bin/bash
# incremental_cloud_backup.sh

REMOTE="gdrive"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建增量备份目录
rclone mkdir "${REMOTE}:backups/incremental/${DATE}"

# 同步到云端
rclone sync /data "${REMOTE}:backups/incremental/${DATE}" \
    --update \
    --verbose

# 清理超过30天的增量备份
rclone delete "${REMOTE}:backups/incremental/" --max-age 30d

# 同步完整备份
rclone copy /data "${REMOTE}:backups/full" --verbose
```

## 本章小结

本章我们学习了数据备份的完整方案：

| 备份类型 | 工具 | 说明 |
|---------|------|------|
| 文件备份 | tar | 打包压缩 |
| 文件同步 | rsync | 增量同步 |
| MySQL | mysqldump | SQL 导出 |
| PostgreSQL | pg_dump | SQL 导出 |
| Redis | SAVE/RDB | 快照备份 |
| 云存储 | rclone/aws cli | 多种云支持 |

备份策略：

```mermaid
graph TB
    A[备份策略] --> B[每日增量]
    A --> C[每周完整]
    A --> D[月度归档]
    
    B --> E[rsync]
    C --> F[tar + 压缩]
    D --> G[云端归档]
    
    E --> H[本地磁盘]
    F --> I[外部硬盘]
    G --> J[云存储 S3/Glacier]
```

---

> 💡 **温馨提示**：
> 备份的 3-2-1 原则：**3 份副本，2 种介质，1 份异地**。记住：不测试的备份等于没有备份！定期做恢复演练，确保备份真正可用。

---

**第五十九章：数据备份 — 完结！** 🎉

下一章我们将学习"数据恢复"，掌握文件恢复、数据库恢复、系统恢复等内容。敬请期待！ 🚀
