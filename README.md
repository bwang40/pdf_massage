# pdf_massage

一个将 PDF 文档转换为 Markdown、清洗并翻译为中文的自动化流程。项目同时提供命令行脚本和简单的 Web API，方便对单个 PDF 进行处理。

## 功能概述

- 使用 [mineru](https://github.com/myshell-ai/mineru) 将 PDF 转为 Markdown 文件
- 提取转换结果中的 Markdown 与图片资源
- 调用 DeepSeek 大语言模型清洗 Markdown 结构、修复格式
- 将清洗后的 Markdown 逐段翻译为中文
- 基于 FastAPI 提供 `/process` 接口，可上传 PDF 触发整个流程

## 安装

1. 安装依赖：
   ```bash
   pip install -r requirement.txt
   ```
2. 安装 `mineru` 命令行工具，并确保其可在命令行中调用。
3. 在项目根目录创建 `api_key.py`，内容如下：
   ```python
   LLM_API_KEY = "你的 DeepSeek API Key"
   ```

## 使用方法

### 命令行

1. 将待处理的 PDF 路径写入 `config.py` 中的 `PDF_PATH`。
2. 运行：
   ```bash
   python main.py
   ```
   处理结果会保存在 `.tmp` 目录的 `origin/`、`extracted_origin/`、`cleaned/` 和 `translated/` 子目录下。

### Web 接口

1. 启动服务：
   ```bash
   uvicorn api:app --reload
   ```
2. 打开浏览器访问 `http://localhost:8000`，上传 PDF 后可看到处理状态。

## 目录结构

- `pdf_processing/`：PDF 转 Markdown 以及文件提取逻辑
- `markdown_processing/`：Markdown 清洗与翻译
- `pipeline.py`：串联整个处理流程的入口
- `static/`：Web 前端页面

## 许可证

本项目代码仅供学习与参考，使用时请自行确认依赖库和外部服务的许可条款。

