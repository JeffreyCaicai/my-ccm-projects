"""
AI信息分析系统 - 内容解析模块

本模块负责解析Markdown文件内容，提取结构化信息。
"""

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class ParsedContent:
    """解析后的内容结构"""
    
    title: str
    date: Optional[str]
    source: Optional[str]
    category: Optional[str]
    content: str
    metadata: Dict[str, str]
    stocks_mentioned: List[str]
    industries_mentioned: List[str]


class ContentParser:
    """内容解析器"""
    
    # 股票代码正则表达式（A股）
    STOCK_CODE_PATTERN = re.compile(
        r'(?:[\(\（])?'
        r'(?:SH|SZ|BJ|sh|sz|bj)?'
        r'[\.:]?'
        r'([036]\d{5})'
        r'(?:[\)\）])?'
    )
    
    # 常见行业关键词
    INDUSTRY_KEYWORDS = [
        "新能源", "光伏", "锂电", "储能",
        "半导体", "芯片", "集成电路",
        "人工智能", "AI", "大模型", "机器人",
        "医药", "医疗", "生物", "创新药",
        "消费", "白酒", "食品", "零售",
        "金融", "银行", "保险", "券商",
        "地产", "房地产", "建材",
        "军工", "国防", "航空航天",
        "汽车", "新能源车", "电动车",
        "通信", "5G", "物联网",
    ]
    
    def parse_file(self, file_path: Path) -> ParsedContent:
        """
        解析Markdown文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            解析后的内容结构
        """
        content = file_path.read_text(encoding="utf-8")
        return self.parse_content(content, file_path.name)
    
    def parse_content(
        self, 
        content: str, 
        filename: str = ""
    ) -> ParsedContent:
        """
        解析Markdown内容
        
        Args:
            content: Markdown文本内容
            filename: 文件名（用于提取日期）
            
        Returns:
            解析后的内容结构
        """
        # 解析YAML前置元数据
        metadata = self._parse_frontmatter(content)
        
        # 移除YAML头部后的正文
        body = self._remove_frontmatter(content)
        
        # 提取标题
        title = self._extract_title(body) or filename
        
        # 提取日期
        date = metadata.get("date") or self._extract_date_from_filename(
            filename
        )
        
        # 提取来源和分类
        source = metadata.get("source", "")
        category = metadata.get("category", "")
        
        # 提取股票代码
        stocks = self._extract_stock_codes(body)
        
        # 提取行业关键词
        industries = self._extract_industries(body)
        
        return ParsedContent(
            title=title,
            date=date,
            source=source,
            category=category,
            content=body,
            metadata=metadata,
            stocks_mentioned=stocks,
            industries_mentioned=industries,
        )
    
    def _parse_frontmatter(self, content: str) -> Dict[str, str]:
        """解析YAML前置元数据"""
        metadata = {}
        
        # 匹配 --- ... --- 格式的YAML头
        match = re.match(
            r'^---\s*\n(.*?)\n---\s*\n',
            content,
            re.DOTALL
        )
        
        if match:
            yaml_content = match.group(1)
            # 简单解析YAML（键: 值）
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
                    
        return metadata
    
    def _remove_frontmatter(self, content: str) -> str:
        """移除YAML前置元数据"""
        return re.sub(
            r'^---\s*\n.*?\n---\s*\n',
            '',
            content,
            flags=re.DOTALL
        )
    
    def _extract_title(self, content: str) -> Optional[str]:
        """从内容中提取标题（第一个H1）"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else None
    
    def _extract_date_from_filename(
        self, 
        filename: str
    ) -> Optional[str]:
        """从文件名中提取日期"""
        match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        return match.group(1) if match else None
    
    def _extract_stock_codes(self, content: str) -> List[str]:
        """提取股票代码"""
        matches = self.STOCK_CODE_PATTERN.findall(content)
        # 去重并保持顺序
        seen = set()
        unique_codes = []
        for code in matches:
            if code not in seen:
                seen.add(code)
                unique_codes.append(code)
        return unique_codes
    
    def _extract_industries(self, content: str) -> List[str]:
        """提取提及的行业"""
        mentioned = []
        for keyword in self.INDUSTRY_KEYWORDS:
            if keyword in content:
                mentioned.append(keyword)
        return mentioned


# 模块级便捷实例
content_parser = ContentParser()
