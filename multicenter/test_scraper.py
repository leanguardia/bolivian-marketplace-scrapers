#!/usr/bin/env python3
"""
Test script for Multicenter scraper
Tests basic functionality with a single category
"""

from scraper_multicenter import MulticenterCategoryScraper


def test_single_category():
    """Test scraping a single category."""
    print("Testing Multicenter scraper with Muebles category...")
    print("-" * 60)
    
    scraper = MulticenterCategoryScraper(headless=False)
    
    try:
        scraper.setup_driver()
        
        # Test with Muebles category
        test_url = "https://www.multicenter.com/muebles"
        test_name = "Muebles"
        
        count = scraper.extract_product_count(test_url, test_name)
        
        if count:
            print(f"\n✓ Successfully extracted product count: {count}")
            print("\nTest PASSED")
            return True
        else:
            print("\n✗ Failed to extract product count")
            print("\nTest FAILED")
            return False
            
    finally:
        scraper.close_driver()


if __name__ == '__main__':
    test_single_category()
