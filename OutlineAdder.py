import fitz
import OutlineScraper
from Constants import PAGE_OFFSET


def add_outline(pdf_path, outline_data, output_path):
    doc = fitz.open(pdf_path)
    toc = []

    for item in outline_data:
        level = item['level']
        title = item['title']
        page_num = item['page_num'] + PAGE_OFFSET
        toc.append([level, title, page_num])

    doc.set_toc(toc)
    doc.save(output_path)


if __name__ == '__main__':
    OutlineScraper.main()
    pdf_path = 'reversing.pdf'
    output_path = 'reversing_with_outline.pdf'
    add_outline(pdf_path, OutlineScraper.document_outline, output_path)
