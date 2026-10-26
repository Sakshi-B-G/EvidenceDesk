
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def retrieve_passages(question, passages, top_k=5, min_score=0.05):
    """
    Retrieve the passages most relevant to a user's question
    using TF-IDF and cosine similarity.
    """
    question = question.strip()

    if not question:
        return []

    if not passages:
        return []

    texts = [passage["text"] for passage in passages]

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english"
        )

        document_vectors = vectorizer.fit_transform(texts)
        question_vector = vectorizer.transform([question])

        scores = cosine_similarity(
            question_vector,
            document_vectors
        ).flatten()

    except ValueError:
        # Handles text that produces no usable vocabulary.
        return []

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )

    results = []

    for index in ranked_indices:
        score = float(scores[index])

        if score < min_score:
            continue

        result = passages[index].copy()
        result["relevance_score"] = round(score, 4)
        results.append(result)

        if len(results) >= top_k:
            break

    return results
