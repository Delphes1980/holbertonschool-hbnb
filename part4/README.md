# HBNB Project - Part 4: Simple Web Client

## Table of Contents
- [Introduction](#introduction)
- [Objectives](#objectives)
- [Features](#features)
- [Structure](#structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies](#technologies-used)
- [Author](#author)


### Introduction
This fourth phase of the HBnB project aims to focus on the front-end development of the application using HTML5, CSS3, and JavaScript ES6.
The goal is to design an interactive user interface connecting with the back-end services.

### Objectives
The main objectives of this part of the project include:
- Developing a user-friendly interface
- Implementation of client-side functionality interacting with the back-end
- Ensuring secure and efficient data handling using JavaScript
- Creating a dynamic web application

### Features
In addition to the functionalities from Part3, this phase introduces:
- Creation of Login, List of Places, Place Details and Add Review pages with a design using HTML and CSS files
- Utilization of cookies to store the token from login function for session management
- Fetching places data from API and display them based on a price selection. If the user is not authenticated, they are redirected to the login page
- Fetching places data from API with a specific ID and display the details of the place. If the user is authenticated, they can access to the review form
- Authenticated users can add a review to a specific place, if they are not authenticated, they are redirected to the login page

### Structure
The project structure evolves to accomodate the new functionalities:
```
part4/
|__README.md
|__base_files/					# Frontend folder
|	|__images/
|	|__static/
|	|	|__css_files/
|	|	|	|__login.css
|	|	|	|__place.css
|	|	|	|__review.css
|	|	|	|__styles.css
|	|	|__js_files/
|	|		|__add_review.js
|	|		|__index.js
|	|		|__login.js
|	|		|__places.js
|	|		|__scripts.js
|	|__templates/
|	|	|__add_review.html
|	|	|__index.html
|	|	|__login.html
|	|	|__place.html
|	|
|__	hbnb/					# Backend folder
	├── app/
	│   ├── __init__.py
	│   ├── api/           
	│   │   ├── __init__.py
	│   │   ├── v1/                         
	│   │       ├── __init__.py
	│   │       ├── users.py
	│   │       ├── places.py
	│   │       ├── reviews.py
	│   │       ├── amenities.py
	|   |       |__ auth.py                 
	|   |       |__ apiResources.py         
	│   ├── models/                         
	│   │   ├── __init__.py
	│   │   ├── user.py
	│   │   ├── place.py
	│   │   ├── review.py
	│   │   ├── amenity.py
	|   |   |__ baseEntity.py
	│   ├── services/                       
	│   │   ├── __init__.py
	│   │   ├── facade.py
	|   |   |__ AmenityService.py
	|   |   |__ PlaceService.py
	|   |   |__ ReviewService.py
	|   |   |__ UserService.py
	│   ├── persistence/                    
	│   |   ├── __init__.py
	│   |   ├── repository.py               
	|   |__ images/
	|   |   |__ ER Diagram.png              
	|   |   |__ ER Diagram_extra.png       
	|   |__ tests/                          
	|       |__ scripts/
	|       |   |__ populate_data.sh
	|       |   |__ tests_api.sh
	|       |__testSQL/
	|       |   |__ test_sql_crud.sql       
	|       |__ test_amenity.py
	|       |__ test_relationships.py
	|       |__ test_reviews.py
	|       |__ test_user.py
	├── run.py                             
	├── config.py
	├── requirements.txt
	|__ create_tables.sql                   
	├── README.md

```

### Installation
#### 0. Install python 3.10.12 (up to 3.12.3 version)
The application does not work with python 3.13 version

#### 1. Clone the repository
```
git clone https://github.com/Delphes1980/holbertonschool-hbnb.git desired_folder_name
```
then 
```
cd desired_folder_name/part4/hbnb/
```

#### 2. Create and activate a virtual environment
```
python3 -m venv venv
```
then
```
source venv/bin/activate
```

#### 3. Install dependecies
```
pip install -r requirements.txt
```

#### 4. Initialize the database
On your terminal, type down the following command:
```
mkdir instance; sqlite3 instance/development.db < create_tables.sql
```

#### 5. Application utilisation
From the hbnb directory (within part4), run:
```
python run.py
```

### Usage
After running the application, open your web browser and go to:
```
http://127.0.0.1:3000/base_files/templates/index.html
```
To login, you can use these various users to leave reviews:
- charles@ingalls.com
- big@daddy.com
- michael@myers.com
- carrie@bradshaw.com

All of these users have the same password: ```password```
**_⚠ WARNING:_** Never put important information like email or password on your README file! These details appear here in order to test the application and its various functionalities.


### Technologies used
- Frontend: HTML5, CSS3, Javascript ES6
- Backend: Python, Flask
- Database: SQLite

### Author
[Delphine Coutouly-Laborda](https://github.com/Delphes1980)