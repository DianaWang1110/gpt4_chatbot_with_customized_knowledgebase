import pinecone
from uuid import uuid4
from website_vectordb_query.constants import *
from tqdm.auto import tqdm


# After embeddings have been generated, store them into pinecone w unique index name
def store_embeddings_pinecone(df, index_name, namespace):
    # Add an 'id' column to the DataFrame
    df['id'] = [str(uuid4()) for _ in range(len(df))]

    # Fill null values in 'title' column with 'No Title'
    df['title'] = df['title'].fillna('No Title')

    # Initialize connection to Pinecone
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_API_ENV)

    # Check if index already exists, create it if it doesn't
    if index_name not in pinecone.list_indexes():
        pinecone.create_index(index_name, dimension=1536, metric='dotproduct')

    # Connect to the index
    index = pinecone.Index(index_name)

    batch_size = 100  # how many embeddings we create and insert at once

    # Convert the DataFrame to a list of dictionaries
    chunks = df.to_dict(orient='records')

    # Upsert embeddings into Pinecone in batches of 100
    for i in tqdm(range(0, len(chunks), batch_size)):
        i_end = min(len(chunks), i + batch_size)
        meta_batch = chunks[i:i_end]
        ids_batch = [x['id'] for x in meta_batch]
        embeds = [x['embeddings'] for x in meta_batch]
        meta_batch = [{
            'title': x['title'],
            'text': x['text']
        } for x in meta_batch]
        to_upsert = list(zip(ids_batch, embeds, meta_batch))
        index.upsert(vectors=to_upsert, namespace=namespace)

    return index
