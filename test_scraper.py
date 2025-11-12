"""
Test script to validate the Boliviamart scraper

This script performs basic validation without doing a full scrape.
"""

import sys
from scraper_boliviamart import BoliviamartScraper
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_connection():
    """Test if we can connect to the website"""
    print("\n" + "="*60)
    print("TEST 1: Connection Test")
    print("="*60)
    
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=12,  # Small page size for testing
        delay=1.0
    )
    
    url = "https://www.boliviamart.com/tienda/?count=12"
    soup = scraper.get_page(url)
    
    if soup:
        print("✓ Successfully connected to Boliviamart")
        return True
    else:
        print("✗ Failed to connect to Boliviamart")
        return False


def test_product_extraction():
    """Test if we can extract product information"""
    print("\n" + "="*60)
    print("TEST 2: Product Extraction Test")
    print("="*60)
    
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=12,
        delay=1.0
    )
    
    url = "https://www.boliviamart.com/tienda/?count=12"
    products = scraper.scrape_page(url)
    
    if products and len(products) > 0:
        print(f"✓ Successfully extracted {len(products)} products")
        
        # Show first product details
        print("\nFirst product details:")
        first_product = products[0]
        for key, value in first_product.items():
            print(f"  {key}: {value}")
        
        return True
    else:
        print("✗ Failed to extract products")
        return False


def test_pagination():
    """Test if pagination detection works"""
    print("\n" + "="*60)
    print("TEST 3: Pagination Detection Test")
    print("="*60)
    
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=12,
        delay=1.0
    )
    
    url = "https://www.boliviamart.com/tienda/?count=12"
    soup = scraper.get_page(url)
    
    if soup:
        total_pages = scraper.get_total_pages(soup)
        print(f"✓ Detected {total_pages} total pages")
        
        if total_pages > 0:
            return True
        else:
            print("✗ Failed to detect pagination")
            return False
    else:
        print("✗ Failed to fetch page for pagination test")
        return False


def test_csv_export():
    """Test CSV export functionality"""
    print("\n" + "="*60)
    print("TEST 4: CSV Export Test")
    print("="*60)
    
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=12,
        delay=1.0
    )
    
    url = "https://www.boliviamart.com/tienda/?count=12"
    products = scraper.scrape_page(url)
    
    if products:
        test_filename = 'test_export.csv'
        scraper.save_to_csv(products, test_filename)
        
        # Check if file was created
        import os
        if os.path.exists(test_filename):
            print(f"✓ Successfully created CSV file: {test_filename}")
            print(f"  File size: {os.path.getsize(test_filename)} bytes")
            
            # Clean up test file
            try:
                os.remove(test_filename)
                print(f"  Test file removed")
            except:
                pass
            
            return True
        else:
            print("✗ Failed to create CSV file")
            return False
    else:
        print("✗ No products to export")
        return False


def run_all_tests():
    """Run all validation tests"""
    print("\n" + "="*60)
    print("BOLIVIAMART SCRAPER - VALIDATION TESTS")
    print("="*60)
    
    results = []
    
    # Test 1: Connection
    results.append(("Connection", test_connection()))
    
    # Test 2: Product Extraction
    results.append(("Product Extraction", test_product_extraction()))
    
    # Test 3: Pagination
    results.append(("Pagination Detection", test_pagination()))
    
    # Test 4: CSV Export
    results.append(("CSV Export", test_csv_export()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:.<40} {status}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    if passed == total:
        print("All tests passed! The scraper is ready to use.")
        return 0
    else:
        print("Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
