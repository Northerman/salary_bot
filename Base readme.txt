## Create database and load csv data into database
cd ไปที่ my_app_folder
run python
from my_app import db
db.create_all()
exit python
cdไปที่ my_app
run python add_data.py
cd.. back to my_app_folder
flask run
DONE!

## Train prediction model
cd to my_app_folder
python model_creation.py

## Train chatbot
cd to my_app_folder
python chatbot_train.py

