+++
title = "ASCII 字符对照表"
date = 2026-04-18T11:10:22+08:00
weight = 1
type = "docs"
description = ""
isCJKLanguage = true
draft = false

+++

# 📋 完整 ASCII 字符对照表（0-127）

# 🔧 一、控制字符（Control Characters, 0-31 & 127）

> 注：控制字符在日常交流中极少读全名，编程/通信中通常直接使用缩写（如 `LF`, `ESC`）。下表按官方标准提供完整名称与读音。

| Dec  | Hex  | 字符 | 缩写 | 英文全称                  | 英语读音 (IPA)             | 主要用途                     |
| :--: | :--: | :--: | :--: | :------------------------ | :------------------------- | ---------------------------- |
|  0   |  00  | `␀`  | NUL  | Null                      | /nʌl/                      | 空字符，C语言字符串结尾 `\0` |
|  1   |  01  | `␁`  | SOH  | Start of Heading          | /stɑːrt əv ˈhɛdɪŋ/         | 通信协议：帧头开始           |
|  2   |  02  | `␂`  | STX  | Start of Text             | /stɑːrt əv tɛkst/          | 正文数据开始                 |
|  3   |  03  | `␃`  | ETX  | End of Text               | /ɛnd əv tɛkst/             | 正文数据结束                 |
|  4   |  04  | `␄`  | EOT  | End of Transmission       | /ɛnd əv trænzˈmɪʃən/       | 传输结束                     |
|  5   |  05  | `␅`  | ENQ  | Enquiry                   | /ˈɪŋkwəri/                 | 请求接收方响应               |
|  6   |  06  | `␆`  | ACK  | Acknowledge               | /əkˈnɒlɪdʒ/                | 确认接收成功                 |
|  7   |  07  | `␇`  | BEL  | Bell                      | /bɛl/                      | 终端响铃/提示音 🔔            |
|  8   |  08  | `␈`  |  BS  | Backspace                 | /ˈbækspeɪs/                | 退格删除前字符 ←             |
|  9   |  09  | `␉`  |  HT  | Horizontal Tab            | /ˌhɔːrəˈzɒntəl tæb/        | 水平制表符 →                 |
|  10  |  0A  | `␊`  |  LF  | Line Feed                 | /laɪn fiːd/                | 换行（Unix/Linux `\n`）      |
|  11  |  0B  | `␋`  |  VT  | Vertical Tab              | /ˈvɜːrtɪkəl tæb/           | 垂直制表（极少用）           |
|  12  |  0C  | `␌`  |  FF  | Form Feed                 | /fɔːrm fiːd/               | 打印机换页                   |
|  13  |  0D  | `␍`  |  CR  | Carriage Return           | /ˈkærɪdʒ rɪˈtɜːrn/         | 回车（Mac `\r`, Win `\r\n`） |
|  14  |  0E  | `␎`  |  SO  | Shift Out                 | /ʃɪft aʊt/                 | 切换备用字符集               |
|  15  |  0F  | `␏`  |  SI  | Shift In                  | /ʃɪft ɪn/                  | 切回默认字符集               |
|  16  |  10  | `␐`  | DLE  | Data Link Escape          | /ˈdeɪtə lɪŋk ɪˈskeɪp/      | 转义控制字符                 |
|  17  |  11  | `␑`  | DC1  | Device Control 1          | /dɪˈvaɪs kənˈtroʊl wʌn/    | 设备控制（常作 XON）         |
|  18  |  12  | `␒`  | DC2  | Device Control 2          | /dɪˈvaɪs kənˈtroʊl tuː/    | 设备控制                     |
|  19  |  13  | `␓`  | DC3  | Device Control 3          | /dɪˈvaɪs kənˈtroʊl θriː/   | 设备控制（常作 XOFF）        |
|  20  |  14  | `␔`  | DC4  | Device Control 4          | /dɪˈvaɪs kənˈtroʊl fɔːr/   | 设备控制                     |
|  21  |  15  | `␕`  | NAK  | Negative Acknowledge      | /ˈnɛɡətɪv əkˈnɒlɪdʒ/       | 否定确认/请求重传            |
|  22  |  16  | `␖`  | SYN  | Synchronous Idle          | /ˈsɪŋkrənəs ˈaɪdl/         | 同步空闲字符                 |
|  23  |  17  | `␗`  | ETB  | End of Transmission Block | /ɛnd əv trænzˈmɪʃən blɑːk/ | 数据块结束                   |
|  24  |  18  | `␘`  | CAN  | Cancel                    | /ˈkænsəl/                  | 取消当前操作                 |
|  25  |  19  | `␙`  |  EM  | End of Medium             | /ɛnd əv ˈmiːdiəm/          | 存储介质结束标记             |
|  26  |  1A  | `␚`  | SUB  | Substitute                | /ˈsʌbstɪtjuːt/             | 替换无效/错误字符            |
|  27  |  1B  | `␛`  | ESC  | Escape                    | /ɪˈskeɪp/                  | 转义/退出键 ⎋                |
|  28  |  1C  | `␜`  |  FS  | File Separator            | /faɪl ˈsɛpəreɪtər/         | 文件级数据分隔               |
|  29  |  1D  | `␝`  |  GS  | Group Separator           | /ɡruːp ˈsɛpəreɪtər/        | 组级数据分隔                 |
|  30  |  1E  | `␞`  |  RS  | Record Separator          | /ˈrɛkɔːrd ˈsɛpəreɪtər/     | 记录级数据分隔               |
|  31  |  1F  | `␟`  |  US  | Unit Separator            | /ˈjuːnɪt ˈsɛpəreɪtər/      | 字段/单元级分隔              |
| 127  |  7F  | `␡`  | DEL  | Delete                    | /dɪˈliːt/                  | 删除（打孔纸带擦除）         |

