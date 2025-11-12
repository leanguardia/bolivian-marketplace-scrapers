"""
Boliviamart Web Scraper
Scrapes product information from Boliviamart.com and saves to CSV

Usage:
    python scraper_boliviamart.py https://www.boliviamart.com/tienda/
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re
from urllib.parse import urljoin, urlparse, parse_qs
import logging
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BoliviamartScraper:
    """Web scraper for Boliviamart.com product pages"""
    
    def __init__(self, base_url: str, page_size: int = 32, delay: float = 1.0):
        """
        Initialize the scraper
        
        Args:
            base_url: The base URL of the store
            page_size: Number of products per page (max 32)
            delay: Delay between requests in seconds
        """
        self.base_url = base_url
        self.page_size = min(page_size, 32)  # Max is 32
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
    def get_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch and parse a page
        
        Args:
            url: URL to fetch
            
        Returns:
            BeautifulSoup object or None if error
        """
        try:
            logger.info(f"Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
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
        
        # Remove currency symbol and clean text
        clean_text = re.sub(r'[^\d.,\-–]', ' ', price_text)
        
        # Find all numbers (price format: 123.00 or 1,234.00)
        price_matches = re.findall(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?', clean_text)
        
        if price_matches:
            if len(price_matches) >= 2:
                # First is regular, second is sale
                prices['regular_price'] = price_matches[0].replace(',', '')
                prices['sale_price'] = price_matches[1].replace(',', '')
            else:
                # Only one price
                prices['regular_price'] = price_matches[0].replace(',', '')
                prices['sale_price'] = price_matches[0].replace(',', '')
        
        return prices
    
    def extract_product_info(self, product_element) -> Optional[Dict]:
        """
        Extract product information from a product element
        
        Args:
            product_element: BeautifulSoup element containing product
            
        Returns:
            Dictionary with product information
        """
        try:
            product_data = {}
            
            # Product title
            title_elem = product_element.find('h3', class_='woocommerce-loop-product__title')
            product_data['title'] = title_elem.get_text(strip=True) if title_elem else 'N/A'
            
            # Product URL
            link_elem = product_element.find('a', class_='product-loop-title')
            if not link_elem:
                link_elem = product_element.find('a', href=True)
            product_data['url'] = link_elem['href'] if link_elem and 'href' in link_elem.attrs else 'N/A'
            
            # Categories
            category_elem = product_element.find('span', class_='category-list')
            if category_elem:
                categories = [cat.get_text(strip=True) for cat in category_elem.find_all('a')]
                product_data['categories'] = ', '.join(categories)
            else:
                product_data['categories'] = 'N/A'
            
            # Price
            price_elem = product_element.find('span', class_='price')
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                prices = self.extract_price(price_text)
                product_data['regular_price'] = prices['regular_price'] or 'N/A'
                product_data['sale_price'] = prices['sale_price'] or 'N/A'
                
                # Check if on sale
                if product_element.find('div', class_='onsale'):
                    product_data['on_sale'] = 'Yes'
                    # Extract discount percentage if available
                    sale_badge = product_element.find('div', class_='onsale')
                    if sale_badge:
                        product_data['discount'] = sale_badge.get_text(strip=True)
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
            
            # Stock status
            stock_elem = product_element.find('div', class_='stock')
            if stock_elem and 'out-of-stock' in stock_elem.get('class', []):
                product_data['stock_status'] = 'Out of Stock'
            else:
                product_data['stock_status'] = 'In Stock'
            
            # Product SKU (if available in data attributes)
            sku = 'N/A'
            add_to_cart_btn = product_element.find('a', {'data-product_sku': True})
            if add_to_cart_btn:
                sku = add_to_cart_btn.get('data-product_sku', 'N/A')
            product_data['sku'] = sku
            
            # Product ID
            product_id = 'N/A'
            add_to_cart_btn = product_element.find('a', {'data-product_id': True})
            if add_to_cart_btn:
                product_id = add_to_cart_btn.get('data-product_id', 'N/A')
            product_data['product_id'] = product_id
            
            # Rating
            rating_elem = product_element.find('div', class_='star-rating')
            if rating_elem:
                rating_strong = rating_elem.find('strong', class_='rating')
                product_data['rating'] = rating_strong.get_text(strip=True) if rating_strong else '0'
            else:
                product_data['rating'] = '0'
            
            # Featured/Hot
            if product_element.find('div', class_='onhot'):
                product_data['featured'] = 'Yes'
            else:
                product_data['featured'] = 'No'
            
            # Image URL
            img_elem = product_element.find('img', class_='attachment-woocommerce_thumbnail')
            if img_elem and 'src' in img_elem.attrs:
                product_data['image_url'] = img_elem['src']
            else:
                product_data['image_url'] = 'N/A'
            
            return product_data
            
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return None
    
    def get_total_pages(self, soup: BeautifulSoup) -> int:
        """
        Determine total number of pages
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Total number of pages
        """
        try:
            # Look for pagination
            pagination = soup.find('ul', class_='page-numbers')
            if pagination:
                page_links = pagination.find_all('a', class_='page-numbers')
                if page_links:
                    # Get the second to last link (last is usually 'next')
                    page_numbers = []
                    for link in page_links:
                        text = link.get_text(strip=True)
                        if text.isdigit():
                            page_numbers.append(int(text))
                    
                    if page_numbers:
                        return max(page_numbers)
            
            # If no pagination found, assume 1 page
            return 1
            
        except Exception as e:
            logger.error(f"Error getting total pages: {e}")
            return 1
    
    def scrape_page(self, url: str) -> List[Dict]:
        """
        Scrape all products from a single page
        
        Args:
            url: URL of the page to scrape
            
        Returns:
            List of product dictionaries
        """
        products = []
        soup = self.get_page(url)
        
        if not soup:
            return products
        
        # Find all product elements
        product_elements = soup.find_all('li', class_='product-col')
        
        if not product_elements:
            logger.warning(f"No products found on page: {url}")
            return products
        
        logger.info(f"Found {len(product_elements)} products on page")
        
        for product_elem in product_elements:
            product_data = self.extract_product_info(product_elem)
            if product_data:
                products.append(product_data)
        
        return products
    
    def scrape_all(self, start_url: str) -> List[Dict]:
        """
        Scrape all products from all pages
        
        Args:
            start_url: Starting URL
            
        Returns:
            List of all products
        """
        all_products = []
        
        # First, determine URL structure with page size
        parsed_url = urlparse(start_url)
        base_path = parsed_url.path.rstrip('/')
        
        # Fetch first page to determine total pages
        first_page_url = f"{parsed_url.scheme}://{parsed_url.netloc}{base_path}/?count={self.page_size}"
        soup = self.get_page(first_page_url)
        
        if not soup:
            logger.error("Failed to fetch first page")
            return all_products
        
        total_pages = self.get_total_pages(soup)
        logger.info(f"Total pages to scrape: {total_pages}")
        
        # Scrape first page
        logger.info(f"Scraping page 1/{total_pages}")
        products = self.scrape_page(first_page_url)
        all_products.extend(products)
        
        # Scrape remaining pages
        for page_num in range(2, total_pages + 1):
            time.sleep(self.delay)  # Respectful delay
            
            page_url = f"{parsed_url.scheme}://{parsed_url.netloc}{base_path}/page/{page_num}/?count={self.page_size}"
            logger.info(f"Scraping page {page_num}/{total_pages}")
            
            products = self.scrape_page(page_url)
            all_products.extend(products)
        
        logger.info(f"Total products scraped: {len(all_products)}")
        return all_products
    
    def save_to_csv(self, products: List[Dict], filename: str = 'boliviamart_products.csv'):
        """
        Save products to CSV file
        
        Args:
            products: List of product dictionaries
            filename: Output filename
        """
        if not products:
            logger.warning("No products to save")
            return
        
        # Define CSV columns
        fieldnames = [
            'product_id',
            'sku',
            'title',
            'categories',
            'regular_price',
            'sale_price',
            'on_sale',
            'discount',
            'stock_status',
            'rating',
            'featured',
            'url',
            'image_url'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(products)
            
            logger.info(f"Successfully saved {len(products)} products to {filename}")
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")


def main():
    """Main function"""
    import sys
    
    # Default URL
    url = "https://www.boliviamart.com/tienda/"
    
    # Check if URL provided as argument
    if len(sys.argv) > 1:
        url = sys.argv[1]
    
    logger.info(f"Starting Boliviamart scraper for: {url}")
    logger.info("This will scrape all products with pagination size set to 32")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url=url,
        page_size=32,  # Maximum page size
        delay=1.0  # 1 second delay between requests
    )
    
    # Scrape all products
    products = scraper.scrape_all(url)
    
    # Save to CSV
    if products:
        output_filename = 'boliviamart_products.csv'
        scraper.save_to_csv(products, output_filename)
        logger.info(f"Scraping complete! Data saved to {output_filename}")
        logger.info(f"Total products: {len(products)}")
    else:
        logger.error("No products were scraped")


if __name__ == "__main__":
    main()
