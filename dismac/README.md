# Dismac Category Scraper

A Python web scraper that recursively crawls through Dismac's multi-level category hierarchy and reports the number of products in each category.

## Features

- **Recursive Category Traversal**: Navigates through main categories, subcategories, and sub-subcategories
- **Product Count Extraction**: Accurately extracts product counts from listing pages
- **CSV Export**: Saves results in structured CSV format
- **Progress Tracking**: Real-time console logging with visual hierarchy
- **Summary Statistics**: Provides overview and top categories report
- **Respectful Scraping**: Implements delays between requests

## Installation

### Requirements

```bash
pip install requests beautifulsoup4
```

Or install from requirements file:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper:

```bash
python scraper_dismac.py
```

This will:
1. Fetch the main categories page
2. Extract all categories (levels 1-3)
3. Visit each category to count products
4. Save results to `dismac_categories_report.csv`
5. Print summary statistics

### Test the Scraper

Before running the full scraper, you can test it:

```bash
python test_scraper.py
```

### Output Files

- **dismac_categories_report.csv**: Complete report with all categories and product counts

## CSV Output Format

The generated CSV file contains the following columns:

| Column | Description |
|--------|-------------|
| `category_name` | Name of the category |
| `level` | Hierarchy level (1=main, 2=sub, 3=sub-sub) |
| `parent` | Parent category name(s) |
| `url` | Full URL to the category page |
| `product_count` | Number of products in this category |
| `scraped_at` | Timestamp when data was collected |

### Example Output

```csv
category_name,level,parent,url,product_count,scraped_at
Línea Blanca,1,,https://www.dismac.com.bo/categorias/50-linea-blanca.html,0,2025-11-12T10:30:00
Refrigeradores,2,Línea Blanca,https://www.dismac.com.bo/categorias/50-linea-blanca/101-refrigeradores.html,125,2025-11-12T10:30:15
Frigobares y cavas,3,Línea Blanca > Refrigeradores,https://www.dismac.com.bo/categorias/50-linea-blanca/101-refrigeradores/frigobares-y-cavas.html,23,2025-11-12T10:30:30
```

## How It Works

### 1. Category Structure Extraction

The scraper parses the main categories page (`/categorias.html`) which contains a hierarchical structure:

```html
<header class="childs-categories-header">
    <h3>Línea Blanca</h3>
    <a href="/categorias/50-linea-blanca.html">Ver categoría completa</a>
</header>
<div class="childs-categories-body">
    <div class="childs-categories-group">
        <a href="/categorias/50-linea-blanca/101-refrigeradores.html">
            <span>Refrigeradores</span>
        </a>
        <ul class="grandchild-categories-list">
            <li><a href="...">Frigobares y cavas</a></li>
        </ul>
    </div>
</div>
```

### 2. Product Count Detection

The scraper identifies product listing pages by looking for:

1. **Page Title Indicator**:
```html
<div class="page-title-wrapper">
    <span class="page-title">Dormitorio</span>
</div>
```

2. **Product Count in JavaScript**:
```javascript
let htmlCount = "44 Productos";
```

3. **Or in HTML Container**:
```html
<div class="container-count-items">
    <span class="count-number">44 Productos</span>
</div>
```

### 3. Category Levels

- **Level 1**: Main categories (e.g., "Línea Blanca", "Hogar")
- **Level 2**: Subcategories (e.g., "Refrigeradores", "Lavadoras")  
- **Level 3**: Sub-subcategories (e.g., "Frigobares y cavas", "Lavadoras")

## Console Output Example

```
================================================================================
DISMAC CATEGORY SCRAPER
================================================================================
Starting scrape at: 2025-11-12 10:30:00
Categories URL: https://www.dismac.com.bo/categorias.html
================================================================================

Extracting category structure...
Found 156 categories to process

Processing categories:
--------------------------------------------------------------------------------
[1/156] Processing: Línea Blanca
Fetching: https://www.dismac.com.bo/categorias/50-linea-blanca.html
○ Línea Blanca: No product listing page

[2/156] Processing: Refrigeradores
Fetching: https://www.dismac.com.bo/categorias/50-linea-blanca/101-refrigeradores.html
  ✓ Refrigeradores: 125 productos

[3/156] Processing: Frigobares y cavas
Fetching: https://www.dismac.com.bo/categorias/50-linea-blanca/101-refrigeradores/frigobares-y-cavas.html
    ✓ Frigobares y cavas: 23 productos

...

================================================================================
SUMMARY
================================================================================
Total categories processed: 156
Categories with products: 98
Total products found: 3,847

Top 10 categories by product count:
--------------------------------------------------------------------------------
 1. Refrigerador doméstico (Línea Blanca > Refrigeradores): 125 productos
 2. Lavadoras (Línea Blanca > Lavadoras y secadoras): 98 productos
 3. Televisores (Electrónica > Video): 87 productos
...

================================================================================
Scraping completed at: 2025-11-12 10:45:23
================================================================================
```

## Error Handling

The scraper includes:

- **Network retry logic**: Handles connection failures gracefully
- **Timeout handling**: Prevents hanging on slow responses
- **Keyboard interrupt**: Save partial results with Ctrl+C
- **URL deduplication**: Avoids scraping the same category twice

## Notes

- The scraper respects the website by adding 1-second delays between requests
- Some categories may not have product listing pages (level 1 categories often serve as navigation only)
- Product counts represent the number shown on the category page, which may vary with inventory

## Troubleshooting

### "Failed to fetch page"
- Check internet connection
- Verify the website is accessible: https://www.dismac.com.bo

### "No product count found"
- Some categories are navigation-only and don't list products directly
- This is expected behavior for parent categories

### SSL Certificate Errors
Add this to the session initialization if needed:
```python
self.session.verify = False
```

## License

This tool is for educational and research purposes only. Please review Dismac's terms of service and robots.txt before extensive scraping.
