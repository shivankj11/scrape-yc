# scrape-yc

### Functionalities
1. Scrape YC batch data from YC API and save it to a CSV file
2. Create a Notion database in a Notion page and add YC companies from the given batch
3. Update an existing Notion database with fresh batch data


## Usage

```bash
git clone https://github.com/shivankj11/scrape-yc
```

### Arguments
`--batch`  (Required)  Name of the YC batch (e.g., "Spring 2025", "Fall 2024", etc.)

`--page_id` (Required) Notion page ID where the database will be created

`--update_db` (Optional) Notion database ID to update with fresh batch data

### Examples
Scraping data from a YC batch and saving it to a CSV file:
```bash
python3 scrape_yc_batch.py --batch "Spring 2025" -o "spring_2025.csv"
```

Creating a Database in a Notion page and dumping batch info into it:
```bash
python3 batch_to_notion.py --batch "Spring 2025" --page_id "<page_id>"
```

Loading an existing Database in a Notion page and dumping batch info into it:
```bash
python3 batch_to_notion.py --batch "Spring 2025" --page_id "<page_id>" --update_db "<db_id>"
```

## Scraping Script Output

- A CSV file with the following columns:
    1. name
    2. website
    3. yc page

- Console output

## Notion Script Output

- A Database in a Notion page with the following columns:
    1. name
    2. website
    3. yc page

- Console output:
    1. Progress tracking
    2. Names of all added startups

## Requirements

`requests`