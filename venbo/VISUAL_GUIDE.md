# Venbo Scraper - Visual Guide

## 🗺️ How The Scraper Navigates

### Starting Point
```
https://venbo.shop/categorias/
    │
    │ Extract all links with /cat-producto/
    │
    ├─ Category 1: Alimentación / Bebidas
    ├─ Category 2: Artesanías  
    ├─ Category 3: Electrónica
    ├─ Category 4: Informática / Oficina
    └─ ... (89 total categories)
```

### Example: Exploring "Alimentación / Bebidas"

```
Step 1: Visit main category
https://venbo.shop/cat-producto/alimentacion/
    │
    ├─ Check: Is this a product listing page?
    │  └─ NO (no "Showing all X results")
    │
    └─ Extract subcategories:
        ├─ aperitivos/
        ├─ cereales-frutos-secos-y-semillas/
        ├─ chocolates-dulces/
        ├─ conservas/
        ├─ lacteos/
        ├─ pastas-y-harinas/
        └─ salsas-aderezos/

Step 2: Visit first subcategory
https://venbo.shop/cat-producto/alimentacion/aperitivos/
    │
    ├─ Check: Is this a product listing page?
    │  └─ YES! (found "Showing all 15 results")
    │
    └─ Scrape products:
        ├─ Product 1: Chocolate Bar XYZ (Bs 25.00)
        ├─ Product 2: Cookies ABC (Bs 18.50)
        └─ ... (15 products total)
```

### Example: Deep Category Navigation

```
Exploring: Cine y TV / Música / Fotos
│
├─ Level 1: /cat-producto/cine-musica-fotos/
│   └─ Not a listing page → Continue
│
├─ Level 2: /cat-producto/cine-musica-fotos/videos/
│   └─ Not a listing page → Continue
│
├─ Level 3: /cat-producto/cine-musica-fotos/videos/videos-generos/
│   └─ Not a listing page → Continue
│
└─ Level 4: /cat-producto/cine-musica-fotos/videos/videos-generos/drama/
    └─ Product listing! → Scrape products
```

## 🎯 Product Listing Page Detection

### Method 1: Text Search
```html
<!-- Search page text for this pattern -->
Showing all 15 results
```

### Method 2: HTML Element
```html
<!-- Look for this element -->
<p class="woocommerce-result-count">
    Showing all 15 results
</p>
```

## 📦 Product Extraction Process

### HTML Structure
```html
<div class="product kad_product post-83829 instock">
    <div class="product_item">
        <a href="https://venbo.shop/productos/..." class="product_item_link">
            <img src="https://venbo.shop/wp-content/uploads/..." />
        </a>
        <div class="product_details">
            <h5>Flor de sal Salar de Uyuni</h5>
            <span class="product_price">
                <span class="woocommerce-Price-amount">
                    17,50<span>Bs</span>
                </span>
            </span>
        </div>
    </div>
</div>
```

### Extracted Data
```python
{
    'product_id': '83829',
    'title': 'Flor de sal Salar de Uyuni',
    'url': 'https://venbo.shop/productos/...',
    'regular_price': '17.50',
    'sale_price': '17.50',
    'on_sale': 'No',
    'discount': 'N/A',
    'in_stock': 'Yes',
    'image_url': 'https://venbo.shop/wp-content/uploads/...',
    'category_url': 'https://venbo.shop/cat-producto/alimentacion/conservas/'
}
```

## 🔄 Scraping Flow Diagram

```
┌─────────────────────────────────────────┐
│  Start: /categorias/ page               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Extract all /cat-producto/ links       │
│  Found: 89 category URLs                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  For each category URL:                 │
└──────────────┬──────────────────────────┘
               │
               ▼
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌──────────────┐  ┌──────────────┐
│  Visit URL   │  │  Already     │
│              │  │  visited?    │
└──────┬───────┘  └──────────────┘
       │                 │
       │                 └──> Skip
       │
       ▼
┌─────────────────────────────────────────┐
│  Check: Contains "Showing all X"?       │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        │             │
       YES           NO
        │             │
        ▼             ▼
┌─────────────┐  ┌─────────────────┐
│  PRODUCT    │  │  CATEGORY NAV   │
│  LISTING    │  │  PAGE           │
└──────┬──────┘  └────────┬────────┘
       │                  │
       ▼                  ▼
┌─────────────┐  ┌─────────────────┐
│  Scrape     │  │  Extract        │
│  Products   │  │  Subcategory    │
│             │  │  Links          │
└──────┬──────┘  └────────┬────────┘
       │                  │
       │                  └──> Recurse
       │
       ▼
┌─────────────────────────────────────────┐
│  Add products to list                   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Continue to next category              │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  All categories done?                   │
└──────────────┬──────────────────────────┘
               │
              YES
               │
               ▼
┌─────────────────────────────────────────┐
│  Save to CSV & Generate Report          │
└─────────────────────────────────────────┘
```

