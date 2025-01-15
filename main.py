from flask import Flask, url_for, redirect,request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DecimalField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, InputRequired, IPAddress, IPAddress, ValidationError
from flask_bcrypt import Bcrypt

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gis.db' 
db =SQLAlchemy(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = '60029032.comQWERTY'
bcrypt = Bcrypt(app)

login_manager= LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#Register Form
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)] ,render_kw={"placeholder":"Username"})
    
    email = StringField('Username', validators=[DataRequired(), Length(min=4, max=40 )] ,render_kw={"placeholder":"Email"})
    
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)] , render_kw={"placeholder":"Password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = User.query.filter_by(username=username.data).first()

        if existing_username:
            raise ValidationError('Username already exists . Please choose a different username')
    
#Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Log In")


#User Info Database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

#Main Web Databse
class GIS_Model(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ImagePath= db.Column(db.String(2000),nullable =False)
    Name = db.Column(db.String(100),nullable =False)
    Latitude =db.Column(db.Float(20),nullable=False)
    Longitude = db.Column(db.Float,nullable=False)
    Comments = db.Column(db.String(1000),nullable=True)
    Source =db.Column(db.String(50),nullable=True)
    Date =db.Column(db.DateTime,default =datetime.utcnow)

#Image Detail Databse
class COMP_Model(db.Model):
    ImageID= db.Column(db.Integer,primary_key=True)
    ImagePath= db.Column(db.String(2000),nullable =False)
    Name = db.Column(db.String(100),nullable =False)
    Hist_Relevance =db.Column(db.String(500),nullable=False)
    Mod_Imp= db.Column(db.String(500),nullable=False)
    Comp_Analysis =db.Column(db.String(500),nullable=False)
    Insight= db.Column(db.String(500),nullable=False)

#Comaprison Databse
class ANALYSIS_Model(db.Model):
    ImageID = db.Column(db.Integer, primary_key=True)
    ImagePath = db.Column(db.String(2000), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Location_Type = db.Column(db.String(500), nullable=False)
    Unique_Feature = db.Column(db.String(500), nullable=False)
    Geographical_Feature = db.Column(db.String(500), nullable=False)
    Climate = db.Column(db.String(500), nullable=False)


#Main Page
@app.route('/',methods=['Post','Get'])
@login_required
def main_page():
    gis_data= GIS_Model.query.all()
    
    return render_template('main.html',gis_data=gis_data)

#Log In Page
@app.route('/login',methods =['Post','Get'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            bcrypt.check_password_hash(user.password,form.password.data)
            login_user(user)
            return redirect('/')
    return render_template('login.html',form=form)

#Register Page
@app.route('/register',methods =['Post','Get'])
def register_page():
    form =RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user =User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',form=form )

#Image Details Page
@app.route('/image/<int:image_id>')
@login_required
def image_detail(image_id):
    # Query the GIS_Model table for the image with the given ID
    image = COMP_Model.query.get_or_404(image_id)
    return render_template('image_detail.html', image=image)

#Comparison Page
@app.route("/comparison", methods=['POST', 'GET'])
@login_required
def comp_page():
    images_data = ANALYSIS_Model.query.all()

    if request.method == 'POST':
        image1_id = request.form.get('image1')
        image2_id = request.form.get('image2')

        # Check if both dropdowns have valid selections
        if not image1_id or not image2_id:
            return render_template('comparison.html', images_data=images_data, error="Please select two images for comparison.")
        
        try:
            image1_id = int(image1_id)
            image2_id = int(image2_id)
        except ValueError:
            return render_template('comparison.html', images_data=images_data, error="Invalid selection. Please try again.")

        # Fetch the selected images
        image1 = ANALYSIS_Model.query.get_or_404(image1_id)
        image2 = ANALYSIS_Model.query.get_or_404(image2_id)

        return render_template('comparison.html', images_data=images_data, image1=image1, image2=image2)

    return render_template('comparison.html', images_data=images_data)


#Logout Page
@app.route('/logout',methods=['Post','Get'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
     