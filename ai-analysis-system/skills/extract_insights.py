"""
AI信息分析系统 - 洞察提取技能

从processing文件夹提取精华内容生成笔记保存到output。
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
    NamingConfig,
    OUTPUT_DIR,
)


def extract_insights(
    source_files: Optional[List[Path]] = None,
    importance_filter: str = "high",
    output_subfolder: str = "notes"
) -> dict:
    """
    从processing提取精华内容生成笔记
    
    Args:
        source_files: 源文件列表，默认为processing中所有文件
        importance_filter: 重要性过滤（high/medium/low/all）
        output_subfolder: 输出子文件夹
        
    Returns:
        提取结果字典
    """
    # 获取processing中的文件
    if source_files is None:
        all_files = file_manager.list_all_files("processing")
        source_files = [
            Path(f["path"]) 
            for f in all_files.get("processing", [])
        ]
    
    if not source_files:
        return {
            "insights_extracted": 0,
            "message": "processing文件夹中没有待处理的内容",
        }
    
    # 收集洞察
    insights = []
    
    for file_path in source_files:
        try:
            content = file_manager.read_file(file_path)
            
            # 解析并分析
            parsed = content_parser.parse_content(content, file_path.name)
            analysis = news_analyzer.analyze(parsed)
            
            # 根据重要性过滤
            if importance_filter != "all":
                if analysis.importance != importance_filter:
                    continue
            
            insights.append({
                "source": file_path.name,
                "summary": analysis.summary,
                "key_points": analysis.key_points,
                "sentiment": analysis.sentiment,
                "importance": analysis.importance,
                "industries": analysis.related_industries,
                "stocks": [s["code"] for s in analysis.related_stocks],
            })
            
        except Exception as e:
            print(f"处理 {file_path} 时出错: {e}")
    
    if not insights:
        return {
            "insights_extracted": 0,
            "message": f"没有符合条件（重要性={importance_filter}）的洞察",
        }
    
    # 生成笔记
    note_content = _format_insights_note(insights)
    
    # 保存到output
    date = datetime.now().strftime(NamingConfig.DATE_FORMAT)
    filename = NamingConfig.INSIGHT_NOTE_NAME.format(date=date)
    
    note_path = file_manager.save_to_output(
        note_content, 
        filename,
        output_subfolder
    )
    
    return {
        "insights_extracted": len(insights),
        "note_path": str(note_path),
        "insights": insights,
        "message": f"已提取 {len(insights)} 条洞察，保存到 {note_path}",
    }


def _format_insights_note(insights: List[dict]) -> str:
    """格式化洞察笔记"""
    date = datetime.now().strftime("%Y年%m月%d日")
    
    lines = [
        f"# {date} 投资洞察笔记\n",
        "## 📊 洞察概览\n",
        f"- 共提取 {len(insights)} 条重要洞察",
    ]
    
    # 统计行业分布
    industry_count = {}
    for insight in insights:
        for ind in insight["industries"]:
            industry_count[ind] = industry_count.get(ind, 0) + 1
    
    if industry_count:
        top_industries = sorted(
            industry_count.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        lines.append(f"- 热门行业：{', '.join([i[0] for i in top_industries])}")
    
    lines.append("\n---\n")
    lines.append("## 🔍 详细洞察\n")
    
    for i, insight in enumerate(insights, 1):
        sentiment_emoji = {
            "positive": "📈",
            "negative": "📉", 
            "neutral": "➖",
        }.get(insight["sentiment"], "➖")
        
        lines.append(f"### {i}. {sentiment_emoji} {insight['summary'][:50]}...\n")
        lines.append(f"**来源**：{insight['source']}")
        lines.append(f"**重要性**：{insight['importance']}")
        
        if insight["key_points"]:
            lines.append("\n**关键要点**：")
            for point in insight["key_points"][:3]:
                lines.append(f"- {point}")
        
        if insight["stocks"]:
            lines.append(f"\n**相关股票**：{', '.join(insight['stocks'])}")
        
        if insight["industries"]:
            lines.append(f"**相关行业**：{', '.join(insight['industries'])}")
        
        lines.append("\n---\n")
    
    lines.append("\n## 💡 行动建议\n")
    lines.append("基于以上洞察，建议：")
    lines.append("1. 持续关注热门行业的政策动态")
    lines.append("2. 对多次被提及的股票做进一步研究")
    lines.append("3. 结合自身风险偏好做出投资决策")
    lines.append("\n---\n")
    lines.append("*本笔记由AI辅助生成，投资需谨慎*\n")
    
    return "\n".join(lines)


def archive_processed(
    source_files: Optional[List[Path]] = None
) -> dict:
    """
    将已处理的文件归档
    
    Args:
        source_files: 要归档的文件列表
        
    Returns:
        归档结果
    """
    if source_files is None:
        all_files = file_manager.list_all_files("processing")
        source_files = [
            Path(f["path"]) 
            for f in all_files.get("processing", [])
        ]
    
    archived = []
    for file_path in source_files:
        try:
            new_path = file_manager.move_to_archive(file_path)
            archived.append(str(new_path))
        except Exception as e:
            print(f"归档 {file_path} 时出错: {e}")
    
    return {
        "archived_count": len(archived),
        "archived_files": archived,
        "message": f"已归档 {len(archived)} 个文件",
    }


if __name__ == "__main__":
    result = extract_insights()
    print(f"洞察提取完成：{result}")