## 📊 Progress Tracking

### Console Output Breakdown

```
================================================================================
Starting Venbo scraper
Base URL: https://venbo.shop
================================================================================
```
↑ Initialization phase

```
Found 89 main category links
```
↑ Extracted all top-level categories

```
================================================================================
Main Category 1/89
================================================================================
```
↑ Processing first main category

```
Exploring: https://venbo.shop/cat-producto/alimentacion/
→ This is a CATEGORY NAVIGATION page
→ Found 7 subcategory links
```
↑ Category has subcategories, will explore them

```
  Exploring: https://venbo.shop/cat-producto/alimentacion/aperitivos/
  → This is a PRODUCT LISTING page
  → Found 15 products in this category
  Found 15 products on https://venbo.shop/cat-producto/alimentacion/aperitivos/
```
↑ Found products! Scraped 15 items

```
================================================================================
Scraping completed
Total categories with products found: 42
Total products scraped: 1,234
================================================================================
```
↑ Final summary

## 🎨 Category Tree Visualization

### Actual Venbo Structure (Sample)

```
Venbo.shop
│
├─ Alimentación / Bebidas (7 subcategories)
│   ├─ Aperitivos [15 products] ✓
│   ├─ Cereales, frutos secos y semillas [8 products] ✓
│   ├─ Chocolates y dulces [23 products] ✓
│   ├─ Conservas [12 products] ✓
│   ├─ Lácteos y para refrigerar [5 products] ✓
│   ├─ Pastas y harinas [18 products] ✓
│   └─ Salsas y aderezos [9 products] ✓
│
├─ Artesanías (6 subcategories)
│   ├─ Cerámica [12 products] ✓
│   ├─ Chala (hoja de maíz) [3 products] ✓
│   ├─ Madera [8 products] ✓
│   ├─ Piel [15 products] ✓
│   ├─ Vidrio [5 products] ✓
│   └─ Textíl [6 products] ✓
│
├─ Electrónica (13 subcategories)
│   ├─ Adaptadores y cargadores [25 products] ✓
│   ├─ Cables [18 products] ✓
│   ├─ Iluminación [32 products] ✓
│   └─ Sonido
│       └─ Audífonos [45 products] ✓
│
├─ Informática / Oficina (8 subcategories)
│   ├─ Almacenamiento [7 products] ✓
│   ├─ Conectividad [12 products] ✓
│   ├─ Laptops [4 products] ✓
│   └─ Periféricos [28 products] ✓
│
└─ ... (more categories)
```

## 🔢 Statistics at a Glance

```
┌──────────────────────────────────────────┐
│  VENBO SCRAPING STATISTICS               │
├──────────────────────────────────────────┤
│  Main Categories:          ~16           │
│  Total Category URLs:      ~90           │
│  Categories with Products: ~40-50        │
│  Average Products/Category: 15-30        │
│  Estimated Total Products: 500-2000      │
│  Scraping Time:            20-40 min     │
│  Delay Between Requests:   1.5 seconds   │
└──────────────────────────────────────────┘
```

## 🎯 Key Points to Remember

1. **Not all categories have products**
   - Some are just navigation pages
   - They help organize the hierarchy

2. **Multi-level navigation**
   - Some categories are 4+ levels deep
   - Scraper handles this automatically

3. **Product detection is reliable**
   - Checks for specific text patterns
   - Validates with HTML structure

4. **No duplicate scraping**
   - Tracks visited URLs
   - Prevents redundant requests

5. **Respectful scraping**
   - 1.5 second delay between requests
   - Proper User-Agent header

## 📈 Expected Results

### CSV File Preview
```
product_id,title,url,regular_price,sale_price,on_sale,discount,in_stock,image_url,category_url
83829,"Flor de sal...",https://venbo.shop/...,17.50,17.50,No,N/A,Yes,https://...,https://...
84583,"Kit de bord...",https://venbo.shop/...,210,210,No,N/A,Yes,https://...,https://...
67160,"Baraja del ...",https://venbo.shop/...,150,140,Yes,-7%,Yes,https://...,https://...
...
```

### Report File Preview
```
VENBO CATEGORIES REPORT
================================================================================

Total categories with products: 42
Total products found: 1,234

================================================================================

[15 products] https://venbo.shop/cat-producto/alimentacion/aperitivos/
[8 products] https://venbo.shop/cat-producto/alimentacion/cereales-frutos-secos-y-semillas/
[23 products] https://venbo.shop/cat-producto/alimentacion/chocolates-dulces/
  [4 products] https://venbo.shop/cat-producto/informatica-oficina/informatica-laptops/
  [12 products] https://venbo.shop/cat-producto/artesania/artesania-ceramica/
...
```

---

**Ready to start?** → Run `python3 scraper_venbo.py`
