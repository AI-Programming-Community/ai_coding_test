# AI编码功能测试试题集

## 项目介绍

这是一个专门用于测试AI编码能力的试题集合项目。包含了各种编程语言和场景的测试用例，用于评估和验证AI在代码生成、调试、优化等方面的能力。

## 项目结构

```
.
├── README.md          # 中文说明文档
├── README.en.md       # 英文说明文档
├── LICENSE            # 许可证文件
└── questions/         # 测试题目目录
```

## 使用方法

1. 克隆此仓库
2. 根据需要选择相应的试题目录
3. 查看题目描述和要求
4. 编写或修改代码解决问题
5. 在浏览器中打开HTML文件验证结果

## 当前测试题目

### HTML/CSS导航栏布局问题
- **位置**: `questions/html-css-navigation/`
- **问题描述**: 导航栏目前靠左对齐，需要修复为居中显示
- **文件**: 
  - `index.html` - 包含导航栏结构的HTML文件
  - `styles.css` - 需要修改的CSS样式文件
- **提示**: 查看CSS文件中的注释，找到需要修改的属性

### 左侧导航栏交互问题
- **位置**: `questions/left-side-navigation/`
- **问题描述**: 左侧导航栏需要改为平时隐藏，鼠标移动到左侧时滑动显示
- **文件**: 
  - `index.html` - 包含左侧导航结构的HTML文件
  - `styles.css` - 需要修改的CSS样式文件
- **提示**: 需要添加鼠标悬停效果和滑动动画

### Redis并发读取缓存问题
- **位置**: `questions/concurrent-redis-reading/`
- **问题描述**: Redis缓存服务存在并发读取bug，需要通过运行test_cache.py发现并修复
- **文件**: 
  - `app.py` - Flask应用主文件
  - `test_cache.py` - 测试文件用于发现bug
  - `requirements.txt` - Python依赖文件
- **提示**: 运行测试文件发现具体问题，修复并发读取相关的bug

### HTML转Markdown表格支持
- **位置**: `questions/html-to-markdown/`
- **问题描述**: 现有的Ruby函数无法正确处理HTML表格转换到Markdown
- **文件**: 
  - `html_to_markdown.rb` - Ruby转换函数文件
  - `readme.md` - 问题说明文件
- **提示**: 需要添加表格转换功能，支持HTML表格到Markdown表格的转换

### 日志分析器
- **位置**: `log-analyzer`
- **问题描述**：编写一个程序，读取日志文件（例如几百MB的文本）
  - 日志格式： client_ip remote_user - [time] "method url version" status body_bytes_sent "http_referer" "http_user_agent"
  - 要求1：统计总访问量PV，统计总的UV（client_ip+http_user_agent组合），总访问独立client_ip数，总平均响应时间（request_time对应），总请求中status响应不是200的占比
  - 要求2：按http_host字段分组统计输出每个http_host访问量TOP N的url，注意从http_referer中提取http_host
  - 要求3：统计每个http_host的TOP N的url的请求次数，耗时大于1s次数，耗时大于1s的占比，最大耗时，平均耗时
  - 要求4：程序需支持流式读取（不能一次性读入内存），TOP N可以配置，默认N=5。
  - 输出：以markdown格式输出统计结果到文件
- **文件**：
  - `access_1000000.log`，从zip解压而来

### 多线程爬虫
- **问题描述**：实现一个简单的并发爬虫
  - 输入一个起始 URL 和深度 n
  - 递归抓取该页面上的链接，直到达到深度 n
  - 使用多线程/协程方式加速请求
  - 统计总共访问的页面数量，以及其中包含指定关键词的页面数量
  - 如果遇到非HTML页面，例如docx、pdf等格式，应该确保文件名保存正确
  - 下载的所有静态页面，能够互相链接，点击跳转

## 贡献

欢迎提交新的测试用例和改进意见。


## 许可证

MIT License