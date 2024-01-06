
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import re
import requests
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.config['GOOGLE_CLIENT_ID'] = '1005445236445-65d6gh91l93gkrrl0qnhnj543haghrn3.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = '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'

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

# Importing the models
from models.user import User
from models.vehicle import Vehicle
from models.office import Office

# Define initial data for offices in Izmir
initial_offices = [
    {'Name': 'Izmir Central Office', 'Address': 'Konak, Izmir', 'City': 'Izmir', 'Country': 'Turkey', 'Latitude': 38.4189, 'Longitude': 27.1287, 'WorkingDays': 'Mon-Fri', 'WorkingHours': '09:00-17:00'},
    {'Name': 'Izmir Karsiyaka Office', 'Address': 'Karsiyaka, Izmir', 'City': 'Izmir', 'Country': 'Turkey', 'Latitude': 38.455441, 'Longitude': 27.120075, 'WorkingDays': 'Mon-Sun', 'WorkingHours': '08:00-20:00'},
    {'Name': 'Izmir Bornova Office', 'Address': 'Bornova, Izmir', 'City': 'Izmir', 'Country': 'Turkey', 'Latitude': 38.4697, 'Longitude': 27.2201, 'WorkingDays': 'Mon-Fri', 'WorkingHours': '10:00-18:00'}
]

# Define initial data for vehicles
initial_vehicles = [
    # Vehicles for the first office
    [
        {'Make': 'Toyota', 'Model': 'Camry', 'Transmission': 'Automatic', 'Mileage': 20000, 'Age': 2, 'Deposit': 150.00, 'Image': 'toyota-camry.PNG'},
        {'Make': 'Honda', 'Model': 'Civic', 'Transmission': 'Manual', 'Mileage': 15000, 'Age': 1, 'Deposit': 120.00, 'Image': 'honda-civic.PNG'},
        {'Make': 'Ford', 'Model': 'Focus', 'Transmission': 'Automatic', 'Mileage': 25000, 'Age': 3, 'Deposit': 100.00, 'Image': 'ford-focus.PNG'}
    ],
    # Vehicles for the second office
    [
        {'Make': 'BMW', 'Model': '320i', 'Transmission': 'Automatic', 'Mileage': 30000, 'Age': 4, 'Deposit': 200.00, 'Image': 'bmw-320i.PNG'},
        {'Make': 'Audi', 'Model': 'A4', 'Transmission': 'Manual', 'Mileage': 22000, 'Age': 2, 'Deposit': 180.00, 'Image': 'audi-a4.PNG'},
        {'Make': 'Mercedes', 'Model': 'C-Class', 'Transmission': 'Automatic', 'Mileage': 35000, 'Age': 5, 'Deposit': 250.00, 'Image': 'mercedes-c-class.PNG'}
    ],
    # Vehicles for the third office
    [
        {'Make': 'Tesla', 'Model': 'Model 3', 'Transmission': 'Automatic', 'Mileage': 10000, 'Age': 1, 'Deposit': 300.00, 'Image': 'tesla-model-3.PNG'},
        {'Make': 'Nissan', 'Model': 'Leaf', 'Transmission': 'Automatic', 'Mileage': 12000, 'Age': 1, 'Deposit': 150.00, 'Image': 'nissan-leaf.PNG'},
        {'Make': 'Chevrolet', 'Model': 'Bolt', 'Transmission': 'Automatic', 'Mileage': 9000, 'Age': 1, 'Deposit': 160.00, 'Image': 'chevrolet-bolt.PNG'}
    ]
]

with app.app_context():
    db.create_all()

    # Populate offices in Izmir if they don't exist
    if Office.query.count() == 0:
        for office_data in initial_offices:
            office = Office(**office_data)
            db.session.add(office)
        db.session.commit()

    # Populate vehicles if they don't exist
    if Vehicle.query.count() == 0:
        for office_index, vehicles_data in enumerate(initial_vehicles, start=1):
            for vehicle_data in vehicles_data:
                vehicle = Vehicle(OfficeID=office_index, **vehicle_data)
                db.session.add(vehicle)
        db.session.commit()

