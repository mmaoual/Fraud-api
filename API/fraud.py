from datetime import datetime
from doctest import DocFileSuite
from fastapi import FastAPI, Depends, Header, HTTPException, status, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
import numpy as np
import json
from random import choices
from sklearn import metrics
from sklearn.model_selection import train_test_split
import joblib
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
import secrets
import uvicorn

# Importer les données du fichier Fraud.csv dans un DataFrame
df = pd.read_csv('fraud.csv')

# Création de la variable time_diff = différence entre l'heure de la connextion et l'heure d'achat
df['signup_time'] = pd.to_datetime(df['signup_time'])
df['purchase_time'] = pd.to_datetime(df['purchase_time'])
df['time_diff']=(df['purchase_time']-df['signup_time']).astype('timedelta64[m]')

dfTransact = pd.get_dummies(df, columns=['source','sex', 'browser'])

dfTransactTemp = dfTransact.drop(['signup_time', 'purchase_time', 'device_id','user_id', 'ip_address'], axis = 1)    

# define min max scaler
scaler = MinMaxScaler()

# transform data
dfTransactScaler = pd.DataFrame(scaler.fit_transform(dfTransactTemp.values), index=dfTransactTemp.index, columns=dfTransactTemp.columns)

# Instanciation du dataframe contenant les variables explicatives
X = dfTransactScaler.drop(['is_fraud'], axis = 1)

# Instanciation de la series contenant la variable cible 
y = dfTransactScaler['is_fraud']

# On applique la fonction train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.30, random_state=42)

oversample = SMOTE()
X_train, y_train = oversample.fit_resample(X_train, y_train)

login_mdp= {
    'alice': 'wonderland',
    'bob': 'builder',
    'clementine': 'mandarine'
}


class Performance(BaseModel):
    accuracy: str
    precision: str
    recall: str
    f1_score: str
    


class Transaction(BaseModel):
    signup_time: datetime
    purchase_time: datetime
    purchase_value: int
    source: str
    browser: str
    sex: str
    age: int
    class Config:
        schema_extra = {
            "example": {
                "signup_time": "2015-07-08 15:35:44",
                "purchase_time": "2015-07-08 15:35:44",
                "purchase_value": "150",
                "source": "Ads",
                "browser": "Chrome",
                "sex": "M",
                "age": "23",
            }
        }



api = FastAPI(
    title="Fraud prediction API",
    description="API pour predire si une transaction est frauduleuse",
    version="1.0.0",
    openapi_tags=[
    {
        'name': 'Status',
        'description': 'Renvoie 1 si l\'API fonctionne'
    },
    {
        'name': 'Performance',
        'description': 'Service permettant de déterminer les performances'
    },
    {
        'name': 'Prediction',
        'description': 'Service de predictions'
    }
    ]
)

security = HTTPBasic()
def getLoginAuthentifie(credentials: HTTPBasicCredentials = Depends(security)):   
    """
    compare HTTPBasicCredentials (username/password) avec la liste des clés/valeurs de login_mdp
    """
    try:
        mdp = secrets.compare_digest(credentials.password, login_mdp[credentials.username])
    except:
        mdp = False
    if not (mdp):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return credentials.username

@api.get("/login")
async def login(login: str = Depends(getLoginAuthentifie)):
    """
    Retourne le login authentifié
    """
    return {"login": login}

    
@api.get('/status', name='Status', tags=['Status'])
def get_status(username: str = Depends(getLoginAuthentifie)):
    """Renvoie 1 si l'API fonctionne.
    """
    return 1

@api.get('/performance', name='Performance du modele ', tags=['Performance'])
async def getPerformance(modele: str, username: str = Depends(getLoginAuthentifie)):
    """Renvoie la performance d'un modele\n
        MODELE : log (LogisticRegression) / dtc (Decision Tree Classification) / rfc (Random Forest Classification)
    """

    global X_test
    global y_test

    try:
        if (modele=="log"):
            mod=load('LogisticRegression_model.joblib')
        elif (modele=="dtc"):
            mod=load('DecisionTreeClassifier_model.joblib')
        elif (modele=="rfc"):
            mod=load('RandomForestClassifier_model.joblib')

        preds = mod.predict(X_test)
        performance = {
            'accuracy': str(metrics.accuracy_score(y_test, preds)),
            'precision': str(metrics.precision_score(y_test, preds)),
            'recall': str(metrics.recall_score(y_test, preds)),
            'f1_score': str(metrics.f1_score(y_test, preds))            
        }

        return performance 
        
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Indice Inconnu')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Type Inconnu'
        )

