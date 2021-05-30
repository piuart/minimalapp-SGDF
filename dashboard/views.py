import os
from flask import render_template,request
from pathlib import Path
from werkzeug.utils import secure_filename, redirect
from flask.helpers import send_file, url_for
import hashlib


from app import app
from models import FileContens
from db_config import *

from flask_login import LoginManager, login_required, logout_user, login_user

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['SECRET_KEY'] = 'secreto'


app.config['UPLOAD_FOLDER'] = "./upload"
#----------------------------------------------------------------------------------------
#RUTAS
#Dashboard
#Carga de archivo en base de datos
@app.route('/uploader', methods=['POST'])
@login_required
def upload():
    variable_path = ''
    file = request.files['inputFile']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    newFile = FileContens(name=file.filename, sha=file.read())
    db.session.add(newFile)
    for i in FileContens.query.order_by('id'):
        variable_path = i.name
        prueba = os.path.join(app.config['UPLOAD_FOLDER'],variable_path.replace(" ","_"))
        with open(prueba,"rb") as f:
            bytes = f.read() # read entire file as bytes
            readable_hash = hashlib.sha256(bytes).hexdigest()
            print(readable_hash)
            FileContens.query.filter_by(id=i.id).update(dict(sha=readable_hash))
        size_file= Path(prueba).stat().st_size
        FileContens.query.filter_by(id=i.id).update(dict(bites=float(size_file)))
        db.session.commit()
    return redirect(url_for('listado'))

#Listado
@app.route('/dashboard')
@app.route('/dashboard.html')
@login_required
def listado():
    files = FileContens.query.order_by('id')
    total_files = FileContens.query.count()
    app.logger.debug(f'Listado de acrhivos: {files}')
    app.logger.debug(f'Total archivos: {total_files}')
    return render_template('dashboard/dashboard.html', files=files, total_files=total_files) 
   
@app.route('/uploader')
@login_required
def uploader():
    return render_template('/dashboard/uploader.html')



#Ver archivo
@app.route('/ver/<int:id>')
@login_required
def ver_detalle(id):
    file_data = FileContens.query.get_or_404(id)
    return render_template('/dashboard/detalle.html', file_data = file_data)


#Eliminar  
@app.route('/eliminar/<int:id>', methods=['GET'])
@login_required
def eliminar(id):
    file = FileContens.query.get_or_404(id)
    app.logger.debug(f'Fichero a Eliminar: {file}')
    db.session.delete(file)
    db.session.commit()
    return redirect(url_for('listado'))



@app.route('/upload/<path:filename>', methods=['GET', 'POST'])
@login_required
def download(filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'],filename.replace(" ","_"))
    #return send_from_directory(directory=uploads, filename=filename)  
    return send_file(uploads, as_attachment=True)  


#---------------------------------------------------------------------------------------------