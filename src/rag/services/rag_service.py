
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

class RagService:
    def __init__(self,  db_name: str):
        self.db_name = db_name

        
    def search(self, query: str, k: int = 10):
        embedding = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-large"
        )
        
        db = FAISS.load_local(
            f"resources/vectorstores/{self.db_name}", 
            embedding,
            allow_dangerous_deserialization=True)
        
        docs = db.similarity_search_with_relevance_scores(query, k=k)
        
        combined_content = "\n\n".join([doc.page_content for doc, score in docs])
        
        return combined_content

    
    