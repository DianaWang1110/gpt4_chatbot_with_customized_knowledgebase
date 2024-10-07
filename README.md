GPT-4 Chatbot with Customized Knowledge Base

This repository contains the code for an interactive GPT-4 chatbot that integrates a customized knowledge base. The project includes functionalities for summarizing audio and video content, extracting text from websites and PDFs, embedding knowledge into vector databases (like Pinecone), and generating responses based on the embedded information.

The system is built to handle multiple input formats, providing a flexible and intelligent chatbot experience.

Features

Audio and Video Summary Module (audio_video_summary/)
This module provides functionalities for processing audio and video files, generating transcriptions, and creating summarized takeaways.

Key Components:

Conversion (conversion.py):
Converts video to audio (video_to_audio()) and formats audio files as needed (e.g., mp3_to_wav()).
Summary Generation (generate.py):
Uses OpenAI GPT to generate bulleted key takeaways from transcribed text. Supports multiple summarization methods like map_reduce and refine.
Ingestion (ingest.py):
Downloads video/audio from sources such as webinars (future support for platforms like Zoom).
Transcription (transcribe.py):
Transcribes audio using models like Whisper and Google Speech-to-Text. Can convert MP3s to text and generate transcripts for the chatbot.
Website and PDF Interaction Module (website_vectordb_query/)
This module is designed to interact with websites, PDFs, and other text sources, extracting information and storing embeddings into a vector database for later use by the chatbot.

Key Components:

Web Crawler (crawler.py):
Automates the process of scraping text from websites using Selenium and undetected-chromedriver.
PDF Processing (gpt_helpers.py & main_functions.py):
Extracts text from PDF files and processes it for embedding using GPT models and Pinecone.
Tokenization and Embedding (tokenize_embedding_helpers.py):
Tokenizes extracted text and generates embeddings using GPT, storing them in Pinecone for fast retrieval.
Pinecone Vector Database Interaction (pinecone_storage.py & update_pinecone.py):
Stores and updates the embeddings in Pinecone for efficient knowledge retrieval by the chatbot.
S3 Upload (upload_s3.py):
Facilitates the upload of large documents or media to Amazon S3 for distributed access and storage.
Installation

Clone the Repository:
bash
Copy code
git clone https://github.com/DianaWang1110/gpt4_chatbot_with_customized_knowledgebase.git
cd gpt4_chatbot_with_customized_knowledgebase
Install Dependencies: Install the required Python packages by running:
bash
Copy code
pip install -r requirements.txt
Required dependencies:

plaintext
Copy code
numpy==1.25.0
openai==0.27.8
pandas==2.0.2
selenium==4.9.1
pinecone-client~=2.2.1
undetected-chromedriver==3.5.0
Additional tools (optional):

Tiktoken: For tokenization support
Langchain: For advanced language model integrations
Set Environment Variables: You will need to set the API keys for both OpenAI and Pinecone.
bash
Copy code
export OPENAI_API_KEY="your_openai_api_key"
export PINECONE_API_KEY="your_pinecone_api_key"
Usage

Audio and Video Summarization
Use the audio_video_summary module to convert, transcribe, and summarize audio/video files:

Example:

python
Copy code
from audio_video_summary.generate import generate_takeaways

text = "Transcription text here"
takeaways = generate_takeaways(text, combine_method="map_reduce")
print(takeaways)
Website and PDF Embedding
Use the website_vectordb_query module to crawl websites or extract text from PDFs and embed the information into Pinecone:

Example:

python
Copy code
from website_vectordb_query.gpt_helpers import embed_pdf

pdf_path = "/path/to/your/pdf"
embed_pdf(pdf_path, pinecone_index="your_index_name")
Chatbot Query
Once the data is embedded, you can query the chatbot to get answers based on the embedded knowledge:

Example:

python
Copy code
from website_vectordb_query.main_functions import query_knowledgebase

response = query_knowledgebase("What are the key takeaways from the document?")
print(response)
Future Enhancements

Full implementation of additional media formats and summarization techniques.
Advanced conversational capabilities for handling complex queries over embedded knowledge.
Support for more data sources like YouTube, Zoom, and others.
Enhanced error handling and performance optimization.
