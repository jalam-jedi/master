from extensions import *

#--------------------------------------------------------------------------------------------------------------------------------------
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

 #--------------------------------------------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------------------------------------------
#Login Form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)], render_kw={"placeholder":"Username"})

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Password"})

    submit = SubmitField("Log In")

#--------------------------------------------------------------------------------------------------------------------------------------
#Comment Form
class CommentForm(FlaskForm):
    content = StringField('Your Comment', validators=[DataRequired()])
    submit = SubmitField('Post Comment')

#--------------------------------------------------------------------------------------------------------------------------------------
#Reply Form

class ReplyForm(FlaskForm):
    content = StringField('Your Reply', validators=[DataRequired()])
    submit = SubmitField('Post Reply')

#--------------------------------------------------------------------------------------------------------------------------------------

#User Info Database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin =db.Column(db.Boolean,nullable=False,default=False)

    comments = db.relationship('Comment', backref='author', lazy=True)

#--------------------------------------------------------------------------------------------------------------------------------------

#Commnets Database
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)  # Content of the comment
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Timestamp for comment creation

    is_reply = db.Column(db.Boolean, default=False, nullable=False)  # Indicates if the comment is a reply
    reply_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # Parent comment ID for replies

    # Foreign Key linking to the User table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('gis_model.ID'), nullable=False)  # Associated image
    user = db.relationship('User', backref='user_comments', lazy=True)  # This allows access to comment.user.username
    replies = db.relationship(
        'Comment',
        backref=db.backref('parent_comment', remote_side=[id]),
        lazy='dynamic'
    )

    # Validation before saving to the database
    def validate(self):
        if not self.is_reply:
            self.reply_id = None  # Ensure reply_id is NULL if it's not a reply

    # Overriding the save process to include validation
    def save(self):
        self.validate()
        db.session.add(self)
        db.session.commit()

#--------------------------------------------------------------------------------------------------------------------------------------

class GIS_Model(db.Model):
    __tablename__ = 'gis_model'
    
    ID = db.Column(db.Integer, primary_key=True)
    ImagePath = db.Column(db.String(2000), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Latitude = db.Column(db.Float(20), nullable=False)
    Longitude = db.Column(db.Float, nullable=False)
    Comments = db.Column(db.String(1000), nullable=True)
    Source = db.Column(db.String(50), nullable=True)
    Date = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-One Relationships
    comp_model = db.relationship('COMP_Model', uselist=False, back_populates='gis_model', cascade='all, delete-orphan')
    analysis_model = db.relationship('ANALYSIS_Model', uselist=False, back_populates='gis_model', cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='image', lazy=True)

#--------------------------------------------------------------------------------------------------------------------------------------
  
#Image Detail Databse
class COMP_Model(db.Model):
    __tablename__ = 'comp_model'

    ImageID = db.Column(db.Integer, db.ForeignKey('gis_model.ID'), primary_key=True)
    Hist_Relevance = db.Column(db.String(500), nullable=False)
    Mod_Imp = db.Column(db.String(500), nullable=False)
    Comp_Analysis = db.Column(db.String(500), nullable=False)
    Insight = db.Column(db.String(500), nullable=False)

    # One-to-One Relationship
    gis_model = db.relationship('GIS_Model', back_populates='comp_model')

#--------------------------------------------------------------------------------------------------------------------------------------

#Analysis Model
class ANALYSIS_Model(db.Model):
    __tablename__ = 'analysis_model'

    ImageID = db.Column(db.Integer, db.ForeignKey('gis_model.ID'), primary_key=True)
    Location_Type = db.Column(db.String(500), nullable=False)
    Unique_Feature = db.Column(db.String(500), nullable=False)
    Geographical_Feature = db.Column(db.String(500), nullable=False)
    Climate = db.Column(db.String(500), nullable=False)

    # One-to-One Relationship
    gis_model = db.relationship('GIS_Model', back_populates='analysis_model')
