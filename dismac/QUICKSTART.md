# Dismac Scraper - Quick Start Guide

## Installation

```bash
# 1. Navigate to the dismac directory
cd dismac/

# 2. Install dependencies
pip install -r requirements.txt
```

## Quick Start (30 seconds)

Run a quick test to see it in action:

```bash
python3 quick_test.py
```

**What it does**: Scrapes the first 5 categories to demonstrate functionality.

**Output**:
- Console: Progress updates and summary
- File: `dismac_quick_test.csv`

## Interactive Mode (Recommended)

```bash
python3 example_usage.py
```

You'll see a menu:

```
================================================================================
DISMAC CATEGORY SCRAPER - Menu
================================================================================

1. Full Scrape (all categories, ~5-10 minutes)
2. Limited Scrape - 20 categories (~1 minute)
3. Limited Scrape - 50 categories (~2-3 minutes)
4. Quick Test - 5 categories (~30 seconds)
5. Exit

Select option (1-5):
```

**Recommendations**:
- First time? → Choose **Option 4** (Quick Test)
- Need full data? → Choose **Option 1** (Full Scrape)
- Testing/Development? → Choose **Option 2** or **3**

## Command Line Mode

### Full Scrape
```bash
python3 scraper_dismac.py
```
**Time**: ~5-10 minutes  
**Output**: `dismac_categories_report.csv`

### Quick Test
```bash
python3 example_usage.py --test
```
**Time**: ~30 seconds  
**Output**: `dismac_categories_limited_5.csv`

### Custom Limit
```bash
python3 example_usage.py --limit=20
```
**Time**: ~1-2 minutes  
**Output**: `dismac_categories_limited_20.csv`

## Understanding the Output

### Console Output

```
[3/243] Processing: Frigobares y cavas
Fetching: https://www.dismac.com.bo/categorias/.../frigobares-y-cavas.html
      ✓ Frigobares y cavas: 15 productos
```

**Symbols**:
- `✓` = Products found (this is a product listing page)
- `○` = No products (navigation/parent category only)

**Indentation**: Shows category hierarchy level
- No indent = Level 1 (Main category)
- 2 spaces = Level 2 (Subcategory)
- 4 spaces = Level 3 (Sub-subcategory)

### CSV Output

Open in Excel, Google Sheets, or any CSV viewer:

| category_name | level | parent | url | product_count | scraped_at |
|---------------|-------|--------|-----|---------------|------------|
| Línea Blanca | 1 | | https://... | 0 | 2025-11-12T... |
| Refrigeradores | 2 | Línea Blanca | https://... | 0 | 2025-11-12T... |
| Frigobares y cavas | 3 | Línea Blanca > Refrigeradores | https://... | 15 | 2025-11-12T... |

**Columns Explained**:
- **category_name**: Display name of category
- **level**: 1 (main), 2 (sub), or 3 (sub-sub)
- **parent**: Breadcrumb path to this category
- **url**: Direct link to category page
- **product_count**: Number of products (0 = navigation only)
- **scraped_at**: When this was collected

## Analyzing Results

### In Excel/Sheets

1. **Sort by product_count** (descending) to find largest categories
2. **Filter by level** to see only leaf categories (level 3)
3. **Pivot Table** by parent to see category group totals

### In Python

```python
import pandas as pd

# Load the CSV
df = pd.read_csv('dismac_categories_report.csv')

# Top 10 categories
top10 = df.nlargest(10, 'product_count')
print(top10[['category_name', 'product_count']])

# Total products
total = df['product_count'].sum()
print(f"Total products: {total}")

# Products by level
by_level = df.groupby('level')['product_count'].sum()
print(by_level)
```

## Examples of Use Cases

### 1. Competitive Analysis
"How many products does Dismac have in each category?"
```bash
python3 scraper_dismac.py
# Open dismac_categories_report.csv
# Sort by product_count descending
```

### 2. Category Planning
"Which subcategories have the most products?"
```bash
python3 scraper_dismac.py
# Filter CSV where level = 3
# These are the actual product-holding categories
```

### 3. Market Research
"What's the product distribution across major categories?"
```bash
python3 scraper_dismac.py
# Group by parent category in Excel
# Create pivot table
```

## Troubleshooting

### "Connection Error"
**Problem**: Can't reach dismac.com.bo  
**Solution**: 
1. Check internet connection
2. Try: `curl https://www.dismac.com.bo/categorias.html`
3. If blocked, wait a few minutes

### "No module named 'requests'"
**Problem**: Dependencies not installed  
**Solution**: `pip install -r requirements.txt`

### "SSL Certificate Error"
**Problem**: SSL verification failing  
**Solution**: Update certificates or disable verification (not recommended)

### Scraper is too slow
**Problem**: Taking longer than expected  
**Solution**: 
- Use limited mode: `python3 example_usage.py --limit=20`
- Check internet speed
- Normal speed: ~1 category every 2 seconds

## Tips for Best Results

1. **Run during off-peak hours**: Less server load = faster scraping
2. **Start small**: Test with `--limit=5` before full scrape
3. **Check robots.txt**: Be respectful to the website
4. **Save regularly**: Interrupt (Ctrl+C) saves partial results
5. **Validate**: Compare a few entries manually to verify accuracy

## Next Steps

After scraping:

1. **Analyze the data**: Use Excel, Python pandas, or data viz tools
2. **Schedule regular runs**: Track changes over time
3. **Compare with competitors**: Similar scrapers for other sites
4. **Build dashboards**: Visualize the category distribution

## Getting Help

1. **Check README.md**: Full documentation
2. **Run tests**: `python3 test_scraper.py`
3. **Review PROJECT_SUMMARY.md**: Technical details
4. **Check console output**: Error messages are descriptive

---

**Ready to start?**

```bash
# Quickest way to see it work:
python3 quick_test.py

# When ready for full data:
python3 scraper_dismac.py
```

Good luck! 🚀
