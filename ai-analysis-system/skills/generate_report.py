"""
AI信息分析系统 - 周报生成技能

生成每周投资分析周报。
"""

from datetime import datetime, timedelta
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
)


def generate_weekly_report(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> dict:
    """
    生成周报
    
    Args:
        start_date: 开始日期（YYYY-MM-DD），默认本周一
        end_date: 结束日期（YYYY-MM-DD），默认今天
        
    Returns:
        生成结果字典
    """
    # 计算默认日期范围
    today = datetime.now()
    
    if end_date is None:
        end_date = today.strftime(NamingConfig.DATE_FORMAT)
    
    if start_date is None:
        # 本周一
        monday = today - timedelta(days=today.weekday())
        start_date = monday.strftime(NamingConfig.DATE_FORMAT)
    
    # 获取日期范围内的分析报告
    processing_files = file_manager.get_files_in_date_range(
        start_date, 
        end_date,
        "processing"
    )
    
    # 同时获取原始input文件进行再分析
    input_files = file_manager.get_files_in_date_range(
        start_date,
        end_date,
        "input"
    )
    
    # 合并分析
    analysis_results: List[AnalysisResult] = []
    
    for file_path in input_files:
        try:
            parsed = content_parser.parse_file(file_path)
            result = news_analyzer.analyze(parsed)
            analysis_results.append(result)
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
    
    # 股票筛选
    recommendations = stock_screener.screen(analysis_results)
    
    # 生成周报
    report_content = report_generator.generate_weekly_report(
        start_date,
        end_date,
        analysis_results,
        recommendations
    )
    
    # 保存周报
    date_obj = datetime.strptime(start_date, NamingConfig.DATE_FORMAT)
    year = date_obj.year
    week = date_obj.isocalendar()[1]
    
    filename = NamingConfig.WEEKLY_REPORT_NAME.format(year=year, week=week)
    report_path = report_generator.save_report(report_content, filename)
    
    return {
        "start_date": start_date,
        "end_date": end_date,
        "files_analyzed": len(input_files),
        "news_count": len(analysis_results),
        "stocks_recommended": len(recommendations),
        "report_path": str(report_path),
        "message": f"周报已生成：{report_path}",
    }


def generate_monthly_report(
    year: Optional[int] = None,
    month: Optional[int] = None
) -> dict:
    """
    生成月报
    
    Args:
        year: 年份，默认当前年
        month: 月份，默认当前月
        
    Returns:
        生成结果字典
    """
    today = datetime.now()
    
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    
    # 计算月份范围
    start_date = f"{year}-{month:02d}-01"
    
    # 下个月第一天 - 1天 = 本月最后一天
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    
    last_day = next_month - timedelta(days=1)
    end_date = last_day.strftime(NamingConfig.DATE_FORMAT)
    
    # 使用周报逻辑（复用代码）
    result = generate_weekly_report(start_date, end_date)
    
    # 重新保存为月报文件名
    filename = NamingConfig.MONTHLY_REPORT_NAME.format(year=year, month=month)
    report_path = report_generator.save_report(
        open(result["report_path"]).read().replace("周报", "月报"),
        filename
    )
    
    result["report_path"] = str(report_path)
    result["message"] = f"月报已生成：{report_path}"
    
    return result


if __name__ == "__main__":
    result = generate_weekly_report()
    print(f"周报生成完成：{result}")
