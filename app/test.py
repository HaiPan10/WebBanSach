import requests

proxies = {
  'http': 'http://10.10.1.10:3128',
}

requests.get('http://example.org', proxies=proxies,timeout=None)
