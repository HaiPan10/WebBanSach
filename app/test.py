import requests
from app import dao, app

# proxies = {
#   'http': 'http://10.10.1.10:3128',
# }
#
# requests.get('http://example.org', proxies=proxies,timeout=None)
with app.app_context():
  print(dao.check_user_name('haiphan'))
