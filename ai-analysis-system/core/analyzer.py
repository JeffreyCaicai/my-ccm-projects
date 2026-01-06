"""
AI信息分析系统 - 信息分析模块

本模块负责对财经内容进行分析，包括：
- 新闻分类
- 情感分析
- 关键信息提取
"""

import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

from .content_parser import ParsedContent


@dataclass
class AnalysisResult:
    """分析结果"""
    
    summary: str
    sentiment: str  # positive, negative, neutral
    sentiment_score: float  # 0.0 - 1.0
    key_points: List[str]
    related_stocks: List[Dict[str, str]]
    related_industries: List[str]
    category: str
    importance: str  # high, medium, low


class NewsAnalyzer:
    """新闻分析器"""
    
    # 情感关键词
    POSITIVE_KEYWORDS = [
        "利好", "上涨", "增长", "突破", "创新高",
        "超预期", "加速", "扩张", "支持", "鼓励",
        "减税", "降息", "降准", "补贴", "激励",
        "盈利", "业绩", "翻倍", "新高", "龙头",
    ]
    
    NEGATIVE_KEYWORDS = [
        "利空", "下跌", "下降", "暴跌", "创新低",
        "不及预期", "放缓", "收缩", "限制", "禁止",
        "加税", "加息", "处罚", "亏损", "退市",
        "风险", "违规", "调查", "暴雷", "爆仓",
    ]
    
    # 新闻类别关键词
    CATEGORY_KEYWORDS = {
        "宏观政策": ["央行", "政策", "国务院", "发改委", "监管", "法规"],
        "行业动态": ["行业", "产业", "市场", "趋势", "发展"],
        "公司公告": ["公告", "业绩", "财报", "分红", "增发", "回购"],
        "市场数据": ["数据", "指数", "成交量", "涨跌", "换手率"],
        "专家观点": ["分析师", "研报", "预测", "观点", "评级"],
        "国际财经": ["美股", "港股", "外资", "汇率", "国际"],
    }
    
    def analyze(self, parsed_content: ParsedContent) -> AnalysisResult:
        """
        分析解析后的内容
        
        Args:
            parsed_content: 解析后的内容
            
        Returns:
            分析结果
        """
        content = parsed_content.content
        
        # 情感分析
        sentiment, score = self._analyze_sentiment(content)
        
        # 分类
        category = self._classify_news(content)
        
        # 提取关键点
        key_points = self._extract_key_points(content)
        
        # 生成摘要
        summary = self._generate_summary(
            parsed_content.title,
            key_points
        )
        
        # 关联股票信息
        related_stocks = self._enrich_stock_info(
            parsed_content.stocks_mentioned
        )
        
        # 判断重要性
        importance = self._assess_importance(
            score, 
            len(parsed_content.stocks_mentioned),
            category
        )
        
        return AnalysisResult(
            summary=summary,
            sentiment=sentiment,
            sentiment_score=score,
            key_points=key_points,
            related_stocks=related_stocks,
            related_industries=parsed_content.industries_mentioned,
            category=category,
            importance=importance,
        )
    
    def _analyze_sentiment(
        self, 
        content: str
    ) -> Tuple[str, float]:
        """
        分析内容情感倾向
        
        Returns:
            (情感标签, 情感分数)
        """
        positive_count = sum(
            1 for kw in self.POSITIVE_KEYWORDS if kw in content
        )
        negative_count = sum(
            1 for kw in self.NEGATIVE_KEYWORDS if kw in content
        )
        
        total = positive_count + negative_count
        if total == 0:
            return "neutral", 0.5
        
        score = positive_count / total
        
        if score > 0.6:
            sentiment = "positive"
        elif score < 0.4:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        return sentiment, score
    
    def _classify_news(self, content: str) -> str:
        """对新闻进行分类"""
        max_score = 0
        best_category = "其他"
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in content)
            if score > max_score:
                max_score = score
                best_category = category
                
        return best_category
    
    def _extract_key_points(
        self, 
        content: str, 
        max_points: int = 5
    ) -> List[str]:
        """提取关键要点"""
        # 按句子分割
        sentences = re.split(r'[。！？\n]', content)
        
        # 过滤和评分
        scored_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10 or len(sentence) > 100:
                continue
                
            # 根据关键词打分
            score = 0
            for kw in self.POSITIVE_KEYWORDS + self.NEGATIVE_KEYWORDS:
                if kw in sentence:
                    score += 1
                    
            if score > 0:
                scored_sentences.append((sentence, score))
        
        # 排序并返回前N个
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_sentences[:max_points]]
    
    def _generate_summary(
        self, 
        title: str, 
        key_points: List[str]
    ) -> str:
        """生成摘要"""
        if not key_points:
            return title
            
        summary_points = key_points[:3]
        return f"{title}。" + "；".join(summary_points) + "。"
    
    def _enrich_stock_info(
        self, 
        stock_codes: List[str]
    ) -> List[Dict[str, str]]:
        """
        丰富股票信息
        
        注意：这里是模拟数据，实际应用中应调用股票API
        """
        stocks = []
        for code in stock_codes:
            market = self._get_market_by_code(code)
            stocks.append({
                "code": code,
                "market": market,
                "name": f"股票{code}",  # 实际应查询股票名称
            })
        return stocks
    
    def _get_market_by_code(self, code: str) -> str:
        """根据股票代码判断市场"""
        if code.startswith("6"):
            return "上海"
        elif code.startswith("0") or code.startswith("3"):
            return "深圳"
        else:
            return "北交所"
    
    def _assess_importance(
        self,
        sentiment_score: float,
        stock_count: int,
        category: str
    ) -> str:
        """评估新闻重要性"""
        score = 0
        
        # 情感极端性
        if sentiment_score > 0.8 or sentiment_score < 0.2:
            score += 2
        elif sentiment_score > 0.7 or sentiment_score < 0.3:
            score += 1
            
        # 涉及股票数量
        if stock_count >= 3:
            score += 2
        elif stock_count >= 1:
            score += 1
            
        # 类别加权
        if category in ["宏观政策", "公司公告"]:
            score += 1
            
        if score >= 4:
            return "high"
        elif score >= 2:
            return "medium"
        else:
            return "low"


# 模块级便捷实例
news_analyzer = NewsAnalyzer()
