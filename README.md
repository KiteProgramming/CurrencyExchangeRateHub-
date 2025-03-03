# My Fullstack App

This project is a fullstack application that combines a Django backend with a React frontend, using PostgreSQL as the database.

## Project Structure

```
my-fullstack-app
├── backend
│   ├── myproject
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── manage.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.js
│   │   ├── index.js
│   │   └── components
│   │       └── ExampleComponent.js
│   ├── package.json
│   ├── .babelrc
│   ├── .eslintrc.js
│   └── README.md
├── docker-compose.yml
└── README.md
```

## Backend

The backend is built using Django and serves as the API for the application. It is configured to use PostgreSQL as the database.

### Setup

1. **Navigate to the `backend` directory**:
   ```sh
   cd my-fullstack-app/backend
   ```

2. **Create a virtual environment and activate it**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Create a `.env` file in the `backend` directory and add the following environment variables**:
   ```properties
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ENCRYPTION_KEY=By2kGKY6DC4oaJkVvN0hQowXM5Z6EhiSTzMF4LFU08I=
   DB_NAME=exchange
   DB_USER=postgres
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

5. **Run the migrations**:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the server**:
   ```sh
   python manage.py runserver
   ```

### Running Unit Tests

To run the unit tests for the backend, use the following command:
```sh
python manage.py test
```

## Frontend

The frontend is built using React and serves as the user interface for the application.

### Setup

1. **Navigate to the `frontend` directory**:
   ```sh
   cd my-fullstack-app/frontend
   ```

2. **Install the required packages**:
   ```sh
   npm install
   ```

3. **Start the development server**:
   ```sh
   npm start
   ```

## Docker

**Note**: The Docker solution will not work as expected due to package issues. Docker has been removed from the equation.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.