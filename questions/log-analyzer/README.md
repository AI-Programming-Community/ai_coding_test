# 日志分析程序

这是一个用于分析Web访问日志的Python程序，可以统计访问量、用户数、响应时间等信息，并按Host分组统计URL访问情况。

## 功能特性

1. 统计总访问量(PV)
2. 统计总访客数(UV)（基于client_ip + http_user_agent组合）
3. 统计独立IP数
4. 计算平均响应时间（如果日志中包含请求时间字段）
5. 计算非200状态码请求占比
6. 按Host分组统计每个Host访问量TOP N的URL
7. 统计每个Host的TOP N URL的请求次数、耗时大于1s次数、耗时大于1s占比、最大耗时、平均耗时

## 使用方法

```bash
python3 log_analyzer.py <日志文件路径> [-n <TOP N>] [-o <输出文件>]
```

### 参数说明

- `file_path`: 日志文件路径（必需）
- `-n, --top-n`: TOP N URL数量，默认为5
- `-o, --output`: 输出文件路径，默认为log_report.md

### 示例

```bash
# 分析日志文件，使用默认参数
python3 log_analyzer.py access_1000000.log

# 分析日志文件，指定TOP 10 URL，输出到指定文件
python3 log_analyzer.py access_1000000.log -n 10 -o my_report.md
```

## 日志格式要求

程序支持的标准日志格式如下：

```
client_ip remote_user - [time] "method url version" status body_bytes_sent "http_referer" "http_user_agent"
```

例如：
```
120.85.113.57 - - [23/Jun/2025:22:43:32] "POST /pub/buyerRec/saleGoodsCount/get HTTP/2.0" 200 300 "https://app.huoqingqing.com/" "Mozilla/5.0 (Linux; Android 14; 22101317C Build/UKQ1.230917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/118.0.0.0 Mobile Safari/537.36 Kuang/2.2.3"
```

可选的请求时间字段可以出现在行末：
```
client_ip remote_user - [time] "method url version" status body_bytes_sent "http_referer" "http_user_agent" request_time
```

## 输出格式

程序会生成Markdown格式的报告，包含以下内容：

1. 基本统计信息
2. 按Host分组的URL统计信息

## 注意事项

1. 程序支持流式读取大文件，不会一次性将整个文件加载到内存中
2. 如果日志中不包含请求时间字段，相关统计会显示"无数据"
3. 程序会自动从http_referer字段提取Host信息进行分组统计