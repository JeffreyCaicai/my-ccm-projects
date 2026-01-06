"""
AI信息分析系统 - 股票筛选模块

本模块负责基于新闻分析结果筛选有投资价值的股票。
"""

from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional

from .analyzer import AnalysisResult
from .config import StockScreenerConfig


@dataclass
class StockRecommendation:
    """股票推荐结果"""
    
    code: str
    name: str
    market: str
    mention_count: int
    avg_sentiment: float
    related_industries: List[str]
    key_news: List[str]
    recommendation_score: float
    recommendation_level: str  # strong, moderate, watch


class StockScreener:
    """股票筛选器"""
    
    def __init__(self, config: Optional[StockScreenerConfig] = None):
        """
        初始化筛选器
        
        Args:
            config: 筛选配置，默认使用StockScreenerConfig
        """
        self.config = config or StockScreenerConfig()
        
    def screen(
        self, 
        analysis_results: List[AnalysisResult]
    ) -> List[StockRecommendation]:
        """
        根据分析结果筛选股票
        
        Args:
            analysis_results: 新闻分析结果列表
            
        Returns:
            股票推荐列表，按推荐分数排序
        """
        # 统计股票被提及的情况
        stock_stats = self._aggregate_stock_stats(analysis_results)
        
        # 生成推荐
        recommendations = []
        for code, stats in stock_stats.items():
            rec = self._evaluate_stock(code, stats)
            if rec:
                recommendations.append(rec)
        
        # 按推荐分数排序
        recommendations.sort(
            key=lambda x: x.recommendation_score, 
            reverse=True
        )
        
        return recommendations
    
    def _aggregate_stock_stats(
        self, 
        results: List[AnalysisResult]
    ) -> Dict[str, dict]:
        """聚合股票统计信息"""
        stats = defaultdict(lambda: {
            "name": "",
            "market": "",
            "mention_count": 0,
            "sentiment_scores": [],
            "industries": set(),
            "news_summaries": [],
        })
        
        for result in results:
            for stock in result.related_stocks:
                code = stock["code"]
                stats[code]["name"] = stock.get("name", f"股票{code}")
                stats[code]["market"] = stock.get("market", "")
                stats[code]["mention_count"] += 1
                stats[code]["sentiment_scores"].append(
                    result.sentiment_score
                )
                stats[code]["industries"].update(result.related_industries)
                stats[code]["news_summaries"].append(result.summary)
                
        return dict(stats)
    
    def _evaluate_stock(
        self, 
        code: str, 
        stats: dict
    ) -> Optional[StockRecommendation]:
        """
        评估单只股票
        
        Args:
            code: 股票代码
            stats: 统计信息
            
        Returns:
            股票推荐结果，不符合条件返回None
        """
        # 最小提及次数过滤
        if stats["mention_count"] < self.config.MIN_MENTION_COUNT:
            return None
        
        # 计算平均情感分数
        avg_sentiment = sum(stats["sentiment_scores"]) / len(
            stats["sentiment_scores"]
        )
        
        # 情感分数阈值过滤
        if avg_sentiment < self.config.SENTIMENT_THRESHOLD:
            return None
        
        # 计算推荐分数
        score = self._calculate_score(
            stats["mention_count"],
            avg_sentiment,
            list(stats["industries"])
        )
        
        # 确定推荐等级
        level = self._get_recommendation_level(score)
        
        return StockRecommendation(
            code=code,
            name=stats["name"],
            market=stats["market"],
            mention_count=stats["mention_count"],
            avg_sentiment=avg_sentiment,
            related_industries=list(stats["industries"]),
            key_news=stats["news_summaries"][:3],  # 最多3条相关新闻
            recommendation_score=score,
            recommendation_level=level,
        )
    
    def _calculate_score(
        self,
        mention_count: int,
        avg_sentiment: float,
        industries: List[str]
    ) -> float:
        """
        计算推荐分数
        
        分数范围：0-100
        """
        score = 0.0
        
        # 提及次数贡献（最高30分）
        mention_score = min(mention_count * 10, 30)
        score += mention_score
        
        # 情感分数贡献（最高40分）
        sentiment_score = avg_sentiment * 40
        score += sentiment_score
        
        # 行业加成（最高30分）
        focus_match = sum(
            1 for ind in industries 
            if any(f in ind for f in self.config.FOCUS_INDUSTRIES)
        )
        industry_score = min(focus_match * 10, 30)
        score += industry_score
        
        return round(score, 2)
    
    def _get_recommendation_level(self, score: float) -> str:
        """根据分数确定推荐等级"""
        if score >= 70:
            return "strong"
        elif score >= 50:
            return "moderate"
        else:
            return "watch"
    
    def filter_by_industry(
        self,
        recommendations: List[StockRecommendation],
        industry: str
    ) -> List[StockRecommendation]:
        """按行业筛选推荐结果"""
        return [
            r for r in recommendations
            if any(industry in ind for ind in r.related_industries)
        ]
    
    def get_top_picks(
        self,
        recommendations: List[StockRecommendation],
        n: int = 5
    ) -> List[StockRecommendation]:
        """获取前N个推荐"""
        return recommendations[:n]


# 模块级便捷实例
stock_screener = StockScreener()
