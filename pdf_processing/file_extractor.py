# pdf_processing/file_extractor.py
import os
import shutil
from pathlib import Path
from config import EXTRACTED_DIR

def sanitize_name(name: str) -> str:
    """统一替换名称中的空格为下划线"""
    return name.replace(" ", "_")

def extract_auto_contents(input_dir: str, output_dir: str):
    # 确保输入目录路径正确
    input_path = Path(input_dir)

    # 获取所有子目录并打印调试信息
    sub_dirs = list(input_path.iterdir())
    
    for sub_dir in sub_dirs:
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
        md_files = list(auto_path.glob("*.md"))
        
        for md_file in md_files:
            if md_file.is_file():
                sanitized_filename = sanitize_name(md_file.name)
                dest_path = os.path.join(target_subdir, sanitized_filename)
                shutil.copy2(md_file, dest_path)

        # 拷贝 auto/images 目录下的所有文件
        image_dir = auto_path / "images"
        if image_dir.exists() and image_dir.is_dir():
            target_image_dir = os.path.join(target_subdir, "images")
            os.makedirs(target_image_dir, exist_ok=True)

            img_files = list(image_dir.rglob("*.*"))
            for img_file in img_files:
                if img_file.is_file():
                    sanitized_img_name = sanitize_name(img_file.name)
                    dest_path = os.path.join(target_image_dir, sanitized_img_name)
                    shutil.copy2(img_file, dest_path)

