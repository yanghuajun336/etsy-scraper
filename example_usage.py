# Example Usage of Etsy Scraper

This file contains complete usage examples for the Etsy Scraper in various scenarios.

## 1. Basic Usage
```python
from etsy_scraper import EtsyScraper

# Create an instance of the scraper
scraper = EtsyScraper()

# Scrape data from the default URL
results = scraper.scrape()
print(results)
```

## 2. Individual Elements
```python
from etsy_scraper import EtsyScraper

# Create an instance of the scraper
scraper = EtsyScraper()

# Scrape a specific item
results = scraper.scrape_item('item_id')
print(results)
```

## 3. List Selectors
```python
from etsy_scraper import EtsyScraper

# Create an instance of the scraper
scraper = EtsyScraper()

# Get items from a specific category
results = scraper.scrape_category('category_name')
print(results)
```

## 4. Multiple URLs
```python
from etsy_scraper import EtsyScraper

# Create an instance of the scraper
scraper = EtsyScraper()

# Scrape multiple URLs
urls = ['url1', 'url2', 'url3']
results = scraper.scrape_urls(urls)
print(results)
```

## 5. Attribute Extraction
```python
from etsy_scraper import EtsyScraper

# Create an instance of the scraper
scraper = EtsyScraper()

# Scrape specific attributes
results = scraper.extract_attributes(['title', 'price', 'rating'])
print(results)
```