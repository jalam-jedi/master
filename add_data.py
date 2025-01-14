from main import app, db
from main import ANALYSIS_Model  # Ensure to import your model

# Data to insert into the ANALYSIS_Model table
data = [
    {
        'ImageID': 1,
        'ImagePath': 'GIS_Image_1.jpg',
        'Name': 'Yosemite Falls',
        'Location_Type': 'Natural waterfall in Yosemite National Park',
        'Unique_Feature': 'Seasonal waterfall, one of the tallest in North America',
        'Geographical_Feature': 'Sierra Nevada Mountains',
        'Climate': 'Mountainous with seasonal water flow'
    },
    {
        'ImageID': 2,
        'ImagePath': 'GIS_Image_1.jpg',
        'Name': 'Los Angeles',
        'Location_Type': 'Urban cultural and entertainment city',
        'Unique_Feature': 'The Hollywood Sign symbolizing the film industry',
        'Geographical_Feature': 'Coastal basin',
        'Climate': 'Mediterranean climate with warm, dry summers'
    },
    {
        'ImageID': 3,
        'ImagePath': 'GIS_Image_1.jpg',
        'Name': 'San Francisco',
        'Location_Type': 'Urban center with iconic landmarks and technology hub',
        'Unique_Feature': 'Golden Gate Bridge and hilly terrain',
        'Geographical_Feature': 'Coastal hills and San Francisco Bay',
        'Climate': 'Cool Mediterranean with frequent fog'
    },
    {
        'ImageID': 4,
        'ImagePath': 'GIS_Image_1.jpg',
        'Name': 'Napa Valley',
        'Location_Type': 'Wine-producing region',
        'Unique_Feature': 'Mediterranean climate and volcanic soil ideal for wine production',
        'Geographical_Feature': 'Valley with unique microclimates',
        'Climate': 'Mediterranean with diverse microclimates'
    },
    {
        'ImageID': 5,
        'ImagePath': 'GIS_Image_1.jpg',
        'Name': 'Death Valley',
        'Location_Type': 'Desert landscape and national park',
        'Unique_Feature': 'Badwater Basin, the lowest point in North America',
        'Geographical_Feature': 'Salt flats, sand dunes, and desert rock formations',
        'Climate': 'Extremely hot desert with minimal rainfall'
    }
]

# Add the data to the database
with app.app_context():
    for item in data:
        analysis_entry = ANALYSIS_Model(
            ImageID=item['ImageID'],
            ImagePath=item['ImagePath'],
            Name=item['Name'],
            Location_Type=item['Location_Type'],
            Unique_Feature=item['Unique_Feature'],
            Geographical_Feature=item['Geographical_Feature'],
            Climate=item['Climate']
        )
        db.session.add(analysis_entry)
    
    db.session.commit()
    print("Data added successfully to ANALYSIS_Model!")
