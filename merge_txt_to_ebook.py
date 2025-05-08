import os
from ebooklib import epub

# 文件夹路径
TXT_DIR = 'txt'
# 输出电子书文件名
OUTPUT_FILE = 'EnglishPod.epub'

def get_txt_files(directory):
    """获取目录下所有txt文件，按文件名排序"""
    files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    return sorted(files)

def main():
    files = get_txt_files(TXT_DIR)
    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('EnglishPod')
    book.set_language('en')
    book.add_author('EnglishPod')

    # 生成目录章节
    toc_html = '<h1>目录</h1><ul>'
    chapters = []
    for fname in files:
        title = os.path.splitext(fname)[0]
        toc_html += f'<li><a href="{title}.xhtml">{fname}</a></li>'
    toc_html += '</ul>'
    toc_chapter = epub.EpubHtml(title='目录', file_name='toc.xhtml', content=toc_html)
    book.add_item(toc_chapter)

    # 添加每个txt为章节
    for fname in files:
        title = os.path.splitext(fname)[0]
        with open(os.path.join(TXT_DIR, fname), 'r', encoding='utf-8') as f:
            content = f.read().replace('\n', '<br/>')
        chapter = epub.EpubHtml(title=fname, file_name=f'{title}.xhtml', content=f'<h2>{fname}</h2><p>{content}</p>')
        book.add_item(chapter)
        chapters.append(chapter)

    # 设置目录和导航
    book.toc = [toc_chapter] + chapters
    book.spine = ['nav', toc_chapter] + chapters
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    epub.write_epub(OUTPUT_FILE, book, {})

    print(f'EPUB电子书已生成：{OUTPUT_FILE}')

if __name__ == '__main__':
    main() 