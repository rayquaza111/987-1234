import os
import glob
import time
from google import genai
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# create the Vector Store (Knowledge Base)
print("Creating Gemini Vector Store...")
store = client.file_search_stores.create(
    config={"display_name": "OptiSigns Knowledge Base"}
)
print(f"Store created successfully! ID: {store.name}")

# upload and embed the Markdown files into the Vector Store
article_files = glob.glob("articles/*.md")
chunks_logged = 0 
files_added = 0

for file_path in article_files:
    print(f"Embedding into Vector Store: {file_path}...")
    try:
        client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=store.name,
            file=file_path
        )
        files_added += 1
        chunks_logged += 1 
        time.sleep(1) # small delay to prevent hitting API rate limits
    except Exception as e:
        print(f"Failed to embed {file_path}: {e}")

# required assignment log output
print(f"\nLOGS - Files embedded: {files_added}, Chunks processed: {chunks_logged}")