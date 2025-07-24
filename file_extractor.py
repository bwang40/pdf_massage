# pdf_processing/file_extractor.py
import os
import shutil
from pathlib import Path
from config import EXTRACTED_DIR

def sanitize_name(name: str) -> str:
    """统一替换名称中的空格为下划线"""
    return name.replace(" ", "_")

def extract_auto_contents(input_dir: str, output_dir: str):
    input_path = Path(input_dir)

    for sub_dir in input_path.iterdir():
        if not sub_dir.is_dir():
            continue

        auto_path = sub_dir / "auto"
        if not auto_path.exists():
            continue

        # 替换子文件夹名中的空格
        sanitized_subdir_name = sanitize_name(sub_dir.name)
        target_subdir = os.path.join(output_dir, sanitized_subdir_name)
        os.makedirs(target_subdir, exist_ok=True)

        # 拷贝 auto 下的 Markdown 文件（*.md）
        for md_file in auto_path.glob("*.md"):
            if md_file.is_file():
                sanitized_filename = sanitize_name(md_file.name)
                shutil.copy2(md_file, os.path.join(target_subdir, sanitized_filename))

        # 拷贝 auto/images 目录下的所有文件
        image_dir = auto_path / "images"
        if image_dir.exists() and image_dir.is_dir():
            target_image_dir = os.path.join(target_subdir, "images")
            os.makedirs(target_image_dir, exist_ok=True)

            for img_file in image_dir.rglob("*.*"):
                if img_file.is_file():
                    sanitized_img_name = sanitize_name(img_file.name)
                    shutil.copy2(img_file, os.path.join(target_image_dir, sanitized_img_name))

