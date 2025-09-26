import requests as req

url = "http://localhost:8008/comp370_hw3.txt"

print(req.get(url).text)