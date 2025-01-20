from extensions import *
from dbclasses import *

#A model view for comments

class GISView(ModelView):
    can_create=True
    can_view_details=True

    column_list =('ID','Name','ImagePath','Latitude','Longitude','Source')
    column_editable_list = ('Name','ImagePath','Latitude','Longitude','Source')
    form_columns=('Name','ImagePath','Latitude','Longitude','Source','Date')    
    column_labels = {'ImagePath':'Path'}

class CommentModelView(ModelView):
    can_delete=False
    column_list = ('id', 'content', 'created_at', 'author')  # 'author.username' accesses the related User's username

    # Specify which columns you want to see in the form view (when adding/editing a comment)
    form_columns = ('content', 'created_at', 'user_id')  # 'author' will display a dropdown of users

    # Optionally, you can also define the column labels
    column_labels = {'content': 'Comment Text', 'created_at': 'Date Created', 'author.username': 'Author'}

    column_formatters = {
        'author': lambda v, c, m, p: m.author.username if m.author else 'No author'
    }

    def is_accessible(self):
        return current_user.is_admin
    
class UserModelView(ModelView):
    # Specify which columns to display in the list view
    column_list = ('id', 'username', 'email', 'is_admin')

    # Specify which columns to display in the form view
    form_columns = ('username', 'email', 'password', 'is_admin')

    def is_accessible(self):
        return current_user.is_admin