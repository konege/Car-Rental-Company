# KonRent Car Rental Web Application

KonRent is a car rental web application, providing an easy and efficient way for users to rent cars from various offices. The application offers functionalities like searching for cars, filtering options, and user authentication including Google Sign-In.
It built with Flask, providing a seamless interface for users to rent vehicles across various locations in Izmir.

## Features
- **Search Functionality**: Users can search for available cars by office location, date, and time.
- **Filter Options**: Ability to filter cars by make, price, and transmission.
- **User Authentication**: Supports login with email/password and Google Sign-In.
- **Google OAuth 2.0 Integration**: For secure and convenient Google-based user authentication.
- **Secure Password Storage**: Utilizes Werkzeug security for hashing and securing user passwords.
- **Responsive Design**: Fully responsive web interface suitable for a variety of devices.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLAlchemy
- **APIs**: Google Maps, Google OAuth 2.0

## MVC (Model-View-Controller) Architecture in Flask

### Models
In your project, you have a `models` directory containing the following Python files:
- `office.py`: This file likely defines data structures and may include business logic related to office data, serving as the Model component.
- `user.py`: This file probably defines data structures and business logic related to user data, also serving as part of the Model component.
- `vehicle.py`: This file possibly defines data structures and business logic related to vehicle data, completing the Model component.

### Views
Your `templates` directory contains HTML files used for rendering web pages:
- `home.html`: This template is used to render the home page, fitting the View component.
- `login.html`: This template is used for rendering the login page, also aligning with the View component.
- `register.html`: This template is used for rendering the registration page, another part of the View component.
- `search.html`: This template is used to render the search page, completing the View component.

### Controllers
Controller logic in Flask is typically handled by view functions defined in the main application file, which, in your case, is `app.py`. This file likely contains routes that process user requests and return responses, serving as the Controller component.

This project structure adheres to the MVC architectural pattern, separating concerns and promoting modularity in your web application.

## Deployment
- I successfully deployed the web app on Azure Web Services, focusing on setting up the required configurations and environment variables to ensure smooth operation and compatibility with the Azure hosting environment.
- Code deployed at: [http://carrentkonege.azurewebsites.net](http://carrentkonege.azurewebsites.net)  (The site takes some time to open. I do not know why.)

## Video
- Also you can watch a short video from [here]([http://carrentkonege.azurewebsites.net](https://drive.google.com/file/d/1lnWEtBx1I7yVgctVvN8OZTGjAOpKUcxn/view)) about the project. 

