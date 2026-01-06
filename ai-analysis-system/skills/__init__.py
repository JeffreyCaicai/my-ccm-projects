"""
AI信息分析系统 - 技能模块

统一导出所有技能功能。
"""

from .analyze_news import analyze_news, analyze_all_pending
from .screen_stocks import screen_stocks, get_top_picks
from .generate_report import generate_weekly_report, generate_monthly_report
from .extract_insights import extract_insights, archive_processed


__all__ = [
    # 新闻分析
    "analyze_news",
    "analyze_all_pending",
    # 股票筛选
    "screen_stocks",
    "get_top_picks",
    # 报告生成
    "generate_weekly_report",
    "generate_monthly_report",
    # 洞察提取
    "extract_insights",
    "archive_processed",
]
