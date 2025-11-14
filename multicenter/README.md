# Multicenter Category Scraper

Web scraper for extracting product counts from Multicenter's main product categories.

## Overview

This scraper navigates through Multicenter's category menu and extracts the total product count for each main category. It uses Selenium to handle JavaScript-rendered content.

## Features

- Scrapes all main categories from **Navidad** through **Bebés**
- Excludes promotional sections (Black Friday, Solo X hoy, Ofertas del Mes, Combos)
- Outputs results to both console and CSV file
- Handles JavaScript-rendered content using Selenium WebDriver

## Main Categories Scraped

- Navidad
- Electrohogar
- Muebles
- Electrónica
- Camping
- Deportes
- Hogar y Deco
- Jardín
- Juguetes
- Ferretería
- Bebés

## Installation

### Prerequisites

- Python 3.7+
- Chrome browser installed
- ChromeDriver (will be managed automatically by Selenium 4.6+)

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Run the Full Scraper

```bash
python scraper_multicenter.py
```

This will:
1. Open each main category page
2. Extract the product count
3. Print results to console
4. Save results to `multicenter_categories_report.csv`

### Run Test Script

Test with a single category first:

```bash
python test_scraper.py
```

## Output

### Console Output

The scraper prints:
- Progress for each category
- Summary table with product counts
- Total products across all categories

Example:
```
============================================================
SCRAPING SUMMARY
============================================================

Categories scraped: 11
Total products found: 5,432

Breakdown by category:
------------------------------------------------------------
  Muebles              498 products
  Electrohogar         856 products
  Electrónica          723 products
  ...
============================================================
```

### CSV Output

Results are saved to `multicenter_categories_report.csv`:

```csv
category_name,product_count,url,scraped_at
Navidad,245,https://www.multicenter.com/navidad,2024-11-13T10:30:00
Electrohogar,856,https://www.multicenter.com/electrohogar,2024-11-13T10:30:15
...
```

## Technical Details

### Website Structure

- **Platform**: VTEX e-commerce platform
- **Category Pages**: `https://www.multicenter.com/{category-slug}`
- **Product Count Location**: Rendered via JavaScript, typically shows as "X productos"

### Scraping Method

1. Opens homepage using Selenium
2. Clicks menu button to reveal category sidebar
3. Extracts category links from menu
4. Visits each category page
5. Waits for JavaScript to render product count
6. Extracts count using regex patterns
7. Saves results to CSV

### Rate Limiting

- 2-3 second delays between requests
- Respectful crawling to avoid overloading the server

## Troubleshooting

### ChromeDriver Issues

If you encounter ChromeDriver errors:

```bash
# Install/update ChromeDriver manually
brew install chromedriver  # macOS
```

Or ensure Chrome browser is up to date.

### No Product Count Found

If product counts are not extracted:
- Check if the website structure has changed
- Run with `headless=False` to see what the browser sees
- Verify the category URL is correct

### Timeout Errors

Increase wait times in the script if pages load slowly:
```python
time.sleep(5)  # Instead of 3
```

## Files

- `scraper_multicenter.py` - Main scraper script
- `test_scraper.py` - Test script for single category
- `requirements.txt` - Python dependencies
- `multicenter_categories_report.csv` - Output file (generated)

## Notes

- The scraper focuses only on main categories as requested
- Subcategories are not scraped since main categories show total counts
- The scraper respects robots.txt and uses reasonable delays

## License

This scraper is for educational and research purposes only.
