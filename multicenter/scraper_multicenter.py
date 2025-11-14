#!/usr/bin/env python3
"""
Multicenter Category Scraper

This scraper crawls through Multicenter's main category menu and extracts
the product count for each main category.

The scraper focuses only on main categories (Navidad through Bebés), 
ignoring promotional sections like Black Friday, Solo X hoy, Ofertas del Mes, and Combos.

Usage:
    python scraper_multicenter.py
"""

import re
import csv
import time
from typing import List, Dict, Optional
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class MulticenterCategoryScraper:
    """Scrapes Multicenter main category product counts."""
    
    BASE_URL = "https://www.multicenter.com"
    
    # Main categories to scrape (from Navidad to Bebés)
    # Excluding: Black Friday, Solo X hoy, Ofertas del Mes, Combos
    MAIN_CATEGORIES = [
        "Navidad",
        "Muebles",
        "Electrohogar",
        "Electrónica",
        "Tecnología",
        "Hogar",
        "Herramientas",
        "Dormitorio y Baño",
        "Juguetería",
        "Camping",
        "Iluminación",
        "Deportes y Ocio",
        "Decoración",
        "Viaje y Regalos",
        "Exteriores",
        "Limpieza y Bioseguridad",
        "Oficina",
        "Bebés"
    ]
    
    def __init__(self, headless: bool = True):
        """
        Initialize scraper with Selenium WebDriver.
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
        self.results: List[Dict] = []
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def close_driver(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            
    def get_category_links(self) -> List[Dict[str, str]]:
        """
        Generate main category links based on known category names.
        
        Returns:
            List of dictionaries with category name and URL
        """
        print("Generating category URLs...")
        
        # Mapping of category names to their URL slugs
        # Based on inspection of the Multicenter website
        category_mapping = {
            "Navidad": "navidad",
            "Muebles": "muebles",
            "Electrohogar": "electrohogar",
            "Tecnología": "tecnologia",
            "Hogar": "hogar",
            "Herramientas": "herramientas",
            "Dormitorio y Baño": "dormitorio-y-bano",
            "Juguetería": "jugueteria",
            "Camping": "camping",
            "Iluminación": "iluminacion",
            "Deportes y Ocio": "deportes-y-ocio",
            "Decoración": "decoracion",
            "Viaje y Regalos": "viaje-y-regalos",
            "Exteriores": "exteriores",
            "Limpieza y Bioseguridad": "limpieza---bioseguridad",
            "Oficina": "oficina",
            "Bebés": "bebes"
        }
        
        categories = []
        for name, slug in category_mapping.items():
            url = f"{self.BASE_URL}/{slug}"
            categories.append({
                'name': name,
                'url': url
            })
            print(f"  - {name}: {url}")
            
        return categories
        
    def extract_product_count(self, url: str, category_name: str) -> Optional[int]:
        """
        Extract product count from a category page.
        
        Args:
            url: Category page URL
            category_name: Name of the category
            
        Returns:
            Number of products or None if not found
        """
        print(f"\nProcessing: {category_name}")
        print(f"URL: {url}")
        
        try:
            self.driver.get(url)
            
            # Wait for the page to load and product count to appear
            time.sleep(4)  # Increased delay for slower pages
            
            # Try multiple patterns to find product count
            patterns = [
                r'(\d+)\s+productos',
                r'(\d+)\s+Productos',
                r'(\d+)\s+PRODUCTOS',
                r'(\d{1,5})\s+resultados',
                r'(\d{1,5})\s+items',
            ]
            
            page_source = self.driver.page_source
            
            for pattern in patterns:
                match = re.search(pattern, page_source)
                if match:
                    count = int(match.group(1))
                    print(f"  ✓ Found {count} products (pattern match)")
                    return count
                    
            # Alternative: Look for result count element
            try:
                # Common class patterns for product counts in e-commerce sites
                selectors = [
                    ".vtex-search-result-3-x-totalProducts",
                    "[class*='totalProducts']",
                    "[class*='product-count']",
                    "[class*='resultado']",
                    "[class*='showing']",
                    ".search-result-totalizer",
                ]
                
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for element in elements:
                            text = element.text.strip()
                            if text:
                                # Try to extract number from text
                                match = re.search(r'(\d+)', text)
                                if match:
                                    count = int(match.group(1))
                                    # Filter out unreasonably small numbers that might be page numbers
                                    if count > 0:
                                        print(f"  ✓ Found {count} products via selector ({selector})")
                                        return count
                    except NoSuchElementException:
                        continue
                        
            except Exception as e:
                pass
            
            # Last resort: count actual product items on the page
            # This gives us at least some indication even if total is not shown
            try:
                product_items = self.driver.find_elements(By.CSS_SELECTOR, "[class*='productSummary']")
                if not product_items:
                    product_items = self.driver.find_elements(By.CSS_SELECTOR, "[class*='product-item']")
                
                if len(product_items) > 0:
                    print(f"  ⚠ Found {len(product_items)} products on page (actual count may be higher)")
                    return len(product_items)
            except Exception as e:
                pass
                
            print("  ✗ Could not find product count")
            return None
            
        except Exception as e:
            print(f"  ✗ Error processing {category_name}: {e}")
            return None
            
    def scrape(self):
        """Main scraping method."""
        print("=" * 60)
        print("Multicenter Category Scraper")
        print("=" * 60)
        
        try:
            self.setup_driver()
            
            # Get all main category links
            categories = self.get_category_links()
            
            print(f"\nFound {len(categories)} categories to scrape")
            print("-" * 60)
            
            # Process each category
            for i, category in enumerate(categories, 1):
                print(f"\n[{i}/{len(categories)}] Processing: {category['name']}")
                
                product_count = self.extract_product_count(
                    category['url'],
                    category['name']
                )
                
                result = {
                    'category_name': category['name'],
                    'url': category['url'],
                    'product_count': product_count if product_count is not None else 0,
                    'scraped_at': datetime.now().isoformat()
                }
                
                self.results.append(result)
                
                # Be respectful with delays
                time.sleep(2)
                
        finally:
            self.close_driver()
            
    def save_to_csv(self, filename: str = 'multicenter_categories_report.csv'):
        """
        Save results to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        if not self.results:
            print("\nNo results to save")
            return
            
        filepath = filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['category_name', 'product_count', 'url', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
                
        print(f"\n✓ Results saved to: {filepath}")
        
    def print_summary(self):
        """Print a summary of the scraping results."""
        if not self.results:
            print("\nNo results to display")
            return
            
        print("\n" + "=" * 60)
        print("SCRAPING SUMMARY")
        print("=" * 60)
        
        total_products = sum(r['product_count'] for r in self.results)
        
        print(f"\nCategories scraped: {len(self.results)}")
        print(f"Total products found: {total_products:,}")
        print("\nBreakdown by category:")
        print("-" * 60)
        
        # Sort by product count descending
        sorted_results = sorted(self.results, key=lambda x: x['product_count'], reverse=True)
        
        for result in sorted_results:
            print(f"  {result['category_name']:<20} {result['product_count']:>6,} products")
            
        print("=" * 60)


def main():
    """Main entry point."""
    scraper = MulticenterCategoryScraper(headless=True)
    
    try:
        scraper.scrape()
        scraper.print_summary()
        scraper.save_to_csv()
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        scraper.close_driver()
        
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        scraper.close_driver()
        

if __name__ == '__main__':
    main()
