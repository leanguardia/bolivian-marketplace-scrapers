# Dismac Category Scraper - Visual Guide

## 🎯 Project Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  DISMAC CATEGORY SCRAPER                    │
│                                                             │
│  Recursively crawls Dismac's category tree and counts      │
│  products in each category, subcategory, and sub-sub-      │
│  category.                                                  │
└─────────────────────────────────────────────────────────────┘
```

## 📂 Project Structure

```
dismac/
│
├── 🚀 CORE SCRIPTS
│   ├── scraper_dismac.py      ⭐ Main scraper (production)
│   ├── example_usage.py       🎮 Interactive menu
│   ├── test_scraper.py        ✅ Unit tests
│   └── quick_test.py          ⚡ Quick demo (5 categories)
│
├── 📚 DOCUMENTATION
│   ├── INDEX.md               📇 Start here - navigation
│   ├── QUICKSTART.md          ⚡ Quick start (30 seconds)
│   ├── README.md              📖 Full documentation
│   ├── PROJECT_SUMMARY.md     🔧 Technical details
│   └── VISUAL_GUIDE.md        🎨 This file
│
├── ⚙️ CONFIGURATION
│   └── requirements.txt       📦 Python dependencies
│
├── 🗂️ SAMPLE DATA
│   ├── dismac-categorias.html      📄 Categories page
│   └── dismac-dormitorio.html      📄 Product listing
│
└── 📊 OUTPUT (generated)
    ├── dismac_categories_report.csv       (full scrape)
    ├── dismac_quick_test.csv             (test run)
    └── dismac_categories_limited_N.csv    (limited runs)
```

## 🔄 How It Works - Flow Diagram

```
┌─────────────────┐
│  START SCRAPER  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ Fetch Main Categories Page  │
│ (categorias.html)            │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Parse Category Hierarchy    │
│ Level 1: Línea Blanca       │
│   Level 2: Refrigeradores   │
│     Level 3: Frigobares     │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ Loop Through Each Category  │ ←──┐
└────────┬────────────────────┘    │
         │                          │
         ▼                          │
┌─────────────────────────────┐    │
│ Fetch Category Page         │    │
└────────┬────────────────────┘    │
         │                          │
         ▼                          │
┌─────────────────────────────┐    │
│ Extract Product Count       │    │
│ "44 Productos"              │    │
└────────┬────────────────────┘    │
         │                          │
         ▼                          │
┌─────────────────────────────┐    │
│ Save to Results List        │    │
└────────┬────────────────────┘    │
         │                          │
         ▼                          │
         More Categories? ──────────┘
         │ No
         ▼
┌─────────────────────────────┐
│ Export to CSV               │
│ + Print Summary Stats       │
└────────┬────────────────────┘
         │
         ▼
┌─────────────────┐
│   COMPLETE!     │
└─────────────────┘
```

## 🏗️ Category Hierarchy Example

```
📁 Línea Blanca (Level 1)
│
├─ 📁 Refrigeradores (Level 2)
│  ├─ 📦 Frigobares y cavas (Level 3) ........... 15 productos
│  └─ 📦 Refrigerador doméstico (Level 3) ....... 82 productos
│
├─ 📁 Lavadoras y secadoras (Level 2)
│  ├─ 📦 Lavadoras (Level 3) .................... 65 productos
│  ├─ 📦 Secadoras (Level 3) .................... 23 productos
│  └─ 📦 Lava/Seca (Level 3) .................... 12 productos
│
└─ 📁 Cocinas (Level 2)
   ├─ 📦 Clásicas (Level 3) ..................... 34 productos
   └─ 📦 Encimeras (Level 3) .................... 18 productos

Legend:
📁 = Navigation category (no products directly)
📦 = Product listing page (has product count)
```

## 💻 Console Output Example

```
================================================================================
DISMAC CATEGORY SCRAPER
================================================================================
Starting scrape at: 2025-11-12 23:59:54
Categories URL: https://www.dismac.com.bo/categorias.html
================================================================================

Extracting category structure...
Found 243 categories to process

Processing categories:
--------------------------------------------------------------------------------

[1/243] Processing: Línea Blanca
Fetching: https://www.dismac.com.bo/categorias/50-linea-blanca.html
○ Línea Blanca: No product listing page
                          ↑
                          └─ Navigation only (parent category)

[2/243] Processing: Refrigeradores
Fetching: https://www.dismac.com.bo/categorias/.../101-refrigeradores.html
  ○ Refrigeradores: No product listing page
  ↑
  └─ 2-space indent = Level 2

[3/243] Processing: Frigobares y cavas
Fetching: https://www.dismac.com.bo/categorias/.../frigobares-y-cavas.html
    ✓ Frigobares y cavas: 15 productos
    ↑   ↑                ↑
    │   │                └─ Product count found!
    │   └─ Success indicator
    └─ 4-space indent = Level 3

...continuing through all categories...

================================================================================
SUMMARY
================================================================================
Total categories processed: 243
Categories with products: 156
Total products found: 3,847

Top 10 categories by product count:
--------------------------------------------------------------------------------
 1. Refrigerador doméstico (Línea Blanca > Refrigeradores): 82 productos
 2. Lavadoras (Línea Blanca > Lavadoras y secadoras): 65 productos
 3. Televisores LED (Electrónica > Video): 58 productos
 ...

