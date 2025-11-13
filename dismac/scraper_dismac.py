#!/usr/bin/env python3
"""
Dismac Category Scraper

This scraper recursively crawls through Dismac's category tree and counts
the number of products in each category, subcategory, and sub-subcategory.

Usage:
    python scraper_dismac.py
"""

import re
import csv
import time
from typing import List, Dict, Set, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
from datetime import datetime


class DismacCategoryScraper:
    """Scrapes Dismac category hierarchy and product counts."""
    
    BASE_URL = "https://www.dismac.com.bo"
    CATEGORIES_URL = f"{BASE_URL}/categorias.html"
    
    def __init__(self):
        """Initialize scraper with session and tracking variables."""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.results: List[Dict] = []
        
    def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch a page with retry logic.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(1)  # Be respectful to the server
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def extract_product_count(self, html: str) -> Optional[int]:
        """
        Extract product count from a product listing page.
        
        Args:
            html: Page HTML content
            
        Returns:
            Number of products or None if not a product page
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check if this is a product listing page (has page-title-wrapper)
        page_title = soup.find('div', class_='page-title-wrapper')
        if not page_title:
            return None
        
        # Look for the product count in JavaScript
        # Pattern: let htmlCount = "44 Productos";
        script_pattern = r'let htmlCount = "(\d+) Productos";'
        match = re.search(script_pattern, html)
        
        if match:
            return int(match.group(1))
        
        # Alternative: look in container-count-items
        count_container = soup.find('div', class_='container-count-items')
        if count_container:
            count_text = count_container.get_text(strip=True)
            match = re.search(r'(\d+)\s+Productos', count_text)
            if match:
                return int(match.group(1))
        
        return None
    
    def extract_category_links(self, html: str) -> List[Dict[str, str]]:
        """
        Extract all category links from the categories page.
        
        Args:
            html: Page HTML content
            
        Returns:
            List of dictionaries with category information
        """
        soup = BeautifulSoup(html, 'html.parser')
        categories = []
        
        # Find all category sections
        # Main categories have class "childs-categories-header"
        category_sections = soup.find_all('div', class_='childs-categories-body')
        
        for section in category_sections:
            # Get the parent category name from the header
            parent_header = section.find_previous('header', class_='childs-categories-header')
            if parent_header:
                parent_h3 = parent_header.find('h3')
                parent_name = parent_h3.get_text(strip=True) if parent_h3 else "Unknown"
                parent_link_tag = parent_header.find('a', class_='view-all-category')
                parent_url = parent_link_tag.get('href') if parent_link_tag else None
                
                # Add parent category
                if parent_url:
                    categories.append({
                        'name': parent_name,
                        'url': parent_url,
                        'level': 1,
                        'parent': None
                    })
                
                # Find child categories
                child_groups = section.find_all('div', class_='childs-categories-group')
                
                for group in child_groups:
                    # Get child category
                    child_link = group.find('a', class_='child-category-name')
                    if child_link:
                        child_name = child_link.find('span').get_text(strip=True) if child_link.find('span') else child_link.get_text(strip=True)
                        child_url = child_link.get('href')
                        
                        categories.append({
                            'name': child_name,
                            'url': child_url,
                            'level': 2,
                            'parent': parent_name
                        })
                        
                        # Find grandchild categories
                        grandchild_list = group.find('ul', class_='grandchild-categories-list')
                        if grandchild_list:
                            grandchild_items = grandchild_list.find_all('li', class_='grandchild-category')
                            
                            for item in grandchild_items:
                                gc_link = item.find('a')
                                if gc_link:
                                    gc_name = gc_link.find('span').get_text(strip=True) if gc_link.find('span') else gc_link.get_text(strip=True)
                                    gc_url = gc_link.get('href')
                                    
                                    categories.append({
                                        'name': gc_name,
                                        'url': gc_url,
                                        'level': 3,
                                        'parent': f"{parent_name} > {child_name}"
                                    })
        
        return categories
    
    def process_category(self, category: Dict[str, str]) -> Dict:
        """
        Process a single category URL to get product count.
        
        Args:
            category: Dictionary with category information
            
        Returns:
            Dictionary with category data and product count
        """
        url = category['url']
        
        # Skip if already visited
        if url in self.visited_urls:
            print(f"  Already visited: {url}")
            return None
        
        self.visited_urls.add(url)
        
        # Fetch the page
        html = self.fetch_page(url)
        if not html:
            return None
        
        # Extract product count
        product_count = self.extract_product_count(html)
        
        result = {
            'category_name': category['name'],
            'level': category['level'],
            'parent': category.get('parent', ''),
            'url': url,
            'product_count': product_count if product_count is not None else 0,
            'scraped_at': datetime.now().isoformat()
        }
        
        # Log result
        indent = "  " * category['level']
        if product_count is not None:
            print(f"{indent}✓ {category['name']}: {product_count} productos")
        else:
            print(f"{indent}○ {category['name']}: No product listing page")
        
        return result
    
    def scrape(self) -> List[Dict]:
        """
        Main scraping method.
        
        Returns:
            List of dictionaries with category and product count data
        """
        print("="*80)
        print("DISMAC CATEGORY SCRAPER")
        print("="*80)
        print(f"Starting scrape at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Categories URL: {self.CATEGORIES_URL}")
        print("="*80)
        print()
        
        # Fetch main categories page
        html = self.fetch_page(self.CATEGORIES_URL)
        if not html:
            print("Failed to fetch main categories page")
            return []
        
        # Extract all category links
        print("Extracting category structure...")
        categories = self.extract_category_links(html)
        print(f"Found {len(categories)} categories to process")
        print()
        
        # Process each category
        print("Processing categories:")
        print("-"*80)
        
        for i, category in enumerate(categories, 1):
            print(f"[{i}/{len(categories)}] Processing: {category['name']}")
            result = self.process_category(category)
            if result:
                self.results.append(result)
            print()
        
        return self.results
    
    def save_to_csv(self, filename: str = "dismac_categories_report.csv"):
        """
        Save results to CSV file.
        
        Args:
            filename: Output CSV filename
        """
        if not self.results:
            print("No results to save")
            return
        
        print("="*80)
        print(f"Saving results to {filename}...")
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['category_name', 'level', 'parent', 'url', 'product_count', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)
        
        print(f"✓ Saved {len(self.results)} categories to {filename}")
    
    def print_summary(self):
        """Print summary statistics."""
        if not self.results:
            print("No results to summarize")
            return
        
        print("="*80)
        print("SUMMARY")
        print("="*80)
        
        total_categories = len(self.results)
        total_products = sum(r['product_count'] for r in self.results)
        categories_with_products = sum(1 for r in self.results if r['product_count'] > 0)
        
        print(f"Total categories processed: {total_categories}")
        print(f"Categories with products: {categories_with_products}")
        print(f"Total products found: {total_products}")
        print()
        
        # Top categories by product count
        print("Top 10 categories by product count:")
        print("-"*80)
        sorted_results = sorted(self.results, key=lambda x: x['product_count'], reverse=True)
        for i, result in enumerate(sorted_results[:10], 1):
            parent_info = f" ({result['parent']})" if result['parent'] else ""
            print(f"{i:2d}. {result['category_name']}{parent_info}: {result['product_count']} productos")
        
        print()
        print("="*80)
        print(f"Scraping completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)


def main():
    """Main entry point."""
    scraper = DismacCategoryScraper()
    
    try:
        # Run the scraper
        results = scraper.scrape()
        
        # Save results
        scraper.save_to_csv()
        
        # Print summary
        scraper.print_summary()
        
    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user")
        if scraper.results:
            print("Saving partial results...")
            scraper.save_to_csv("dismac_categories_report_partial.csv")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
