"""
AI信息分析系统 - 新闻分析技能

提供财经新闻分析功能的技能模块。
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
    report_generator,
    NamingConfig,
    AnalysisResult,
)


def analyze_news(
    date: Optional[str] = None,
    files: Optional[List[Path]] = None
) -> dict:
    """
    分析财经新闻
    
    Args:
        date: 要分析的日期（YYYY-MM-DD），默认为今天
        files: 直接指定要分析的文件列表，覆盖date参数
        
    Returns:
        分析结果字典，包含：
        - date: 分析日期
        - files_processed: 处理的文件数
        - analysis_results: 分析结果列表
        - report_path: 生成的报告路径
    """
    # 确定日期
    if date is None:
        date = datetime.now().strftime(NamingConfig.DATE_FORMAT)
    
    # 获取待分析文件
    if files is None:
        files = file_manager.get_files_by_date(date, "input")
        
        # 如果没有指定日期的文件，获取所有待处理文件
        if not files:
            files = file_manager.get_pending_files()
    
    if not files:
        return {
            "date": date,
            "files_processed": 0,
            "analysis_results": [],
            "report_path": None,
            "message": "没有找到待分析的文件",
        }
    
    # 分析每个文件
    analysis_results: List[AnalysisResult] = []
    
    for file_path in files:
        try:
            # 解析内容
            parsed = content_parser.parse_file(file_path)
            
            # 分析内容
            result = news_analyzer.analyze(parsed)
            analysis_results.append(result)
            
        except Exception as e:
            print(f"处理文件 {file_path} 时出错: {e}")
            continue
    
    # 生成每日分析报告
    report_content = report_generator.generate_daily_analysis(
        date, 
        analysis_results
    )
    
    # 保存报告
    filename = NamingConfig.DAILY_ANALYSIS_NAME.format(date=date)
    report_path = report_generator.save_report(report_content, filename)
    
    return {
        "date": date,
        "files_processed": len(files),
        "analysis_results": [
            {
                "summary": r.summary,
                "sentiment": r.sentiment,
                "importance": r.importance,
                "industries": r.related_industries,
            }
            for r in analysis_results
        ],
        "report_path": str(report_path),
        "message": f"成功分析 {len(files)} 个文件，报告已保存",
    }


def analyze_all_pending() -> dict:
    """
    分析所有待处理的文件
    
    Returns:
        分析结果
    """
    pending_files = file_manager.get_pending_files()
    return analyze_news(files=pending_files)


if __name__ == "__main__":
    # 示例用法
    result = analyze_news()
    print(f"分析完成：{result}")
