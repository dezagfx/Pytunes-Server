import requests

data_dict = {
    user_name: 'ruben',
    password: '123'
}
r = requests.get('https://127.0.0.1:8080/auth/login', data_dict)
print(r)