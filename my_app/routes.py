from my_app import app, db
from my_app.models import Profile
from flask import Flask, render_template, request, redirect, url_for, make_response
from my_app.chatbot import chatbot
import webbrowser
import pickle
import numpy as np
import json
import pandas as pd
from collections import OrderedDict


#Model trained on local data
model_local = pickle.load(open('prediction_model/model_local.pkl','rb'))
occupation_mapping_local = pickle.load(open('prediction_model/occupation_mapping_local.pkl','rb'))

# Model trained on firebase data
model_firebase = pickle.load(open('prediction_model/model_firebase.pkl','rb'))
occupation_mapping_firebase = pickle.load(open('prediction_model/occupation_mapping_firebase.pkl','rb'))


# create necessary functions
def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def add_to_database(userText):
    data_list = userText.split(',')
    check_float_list = list(map(isfloat,data_list))
    if sum(check_float_list[0:2]) != 0 or sum(check_float_list[2:]) != 2 :
        return "Error input data is not valid"
    else:
        profile = Profile(name = data_list[0], occupation = data_list[1],
                          experience = data_list[2], salary = data_list[3])
        db.session.add(profile)
        db.session.commit()
        return 'Thanks Data is Added to local!'

def predict_salary(userText):
    data_list = userText.split(',')
    check_float_list = list(map(isfloat,data_list))
    if sum(check_float_list[0:1]) == 0 and sum(check_float_list[1:]) == 1:
        if data_list[0] in occupation_mapping_local:
            features = [[occupation_mapping_local[data_list[0]],data_list[1]]]
            return str('Your predicted Salary is ' + str(model_local.predict(features)))
        else:
            features = [[occupation_mapping_local['other'],data_list[1]]]
            return str('Your predicted Salary is ' + str(model_local.predict(features)))
            # return 'Error Cant find occupation or wrong input type'


def predict_salary_firebase(userText):
    data_list = userText.split(',')
    check_float_list = list(map(isfloat,data_list))
    if sum(check_float_list[0:1]) == 0 and sum(check_float_list[1:]) == 1:
        if data_list[0] in occupation_mapping_firebase:
            features = [[occupation_mapping_firebase[data_list[0]],data_list[1]]]
            return str('Your predicted Salary is ' + str(model_firebase.predict(features)))
        else:
            features = [[occupation_mapping_firebase['other'],data_list[1]]]
            return str('Your predicted Salary is ' + str(model_firebase.predict(features)))

# --------------------------------------------------------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')


#Left side chat (doesn't check intent, only check keywords)
@app.route("/getresponse")
def get_bot_response():
    userText = request.args.get('msg')   #Get user message
    data_list = userText.split(',')

    if userText == 'Add Data':
        return 'Please input your Name,Occupation,\nexperience,     salary per month seperated by comma to add occupation data'

    elif userText == 'Show Data':
        return str(Profile.query.all())

    elif len(data_list) == 4:
        return add_to_database(userText)

    elif len(data_list) == 2:
        return predict_salary(userText)

    ## Return python chatbot response if keyword doesn't match
    else:
        # chatbot = ChatBot('Northerman',trainer = 'chatterbot.corpus.english') #added line
        return str(chatbot.get_response(userText))

########################## DialogFlow Section ################################

#Note: Dont forget to connect to Ngrok to get dialogflow response
#Note2: Dont forget to add /webhook to dialogflow URL when connecting to webhook


## Connect to firebase database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("C://Users//North//my_app_folder//myappbot-sbhejl-f9cc87463f05.json")
firebase_admin.initialize_app(cred)
db_firebase = firestore.client()


## Webhook = the way dialogflow connects (send and receive data) with an app can be LINE,Skype,... or our webapplication! by using webhook URL.
@app.route('/webhook', methods = ['POST'])
def webhook():
    req = request.get_json(silent = True, force = True)  # the json that dialogflow sends us , req is a dict type
    res = processRequest(req)
    res = json.dumps(res, indent = 4)   #json to string
    r = make_response(res) #response object
    r.headers['Content-Type'] = 'application/json'

    return r  # send r back to dialogflow to make it output into the chat. (This is not a string)


def processRequest(req):
    intent = req["queryResult"]["intent"]["displayName"]  #finding intent from json dictionary

    # Show existing data in our firebase database
    if intent == 'show data':
        # doc_ref = db_firebase.collection(u'profiles').document(u'YVexRUVe88aZ7ieItyGZ')
        all_documents = []
        doc_ref = db_firebase.collection(u'profiles').stream()
        for doc in doc_ref:
            doc_json = json.dumps(doc.to_dict())
            all_documents.append(doc_json)
        speech = '\n'.join(all_documents)

    # Add data to our firebase database
    elif intent == 'AddData':
        userText = req['queryResult']['queryText']
        data_list = userText.split(',')
        if len(data_list) == 4:
            check = list(map(isfloat,data_list))
            if sum(check[0:2]) != 0 or sum(check[2:]) !=2:
                speech = 'Wrong input format please try again'
            else:
                user_data_dict = {
                    u'Name': data_list[0],
                    u'Occupation': data_list[1],
                    u'Experience': data_list[2],
                    u'Salary': data_list[3]
                    }
                doc_ref = db_firebase.collection(u'profiles').add(user_data_dict)
                speech = 'Thanks Data is Added to Firebase'
        else:
            speech = 'Wrong input format of adding data please try again.'

    # predict salary based on our firebase data model
    elif intent == 'predict':
        userText = req['queryResult']['queryText']
        speech = predict_salary_firebase(userText)
    # Other cases
    else:
        speech = "I don't understand please try again."

    res = makeWebhookResult(speech)

    return res

def makeWebhookResult(speech):
    return {"fulfillmentText":speech}




