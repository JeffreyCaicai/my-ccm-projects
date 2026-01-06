---
description: 处理input文件夹中的所有待处理文件
---

# 处理输入 /process-input

此工作流用于一键处理 `input` 文件夹中的所有待处理文件。

## 使用方法

```
/process-input
```

## 执行步骤

1. 查看待处理文件
```bash
// turbo
ls -la /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/input/
```

2. 运行完整处理流程
```bash
cd /Users/mac/Desktop/my-ccm-projects/ai-analysis-system && python -c "
from skills import analyze_all_pending, screen_stocks

# 分析所有待处理文件
print('=== 分析新闻 ===')
result = analyze_all_pending()
print(result)

# 筛选股票
print('\\n=== 筛选股票 ===')
stocks = screen_stocks()
print(stocks)
"
```

3. 查看生成的报告
```bash
// turbo
ls -la /Users/mac/Desktop/my-ccm-projects/ai-analysis-system/processing/
```

## 输出

- 生成每日新闻分析报告
- 生成股票筛选报告
- 所有报告保存在 `processing/` 文件夹
