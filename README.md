# 🛒 淘宝商品搜索结果批量采集脚本

> 基于 Python 的电商数据采集工具 | 简历实战项目 1

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

## 📌 项目简介

按关键词批量采集淘宝搜索结果，支持自定义翻页深度、关键词、输出格式，含数据清洗与去重。

**适用场景**：
- 电商选品分析
- 商品价格监控
- 竞品数据调研
- 个人学习与研究

## ✨ 核心功能

- 🔍 **关键词搜索**：支持任意商品类目（耳机、衣服、数码等）
- 📄 **多页翻页**：自动翻页采集，每页 44 条
- 🧹 **数据清洗**：价格数值化、销量文本标准化、按链接去重
- 💾 **多格式导出**：Excel（.xlsx）+ CSV（带 BOM，Excel 直接打开不乱码）
- 🛡️ **反爬策略**：随机 User-Agent + 请求间隔 + 失败重试
- 📊 **结构化输出**：8 大字段（标题/价格/销量/店铺/地区/链接/商品图/评价数）

## 🛠 技术栈

```
Python 3.8+
├── requests      # HTTP 请求
├── beautifulsoup4 # HTML 解析
├── lxml          # 解析引擎
├── pandas        # 数据处理
└── openpyxl      # Excel 写入
```

## 📁 项目结构

```
taobao-spider/
├── spider.py          # 主爬虫脚本（核心）
├── requirements.txt   # 依赖清单
├── README.md          # 项目说明（本文件）
├── .gitignore         # Git 忽略文件
└── examples/          # 示例输出
    └── taobao_蓝牙耳机.xlsx
```

## 🚀 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/alight1431/taobao-spider.git
cd taobao-spider
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 运行爬虫
```bash
python spider.py
```

### 4. 自定义关键词与页数
编辑 `spider.py` 末尾：
```python
KEYWORD = "你的商品关键词"  # 如 "蓝牙耳机" / "运动鞋"
PAGES = 5                  # 采集页数（每页 44 条）
```

## 📊 数据字段

| 字段 | 说明 | 示例 |
|---|---|---|
| `title` | 商品标题 | 索尼 WH-1000XM4 头戴式耳机 |
| `price` | 售价（数值型） | 1599.0 |
| `sales` | 销量（清洗后） | 1.2万+ |
| `shop` | 店铺名 | 索尼官方旗舰店 |
| `link` | 商品详情链接 | https://item.taobao.com/... |

## 🛡️ 反爬策略

- ✅ **随机 User-Agent**：模拟不同浏览器
- ✅ **请求间隔**：1.5-3.0 秒随机延迟
- ✅ **失败重试**：最多 3 次自动重试
- ✅ **超时控制**：单次请求 10 秒超时

## ⚠️ 免责声明

> **本项目仅供学习与个人研究使用，请遵守以下原则：**
>
> 1. 遵守淘宝 [robots 协议](https://www.taobao.com/robots.txt) 与服务条款
> 2. 控制采集频率，**不要对服务器造成过大压力**
> 3. **不要用于商业爬取、数据贩卖、恶意竞争等违法用途**
> 4. 采集数据请妥善保管，**不要泄露他人隐私**
>
> 因不当使用本项目造成的法律后果，由使用者自行承担。

## 📈 后续优化方向

- [ ] 加入 Selenium 处理登录态
- [ ] 接入代理 IP 池
- [ ] 加入分布式爬取（Scrapy-Redis）
- [ ] 数据可视化（Matplotlib 销量分布图）
- [ ] 定时任务调度（APScheduler）

## 🤝 贡献

欢迎提交 Issue 与 PR！

## 📄 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**作者**：季先生 · 合肥经济学院 · 软件工程 · 2026 应届
**目标岗位**：爬虫工程师 / 数据采集工程师 · 杭州
**联系方式**：193 5846 7674 / 1813422236@qq.com

