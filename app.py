from flask import render_template

from db_config import *
from dashboard.views import * 
from login.views import * 



#RUTAS
#Publicas

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/login')
def login():
    return render_template('login/login.html')










#----------------------------------------------------------------------------------------
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)    