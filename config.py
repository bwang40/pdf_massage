# config.py
import os

# PDF 文件路径
PDF_PATH = r"D:\workspace\pdf_convert_clean_trans\input\ISO 26262-1-2018.pdf"

# 处理目录
TMP_DIR = os.path.join(os.getcwd(), ".tmp")
ORIGIN_DIR = os.path.join(TMP_DIR, "origin")
EXTRACTED_DIR = os.path.join(TMP_DIR, "extracted_origin")
CLEANED_DIR = os.path.join(TMP_DIR, "cleaned")
TRANSLATED_DIR = os.path.join(TMP_DIR, "translated")
DEBUG_CLEAN_DIR = os.path.join(TMP_DIR, "debug_clean_chunk")
DEBUG_TRANS_DIR = os.path.join(TMP_DIR, "debug_trans_chunk")

# LLM 配置
LLM_API_KEY = "sk-eac019be79f14f948591d963d8c17656"
max_chars_per_chunk = 6000  # 每个 Markdown 块的最大字符数