"""
AI信息分析系统 - 股票筛选技能

基于新闻分析结果筛选有投资价值的股票。
"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    file_manager,
    content_parser,
    news_analyzer,
    stock_screener,
    report_generator,
    NamingConfig,
    AnalysisResult,
    StockRecommendation,
)


def screen_stocks(
    date: Optional[str] = None,
    min_mentions: int = 2,
    sentiment_threshold: float = 0.6,
    industry_filter: Optional[str] = None
) -> dict:
    """
    筛选有投资价值的股票
    
    Args:
        date: 筛选日期，默认今天
        min_mentions: 最小提及次数
        sentiment_threshold: 情感分数阈值
        industry_filter: 可选的行业过滤
        
    Returns:
        筛选结果字典
    """
    if date is None:
        date = datetime.now().strftime(NamingConfig.DATE_FORMAT)
    
    # 获取processing中的分析结果文件
    processing_files = file_manager.get_files_by_date(date, "processing")
    
    # 如果没有当日分析结果，先进行分析
    if not processing_files:
        from .analyze_news import analyze_news
        analyze_result = analyze_news(date)
        
        if analyze_result["files_processed"] == 0:
            return {
                "date": date,
                "recommendations": [],
                "message": "没有足够的数据进行股票筛选",
            }
    
    # 重新获取所有待处理的原始文件进行分析
    input_files = file_manager.get_pending_files()
    
    analysis_results: List[AnalysisResult] = []
    for file_path in input_files:
        try:
            parsed = content_parser.parse_file(file_path)
            result = news_analyzer.analyze(parsed)
            analysis_results.append(result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
    
    if not analysis_results:
        return {
            "date": date,
            "recommendations": [],
            "message": "没有可分析的内容",
        }
    
    # 配置筛选器
    stock_screener.config.MIN_MENTION_COUNT = min_mentions
    stock_screener.config.SENTIMENT_THRESHOLD = sentiment_threshold
    
    # 执行筛选
    recommendations = stock_screener.screen(analysis_results)
    
    # 行业过滤
    if industry_filter:
        recommendations = stock_screener.filter_by_industry(
            recommendations, 
            industry_filter
        )
    
    # 生成筛选报告
    report_content = report_generator.generate_stock_screening_report(
        date,
        recommendations,
        min_mentions,
        sentiment_threshold
    )
    
    # 保存报告
    filename = NamingConfig.STOCK_SCREENING_NAME.format(date=date)
    report_path = report_generator.save_report(report_content, filename)
    
    return {
        "date": date,
        "total_recommendations": len(recommendations),
        "recommendations": [
            {
                "code": r.code,
                "name": r.name,
                "level": r.recommendation_level,
                "score": r.recommendation_score,
                "industries": r.related_industries,
            }
            for r in recommendations
        ],
        "report_path": str(report_path),
        "message": f"筛选出 {len(recommendations)} 只推荐股票",
    }


def get_top_picks(n: int = 5) -> List[dict]:
    """
    获取今日最佳推荐
    
    Args:
        n: 返回数量
        
    Returns:
        推荐股票列表
    """
    result = screen_stocks()
    return result.get("recommendations", [])[:n]


if __name__ == "__main__":
    result = screen_stocks()
    print(f"筛选结果：{result}")
