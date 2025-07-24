# main.py
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Optional
import logging

from mineru_converter import convert_pdf_to_markdown
from file_extractor import extract_auto_contents
from cleaner import clean_md
from translator import translate_md
from config import (
    EXTRACTED_DIR, CLEANED_DIR, TRANSLATED_DIR, ORIGIN_DIR,
    DEBUG, PDF_PATH, LLM_API_KEY
)
from llama_index.core import Settings
from llama_index.llms.deepseek import DeepSeek

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def process_files(
    input_dir: Path,
    output_dir: Path,
    process_func: Callable[[str, str, Optional[DeepSeek], bool], None],
    llm: Optional[DeepSeek] = None,
    debug: bool = False,
    parallel: bool = False
) -> None:
    """处理目录中的所有Markdown文件"""
    files = list(input_dir.rglob("*.md"))
    if not files:
        logger.warning(f"在目录 {input_dir} 中未找到Markdown文件")
        return

    def process_file(file_path: Path) -> None:
        try:
            output_path = output_dir / file_path.relative_to(input_dir)
            process_func(str(file_path), str(output_path), llm, debug)
            logger.info(f"成功处理: {file_path}")
        except Exception as e:
            logger.error(f"处理文件 {file_path} 失败: {e}")

    if parallel:
        with ThreadPoolExecutor() as executor:
            executor.map(process_file, files)
    else:
        for file_path in files:
            process_file(file_path)

def main() -> None:
    try:
        # 初始化LLM
        Settings.llm = DeepSeek(model="deepseek-chat", api_key=LLM_API_KEY)

        logger.info("🚀 开始PDF处理流程")

        # Step 1: PDF 转换为 Markdown
        logger.info("📄 转换PDF为Markdown")
        convert_pdf_to_markdown(pdf_path=PDF_PATH, output_dir=ORIGIN_DIR)

        # Step 2: 提取Markdown和图像文件
        logger.info("🔍 提取Markdown内容")
        extract_auto_contents(ORIGIN_DIR, EXTRACTED_DIR)

        # Step 3: 清洗Markdown文件
        logger.info("🧹 清洗Markdown文件")
        process_files(
            Path(EXTRACTED_DIR),
            Path(CLEANED_DIR),
            clean_md,
            debug=DEBUG
        )

        # Step 4: 翻译Markdown文件
        logger.info("🌍 翻译Markdown文件")
        process_files(
            Path(CLEANED_DIR),
            Path(TRANSLATED_DIR),
            translate_md,
            debug=DEBUG
        )

        logger.info("✅ 处理完成")
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise

if __name__ == "__main__":
    main()
