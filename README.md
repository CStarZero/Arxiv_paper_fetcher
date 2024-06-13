
# arXiv Paper Fetcher

## Overview
This script fetches research papers from the arXiv repository based on a keyword search, downloads the PDFs of these papers, extracts the text from the PDFs, and saves the collected data into a CSV file.

## Dependencies
The script requires the following Python libraries:
- `requests`: For making HTTP requests.
- `BeautifulSoup` from `bs4`: For parsing XML data.
- `fitz` (from `PyMuPDF`): For extracting text from PDFs.
- `os`: For file operations.
- `pandas`: For data manipulation and saving to a CSV file.

You can install the dependencies using pip:
\`\`\`bash
pip install requests beautifulsoup4 pymupdf pandas
\`\`\`

## Functions

### `get_arxiv_papers(keyword, max_results=50)`
Fetches research papers from arXiv based on a keyword search.

**Parameters:**
- `keyword` (str): The search term to use for querying arXiv.
- `max_results` (int, optional): The maximum number of results to fetch. Default is 50.

**Returns:**
- `papers` (list of dict): A list of dictionaries, each containing the title, summary, and PDF link of a paper.

### `download_pdf(pdf_url, save_path)`
Downloads a PDF file from a given URL.

**Parameters:**
- `pdf_url` (str): The URL of the PDF to download.
- `save_path` (str): The local path to save the downloaded PDF.

### `extract_text_from_pdf(pdf_path)`
Extracts text from a PDF file.

**Parameters:**
- `pdf_path` (str): The path to the PDF file.

**Returns:**
- `text` (str): The extracted text from the PDF.

## Usage Example

### Define Keyword and Fetch Papers
\`\`\`python
keyword = "european+space+agency+remote+sensing+earth+observation"
papers = get_arxiv_papers(keyword)
\`\`\`

### Process Each Paper
\`\`\`python
data = []

for i, paper in enumerate(papers, 1):
    print(f"Paper {i}: {paper['title']}")
    print(f"Summary: {paper['summary']}")
    print(f"PDF Link: {paper['pdf_link']}")

    pdf_filename = f"paper_{i}.pdf"
    download_pdf(paper['pdf_link'], pdf_filename)
    text_content = extract_text_from_pdf(pdf_filename)

    print(f"Content of Paper {i}:
{text_content[:500]}...")  # Display the first 500 characters
    print("-" * 80)

    data.append({
        'title': paper['title'],
        'summary': paper['summary'],
        'pdf_link': paper['pdf_link'],
        'content': text_content
    })

    # Optionally, clean up by removing the downloaded PDF
    os.remove(pdf_filename)
\`\`\`

### Save Data to CSV
\`\`\`python
df = pd.DataFrame(data)
df.to_csv('arxiv_papers.csv', index=False)
\`\`\`

## Script Execution
When the script is executed, it performs the following steps:
1. Searches for papers on arXiv using the specified keyword.
2. Downloads the PDF of each paper.
3. Extracts the text content from each PDF.
4. Prints a summary and a portion of the content of each paper.
5. Saves the collected data (title, summary, PDF link, and content) into a CSV file named `arxiv_papers.csv`.