================================================================================
Scraping completed at: 2025-11-13 00:05:23
================================================================================
```

## 📊 CSV Output Structure

```
┌──────────────────┬───────┬─────────────────┬──────────────┬───────────────┬─────────────────────┐
│ category_name    │ level │ parent          │ url          │ product_count │ scraped_at          │
├──────────────────┼───────┼─────────────────┼──────────────┼───────────────┼─────────────────────┤
│ Línea Blanca     │   1   │                 │ https://...  │      0        │ 2025-11-12T23:59:54 │
│ Refrigeradores   │   2   │ Línea Blanca    │ https://...  │      0        │ 2025-11-12T23:59:59 │
│ Frigobares       │   3   │ Línea B... > R..│ https://...  │     15        │ 2025-11-13T00:00:04 │
│ Refrigerador     │   3   │ Línea B... > R..│ https://...  │     82        │ 2025-11-13T00:00:11 │
└──────────────────┴───────┴─────────────────┴──────────────┴───────────────┴─────────────────────┘
```

## 🎮 Usage Modes - Visual Decision Tree

```
                   ┌─────────────────┐
                   │  Want to run    │
                   │   the scraper?  │
                   └────────┬────────┘
                            │
           ┌────────────────┼────────────────┐
           │                │                │
           ▼                ▼                ▼
    ┌───────────┐   ┌──────────┐   ┌────────────┐
    │ First     │   │ Need      │   │ Production │
    │ time?     │   │ specific  │   │ full data? │
    └─────┬─────┘   │ amount?   │   └──────┬─────┘
          │         └─────┬─────┘          │
          │               │                │
          ▼               ▼                ▼
    quick_test.py   example_usage.py   scraper_dismac.py
    (5 categories)   --limit=N          (all ~243)
    ~30 seconds      ~1-3 minutes       ~5-10 minutes
```

## 🔍 Product Count Detection Methods

The scraper uses multiple methods to find product counts:

```
Method 1: JavaScript Variable
┌─────────────────────────────────┐
│ <script>                        │
│   let htmlCount = "44 Productos";│  ← Regex search
│ </script>                       │
└─────────────────────────────────┘

Method 2: HTML Container
┌──────────────────────────────────────┐
│ <div class="container-count-items"> │
│   <span id="counter-items-page">    │  ← BeautifulSoup
│     44 Productos                     │     parsing
│   </span>                            │
│ </div>                               │
└──────────────────────────────────────┘

Both methods extract: 44
```

## 📈 Performance Metrics

```
┌─────────────────────────────────────────────┐
│           SCRAPING PERFORMANCE              │
├─────────────────────────────────────────────┤
│ Categories Found:     ~243                  │
│ Request Rate:         1 request/second      │
│ Success Rate:         >95%                  │
│                                             │
│ TIMING:                                     │
│ ├─ 5 categories:      ~30 seconds          │
│ ├─ 20 categories:     ~1 minute            │
│ ├─ 50 categories:     ~2-3 minutes         │
│ └─ Full (243):        ~5-10 minutes        │
└─────────────────────────────────────────────┘
```

## 🎯 Quick Command Reference

```
┌──────────────────────────────────────────────────────────┐
│ COMMAND                          │ WHAT IT DOES           │
├──────────────────────────────────┼────────────────────────┤
│ python3 test_scraper.py          │ ✅ Run tests           │
│ python3 quick_test.py            │ ⚡ Demo (5 cats)       │
│ python3 example_usage.py         │ 🎮 Interactive menu    │
│ python3 example_usage.py --test  │ ⚡ Quick test          │
│ python3 example_usage.py --full  │ 📊 Full scrape         │
│ python3 example_usage.py --limit=20 │ 📊 Limited (20)     │
│ python3 scraper_dismac.py        │ ⭐ Production run      │
└──────────────────────────────────┴────────────────────────┘
```

## 🛠️ Troubleshooting Visual Guide

```
Problem                  Solution
   │                        │
   ├─ Can't connect     →  Check internet
   │                        curl dismac.com.bo
   │
   ├─ No module found   →  pip install -r requirements.txt
   │
   ├─ SSL error         →  Update certificates
   │                        OR disable verification (not recommended)
   │
   ├─ Too slow          →  Normal (1 sec/category)
   │                        Use --limit for testing
   │
   └─ Wrong count       →  Website changed?
                            Check HTML structure
```

## 📚 Documentation Navigation Map

```
                    INDEX.md
                        │
         ┌──────────────┼──────────────┐
         │              │              │
         ▼              ▼              ▼
   QUICKSTART.md   README.md   PROJECT_SUMMARY.md
   (Fast Start)    (Complete)   (Technical)
         │              │              │
         │              │              │
    For Users      For Learning   For Developers
```

## 🎓 Learning by Example

### Example 1: Quick Test (30 seconds)
```bash
$ python3 quick_test.py

Output:
✓ 5 categories processed
✓ CSV file created
✓ Summary shown
```

### Example 2: Interactive Mode
```bash
$ python3 example_usage.py

Menu appears → Choose option 4 (Quick Test)
→ Processes 5 categories
→ Shows results
```

### Example 3: Full Production Run
```bash
$ python3 scraper_dismac.py

Progress shown for all 243 categories
→ CSV: dismac_categories_report.csv
→ Summary with Top 10 categories
```

---

## 🚀 Ready to Start?

1. **Install**: `pip install -r requirements.txt`
2. **Test**: `python3 test_scraper.py`
3. **Demo**: `python3 quick_test.py`
4. **Production**: `python3 scraper_dismac.py`

---

*This visual guide shows the structure and flow of the Dismac scraper.*  
*For detailed instructions, see: [QUICKSTART.md](QUICKSTART.md)*  
*For technical details, see: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)*
