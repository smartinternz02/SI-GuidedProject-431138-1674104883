# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 15:53:00 2023

@author: FARHANA
"""

from flask import Flask, render_template, request
import requests
import pickle




API_KEY = "0T81aAhdDix560lMJHNQBh8rihW1OR_0_XDT564hcEGH"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)



@app.route('/')
def home():
    return render_template("index.html")


@app.route('/prediction',methods =['POST'])
def predict():
    mpg= request.form['mpg']
    cylinders = request.form['cylinders']
    displacement = request.form['displacement']
    horsepower= request.form[' horsepower']
    weight = request.form['weight']
    if(weight == " "):
        origin1,origin2,origin3,origin4,orgin5 = 0,0,0,0,1
    if(origin == "dtw"):
        origin1,origin2,origin3,origin4,orgin5 = 1,0,0,0,0
    if(origin == "jfk"):
         origin1,origin2,origin3,origin4,orgin5 = 0,0,1,0,0
    if(origin == "sea"):
         origin1,origin2,origin3,origin4,orgin5 = 0,1,0,0,0  
    if(origin == "alt"):
         origin1,origin2,origin3,origin4,orgin5 = 0,0,0,1,0
         
    acceleration= request.form['acceleration']
    if(acceleration== "msp"):
        acceleration1,acceleration2,acceleration3 = 0,0,0,0,1
    if(destination == "dtw"):
        acceleration1,acceleration2,acceleration3,acceleration4,acceleration5 = 1,0,0,0,0
    if(acceleration == "jfk"):
         acceleration1,acceleration2,acceleration3,acceleration4,acceleration5 = 0,0,1,0,0
    if(acceleration == "sea"):
         acceleration1,acceleration2,acceleration3,acceleration4,acceleration5 = 0,1,0,0,0  
    if(acceleration == "alt"):
         destination1,destination2,destination3,destination4,destination5 = 0,0,0,1,0
    dept = request.form['dept']    
    model year = request.form['model year']
    origin  = request.form['origin  ']
    dept15=int(dept)-int(origin )
    total = [[msp,cylinders,displacement,horsepower,weight1,weight2,weight3,acceleration1,acceleration2,acceleration3,acceleration4,int (model year),int (orgin)]]
    #print(total)

    payload_scoring = {"input_data": [{"field": [['msp', 'cylinders', 'displacement', 'horsepower', 'weight1','weight2','weight3',4','acceleration1','acceleration2','acceleration3','acceleration4','model year','orgin']],
                                       "values": total}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/2d1a6b1f-2a62-4fad-aa28-7e9ef9b3d8a9/predictions?version=2022-10-30', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})

    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)

    pred = response_scoring.json()

    output = pred['predictions'][0]['values'][0][0]

    if(output==[0.]):
        ans="The Flight will be on time"
    else:
        ans="The Flight will be delayed"
    return render_template("index.html",showcase = ans)
    

    

if __name__ == "__main__":
    app.run(debug=False)
