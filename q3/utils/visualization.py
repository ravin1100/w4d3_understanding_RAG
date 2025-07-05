import streamlit as st
import pandas as pd
from typing import List, Dict, Any
from chunking.base import Chunk

def render_chunk_preview(chunk: Chunk, index: int) -> None:
    """Render a preview of a chunk in Streamlit.
    
    Args:
        chunk (Chunk): The chunk to render
        index (int): Index of the chunk in the list
    """
    with st.expander(f"📄 Chunk {index + 1}"):
        # Create two columns for metadata and text
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("**📊 Chunk Info**")
            st.markdown(f"• Length: {chunk.length} characters")
            st.markdown(f"• Position: {chunk.start_char} → {chunk.end_char}")
            if chunk.overlap_prev > 0:
                st.markdown(f"• Overlap with previous: {chunk.overlap_prev} chars")
            if chunk.overlap_next > 0:
                st.markdown(f"• Overlap with next: {chunk.overlap_next} chars")
        
        with col2:
            st.markdown("**📝 Content Preview**")
            preview = chunk.text[:500] + "..." if len(chunk.text) > 500 else chunk.text
            st.markdown(f"```text\n{preview}\n```")

def render_chunks_table(chunks: List[Chunk]) -> None:
    """Render a table view of chunks in Streamlit.
    
    Args:
        chunks (List[Chunk]): List of chunks to render
    """
    # Convert chunks to DataFrame with simplified columns
    chunks_data = [{
        "Chunk #": f"Chunk {i+1}",
        "Length": f"{chunk.length} chars",
        "Preview": chunk.text[:100] + "..." if len(chunk.text) > 100 else chunk.text,
        "Overlaps": f"Prev: {chunk.overlap_prev}, Next: {chunk.overlap_next}" if (chunk.overlap_prev > 0 or chunk.overlap_next > 0) else "None"
    } for i, chunk in enumerate(chunks)]
    
    df = pd.DataFrame(chunks_data)
    
    # Add custom CSS to ensure table takes full width
    st.markdown("""
        <style>
        .stDataFrame {
            width: 100%;
        }
        .stDataFrame > div {
            width: 100%;
        }
        .stDataFrame table {
            width: 100% !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Render table with full width configuration
    st.dataframe(
        df,
        column_config={
            "Chunk #": st.column_config.TextColumn("Chunk #", width="small"),
            "Length": st.column_config.TextColumn("Length", width="small"),
            "Preview": st.column_config.TextColumn("Content Preview", width="large"),
            "Overlaps": st.column_config.TextColumn("Overlaps", width="medium")
        },
        hide_index=True,
        use_container_width=True  # This makes the table use full container width
    )

def render_strategy_info(strategy_metadata: Dict[str, Any]) -> None:
    """Render information about the selected chunking strategy.
    
    Args:
        strategy_metadata (Dict[str, Any]): Strategy metadata from BaseChunker
    """
    # Create tabs for different aspects of the strategy
    tab1, tab2, tab3 = st.tabs(["📖 Overview", "✨ Features", "⚙️ Settings"])
    
    with tab1:
        st.markdown(f"### About {strategy_metadata['name']}")
        st.info(strategy_metadata["description"])
    
    with tab2:
        # Create two columns for pros and cons
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Advantages")
            for pro in strategy_metadata["pros"]:
                st.markdown(f"• {pro}")
        
        with col2:
            st.markdown("#### ⚠️ Limitations")
            for con in strategy_metadata["cons"]:
                st.markdown(f"• {con}")
        
        st.markdown("#### 🎯 Best Use Cases")
        for use_case in strategy_metadata["use_cases"]:
            st.markdown(f"• {use_case}")
    
    with tab3:
        if strategy_metadata["parameters"]:
            st.markdown("#### Current Configuration")
            for param, value in strategy_metadata["parameters"].items():
                # Convert parameter name from snake_case to Title Case
                param_name = " ".join(word.capitalize() for word in param.split("_"))
                st.markdown(f"• **{param_name}:** {value}")

def download_chunks_as_json(chunks: List[Chunk]) -> None:
    """Create a download button for chunks in JSON format.
    
    Args:
        chunks (List[Chunk]): List of chunks to download
    """
    chunks_data = [{
        "chunk_number": i + 1,
        "text": chunk.text,
        "length": chunk.length,
        "start_position": chunk.start_char,
        "end_position": chunk.end_char,
        "overlap_previous": chunk.overlap_prev,
        "overlap_next": chunk.overlap_next
    } for i, chunk in enumerate(chunks)]
    
    df = pd.DataFrame(chunks_data)
    
    # Convert to string explicitly for download
    json_str = df.to_json(orient="records")
    csv_str = df.to_csv(index=False)
    
    # Create a container for download buttons
    st.markdown("#### 💾 Export Options")
    col1, col2 = st.columns(2)
    
    if json_str is not None:
        with col1:
            st.download_button(
                "📥 Download as JSON",
                json_str,
                "chunks.json",
                "application/json",
                use_container_width=True
            )
    
    if csv_str is not None:
        with col2:
            st.download_button(
                "📥 Download as CSV",
                csv_str,
                "chunks.csv",
                "text/csv",
                use_container_width=True
            ) 