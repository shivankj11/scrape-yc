#!/usr/bin/env python3
"""
Functions to interface with YC API and Notion API
"""

from scrape_yc_batch import *
from dotenv import load_dotenv, find_dotenv
import os, sys, contextlib, io
import requests

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout

load_dotenv(find_dotenv())
NOTION_TOKEN = os.environ.get("NOTION_TOKEN")

headers = {
    'Authorization': f'Bearer {NOTION_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def create_db(page_id : str, batch_name : str) -> requests.Response:
    url = "https://api.notion.com/v1/databases"
    data = {
        "parent": {
            "type": "page_id",
            "page_id": page_id
        },
        "icon": {
            "type": "emoji",
            "emoji": "🟠"
        },
        "title": [
            {
            "type": "text",
            "text": {
                "content": "YC " + batch_name + " Batch",
                "link": None
            }
            }
        ],
        "is_inline": True,
        "properties": {
            "Name": {
                "title": {
                }
            },
            "Website": {
                "rich_text": {
                }
            },
            "YC Page": {
                "rich_text": {
                }
            },
            "Person": {
                "people" : {
                }
            },
            "Notes": {
                "rich_text": {
                }
            }
        }
    }

    response = requests.request("POST", url, json=data, headers=headers)
    response.raise_for_status()
    print("Successfully created database")
    return response


def load_db_pages(db_id : str) -> List[Dict[str, Any]]:
    url = f"https://api.notion.com/v1/databases/{db_id}/query"

    print("Loading database pages...")
    data = {
        "page_size": 100,
    }
    response = requests.request("POST", url, json=data, headers=headers)
    response.raise_for_status()
    page_data = response.json()['results']
    while response.json()['has_more']:
        data['start_cursor'] = response.json()['next_cursor']
        response = requests.request("POST", url, json=data, headers=headers)
        response.raise_for_status()
        page_data.extend(response.json()['results'])

    print("Successfully loaded database pages")
    return page_data


def add_page_to_db(db_id : str, company : Dict) -> None:
    url = "https://api.notion.com/v1/pages"
    data = {
        "parent": { "database_id": db_id },
        "properties": {
            "Name": {
                "title": [
                    {
                    "text": {
                        "content": company['name']
                    }
                    }
                ]
            },
            "Website": {
                "rich_text": [
                    {
                    "text": {
                        "content": company['website']
                    }
                    }
                ]
            },
            "YC Page": {
                "rich_text": [
                    {
                    "text": {
                        "content": company['yc page']
                    }
                    }
                ]
            },
        },
    }
    response = requests.request("POST", url, json=data, headers=headers)
    response.raise_for_status()


def update_db(db_id : str, batch_name : str) -> None:
    """
        Scrapes batch data from YC API and updates given Notion database
    """
    # get companies already existing in database
    present = load_db_pages(db_id)
    present_names = set()
    for v in present:
        try:
            present_names.add(v['properties']['Name']['title'][0]['plain_text'])
        except:
            continue

    # get fresh batch data
    print("Scraping YC Batch Data...")
    with nostdout():
        batch_data = scrape_batch(batch_name)
    print("Successfully scraped YC Batch Data")
    new_batch_data = [c for c in batch_data if c['name'] not in present_names]
    print(f"{len(new_batch_data)} new companies:", new_batch_data)

    # update database with any new visible companies
    print("Adding batch data to database...")
    company_ct = len(new_batch_data)
    for i, company in enumerate(new_batch_data):
        add_page_to_db(db_id, company)
        print("Progress: " + str(i + 1) + "/" + str(company_ct), end="\r")
    
    print("Successfully added all batch data to database")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape YC companies by batch')
    parser.add_argument('--batch', type=str, required=True, help='Batch name (e.g., "Spring 2025", "Fall 2024", etc.)')
    parser.add_argument('--page_id', type=str, required=True, help='Page ID of the Notion page to add the database to')
    parser.add_argument('--update_db', type=str, default=False, help='Update existing Notion database with fresh batch data')
    args = parser.parse_args()

    if args.update_db:
        db_id = args.update_db
    else:
        response = create_db(args.page_id, args.batch)
        db_id = response.json()['id']

    update_db(db_id, args.batch)
