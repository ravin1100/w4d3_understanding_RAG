import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import List, Tuple

def create_similarity_heatmap(similarity_matrix: np.ndarray, texts: List[str]) -> plt.Figure:
    """Create a heatmap visualization of the similarity matrix."""
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        similarity_matrix,
        annot=True,
        cmap='YlOrRd',
        fmt='.2f',
        xticklabels=[f'Text {i+1}' for i in range(len(texts))],
        yticklabels=[f'Text {i+1}' for i in range(len(texts))]
    )
    plt.title('Text Similarity Matrix')
    return plt.gcf()

def create_similarity_table(similar_pairs: List[Tuple[str, str, float]]) -> pd.DataFrame:
    """Create a DataFrame of similar text pairs."""
    if not similar_pairs:
        return pd.DataFrame(columns=['Text 1', 'Text 2', 'Similarity Score'])
    
    df = pd.DataFrame(similar_pairs, columns=['Text 1', 'Text 2', 'Similarity Score'])
    df['Similarity Score'] = df['Similarity Score'].round(3)
    return df.sort_values('Similarity Score', ascending=False)

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text for display purposes."""
    return text[:max_length] + '...' if len(text) > max_length else text 