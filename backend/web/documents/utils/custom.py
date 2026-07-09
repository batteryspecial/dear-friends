
from typing import List
from langchain_core.embeddings import Embeddings
from langchain_huggingface import HuggingFaceEmbeddings

class CustomEmbeddings(Embeddings):
    def __init__(self):
        # Wrap the Hugging Face embedding model inside the class contract
        self.model = HuggingFaceEmbeddings(
            model_name='sentence-transformers/all-MiniLM-L6-v2',
            model_kwargs={'device':'mps'} # 'cuda', 'cpu', etc.
        )
        if hasattr(self.model, "cache_folder"):
            delattr(self.model, "cache_folder")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents locally."""
        cleaned_texts = [t for t in texts if t.strip()]
        if not cleaned_texts:
            return []
            
        return self.model.embed_documents(cleaned_texts)

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query string locally."""
        if not text.strip():
            return []
            
        return self.model.embed_query(text)
