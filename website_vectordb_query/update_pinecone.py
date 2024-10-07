from constants import *
import pinecone

pinecone.deployment.api_key = pinecone_api_key

def update_pinecone(link, title, content_type):
    if content_type == 'pdf':
        
