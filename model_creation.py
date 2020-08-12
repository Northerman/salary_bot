# import local data
from my_app.models import Profile
import sqlalchemy as sql

# import necessary libraries
import numpy as numpy
import pandas as pd
import pickle
import json

##sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

##To load firebase db
from my_app.routes import db_firebase


#----------------------------------------- Start create model local


#Load data from local
print('Creating Model from Local data .......')
connect_string = 'sqlite:///C:\\Users\\North\\my_app_folder\\my_app\\site.db'
sql_engine = sql.create_engine(connect_string)
# print(sql_engine.table_names())
query = "SELECT * from Profile"
df = pd.read_sql_query(query, sql_engine)


# LabelEncoding categorical data
le = LabelEncoder()
df['occupation'] = le.fit_transform(df['occupation'])
print(df)
occupation_mapping = dict(zip(le.classes_,le.transform(le.classes_)))
label_other = len(occupation_mapping)
occupation_mapping['other'] = label_other


#Modelling
X = df[['occupation','experience']]
y = df[['salary']]
regressor = DecisionTreeRegressor()
regressor.fit(X,y)

#Save Local Data Model
pickle.dump(regressor,open('prediction_model/model_local.pkl','wb'))
pickle.dump(occupation_mapping,open('prediction_model/occupation_mapping_local.pkl','wb'))

#----------------------------------------- Start create model firebase
print('Creating Model from Firebase data .......')

#Load data from firebase
all_documents = []
doc_ref = db_firebase.collection(u'profiles').stream()
for doc in doc_ref:
    doc_dict = doc.to_dict()
    all_documents.append(doc_dict)
df = pd.DataFrame(all_documents)

# LabelEncoding categorical data
le = LabelEncoder()
df['Occupation'] = le.fit_transform(df['Occupation'])
occupation_mapping_firebase = dict(zip(le.classes_,le.transform(le.classes_)))
label_other = len(occupation_mapping_firebase)
occupation_mapping_firebase['other'] = label_other

#Modelling
X = df[['Occupation','Experience']]
y = df[['Salary']]
regressor = DecisionTreeRegressor()
regressor.fit(X,y)


#Save Firebase Data Model
pickle.dump(regressor,open('prediction_model/model_firebase.pkl','wb'))
pickle.dump(occupation_mapping,open('prediction_model/occupation_mapping_firebase.pkl','wb'))







