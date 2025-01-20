from flask import Flask, url_for, redirect,request, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, InputRequired, IPAddress, IPAddress, ValidationError
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import json

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gis.db' 
db =SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = '60029032.comQWERTY'
bcrypt = Bcrypt(app)
login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
admin = Admin(app, name='My Admin Panel', template_mode='bootstrap3')

