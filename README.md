# Fraud-api
Le projet consiste à implémenter une api capable de prédir si une transaction est frauduleuse via plusieurs modeles de Machine Learning

Audit, exploration, et nettoyage des données, Visualisation, Entraînement et évaluation de modèles de machine learning : Projet_FRAUD.ipynb

Déploiement du modèle du projet via une API HTTP REST FastAPI : fraud.py

L'objectif de cette API est de déployer les modèles créés. 

Les modèles ne sont pas ré-entrainés et nous faisons donc appel à un joblib pour chaque modèle.

L'API permet d'interroger les différents modèles. Les utilisateurs pourront interroger l'API pour accéder aux performances de l'algorithme sur le jeux de tests contenus dans le fichier "fraud.csv".

La liste exhaustive d'utilisateurs/mots de passe est la suivante: alice/wonderland, bob/builder, clementine/mandarine

Services :

GET /status

Renvoie 1 si l’API fonctionne.

GET /performance

Cette fonction renvoie les performance d'un modele MODEL : log (LogisticRegression) / dtc (Decision Tree Classification) / rfc (Random Forest Classification)

POST /prediction

Cette fonction renvoie les predictions pour un modèle donné.

POST /transaction/prediction

Cette fonction renvoie les predictions pour une ou plusieurs transactions. Renvoie 1 si la transaction est susceptible d'etre une fraude, 0 sinon.

Example value: [
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
