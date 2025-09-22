import requests

url = 'https://dw2-wendel-mab.vercel.app/api/test_basic'
print('Chamando', url)
resp = requests.get(url, timeout=15)
print('Status:', resp.status_code)
print('Body:', resp.text)
