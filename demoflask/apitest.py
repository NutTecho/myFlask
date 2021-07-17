import requests
url ="http://localhost:5000/weather"
response = requests.get(url)
print(response.json())