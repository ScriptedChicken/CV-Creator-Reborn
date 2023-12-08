import requests
import json

url = r"https://www.seek.co.nz/api/chalice-search/v4/search?siteKey=NZ-Main&where=All+Australia&keywords=Python+Developer"
res = requests.get(url)
print(res.status_code)

with open('listings.json', 'w') as file:
    json.dump(res.json().get('data'), file, indent=4)
