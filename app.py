
import streamlit as st

from document_processor import extract_document, split_into_passages
from retrieval import retrieve_passages


st.set_page_config(
    page_title="EvidenceDesk",
    page_icon="📚",
    layout="wide",
)

st.title("📚 EvidenceDesk")
st.write(
    "Ask questions about your documents and inspect the evidence "
    "behind each result."
)

st.caption(
    "PDF and TXT support · TF-IDF retrieval · Source references"
)

st.info(
    "Free local mode: no OpenAI API key or paid AI service is required."
)

uploaded_files = st.file_uploader(
    "Upload your documents",
    type=["pdf", "txt"],
    accept_multiple_files=True,
)

if uploaded_files:
    all_passages = []
    failed_files = []

    with st.spinner("Reading your documents..."):
        for uploaded_file in uploaded_files:
            try:
                pages = extract_document(uploaded_file)
                passages = split_into_passages(pages)
                all_passages.extend(passages)
            except Exception as error:
                failed_files.append(
                    f"{uploaded_file.name}: {error}"
                )

    for message in failed_files:
        st.warning(message)

    if all_passages:
        st.success(
            f"Created {len(all_passages)} passages from your documents."
        )

        question = st.text_input(
            "Ask a question",
            placeholder="How does TF-IDF find relevant passages?",
        )

        if st.button("Find evidence", type="primary"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Searching document evidence..."):
                    evidence = retrieve_passages(
                        question,
                        all_passages,
                        top_k=5,
                        min_score=0.05,
                    )

                if not evidence:
                    st.warning(
                        "Insufficient evidence: no relevant passages "
                        "were found in the uploaded documents."
                    )
                else:
                    st.subheader("Evidence found")

                    st.write(
                        "The following passages are the closest matches "
                        "found in your documents. Review them before "
                        "drawing a conclusion."
                    )

                    for item in evidence:
                        st.markdown(
                            f"**[{item['passage_id']}] "
                            f"{item['document_name']}**"
                        )
                        st.caption(
                            f"Page {item['page_number']} · "
                            f"Relevance score: "
                            f"{item['relevance_score']}"
                        )
                        st.write(item["text"])
                        st.divider()

                    st.caption(
                        "This free version retrieves evidence using "
                        "TF-IDF. It does not generate AI-written answers "
                        "or independently verify factual claims."
                    )

    else:
        st.error(
            "No readable passages were found. Try a text-based PDF "
            "or TXT file."
        )

else:
    st.info("Upload a PDF or TXT document to begin.")
