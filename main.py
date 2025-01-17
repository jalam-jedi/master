from extensions import *
from dbclasses import *
from viewmodels import *

admin.add_view(UserModelView(User, db.session))
admin.add_view(CommentModelView(Comment, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
            if user.is_admin:
                return redirect(url_for('admin.index'))
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
    # Query the COMP_Model table for the image with the given ID
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
     