# website_vectordb_query

## Current Functionality:

### website_to_vectordb_storage: 
#### Description:
def website_to_vectordb_storage(full_url, index_name, pdf_download_path, namespace, openai_key, vectordb="pinecone", force_crawl=False, limit=LIMIT, driver=None):
This process only needs to be done once per website+vectordb unless the website has been updated. Given the full url of a website, the crawler will store the full contents as a text file, then open the same-domain urls that are linked, store the contents of those pages and so on. The crawler currently uses selenium's undetected chromedriver in order to bypass Cloudflare protection and similar issues. Next, process and tokenize (using openAI's tiktoken) the stored text and combine tokens into chunks. Then we use openAI's model ada to embed the text. Finally, we store the embeddings in a vector database. Currently only pinecone is supported.

#### Parameters:
full_url: Full url of a website, eg https://www.egnyte.com/. 

vector_db: Name of the vector database to use (case insensitive). Defaults to pinecone - currently only pinecone storage is implemented.

namespace: Name of the namespace to create or update, usually the name of the company. 

openai_key: Your openai api key

pdf_download_path: Name of your downloads folder. Chromedriver has to download pdfs to this folder before we can extract text from them.

force_crawl: Defaults to false - won't run the crawler if there is already a local text directory for the domain unless force_crawl is true. 

limit: Limit to the iterations the crawler will run. Defaults to 100

driver: Custom chromedriver you can pass in

#### Example Usage:
I was unable to get this to work on a colab notebook due to a problem with passing the chrome executable file to undetected-chromedriver. However, I am able to run this in a local python file like so:
```
from website_vectordb_query.main_functions import *
full_url = "https://www.snowflake.com/en/"
index_name = "websites"
namespace = "snowflake
pdf_download_path = "/Users/saigopinath/Downloads"
website_to_vectordb_storage(full_url, index_name, pdf_download_path, namespace, openai_key)
```
Note: Renamed the index name egnyte -> websites.

Then you can navigate to the pinecone website and verify that the namespace has been created in the index.


### create_augmented_query_vectordb:

#### Description:
def create_augmented_query_vectordb(index_name, namespace, query, openai_key, vectordb="pinecone"):
Given the index name, namespace, query, your openai key, and vector database, search the database index for similar context to the query. Then append that context to the query and return it. This is a replacement for having to finetune a model on all the website's data before generating a response. 

#### Example Usage:
https://colab.research.google.com/drive/1eQUjFa3INWrNZQi2-8unZocr6LjWB_ZV?usp=sharing

### create_augmented_query_local:
#### Description: 
create_augmented_query_local(domain, query, max_len=500, size="ada"):
Given the domain name and query, search the corresponding local dataframe for similar context to the query (based on cosine similarity). Then append that context to the query and return it. 


### test_augmented_query:
#### Description:
def test_augmented_query(augmented_query, system_msg, openai_key):
Given an augmented_query (from a create_augmented_query function) and a system message, feed them into OpenAI's GPT-4 model and generate a response. 

#### Example Usage:
https://colab.research.google.com/drive/1eQUjFa3INWrNZQi2-8unZocr6LjWB_ZV?usp=sharing


## Todos:

1.) More test cases

2.) Ingest video and audio

3.) Improve parsing while crawling so storage and search is more efficient. The AI seems to already do a good job at figuring out what is
most important when searching for similar contexts and generating text, but the current method of just storing pretty much everything could lead to issues later. 

4.) Add support for updating. Instead of having to complete the whole crawling job again, we should be able to just update the vectordb with a few urls that have been changed. 
