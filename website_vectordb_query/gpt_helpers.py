import openai
import pinecone
from website_vectordb_query.tokenize_embedding_helpers import *
from website_vectordb_query.constants import *


# Take user query as input, search the pinecone index for relevant context, and combine context with query
def create_query_with_pinecone_context(index_name, namespace, query, openai_key):
    openai.api_key = openai_key
    embed_query = openai.Embedding.create(
        input=query,
        engine=EMBED_MODEL
    )
    query_embeds = embed_query['data'][0]['embedding']

    # Initialize connection to Pinecone
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)
    index = pinecone.Index(index_name)

    # Get relevant contexts (including the questions) from pinecone
    response = index.query(query_embeds, top_k=5, include_metadata=True, namespace=namespace)

    contexts = [item['metadata']['text'] for item in response['matches']]

    augmented_query = "\n\n---\n\n".join(contexts) + "\n\n-----\n\n" + query

    return augmented_query


# Take augmented query and generate a response using gpt-4
def generate(augmented_query, system_msg, openai_key):
    openai.api_key = openai_key
    chat = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": augmented_query}
        ]
    )
    result = chat['choices'][0]['message']['content']
    #print(result)
    return result


