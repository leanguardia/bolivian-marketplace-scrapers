"""
Test script for Venbo scraper
Tests basic functionality without running a full scrape
"""

import requests
from bs4 import BeautifulSoup
import re

def test_category_page():
    """Test fetching the main categories page"""
    print("=" * 80)
    print("TEST 1: Fetching main categories page")
    print("=" * 80)
    
    url = "https://venbo.shop/categorias/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find category links
        category_links = []
        for link in soup.find_all('a', href=True):
            if '/cat-producto/' in link['href']:
                category_links.append(link['href'])

        category_links = list(set(category_links))  # Remove duplicates

        print(f"✓ Successfully fetched categories page")
        print(f"✓ Found {len(category_links)} unique category links")
        print("\nSample category links:")
        for i, link in enumerate(category_links[:5], 1):
            print(f"  {i}. {link}")
        
        return True, category_links
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False, []


def test_product_listing_page(category_url=None):
    """Test fetching a product listing page"""
    print("\n" + "=" * 80)
    print("TEST 2: Checking product listing page")
    print("=" * 80)
    
    # Use a known product category if none provided
    if not category_url:
        category_url = "https://venbo.shop/cat-producto/alimentacion/conservas/"
    
    print(f"Testing URL: {category_url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(category_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if it's a product listing page
        page_text = soup.get_text()
        is_listing = False
        product_count = 0
        
        # Check for "Showing all X results"
        match = re.search(r'Showing all (\d+) results', page_text, re.IGNORECASE)
        if match:
            is_listing = True
            product_count = int(match.group(1))
            print(f"✓ This IS a product listing page")
            print(f"✓ Found indicator: 'Showing all {product_count} results'")
        
        # Check for result count element
        result_count = soup.find('p', class_='woocommerce-result-count')
        if result_count:
            is_listing = True
            print(f"✓ Found woocommerce-result-count element")
        
        if not is_listing:
            print(f"✗ This does NOT appear to be a product listing page")
            return False
        
        # Try to find products
        product_containers = soup.find_all(['li', 'div'], class_=re.compile(r'product|kad_product'))
        print(f"✓ Found {len(product_containers)} product containers")
        
        # Try to extract one product
        if product_containers:
            print("\nSample product extraction:")
            first_product = product_containers[0]
            
            # Title
            title_elem = first_product.find('h5')
            if title_elem:
                print(f"  Title: {title_elem.get_text(strip=True)[:60]}...")
            
            # URL
            link_elem = first_product.find('a', class_='product_item_link')
            if link_elem and 'href' in link_elem.attrs:
                print(f"  URL: {link_elem['href']}")
            
            # Price
            price_elem = first_product.find('span', class_='product_price')
            if price_elem:
                print(f"  Price: {price_elem.get_text(strip=True)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def test_recursive_detection():
    """Test detection of multi-level categories"""
    print("\n" + "=" * 80)
    print("TEST 3: Multi-level category detection")
    print("=" * 80)
    
    # Example of a deep category path
    test_url = "https://venbo.shop/cat-producto/cine-musica-fotos/videos/videos-generos/drama/"
    
    print(f"Testing deep category: {test_url}")
    
    # Count the levels
    path = test_url.split('/cat-producto/')[1].rstrip('/')
    levels = path.count('/') + 1
    
    print(f"✓ Category depth: {levels} levels")
    print(f"✓ Category path: {path}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(test_url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Check if it's a listing or navigation page
        page_text = soup.get_text()
        if re.search(r'Showing all \d+ results', page_text, re.IGNORECASE):
            print(f"✓ This is a PRODUCT LISTING page (end of category tree)")
        else:
            print(f"✓ This is a CATEGORY NAVIGATION page (has subcategories)")
            
            # Find subcategories
            subcategories = []
            for link in soup.find_all('a', href=True):
                if '/cat-producto/' in link['href']:
                    subcategories.append(link['href'])
            
            subcategories = list(set(subcategories))
            print(f"✓ Found {len(subcategories)} potential subcategory links")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 80)
    print("VENBO SCRAPER - TEST SUITE")
    print("=" * 80)
    
    results = []
    
    # Test 1: Categories page
    success, categories = test_category_page()
    results.append(("Categories page", success))
    
    # Test 2: Product listing page
    if categories:
        # Find a product category from the list
        product_cat = None
        for cat in categories:
            if any(keyword in cat for keyword in ['alimentacion', 'libros', 'juguetes']):
                product_cat = cat if cat.startswith('http') else f"https://venbo.shop{cat}"
                break
        
        if product_cat:
            success = test_product_listing_page(product_cat)
        else:
            success = test_product_listing_page()
    else:
        success = test_product_listing_page()
    
    results.append(("Product listing page", success))
    
    # Test 3: Multi-level categories
    success = test_recursive_detection()
    results.append(("Multi-level categories", success))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 80)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("\n✓ All tests passed! The scraper should work correctly.")
        print("\nYou can now run: python scraper_venbo.py")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")


if __name__ == "__main__":
    main()
