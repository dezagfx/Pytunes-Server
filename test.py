import requests
token = 'jXVQOHEaNUpxJ1bZaDOzCKSyTYGu3n97OcrTLTBa6ng=1441302159.970998'

r = requests.get('https://127.0.0.1:8080/playlists/1', data={'token':token}, verify=False)
print(r.content)