import requests
from requests.auth import HTTPBasicAuth

# Your Companies House API key
api_key = 'YOUR_API_KEY'

# Example: Search for "John Cena" company
search_query = "John Cena Meme"

url = f"https://api.company-information.service.gov.uk/search/companies?q={search_query}"

response = requests.get(url, auth=HTTPBasicAuth(api_key, ''))

if response.status_code == 200:
    results = response.json()
    for item in results['items']:
        print(f"Name: {item['title']}")
        print(f"Company Number: {item['company_number']}")
        print(f"Status: {item['company_status']}")
        print(f"Address: {item['address_snippet']}")
        print("-" * 30)
else:
    print(f"Error: {response.status_code} - {response.text}")
