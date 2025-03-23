import csv
import logging
from typing import List
from pathlib import Path
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

@dataclass
class Config:
    CHROME_DRIVER_PATH: str = r"C:\Users\SudharsanDhakshinamo\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    COUNTRIES_FILE: str = "country.txt"
    BASE_URL: str = "https://www.worldometers.info/world-population/{}-population/"
    OUTPUT_FILES: List[str] = ("Historical_Population.csv", "Foarcast_Population.csv", "City_Population.csv")

def setup_webdriver(driver_path: str) -> webdriver.Chrome:
    """Initialize and return Chrome webdriver."""
    try:
        service = Service(driver_path)
        return webdriver.Chrome(service=service)
    except WebDriverException as e:
        logging.error(f"Failed to initialize WebDriver: {e}")
        raise

def read_countries(file_path: str) -> List[str]:
    """Read country names from file."""
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        logging.error(f"Countries file not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading countries file: {e}")
        raise

def scrape_country_data(driver: webdriver.Chrome, country: str, country_index: int) -> List[List[str]]:
    """Scrape population data for a single country."""
    try:
        url = Config.BASE_URL.format(country)
        logging.info(f"Scraping data for {country} from {url}")
        driver.get(url)
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        containers = soup.find_all("div", class_="table-responsive")
        
        all_table_data = []
        for container in containers:
            table_data = []
            for body in container.find_all("tbody"):
                for row in body.find_all("tr"):
                    cells = [cell.text.strip() for cell in row.find_all("td")]
                    if cells:
                        # Add country index at the beginning of each row
                        cells.insert(0, str(country_index))
                        table_data.append(cells)
            all_table_data.append(table_data)
        
        return all_table_data
    except Exception as e:
        logging.error(f"Error scraping data for {country}: {e}")
        return []

def write_to_csv(data: List[List[str]], filename: str):
    """Write data to CSV file."""
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerows(data)
    except Exception as e:
        logging.error(f"Error writing to {filename}: {e}")
        raise

def process_countries(countries: List[str]):
    """Process all countries and save their data."""
    driver = None
    try:
        driver = setup_webdriver(Config.CHROME_DRIVER_PATH)
        
        # Initialize CSV files
        for filename in Config.OUTPUT_FILES:
            Path(filename).write_text("", encoding="utf-8")
        
        for index, country in enumerate(countries, start=1):
            try:
                tables_data = scrape_country_data(driver, country, index)
                
                # Write each table's data to its respective CSV file
                for table_index, table_data in enumerate(tables_data):
                    if table_data:
                        write_to_csv(table_data, Config.OUTPUT_FILES[table_index])
                        logging.info(f"Data written for {country} (index: {index}) to {Config.OUTPUT_FILES[table_index]}")
            
            except Exception as e:
                logging.error(f"Failed to process country {country}: {e}")
                continue
                
    except Exception as e:
        logging.error(f"Process failed: {e}")
    finally:
        if driver:
            driver.quit()

def main():
    """Main entry point of the script."""
    try:
        countries = read_countries(Config.COUNTRIES_FILE)
        process_countries(countries)
        logging.info("Processing completed successfully")
    except Exception as e:
        logging.error(f"Script failed: {e}")
        raise


main()