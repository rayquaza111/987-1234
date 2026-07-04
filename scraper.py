import os
import re
import requests
import logging
from markdownify import markdownify as md

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text)
    return text.strip('-')

def scrape_articles():
    if not os.path.exists('articles'):
        os.makedirs('articles')
        
    logging.info("Fetching data from Zendesk API...")
    response = requests.get(URL)
    
    if response.status_code != 200:
        logging.error(f"Failed to fetch articles. HTTP Status: {response.status_code}")
        return

    data = response.json()
    articles_list = data.get('articles', [])
    
    target_count = min(30, len(articles_list))
    logging.info(f"Syncing top {target_count} articles...")

    for i in range(target_count):
        article = articles_list[i]
        title = article.get('title')
        html_body = article.get('body')
        
        if not html_body:
            continue
            
        markdown_content = md(html_body, heading_style="ATX")
        slug = slugify(title)
        file_path = f"articles/{slug}.md"
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(f"# {title}\n\n")
            file.write(markdown_content)
            
        logging.info(f"Saved markdown: {file_path}")

if __name__ == "__main__":
    scrape_articles()