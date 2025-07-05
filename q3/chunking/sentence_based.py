from typing import List
import uuid
import nltk
from .base import BaseChunker, Chunk

class SentenceBasedChunker(BaseChunker):
    """Chunker that splits text into chunks based on sentence boundaries."""
    
    def __init__(self, max_sentences: int = 5, min_sentences: int = 1):
        """Initialize sentence-based chunker.
        
        Args:
            max_sentences (int): Maximum number of sentences per chunk
            min_sentences (int): Minimum number of sentences per chunk
        """
        super().__init__(max_sentences=max_sentences, min_sentences=min_sentences)
        self.max_sentences = max_sentences
        self.min_sentences = min_sentences
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
    
    def chunk_text(self, text: str) -> List[Chunk]:
        """Split text into chunks based on sentence boundaries.
        
        Args:
            text (str): Input text to be chunked
            
        Returns:
            List[Chunk]: List of chunks with metadata
        """
        # Tokenize text into sentences
        sentences = nltk.sent_tokenize(text)
        chunks = []
        current_sentences = []
        current_length = 0
        start_char = 0
        
        for sentence in sentences:
            current_sentences.append(sentence)
            current_length += len(sentence)
            
            # Create chunk when we reach max sentences or last sentence
            if (len(current_sentences) >= self.max_sentences or 
                (len(current_sentences) >= self.min_sentences and 
                 sentence == sentences[-1])):
                
                # Join sentences with space
                chunk_text = ' '.join(current_sentences)
                end_char = start_char + len(chunk_text)
                
                chunk = Chunk(
                    id=str(uuid.uuid4()),
                    text=chunk_text,
                    start_char=start_char,
                    end_char=end_char,
                    length=len(chunk_text),
                    overlap_prev=0,  # No overlap in sentence-based chunking
                    overlap_next=0
                )
                chunks.append(chunk)
                
                # Reset for next chunk
                start_char = end_char + 1  # +1 for the space that will be added
                current_sentences = []
                current_length = 0
        
        # Handle any remaining sentences
        if current_sentences:
            chunk_text = ' '.join(current_sentences)
            end_char = start_char + len(chunk_text)
            
            chunk = Chunk(
                id=str(uuid.uuid4()),
                text=chunk_text,
                start_char=start_char,
                end_char=end_char,
                length=len(chunk_text),
                overlap_prev=0,
                overlap_next=0
            )
            chunks.append(chunk)
        
        return chunks
    
    @property
    def description(self) -> str:
        return "Splits text into chunks based on sentence boundaries, maintaining semantic coherence."
    
    @property
    def pros(self) -> List[str]:
        return [
            "Preserves sentence integrity",
            "Maintains semantic meaning",
            "Natural text boundaries",
            "Better for downstream NLP tasks"
        ]
    
    @property
    def cons(self) -> List[str]:
        return [
            "Variable chunk sizes",
            "May create very large chunks with long sentences",
            "Dependent on sentence detection quality",
            "May struggle with informal text or unusual punctuation"
        ]
    
    @property
    def use_cases(self) -> List[str]:
        return [
            "Processing formal documents",
            "When semantic coherence is important",
            "Question-answering systems",
            "Summarization tasks"
        ] 