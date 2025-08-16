# pdf_processing/mineru_converter.py
import subprocess
import shutil
import os

def convert_pdf_to_markdown(pdf_path=None, output_dir=None):
    # 获取文件名并替换字符
    filename = os.path.basename(pdf_path)
    new_filename = filename.replace("-", "_").replace(" ", "_")
    new_pdf_path = os.path.join(output_dir, new_filename)

    # 创建 .tmp 文件夹
    tmp_dir = os.path.dirname(new_pdf_path)
    os.makedirs(tmp_dir, exist_ok=True)

    # 将原始 PDF 文件复制到 .tmp 文件夹
    shutil.copy(pdf_path, new_pdf_path)

    # 构造输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 调用 mineru 命令行工具进行 PDF 转换
    result = subprocess.run(
        ["mineru", "-p", new_pdf_path, "-o", output_dir],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print("PDF 转换成功")
        print("输出：", result.stdout)
    else:
        print("PDF 转换失败")
        print("错误：", result.stderr)
