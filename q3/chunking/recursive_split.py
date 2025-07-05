from typing import List
import uuid
import re
from .base import BaseChunker, Chunk

class RecursiveChunker(BaseChunker):
    """Chunker that recursively splits text based on document structure."""
    
    def __init__(self, max_chunk_size: int = 2000, min_chunk_size: int = 100):
        """Initialize recursive chunker.
        
        Args:
            max_chunk_size (int): Maximum size of a chunk in characters
            min_chunk_size (int): Minimum size of a chunk in characters
        """
        super().__init__(max_chunk_size=max_chunk_size, min_chunk_size=min_chunk_size)
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
        
        # Define split patterns in order of preference
        self.split_patterns = [
            r'\n\s*#{2,}[^\n]+\n',  # Headers
            r'\n\s*\n',             # Double newlines (paragraphs)
            r'[.!?]\s+',            # Sentence endings
            r'[,;:]\s+',            # Other punctuation
            r'\s+'                  # Any whitespace
        ]
    
    def find_best_split_point(self, text: str) -> int:
        """Find the best point to split the text based on document structure.
        
        Args:
            text (str): Text to find split point in
            
        Returns:
            int: Index of best split point
        """
        # Try each pattern in order until we find a good split point
        for pattern in self.split_patterns:
            matches = list(re.finditer(pattern, text))
            if matches:
                # Find the match closest to the middle
                middle = len(text) / 2
                best_match = min(matches, key=lambda m: abs(m.end() - middle))
                return best_match.end()
        
        # If no patterns match, split at the middle of the text
        return len(text) // 2
    
    def recursive_split(self, text: str, start_char: int = 0) -> List[Chunk]:
        """Recursively split text into chunks.
        
        Args:
            text (str): Text to split
            start_char (int): Starting character position in original text
            
        Returns:
            List[Chunk]: List of chunks
        """
        if len(text) <= self.max_chunk_size:
            if len(text) >= self.min_chunk_size:
                return [Chunk(
                    id=str(uuid.uuid4()),
                    text=text,
                    start_char=start_char,
                    end_char=start_char + len(text),
                    length=len(text),
                    overlap_prev=0,
                    overlap_next=0
                )]
            return []
        
        # Find best split point
        split_point = self.find_best_split_point(text)
        
        # Recursively split both halves
        first_half = text[:split_point].strip()
        second_half = text[split_point:].strip()
        
        chunks = []
        if first_half:
            chunks.extend(self.recursive_split(first_half, start_char))
        if second_half:
            chunks.extend(self.recursive_split(
                second_half, 
                start_char + split_point
            ))
        
        return chunks
    
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text recursively based on document structure.
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        return self.recursive_split(text)
    
    @property
    def description(self) -> str:
        return "Recursively splits text based on document structure, respecting natural boundaries."
    
    @property
    def pros(self) -> List[str]:
        return [
            "Respects document structure",
            "Adapts to content patterns",
            "Creates more natural chunks",
            "Maintains hierarchical relationships"
        ]
    
    @property
    def cons(self) -> List[str]:
        return [
            "More complex implementation",
            "Variable chunk sizes",
            "May be slower than simpler methods",
            "Requires well-structured input text"
        ]
    
    @property
    def use_cases(self) -> List[str]:
        return [
            "Processing structured documents",
            "Technical documentation",
            "Academic papers",
            "Content with clear hierarchical structure"
        ] 