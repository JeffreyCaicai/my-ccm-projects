---
description: 筛选有投资价值的股票
---

# 筛选股票 /screen-stocks

此工作流用于基于新闻分析结果筛选有投资价值的股票。

## 使用方法

```
/screen-stocks [日期] [行业]
```

### 参数
- `日期`：可选，格式为 YYYY-MM-DD，默认为今天
- `行业`：可选，指定行业过滤（如：新能源、半导体）

### 示例
```
/screen-stocks 2026-01-05
/screen-stocks 2026-01-05 新能源
/screen-stocks  # 筛选今日推荐
```

## 执行步骤

1. 确保有足够的分析数据
```bash
// turbo
ls /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/input/
```

2. 运行股票筛选脚本
```bash
cd /Users/mac/Desktop/my-ccm-projects/ai-analysis-system && python -c "from skills import screen_stocks; result = screen_stocks(); print(result)"
```

3. 查看筛选结果
```bash
// turbo
cat /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/*股票筛选.md 2>/dev/null
```

## 筛选条件

默认筛选条件：
- 最小提及次数：2次
- 情感分数阈值：0.6（偏积极）
- 重点关注行业：新能源、半导体、人工智能、医疗健康、消费、金融

## 输出

- 在 `processing/` 文件夹生成 `YYYY-MM-DD-股票筛选.md` 文件
- 包含推荐股票列表和详细分析
