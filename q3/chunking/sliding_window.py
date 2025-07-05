from typing import List
import uuid
from .base import BaseChunker, Chunk

class SlidingWindowChunker(BaseChunker):
    """Chunker that uses a sliding window approach with fixed stride."""
    
    def __init__(self, window_size: int = 1000, stride: int = 500):
        """Initialize sliding window chunker.
        
        Args:
            window_size (int): Size of the window in characters
            stride (int): Number of characters to move the window in each step
        """
        super().__init__(window_size=window_size, stride=stride)
        self.window_size = window_size
        self.stride = stride
        
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text using sliding window approach.
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        chunks = []
        text_length = len(text)
        start = 0
        
        while start < text_length:
            # Calculate end position for current window
            end = min(start + self.window_size, text_length)
            
            # Calculate overlaps
            overlap_prev = min(start, self.window_size - self.stride)
            overlap_next = min(text_length - end, self.window_size - self.stride)
            
            # Create chunk with metadata
            chunk = Chunk(
                id=str(uuid.uuid4()),
                text=text[start:end],
                start_char=start,
                end_char=end,
                length=end - start,
                overlap_prev=overlap_prev,
                overlap_next=overlap_next
            )
            chunks.append(chunk)
            
            # Move window by stride
            start += self.stride
            
            # Break if we've reached the end
            if start >= text_length:
                break
        
        return chunks
    
    @property
    def description(self) -> str:
        return "Uses a sliding window approach with fixed stride to create overlapping chunks of text."
    
    @property
    def pros(self) -> List[str]:
        return [
            "Controlled overlap between chunks",
            "Good for capturing context around chunk boundaries",
            "Flexible stride size for different use cases",
            "Can help with context-dependent tasks"
        ]
    
    @property
    def cons(self) -> List[str]:
        return [
            "Duplicate content in overlapping regions",
            "Higher storage requirements due to overlap",
            "May still split sentences or logical units",
            "Requires careful tuning of window and stride sizes"
        ]
    
    @property
    def use_cases(self) -> List[str]:
        return [
            "Text classification with context",
            "Named entity recognition across chunk boundaries",
            "When context preservation is important",
            "Pattern detection across text segments"
        ] 