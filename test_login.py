import requests


r = requests.post('https://127.0.0.1:8080/auth/login', data={'user_name': 'ruben', 'password': '123'}, verify=False)
print(r.content)