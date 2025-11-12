#!/bin/bash

# Boliviamart Web Scraper - Installation & Setup Script
# This script helps you set up and run the scraper quickly

echo "=========================================="
echo "Boliviamart Web Scraper - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.7 or higher"
    exit 1
fi

echo ""
echo "=========================================="
echo "Installing Dependencies"
echo "=========================================="
echo ""

# Install dependencies
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "=========================================="
echo "Running Validation Tests"
echo "=========================================="
echo ""

# Run tests
python3 test_scraper.py

if [ $? -ne 0 ]; then
    echo ""
    echo "Warning: Some tests failed"
    echo "The scraper may not work properly"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "You can now run the scraper:"
echo ""
echo "  Basic usage:"
echo "    python3 scraper_boliviamart.py"
echo ""
echo "  Custom URL:"
echo "    python3 scraper_boliviamart.py https://www.boliviamart.com/tienda/"
echo ""
echo "  Run examples:"
echo "    python3 example_usage.py"
echo ""
echo "=========================================="
echo ""
read -p "Would you like to run a test scrape now? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Running test scrape (first page only)..."
    echo ""
    python3 -c "
from scraper_boliviamart import BoliviamartScraper
scraper = BoliviamartScraper('https://www.boliviamart.com/tienda/', page_size=12, delay=1.0)
products = scraper.scrape_page('https://www.boliviamart.com/tienda/?count=12')
print(f'\nTest scrape complete: {len(products)} products extracted')
if products:
    print(f'\nFirst product: {products[0][\"title\"]}')
    scraper.save_to_csv(products, 'test_sample.csv')
    print('Sample saved to: test_sample.csv')
"
    echo ""
    echo "Test complete! Check test_sample.csv"
fi

echo ""
echo "Setup finished successfully!"
