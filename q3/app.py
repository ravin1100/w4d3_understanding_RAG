import streamlit as st
import os
from typing import Dict, Type

from chunking.base import BaseChunker
from chunking.fixed_size import FixedSizeChunker
from chunking.sliding_window import SlidingWindowChunker
from chunking.sentence_based import SentenceBasedChunker
from chunking.recursive_split import RecursiveChunker
from utils.pdf_utils import extract_text_from_pdf, get_pdf_preview
from utils.visualization import (
    render_chunk_preview,
    render_chunks_table,
    render_strategy_info,
    download_chunks_as_json
)

# Define available chunking strategies
CHUNKING_STRATEGIES: Dict[str, Type[BaseChunker]] = {
    "Fixed Size": FixedSizeChunker,
    "Sliding Window": SlidingWindowChunker,
    "Sentence Based": SentenceBasedChunker,
    "Recursive": RecursiveChunker
}

def main():
    st.title("RAG Chunking Strategy Visualizer")
    st.markdown("""
    Upload a PDF document and explore different text chunking strategies used in 
    Retrieval-Augmented Generation (RAG) pipelines.
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])
    
    if uploaded_file:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        try:
            # Extract text from PDF
            result = extract_text_from_pdf(temp_path)
            text = result["text"]
            
            # Display PDF metadata
            st.markdown("### Document Information")
            st.json(result["metadata"])
            
            # Show text preview
            st.markdown("### Text Preview")
            st.text(get_pdf_preview(text))
            
            # Strategy selection
            st.markdown("### Chunking Strategy")
            strategy_name = st.selectbox(
                "Select a chunking strategy",
                list(CHUNKING_STRATEGIES.keys()),
                index=0  # Set default selection to first strategy
            )
            
            # Strategy parameters
            st.markdown("### Strategy Parameters")
            if strategy_name is not None:  # Type check
                chunker_class = CHUNKING_STRATEGIES[strategy_name]
                
                params = {}
                if strategy_name == "Fixed Size":
                    params["chunk_size"] = st.number_input(
                        "Chunk size (characters)",
                        min_value=100,
                        max_value=10000,
                        value=1000
                    )
                    params["overlap"] = st.number_input(
                        "Overlap size (characters)",
                        min_value=0,
                        max_value=1000,
                        value=0
                    )
                
                elif strategy_name == "Sliding Window":
                    params["window_size"] = st.number_input(
                        "Window size (characters)",
                        min_value=100,
                        max_value=10000,
                        value=1000
                    )
                    params["stride"] = st.number_input(
                        "Stride size (characters)",
                        min_value=50,
                        max_value=5000,
                        value=500
                    )
                
                elif strategy_name == "Sentence Based":
                    params["max_sentences"] = st.number_input(
                        "Maximum sentences per chunk",
                        min_value=1,
                        max_value=50,
                        value=5
                    )
                    params["min_sentences"] = st.number_input(
                        "Minimum sentences per chunk",
                        min_value=1,
                        max_value=10,
                        value=1
                    )
                
                elif strategy_name == "Recursive":
                    params["max_chunk_size"] = st.number_input(
                        "Maximum chunk size (characters)",
                        min_value=100,
                        max_value=10000,
                        value=2000
                    )
                    params["min_chunk_size"] = st.number_input(
                        "Minimum chunk size (characters)",
                        min_value=50,
                        max_value=1000,
                        value=100
                    )
                
                # Create chunker instance
                chunker = chunker_class(**params)
                
                # Display strategy information
                render_strategy_info(chunker.get_metadata())
                
                # Process button
                if st.button("Process Text"):
                    with st.spinner("Processing..."):
                        # Generate chunks
                        chunks = chunker.chunk_text(text)
                        
                        # Display results
                        st.markdown(f"### Results ({len(chunks)} chunks)")
                        
                        # Table view
                        st.markdown("#### Chunks Overview")
                        render_chunks_table(chunks)
                        
                        # Detailed view
                        st.markdown("#### Detailed View")
                        for i, chunk in enumerate(chunks):
                            render_chunk_preview(chunk, i)
                        
                        # Download options
                        st.markdown("#### Download Results")
                        download_chunks_as_json(chunks)
        
        except Exception as e:
            st.error(f"Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)

if __name__ == "__main__":
    main() 