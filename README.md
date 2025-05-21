# scrape-yc

Scrape YC batch data from YC API and save it to a CSV file.

## Usage

```bash
pip install scrape-yc-batch
scrape-yc-batch --batch "Spring 2025" -o "spring_2025.csv"
```

Or, an example calling the script directly:
```bash
python3 scrape_yc_batch.py --batch "Spring 2025" -o "spring_2025.csv"
```

## Output

1. Print statement for each page of companies scraped from YC API

2. A CSV file with the following columns:
- name
- website
- url of yc page

## Requirements

`requests`