# Rule Engine Project

A comprehensive rule engine application built with Django, providing rule evaluation and management capabilities.

## Project Structure

The main components of the project are:

- rule_engine/: The main Django project directory
- rules/: The Django app containing the rule engine logic
- rules/models.py: Defines the data models for rules
- rules/views.py: Contains the views for rule management and evaluation
- rules/rule_engine.py: The core logic for rule evaluation

## Features

- Rule creation and management
- Rule evaluation engine
- API for rule operations
- Web interface for rule management

## Prerequisites

- Python 3.8+
- Django 3.2
- Other dependencies listed in requirements.txt

## Installation

1. Clone the repository
```bash
git clone https://github.com/your-username/rule_engine.git
cd rule_engine
```
2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install required packages
```bash
pip install -r requirements.txt
```
4. Apply database migrations
```bash
python manage.py migrate
```
5. Create a superuser (optional)
```bash
python manage.py createsuperuser
```

## Usage

1. Start the development server
```bash
python manage.py runserver
```
2. Open a web browser and navigate to http://127.0.0.1:8000/
3. To access the admin interface, go to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

## Running Tests

Execute the test suite by running: python manage.py test

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- OpenWeatherMap API for providing weather data
- Django community for the excellent web framework
- All contributors who have helped shape this project

## Screenshots

### Home Page
![Home Page](images/rules%20homepage1.png)
![Home Page](images/rules%20homepage2.png)

### Weather Summary
![Evaluate](images/evaluate%20page.png)