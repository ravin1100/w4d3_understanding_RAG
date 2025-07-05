import streamlit as st
import os
from dotenv import load_dotenv
from embeddings import EmbeddingGenerator
from similarity import compute_similarity_matrix, get_similar_pairs
from visualization import create_similarity_heatmap, create_similarity_table, truncate_text

# Load environment variables
load_dotenv()

# Initialize session state
if 'texts' not in st.session_state:
    st.session_state.texts = [""]
if 'embedding_generator' not in st.session_state:
    st.session_state.embedding_generator = EmbeddingGenerator()

def main():
    st.set_page_config(page_title="Semantic Plagiarism Detector", layout="wide")
    
    st.title("🔍 Semantic Plagiarism Detector")
    st.write("Compare multiple text entries for semantic similarity using different embedding models.")

    # Sidebar for model selection and OpenAI API key
    with st.sidebar:
        st.header("Model Configuration")
        model_name = st.selectbox(
            "Select Embedding Model",
            st.session_state.embedding_generator.get_available_models()
        )
        
        if model_name == "text-embedding-ada-002":
            api_key = st.text_input("OpenAI API Key", type="password")
            if api_key:
                os.environ["OPENAI_API_KEY"] = api_key
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        This tool helps detect semantic similarities between texts using:
        - Sentence Transformers
        - OpenAI Embeddings
        - Cosine Similarity
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Texts")
        
        # Dynamic text input fields
        for i in range(len(st.session_state.texts)):
            text = st.text_area(
                f"Text {i+1}",
                value=st.session_state.texts[i],
                key=f"text_{i}",
                height=100
            )
            st.session_state.texts[i] = text

        # Add/remove text fields
        col_add, col_remove = st.columns([1, 1])
        with col_add:
            if st.button("➕ Add Text Field"):
                st.session_state.texts.append("")
                st.rerun()
        with col_remove:
            if len(st.session_state.texts) > 1 and st.button("➖ Remove Last Field"):
                st.session_state.texts.pop()
                st.rerun()

    with col2:
        st.subheader("Analysis Controls")
        similarity_threshold = st.slider(
            "Similarity Threshold (%)",
            min_value=0,
            max_value=100,
            value=80
        ) / 100.0

        analyze_button = st.button("🔍 Analyze Texts")

    # Analysis and visualization
    if analyze_button:
        # Validate inputs
        texts = [text.strip() for text in st.session_state.texts if text.strip()]
        if len(texts) < 2:
            st.error("Please enter at least 2 texts to compare.")
            return

        if model_name == "text-embedding-ada-002" and not os.getenv("OPENAI_API_KEY"):
            st.error("Please provide an OpenAI API key to use this model.")
            return

        with st.spinner("Analyzing texts..."):
            try:
                # Generate embeddings
                st.session_state.embedding_generator.load_model(
                    model_name,
                    api_key=os.getenv("OPENAI_API_KEY")
                )
                embeddings = st.session_state.embedding_generator.get_embeddings(texts, model_name)

                # Compute similarity
                similarity_matrix = compute_similarity_matrix(embeddings)
                similar_pairs = get_similar_pairs(similarity_matrix, texts, similarity_threshold)

                # Display results
                st.subheader("Results")
                
                tab1, tab2 = st.tabs(["Similarity Matrix", "Similar Pairs"])
                
                with tab1:
                    st.pyplot(create_similarity_heatmap(similarity_matrix, texts))
                
                with tab2:
                    if similar_pairs:
                        df = create_similarity_table(similar_pairs)
                        st.dataframe(
                            df.style.background_gradient(subset=['Similarity Score'], cmap='YlOrRd'),
                            use_container_width=True
                        )
                    else:
                        st.info("No text pairs found above the similarity threshold.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 