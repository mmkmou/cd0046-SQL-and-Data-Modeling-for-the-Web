import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
'''
 Set variable PG_URL before launch application
 Windows : 
 SET PG_URL= "postgresql://<username>:<password>@localhost:5432/<dbname>"
 
 Mac / Linux :
 export PG_URL="postgresql://postgres:Pa553R@localhost:5432/fyyur"

'''
SQLALCHEMY_DATABASE_URI = os.environ.get('PG_URL')
