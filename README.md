# Boliviamart Web Scraper

A Python web scraper designed to extract product information from Boliviamart.com and save it to a CSV file.

## Features

- ✅ Scrapes all products from paginated pages
- ✅ Automatically handles pagination (maximum 32 products per page)
- ✅ Extracts comprehensive product information:
  - Product ID and SKU
  - Title and categories
  - Regular price and sale price
  - Discount percentage
  - Stock status
  - Rating
  - Featured/Hot status
  - Product URL and image URL
- ✅ Exports data to CSV format
- ✅ Respectful scraping with configurable delays
- ✅ Error handling and logging
- ✅ Command-line interface

## Requirements

- Python 3.7 or higher
- Required packages (see requirements.txt):
  - requests
  - beautifulsoup4
  - lxml

## Installation

1. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests beautifulsoup4 lxml
```

## Usage

### Basic Usage

Scrape the default Boliviamart store page:

```bash
python scraper_boliviamart.py
```

### Custom URL

Scrape a specific URL:

```bash
python scraper_boliviamart.py https://www.boliviamart.com/tienda/
```

### Output

The scraper will create a CSV file named `boliviamart_products.csv` with the following columns:

- `product_id` - Product ID
- `sku` - Stock Keeping Unit
- `title` - Product title/name
- `categories` - Product categories (comma-separated)
- `regular_price` - Regular price (Bs.)
- `sale_price` - Sale price (Bs.)
- `on_sale` - Whether product is on sale (Yes/No)
- `discount` - Discount percentage
- `stock_status` - Stock availability (In Stock/Out of Stock)
- `rating` - Product rating (0-5)
- `featured` - Whether product is featured (Yes/No)
- `url` - Product page URL
- `image_url` - Product image URL

## Configuration

You can modify the scraper behavior by editing the `BoliviamartScraper` initialization in the `main()` function:

```python
scraper = BoliviamartScraper(
    base_url=url,
    page_size=32,      # Products per page (max 32)
    delay=1.0          # Delay between requests in seconds
)
```

### Parameters:

- **page_size**: Number of products to display per page (1-32, default: 32)
  - Maximum value is 32 as per website limitations
  - Higher values reduce total number of requests
  
- **delay**: Time to wait between page requests in seconds (default: 1.0)
  - Increase this value if you encounter rate limiting
  - Recommended: 1.0-2.0 seconds for respectful scraping

## Examples

### Example 1: Scrape with default settings

```bash
python scraper_boliviamart.py
```

Output:
```
2024-11-12 10:30:00 - INFO - Starting Boliviamart scraper for: https://www.boliviamart.com/tienda/
2024-11-12 10:30:00 - INFO - Fetching: https://www.boliviamart.com/tienda/?count=32
2024-11-12 10:30:01 - INFO - Total pages to scrape: 2
2024-11-12 10:30:01 - INFO - Scraping page 1/2
2024-11-12 10:30:01 - INFO - Found 32 products on page
2024-11-12 10:30:02 - INFO - Scraping page 2/2
2024-11-12 10:30:02 - INFO - Found 32 products on page
2024-11-12 10:30:02 - INFO - Total products scraped: 64
2024-11-12 10:30:02 - INFO - Successfully saved 64 products to boliviamart_products.csv
```

### Example 2: Scrape specific category

```bash
python scraper_boliviamart.py https://www.boliviamart.com/categoria/seguridad/
```

## CSV Output Sample

```csv
product_id,sku,title,categories,regular_price,sale_price,on_sale,discount,stock_status,rating,featured,url,image_url
2570,5YBM1A,ACCESO CON LECTOR BIOMETRICO 5Y0A 5YBM1A,"Controles de Acceso, Seguridad",475.00,475.00,No,N/A,In Stock,0,No,https://www.boliviamart.com/producto/acceso-con-lector-biometrico-5y0a-5ybm1a/,https://www.boliviamart.com/wp-content/uploads/2020/11/5yoa5ybm1a.jpg
2575,SOS Alert,ALARMA PERSONAL SOS ALERT 130 dB,"Accesorios, Seguridad",135.00,130.00,Yes,-4%,In Stock,0,No,https://www.boliviamart.com/producto/alarma-personal-sos-alert-130-db/,https://www.boliviamart.com/wp-content/uploads/2020/11/alarma.jpg
```

## Features Breakdown

### Automatic Pagination Handling

The scraper automatically:
1. Detects total number of pages
2. Sets page size to maximum (32 products)
3. Iterates through all pages
4. Combines results into single CSV

### Price Extraction

Handles multiple price formats:
- Regular prices
- Sale prices
- Discount percentages
- Price ranges for variable products

### Stock Status Detection

Identifies:
- In stock products
- Out of stock products
- Featured/hot items

### Error Handling

- Request timeouts
- Network errors
- Parsing errors
- Missing data fields

## Logging

The scraper provides detailed logging:
- INFO: Progress updates
- WARNING: Non-critical issues
- ERROR: Critical errors

Logs are printed to console during execution.

## Best Practices

1. **Respect the website**: Use reasonable delays (1-2 seconds) between requests
2. **Run during off-peak hours**: Minimize impact on server
3. **Don't scrape too frequently**: Cache results and avoid unnecessary re-scraping
4. **Check robots.txt**: Ensure compliance with website's scraping policy
5. **Monitor for changes**: Website structure may change; update scraper accordingly

## Troubleshooting

### No products found

- Check if the URL is correct
- Verify the website is accessible
- Website structure may have changed

### Connection errors

- Check internet connection
- Increase delay between requests
- Website may be blocking automated requests

### Missing data in CSV

- Some products may not have all fields
- Fields marked as 'N/A' indicate missing data
- Check website source for data availability

## Legal and Ethical Considerations

- This scraper is for educational purposes
- Always respect website's Terms of Service
- Check and follow robots.txt guidelines
- Don't overload servers with excessive requests
- Use scraped data responsibly and legally

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please check the code comments or modify the scraper according to your needs.
