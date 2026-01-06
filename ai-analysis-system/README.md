# 个人AI信息分析系统

基于Claude Code + Kimi的三层文件夹架构个人AI信息分析系统，专注于每日财经新闻和中国股市分析。

## 🎯 系统特点

- **三层流水线架构**：input → processing → output
- **自定义工作流命令**：/analyze-news、/screen-stocks 等
- **自动化分析报告**：每日分析、周报、股票推荐

## 📁 目录结构

```
ai-analysis-system/
├── input/              # 📥 原始资料（待处理）
├── processing/         # ⚙️ AI处理结果（待消化）
├── output/             # 📤 精选笔记（知识库）
├── core/               # 核心模块
├── skills/             # 技能模块
├── tests/              # 测试文件
└── main.py             # 主程序入口
```

## 🚀 快速开始

### 1. 保存财经新闻
将新闻文章保存到 `input/` 文件夹，格式：`YYYY-MM-DD-标题.md`

### 2. 运行分析
```
/analyze-news
```

### 3. 生成周报
```
/generate-weekly-report
```

### 4. 提取洞察
```
/extract-insights
```

## 💻 可用命令

| 命令 | 说明 |
|------|------|
| `/analyze-news` | 分析财经新闻，生成分析报告 |
| `/screen-stocks` | 筛选有投资价值的股票 |
| `/generate-weekly-report` | 生成每周投资分析周报 |
| `/extract-insights` | 从processing提取精华内容生成笔记 |
| `/process-input` | 处理input文件夹中的所有待处理文件 |

## 📝 文件命名规范

| 文件夹 | 命名格式 | 示例 |
|--------|----------|------|
| input | `YYYY-MM-DD-标题.md` | 2026-01-05-央行降准政策.md |
| processing | `YYYY-MM-DD-类型.md` | 2026-01-05-新闻分析.md |
| output | `YYYY-MM-DD-投资笔记.md` | 2026-01-05-投资笔记.md |

## 🔧 技术架构

- **核心模块**
  - `config.py` - 系统配置
  - `file_manager.py` - 文件管理
  - `content_parser.py` - 内容解析
  - `analyzer.py` - 新闻分析
  - `stock_screener.py` - 股票筛选
  - `report_generator.py` - 报告生成

- **技能模块**
  - `analyze_news.py` - 新闻分析技能
  - `screen_stocks.py` - 股票筛选技能
  - `generate_report.py` - 报告生成技能
  - `extract_insights.py` - 洞察提取技能

## 📊 股票筛选条件

- 最小提及次数：2次
- 情感分数阈值：0.6（偏积极）
- 重点关注行业：新能源、半导体、人工智能、医疗健康、消费、金融

## ⚠️ 免责声明

本系统仅供学习和参考使用，分析结果不构成投资建议。投资有风险，决策需谨慎。

---

*由 Claude Code + Kimi 驱动的个人AI信息分析系统*
