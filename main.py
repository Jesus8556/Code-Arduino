import requests

url = 'http://192.168.1.60:8000/api/admin/curso/'
data = requests.get(url)
if data.status_code == 200:
    data = data.json()
    for e in data:
        print(e['id'])
        