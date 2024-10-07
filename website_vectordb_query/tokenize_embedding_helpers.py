import tiktoken
import os
import pandas as pd
from website_vectordb_query.constants import *


# Remove newlines from text
def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


# Create a dataframe from text files and remove newlines
def process_text(domain):
    texts = []

    # Get all the text files in the text directory
    for file in os.listdir("./text/" + domain + "/"):
        # Open the file and read the text
        with open("./text/" + domain + "/" + file, "r") as f:
            text = f.read()

            # Omit the first 11 lines and the last 4 lines, then replace -, _, and #update with spaces.
            texts.append((file[11:-4].replace('-', ' ').replace('_', ' ').replace('#update', ''), text))

    # Create a dataframe from the list of texts
    df = pd.DataFrame(texts, columns=['fname', 'text'])

    # Set the text column to be the raw text with the newlines removed
    df['text'] = df.fname + ". " + remove_newlines(df.text)
    df.to_csv("./processed/" + domain + "scraped.csv")
    print(df.head())


# Use openAI's tokenizer to split the text into tokens
def tokenize(domain):
    # Load the cl100k_base tokenizer which is designed to work with the ada-002 model
    tokenizer = tiktoken.get_encoding("cl100k_base")

    df = pd.read_csv("./processed/" + domain + "scraped.csv", index_col=0)
    df.columns = ['title', 'text']

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))

    return tokenizer, df


# Split tokens into chunks
def split_into_many(text, tokenizer, max_tokens=MAX_TOKENS):
    # Split the text into sentences
    sentences = text.split('. ')

    # Get the number of tokens for each sentence
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]

    chunks = []
    tokens_so_far = 0
    chunk = []

    # Loop through the sentences and tokens joined together in a tuple
    for sentence, token in zip(sentences, n_tokens):

        # If the number of tokens so far plus the number of tokens in the current sentence is greater
        # than the max number of tokens, then add the chunk to the list of chunks and reset
        # the chunk and tokens so far
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0

        # If the number of tokens in the current sentence is greater than the max number of
        # tokens, go to the next sentence
        if token > max_tokens:
            continue

        # Otherwise, add the sentence to the chunk and add the number of tokens to the total
        chunk.append(sentence)
        tokens_so_far += token + 1

    return chunks


# Split text in dataframe into chunks of tokens
def split_tokens_df(df, tokenizer, max_tokens=MAX_TOKENS):
    shortened = []

    # Loop through the dataframe
    for row in df.iterrows():

        # If the text is None, go to the next row
        if row[1]['text'] is None:
            continue

        # If the number of tokens is greater than the max number of tokens, split the text into chunks
        if row[1]['n_tokens'] > max_tokens:
            text_chunks = split_into_many(row[1]['text'], tokenizer)
            shortened.extend([{'title': row[1]['title'], 'text': chunk} for chunk in text_chunks])

        # Otherwise, add the text, title to the list of shortened texts
        else:
            shortened.append({'title': row[1]['title'], 'text': row[1]['text']})

    df = pd.DataFrame(shortened, columns=['title', 'text'])
    df['n_tokens'] = df.text.apply(lambda x: len(tokenizer.encode(x)))
    return df


# Create embeddings from the text that has been broken into chunks of tokens
def create_df_embeddings(domain, df, openai_key):
    openai.api_key = openai_key
    succeeded = False
    for i in range(100):
        try:
            df['embeddings'] = df.text.apply(
                lambda x: openai.Embedding.create(input=x, engine='text-embedding-ada-002')['data'][0]['embedding'])
        except Exception as e:
            print(e)
            continue
        else:
            succeeded = True
            break
    if not succeeded:
        print("Couldn't connect to OpenAI server. Please try again later")
        return df
    df.to_csv("./processed/" + domain + "embeddings.csv")
    print(df.head())
    return df


# Process all the text files, tokenize, split into chunks, and create embeddings
def create_embeddings_from_text(domain, openai_key):
    process_text(domain)
    tokenizer, df = tokenize(domain)
    df = split_tokens_df(df=df, tokenizer=tokenizer)
    df = create_df_embeddings(domain, df, openai_key)
    return df