@api.get('/prediction', name='Predire en fonction du modele', tags=['Prediction'])
async def predire(modele: str, username: str = Depends(getLoginAuthentifie)):
    """Cette fonction renvoie les predictions de fraudes par rapport au modele choisi.\n
       MODEL : log (LogisticRegression) / dtc (Decision Tree Classification) / rfc (Random Forest Classification)
    """
    try:
        if (modele=="log"):
            mod=load('LogisticRegression_model.joblib')
        elif (modele=="dtc"):
            mod=load('DecisionTreeClassifier_model.joblib')
        elif (modele=="rfc"):
            mod=load('RandomForestClassifier_model.joblib')
            
        pred = mod.predict(X_test)
        pred_lists = pred.tolist()
        pred_jason = json.dumps(pred_lists)
        return pred_jason
            
    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )


@api.post('/transaction/prediction', name='Predire pour une/des transaction(s)', tags=['Prediction'])
async def predire(modele: str, transactions: List[Transaction], username: str = Depends(getLoginAuthentifie)):
    """Cette fonction renvoie les predictions pour une ou plusieurs transactions.\n
       MODEL : log (LogisticRegression) / dtc (Decision Tree Classification) / rfc (Random Forest Classification)
    """
    
    try:
        if (modele=="log"):
            mod=load('LogisticRegression_model.joblib')
        elif (modele=="dtc"):
            mod=load('DecisionTreeClassifier_model.joblib')
        elif (modele=="rfc"):
            mod=load('RandomForestClassifier_model.joblib')

        transactionsPred = []
        for index, transaction in enumerate(transactions):
            if transaction.source == "Ads":
                source_Ads = 1
            else:
                source_Ads = 0            
            if transaction.source == "Direct":
                source_Direct = 1
            else:
                source_Direct = 0
            if transaction.source == "SEO":
                source_SEO = 1
            else:
                source_SEO = 0
            
            if transaction.browser == "Chrome":
                browser_Chrome = 1
            else:
                browser_Chrome = 0            
            if transaction.browser == "FireFox":
                browser_FireFox = 1
            else:
                browser_FireFox = 0
            if transaction.browser == "IE":
                browser_IE = 1
            else:
                browser_IE = 0
            if transaction.browser == "Opera":
                browser_Opera = 1
            else:
                browser_Opera = 0
            if transaction.browser == "Safari":
                browser_Safari = 1
            else:
                browser_Safari = 0 
            
            if transaction.sex == "M":
                sex_M = 1
            else:
                sex_M = 0
            if transaction.browser == "F":
                sex_F = 1
            else:
                sex_F = 0            
            
            
            transact = {
                'signup_time': transaction.signup_time,
                'purchase_time': transaction.purchase_time,
                'purchase_value': transaction.purchase_value,
                'source_Ads': source_Ads,
                'source_Direct': source_Direct,
                'source_SEO': source_SEO,
                'browser_Chrome': browser_Chrome,
                'browser_FireFox': browser_FireFox,
                'browser_IE': browser_IE,
                'browser_Opera': browser_Opera,
                'browser_Safari': browser_Safari,
                'sex_M': sex_M,
                'sex_F': sex_F,
                'age': transaction.age
            }
            transactionsPred.append(transact)

        dframe = pd.DataFrame(transactionsPred)
        # Création de la variable time_diff = différence entre l'heure de la connextion et l'heure d'achat
        dframe['signup_time'] = pd.to_datetime(dframe['signup_time'])
        dframe['purchase_time'] = pd.to_datetime(dframe['purchase_time'])
        dframe['time_diff']=(dframe['purchase_time']-dframe['signup_time']).astype('timedelta64[m]')

        dfTransactTemp = dframe.drop(['signup_time', 'purchase_time'], axis = 1)
        # define min max scaler
        scaler = MinMaxScaler()

        # transform data
        dataframeScaler = pd.DataFrame(scaler.fit_transform(dfTransactTemp.values), index=dfTransactTemp.index, columns=dfTransactTemp.columns)

        prediction = mod.predict(dataframeScaler)
        predictionsList = prediction.tolist()
        resultatJson = json.dumps(predictionsList)
        return resultatJson

    except IndexError:
        raise HTTPException(
            status_code=404,
            detail='Unknown Index')
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail='Bad Type'
        )


if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8000)