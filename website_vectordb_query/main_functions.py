from website_vectordb_query.crawler import *
from website_vectordb_query.pinecone_storage import *
from website_vectordb_query.gpt_helpers import *
from website_vectordb_query.tokenize_embedding_helpers import *
from website_vectordb_query.constants import *
import pandas as pd
import numpy as np



# Given a website, scrape the top limit (default 100) urls, get embeddings, and store them in a vector database
# We don't need to run this multiple times if the website has not been updated
def website_to_vectordb_storage(full_url, index_name, namespace, openai_key, vectordb="pinecone", force_crawl=False, limit=LIMIT, driver=None):
    domain = urlparse(full_url).netloc

    if not os.path.exists("text/" + domain + "/") or force_crawl:
        crawl(full_url, limit, driver)

    # Uses GPT-ada to create embeddings
    df = create_embeddings_from_text(domain, openai_key)

    # Currently only pinecone storage is implemented
    if vectordb.lower() == "pinecone":
        index = store_embeddings_pinecone(df=df, index_name=index_name, namespace=namespace)
        return index
    else:
        print(vectordb + " is not yet supported")
        return None


# Given a query, combine it with similar context from vector database. Instead of fine-tuning a complex model,
# we can just provide the relevant context alongside user input.
def create_augmented_query_vectordb(index_name, namespace, query, openai_key, vectordb="pinecone"):
    if vectordb.lower() == "pinecone":
        augmented_query = create_query_with_pinecone_context(index_name=index_name, namespace=namespace, query=query, openai_key=openai_key)
        return augmented_query
    else:
        print(vectordb + " is not yet supported")
        return None


# Given an augmented query generated from the previous function, use gpt-4 to generate an
# answer to the user input and relevant context
def test_augmented_query(augmented_query, system_msg, openai_key):
    # Unfortunately, openai often returns a server error and we need to try multiple times.
    succeeded = False
    for i in range(100):
        try:
            response = generate(augmented_query, system_msg, openai_key)
        except:
            continue
        else:
            succeeded = True
            break
    if not succeeded:
        print("Unable to connect to openai server")
        return None
    return response