---

## 🔣 二、可打印字符：空格、标点与符号（32-47, 58-64, 91-96, 123-126）

| Dec  | Hex  |  字符   | 标准英文名                    | 英语读音 (IPA)              | 常见场景           |
| :--: | :--: | :-----: | :---------------------------- | :-------------------------- | ------------------ |
|  32  |  20  |   ` `   | Space                         | /speɪs/                     | 空格               |
|  33  |  21  |   `!`   | Exclamation Mark              | /ˌɛkskləˈmeɪʃən mɑːrk/      | 感叹号             |
|  34  |  22  |   `"`   | Quotation Mark / Double Quote | /kwoʊˈteɪʃən mɑːrk/         | 双引号             |
|  35  |  23  |   `#`   | Number Sign / Hash            | /ˈnʌmbər saɪn/              | 井号/标签          |
|  36  |  24  |   `$`   | Dollar Sign                   | /ˈdɒlər saɪn/               | 美元/变量前缀      |
|  37  |  25  |   `%`   | Percent Sign                  | /pərˈsɛnt saɪn/             | 百分号/取模        |
|  38  |  26  |   `&`   | Ampersand                     | /ˈæmpərsænd/                | 逻辑与/和号        |
|  39  |  27  |   `'`   | Apostrophe / Single Quote     | /əˈpɒstrəfi/                | 单引号/撇号        |
|  40  |  28  |   `(`   | Left Parenthesis              | /lɛft pəˈrɛnθəsɪs/          | 左圆括号           |
|  41  |  29  |   `)`   | Right Parenthesis             | /raɪt pəˈrɛnθəsɪs/          | 右圆括号           |
|  42  |  2A  |   `*`   | Asterisk                      | /ˈæstərɪsk/                 | 星号/乘法/通配符   |
|  43  |  2B  |   `+`   | Plus Sign                     | /plʌs saɪn/                 | 加号/正号          |
|  44  |  2C  |   `,`   | Comma                         | /ˈkɒmə/                     | 逗号               |
|  45  |  2D  |   `-`   | Hyphen-Minus / Dash           | /ˈhaɪfən ˈmaɪnəs/           | 连字符/减号        |
|  46  |  2E  |   `.`   | Period / Full Stop / Dot      | /ˈpɪəriəd/                  | 句号/小数点        |
|  47  |  2F  |   `/`   | Slash / Forward Slash         | /slæʃ/                      | 斜杠/除法/路径     |
|  58  |  3A  |   `:`   | Colon                         | /ˈkoʊlən/                   | 冒号               |
|  59  |  3B  |   `;`   | Semicolon                     | /ˈsɛmikoʊlən/               | 分号               |
|  60  |  3C  |   `<`   | Less-Than Sign                | /lɛs ðæn saɪn/              | 小于号             |
|  61  |  3D  |   `=`   | Equals Sign                   | /ˈiːkwəlz saɪn/             | 等号/赋值          |
|  62  |  3E  |   `>`   | Greater-Than Sign             | /ˈɡreɪtər ðæn saɪn/         | 大于号             |
|  63  |  3F  |   `?`   | Question Mark                 | /ˈkwɛstʃən mɑːrk/           | 问号               |
|  64  |  40  |   `@`   | At Sign / At Symbol           | /æt saɪn/                   | 邮箱符/修饰器      |
|  91  |  5B  |   `[`   | Left Square Bracket           | /lɛft skwɛr ˈbrækɪt/        | 左方括号           |
|  92  |  5C  |   `\`   | Backslash                     | /ˈbækslæʃ/                  | 反斜杠/转义/路径   |
|  93  |  5D  |   `]`   | Right Square Bracket          | /raɪt skwɛr ˈbrækɪt/        | 右方括号           |
|  94  |  5E  |   `^`   | Circumflex / Caret            | /ˈsɜːrkəmfleks/ · /ˈkærət/  | 脱字符/幂运算/异或 |
|  95  |  5F  |   `_`   | Underscore                    | /ˌʌndərˈskɔːr/              | 下划线             |
|  96  |  60  | `` ` `` | Grave Accent / Backtick       | /ɡreɪv ˈæksənt/ · /ˈbæktɪk/ | 反引号/命令替换    |
| 123  |  7B  |   `{`   | Left Curly Brace / Bracket    | /lɛft ˈkɜːrli breɪs/        | 左花括号/代码块    |
| 124  |  7C  |   `|`   | Vertical Bar / Pipe           | /ˈvɜːrtɪkəl bɑːr/ · /paɪp/  | 竖线/逻辑或/管道   |
| 125  |  7D  |   `}`   | Right Curly Brace / Bracket   | /raɪt ˈkɜːrli breɪs/        | 右花括号/代码块    |
| 126  |  7E  |   `~`   | Tilde                         | /ˈtɪldə/                    | 波浪号/近似/家目录 |

