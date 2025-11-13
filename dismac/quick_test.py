#!/usr/bin/env python3
"""
Quick test run of Dismac scraper - processes only first 5 categories
"""

from scraper_dismac import DismacCategoryScraper


def main():
    """Run a quick test with limited categories."""
    print("Running QUICK TEST - processing only first 5 categories")
    print("="*80)
    
    scraper = DismacCategoryScraper()
    
    # Fetch main page
    html = scraper.fetch_page(scraper.CATEGORIES_URL)
    if not html:
        print("Failed to fetch categories page")
        return
    
    # Extract categories
    categories = scraper.extract_category_links(html)
    print(f"Found {len(categories)} total categories")
    print("Processing first 5 for testing...\n")
    
    # Process only first 5
    for i, category in enumerate(categories[:5], 1):
        print(f"[{i}/5] Processing: {category['name']}")
        result = scraper.process_category(category)
        if result:
            scraper.results.append(result)
        print()
    
    # Save and print summary
    scraper.save_to_csv("dismac_quick_test.csv")
    scraper.print_summary()


if __name__ == "__main__":
    main()
