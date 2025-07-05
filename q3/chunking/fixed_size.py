from typing import List
import uuid
from .base import BaseChunker, Chunk

class FixedSizeChunker(BaseChunker):
    """Chunker that splits text into fixed-size chunks with optional overlap."""
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 0):
        """Initialize fixed-size chunker.
        
        Args:
            chunk_size (int): Size of each chunk in characters
            overlap (int): Number of characters to overlap between chunks
        """
        super().__init__(chunk_size=chunk_size, overlap=overlap)
        self.chunk_size = chunk_size
        self.overlap = overlap
        
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text into fixed-size chunks.
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        chunks = []
        text_length = len(text)
        start = 0
        
        while start < text_length:
            # Calculate end position for current chunk
            end = min(start + self.chunk_size, text_length)
            
            # Create chunk with metadata
            chunk = Chunk(
                id=str(uuid.uuid4()),
                text=text[start:end],
                start_char=start,
                end_char=end,
                length=end - start,
                overlap_prev=min(self.overlap, start),  # For first chunk
                overlap_next=min(self.overlap, text_length - end)  # For last chunk
            )
            chunks.append(chunk)
            
            # Move start position for next chunk, considering overlap
            start = end - self.overlap if self.overlap > 0 else end
            
        return chunks
    
    @property
    def description(self) -> str:
        return "Splits text into chunks of fixed character length with optional overlap between chunks."
    
    @property
    def pros(self) -> List[str]:
        return [
            "Simple and predictable chunk sizes",
            "Consistent memory usage",
            "Easy to implement and maintain",
            "Good for uniform text distribution"
        ]
    
    @property
    def cons(self) -> List[str]:
        return [
            "May split sentences or logical units",
            "Not context-aware",
            "Can create awkward breaks in text",
            "May not preserve semantic meaning"
        ]
    
    @property
    def use_cases(self) -> List[str]:
        return [
            "Processing large documents with uniform content",
            "When consistent chunk sizes are required",
            "Simple text splitting without semantic requirements",
            "Memory-constrained environments"
        ] 