import os
import requests
from requests.auth import HTTPBasicAuth

# definition de l'adresse de l'API
api_address = 'fastapi_container'
# port de l'API
api_port = 8000

# requÃªte
r = requests.post(
    url='http://{address}:{port}/transaction/prediction'.format(address=api_address, port=api_port), auth=HTTPBasicAuth('alice', 'wonderland'),
    params= {
        'modele': 'log'
    },
    json=[
         {
                "signup_time": "2015-07-08 15:35:44",
                "purchase_time": "2015-07-08 15:35:44",
                "purchase_value": "150",
                "source": "Ads",
                "browser": "Chrome",
                "sex": "M",
                "age": "23",
            }
    ]

)

output = '''
============================
    Transaction prediction test
============================

request done at "/transaction/prediction"
| modele="log"

expected result = [1]
actual result = {result}

==>  {test_status}

'''

# statut de la requête
status_code = r.status_code
# resultat de la requête
result = r.json()

# affichage des resultats
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(result=result, test_status=test_status))

log=os.environ.get('LOG')

# impression dans un fichier
if int(log) == 1:
    with open('api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))

