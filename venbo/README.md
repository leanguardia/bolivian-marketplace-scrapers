# Venbo Web Scraper

A Python web scraper for extracting product information from [Venbo.shop](https://venbo.shop), a Bolivian e-commerce marketplace.

## Features

- **Recursive Category Traversal**: Automatically navigates through the multi-level category tree
- **Product Detection**: Identifies product listing pages by looking for "Showing all X results" text
- **Product Information Extraction**: Extracts:
  - Product ID
  - Title
  - URL
  - Regular price
  - Sale price
  - Discount percentage
  - Stock status
  - Image URL
  - Category URL
- **CSV Export**: Saves all products to a CSV file
- **Category Report**: Generates a text report showing all categories and their product counts
- **Smart URL Management**: Avoids visiting the same URL twice
- **Progress Logging**: Detailed logging of the scraping progress

## Installation

1. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Simply run the scraper:

```bash
python scraper_venbo.py
```

The scraper will:
1. Start from https://venbo.shop/categorias/
2. Extract all category links
3. Recursively explore each category and subcategory
4. Identify product listing pages
5. Scrape products from each listing page
6. Save results to CSV and generate a report

### Output Files

After running, you'll get two files:

1. **venbo_products.csv**: Contains all scraped products with columns:
   - `product_id`: Unique product identifier
   - `title`: Product name
   - `url`: Product page URL
   - `regular_price`: Original price in Bs
   - `sale_price`: Discounted price (if on sale)
   - `on_sale`: Yes/No indicator
   - `discount`: Discount percentage
   - `in_stock`: Stock availability
   - `image_url`: Product image URL
   - `category_url`: Category where the product was found

2. **venbo_categories_report.txt**: A hierarchical report showing:
   - All categories explored
   - Number of products in each category
   - Category tree structure

## How It Works

### Category Tree Navigation

The scraper uses a recursive approach to navigate the category tree:

1. **Start**: Begins at `/categorias/` page
2. **Extract Links**: Finds all links matching `/cat-producto/...` pattern
3. **Identify Page Type**: Checks if page contains "Showing all X results"
   - If YES → It's a product listing page, scrape products
   - If NO → It's a category navigation page, continue exploring
4. **Recurse**: For each page, extract more category links and repeat

### Example Category Structure

```
Alimentación / Bebidas
  ├── Aperitivos [15 products]
  ├── Cereales, frutos secos y semillas [8 products]
  └── Chocolates y dulces [23 products]

Artesanías
  ├── Cerámica [12 products]
  └── Textil [5 products]

Informática / Oficina
  ├── Almacenamiento [7 products]
  └── Laptops [4 products]
```

### Product Detection

A page is identified as a product listing page if it contains:
- Text matching "Showing all X results"
- OR a `<p class="woocommerce-result-count">` element

## Configuration

You can customize the scraper by modifying parameters in `main()`:

```python
scraper = VenboScraper(
    base_url="https://venbo.shop",  # Base URL
    delay=1.5                         # Delay between requests (seconds)
)
```

### Delay Between Requests

The default delay is 1.5 seconds. You can adjust this:
- **Lower delay** (e.g., 0.5): Faster scraping, but may overload the server
- **Higher delay** (e.g., 2.0): Slower but more respectful to the server

## Troubleshooting

### No products found

If the scraper reports 0 products:
1. Check your internet connection
2. Verify the website is accessible
3. The website structure may have changed

### Incomplete results

If some categories are missing:
1. Increase the `delay` parameter
2. Check the logs for error messages
3. Some categories may not have products

### Request errors

If you see timeout or connection errors:
- Increase the delay between requests
- Check if the website is blocking automated requests
- Try running at a different time

## Technical Details

### Dependencies

- **requests**: HTTP library for making web requests
- **beautifulsoup4**: HTML parsing library
- **lxml**: Fast XML/HTML parser (used by BeautifulSoup)

### URL Pattern

Venbo uses the following URL structure for categories:
```
https://venbo.shop/cat-producto/{category-name}/
https://venbo.shop/cat-producto/{parent}/{child}/
https://venbo.shop/cat-producto/{parent}/{child}/{grandchild}/
```

Example:
```
https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-generos/drama/
```

### Product HTML Structure

Products are contained in elements with classes:
- `product` (WooCommerce standard)
- `kad_product` (Virtue theme specific)

## Example Output

### Console Output
```
================================================================================
Starting Venbo scraper
Base URL: https://venbo.shop
================================================================================
Fetching: https://venbo.shop/categorias/
Found 50 main category links

================================================================================
Main Category 1/50
================================================================================
Exploring: https://venbo.shop/cat-producto/alimentacion/
→ This is a CATEGORY NAVIGATION page
→ Found 7 subcategory links
  Exploring: https://venbo.shop/cat-producto/alimentacion/aperitivos/
  → This is a PRODUCT LISTING page
  → Found 15 products in this category
  Found 15 products on https://venbo.shop/cat-producto/alimentacion/aperitivos/
...

================================================================================
Scraping completed
Total categories with products found: 42
Total products scraped: 1,234
================================================================================
```

### CSV Sample
```csv
product_id,title,url,regular_price,sale_price,on_sale,discount,in_stock,image_url,category_url
83829,Flor de sal Salar de Uyuni,https://venbo.shop/productos/...,17.50,17.50,No,N/A,Yes,https://venbo.shop/wp-content/...,https://venbo.shop/cat-producto/alimentacion/conservas/
```

## License

This scraper is for educational purposes. Please respect Venbo's terms of service and robots.txt when using this tool.

## Contributing

Feel free to submit issues or pull requests if you find bugs or have improvements to suggest.
