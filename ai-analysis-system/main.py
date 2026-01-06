"""
AI信息分析系统 - 主程序入口

本模块提供系统的功能演示示例。
"""

import sys
from pathlib import Path

# 确保模块可以被导入
sys.path.insert(0, str(Path(__file__).parent))

from core import (
    file_manager,
    content_parser,
    news_analyzer,
    stock_screener,
    report_generator,
    INPUT_DIR,
    PROCESSING_DIR,
    OUTPUT_DIR,
)

from skills import (
    analyze_news,
    analyze_all_pending,
    screen_stocks,
    get_top_picks,
    generate_weekly_report,
    generate_monthly_report,
    extract_insights,
    archive_processed,
)


def example_analyze_news():
    """
    示例：分析财经新闻
    
    演示如何分析 input 文件夹中的新闻文件
    """
    print("=" * 50)
    print("示例：分析财经新闻")
    print("=" * 50)
    
    # 调用分析函数
    result = analyze_news()
    
    print(f"\n分析日期: {result['date']}")
    print(f"处理文件数: {result['files_processed']}")
    print(f"消息: {result['message']}")
    
    if result['report_path']:
        print(f"报告路径: {result['report_path']}")
    
    return result


def example_screen_stocks():
    """
    示例：筛选股票
    
    演示如何基于新闻分析筛选有投资价值的股票
    """
    print("=" * 50)
    print("示例：筛选股票")
    print("=" * 50)
    
    # 调用筛选函数
    result = screen_stocks()
    
    print(f"\n筛选日期: {result['date']}")
    print(f"推荐股票数: {result.get('total_recommendations', 0)}")
    print(f"消息: {result['message']}")
    
    # 打印推荐列表
    if result.get('recommendations'):
        print("\n推荐股票列表:")
        for stock in result['recommendations'][:5]:
            print(f"  - {stock['code']} ({stock['level']}): 分数 {stock['score']}")
    
    return result


def example_generate_report():
    """
    示例：生成周报
    
    演示如何生成每周投资分析周报
    """
    print("=" * 50)
    print("示例：生成周报")
    print("=" * 50)
    
    # 调用周报生成函数
    result = generate_weekly_report()
    
    print(f"\n时间范围: {result['start_date']} 至 {result['end_date']}")
    print(f"分析文件数: {result['files_analyzed']}")
    print(f"新闻数量: {result['news_count']}")
    print(f"推荐股票数: {result['stocks_recommended']}")
    print(f"消息: {result['message']}")
    
    return result


def example_extract_insights():
    """
    示例：提取洞察
    
    演示如何从processing提取精华内容生成笔记
    """
    print("=" * 50)
    print("示例：提取洞察")
    print("=" * 50)
    
    # 调用洞察提取函数
    result = extract_insights(importance_filter="all")
    
    print(f"\n提取洞察数: {result['insights_extracted']}")
    print(f"消息: {result['message']}")
    
    if result.get('note_path'):
        print(f"笔记路径: {result['note_path']}")
    
    return result


def show_system_status():
    """
    显示系统状态
    
    展示三层文件夹的当前状态
    """
    print("=" * 50)
    print("系统状态")
    print("=" * 50)
    
    files = file_manager.list_all_files("all")
    
    for folder, file_list in files.items():
        print(f"\n📁 {folder}/")
        if file_list:
            for f in file_list[:5]:
                print(f"   - {f['name']}")
            if len(file_list) > 5:
                print(f"   ... 还有 {len(file_list) - 5} 个文件")
        else:
            print("   (空)")
    
    return files


def main():
    """
    主函数 - 运行所有示例
    """
    print("\n" + "=" * 60)
    print("   个人AI信息分析系统 - 功能演示")
    print("=" * 60)
    
    # 显示系统状态
    show_system_status()
    
    # 运行示例
    print("\n")
    example_analyze_news()
    
    print("\n")
    example_screen_stocks()
    
    print("\n")
    example_generate_report()
    
    print("\n")
    example_extract_insights()
    
    print("\n" + "=" * 60)
    print("   演示完成！")
    print("=" * 60)
    print("\n提示：将财经新闻保存到 input/ 文件夹后，")
    print("      运行相应的工作流命令来处理。")
    print("\n可用命令：")
    print("  /analyze-news        - 分析新闻")
    print("  /screen-stocks       - 筛选股票")
    print("  /generate-weekly-report - 生成周报")
    print("  /extract-insights    - 提取洞察")
    print("  /process-input       - 处理所有输入")


if __name__ == "__main__":
    main()
