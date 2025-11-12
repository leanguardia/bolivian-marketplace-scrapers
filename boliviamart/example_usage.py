"""
Example usage of the Boliviamart scraper

This script demonstrates different ways to use the scraper programmatically.
"""

from scraper_boliviamart import BoliviamartScraper
import logging

# Configure logging to see detailed output
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def example_basic_scrape():
    """Example 1: Basic scraping with default settings"""
    print("\n" + "="*60)
    print("Example 1: Basic Scraping")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=32,
        delay=1.0
    )
    
    # Scrape all products
    products = scraper.scrape_all("https://www.boliviamart.com/tienda/")
    
    # Save to CSV
    scraper.save_to_csv(products, 'example_basic_products.csv')
    
    print(f"\nScraped {len(products)} products")
    
    # Show first 3 products
    if products:
        print("\nFirst 3 products:")
        for i, product in enumerate(products[:3], 1):
            print(f"\n{i}. {product['title']}")
            print(f"   Price: Bs.{product['sale_price']}")
            print(f"   Stock: {product['stock_status']}")
            print(f"   URL: {product['url']}")


def example_category_scrape():
    """Example 2: Scraping a specific category"""
    print("\n" + "="*60)
    print("Example 2: Scraping Specific Category (Seguridad)")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/categoria/seguridad/",
        page_size=32,
        delay=1.5  # Slightly longer delay
    )
    
    # Scrape products from security category
    products = scraper.scrape_all("https://www.boliviamart.com/categoria/seguridad/")
    
    # Save to CSV
    scraper.save_to_csv(products, 'example_security_products.csv')
    
    print(f"\nScraped {len(products)} security products")


def example_filter_products():
    """Example 3: Scraping and filtering products"""
    print("\n" + "="*60)
    print("Example 3: Scraping and Filtering Products")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=32,
        delay=1.0
    )
    
    # Scrape all products
    all_products = scraper.scrape_all("https://www.boliviamart.com/tienda/")
    
    # Filter products on sale
    on_sale_products = [p for p in all_products if p['on_sale'] == 'Yes']
    
    # Filter products in stock
    in_stock_products = [p for p in all_products if p['stock_status'] == 'In Stock']
    
    # Filter featured products
    featured_products = [p for p in all_products if p['featured'] == 'Yes']
    
    # Filter products under Bs.500
    affordable_products = []
    for p in all_products:
        try:
            price = float(p['sale_price'].replace(',', ''))
            if price < 500:
                affordable_products.append(p)
        except (ValueError, AttributeError):
            pass
    
    print(f"\nTotal products: {len(all_products)}")
    print(f"Products on sale: {len(on_sale_products)}")
    print(f"Products in stock: {len(in_stock_products)}")
    print(f"Featured products: {len(featured_products)}")
    print(f"Products under Bs.500: {len(affordable_products)}")
    
    # Save filtered results
    if on_sale_products:
        scraper.save_to_csv(on_sale_products, 'example_on_sale_products.csv')
        print("\nOn-sale products saved to: example_on_sale_products.csv")
    
    if affordable_products:
        scraper.save_to_csv(affordable_products, 'example_affordable_products.csv')
        print("Affordable products saved to: example_affordable_products.csv")


def example_price_analysis():
    """Example 4: Price analysis"""
    print("\n" + "="*60)
    print("Example 4: Price Analysis")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=32,
        delay=1.0
    )
    
    # Scrape all products
    products = scraper.scrape_all("https://www.boliviamart.com/tienda/")
    
    # Analyze prices
    prices = []
    for p in products:
        try:
            price = float(p['sale_price'].replace(',', ''))
            prices.append(price)
        except (ValueError, AttributeError):
            pass
    
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        print(f"\nPrice Statistics:")
        print(f"Average price: Bs.{avg_price:.2f}")
        print(f"Minimum price: Bs.{min_price:.2f}")
        print(f"Maximum price: Bs.{max_price:.2f}")
        print(f"Price range: Bs.{max_price - min_price:.2f}")
        
        # Find most expensive product
        most_expensive = max(products, key=lambda x: float(x['sale_price'].replace(',', '')) 
                           if x['sale_price'] != 'N/A' else 0)
        
        # Find cheapest product
        cheapest = min(products, key=lambda x: float(x['sale_price'].replace(',', '')) 
                     if x['sale_price'] != 'N/A' else float('inf'))
        
        print(f"\nMost expensive: {most_expensive['title']} - Bs.{most_expensive['sale_price']}")
        print(f"Cheapest: {cheapest['title']} - Bs.{cheapest['sale_price']}")


def example_single_page():
    """Example 5: Scraping just one page"""
    print("\n" + "="*60)
    print("Example 5: Scraping Single Page")
    print("="*60 + "\n")
    
    # Initialize scraper
    scraper = BoliviamartScraper(
        base_url="https://www.boliviamart.com/tienda/",
        page_size=32,
        delay=1.0
    )
    
    # Scrape only the first page
    url = "https://www.boliviamart.com/tienda/?count=32"
    products = scraper.scrape_page(url)
    
    print(f"\nScraped {len(products)} products from first page")
    
    # Save to CSV
    scraper.save_to_csv(products, 'example_single_page_products.csv')


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("BOLIVIAMART SCRAPER - USAGE EXAMPLES")
    print("="*60)
    
    # Uncomment the examples you want to run:
    
    # Example 1: Basic scraping
    example_basic_scrape()
    
    # Example 2: Category scraping
    # example_category_scrape()
    
    # Example 3: Filtering products
    # example_filter_products()
    
    # Example 4: Price analysis
    # example_price_analysis()
    
    # Example 5: Single page scraping
    # example_single_page()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
