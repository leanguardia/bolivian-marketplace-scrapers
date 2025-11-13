#!/usr/bin/env python3
"""
Test script for Dismac scraper
"""

import os
import sys
from scraper_dismac import DismacCategoryScraper


def test_scraper():
    """Test the scraper with a quick run."""
    print("Testing Dismac Category Scraper")
    print("="*80)
    
    scraper = DismacCategoryScraper()
    
    # Test 1: Fetch categories page
    print("\nTest 1: Fetching main categories page...")
    html = scraper.fetch_page(scraper.CATEGORIES_URL)
    if html:
        print("✓ Successfully fetched categories page")
    else:
        print("✗ Failed to fetch categories page")
        return False
    
    # Test 2: Extract categories
    print("\nTest 2: Extracting category structure...")
    categories = scraper.extract_category_links(html)
    print(f"✓ Found {len(categories)} categories")
    
    if categories:
        print("\nSample categories:")
        for i, cat in enumerate(categories[:5], 1):
            indent = "  " * cat['level']
            print(f"{i}. {indent}{cat['name']} (Level {cat['level']})")
    
    # Test 3: Test product count extraction from dormitorio page
    print("\nTest 3: Testing product count extraction...")
    test_url = "https://www.dismac.com.bo/categorias/52-hogar/130-muebles/126-dormitorio.html"
    
    if os.path.exists('dismac/dismac-dormitorio.html'):
        print("  Using local file: dismac-dormitorio.html")
        with open('dismac/dismac-dormitorio.html', 'r', encoding='utf-8') as f:
            test_html = f.read()
    else:
        print(f"  Fetching: {test_url}")
        test_html = scraper.fetch_page(test_url)
    
    if test_html:
        count = scraper.extract_product_count(test_html)
        if count is not None:
            print(f"✓ Successfully extracted product count: {count} productos")
        else:
            print("✗ Failed to extract product count")
            return False
    else:
        print("✗ Failed to fetch test page")
        return False
    
    print("\n" + "="*80)
    print("All tests passed! Ready to run full scraper.")
    print("="*80)
    print("\nTo run the full scraper, execute:")
    print("  python scraper_dismac.py")
    
    return True


if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)
