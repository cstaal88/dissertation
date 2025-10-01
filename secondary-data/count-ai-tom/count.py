import time
import webbrowser
from urllib.parse import quote

print("Opening a G-Scholar tab per year ...")

def search_multiple_years(list_a, list_b, start_year, end_year):
    for year in range(start_year, end_year + 1):
        print(f"\nSearching for year {year}...")
        
        # Build query
        query_a = " OR ".join([f'"{term}"' if " " in term else term for term in list_a])
        query_b = " OR ".join([f'"{term}"' if " " in term else term for term in list_b])
        final_query = f"({query_a}) AND ({query_b})"
        
        # Build URL
        encoded_query = quote(final_query)
        url = f"https://scholar.google.com/scholar?q={encoded_query}&as_ylo={year}&as_yhi={year}"
        
        print(f"Opening: {url}")
        webbrowser.open(url)
        
        # Wait before next search to avoid being blocked
        if year < end_year:
            print("Waiting 15 seconds before next search...")
            time.sleep(15)

# Define the search terms
list_a = [
    "ai",
    "llm*",
    "artificial intelligence",
    "large language model*"
]

list_b = [
    "theory of mind",
    "mentaliz*"
]

# This will open tabs for each year from 2020-2024
search_multiple_years(list_a, list_b, 2000, 2024)