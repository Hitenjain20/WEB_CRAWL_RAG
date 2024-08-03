import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import hashlib
import nltk
from textblob import TextBlob
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Download necessary NLTK data files
nltk.download('punkt')


def get_text_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def clean_text(text):
    # Remove special characters and extra spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    return text.strip()


def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())


def crawl(start_url, max_depth):
    visited = set()
    queue = [(start_url, 0)]
    crawled_data = {}
    non_crawlable_links = set()
    unique_paragraphs = set()

    while queue:
        url, depth = queue.pop(0)

        if url not in visited and depth <= max_depth:
            try:
                response = requests.get(url)
                html = response.text
                visited.add(url)

                soup = BeautifulSoup(html, 'html.parser')

                # Extract main title
                title = soup.title.string if soup.title else 'No Title'

                # Extract paragraphs
                paragraphs = soup.find_all('p')
                full_paragraph = ' '.join([para.get_text() for para in paragraphs])
                clean_para = clean_text(full_paragraph)
                correct_para = correct_spelling(clean_para)
                para_hash = get_text_hash(correct_para)

                if para_hash not in unique_paragraphs:
                    unique_paragraphs.add(para_hash)
                    crawled_data[url] = {'title': title, 'paragraph': correct_para}

                if depth < max_depth:
                    for link in soup.find_all('a', href=True):
                        absolute_link = urljoin(url, link['href'])
                        if absolute_link not in visited:
                            queue.append((absolute_link, depth + 1))

                print(f"Crawled: {url}")

            except requests.RequestException as e:
                print(f"Failed to fetch {url}: {str(e)}")
                non_crawlable_links.add(url)

            # Optional delay to avoid overloading the server
            time.sleep(1)

        # Optional break condition for demonstration
        if len(visited) >= 24:
            break

    return crawled_data, non_crawlable_links


def save_to_pdf(crawled_data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    text = c.beginText(40, height - 40)
    text.setFont("Helvetica", 12)

    for url, data in crawled_data.items():
        text.setFont("Helvetica-Bold", 12)
        text.textLine(f"URL: {url}")
        text.setFont("Helvetica-Oblique", 12)
        text.textLine(f"Title: {data['title']}")
        text.setFont("Helvetica", 12)
        text.textLines(f"Paragraph: {data['paragraph']}\n")
        text.textLine("\n")

    c.drawText(text)
    c.save()


start_url = "https://pratham.org/"
max_depth = 1
crawled_data, non_crawlable_links = crawl(start_url, max_depth)

# Save cleaned data to a PDF file
pdf_filename = 'cleaned_crawled_data.pdf'
save_to_pdf(crawled_data, pdf_filename)

# Save non-crawlable links to a text file
with open('non_crawlable_links.txt', 'w', encoding='utf-8') as text_file:
    for url in non_crawlable_links:
        text_file.write(f"Non-crawlable URL: {url}\n")

print('*********************************************')
print("Crawled URLs:", len(crawled_data))
print("Non-crawlable URLs:", len(non_crawlable_links))
print('*********************************************')
