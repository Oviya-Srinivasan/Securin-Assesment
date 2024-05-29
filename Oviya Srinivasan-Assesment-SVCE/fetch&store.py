import requests
import json
from pymongo import MongoClient

def fetch_and_save_cve_data():
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("API connection successful.")
            json_data = response.json()
            
            # Save JSON data to a file
            with open("cvedata.json", "w") as file:
                json.dump(json_data, file, indent=4)
                
            print("CVE data saved to cvedata.json")
        else:
            print(f"Failed to fetch data from API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching data from API: {e}")

def store_json_data_to_db():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["NVD"]
    cve_collection = db["CVE"]
    
    try:
        # Open the JSON file and load the data
        with open("cvedata.json", "r") as file:
            json_data = json.load(file)
            
            # Extract CVE entries from the JSON data
            cve_entries = json_data.get("vulnerabilities", [])
            
            # Insert each CVE entry into the database
            if cve_entries:
                result = cve_collection.insert_many(cve_entries)
                print(f"{len(result.inserted_ids)} documents inserted into the database.")
            else:
                print("No CVE entries found in the JSON data.")
    except Exception as e:
        print(f"Error storing JSON data to the database: {e}")

if __name__ == "__main__":
    fetch_and_save_cve_data()
    store_json_data_to_db()
