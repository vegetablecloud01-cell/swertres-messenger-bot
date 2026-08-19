import json
import os
from datetime import datetime
import requests

def scrape_swertres():
    # Updated source endpoint to the developer interface on pcsolotto.org
    url = "https://pcsolotto.org" 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    
    # Default structure fallback if tracking errors happen
    results = {"11am": "No result", "4pm": "No result", "9pm": "No result", "updated": ""}
    
    try:
        # Request live stream from the updated target site
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            results["updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Target games inside the structure
            # PCSO matches map to games like '3D Lotto' or 'Swertres'
            for game in data.get("games", []):
                if "3D" in game.get("name", "") or "Swertres" in game.get("name", ""):
                    # Capture exact draws based on official PCSO slots
                    draws = game.get("draws", {})
                    results["11am"] = draws.get("2pm", "No result") # PCSO renamed the 11AM slot to 2PM in recent schedule shifts
                    results["4pm"] = draws.get("5pm", "No result")  # PCSO shifted the 4PM slot to 5PM
                    results["9pm"] = draws.get("9pm", "No result")
                    
    except Exception as e:
        print(f"Error accessing updated URL data: {e}")
        
    # Write directly to local file repository for your Render server to read
    with open("results.json", "w") as f:
        json.dump(results, f, indent=4)

if __name__ == "__main__":
    scrape_swertres()
