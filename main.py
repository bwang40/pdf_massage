# main.py
from pdf_processing.mineru_converter import convert_pdf_to_markdown
from pdf_processing.file_extractor import extract_auto_contents
from markdown_processing.cleaner import clean_md
from markdown_processing.translator import translate_md
from config import EXTRACTED_DIR, CLEANED_DIR, TRANSLATED_DIR, DEBUG
from llama_index.core import Settings
from llama_index.llms.deepseek import DeepSeek
from llama_index.embeddings.openai_like import OpenAILikeEmbedding
from pathlib import Path

def main():

    Settings.llm = DeepSeek(model="deepseek-chat", api_key="sk-eac019be79f14f948591d963d8c17656")
    Settings.embed_model = OpenAILikeEmbedding(
        model_name="text-embedding-v4",
        api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
        api_key="sk-e9aeb7dc9a3e4bf784411b295ddfa402",
        embed_batch_size=10,
)
    # Step 1: PDF 转换为 Markdown
    convert_pdf_to_markdown()

    # Step 2: 提取 Markdown 和图像文件
    extract_auto_contents(EXTRACTED_DIR, EXTRACTED_DIR)

    # Step 3: 清洗 Markdown 文件
    for file_path in Path(EXTRACTED_DIR).rglob("*.md"):
        clean_md(str(file_path), str(CLEANED_DIR), debug=DEBUG)

    # Step 4: 翻译 Markdown 文件
    for file_path in Path(CLEANED_DIR).rglob("*.md"):
        translate_md(str(file_path), str(TRANSLATED_DIR), debug=DEBUG)

    print("📦 处理完成")

if __name__ == "__main__":
    main()
