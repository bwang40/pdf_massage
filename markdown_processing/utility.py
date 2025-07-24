import re
import logging
from pathlib import Path
from typing import List, Tuple
from tqdm import tqdm
from config import DEBUG_CLEAN_DIR

# ========== 工具函数 ==========
def extract_code_blocks(text: str) -> Tuple[str, List[str]]:
    code_blocks = []
    def replacer(match):
        code_blocks.append(match.group(0))
        return f"__CODE_BLOCK_{len(code_blocks) - 1}__"
    safe_text = re.sub(r"```.*?\n.*?```", replacer, text, flags=re.DOTALL)
    return safe_text, code_blocks

def restore_code_blocks(text: str, code_blocks: List[str]) -> str:
    for i, block in enumerate(code_blocks):
        text = text.replace(f"__CODE_BLOCK_{i}__", block)
    return text

def split_markdown_by_heading(text: str, max_chars_per_chunk: int = 3000) -> List[str]:
    safe_text, code_blocks = extract_code_blocks(text)
    headings = list(re.finditer(r'^(#{1,6}\s+.*)', safe_text, re.MULTILINE))
    
    sections = []
    for i, match in enumerate(headings):
        start = match.start()
        end = headings[i + 1].start() if i + 1 < len(headings) else len(safe_text)
        sections.append(safe_text[start:end].strip())

    chunks, current_chunk = [], ""
    for section in sections:
        if len(current_chunk) + len(section) < max_chars_per_chunk:
            current_chunk += section + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = section + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())

    return [restore_code_blocks(chunk, code_blocks) for chunk in chunks]

def run_cleaning(chunks: List[str], prompt_template, llm) -> List[str]:
    results = []
    for i, chunk in enumerate(tqdm(chunks, desc="🧹 Cleaning Chunks", leave=False)):
        try:
            prompt = prompt_template.format(context_str=chunk)
            response = llm.complete(prompt)
            results.append(response.text.strip())
        except Exception as e:
            logging.error(f"[Chunk {i+1}] 清洗失败: {e}")
            results.append(f"<!-- 清洗失败：{e} -->")
    return results

def write_debug_chunks(original_chunks, processed_chunks, rel_path: str, output_dir: str = DEBUG_CLEAN_DIR):
    """
    将原始和处理后的 Markdown 文本块写入指定目录。
    
    :param original_chunks: 原始的 Markdown 文本块列表
    :param processed_chunks: 处理后的 Markdown 文本块列表
    :param rel_path: 相对路径，用于生成输出文件的路径
    :param output_dir: 输出文件夹路径，默认为 DEBUG_CLEAN_DIR
    """
    sep = "\n" + "=" * 100 + "\n"
    rel_md_path = Path(rel_path).with_suffix(".md")

    # 确保输出目录存在
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    # 原始切片路径
    input_path = output_dir_path / ("input_" + rel_md_path)
    input_path.write_text(sep.join(original_chunks), encoding="utf-8")

    # 处理后切片路径
    output_path = output_dir_path / ("processed_" + rel_md_path)
    output_path.write_text(sep.join(processed_chunks), encoding="utf-8")
