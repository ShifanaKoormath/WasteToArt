from sentence_transformers import SentenceTransformer

sbert = SentenceTransformer("all-MiniLM-L6-v2")

def get_text_embedding(text):
    return sbert.encode(text)
