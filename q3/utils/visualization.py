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
    with st.expander(f"Chunk {index + 1} ({chunk.length} chars)"):
        # Display metadata
        st.markdown("**Metadata:**")
        st.json({
            "id": chunk.id,
            "start_char": chunk.start_char,
            "end_char": chunk.end_char,
            "length": chunk.length,
            "overlap_prev": chunk.overlap_prev,
            "overlap_next": chunk.overlap_next
        })
        
        # Display text preview
        st.markdown("**Text:**")
        st.text(chunk.text[:500] + "..." if len(chunk.text) > 500 else chunk.text)

def render_chunks_table(chunks: List[Chunk]) -> None:
    """Render a table view of chunks in Streamlit.
    
    Args:
        chunks (List[Chunk]): List of chunks to render
    """
    # Convert chunks to DataFrame
    chunks_data = [{
        "Chunk ID": chunk.id,
        "Length": chunk.length,
        "Start": chunk.start_char,
        "End": chunk.end_char,
        "Overlap Prev": chunk.overlap_prev,
        "Overlap Next": chunk.overlap_next,
        "Preview": chunk.text[:50] + "..."
    } for chunk in chunks]
    
    df = pd.DataFrame(chunks_data)
    st.dataframe(df)

def render_strategy_info(strategy_metadata: Dict[str, Any]) -> None:
    """Render information about the selected chunking strategy.
    
    Args:
        strategy_metadata (Dict[str, Any]): Strategy metadata from BaseChunker
    """
    st.markdown("### Strategy Information")
    
    # Description
    st.markdown("**Description:**")
    st.write(strategy_metadata["description"])
    
    # Advantages
    st.markdown("**Advantages:**")
    for pro in strategy_metadata["pros"]:
        st.markdown(f"- {pro}")
    
    # Disadvantages
    st.markdown("**Disadvantages:**")
    for con in strategy_metadata["cons"]:
        st.markdown(f"- {con}")
    
    # Use Cases
    st.markdown("**Best Use Cases:**")
    for use_case in strategy_metadata["use_cases"]:
        st.markdown(f"- {use_case}")
    
    # Parameters
    if strategy_metadata["parameters"]:
        st.markdown("**Current Parameters:**")
        st.json(strategy_metadata["parameters"])

def download_chunks_as_json(chunks: List[Chunk]) -> None:
    """Create a download button for chunks in JSON format.
    
    Args:
        chunks (List[Chunk]): List of chunks to download
    """
    chunks_data = [{
        "id": chunk.id,
        "text": chunk.text,
        "start_char": chunk.start_char,
        "end_char": chunk.end_char,
        "length": chunk.length,
        "overlap_prev": chunk.overlap_prev,
        "overlap_next": chunk.overlap_next
    } for chunk in chunks]
    
    df = pd.DataFrame(chunks_data)
    
    # Convert to string explicitly for download
    json_str = df.to_json(orient="records")
    csv_str = df.to_csv(index=False)
    
    if json_str is not None:  # Ensure we have valid data
        st.download_button(
            "Download Chunks (JSON)",
            json_str,
            "chunks.json",
            "application/json"
        )
    
    if csv_str is not None:  # Ensure we have valid data
        st.download_button(
            "Download Chunks (CSV)",
            csv_str,
            "chunks.csv",
            "text/csv"
        ) 