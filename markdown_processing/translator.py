# markdown_processing/translator.py
from llama_index.core.prompts import PromptTemplate
from utility import split_markdown_by_heading, run_cleaning, write_debug_chunks
from pathlib import Path
from config import max_chars_per_chunk


# 翻译 Prompt 模板
translation_prompt = PromptTemplate("""
你是一个专业的 Markdown 文档翻译机器人，负责将英文 Markdown 文档翻译为自然、准确的中文。你收到的 Markdown 文档可能是经过切分的片段，结构可能不完整，存在缺少一级标题、从中间段落开始或标题层级不规范等情况。请严格保留原文 Markdown 格式，不得更改标题层级或破坏任何结构性语法。

请遵循以下翻译规则：

1. **严格保留所有 Markdown 结构和语法**，包括但不限于标题（如 `#` `##` `###` `####` 等）、列表（有序/无序）、链接、图片、代码块、表格、引用、分隔线等，不得增删或调整层级；
2. **所有标题符号必须严格保留，标题等级不可更改**；
3. **所有代码块（```）和行内代码（`code`）必须完整保留，禁止翻译或更动任何字符**；
4. **图片和链接中的 URL、文件名、路径等保持原样，不得翻译或修改**；
5. 正文内容应翻译为专业、通顺、自然的中文；
6. **仅输出翻译后的中文 Markdown 内容**；
7. 即使输入被切分为不完整段落，也**不得破坏原有 Markdown 的结构**；

请翻译以下 Markdown 文本：

{context_str}
""")

def translate_md(input_path: str, output_path: str, llm=None, debug=False):
    text = Path(input_path).read_text(encoding="utf-8")
    chunks = split_markdown_by_heading(text, max_chars_per_chunk=max_chars_per_chunk)
    results = run_cleaning(chunks, translation_prompt, llm)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n\n".join(results), encoding="utf-8")

    if debug:
        write_debug_chunks(chunks, results, input_path)
