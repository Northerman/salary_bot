from my_app import db


class Profile(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),nullable = False)
    occupation = db.Column(db.String(100),nullable = False)
    experience = db.Column(db.Integer,nullable = False)
    salary = db.Column(db.Integer,nullable = False)


    def __repr__(self):
        return f"Name('{self.name}','{self.occupation}','{self.experience}','{self.salary}')"





# engine = create_engine('sqlite:///site.db')
# Base.metadata.create_all(engine)
# file_name = 'my_app/jobs_for_model.csv'
# df = pd.read_csv(file_name)
# print(df.to_sql(con=engine, index_label='id', name=Profile.__tablename__, if_exists='append'))
# print(df)


