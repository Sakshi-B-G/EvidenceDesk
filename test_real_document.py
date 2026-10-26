
from pathlib import Path
from document_processor import extract_document, split_into_passages
from retrieval import retrieve_passages


class UploadedText:
    def __init__(self, path):
        self.name = path.name
        self._content = path.read_bytes()

    def getvalue(self):
        return self._content


file_path = Path("sample.txt")
uploaded_file = UploadedText(file_path)

pages = extract_document(uploaded_file)
passages = split_into_passages(pages)

question = "How does TF-IDF find relevant passages?"
results = retrieve_passages(question, passages)

print("Pages extracted:", len(pages))
print("Passages created:", len(passages))
print("Results found:", len(results))

for result in results:
    print("\nPassage ID:", result["passage_id"])
    print("Document:", result["document_name"])
    print("Page:", result["page_number"])
    print("Score:", result["relevance_score"])
    print("Text:", result["text"])

assert len(pages) == 1
assert len(passages) > 0
assert len(results) > 0
assert results[0]["document_name"] == "sample.txt"
assert results[0]["page_number"] == 1

print("\nReal TXT extraction and retrieval test passed!")

# A blank question should return no results.
assert retrieve_passages("", passages) == []

# An unrelated question should normally return no results
# with the current minimum similarity threshold.
unrelated = retrieve_passages(
    "What is the capital of Mars?",
    passages
)
print("Unrelated question results:", len(unrelated))
