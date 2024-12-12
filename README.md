# Expense Tracker

This repository contains a Django-based Expense Tracker application.

---

## Features
- User Registration and Login.
- Add, View, and Analyze Expenses.
- Responsive design using Bootstrap.
- Secure user authentication with CSRF protection.

---

## Prerequisites
1. Python 3.8+
2. Django (refer to `requirements.txt` for exact dependencies)
3. Git installed locally

---

## Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Spandana-M-Patil/Expense-Tracker.git
cd expense-tracker
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Collect Static Files
```bash
python manage.py collectstatic
```

### 6. Run the Application Locally
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` in your browser to view the app.

---

## Documentation
For a detailed guide on using the app:
1. Navigate to the "How It Works?" section on the Registration Page.
2. View the demo and documentation linked in the modal.

---

