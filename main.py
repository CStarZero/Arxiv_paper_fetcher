import requests
from bs4 import BeautifulSoup
import fitz
import os
import pandas as pd

def get_arxiv_papers(keyword, max_results=50):
    url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}&start=0&max_results={max_results}"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from arXiv. Status code: {response.status_code}")

    soup = BeautifulSoup(response.content, 'xml')
    entries = soup.find_all('entry')

    papers = []
    for entry in entries:
        title = entry.title.text.strip()
        summary = entry.summary.text.strip()
        pdf_link = entry.find('link', title='pdf')['href']
        papers.append({'title': title, 'summary': summary, 'pdf_link': pdf_link})

    return papers


def download_pdf(pdf_url, save_path):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        raise Exception(f"Failed to download PDF. Status code: {response.status_code}")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

# Example usage:
keyword = "european+space+agency+remote+sensing+earth+observation"
papers = get_arxiv_papers(keyword)

data = []

for i, paper in enumerate(papers, 1):
    print(f"Paper {i}: {paper['title']}")
    print(f"Summary: {paper['summary']}")
    print(f"PDF Link: {paper['pdf_link']}")

    pdf_filename = f"paper_{i}.pdf"
    download_pdf(paper['pdf_link'], pdf_filename)
    text_content = extract_text_from_pdf(pdf_filename)

    print(f"Content of Paper {i}:\n{text_content[:500]}...")  # Display the first 500 characters
    print("-" * 80)

    data.append({
        'title': paper['title'],
        'summary': paper['summary'],
        'pdf_link': paper['pdf_link'],
        'content': text_content
    })

    # Optionally, clean up by removing the downloaded PDF
    os.remove(pdf_filename)

# Creating a DataFrame from the collected data
df = pd.DataFrame(data)

# Saving the DataFrame to a CSV file
df.to_csv('arxiv_papers.csv', index=False)
