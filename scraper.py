import time
import pandas as pd
import requests
from typing import Optional
from io import StringIO

def fetch_screener_data(link: str) -> pd.DataFrame:
    """
    Fetch data from screener.in by scraping multiple pages.
    
    Args:
        link (str): The screener.in URL to scrape
        
    Returns:
        pd.DataFrame: Combined data from all pages
        
    Raises:
        Exception: If there's an error fetching the data
    """
    try:
        # Headers to mimic a browser request and prevent caching
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        data = pd.DataFrame()
        current_page = 1
        page_limit = 100
        
        while current_page < page_limit:
            url = f'{link}?page={current_page}'
            
            # Fetch the HTML content with headers
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an error for bad status codes
            
            # Read all tables from the HTML content
            all_tables = pd.read_html(StringIO(response.text), flavor='bs4')
            
            if not all_tables:
                # No tables found, we've reached the end
                break
                
            combined_df = pd.concat(all_tables)

            # Drop rows where S.No. is null
            if 'S.No.' in combined_df.columns:
                combined_df = combined_df.drop(
                    combined_df[combined_df['S.No.'].isnull()].index)
            
            # If less than 26 rows, this is the last page
            if len(combined_df.index) < 26:
                data = pd.concat([data, combined_df], axis=0)
                break

            data = pd.concat([data, combined_df], axis=0)
            current_page += 1
            
            # Sleep to avoid overwhelming the server
            time.sleep(3)
        
        # Clean up the data - remove duplicate headers
        if 'S.No.' in data.columns:
            data = data.iloc[0:].drop(data[data['S.No.'] == 'S.No.'].index)
        
        # Reset index
        data = data.reset_index(drop=True)
        
        return data
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error fetching data: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")


def validate_screener_url(url: str) -> bool:
    """
    Validate if the URL is from screener.in
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid screener.in URL, False otherwise
    """
    return 'screener.in' in url.lower()


def convert_to_csv(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to CSV format
    
    Args:
        df (pd.DataFrame): DataFrame to convert
        
    Returns:
        str: CSV formatted string
    """
    return df.to_csv(index=False)


def convert_to_json(df: pd.DataFrame) -> str:
    """
    Convert DataFrame to JSON format
    
    Args:
        df (pd.DataFrame): DataFrame to convert
        
    Returns:
        str: JSON formatted string
    """
    return df.to_json(orient='records', indent=2)


if __name__ == "__main__":
    # Test the scraper
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    
    screen_url = 'https://www.screener.in/screens/2448025/sales-profit-20-eps-up/'
    df = fetch_screener_data(screen_url)
    print(df.head())
    print(f"\nTotal rows: {len(df)}")
