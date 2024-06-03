# Django Library Management System Backend

This is a Django-based Library Management System that allows a librarian to manage books, members, and issued books. It also provides functionalities for members to view their current fines after login .

## Features

- **Librarian Functions:**
  - Add, update, delete books
  - Issue and return books
  - Add, update, delete member
- **Member Functions:**
  - View list of books
  - View current fine status

## Requirements

- Python 3.10 or +
- Django 5.0.6
- Django REST Framework
- Django CORS Headers

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/Pasindu-Vishmika/lib_backend.git
    cd lib_backend
    ```

2. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```
## Changing Database to MySQL

To change the database to MySQL, follow these steps:

- **Install MySQL Client:**

    ```sh
    pip install mysqlclient
    ```

- **Update `DATABASES` in `settings.py`:**

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',  # Or the database server IP
            'PORT': '3306',       # Default MySQL port
        }
    }
    ```


## Changing Database to PostgreSQL

To change the database to PostgreSQL, follow these steps:

- **Install PostgreSQL Client:**

    ```sh
    pip install psycopg2-binary
    ```

- **Update `DATABASES` in `settings.py`:**

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',  # Or the database server IP
            'PORT': '5432',       # Default PostgreSQL port
        }
    }
    ```


3. **Run migrations:**

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create a superuser:**

    ```sh
    python manage.py createsuperuser
    ```

5. **Run the development server:**

    ```sh
    python manage.py runserver
    ```

## Usage

### API Endpoints

- **Login:** `POST /api/login/`
- **Logout:** `POST /api/logout/`
- **Add Book:** `POST /api/add-book/`
- **Get Books:** `GET /api/book-list/`
- **Get Book Details:** `GET /api/book/<str:pk>/`
- **Update Book:** `PUT /api/update-book/<str:pk>/`
- **Delete Book:** `DELETE /api/delete-book/<str:pk>/`
- **Issue Book:** `POST /api/issue-book/<str:pk>/`
- **Return Book:** `POST /api/return-book/<str:pk>/`
- **Add Member:** `POST /api/add-member/`
- **Get Members:** `GET /api/member-list/`
- **Get Member Details:** `GET /api/member/<str:pk>/`
- **Update Member:** `PUT /api/update-member/<str:pk>/`
- **Delete Member:** `DELETE /api/delete-member/<str:pk>/`
- **Get Member Fine:** `GET /api/member-fine/`

### Example Requests

- **Login:**

    ```sh
    curl -X POST http://127.0.0.1:8000/api/login/ -H "Content-Type: application/json" -d '{"username": "your email", "password": "your password"}'
    ```

- **Get Books:**

    ```sh
    curl -X GET http://127.0.0.1:8000/api/book-list/ -H "Authorization: Token <your-token>"
    ```

- **Issue Book:**

    ```sh
    curl -X POST http://127.0.0.1:8000/api/issue-book/1/ -H "Authorization: Token <your-token>" -H "Content-Type: application/json" -d '{"member_id": 2, "issue_date": "2024-06-01", "due_date": "2024-06-15"}'
    ```

