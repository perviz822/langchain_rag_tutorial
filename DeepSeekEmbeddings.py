import os
import requests
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("DEEP_SEEK_API_KEY")
if not API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not found. Please set it in your .env file.")

class DeepSeekEmbeddings:
    def __init__(self, model: str = "text-embedding-3"):
        """
        Initialize the DeepSeek embeddings class.

        Args:
            model (str): DeepSeek model to use for embeddings.
        """
        self.model = model
        self.endpoint = "https://api.deepseek.com/v1/embeddings"
        self.headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

    def _embed(self, texts):
        """
        Internal method to send request to DeepSeek API.

        Args:
            texts (list of str): Texts to embed.

        Returns:
            list of list of floats: Embedding vectors.
        """
        if isinstance(texts, str):
            texts = [texts]

        data = {
            "model": self.model,
            "input": texts
        }

        response = requests.post(self.endpoint, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(f"DeepSeek API error {response.status_code}: {response.text}")

        embeddings = [item["embedding"] for item in response.json()["data"]]
        return embeddings

    def embed_documents(self, texts):
        """
        Embed a list of documents.

        Args:
            texts (list of str): Documents to embed.

        Returns:
            list of list of floats: Embedding vectors.
        """
        return self._embed(texts)

    def embed_query(self, query):
        """
        Embed a single query.

        Args:
            query (str): Query text.

        Returns:
            list of floats: Embedding vector.
        """
        return self._embed(query)[0]


# =========================
# Example usage
# =========================
if __name__ == "__main__":
    texts = ["Hello, world!", "LangChain is awesome."]
    ds = DeepSeekEmbeddings()

    # Embed multiple documents
    vectors = ds.embed_documents(texts)
    print("Document embeddings:", vectors)

    # Embed a single query
    query_vector = ds.embed_query("Hello LangChain!")
    print("Query embedding:", query_vector)
