import requests
from typing import List, Dict, Any
import csv
import argparse

headers = {
    'Referer': 'https://www.ycombinator.com',
    'Accept-Language': 'en-US,en'
}

baseurl = "https://api.ycombinator.com/v0.1/companies"

def scrape_batch(batch : str) -> List[Dict[str, Any]]:
    """
    Scrape the batch data from YC API and return it as a list of dict with keys 'name', 'website', 'yc page'
    
    Args:
        batch: The batch name to search for

    Returns:
        List of dict with keys 'name', 'website', 'yc page'
    """
    data = []
    page_ct = 0

    while page_ct == 0 or 'nextPage' in page_data:
        pageurl = f"{baseurl}?batch={batch}&page={page_ct}"
        response = requests.get(pageurl, headers=headers)
        response.raise_for_status()

        page_data = response.json()
        print(f"Progress: {page_data['page'] + 1}/{page_data['totalPages']}\n\tPage: {pageurl}")

        for company in page_data['companies']:
            data.append({
                'name': company['name'],
                'website': company['website'],
                'yc page': company['url'],
            })

        page_ct += 1
        
    return data


def write_sheet(data: List[Dict[str, Any]], filename: str) -> None:
    """
    Write the data to a CSV file named 'filename' in the cwd
    
    Args:
        filename: The output CSV filename
        data: list of dict with keys 'name', 'website', 'yc page'

    Returns:
        None
    """
    if len(data) == 0:
        print('No data to write')
        return

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Data written to {filename}")    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape YC companies by batch')
    parser.add_argument('--batch', type=str, required=True, help='Batch name (e.g., "Spring 2025", "Fall 2024", etc.)')
    parser.add_argument('-o', type=str, default=None, help='Output CSV filename (optional)')
    args = parser.parse_args()
    batch_data = scrape_batch(args.batch)
    write_sheet(batch_data, filename=args.batch if args.o is None else args.o)
