# scrape-yc

Scrape YC batch data from YC API and save it to a CSV file.

## Usage

```bash
git clone https://github.com/shivankj11/scrape-yc
python3 .../scrape_yc_batch.py --batch <batch_name> -o <filename.csv>
```

Example (calling the script directly):
```bash
python3 scrape_yc_batch.py --batch "Spring 2025" -o "spring_2025.csv"
```

Example (creating a Database in a Notion page and dumping batch info into it):
```bash
python3 batch_to_notion.py --batch "Spring 2025" --page_id "<page_id>"
```

## 1. Scraping Script Output

1. A CSV file with the following columns:
- name
- website
- yc page

2. Console output

## 2. Notion Script Output

1. A Database in a Notion page with the following columns:
- name
- website
- yc page

2. Console output

## Requirements

`requests`