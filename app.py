from flask import Flask, render_template ,url_for ,request
import numpy as np
import joblib
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()

model = open( "Heart_model1.pkl" , "rb" )
clfr = joblib.load(model)

app = Flask ( __name__ )

def preprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal ):   
 
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
        thal=6
    elif thal=="reversable defect: no proper blood movement when excercising":
        thal=7
    elif thal=="normal":
        thal=2.31
    if restecg=="Nothing to note":
        restecg=0
    elif restecg=="ST-T Wave abnormality":
        restecg=1
    elif restecg=="Possible or definite left ventricular hypertrophy":
        restecg=2
    user_input=[age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    user_input=scal.fit_transform(user_input)
    prediction = clfr.predict(user_input)

    return prediction

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict',methods=['POST'])
def predict():
    if request.method  == 'POST':
        nameofpatient= request.form ['name']
        age= request.form ['age']
        sex=request.form ['sex']
        cp= request.form ['cp']
        trestbps= request.form ['trestbps']
        chol= request.form ['chol']
        fbs= request.form ['fbs']
        restecg=request.form ['restecg']
        thalach=request.form ['thalach']
        exang=request.form ['exang']
        oldpeak=request.form ['oldpeak']
        slope=request.form ['slope']
        ca=request.form ['ca']
        thal=request.form ['thal']
        result=preprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal )
        return render_template ('result.html',prediction = result, nameofpatient=nameofpatient)

@app.errorhandler(500)
def internal_error(error):

    return render_template('error.html')

@app.errorhandler(404)
def not_found(error):
    return "404 error",404

if __name__ == '__main__':
    app.run( debug = True)