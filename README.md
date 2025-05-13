# scrape-yc

Scrape YC batch data from YC API and save it to a CSV file.

## Usage

```bash
python3 scrape_yc_batch.py
```
Enter batch name when prompted (eg. 'Spring 2025')

## Output

1. Print statement for each page of companies scraped from YC API

2. a CSV file with the following columns:
- name
- website
- url
- githubs

## Requirements

`requests`