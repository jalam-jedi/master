from datetime import datetime
from extensions import *  # Adjust import based on your app's structure
from dbclasses import *  # Adjust import to your actual model

# Data to be added
# Creating a new user instance with hashed password
hashed_password = bcrypt.generate_password_hash("admin123").decode('utf-8')

new_user = User(
    username="jawad_admin", 
    email="jawadalam6002@gmail.com", 
    password=hashed_password,  # Use the hashed password
    is_admin=True
)

# Add the new user to the session and commit to the database
with app.app_context():  # Ensures the app context is set
    db.session.add(new_user)
    db.session.commit()

    print("New admin user added successfully!")