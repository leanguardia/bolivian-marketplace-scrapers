"""
Venbo Web Scraper
Scrapes product information from Venbo.shop and saves to CSV

This scraper navigates through the multi-level category tree starting from
https://venbo.shop/categorias/ and extracts product information from all
product listing pages.

Usage:
    python scraper_venbo.py
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin, urlparse
import logging
from typing import List, Dict, Optional, Set
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VenboScraper:
    """Web scraper for Venbo.shop product pages"""
    
    def __init__(self, base_url: str = "https://venbo.shop", delay: float = 1.5):
        """
        Initialize the scraper
        
        Args:
            base_url: The base URL of the store
            delay: Delay between requests in seconds
        """
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.visited_urls: Set[str] = set()
        self.categories_found: Dict[str, Dict] = {}
        self.products: List[Dict] = []
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a page
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if error
        """
        if url in self.visited_urls:
            logger.debug(f"Already visited: {url}")
            return None
            
        try:
            logger.info(f"Fetching: {url}")
            time.sleep(self.delay)
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            self.visited_urls.add(url)
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def is_product_listing_page(self, soup: BeautifulSoup) -> bool:
        """
        Check if the page is a product listing page
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            True if this is a product listing page (contains "Showing all X results")
        """
        # Check for "Showing all X results" text
        page_text = soup.get_text()
        if re.search(r'Showing all \d+ results', page_text, re.IGNORECASE):
            return True
        
        # Also check for woocommerce result count element
        result_count = soup.find('p', class_='woocommerce-result-count')
        if result_count:
            return True
            
        return False
    
    def extract_category_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """
        Extract all category links from a page
        
        Args:
            soup: BeautifulSoup object of the page
            base_url: Base URL for resolving relative links
            
        Returns:
            List of category URLs
        """
        category_links = []
        
        # Find all links that match the category URL pattern
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Check if it's a category link (/cat-producto/)
            if '/cat-producto/' in href:
                full_url = urljoin(base_url, href)
                
                # Normalize URL (remove trailing slash, fragments, etc.)
                full_url = full_url.rstrip('/')
                
                if full_url not in self.visited_urls:
                    category_links.append(full_url)
        
        return list(set(category_links))  # Remove duplicates
    
    def extract_price(self, price_text: str) -> Dict[str, Optional[str]]:
        """
        Extract price information from text
        
        Args:
            price_text: Text containing price
            
        Returns:
            Dictionary with regular_price and sale_price
        """
        prices = {
            'regular_price': None,
            'sale_price': None
        }
        
        # Remove HTML tags if any
        clean_text = re.sub(r'<[^>]+>', '', price_text)
        
        # Find all prices (numbers before 'Bs')
        price_matches = re.findall(r'([\d,\.]+)\s*Bs', clean_text)
        
        if price_matches:
            # Clean up prices (remove commas and extra whitespace)
            clean_prices = [p.replace(',', '').strip() for p in price_matches]
            
            if len(clean_prices) >= 2:
                # First is regular, second is sale
                prices['regular_price'] = clean_prices[0]
                prices['sale_price'] = clean_prices[1]
            else:
                # Only one price
                prices['regular_price'] = clean_prices[0]
                prices['sale_price'] = clean_prices[0]
        
        return prices
    
    def extract_product_info(self, product_element, category_url: str) -> Optional[Dict]:
        """
        Extract product information from a product element
        
        Args:
            product_element: BeautifulSoup element containing product
            category_url: URL of the category being scraped
            
        Returns:
            Dictionary with product information
        """
        try:
            product_data = {}
            
            # Category URL
            product_data['category_url'] = category_url
            
            # Product title
            title_elem = product_element.find('h5')
            if not title_elem:
                title_elem = product_element.find('h2', class_='woocommerce-loop-product__title')
            if not title_elem:
                title_elem = product_element.find(class_='product_details')
                if title_elem:
                    title_elem = title_elem.find('h5')
            product_data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Product URL
            link_elem = product_element.find('a', class_='product_item_link')
            if not link_elem:
                link_elem = product_element.find('a', href=True)
            
            if link_elem and 'href' in link_elem.attrs:
                product_data['url'] = link_elem['href']
            else:
                product_data['url'] = 'N/A'
            
            # Price
            price_elem = product_element.find('span', class_='product_price')
            if not price_elem:
                price_elem = product_element.find('span', class_='price')
            
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                prices = self.extract_price(price_text)
                product_data['regular_price'] = prices['regular_price'] or 'N/A'
                product_data['sale_price'] = prices['sale_price'] or 'N/A'
                
                # Check if on sale (has del tag or ins tag)
                if price_elem.find('del') or price_elem.find('ins'):
                    product_data['on_sale'] = 'Yes'
                    # Extract discount percentage if available
                    discount_match = re.search(r'\(([^)]+%)\)', price_text)
                    if discount_match:
                        product_data['discount'] = discount_match.group(1)
                    else:
                        product_data['discount'] = 'N/A'
                else:
                    product_data['on_sale'] = 'No'
                    product_data['discount'] = 'N/A'
            else:
                product_data['regular_price'] = 'N/A'
                product_data['sale_price'] = 'N/A'
                product_data['on_sale'] = 'No'
                product_data['discount'] = 'N/A'
            
            # Product ID (from class or data attributes)
            classes = product_element.get('class', [])
            product_id = 'N/A'
            for cls in classes:
                if cls.startswith('post-'):
                    product_id = cls.replace('post-', '')
                    break
            product_data['product_id'] = product_id
            
            # In stock status
            if 'instock' in ' '.join(classes):
                product_data['in_stock'] = 'Yes'
            elif 'outofstock' in ' '.join(classes):
                product_data['in_stock'] = 'No'
            else:
                product_data['in_stock'] = 'Unknown'
            
            # Image URL
            img_elem = product_element.find('img')
            if img_elem:
                # Try data-src first (lazy loading), then src
                img_url = img_elem.get('data-src') or img_elem.get('src')
                product_data['image_url'] = img_url if img_url else 'N/A'
            else:
                product_data['image_url'] = 'N/A'
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return None
    
    def scrape_product_listing(self, url: str) -> List[Dict]:
        """
        Scrape all products from a product listing page
        
        Args:
            url: URL of the product listing page
            
        Returns:
            List of product dictionaries
        """
        products = []
        soup = self.get_page(url)
        
        if not soup:
            return products
        
        # Find all product items
        # Look for various product container classes used by WooCommerce/Virtue theme
        product_containers = soup.find_all(['li', 'div'], class_=re.compile(r'product|kad_product'))
        
        logger.info(f"Found {len(product_containers)} products on {url}")
        
        for product_elem in product_containers:
            product_info = self.extract_product_info(product_elem, url)
            if product_info:
                products.append(product_info)
        
        return products
    
    def explore_category(self, category_url: str, level: int = 0) -> None:
        """
        Recursively explore a category and its subcategories
        
        Args:
            category_url: URL of the category to explore
            level: Current depth level in the category tree
        """
        indent = "  " * level
        logger.info(f"{indent}Exploring: {category_url}")
        
        soup = self.get_page(category_url)
        if not soup:
            return
        
        # Check if this is a product listing page
        if self.is_product_listing_page(soup):
            logger.info(f"{indent}→ This is a PRODUCT LISTING page")
            
            # Extract product count
            result_count = soup.find('p', class_='woocommerce-result-count')
            product_count = 0
            if result_count:
                count_match = re.search(r'(\d+)\s+results?', result_count.get_text())
                if count_match:
                    product_count = int(count_match.group(1))
            else:
                # Try alternative pattern in page text
                page_text = soup.get_text()
                count_match = re.search(r'Showing all (\d+) results', page_text, re.IGNORECASE)
                if count_match:
                    product_count = int(count_match.group(1))
            
            # Store category info
            self.categories_found[category_url] = {
                'url': category_url,
                'product_count': product_count,
                'level': level
            }
            
            logger.info(f"{indent}→ Found {product_count} products in this category")
            
            # Scrape products from this page
            products = self.scrape_product_listing(category_url)
            self.products.extend(products)
            
        else:
            logger.info(f"{indent}→ This is a CATEGORY NAVIGATION page")
        
        # Extract and explore subcategories
        subcategory_links = self.extract_category_links(soup, category_url)
        
        if subcategory_links:
            logger.info(f"{indent}→ Found {len(subcategory_links)} subcategory links")
            for subcat_url in subcategory_links:
                self.explore_category(subcat_url, level + 1)
        else:
            logger.info(f"{indent}→ No more subcategories")
    
    def scrape(self) -> None:
        """
        Main scraping method - starts from the categories page
        """
        categories_page = f"{self.base_url}/categorias/"
        
        logger.info("=" * 80)
        logger.info("Starting Venbo scraper")
        logger.info(f"Base URL: {self.base_url}")
        logger.info("=" * 80)
        
        # Get the main categories page
        soup = self.get_page(categories_page)
        if not soup:
            logger.error("Failed to fetch categories page")
            return
        
        # Extract all category links from the main page
        main_category_links = self.extract_category_links(soup, categories_page)
        
        logger.info(f"Found {len(main_category_links)} main category links")
        
        # Explore each main category recursively
        for idx, category_url in enumerate(main_category_links, 1):
            logger.info(f"\n{'='*80}")
            logger.info(f"Main Category {idx}/{len(main_category_links)}")
            logger.info(f"{'='*80}")
            self.explore_category(category_url)
        
        logger.info("\n" + "=" * 80)
        logger.info("Scraping completed")
        logger.info(f"Total categories with products found: {len(self.categories_found)}")
        logger.info(f"Total products scraped: {len(self.products)}")
        logger.info("=" * 80)
    
    def save_to_csv(self, filename: str = 'venbo_products.csv') -> None:
        """
        Save scraped products to CSV file
        
        Args:
            filename: Output CSV filename
        """
        if not self.products:
            logger.warning("No products to save")
            return
        
        # Define CSV columns
        fieldnames = [
            'product_id',
            'title',
            'url',
            'regular_price',
            'sale_price',
            'on_sale',
            'discount',
            'in_stock',
            'image_url',
            'category_url'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.products)
            
            logger.info(f"Products saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
    
    def save_category_report(self, filename: str = 'venbo_categories_report.txt') -> None:
        """
        Save a report of categories and their product counts
        
        Args:
            filename: Output report filename
        """
        if not self.categories_found:
            logger.warning("No categories to report")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("VENBO CATEGORIES REPORT\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Total categories with products: {len(self.categories_found)}\n")
                f.write(f"Total products found: {len(self.products)}\n\n")
                f.write("=" * 80 + "\n\n")
                
                # Sort by level, then by product count
                sorted_categories = sorted(
                    self.categories_found.values(),
                    key=lambda x: (x['level'], -x['product_count'])
                )
                
                for cat in sorted_categories:
                    indent = "  " * cat['level']
                    f.write(f"{indent}[{cat['product_count']} products] {cat['url']}\n")
            
            logger.info(f"Category report saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving category report: {e}")


def main():
    """Main function"""
    # Initialize scraper
    scraper = VenboScraper(base_url="https://venbo.shop", delay=1.5)
    
    # Start scraping
    scraper.scrape()
    
    # Save results
    scraper.save_to_csv('venbo_products.csv')
    scraper.save_category_report('venbo_categories_report.txt')
    
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    print(f"Categories with products: {len(scraper.categories_found)}")
    print(f"Total products scraped: {len(scraper.products)}")
    print(f"URLs visited: {len(scraper.visited_urls)}")
    print("\nOutput files:")
    print("  - venbo_products.csv (product data)")
    print("  - venbo_categories_report.txt (category report)")
    print("=" * 80)


if __name__ == "__main__":
    main()
