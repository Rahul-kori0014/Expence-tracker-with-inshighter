# Expense Tracker with Smart Insights

A full-stack Django web application to track daily expenses and provide smart financial insights.

## 🚀 Features
- User Authentication (Login/Register)
- Add, Edit, Delete Expenses
- Category-wise Expense Tracking
- Budget Management
- Smart Insights & Alerts
- Interactive Charts (Chart.js)

## 🛠️ Tech Stack
- Backend: Django (Python)
- Frontend: HTML, CSS, JavaScript
- Database: SQLite (can switch to MySQL)
- Charts: Chart.js

## ▶️ How to Run
1. Clone the repo
2. Create virtual environment
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run migrations:
```bash
python manage.py migrate
```
5. Create categories:
```bash
python create_categories.py
```
6. Run server:
```bash
python manage.py runserver
```
7. Open [http://localhost:8000](http://localhost:8000) in browser

8. https://expence-tracker-with-inshighter-1.onrender.com

## 📂 Project Structure
```
expense_tracker/
├── tracker/            # Main application
│   ├── models.py       # Database models
│   ├── views.py        # Business logic
│   ├── forms.py        # Forms
│   ├── urls.py         # URL patterns
│   └── templates/      # HTML templates
├── static/             # CSS, JS, Images
├── templates/          # Global templates
├── manage.py           # Django management script
└── requirements.txt    # Dependencies
```

## 📊 Screenshots

### Dashboard
![Dashboard](static/images/dashboard.png)

### Add Expense
![Add Expense](static/images/add_expense.png)

### Expense List
![Expense List](static/images/expense_list.png)

### Budgets
![Budgets](static/images/budgets.png)

### Categories
![Categories](static/images/categories.png)

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
