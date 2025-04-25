
"""
Search Results - AI Assistant
Provides semantic search over Confluence pages and QA-based answers.
"""
import os
import requests
import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

class SearchService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.qa_tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.qa_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.index = None
        self.pages = []
        self.page_embeddings = None

    def fetch_confluence_pages(self, base_url, space_key, auth_token):
        """Fetch pages from Confluence using REST API"""
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }
        
        url = f"{base_url}/rest/api/content?spaceKey={space_key}&limit=100&expand=body.storage"
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            self.pages = []
            
            for page in data.get('results', []):
                page_id = page.get('id')
                title = page.get('title', '')
                content = page.get('body', {}).get('storage', {}).get('value', '')
                
                # Simple HTML to text conversion (can be improved)
                content = content.replace('<p>', ' ').replace('</p>', ' ')
                content = ' '.join(content.split())
                
                self.pages.append({
                    'id': page_id,
                    'title': title,
                    'content': content,
                    'url': f"{base_url}/wiki/spaces/{space_key}/pages/{page_id}"
                })
            
            # Create embeddings for all fetched pages
            self._create_embeddings()
            
            return {"status": "success", "message": f"Fetched {len(self.pages)} pages"}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _create_embeddings(self):
        """Create embeddings for all the page content"""
        if not self.pages:
            return
        
        # Create embeddings for each page
        texts = [f"{page['title']} {page['content']}" for page in self.pages]
        self.page_embeddings = self.embedding_model.encode(texts)
        
        # Create FAISS index
        embedding_dim = self.page_embeddings.shape[1]
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.index.add(np.array(self.page_embeddings).astype('float32'))

    def search(self, query, top_k=5):
        """Search for relevant pages using semantic search"""
        if not self.index or not self.pages:
            return {"status": "error", "message": "No pages indexed"}
        
        # Get query embedding
        query_embedding = self.embedding_model.encode([query])
        
        # Search in FAISS index
        distances, indices = self.index.search(np.array(query_embedding).astype('float32'), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.pages):
                page = self.pages[idx]
                results.append({
                    "title": page["title"],
                    "snippet": page["content"][:200] + "...",
                    "url": page["url"],
                    "relevance_score": float(1 / (1 + distances[0][i]))
                })
        
        return {"status": "success", "results": results}

    def answer_question(self, question, context):
        """Generate an answer using the FLAN-T5 model"""
        try:
            input_text = f"question: {question} context: {context}"
            inputs = self.qa_tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True)
            
            outputs = self.qa_model.generate(
                inputs.input_ids,
                max_length=100,
                min_length=30,
                do_sample=False,
                num_beams=4,
            )
            
            answer = self.qa_tokenizer.decode(outputs[0], skip_special_tokens=True)
            return {"status": "success", "answer": answer}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
