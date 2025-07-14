
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document # Import the Document class
from langchain_community.vectorstores import FAISS
import os

class RagBuilderService:
    def __init__(self, markdown: str, db_name: str):
        self.markdown = markdown
        self.db_name = db_name
    
    def create_rag_db(self):
        chunks = self.chunk_markdown(self.markdown)
        
        embeddings = OpenAIEmbeddings(
            openai_api_key = os.getenv("OPENAI_API_KEY"),  # Ensure you have set your OpenAI API key in the environment variables
            model = "text-embedding-3-large" # Specify the embedding model to use
        )
        
        documents = [Document(page_content=chunk['text'], metadata=chunk['metadata']) for chunk in chunks]

        # Create the FAISS index from the documents using the embeddings
        db_faiss = FAISS.from_documents(documents, embeddings)
        
        db_faiss.save_local(f"resources/vectorstores/{self.db_name}")
        
    def search(self, query: str, db_name: str, k: int = 10):
        db = FAISS.load_local(f"resources/vectorstores/{db_name}", OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-large"
        ))
        
        docs = db.similarity_search_with_relevance_scores(query, k=k)
        
        combined_content = "\n\n".join([doc.page_content for doc, score in docs])
        
        return combined_content

    
    def chunk_markdown(self, markdown_text: str) -> list:
        # First split by headers
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ("####", "Header 4"),
            ("#####", "Header 5"),
            ("######", "Header 6"),
        ]

        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False
        )

        md_header_splits = markdown_splitter.split_text(markdown_text)

        chunks = []
        for doc in md_header_splits:
            chunks.append({
                'text': doc.page_content,
                'metadata': doc.metadata
            })

        return chunks
    
    