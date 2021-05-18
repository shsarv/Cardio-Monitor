from itertools import count
from flask import Flask, render_template ,url_for ,request,Response
import numpy as np
import database
import prediction
import json
import io
import random
import visualization
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import modelbuild


app = Flask ( __name__ )



# @app.route('/plot1.png')
# def plot_png1():
#     fig = visualization.create_figure2(data1)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')

# @app.route('/plot2.png')
# def plot_png2():
#     fig = visualization.create_figure2(data2)
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')


def create_figure1(data1):
    fig = plt.subplots(figsize =(12, 8))
    barWidth = 0.25
    normal = data1[0]
    user = data1[1]
    br1 = np.arange(len(normal))
    br2 = [x + barWidth for x in br1]
    # br3 = [x + barWidth for x in br2]
    plt.bar(br1, normal, color ='g', width = barWidth,edgecolor ='grey', label ='Normal Value')
    plt.bar(br2, user, color ='r', width = barWidth,edgecolor ='grey', label ="Yours Value")
    # plt.bar(br3, CSE, color ='b', width = barWidth, edgecolor ='grey', label ='CSE')
    plt.xlabel('Health status defining attributes', fontweight ='bold', fontsize = 15)
    plt.ylabel('respective values', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(normal))],['cp','chol','fbs','exang','oldpeak','slope','ca','thal'])
    plt.legend()
    plt.savefig('static/plotng.png') 

def create_figure2(data2):
    fig = plt.subplots(figsize =(12, 8))
    barWidth = 0.25
    normal = data2[0]
    user = data2[1]
    br1 = np.arange(len(normal))
    br2 = [x + barWidth for x in br1]
    plt.bar(br1, normal, color ='g', width = barWidth,edgecolor ='grey', label ='Normal Value')
    plt.bar(br2, user, color ='r', width = barWidth,edgecolor ='grey', label ="Yours Value")
    plt.xlabel('Health status defining attributes', fontweight ='bold', fontsize = 15)
    plt.ylabel('respective values', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(normal))],['trestbps','chol','thalach'])
    plt.legend()
    plt.savefig('static/plotng2.png') 

@app.route('/')
def home():
    global counter2
    counter2+=1
    return render_template('home.html',all_count=counter2)


global counter
counter=0
global counter2
counter2=0

@app.route('/predict',methods=['POST'])
def predict():
    global data1
    global data2
    global counter
    global counter2
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
        counter+=1
        if(counter<=50):
            result=prediction.preprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal )
        else:
            #modelbuild.bulidmodel()
            result=prediction.preprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal )
            counter=0
        #database.crudOperation(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result)
        data1,data2=visualization.visualizationpreprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result)
        create_figure1(data1)
        create_figure2(data2)
        return render_template ('result.html',prediction = result, nameofpatient=nameofpatient, model_counter=counter, total_counter=counter2)

@app.route('/about')
def about():
    return render_template('disease.html')


@app.errorhandler(500)
def internal_error(error):

    return render_template('error.html')


@app.errorhandler(404)
def not_found(error):
    return "404 error",404

if __name__ == '__main__':
    app.run( debug = True)