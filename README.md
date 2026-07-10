# PostgreSQL-DB_with_Flask

A secure Python-Flask web application featuring user authentication (Login, Registration, Password Recovery) and a dynamic User Dashboard, fully integrated with a PostgreSQL database.

## 🚀 Features
- **User Authentication**: Secure signup, login, and logout system.
- **Password Recovery**: Forgot password feature for user convenience.
- **Dynamic Dashboard**: Personalized user area after successful login.
- **PostgreSQL Database**: Relational database for safe and structured data storage.
- **Responsive UI**: Clean design built with HTML5, CSS3, and JavaScript.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com
cd PostgreSQL-DB_with_Flask
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.required
```
*(Make sure your requirements file includes: flask, psycopg2-binary, flask-sqlalchemy, etc.)*

### 4. Database Configuration
Create a PostgreSQL database and update your environment variables or connection string inside `app.py`:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost:5432/your_database_name'
```

### 5. Run the Application
```bash
python main.py
```
Open `http://127.0.0` or `http://192.168.1.9...` in your web browser.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
