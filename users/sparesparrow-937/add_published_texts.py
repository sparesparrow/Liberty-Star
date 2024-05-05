import requests
from bs4 import BeautifulSoup
from markdown2 import markdown
import os

def fetch_new_publications(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    publications = []

    # Assuming each publication is in a specific table or div
    for entry in soup.find_all('tr'):
        date = entry.find('td').text.strip()
        title = entry.find('a').text.strip()
        link = entry.find('a')['href']
        publications.append((date, title, link))
    return publications

def download_text(url, filename):
    response = requests.get(url)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(response.text)

def update_markdown_file(publications, md_file_path):
    if not os.path.exists(md_file_path):
        with open(md_file_path, 'w', encoding='utf-8') as file:
            file.write("# Published Texts\n\n")

    with open(md_file_path, 'a', encoding='utf-8') as file:
        for date, title, link in publications:
            markdown_entry = f"* [{date} {title}]({link})\n"
            file.write(markdown_entry)

def main():
    url = 'https://stoky.urza.cz/autori/sparesparrow-937'
    md_file_path = 'published_texts.md'

    publications = fetch_new_publications(url)
    for date, title, link in publications:
        filename = f"{title.replace(' ', '_')}.txt"
        download_text(link, filename)
    update_markdown_file(publications, md_file_path)

if __name__ == "__main__":
    main()
