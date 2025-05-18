# makedownchange

## 简介 | Introduction

**makedownchange** 是一个用于 Dify 的 Markdown 文件批量转换插件，支持将 Markdown 文件自动转换为 PDF，并可自定义样式。支持实时目录监控、批量处理、以及多种输出风格，适合文档自动归档、批量格式转换等场景。

**makedownchange** is a Dify plugin for batch converting Markdown files to PDF with customizable styles. It supports real-time directory monitoring, batch processing, and multiple output styles, making it ideal for document archiving and format conversion.

---

## 功能特性 | Features

- 批量将 Markdown 文件转换为 PDF | Batch convert Markdown files to PDF
- 支持自定义 PDF 样式（默认、现代、经典）| Customizable PDF styles (default, modern, classic)
- 支持自动监控目录，实时转换 | Real-time directory monitoring and conversion
- 支持直接传入 Markdown 内容 | Direct conversion from Markdown content
- 支持多语言内容，兼容中文 | Multilingual support, including Chinese

---

## 安装方法 | Installation

1. 在 Dify 插件管理后台上传本插件，或通过 Dify 插件市场安装。
2. 本地开发调试可在插件目录下执行：
   ```bash
   pip install -r requirements.txt
   ```

---

## 使用说明 | Usage

### 方式一：批量转换目录下所有 Markdown 文件 | Batch convert all Markdown files in a directory
- 不传 `markdown_content` 参数时，插件会自动查找当前目录下所有 `.md` 或 `.markdown` 文件并批量转换为 PDF。
- If `markdown_content` is not provided, the plugin will batch convert all `.md` or `.markdown` files in the current directory to PDF.

### 方式二：直接传入 Markdown 内容 | Convert from Markdown content
- 传入 `markdown_content` 字符串参数，插件会将其转换为 PDF 并返回结果。
- Provide the `markdown_content` string parameter to convert it directly to PDF.

### 方式三：自动监控目录 | Auto-monitor directory
- 设置 `auto_monitor` 为 `true`，并指定 `monitor_dir`，插件会自动监控该目录下的 Markdown 文件变动，自动转换为 PDF。
- Set `auto_monitor` to `true` and specify `monitor_dir` to enable real-time monitoring and conversion.

---

## 参数说明 | Parameters

| 参数名 Name        | 类型 Type | 必填 Required | 说明 Description |
|-------------------|-----------|--------------|-----------------|
| markdown_content  | string    | 否 No        | 需要转换的 Markdown 内容（不传则批量处理目录下所有文件）<br>Markdown content to convert (if not provided, batch process all files in directory) |
| style             | string    | 否 No        | PDF 样式，可选：default, modern, classic，默认 default<br>PDF style: default, modern, classic (default: default) |
| output_filename   | string    | 否 No        | 输出 PDF 文件名（仅在传入 markdown_content 时生效）<br>Output PDF filename (only used when markdown_content is provided) |
| auto_monitor      | boolean   | 否 No        | 是否自动监控目录，默认 false<br>Enable auto-monitoring (default: false) |
| monitor_dir       | string    | 否 No        | 监控的目录，auto_monitor 为 true 时生效，默认当前目录<br>Directory to monitor (used when auto_monitor is true, default: .) |
| output_dir        | string    | 否 No        | 输出 PDF 文件保存目录，auto_monitor 为 true 时生效<br>Output directory for PDFs (used when auto_monitor is true) |

---

## 输出结果 | Output

- 单文件转换时，返回 PDF 文件路径。
- For single file conversion, returns the PDF file path.
- 批量转换时，返回所有处理文件的状态和路径。
- For batch conversion, returns the status and path of all processed files.

---

## 常见问题 | FAQ

1. **PDF 中文乱码？| Garbled Chinese in PDF?**  
   插件已内置 Noto Sans SC 字体支持中文，若仍有问题请检查本地字体或网络字体加载。  
   The plugin uses Noto Sans SC for Chinese support. If issues persist, check local or network font loading.

2. **目录监控无效？| Directory monitoring not working?**  
   请确保 `watchdog` 依赖已正确安装，且有权限访问监控目录。  
   Ensure `watchdog` is installed and you have permission to access the monitored directory.

3. **转换失败？| Conversion failed?**  
   请检查 Markdown 文件内容格式，或查看 Dify 日志获取详细错误信息。  
   Check the Markdown file format or Dify logs for detailed error messages.

---

## 联系作者 | Contact

如有问题或建议，请联系作者 morgan。  
For questions or suggestions, contact the author: morgan.
