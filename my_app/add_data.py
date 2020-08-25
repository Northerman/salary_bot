from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()


engine = create_engine('sqlite:///site.db')
Base.metadata.create_all(engine)
file_name = 'jobs_for_model.csv'
df = pd.read_csv(file_name)
df.to_sql(con=engine, index = False, name='profile', if_exists='append')
