# pipeline.py
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable, Optional
import logging
import shutil

from pdf_processing.mineru_converter import convert_pdf_to_markdown
from pdf_processing.file_extractor import extract_auto_contents
from markdown_processing.cleaner import clean_md
from markdown_processing.translator import translate_md
from config import (
    EXTRACTED_DIR,
    CLEANED_DIR,
    TRANSLATED_DIR,
    ORIGIN_DIR,
    DEBUG,
)

from api_key import LLM_API_KEY  # Ensure this is imported correctly
from llama_index.core import Settings
from llama_index.llms.deepseek import DeepSeek

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

def copy_non_markdown_files(input_dir: Path, output_dir: Path) -> None:
    """递归地复制非Markdown文件和文件夹"""
    for item in input_dir.iterdir():
        dst = output_dir / item.name
        if item.is_dir():
            print(f"复制文件夹: {item}")
            dst.mkdir(parents=True, exist_ok=True)  # 创建目标文件夹
            copy_non_markdown_files(item, dst)  # 递归处理子文件夹
        elif item.suffix.lower() != ".md":
            print(f"复制文件: {item}")
            shutil.copy2(item, dst)  # 复制非Markdown文件

def process_files(
    input_dir: Path,
    output_dir: Path,
    process_func: Callable[[str, str, Optional[DeepSeek], bool], None],
    llm: Optional[DeepSeek] = None,
    debug: bool = False,
    parallel: bool = False
) -> None:
    """处理目录中的所有Markdown文件并复制非Markdown文件夹"""
    # 复制所有非Markdown文件夹
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制所有非 Markdown 文件和文件夹
    copy_non_markdown_files(input_dir, output_dir)
    
    # 处理Markdown文件
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

def run_pipeline(pdf_path: str) -> None:
    try:
        # 初始化LLM
        Settings.llm = DeepSeek(model="deepseek-chat", api_key=LLM_API_KEY)

        logger.info("🚀 开始PDF处理流程")

        # Step 1: PDF 转换为 Markdown
        logger.info("📄 转换PDF为Markdown")
        convert_pdf_to_markdown(pdf_path=pdf_path, output_dir=ORIGIN_DIR)

        # Step 2: 提取Markdown和图像文件
        logger.info("🔍 提取Markdown内容")
        extract_auto_contents(ORIGIN_DIR, EXTRACTED_DIR)

        # Step 3: 清洗Markdown文件
        logger.info("🧹 清洗Markdown文件")
        process_files(
            Path(EXTRACTED_DIR),
            Path(CLEANED_DIR),
            clean_md,
            llm=Settings.llm,
            debug=DEBUG,
        )

        # Step 4: 翻译Markdown文件
        logger.info("🌍 翻译Markdown文件")
        process_files(
            Path(CLEANED_DIR),
            Path(TRANSLATED_DIR),
            translate_md,
            llm=Settings.llm,
            debug=DEBUG,
        )

        logger.info("✅ 处理完成")
    except Exception as e:
        logger.error(f"处理失败: {e}")
        raise


if __name__ == "__main__":
    from config import PDF_PATH

    run_pipeline(PDF_PATH)
