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

# Define available chunking strategies with descriptions
CHUNKING_STRATEGIES: Dict[str, Type[BaseChunker]] = {
    "Fixed Size": FixedSizeChunker,
    "Sliding Window": SlidingWindowChunker,
    "Sentence Based": SentenceBasedChunker,
    "Recursive": RecursiveChunker
}

# Strategy descriptions with examples
STRATEGY_DESCRIPTIONS = {
    "Fixed Size": """
    📏 **How it works:**
    - Splits text into chunks of exactly N characters
    - Can add overlap between chunks to preserve context
    
    Example with chunk_size=10, overlap=2:
    ```
    Text: "Hello world! How are you?"
    Chunk 1: "Hello worl"
    Chunk 2: "rld! How a"
    Chunk 3: "are you?"
    ```
    """,
    
    "Sliding Window": """
    🔄 **How it works:**
    - Uses a moving window of size N
    - Moves window by stride length
    - Creates overlapping chunks naturally
    
    Example with window=10, stride=6:
    ```
    Text: "Hello world! How are you?"
    Chunk 1: "Hello worl"
    Chunk 2: "world! How"
    Chunk 3: "! How are"
    Chunk 4: "are you?"
    ```
    """,
    
    "Sentence Based": """
    📝 **How it works:**
    - Respects sentence boundaries
    - Groups N sentences together
    - Maintains semantic meaning
    
    Example with max_sentences=2:
    ```
    Text: "Hello world! How are you? I am good. Thanks!"
    Chunk 1: "Hello world! How are you?"
    Chunk 2: "I am good. Thanks!"
    ```
    """,
    
    "Recursive": """
    🌳 **How it works:**
    - Analyzes document structure
    - Splits at natural boundaries:
      1. Headers
      2. Paragraphs
      3. Sentences
      4. Punctuation
    
    Example:
    ```
    Text: "# Section 1
    First paragraph here.
    
    # Section 2
    Second paragraph."
    
    Chunk 1: "# Section 1\\nFirst paragraph here."
    Chunk 2: "# Section 2\\nSecond paragraph."
    ```
    """
}

