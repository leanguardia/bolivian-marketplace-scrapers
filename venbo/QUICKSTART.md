# Venbo Scraper - Quick Start Guide

## 🚀 Quick Start (3 steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Test the scraper (optional but recommended)
```bash
python test_scraper.py
```

This will verify:
- ✓ Can access Venbo.shop
- ✓ Can detect category pages
- ✓ Can extract product information
- ✓ Multi-level category navigation works

### 3. Run the scraper
```bash
python scraper_venbo.py
```

This will:
- Explore all categories recursively
- Extract products from each category
- Save results to `venbo_products.csv`
- Generate a report in `venbo_categories_report.txt`

## 📊 Expected Results

The scraper will visit all category URLs like:
- `https://venbo.shop/cat-producto/alimentacion/`
- `https://venbo.shop/cat-producto/alimentacion/aperitivos/`
- `https://venbo.shop/cat-producto/informatica-oficina/informatica-laptops/`
- etc.

### Sample Output

```
================================================================================
Starting Venbo scraper
Base URL: https://venbo.shop
================================================================================
Found 50 main category links

Exploring: https://venbo.shop/cat-producto/alimentacion/
→ This is a CATEGORY NAVIGATION page
→ Found 7 subcategory links
  Exploring: https://venbo.shop/cat-producto/alimentacion/aperitivos/
  → This is a PRODUCT LISTING page
  → Found 15 products in this category
...

================================================================================
Scraping completed
Total categories with products found: 42
Total products scraped: 1,234
================================================================================
```

## 📁 Output Files

### 1. venbo_products.csv
Contains all products with these columns:
- `product_id` - Unique product ID
- `title` - Product name
- `url` - Product page URL
- `regular_price` - Original price (Bs)
- `sale_price` - Discounted price (Bs)
- `on_sale` - Yes/No
- `discount` - Discount percentage
- `in_stock` - Stock status
- `image_url` - Product image URL
- `category_url` - Category where found

### 2. venbo_categories_report.txt
Shows category hierarchy with product counts:
```
[15 products] https://venbo.shop/cat-producto/alimentacion/aperitivos/
[8 products] https://venbo.shop/cat-producto/alimentacion/cereales-frutos-secos-y-semillas/
  [4 products] https://venbo.shop/cat-producto/informatica-oficina/informatica-laptops/
```

## ⏱️ How Long Will It Take?

With default settings (1.5 second delay between requests):
- Estimated time: **20-40 minutes** (depends on number of categories)
- This is intentionally slow to be respectful to the server

To speed up (not recommended for production):
```python
# In scraper_venbo.py, change:
scraper = VenboScraper(base_url="https://venbo.shop", delay=0.5)  # Faster
```

## 🔍 Monitoring Progress

The scraper logs detailed progress:
- URL being visited
- Whether it's a category or product listing page
- Number of products found
- Number of subcategories discovered

Watch the console output to monitor progress.

## ❓ Common Issues

### No products found
- Check internet connection
- Verify Venbo.shop is accessible
- Run test_scraper.py first

### Slow performance
- Normal! The default delay is 1.5 seconds per request
- This prevents overloading the server
- Can reduce delay if needed (see above)

### Connection errors
- Increase delay between requests
- Check if site is blocking automated requests
- Try again later

## 🎯 What Gets Scraped

The scraper will find and extract products from ALL categories, including:
- Alimentación / Bebidas
- Artesanías
- Bioseguridad
- Bricolaje y herramientas
- Cine y TV / Música / Fotos
- Electrónica
- Hogar / Jardín / Mascotas
- Informática / Oficina
- Juguetes e infantil
- Libros / Cómics
- Moda
- Papelería
- Reservas en línea
- Salud y belleza
- Servicios profesionales
- Suministros industriales

And all their subcategories!

## 📝 Need Help?

See the full README.md for:
- Detailed documentation
- Configuration options
- Troubleshooting guide
- Technical details
