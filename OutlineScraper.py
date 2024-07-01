import PyPDF2
import re
from typing import Optional, Union
from Constants import STARTING_CONTENT_PAGE, END_CONTENT_PAGE


class Chapter:
    def __init__(self, number: str, title: str, page: str):
        self.number = number
        self.title = title
        self.page = page

    def to_dict(self):
        return {'level': 2, 'title': f'{self.number} {self.title}', 'page_num': int(self.number)}


class SubPage:
    def __init__(self, title: str, page: str):
        self.title = title
        self.page = page

    def to_dict(self):
        return {'level': 3, 'title': self.title, 'page_num': int(self.page)}


class Part:
    def __init__(self, number: str, title: str, page: str):
        self.number = number
        self.title = title
        self.page = page

    def to_dict(self):
        return {'level': 1, 'title': f'{self.number} {self.title}', 'page_num': int(self.page)}


def parse_pdf(file_path, num_pages=None):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        if num_pages is None or num_pages > total_pages:
            num_pages = total_pages

        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            print(f"Page {page_num + 1}: {text}")


def read_page(file_path, page_num) -> str:
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        page = reader.pages[page_num - 1]
        text = page.extract_text()
        return text


def search_text(file_path, search_text):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)

        for page_num in range(total_pages):
            page = reader.pages[page_num]
            text = page.extract_text()

            if search_text in text:
                print(f"Found '{search_text}' on page {page_num + 1}")


def parseContent(text: str) -> Optional[Union[Chapter, SubPage, Part]]:
    # Regex pattern to match part, chapter, and subpage entries
    part_pattern = r"Part ([IVXLCDM]+) (.*?) (\d+)$"
    chapter_pattern = r"(?:Chapter (\d+)\s)?(.*?)\s(\d+)$"

    part_match = re.search(part_pattern, text)
    if part_match:
        part_number = part_match.group(1)
        title = part_match.group(2).strip()
        page = part_match.group(3)
        return Part(part_number, title, page)

    chapter_match = re.search(chapter_pattern, text)
    if chapter_match:
        chapter_number = chapter_match.group(1)
        title = chapter_match.group(2).strip()
        page = chapter_match.group(3)
        if chapter_number:
            return Chapter(chapter_number, title, page)
        else:
            return SubPage(title, page)
    return None


def main():
    global document_outline

    contentPages = [i for i in range(
        STARTING_CONTENT_PAGE, END_CONTENT_PAGE + 1)]

    parsed_entries = []
    for page in contentPages:
        text = read_page('reversing.pdf', page)
        lines = text.split("\n")
        for line in lines:
            parsed_entry = parseContent(line)
            if parsed_entry:
                parsed_entries.append(parsed_entry)

    document_outline = []
    for entry in parsed_entries:
        document_outline.append(entry.to_dict())


if __name__ == '__main__':
    main()