def set_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="RAG Chunking Visualizer",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS to reduce top margin and improve spacing
    st.markdown("""
        <style>
        /* Reduce top padding in main content */
        .main .block-container {
            padding-top: 2rem !important;
        }
        
        /* Reduce top padding in sidebar */
        .css-1d391kg {
            padding-top: 2rem !important;
        }
        
        /* Adjust sidebar title spacing */
        .css-1d391kg > div:first-child {
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        /* Reduce space between sidebar elements */
        .css-1d391kg .block-container {
            padding-top: 0 !important;
        }
        
        /* Adjust other spacings */
        .main {
            padding: 0rem;
        }
        .stButton>button {
            width: 100%;
        }
        .uploadedFile {
            margin-bottom: 1rem;
        }
        .strategy-description {
            background-color: #f0f2f6;
            border-radius: 5px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        code {
            background-color: #e6e6e6;
            padding: 2px 4px;
            border-radius: 3px;
        }
        pre {
            background-color: #f8f9fa;
            padding: 1rem;
            border-radius: 5px;
            margin: 0.5rem 0;
        }
        
        /* Reduce space between sections */
        .stMarkdown {
            margin-top: 0 !important;
        }
        
        /* Make headings more compact */
        h1, h2, h3 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
            padding-top: 0 !important;
        }
        
        /* Adjust file uploader spacing */
        .stFileUploader {
            margin-bottom: 1rem !important;
        }
        
        /* Reduce space in expanders */
        .streamlit-expanderHeader {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    set_page_config()
    
    # Header with reduced spacing
    st.title("📚 RAG Chunking Strategy Visualizer")
    st.markdown("""
    Explore different text chunking strategies used in Retrieval-Augmented Generation (RAG) pipelines.
    Upload a PDF document to see how different strategies would split your text.
    """)
    
    # Sidebar with reduced spacing
    with st.sidebar:
        st.markdown("### 📤 Upload Document")  # Changed from ## to ### for more compact look
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
            help="Upload a PDF document to analyze"
        )
        
        if uploaded_file:
            st.success("✅ File uploaded successfully!")
            
            st.markdown("### 🔧 Select Strategy")  # Changed from ## to ### for more compact look
            strategy_name = st.selectbox(
                "Chunking Strategy",
                list(CHUNKING_STRATEGIES.keys()),
                index=0,
                help="Choose how you want to split the text"
            )
            
            # Show strategy description
            if strategy_name in STRATEGY_DESCRIPTIONS:
                st.markdown("#### How this strategy works")  # Changed from ### to #### for more compact look
                st.markdown(STRATEGY_DESCRIPTIONS[strategy_name])
    
    # Main content area
    if uploaded_file:
        # Save uploaded file temporarily
        temp_path = f"temp_{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        try:
            # Extract text from PDF
            with st.spinner("📄 Extracting text from PDF..."):
                result = extract_text_from_pdf(temp_path)
                text = result["text"]
            
            # Create columns for document info and preview
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("### 📋 Document Details")
                st.markdown(f"**Title:** {result['metadata'].get('title', 'N/A')}")
                st.markdown(f"**Pages:** {result['metadata'].get('num_pages', 0)}")
                st.markdown(f"**Characters:** {len(text):,}")
            
            with col2:
                st.markdown("### 👀 Text Preview")
                with st.expander("Show preview", expanded=True):
                    st.markdown(f"```text\n{get_pdf_preview(text)}\n```")
            
            # Strategy configuration
            st.markdown("---")
            if strategy_name is not None:
                chunker_class = CHUNKING_STRATEGIES[strategy_name]
                
                # Parameters in a card-like container
                st.markdown("### ⚙️ Strategy Configuration")
                with st.container():
                    params = {}
                    
                    if strategy_name == "Fixed Size":
                        col1, col2 = st.columns(2)
                        with col1:
                            params["chunk_size"] = st.number_input(
                                "Chunk Size (characters)",
                                min_value=100,
                                max_value=10000,
                                value=1000,
                                help="Number of characters in each chunk"
                            )
                        with col2:
                            params["overlap"] = st.number_input(
                                "Overlap Size",
                                min_value=0,
                                max_value=1000,
                                value=0,
                                help="Number of characters to overlap between chunks"
                            )
                    
                    elif strategy_name == "Sliding Window":
                        col1, col2 = st.columns(2)
                        with col1:
                            params["window_size"] = st.number_input(
                                "Window Size",
                                min_value=100,
                                max_value=10000,
                                value=1000,
                                help="Size of the sliding window"
                            )
                        with col2:
                            params["stride"] = st.number_input(
                                "Stride Size",
                                min_value=50,
                                max_value=5000,
                                value=500,
                                help="How far to move the window in each step"
                            )
                    
                    elif strategy_name == "Sentence Based":
                        col1, col2 = st.columns(2)
                        with col1:
                            params["max_sentences"] = st.number_input(
                                "Maximum Sentences",
                                min_value=1,
                                max_value=50,
                                value=5,
                                help="Maximum number of sentences per chunk"
                            )
                        with col2:
                            params["min_sentences"] = st.number_input(
                                "Minimum Sentences",
                                min_value=1,
                                max_value=10,
                                value=1,
                                help="Minimum number of sentences per chunk"
                            )
                    
                    elif strategy_name == "Recursive":
                        col1, col2 = st.columns(2)
                        with col1:
                            params["max_chunk_size"] = st.number_input(
                                "Maximum Chunk Size",
                                min_value=100,
                                max_value=10000,
                                value=2000,
                                help="Maximum characters in a chunk"
                            )
                        with col2:
                            params["min_chunk_size"] = st.number_input(
                                "Minimum Chunk Size",
                                min_value=50,
                                max_value=1000,
                                value=100,
                                help="Minimum characters in a chunk"
                            )
                
                # Create chunker instance
                chunker = chunker_class(**params)
                
                # Display strategy information
                st.markdown("---")
                render_strategy_info(chunker.get_metadata())
                
                # Process button
                st.markdown("---")
                if st.button("🚀 Process Text", use_container_width=True):
                    with st.spinner("🔄 Processing text..."):
                        # Generate chunks
                        chunks = chunker.chunk_text(text)
                        
                        # Display results
                        st.markdown(f"### 📊 Results: {len(chunks):,} chunks generated")
                        
                        # Metrics summary
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Chunks", f"{len(chunks):,}")
                        with col2:
                            avg_length = sum(c.length for c in chunks) / len(chunks)
                            st.metric("Average Chunk Size", f"{avg_length:.0f} chars")
                        with col3:
                            total_overlap = sum(c.overlap_prev + c.overlap_next for c in chunks)
                            st.metric("Total Overlap", f"{total_overlap:,} chars")
                        
                        # Table view
                        st.markdown("#### 📋 Chunks Overview")
                        render_chunks_table(chunks)
                        
                        # Detailed view
                        st.markdown("#### 🔍 Detailed View")
                        for i, chunk in enumerate(chunks):
                            render_chunk_preview(chunk, i)
                        
                        # Download options
                        st.markdown("---")
                        download_chunks_as_json(chunks)
        
        except Exception as e:
            st.error(f"❌ Error processing PDF: {str(e)}")
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    else:
        # Show welcome message when no file is uploaded
        st.info("👆 Upload a PDF document using the sidebar to get started!")

if __name__ == "__main__":
    main() 