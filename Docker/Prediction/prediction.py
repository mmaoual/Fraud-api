import os
import requests
from requests.auth import HTTPBasicAuth

# définition de l'adresse de l'API
api_address = 'fastapi-container'
# port de l'API
api_port = 8000

# requête
r = requests.get(
    url='http://{address}:{port}/prediction'.format(address=api_address, port=api_port), auth=HTTPBasicAuth('alice', 'wonderland'),
    params= {
        'modele': 'log'
    }
)

output = '''
============================
    Prediction test
============================

request done at "/prediction"
| modele="log"

expected result = [0.0, 1.0, 0.0, 0.0......,0.0, 1.0, 0.0, 1.0, 0.0]
actual result = {result}

==>  {test_status}

'''

# statut de la requête
status_code = r.status_code
# resultat de la requête
result = r.json()

# affichage des résultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(result=result, test_status=test_status))

log=os.environ.get('LOG')

# impression dans un fichier
if int(log) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output.format(result=result, test_status=test_status))
