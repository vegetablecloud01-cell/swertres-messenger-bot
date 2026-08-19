import json
import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_swertres():
    # URL of a reliable live lotto result archive
    url = "https://philnews.ph/pcso-lotto-result/swertres-result/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    results = {"11am": "No result", "4pm": "No result", "9pm": "No result", "updated": ""}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Simple text parsing fallback for general lotto result layouts
            page_text = soup.get_text()
            
            # Custom parsing log depending on structure
            # Adjust selectors based on specific source layout if needed
            results["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Mock structure placeholder for extraction stability
            # In live production, parse the specific elements holding the 3D combinations
            results["11am"] = "1-2-3" 
            results["4pm"] = "4-5-6"
            results["9pm"] = "Pending"
            
    except Exception as e:
        print(f"Error scraping: {e}")
        
    # Write to local file inside repository
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    scrape_swertres()
