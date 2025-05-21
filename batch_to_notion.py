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
        }
    }

    response = requests.request("POST", url, json=data, headers=headers)
    response.raise_for_status()
    print("Successfully created database")
    return response


def add_batch_to_db(db_id : str, batch_data : List):
    url = "https://api.notion.com/v1/pages"

    print("Adding batch data to database...")
    company_ct = len(batch_data)
    for i, company in enumerate(batch_data):
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
        print("Progress: " + str(i + 1) + "/" + str(company_ct), end="\r")
    
    print("Successfully added all batch data to database")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape YC companies by batch')
    parser.add_argument('--batch', type=str, required=True, help='Batch name (e.g., "Spring 2025", "Fall 2024", etc.)')
    parser.add_argument('--page_id', type=str, required=True, help='Page ID of the Notion page to add the database to')
    args = parser.parse_args()

    response = create_db(args.page_id, args.batch)
    db_id = response.json()['id']

    print("Scraping YC Batch Data...")
    with nostdout():
        batch_data = scrape_batch(args.batch)
    print("Successfully scraped YC Batch Data")
    
    add_batch_to_db(db_id, batch_data)
