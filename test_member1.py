
from document_processor import extract_document, split_into_passages
from retrieval import retrieve_passages


class TestUpload:
    name = "sample.txt"

    def getvalue(self):
        return (
            b"Python is a programming language. "
            b"TF-IDF helps retrieve relevant text passages. "
            b"EvidenceDesk answers questions using document evidence."
        )


pages = extract_document(TestUpload())
passages = split_into_passages(
    pages,
    max_words=10,
    overlap_words=2
)

results = retrieve_passages("What does TF-IDF do?", passages)

print("Extracted pages:", len(pages))
print("Created passages:", len(passages))
print("Retrieved passages:", len(results))

for passage in results:
    print("\nPassage ID:", passage["passage_id"])
    print("Text:", passage["text"])
    print("Score:", passage["relevance_score"])

assert len(pages) == 1
assert len(passages) > 0
assert len(results) > 0

print("\nMember 1 test passed!")
