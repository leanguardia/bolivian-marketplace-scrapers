#!/usr/bin/env python3
"""
Dismac Category Scraper - Example Usage

This script shows different ways to use the scraper.
"""

import sys
from scraper_dismac import DismacCategoryScraper


def run_full_scrape():
    """Run the complete scraper on all categories."""
    print("="*80)
    print("FULL SCRAPE - All Categories")
    print("="*80)
    print("This will scrape all 200+ categories from Dismac.")
    print("Estimated time: 5-10 minutes")
    print()
    
    response = input("Continue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    scraper = DismacCategoryScraper()
    scraper.scrape()
    scraper.save_to_csv()
    scraper.print_summary()


def run_limited_scrape(max_categories=20):
    """Run scraper on limited number of categories."""
    print("="*80)
    print(f"LIMITED SCRAPE - First {max_categories} Categories")
    print("="*80)
    
    scraper = DismacCategoryScraper()
    
    # Fetch and extract categories
    html = scraper.fetch_page(scraper.CATEGORIES_URL)
    if not html:
        print("Failed to fetch categories page")
        return
    
    categories = scraper.extract_category_links(html)
    print(f"Found {len(categories)} total categories")
    print(f"Processing first {max_categories}...\n")
    
    # Process limited set
    for i, category in enumerate(categories[:max_categories], 1):
        print(f"[{i}/{max_categories}] Processing: {category['name']}")
        result = scraper.process_category(category)
        if result:
            scraper.results.append(result)
        print()
    
    # Save and print summary
    filename = f"dismac_categories_limited_{max_categories}.csv"
    scraper.save_to_csv(filename)
    scraper.print_summary()


def show_menu():
    """Display interactive menu."""
    print()
    print("="*80)
    print("DISMAC CATEGORY SCRAPER - Menu")
    print("="*80)
    print()
    print("1. Full Scrape (all categories, ~5-10 minutes)")
    print("2. Limited Scrape - 20 categories (~1 minute)")
    print("3. Limited Scrape - 50 categories (~2-3 minutes)")
    print("4. Quick Test - 5 categories (~30 seconds)")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ")
    
    if choice == '1':
        run_full_scrape()
    elif choice == '2':
        run_limited_scrape(20)
    elif choice == '3':
        run_limited_scrape(50)
    elif choice == '4':
        run_limited_scrape(5)
    elif choice == '5':
        print("Exiting...")
        sys.exit(0)
    else:
        print("Invalid option. Please try again.")
        show_menu()


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Command line argument provided
        arg = sys.argv[1]
        
        if arg == '--full':
            run_full_scrape()
        elif arg == '--test':
            run_limited_scrape(5)
        elif arg.startswith('--limit='):
            try:
                limit = int(arg.split('=')[1])
                run_limited_scrape(limit)
            except (ValueError, IndexError):
                print(f"Invalid limit value: {arg}")
                print("Usage: --limit=N where N is a number")
        else:
            print("Unknown argument:", arg)
            print()
            print("Usage:")
            print("  python example_usage.py              # Interactive menu")
            print("  python example_usage.py --full       # Full scrape")
            print("  python example_usage.py --test       # Quick test (5 categories)")
            print("  python example_usage.py --limit=20   # Limited scrape")
    else:
        # No arguments - show interactive menu
        show_menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
