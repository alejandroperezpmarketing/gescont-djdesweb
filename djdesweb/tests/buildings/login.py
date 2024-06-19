'''
Created on Apr 11, 2024

@author: vagrant
'''

import requests


d=['hola', 'clase', 'esto', 'es', 'divertido']

for w in d:
    payload = {'user': 'joamona', 'password': w}
    r = requests.post('http://localhost:8000/appdesweb/login/', data=payload)
    print(r.status_code,r.text, r.json())

