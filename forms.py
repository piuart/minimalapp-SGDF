from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from wtforms.fields.simple import BooleanField


class UserForm(FlaskForm):
    username = StringField('User name', validators=[DataRequired()])
    password = StringField('Password',validators=[DataRequired()])
    is_admin = BooleanField('Is admin')
    enviar = SubmitField(' Crear ')    