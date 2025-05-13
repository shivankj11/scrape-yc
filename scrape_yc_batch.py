import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import re
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
    'Referer': 'https://www.ycombinator.com',
    'Accept-Language': 'en-US,en;q=0.9'
}

def scrape_batch(batch : str) -> List[Dict[str, Any]]:
    data = []

    page = 0
    while True:
        response = requests.get(f'https://api.ycombinator.com/v0.1/companies?batch={batch}&page={page}', headers=headers)
        response.raise_for_status()
        page_data = response.json()

        print(f"Batch {batch} Page {page_data['page'] + 1} of {page_data['totalPages']}")

        for company in page_data['companies']:
            try:
                html = requests.get(company['website'], headers=headers)
                html_text = html.text
                githubs = re.findall(r'github.com\/[-A-Za-z0-9_./]+', html_text)
                # print(f"{company['name']}, {company['website']}, {company['url']}, [{'|'.join(githubs)}]")
                data.append({
                    'name': company['name'],
                    'website': company['website'],
                    'url': company['url'],
                    'githubs': githubs
                })
            except Exception as e:
                # print(f"{company['name']}, {company['website']} #SITEDOWN, {company['url']}, []")
                data.append({
                    'name': company['name'],
                    'website': company['website'],
                    'url': company['url'],
                    'githubs': []
                })

        if 'nextPage' not in page_data or page_data['nextPage'] is None:
            break
        else:
            page += 1
        
    return data

def write_sheet(batch : str, data : List[Dict[str, Any]]) -> None:
    if len(data) == 0:
        print('No data to write')
        return

    with open(f"{batch}.csv", 'w', newline='') as filename:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(filename, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data written to {batch}.csv")    

if __name__ == '__main__':
    batch = input('Enter batch name: ')
    batch_data = scrape_batch(batch)

    write_sheet(batch, batch_data)