"""
AI信息分析系统 - 报告生成模块

本模块负责生成各类分析报告。
"""

from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional

from .analyzer import AnalysisResult
from .config import ReportTemplates, NamingConfig, PROCESSING_DIR
from .stock_screener import StockRecommendation


class ReportGenerator:
    """报告生成器"""
    
    def __init__(self):
        """初始化报告生成器"""
        self.templates = ReportTemplates()
        self.output_dir = PROCESSING_DIR
        
    def generate_daily_analysis(
        self,
        date: str,
        analysis_results: List[AnalysisResult]
    ) -> str:
        """
        生成每日分析报告
        
        Args:
            date: 日期字符串（YYYY-MM-DD）
            analysis_results: 当日新闻分析结果
            
        Returns:
            生成的Markdown报告内容
        """
        # 生成新闻摘要
        news_summary = self._format_news_summary(analysis_results)
        
        # 计算整体情感
        overall_sentiment = self._calculate_overall_sentiment(
            analysis_results
        )
        
        # 提取热门行业
        hot_industries = self._get_hot_industries(analysis_results)
        
        # 提取重点股票
        stock_highlights = self._format_stock_highlights(analysis_results)
        
        # 生成投资建议
        investment_advice = self._generate_investment_advice(
            overall_sentiment,
            hot_industries
        )
        
        # 填充模板
        report = self.templates.DAILY_ANALYSIS.format(
            date=date,
            news_summary=news_summary,
            overall_sentiment=overall_sentiment,
            hot_industries="、".join(hot_industries) or "无明显热点",
            stock_highlights=stock_highlights,
            investment_advice=investment_advice,
        )
        
        return report
    
    def generate_weekly_report(
        self,
        start_date: str,
        end_date: str,
        analysis_results: List[AnalysisResult],
        stock_recommendations: List[StockRecommendation]
    ) -> str:
        """
        生成周报
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            analysis_results: 本周所有分析结果
            stock_recommendations: 股票推荐列表
            
        Returns:
            生成的Markdown周报内容
        """
        # 获取周数
        date_obj = datetime.strptime(start_date, NamingConfig.DATE_FORMAT)
        year = date_obj.year
        week = date_obj.isocalendar()[1]
        
        # 本周热点
        weekly_highlights = self._format_weekly_highlights(analysis_results)
        
        # 行业表现
        industry_performance = self._format_industry_performance(
            analysis_results
        )
        
        # 推荐股票
        recommended_stocks = self._format_recommendations(
            stock_recommendations
        )
        
        # 周总结
        weekly_summary = self._generate_weekly_summary(analysis_results)
        
        # 下周展望
        next_week_outlook = self._generate_outlook()
        
        report = self.templates.WEEKLY_REPORT.format(
            year=year,
            week=week,
            start_date=start_date,
            end_date=end_date,
            weekly_highlights=weekly_highlights,
            industry_performance=industry_performance,
            recommended_stocks=recommended_stocks,
            weekly_summary=weekly_summary,
            next_week_outlook=next_week_outlook,
        )
        
        return report
    
    def generate_stock_screening_report(
        self,
        date: str,
        recommendations: List[StockRecommendation],
        min_mentions: int = 2,
        sentiment_threshold: float = 0.6
    ) -> str:
        """
        生成股票筛选报告
        
        Args:
            date: 日期
            recommendations: 推荐列表
            min_mentions: 最小提及次数
            sentiment_threshold: 情感阈值
            
        Returns:
            生成的Markdown报告内容
        """
        # 格式化筛选结果
        screening_results = self._format_screening_results(recommendations)
        
        # 详细分析
        detailed_analysis = self._format_detailed_analysis(recommendations)
        
        from .config import StockScreenerConfig
        
        report = self.templates.STOCK_SCREENING.format(
            date=date,
            min_mentions=min_mentions,
            sentiment_threshold=sentiment_threshold,
            focus_industries="、".join(StockScreenerConfig.FOCUS_INDUSTRIES),
            screening_results=screening_results,
            detailed_analysis=detailed_analysis,
        )
        
        return report
    
    def save_report(
        self, 
        content: str, 
        filename: str,
        output_dir: Optional[Path] = None
    ) -> Path:
        """
        保存报告到文件
        
        Args:
            content: 报告内容
            filename: 文件名
            output_dir: 输出目录，默认为processing
            
        Returns:
            保存的文件路径
        """
        target_dir = output_dir or self.output_dir
        file_path = target_dir / filename
        file_path.write_text(content, encoding="utf-8")
        return file_path
    
    # ========== 私有辅助方法 ==========
    
    def _format_news_summary(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """格式化新闻摘要"""
        if not results:
            return "今日暂无重要财经新闻。"
            
        lines = []
        for i, result in enumerate(results[:5], 1):
            sentiment_emoji = {
                "positive": "📈",
                "negative": "📉",
                "neutral": "➖",
            }.get(result.sentiment, "➖")
            
            lines.append(f"{i}. {sentiment_emoji} {result.summary}")
            
        return "\n".join(lines)
    
    def _calculate_overall_sentiment(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """计算整体市场情感"""
        if not results:
            return "中性"
            
        avg_score = sum(r.sentiment_score for r in results) / len(results)
        
        if avg_score > 0.6:
            return "偏乐观 📈"
        elif avg_score < 0.4:
            return "偏悲观 📉"
        else:
            return "中性 ➖"
    
    def _get_hot_industries(
        self, 
        results: List[AnalysisResult]
    ) -> List[str]:
        """获取热门行业"""
        industry_count = {}
        for result in results:
            for ind in result.related_industries:
                industry_count[ind] = industry_count.get(ind, 0) + 1
                
        # 按出现次数排序，取前5
        sorted_industries = sorted(
            industry_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return [ind for ind, _ in sorted_industries[:5]]
    
    def _format_stock_highlights(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """格式化重点股票"""
        all_stocks = {}
        for result in results:
            for stock in result.related_stocks:
                code = stock["code"]
                if code not in all_stocks:
                    all_stocks[code] = {
                        "info": stock,
                        "count": 0,
                        "positive": 0,
                    }
                all_stocks[code]["count"] += 1
                if result.sentiment == "positive":
                    all_stocks[code]["positive"] += 1
        
        if not all_stocks:
            return "今日暂无明显的股票热点。"
        
        # 按提及次数排序
        sorted_stocks = sorted(
            all_stocks.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:5]
        
        lines = ["| 代码 | 名称 | 提及次数 | 积极消息 |",
                 "|------|------|----------|----------|"]
        for code, data in sorted_stocks:
            lines.append(
                f"| {code} | {data['info'].get('name', '-')} | "
                f"{data['count']} | {data['positive']} |"
            )
            
        return "\n".join(lines)
    
    def _generate_investment_advice(
        self,
        sentiment: str,
        industries: List[str]
    ) -> str:
        """生成投资建议"""
        advice = []
        
        if "乐观" in sentiment:
            advice.append("市场情绪偏暖，可适当关注热点板块机会。")
        elif "悲观" in sentiment:
            advice.append("市场情绪偏冷，建议保持谨慎，控制仓位。")
        else:
            advice.append("市场情绪中性，建议保持观望，等待明确信号。")
        
        if industries:
            advice.append(f"重点关注行业：{' / '.join(industries[:3])}。")
            
        return "\n".join(advice)
    
    def _format_weekly_highlights(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """格式化本周热点"""
        high_importance = [r for r in results if r.importance == "high"]
        
        if not high_importance:
            return "本周暂无特别重大事件。"
            
        lines = []
        for result in high_importance[:5]:
            lines.append(f"- {result.summary}")
            
        return "\n".join(lines)
    
    def _format_industry_performance(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """格式化行业表现"""
        industry_sentiment = {}
        for result in results:
            for ind in result.related_industries:
                if ind not in industry_sentiment:
                    industry_sentiment[ind] = {"scores": [], "count": 0}
                industry_sentiment[ind]["scores"].append(
                    result.sentiment_score
                )
                industry_sentiment[ind]["count"] += 1
        
        if not industry_sentiment:
            return "本周行业表现数据不足。"
        
        lines = ["| 行业 | 热度 | 平均情感 |",
                 "|------|------|----------|"]
        for ind, data in sorted(
            industry_sentiment.items(),
            key=lambda x: x[1]["count"],
            reverse=True
        )[:8]:
            avg_score = sum(data["scores"]) / len(data["scores"])
            sentiment_str = "🔥" if avg_score > 0.6 else (
                "❄️" if avg_score < 0.4 else "➖"
            )
            lines.append(
                f"| {ind} | {data['count']}篇 | {sentiment_str} |"
            )
            
        return "\n".join(lines)
    
    def _format_recommendations(
        self, 
        recommendations: List[StockRecommendation]
    ) -> str:
        """格式化股票推荐"""
        if not recommendations:
            return "本周暂无符合条件的推荐股票。"
            
        lines = ["| 代码 | 名称 | 推荐等级 | 分数 | 相关行业 |",
                 "|------|------|----------|------|----------|"]
        
        level_emoji = {
            "strong": "⭐⭐⭐",
            "moderate": "⭐⭐",
            "watch": "⭐",
        }
        
        for rec in recommendations[:10]:
            industries = "、".join(rec.related_industries[:2])
            lines.append(
                f"| {rec.code} | {rec.name} | "
                f"{level_emoji.get(rec.recommendation_level, '⭐')} | "
                f"{rec.recommendation_score} | {industries} |"
            )
            
        return "\n".join(lines)
    
    def _generate_weekly_summary(
        self, 
        results: List[AnalysisResult]
    ) -> str:
        """生成周总结"""
        total = len(results)
        positive = sum(1 for r in results if r.sentiment == "positive")
        negative = sum(1 for r in results if r.sentiment == "negative")
        
        return (
            f"本周共分析 {total} 条财经信息，其中积极消息 {positive} 条，"
            f"消极消息 {negative} 条。"
        )
    
    def _generate_outlook(self) -> str:
        """生成下周展望"""
        return (
            "持续关注宏观政策动向和行业热点变化，"
            "注意控制风险，把握结构性机会。"
        )
    
    def _format_screening_results(
        self, 
        recommendations: List[StockRecommendation]
    ) -> str:
        """格式化筛选结果摘要"""
        if not recommendations:
            return "未筛选出符合条件的股票。"
            
        strong = [r for r in recommendations if r.recommendation_level == "strong"]
        moderate = [r for r in recommendations if r.recommendation_level == "moderate"]
        watch = [r for r in recommendations if r.recommendation_level == "watch"]
        
        return f"""
- 强烈推荐：{len(strong)} 只
- 适度关注：{len(moderate)} 只
- 持续观察：{len(watch)} 只
"""
    
    def _format_detailed_analysis(
        self, 
        recommendations: List[StockRecommendation]
    ) -> str:
        """格式化详细分析"""
        if not recommendations:
            return "无详细分析。"
            
        lines = []
        for rec in recommendations[:5]:
            lines.append(f"""
### {rec.code} - {rec.name}

- **推荐等级**：{rec.recommendation_level}
- **推荐分数**：{rec.recommendation_score}
- **提及次数**：{rec.mention_count}
- **平均情感**：{rec.avg_sentiment:.2f}
- **相关行业**：{', '.join(rec.related_industries)}

**相关新闻**：
""")
            for news in rec.key_news:
                lines.append(f"- {news}")
                
        return "\n".join(lines)


# 模块级便捷实例
report_generator = ReportGenerator()
