from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np
from typing import List, Dict, Any

class EmbeddingGenerator:
    def __init__(self):
        self.models = {
            "all-MiniLM-L6-v2": None,
            "paraphrase-MiniLM-L12-v2": None,
            "text-embedding-ada-002": None
        }
        self.openai_client = None

    def load_model(self, model_name: str, api_key: str = None) -> None:
        """Load the specified embedding model."""
        if model_name in ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L12-v2"]:
            if self.models[model_name] is None:
                self.models[model_name] = SentenceTransformer(model_name)
        elif model_name == "text-embedding-ada-002":
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
            else:
                raise ValueError("OpenAI API key is required for text-embedding-ada-002")

    def get_embeddings(self, texts: List[str], model_name: str) -> np.ndarray:
        """Generate embeddings for the input texts using the specified model."""
        if model_name in ["all-MiniLM-L6-v2", "paraphrase-MiniLM-L12-v2"]:
            if self.models[model_name] is None:
                self.load_model(model_name)
            embeddings = self.models[model_name].encode(texts)
            return embeddings
        
        elif model_name == "text-embedding-ada-002":
            if self.openai_client is None:
                raise ValueError("OpenAI client not initialized. Please provide API key.")
            
            embeddings = []
            for text in texts:
                response = self.openai_client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=text
                )
                embeddings.append(response.data[0].embedding)
            return np.array(embeddings)
        
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def get_available_models(self) -> List[str]:
        """Return list of available embedding models."""
        return list(self.models.keys()) 