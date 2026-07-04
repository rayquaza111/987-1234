import os
import re
import glob
import time
import logging
from dotenv import load_dotenv
from google import genai
from scraper import scrape_articles 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STORE_DISPLAY_NAME = "OptiSigns Knowledge Base"
SOURCE_DIR = "articles/*.md"

def get_or_create_store(client):
    for store in client.file_search_stores.list():
        if store.display_name == STORE_DISPLAY_NAME:
            return store.name
            
    logging.info(f"Store '{STORE_DISPLAY_NAME}' not found. Initializing a new RAG store.")
    return client.file_search_stores.create(config={"display_name": STORE_DISPLAY_NAME}).name

def get_cloud_state(client, store_name):
    """
    Builds a dictionary of what is currently live inside the specific Vector Store.
    """
    cloud_map = {}
    try:
        # check the Vector Store directly
        for doc in client.file_search_stores.documents.list(parent=store_name):
            
            # the name comes back as a path (e.g., 'fileSearchStores/123/documents/abc'). 
            # in Gemini RAG, the original filename is usually preserved in the name or display_name field depending on the upload method.
            doc_identifier = getattr(doc, 'display_name', doc.name)
            
            match = re.search(r"(.+)_([a-zA-Z0-9]+)\.md", doc_identifier)
            if match:
                slug, timestamp = match.groups()
                cloud_map[slug] = {
                    "id": doc.name, 
                    "timestamp": timestamp
                }
    except Exception as e:
        logging.warning(f"Could not read Vector Store state (It might be empty): {e}")
        
    return cloud_map

def sync_vector_store():
    load_dotenv(dotenv_path=".env")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("CRITICAL: Missing GEMINI_API_KEY.")

    client = genai.Client(api_key=api_key)
    store_name = get_or_create_store(client)
    
    logging.info("Retrieving active cloud state for delta comparison...")
    
    # pass the store_name into the state function 
    cloud_map = get_cloud_state(client, store_name)
    
    local_files = glob.glob(SOURCE_DIR)
    stats = {"added": 0, "updated": 0, "skipped": 0}

    for path in local_files:
        filename = os.path.basename(path)
        match = re.match(r"^(.+)_([a-zA-Z0-9]+)\.md$", filename)
        
        if not match:
            continue
            
        local_slug, local_timestamp = match.groups()

        if local_slug in cloud_map:
            if cloud_map[local_slug]["timestamp"] == local_timestamp:
                stats["skipped"] += 1
            else:
                logging.info(f"[~] Updating: {local_slug}...")
                try:
                    # delete the old document out of the Vector Store
                    client.file_search_stores.documents.delete(name=cloud_map[local_slug]["id"])
                    
                    # upload the new one
                    client.file_search_stores.upload_to_file_search_store(
                        file_search_store_name=store_name,
                        file=path
                    )
                    stats["updated"] += 1
                    time.sleep(1) 
                except Exception as e:
                    logging.error(f"Update failed for {local_slug}: {e}")
        else:
            logging.info(f"[+] Adding: {local_slug}...")
            try:
                client.file_search_stores.upload_to_file_search_store(
                    file_search_store_name=store_name,
                    file=path
                )
                stats["added"] += 1
                time.sleep(1)
            except Exception as e:
                logging.error(f"Add failed for {local_slug}: {e}")

    print("\n================ DAILY JOB LOGS ================")
    print(f"Added: {stats['added']}, Updated: {stats['updated']}, Skipped: {stats['skipped']}")
    print("================================================\n")

def main():
    logging.info("--- STARTING DAILY SYNC JOB ---")
    scrape_articles()
    sync_vector_store()
    logging.info("--- JOB COMPLETED SUCCESSFULLY ---")

if __name__ == "__main__":
    main()