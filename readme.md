# Silky

Silky is an online digital store built with Django and Django REST Framework. The project is designed with a modular architecture and focuses on product management, category organization, user authentication, and product ratings.

> ⚠️ This project is currently under active development.

## Features

### Current Features

* User Authentication System
* User Dashboard
* Product Management
* Product Detail Pages
* Product Rating System
* Category & Subcategory Management
* Product Filtering
* Responsive User Interface
* Modular Django Architecture
* contact us

### Upcoming Features

* Shopping Cart
* Cart Management
* Order Processing
* Payment Gateway Integration
* Order History
* Blog System
* Django REST Framework Integration


## Tech Stack

### Backend

* Django
* Django REST Framework (DRF)
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Alpine.js

## Project Structure

```text
Silky
│
├── category/
├── config/
├── core/
├── product/
├── user/
│
├── static/
├── media/
├── templates/
│
└── manage.py
```

## Application Modules

### User App

Responsible for:

* User Registration
* Authentication
* User Management
* User address

### Category App

Responsible for:

* Categories
* Categories Attributes
* Nested Categories
* Product Classification
* Category managment

### Product App

Responsible for:

* Product Management
* Product Details
* Product Ratings
* Product Filtering
* Product Review

### Core App

Shared functionality and reusable components across the project.
* Contact us Page managment
* Contact form

## Installation

Clone the repository:

```bash
git clone https://github.com/SinaParekari/Silky.git
cd Silky
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

## Screenshots

### Home Page

![Home Page](screenshots/home.png)

### Product Listing

![Products](screenshots/products.png)

### Login and Register Page

![Login](screenshots/login.png)
![Register](screenshots/register.png)

### Dashboard and Profile Page

![Dashboard](screenshots/dash.png)
![Profile](screenshots/Profile.png)

### Contact us Page

![Contact-us](screenshots/contact.png)


## Future Improvements

* PostgreSQL Support
* REST API Expansion
* Shopping Cart & Checkout
* Payment Integration
* Order Management
* Performance Optimization

## Author

**Sina Parekari**

GitHub:
https://github.com/SinaParekari/Silky
