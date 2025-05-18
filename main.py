import os
import markdown
from weasyprint import HTML
import tempfile
import glob
import mimetypes
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import queue

class MarkdownHandler(FileSystemEventHandler):
    def __init__(self, style='default', output_dir='pdf_output'):
        self.style = style
        self.output_dir = output_dir
        self.conversion_queue = queue.Queue()
        self.processing = False
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def on_created(self, event):
        if not event.is_directory and is_markdown_file(event.src_path):
            self.conversion_queue.put(event.src_path)
            if not self.processing:
                self.process_queue()
    
    def on_modified(self, event):
        if not event.is_directory and is_markdown_file(event.src_path):
            self.conversion_queue.put(event.src_path)
            if not self.processing:
                self.process_queue()
    
    def process_queue(self):
        self.processing = True
        while not self.conversion_queue.empty():
            file_path = self.conversion_queue.get()
            try:
                self.convert_file(file_path)
            except Exception as e:
                print(f"Error converting {file_path}: {str(e)}")
        self.processing = False
    
    def convert_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_path = os.path.join(self.output_dir, f"{base_name}.pdf")
        
        result = convert_markdown_to_pdf(content, self.style, output_path)
        print(f"Converted {file_path} to {output_path}")

def start_auto_monitor(directory='.', style='default', output_dir='pdf_output'):
    """Start monitoring directory for Markdown files and convert them automatically."""
    event_handler = MarkdownHandler(style, output_dir)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def is_markdown_file(file_path):
    """Check if a file is a markdown file based on extension or content."""
    # Check file extension
    if file_path.lower().endswith(('.md', '.markdown')):
        return True
    
    # Check mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type == 'text/markdown'

def find_markdown_files(directory='.'):
    """Find all markdown files in the given directory."""
    markdown_files = []
    for file_path in glob.glob(os.path.join(directory, '**/*'), recursive=True):
        if os.path.isfile(file_path) and is_markdown_file(file_path):
            markdown_files.append(file_path)
    return markdown_files

def convert_markdown_to_pdf(markdown_content, style='default', output_filename='output'):
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])
    
    # Add CSS based on style
    css = get_style_css(style)
    html_with_style = f"""
    <html>
        <head>
            <meta charset="utf-8">
            <style>
                @font-face {{
                    font-family: 'Noto Sans SC';
                    src: url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC&display=swap');
                }}
                {css}
            </style>
        </head>
        <body>
            {html_content}
        </body>
    </html>
    """
    
    # Create temporary file for HTML
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False, mode='w', encoding='utf-8') as temp_html:
        temp_html.write(html_with_style)
        temp_html_path = temp_html.name
    
    try:
        # Convert HTML to PDF
        pdf_path = f"{output_filename}.pdf"
        HTML(filename=temp_html_path).write_pdf(pdf_path)
        return {"status": "success", "file_path": pdf_path}
    finally:
        # Clean up temporary file
        os.unlink(temp_html_path)

def get_style_css(style):
    styles = {
        'default': """
            body { font-family: 'Noto Sans SC', Arial, sans-serif; line-height: 1.6; margin: 2em; }
            h1 { color: #333; border-bottom: 1px solid #eee; padding-bottom: 0.3em; }
            h2 { color: #444; margin-top: 1.5em; }
            h3 { color: #555; }
            code { background: #f4f4f4; padding: 2px 4px; border-radius: 4px; font-family: monospace; }
            pre { background: #f4f4f4; padding: 1em; border-radius: 4px; overflow-x: auto; }
            blockquote { border-left: 4px solid #ddd; padding-left: 1em; color: #666; }
            img { max-width: 100%; height: auto; }
            table { border-collapse: collapse; width: 100%; margin: 1em 0; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f4f4f4; }
        """,
        'modern': """
            body { font-family: 'Noto Sans SC', 'Helvetica Neue', sans-serif; line-height: 1.8; margin: 2em; color: #2c3e50; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 0.3em; }
            h2 { color: #34495e; margin-top: 1.5em; }
            h3 { color: #2980b9; }
            code { background: #f8f9fa; padding: 3px 6px; border-radius: 6px; font-family: 'Fira Code', monospace; }
            pre { background: #f8f9fa; padding: 1em; border-radius: 6px; overflow-x: auto; }
            blockquote { border-left: 4px solid #3498db; padding-left: 1em; color: #7f8c8d; }
            img { max-width: 100%; height: auto; border-radius: 4px; }
            table { border-collapse: collapse; width: 100%; margin: 1em 0; }
            th, td { border: 1px solid #bdc3c7; padding: 8px; }
            th { background-color: #ecf0f1; }
        """,
        'classic': """
            body { font-family: 'Noto Sans SC', 'Times New Roman', serif; line-height: 1.5; margin: 2em; color: #000; }
            h1 { color: #000; text-align: center; border-bottom: 2px solid #000; padding-bottom: 0.3em; }
            h2 { color: #333; margin-top: 1.5em; border-bottom: 1px solid #ccc; }
            h3 { color: #444; }
            code { background: #eee; padding: 1px 3px; border: 1px solid #ddd; font-family: 'Courier New', monospace; }
            pre { background: #eee; padding: 1em; border: 1px solid #ddd; overflow-x: auto; }
            blockquote { border-left: 4px solid #ccc; padding-left: 1em; color: #666; font-style: italic; }
            img { max-width: 100%; height: auto; }
            table { border-collapse: collapse; width: 100%; margin: 1em 0; }
            th, td { border: 1px solid #ccc; padding: 8px; }
            th { background-color: #eee; }
        """
    }
    return styles.get(style, styles['default'])

def run(**kwargs):
    markdown_content = kwargs.get('markdown_content')
    style = kwargs.get('style', 'default')
    output_filename = kwargs.get('output_filename', 'output')
    auto_monitor = kwargs.get('auto_monitor', False)
    monitor_dir = kwargs.get('monitor_dir', '.')
    output_dir = kwargs.get('output_dir', 'pdf_output')
    
    # Start auto-monitoring if requested
    if auto_monitor:
        monitor_thread = threading.Thread(
            target=start_auto_monitor,
            args=(monitor_dir, style, output_dir)
        )
        monitor_thread.daemon = True
        monitor_thread.start()
        return {
            "status": "success",
            "message": f"Started monitoring {monitor_dir} for Markdown files. PDFs will be saved to {output_dir}"
        }
    
    # If no markdown content is provided, try to find markdown files
    if not markdown_content:
        markdown_files = find_markdown_files()
        if not markdown_files:
            return {"status": "error", "message": "No markdown content provided and no markdown files found"}
        
        # Process all found markdown files
        results = []
        for file_path in markdown_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                result = convert_markdown_to_pdf(content, style, base_name)
                results.append({
                    "file": file_path,
                    "status": result["status"],
                    "pdf_path": result["file_path"]
                })
            except Exception as e:
                results.append({
                    "file": file_path,
                    "status": "error",
                    "message": str(e)
                })
        return {"status": "success", "results": results}
    
    # Process single markdown content
    try:
        result = convert_markdown_to_pdf(markdown_content, style, output_filename)
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == '__main__':
    # 自动测试 run 函数
    result = run(markdown_content="# Hello\nThis is a test.", style="modern", output_filename="test_output")
    print(result)