---

## 🔢 三、可打印字符：数字（Digits, 48-57）

| Dec  | Hex  | 字符 | 英文名称 | 英语读音 (IPA) |
| :--: | :--: | :--: | :------- | :------------- |
|  48  |  30  | `0`  | Zero     | /ˈzɪəroʊ/      |
|  49  |  31  | `1`  | One      | /wʌn/          |
|  50  |  32  | `2`  | Two      | /tuː/          |
|  51  |  33  | `3`  | Three    | /θriː/         |
|  52  |  34  | `4`  | Four     | /fɔːr/         |
|  53  |  35  | `5`  | Five     | /faɪv/         |
|  54  |  36  | `6`  | Six      | /sɪks/         |
|  55  |  37  | `7`  | Seven    | /ˈsɛvən/       |
|  56  |  38  | `8`  | Eight    | /eɪt/          |
|  57  |  39  | `9`  | Nine     | /naɪn/         |

---

## 🔤 四、可打印字符：英文字母（Letters, 65-122）
> 📌 注：大写字母与小写字母的**英文名称与读音完全一致**，仅字形不同。下表为完整 52 行展开版，方便对照查阅。

| Dec  | Hex  | 字符 | 类型 | 英文名称 | 英语读音 (IPA)          |
| :--: | :--: | :--: | :--: | :------- | :---------------------- |
|  65  |  41  | `A`  | 大写 | A        | /eɪ/                    |
|  66  |  42  | `B`  | 大写 | B        | /biː/                   |
|  67  |  43  | `C`  | 大写 | C        | /siː/                   |
|  68  |  44  | `D`  | 大写 | D        | /diː/                   |
|  69  |  45  | `E`  | 大写 | E        | /iː/                    |
|  70  |  46  | `F`  | 大写 | F        | /ɛf/                    |
|  71  |  47  | `G`  | 大写 | G        | /dʒiː/                  |
|  72  |  48  | `H`  | 大写 | H        | /eɪtʃ/                  |
|  73  |  49  | `I`  | 大写 | I        | /aɪ/                    |
|  74  |  4A  | `J`  | 大写 | J        | /dʒeɪ/                  |
|  75  |  4B  | `K`  | 大写 | K        | /keɪ/                   |
|  76  |  4C  | `L`  | 大写 | L        | /ɛl/                    |
|  77  |  4D  | `M`  | 大写 | M        | /ɛm/                    |
|  78  |  4E  | `N`  | 大写 | N        | /ɛn/                    |
|  79  |  4F  | `O`  | 大写 | O        | /oʊ/                    |
|  80  |  50  | `P`  | 大写 | P        | /piː/                   |
|  81  |  51  | `Q`  | 大写 | Q        | /kjuː/                  |
|  82  |  52  | `R`  | 大写 | R        | /ɑːr/                   |
|  83  |  53  | `S`  | 大写 | S        | /ɛs/                    |
|  84  |  54  | `T`  | 大写 | T        | /tiː/                   |
|  85  |  55  | `U`  | 大写 | U        | /juː/                   |
|  86  |  56  | `V`  | 大写 | V        | /viː/                   |
|  87  |  57  | `W`  | 大写 | W        | /ˈdʌbəljuː/             |
|  88  |  58  | `X`  | 大写 | X        | /ɛks/                   |
|  89  |  59  | `Y`  | 大写 | Y        | /waɪ/                   |
|  90  |  5A  | `Z`  | 大写 | Z        | /ziː/ (美) · /zɛd/ (英) |
|  97  |  61  | `a`  | 小写 | a        | /eɪ/                    |
|  98  |  62  | `b`  | 小写 | b        | /biː/                   |
|  99  |  63  | `c`  | 小写 | c        | /siː/                   |
| 100  |  64  | `d`  | 小写 | d        | /diː/                   |
| 101  |  65  | `e`  | 小写 | e        | /iː/                    |
| 102  |  66  | `f`  | 小写 | f        | /ɛf/                    |
| 103  |  67  | `g`  | 小写 | g        | /dʒiː/                  |
| 104  |  68  | `h`  | 小写 | h        | /eɪtʃ/                  |
| 105  |  69  | `i`  | 小写 | i        | /aɪ/                    |
| 106  |  6A  | `j`  | 小写 | j        | /dʒeɪ/                  |
| 107  |  6B  | `k`  | 小写 | k        | /keɪ/                   |
| 108  |  6C  | `l`  | 小写 | l        | /ɛl/                    |
| 109  |  6D  | `m`  | 小写 | m        | /ɛm/                    |
| 110  |  6E  | `n`  | 小写 | n        | /ɛn/                    |
| 111  |  6F  | `o`  | 小写 | o        | /oʊ/                    |
| 112  |  70  | `p`  | 小写 | p        | /piː/                   |
| 113  |  71  | `q`  | 小写 | q        | /kjuː/                  |
| 114  |  72  | `r`  | 小写 | r        | /ɑːr/                   |
| 115  |  73  | `s`  | 小写 | s        | /ɛs/                    |
| 116  |  74  | `t`  | 小写 | t        | /tiː/                   |
| 117  |  75  | `u`  | 小写 | u        | /juː/                   |
| 118  |  76  | `v`  | 小写 | v        | /viː/                   |
| 119  |  77  | `w`  | 小写 | w        | /ˈdʌbəljuː/             |
| 120  |  78  | `x`  | 小写 | x        | /ɛks/                   |
| 121  |  79  | `y`  | 小写 | y        | /waɪ/                   |
| 122  |  7A  | `z`  | 小写 | z        | /ziː/ (美) · /zɛd/ (英) |

