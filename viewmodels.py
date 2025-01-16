from extensions import *
from dbclasses import *

#A model view for comments

class CommentModelView(ModelView):

    column_list = ('id', 'content', 'created_at', 'Comment.author.username')  # 'author.username' accesses the related User's username

    # Specify which columns you want to see in the form view (when adding/editing a comment)
    form_columns = ('content', 'created_at', 'author')  # 'author' will display a dropdown of users

    # Optionally, you can also define the column labels
    column_labels = {'content': 'Comment Text', 'created_at': 'Date Created', 'Comment.author.username': 'Author'}

    def is_accessible(self):
        return current_user.is_admin
    
class UserModelView(ModelView):
    # Specify which columns to display in the list view
    column_list = ('id', 'username', 'email', 'is_admin')

    # Specify which columns to display in the form view
    form_columns = ('username', 'email', 'password', 'is_admin')

    def is_accessible(self):
        return current_user.is_admin