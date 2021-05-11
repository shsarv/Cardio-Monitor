from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import io
import random
import numpy as np

def visualizationpreprocess(age,sex,cp,trestbps,restecg,chol,fbs,thalach,exang,oldpeak,slope,ca,thal,result):
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
    
    #final_list=[int(cp),int(trestbps),int(restecg),int(chol),int(fbs),int(thalach),int(exang),float(oldpeak),int(slope),int(ca),int(thal)]
    normal_value1=[0.478261,0.159420,0.449275,0.550725,1.585507,1.166667,1.166667,2.543478]
    user_value1=[float(cp),float(fbs),float(restecg),float(exang),float(oldpeak),float(slope),float(ca),float(thal)]
    normal_value2=[134.398551,251.086957,139.101449]
    user_value2=[float(trestbps),float(chol),float(thalach)]
    list1=[normal_value1,user_value1]
    list2=[normal_value2,user_value2]

    return list1,list2

# def create_figure1(data1):
#     fig = plt.figure()
#     axis = fig.add_axes([0,0,1,1])
#     y1 = data1[0]
#     y2 = data1[1]
#     width = 0.30
#     x=np.arange(8)
#     axis.bar(x-0.3, y1, width, color='cyan')
#     axis.bar(x, y2, width, color='orange')
#     # axis.bar(xs, ys)
#     # axis.xticks(x, ['cp','chol','fbs','exang','oldpeak','slope','ca','thal'])
#     # axis.xlabel("Heart health defining attributes")
#     axis.set_ylabel("values")
#     # axis.legend(["Normal", "Yours"])
#     axis.set_title('Your data corresponding to normal data')
#     return fig




