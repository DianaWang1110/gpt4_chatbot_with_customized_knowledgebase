# GPT-4 Chatbot with Customized Knowledge Base :rocket: :rocket: :rocket:

This repository contains the code for an interactive GPT-4 chatbot that integrates a customized knowledge base. The project includes functionalities for summarizing audio and video content, extracting text from websites and PDFs, embedding knowledge into vector databases (like Pinecone), and generating responses based on the embedded information. 

The system is built to handle multiple input formats, providing a flexible and intelligent chatbot experience.

## Features :star:

### Audio and Video Summary Module (`audio_video_summary/`)

This module provides functionalities for processing audio and video files, generating transcriptions, and creating summarized takeaways.

#### Key Components:
1. **Conversion (`conversion.py`)**: 
   - Converts video to audio (`video_to_audio()`) and formats audio files as needed (e.g., `mp3_to_wav()`).

2. **Summary Generation (`generate.py`)**: 
   - Uses OpenAI GPT to generate bulleted key takeaways from transcribed text. Supports multiple summarization methods like `map_reduce` and `refine`.

3. **Ingestion (`ingest.py`)**: 
   - Downloads video/audio from sources such as webinars (future support for platforms like Zoom).

4. **Transcription (`transcribe.py`)**: 
   - Transcribes audio using models like Whisper and Google Speech-to-Text. Can convert MP3s to text and generate transcripts for the chatbot.

---

### Website and PDF Interaction Module (`website_vectordb_query/`)

This module is designed to interact with websites, PDFs, and other text sources, extracting information and storing embeddings into a vector database for later use by the chatbot.

#### Key Components:
1. **Web Crawler (`crawler.py`)**: 
   - Automates the process of scraping text from websites using Selenium and undetected-chromedriver.

2. **PDF Processing (`gpt_helpers.py` & `main_functions.py`)**: 
   - Extracts text from PDF files and processes it for embedding using GPT models and Pinecone.

3. **Tokenization and Embedding (`tokenize_embedding_helpers.py`)**: 
   - Tokenizes extracted text and generates embeddings using GPT, storing them in Pinecone for fast retrieval.

4. **Pinecone Vector Database Interaction (`pinecone_storage.py` & `update_pinecone.py`)**: 
   - Stores and updates the embeddings in Pinecone for efficient knowledge retrieval by the chatbot.

5. **S3 Upload (`upload_s3.py`)**: 
   - Facilitates the upload of large documents or media to Amazon S3 for distributed access and storage.

---

## Installation :star: 

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/DianaWang1110/gpt4_chatbot_with_customized_knowledgebase.git
   cd gpt4_chatbot_with_customized_knowledgebase
2. **Install Dependencies:** Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   
  Required dependencies:
  numpy==1.25.0
  openai==0.27.8
  pandas==2.0.2
  selenium==4.9.1
  pinecone-client~=2.2.1
  undetected-chromedriver==3.5.0

3. **Set Environment Variables**: Set the API keys for both OpenAI and Pinecone.
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export PINECONE_API_KEY="your_pinecone_api_key"

 ---

  ## Usage :star: 
  ### Audio and Video Summarization
  Use the (`audio_video_summary`) module to convert, transcribe, and summarize audio/video files:

    
      from audio_video_summary.generate import generate_takeaways
      
      text = "Transcription text here"
      takeaways = generate_takeaways(text, combine_method="map_reduce")
      print(takeaways)

  ### Website and PDF Embedding
  Use the (`website_vectordb_query`) module to crawl websites or extract text from PDFs and embed the information into Pinecone:
   
   
    from website_vectordb_query.gpt_helpers import embed_pdf
    pdf_path = "/path/to/your/pdf"
    embed_pdf(pdf_path, pinecone_index="your_index_name")


  ### Chatbot Query
  Once the data is embedded, you can query the chatbot to get answers based on the embedded knowledge:

  ```bash
  from website_vectordb_query.main_functions import query_knowledgebase

  response = query_knowledgebase("What are the key takeaways from the document?")
  print(response)


  
