from flask import request, redirect, render_template, flash
from flask_login import LoginManager, login_required, logout_user, login_user
from flask.helpers import url_for

from app import app
from models import User
from db_config import *

from forms import UserForm

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
app.config['SECRET_KEY'] = 'secreto'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route('/logmein',methods=['POST'])    
def logmein():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username,password=password).first()
    if not user:
        flash('Aun no eres un usuario de la plataforma, puedes contactar con el administrador info@minimalapp.com')
        return redirect('login')    
    login_user(user, remember=True)
    print(user.is_authenticated)
    print(user.is_active)
    print(user.get_id)
    print(user.is_anonymous)
    return redirect('dashboard')   



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('/index.html')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('/dashboard/dashboard.html')



@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    return 'Estamos en el escritorio'    



@app.route('/create_user', methods=['GET','POST'])
@login_required
def create_user():
    username = User()
    userForm = UserForm(obj=username)
    if request.method == 'POST':
        if userForm.validate_on_submit():
            userForm.populate_obj(username)
            app.logger.debug(f'Persona a insertar: {username}')
            #insertamos el registro
            db.session.add(username)
            db.session.commit()
            return redirect(url_for('listado_user'))        
    return render_template('/dashboard/create_user.html', forma=userForm)    




@app.route('/listado_user')
@app.route('/listado_user.html')
@login_required 
def listado_user():
    #listado de personas
    #username = User.query.all()
    users = User.query.order_by('id')
    total_users = User.query.count()
    app.logger.debug(f'Listado de personas: {users}')
    app.logger.debug(f'Total Personas: {total_users}')
    return render_template('/login/listado_user.html', users=users, total_users=total_users)  



@app.route('/ver_user/<int:id>')
@login_required
def ver_user(id):
    user_data = User.query.get_or_404(id)
    return render_template('/login/ver_user.html', user_data = user_data)   



@app.route('/editar/<int:id>', methods=['GET','POST'])  
@login_required
def editar(id):
    #recuperamos el objeto persona a editar de la base de datos
    user = User.query.get_or_404(id)
    userForma= UserForm(obj=user)
    if request.method == 'POST':
        if userForma.validate_on_submit():
            userForma.populate_obj(user)
            app.logger.debug(f'Persona actualizada: {user}')
            #editar el registro
            db.session.commit()
            return redirect(url_for('listado_user'))
    return render_template('/login/editar.html', forma=userForma)   



@app.route('/eliminar_user/<int:id>', methods=['GET'])
@login_required
def eliminar_user(id):
    user = User.query.get_or_404(id)
    app.logger.debug(f'Persona a Eliminar: {user}')
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('listado_user'))        