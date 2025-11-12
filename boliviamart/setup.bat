@echo off
REM Boliviamart Web Scraper - Setup Script for Windows

echo ==========================================
echo Boliviamart Web Scraper - Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Installing Dependencies
echo ==========================================
echo.

REM Install dependencies
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Running Validation Tests
echo ==========================================
echo.

REM Run tests
python test_scraper.py
if errorlevel 1 (
    echo.
    echo Warning: Some tests failed
    echo The scraper may not work properly
    echo.
    set /p continue="Do you want to continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo You can now run the scraper:
echo.
echo   Basic usage:
echo     python scraper_boliviamart.py
echo.
echo   Custom URL:
echo     python scraper_boliviamart.py https://www.boliviamart.com/tienda/
echo.
echo   Run examples:
echo     python example_usage.py
echo.
echo ==========================================
echo.
set /p test="Would you like to run a test scrape now? (y/n): "

if /i "%test%"=="y" (
    echo.
    echo Running test scrape (first page only)...
    echo.
    python -c "from scraper_boliviamart import BoliviamartScraper; scraper = BoliviamartScraper('https://www.boliviamart.com/tienda/', page_size=12, delay=1.0); products = scraper.scrape_page('https://www.boliviamart.com/tienda/?count=12'); print(f'\nTest scrape complete: {len(products)} products extracted'); print(f'\nFirst product: {products[0][\"title\"]}') if products else None; scraper.save_to_csv(products, 'test_sample.csv') if products else None; print('Sample saved to: test_sample.csv') if products else None"
    echo.
    echo Test complete! Check test_sample.csv
)

echo.
echo Setup finished successfully!
pause
