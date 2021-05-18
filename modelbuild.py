# Basic
import os
import sys
import json
import pymongo 
import warnings
import numpy as np
import pandas as pd
from itertools import chain
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
from xgboost import plot_importance
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
#Model Selection
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,recall_score,f1_score,precision_score,roc_auc_score,confusion_matrix,classification_report
from sklearn.metrics import r2_score,mean_squared_error,accuracy_score,recall_score,precision_score,confusion_matrix,classification_report
import pickle
import joblib
warnings.filterwarnings('ignore')

def import_content(filepath):
    mng_client = pymongo.MongoClient("mongodb+srv://shsarv:swatisahu@heart.9ynzc.mongodb.net/Heartpatientdatabase?retryWrites=true&w=majority")
    mng_db = mng_client['Heartpatientdatabase'] 
    collection_name = 'Heart_Data_new'
    db_cm = mng_db[collection_name]
    cdir = os.path.abspath('./')
    file_res = os.path.join(cdir, filepath)
    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

#import_content('heart.csv')

def mongodbConnect():
    datalink=os.environ.get("DATABASE_LINK")
    myclient =pymongo.MongoClient(datalink)
    mydb = myclient["Heartpatientdatabase"] 
    mycol = mydb["Heart_Data"]
    df=pd.DataFrame(list(mycol.find({},{'_id': False})))
    df.drop_duplicates()
    scal=MinMaxScaler()
    feat=['age', 'sex', 'cp', 'trestbps', 'chol','fbs','restecg','thalach' ,'exang', 'oldpeak' ,'slope', 'ca', 'thal']
    df[feat] = scal.fit_transform(df[feat])
    return df

def bulidmodel():
    df=mongodbConnect()
    y = df["target"]
    X = df.drop('target',axis=1)
    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.20, random_state = 0)
    Knn_clf=  KNeighborsClassifier(n_neighbors=7)
    Knn_clf.fit(X_train,Y_train)
    y_pred=Knn_clf.predict(X_test)
    accuracy = accuracy_score(Y_test,y_pred)
    if accuracy>0.9:
        joblib.dump(Knn_clf, 'Heart_Model.pkl')

