
from pathlib import Path
from document_processor import extract_document, split_into_passages


class UploadedPDF:
    def __init__(self, path):
        self.name = path.name
        self._content = path.read_bytes()

    def getvalue(self):
        return self._content


pdf_file = UploadedPDF(Path("sample.pdf"))

pages = extract_document(pdf_file)
passages = split_into_passages(pages)

print("PDF pages extracted:", len(pages))
print("Passages created:", len(passages))

for passage in passages[:3]:
    print("\nPassage ID:", passage["passage_id"])
    print("Page:", passage["page_number"])
    print("Text:", passage["text"][:200])

assert len(pages) > 0
assert len(passages) > 0
assert all(p["page_number"] >= 1 for p in passages)

print("\nPDF extraction test passed!")
