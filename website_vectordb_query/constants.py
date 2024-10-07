import openai

# CRAWLER CONSTANTS

# Regex pattern to match a URL
HTTP_URL_PATTERN = r'^http[s]*://.+'

# Add user agent header to requests to bypass bot detection
"""
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
HEADER = {
    "user-agent": USER_AGENT,
    'referer': 'https://www.google.com/'
}"""
# Add blacklist to filter out unwanted pages
BLACKLIST = ["tel:", "blog", "press-releases", "jpg", "png", "jpeg", "heic", "tiff", "bmp", "events",
             "mobile-nav", "login"]

# Add limit to cap crawler to x most relevant links
LIMIT = 100


# TOKENIZER CONSTANTS

# Max tokens that each chunk of text should be split into
MAX_TOKENS = 500

# API KEYS
PINECONE_API_KEY = '84676f32-638f-4453-aea4-31b6cfad030b'
PINECONE_API_ENV = 'us-central1-gcp'

# GENERATION
EMBED_MODEL = "text-embedding-ada-002"
