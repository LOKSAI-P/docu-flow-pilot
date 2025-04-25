
# tGPT Backend

This folder contains the backend code for the Team Guidance and Productive Tool (tGPT) with the following components:

1. **Search Results - AI Assistant**: Semantic search and QA for Confluence pages
2. **Sample Data Generator**: JSON/XML record generator using templates
3. **AI Meeting Summarizer**: Convert meeting audio/text to summaries
4. **NFR Capture & Testing Strategy Assistant**: NFR tracking and documentation

## Integration with Frontend

The backend services are designed to be called from the React frontend using API endpoints.

## Key Technologies
- FAISS for vector similarity search
- SentenceTransformers for embeddings
- HuggingFace Transformers for QA models
- Confluence REST API integration
- Whisper for audio transcription
- BART for text summarization
- Jinja2 templating for data generation
