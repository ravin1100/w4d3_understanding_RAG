import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple

def compute_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute pairwise cosine similarity matrix for the embeddings."""
    return cosine_similarity(embeddings)

def get_similar_pairs(similarity_matrix: np.ndarray, texts: List[str], threshold: float = 0.8) -> List[Tuple[str, str, float]]:
    """Find pairs of texts with similarity above the threshold."""
    similar_pairs = []
    n = len(texts)
    
    # Get pairs above threshold (excluding self-comparisons)
    for i in range(n):
        for j in range(i + 1, n):
            similarity = similarity_matrix[i][j]
            if similarity >= threshold:
                similar_pairs.append((texts[i], texts[j], similarity))
    
    return similar_pairs 