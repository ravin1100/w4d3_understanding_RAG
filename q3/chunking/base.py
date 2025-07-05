from abc import ABC, abstractmethod
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class Chunk:
    """Data class representing a text chunk with metadata."""
    id: str
    text: str
    start_char: int
    end_char: int
    length: int
    overlap_prev: int = 0
    overlap_next: int = 0

class BaseChunker(ABC):
    """Abstract base class for text chunking strategies."""
    
    def __init__(self, **kwargs):
        """Initialize chunker with strategy-specific parameters."""
        self.params = kwargs
        
    @abstractmethod
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text into chunks according to the strategy.
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of the chunking strategy."""
        pass
    
    @property
    @abstractmethod
    def pros(self) -> List[str]:
        """Return list of advantages of this chunking strategy."""
        pass
    
    @property
    @abstractmethod
    def cons(self) -> List[str]:
        """Return list of disadvantages of this chunking strategy."""
        pass
    
    @property
    @abstractmethod
    def use_cases(self) -> List[str]:
        """Return list of recommended use cases for this strategy."""
        pass
    
    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata about the chunking strategy."""
        return {
            "name": self.__class__.__name__,
            "description": self.description,
            "pros": self.pros,
            "cons": self.cons,
            "use_cases": self.use_cases,
            "parameters": self.params
        } 