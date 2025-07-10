

2020Mission Eyeglass Manager

2020Mission is a Flask-based web application for managing eyeglass inventory and prescription data. It features admin tools for adding, editing, and searching for eyeglass information using a web interface backed by a MySQL database.

Features
	•	Add and manage frame and lens data
	•	Search eyeglasses by ID
	•	Built-in validation and error handling
	•	User authentication and admin panel
	•	MySQL database integration

Tech Stack
	•	Backend: Python (Flask)
	•	Frontend: HTML, CSS (Jinja2 templates)
	•	Database: MySQL

Prerequisites
	•	Python 3.10+
	•	MySQL server
	•	pip package manager

Installation
	1.	Clone the repository:

git clone https://github.com/your-username/2020Mission_Eyeglass_Manager.git
cd 2020Mission_Eyeglass_Manager/2020Mission


	2.	Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


	3.	Install dependencies:

pip install -r requirements.txt


	4.	Configure your MySQL connection in Website/__init__.py:

mysql.connector.connect(
    host='your_host',
    user='your_username',
    password='your_password',
    database='your_db_name'
)


	5.	Run the app:

python Main.py


	6.	Visit http://localhost:5001 in your browser.

📁 Project Structure

2020Mission/
│
├── Main.py                 # Entry point for Flask app
├── Website/                # Flask app package
│   ├── __init__.py         # App factory and DB config
│   ├── views.py            # Frontend routes
│   ├── auth.py             # Authentication logic
│   ├── functions.py        # Database interaction and utilities
│   └── templates/          # HTML templates (not shown)
└── README.md               # Project documentation
