"""
AI信息分析系统 - 配置文件

本模块包含系统的所有配置参数，包括：
- 文件夹路径配置
- AI模型参数配置
- 股票筛选条件配置
- 报告模板配置
"""

import os
from pathlib import Path


# ============================================================
# 基础路径配置
# ============================================================

# 系统根目录
BASE_DIR = Path(__file__).parent.parent

# 三层文件夹路径
INPUT_DIR = BASE_DIR / "input"
PROCESSING_DIR = BASE_DIR / "processing"
OUTPUT_DIR = BASE_DIR / "output"

# 确保目录存在
for directory in [INPUT_DIR, PROCESSING_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


# ============================================================
# AI模型配置（Kimi API）
# ============================================================

class KimiConfig:
    """Kimi API 配置"""
    
    # API密钥（从环境变量读取）
    API_KEY = os.getenv("KIMI_API_KEY", "")
    
    # API基础URL
    BASE_URL = "https://api.moonshot.cn/v1"
    
    # 默认模型
    DEFAULT_MODEL = "moonshot-v1-8k"
    
    # 模型参数
    TEMPERATURE = 0.7
    MAX_TOKENS = 4096


# ============================================================
# 股票筛选配置
# ============================================================

class StockScreenerConfig:
    """股票筛选配置"""
    
    # 最小提及次数（被多次提及的股票更受关注）
    MIN_MENTION_COUNT = 2
    
    # 情感分数阈值（0-1，越高越乐观）
    SENTIMENT_THRESHOLD = 0.6
    
    # 重点关注行业
    FOCUS_INDUSTRIES = [
        "新能源",
        "半导体",
        "人工智能",
        "医疗健康",
        "消费",
        "金融",
    ]
    
    # 排除的股票类型
    EXCLUDED_TYPES = [
        "ST股",
        "*ST股",
    ]


# ============================================================
# 报告模板配置
# ============================================================

class ReportTemplates:
    """报告模板"""
    
    # 每日分析报告模板
    DAILY_ANALYSIS = """# {date} 财经新闻分析

## 📰 今日要闻摘要
{news_summary}

## 📈 市场情绪
- 整体情绪：{overall_sentiment}
- 热门行业：{hot_industries}

## 🔍 重点关注股票
{stock_highlights}

## 💡 投资建议
{investment_advice}

---
*本报告由AI自动生成，仅供参考*
"""
    
    # 周报模板
    WEEKLY_REPORT = """# {year}年第{week}周 投资周报

## 📅 时间范围
{start_date} 至 {end_date}

## 🔥 本周热点
{weekly_highlights}

## 📊 行业表现
{industry_performance}

## 🏆 推荐股票列表
{recommended_stocks}

## 📝 本周总结
{weekly_summary}

## 🔮 下周展望
{next_week_outlook}

---
*本报告由AI自动生成，仅供参考*
"""
    
    # 股票筛选报告模板
    STOCK_SCREENING = """# {date} 股票筛选报告

## 筛选条件
- 最小提及次数：{min_mentions}
- 情感阈值：{sentiment_threshold}
- 关注行业：{focus_industries}

## 筛选结果

{screening_results}

## 详细分析

{detailed_analysis}

---
*本报告由AI自动生成，仅供参考*
"""


# ============================================================
# 内容分类配置
# ============================================================

class CategoryConfig:
    """内容分类配置"""
    
    # 新闻类型
    NEWS_CATEGORIES = [
        "宏观政策",
        "行业动态",
        "公司公告",
        "市场数据",
        "专家观点",
        "国际财经",
    ]
    
    # 情感标签
    SENTIMENT_LABELS = {
        "positive": "利好",
        "negative": "利空",
        "neutral": "中性",
    }


# ============================================================
# 文件命名配置
# ============================================================

class NamingConfig:
    """文件命名配置"""
    
    # 日期格式
    DATE_FORMAT = "%Y-%m-%d"
    
    # 文件名模板
    DAILY_ANALYSIS_NAME = "{date}-新闻分析.md"
    WEEKLY_REPORT_NAME = "{year}-W{week:02d}-周报.md"
    MONTHLY_REPORT_NAME = "{year}-{month:02d}-月报.md"
    STOCK_SCREENING_NAME = "{date}-股票筛选.md"
    INSIGHT_NOTE_NAME = "{date}-投资笔记.md"
