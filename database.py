from pymongo import MongoClient
import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import os
import visualization
import sys


def mongodbConncect():
    datalink=os.environ.get("DATABASE_LINK")
    myclient =MongoClient(datalink)
    mydb = myclient["Heartpatientdatabase"] 
    mycol = mydb["Heart_Data"]
    
    # df=pd.DataFrame(list(mycol.find({})))
    # print(df.head())
    
    return mycol



def crudprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):   
    if sex=="male":
        sex=1
    else: sex=0
    if cp=="Typical angina":
        cp=0
    elif cp=="Atypical angina":
        cp=1
    elif cp=="Non-anginal pain":
        cp=2
    elif cp=="Asymptomatic":
        cp=2
    if exang=="Yes":
        exang=1
    elif exang=="No":
        exang=0
    if fbs=="Yes":
        fbs=1
    elif fbs=="No":
        fbs=0
    if slope=="Upsloping: better heart rate with excercise(uncommon)":
        slope=0
    elif slope=="Flatsloping: minimal change(typical healthy heart)":
          slope=1
    elif slope=="Downsloping: signs of unhealthy heart":
        slope=2  
    if thal=="fixed defect: used to be defect but ok now":
        thal=2
    elif thal=="reversable defect: no proper blood movement when excercising":
        thal=3
    elif thal=="normal":
        thal=1
    if restecg=="Nothing to note":
        restecg=0
    elif restecg=="ST-T Wave abnormality":
        restecg=1
    elif restecg=="Possible or definite left ventricular hypertrophy":
        restecg=2
    data_dict={"age":int(age),"sex":int(sex),"cp":int(cp),"trestbps":int(trestbps),"restecg":int(restecg),"chol":int(chol),"fbs":int(fbs),"thalach":int(thalach),"exang":int(exang),"oldpeak":float(oldpeak),"slope":int(slope),"ca":int(ca),"thal":int(thal),"target":int(result)}
    return data_dict




def crudOperation(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):
    data_dict=crudprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result)
    data1=json.dumps(data_dict,separators=(',', ':'), sort_keys=True)
    value = json.loads(data1)
    try:
        mycol=mongodbConncect()
        mycol.insert(value)
        print('Inserted 1 data to database')
    except:
        print('unable to insert', file=sys.stderr)



# if __name__ == '__main__':
#     crudOperation(39,"male","Non-anginal pain",130,"ST-T Wave abnormality",250,"Yes",187,"Yes",2,"Downsloping: signs of unhealthy heart",2,"normal",1)
#     # mongodbConncect()
#     # print("hi")