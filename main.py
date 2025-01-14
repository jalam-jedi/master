from flask import Flask, url_for, redirect,request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate



app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gis.db'
db =SQLAlchemy(app)
migrate = Migrate(app, db)

class GIS_Model(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    ImagePath= db.Column(db.String(2000),nullable =False)
    Name = db.Column(db.String(100),nullable =False)
    Latitude =db.Column(db.Float(20),nullable=False)
    Longitude = db.Column(db.Float,nullable=False)
    Comments = db.Column(db.String(1000),nullable=True)
    Source =db.Column(db.String(50),nullable=True)
    Date =db.Column(db.DateTime,default =datetime.utcnow)

class COMP_Model(db.Model):
    ImageID= db.Column(db.Integer,primary_key=True)
    ImagePath= db.Column(db.String(2000),nullable =False)
    Name = db.Column(db.String(100),nullable =False)
    Hist_Relevance =db.Column(db.String(500),nullable=False)
    Mod_Imp= db.Column(db.String(500),nullable=False)
    Comp_Analysis =db.Column(db.String(500),nullable=False)
    Insight= db.Column(db.String(500),nullable=False)

class ANALYSIS_Model(db.Model):
    ImageID = db.Column(db.Integer, primary_key=True)
    ImagePath = db.Column(db.String(2000), nullable=False)
    Name = db.Column(db.String(100), nullable=False)
    Location_Type = db.Column(db.String(500), nullable=False)
    Unique_Feature = db.Column(db.String(500), nullable=False)
    Geographical_Feature = db.Column(db.String(500), nullable=False)
    Climate = db.Column(db.String(500), nullable=False)


@app.route('/')

def main_page():
    gis_data= GIS_Model.query.all()
    
    return render_template('main.html',gis_data=gis_data)

@app.route('/image/<int:image_id>')
def image_detail(image_id):
    # Query the GIS_Model table for the image with the given ID
    image = COMP_Model.query.get_or_404(image_id)
    return render_template('image_detail.html', image=image)



@app.route("/comparison", methods=['POST', 'GET'])
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


    



if __name__ == '__main__':
    app.run(debug=True)
    