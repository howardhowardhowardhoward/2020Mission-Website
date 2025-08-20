# 2020Mission Eyeglass Manager

**2020Mission** is a Flask-based web application for managing eyeglass inventory and prescription data. It features admin tools for adding, editing, and searching for eyeglass information using a web interface backed by a MySQL database.

## Features

- Add and manage frame and lens data
- Search eyeglasses by ID
- Built-in validation and error handling
- User authentication and admin panel
- MySQL database integration

## Tech Stack

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS (Jinja2 templates)
- **Database**: MySQL

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL server
- `pip` package manager

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/2020Mission_Eyeglass_Manager.git
   cd 2020Mission_Eyeglass_Manager/2020Mission
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt.txt
   ```

4.Setup MySQL database using the schema in the repository.

5. Create a `.env` file in your project root with the following content:

```env
DB_HOST=your_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_db_name
```

6. Run the app:
   ```bash
   python Main.py
   ```

7. Visit [http://localhost:5001](http://localhost:5001) in your browser.

## Project Structure

```
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
```
