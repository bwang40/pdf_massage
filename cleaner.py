# markdown_processing/cleaner.py
from llama_index.core import Settings
from llama_index.core.prompts import PromptTemplate
from utility import split_markdown_by_heading, run_llm_process, write_debug_chunks
from pathlib import Path
from config import max_chars_per_chunk, DEBUG_CLEAN_DIR

# Prompt 模板
clean_prompt = PromptTemplate(r"""
你是一个专业的 Markdown 格式修复专家。你将接收由 OCR 或 PDF 转换工具（如 Mineru）生成的 Markdown 文件，该文件格式存在严重错误，请你对其进行以下修复，保持语义和结构不变，仅修复格式问题。

请严格遵守以下规则：

1. **修复标题格式：**
   - 所有形如 `# N` 的标题为一级标题（例如 `# 1`、`# 2`）；
   - 所有形如 `N.N` 的应为二级标题 `## N.N`；
   - 所有形如 `N.N.N` 的为三级标题 `### N.N.N`；
   - 如果标题前存在错误的 `#` 个数（如 `### 3.3` 应是 `## 3.3`），请纠正。

2. **修复列表格式：**
   - 所有以 `—` 或 `–`、长破折号或错误符号开头的条目，应统一为 `-`（标准 Markdown 无序列表）；
   - 若嵌套列表存在缩进错误，按照 2 个空格作为每一级缩进进行规范；
   - 若多级列表中存在自然语言段落描述，请确保子项缩进正确，并在每项后加换行。

3. **修复 NOTE 标注：**
   - 将类似“Note 1 to entry: …” 转换为以下标准格式：
     > [!NOTE]
     > Note 1 to entry: ...
   - 同一段中多个 Note，依次编号，保持缩进一致。

4. **修复数学公式污染：**
   - 若出现 LaTeX 数学语法未正确渲染，例如：
     $" \mathrm { m } { \cdot } \mathrm { n } ^ { \prime \prime }$ 
     应尽量转换为正常文本（如 `m·n″`），或保留为行内公式 `\( m \cdot n^{\prime\prime} \)`。

5. **修复乱码和不必要符号：**
   - 删除无效转义符（如 `\`、`\``, `\`, `,` 等成对混乱出现的标点）；
   - 修复 markdown 中图像语法错误（如 `![]()`）中路径丢失或注释混乱的问题；
   - 删除重复空格和空行，确保段落之间最多保留一个空行。

6. **保持内容原始语义不变**，仅做格式清洗。

输出格式为**修复后的完整 Markdown 文件**。不要进行额外解释或注释。更不要在清理后的文件前添加```markdown，以及最后添加```；

请清洗以下 Markdown 文本：

{context_str}
""")

def clean_md(input_path: str, output_path: str, llm=None, debug=False):
    text = Path(input_path).read_text(encoding="utf-8")
    chunks = split_markdown_by_heading(text, max_chars_per_chunk=max_chars_per_chunk)
    results = run_llm_process(chunks, clean_prompt, llm)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text("\n\n".join(results), encoding="utf-8")

    if debug:
        write_debug_chunks(chunks, results, input_path, DEBUG_CLEAN_DIR)