@app.route('/')
def home():
    # Assuming Office has attributes like name, address, etc.
    offices = Office.query.all()  # Fetch all office locations from the database
    return render_template('home.html', offices=offices)

@app.route('/search', methods=['GET'])
def search():
    selected_office_index = int(request.args.get('pickup_office'))
    # Retrieve the office name using the selected index
    selected_office_name = initial_offices[selected_office_index]['Name']

    # Get the list of vehicles for the selected office
    vehicles_for_office = initial_vehicles[selected_office_index]

    # Retrieve other request parameters
    pickup_date = request.args.get('pickup_date')
    pickup_time = request.args.get('pickup_time')
    return_date = request.args.get('return_date')
    return_time = request.args.get('return_time')

    # Pass the office name instead of the index to the template
    return render_template('search.html', vehicles=vehicles_for_office,
                           pickup_date=pickup_date, pickup_time=pickup_time,
                           return_date=return_date, return_time=return_time,
                           pickup_office=selected_office_name)  # Use the office name here


@app.route('/filter_vehicles', methods=['GET'])
def filter_vehicles():
    # Retrieve the pickup and return information
    pickup_date = request.args.get('pickup_date')
    pickup_time = request.args.get('pickup_time')
    return_date = request.args.get('return_date')
    return_time = request.args.get('return_time')
    pickup_office = request.args.get("pickup_office")
    selected_office_index = request.args.get('pickup_office')  # Assuming this is the index of the office in your initial_offices list

    # Retrieve filter criteria
    make = request.args.get('make')
    price_sort = request.args.get('price')  # 'ascending' or 'descending'
    transmission = request.args.get('transmission')

    # Get the list of vehicles for the selected office
    # This assumes that initial_vehicles is a list of lists, with each sub-list corresponding to an office
    vehicles_for_office = initial_vehicles[int(selected_office_index)]

    # Apply filters to the vehicles for the selected office
    if make and make != 'Make':
        vehicles_for_office = [v for v in vehicles_for_office if v['Make'] == make]

    if transmission and transmission != 'Transmission':
        vehicles_for_office = [v for v in vehicles_for_office if v['Transmission'] == transmission]

    # Apply sorting based on price
    if price_sort == 'ascending':
        vehicles_for_office.sort(key=lambda x: x['Deposit'])
    elif price_sort == 'descending':
        vehicles_for_office.sort(key=lambda x: x['Deposit'], reverse=True)

    # Check if any vehicles match the criteria
    if not vehicles_for_office:
        flash("There is no vehicle that matches your criteria in our office.")

    # Render the template with the filtered and sorted list of vehicles, and the pickup/return info
    return render_template('search.html', vehicles=vehicles_for_office,
                           pickup_date=pickup_date, pickup_time=pickup_time,
                           return_date=return_date, return_time=return_time,
                           pickup_office=pickup_office,
                           selected_office_index=selected_office_index)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(Email=email).first()

        if user and check_password_hash(user.Pword, password):
            login_user(user)
            flash('Login Success!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong Email or Password. Please try again.', 'danger')

    return render_template('login.html')

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        country = request.form.get('country')
        city = request.form.get('city')


        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
        elif len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalnum() for char in password):
            flash('The password must be at least 8 characters long and contain at least one number and one special character.', 'danger')
        else:

            hashed_password = generate_password_hash(password, method='sha256')
            new_user = User(Email=email, Pword=hashed_password, Country=country, City=city)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration Successful! You can log in now.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login/google')
def google_login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()

    # Check if the user exists in your database
    user = User.query.filter_by(Email=user_info['email']).first()
    if not user:
        # Create a new user if not exist
        user = User(Email=user_info['email'], Country='Default Country', City='Default City')
        db.session.add(user)
        db.session.commit()

    # Log in the user
    login_user(user)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)