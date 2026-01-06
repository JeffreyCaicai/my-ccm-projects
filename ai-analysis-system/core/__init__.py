"""
AI信息分析系统 - 核心模块

统一导出所有核心功能。
"""

from .config import (
    BASE_DIR,
    INPUT_DIR,
    PROCESSING_DIR,
    OUTPUT_DIR,
    KimiConfig,
    StockScreenerConfig,
    ReportTemplates,
    CategoryConfig,
    NamingConfig,
)

from .file_manager import FileManager, file_manager
from .content_parser import ContentParser, content_parser, ParsedContent
from .analyzer import NewsAnalyzer, news_analyzer, AnalysisResult
from .stock_screener import StockScreener, stock_screener, StockRecommendation
from .report_generator import ReportGenerator, report_generator


__all__ = [
    # 配置
    "BASE_DIR",
    "INPUT_DIR",
    "PROCESSING_DIR",
    "OUTPUT_DIR",
    "KimiConfig",
    "StockScreenerConfig",
    "ReportTemplates",
    "CategoryConfig",
    "NamingConfig",
    # 文件管理
    "FileManager",
    "file_manager",
    # 内容解析
    "ContentParser",
    "content_parser",
    "ParsedContent",
    # 分析器
    "NewsAnalyzer",
    "news_analyzer",
    "AnalysisResult",
    # 股票筛选
    "StockScreener",
    "stock_screener",
    "StockRecommendation",
    # 报告生成
    "ReportGenerator",
    "report_generator",
]
