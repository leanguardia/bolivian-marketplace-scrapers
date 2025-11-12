# Quick Start Guide - Boliviamart Web Scraper

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Scraper

```bash
python scraper_boliviamart.py
```

That's it! The scraper will:
- Automatically scrape all products from https://www.boliviamart.com/tienda/
- Handle pagination (max 32 products per page)
- Save results to `boliviamart_products.csv`

## 📊 Expected Output

```
2024-11-12 10:30:00 - INFO - Starting Boliviamart scraper
2024-11-12 10:30:00 - INFO - Fetching: https://www.boliviamart.com/tienda/?count=32
2024-11-12 10:30:01 - INFO - Total pages to scrape: 2
2024-11-12 10:30:01 - INFO - Scraping page 1/2
2024-11-12 10:30:01 - INFO - Found 32 products on page
2024-11-12 10:30:02 - INFO - Scraping page 2/2
2024-11-12 10:30:02 - INFO - Found 32 products on page
2024-11-12 10:30:02 - INFO - Total products scraped: 64
2024-11-12 10:30:02 - INFO - Successfully saved 64 products to boliviamart_products.csv
```

## 🎯 Common Use Cases

### Scrape Specific Category

```bash
python scraper_boliviamart.py https://www.boliviamart.com/categoria/seguridad/
```

### Test the Scraper (without full scrape)

```bash
python test_scraper.py
```

### See Examples

```bash
python example_usage.py
```

## 📁 Output File Structure

The CSV file will contain:

| Column | Description |
|--------|-------------|
| product_id | Unique product identifier |
| sku | Stock Keeping Unit |
| title | Product name |
| categories | Product categories |
| regular_price | Original price (Bs.) |
| sale_price | Current/sale price (Bs.) |
| on_sale | Whether on sale (Yes/No) |
| discount | Discount percentage |
| stock_status | In Stock / Out of Stock |
| rating | Product rating (0-5) |
| featured | Featured status (Yes/No) |
| url | Product page URL |
| image_url | Product image URL |

## 🔧 Customization

Edit `scraper_boliviamart.py` line 442:

```python
scraper = BoliviamartScraper(
    base_url=url,
    page_size=32,      # 1-32 products per page
    delay=1.0          # Seconds between requests
)
```

## ⚠️ Important Notes

1. **Page Size Limit**: Maximum 32 products per page (website limitation)
2. **Respect the Website**: 1-second delay between requests is recommended
3. **Total Products**: If page size = 32 and max page = 2, expect ~64 products
4. **Stock Status**: Some products may be out of stock
5. **Data Quality**: Some fields may be "N/A" if not available

## 🐛 Troubleshooting

### Problem: No products found
**Solution**: Check URL, website may be down or structure changed

### Problem: Connection timeout
**Solution**: Check internet connection, increase delay parameter

### Problem: Missing data in CSV
**Solution**: Some products don't have all fields, this is normal

## 📚 More Information

See `README.md` for complete documentation.

## ✅ Validation

Before running a full scrape, validate the scraper:

```bash
python test_scraper.py
```

This will run 4 tests:
1. ✓ Connection Test
2. ✓ Product Extraction Test  
3. ✓ Pagination Detection Test
4. ✓ CSV Export Test

If all tests pass, you're ready to scrape!

## 💡 Tips

- Run during off-peak hours to minimize server load
- Start with test script to verify everything works
- Check output CSV file to ensure data quality
- Don't run too frequently - cache results when possible
- Increase delay if you encounter rate limiting

---

**Need Help?** Check the full README.md for detailed documentation.
