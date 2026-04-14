# Help Desk Ticket System

This project is a Flask-based help desk application backed by MySQL. Users can sign up, log in, create support tickets, and view or update tickets based on their role.

## Features

- User signup and login
- Session-based authentication
- Ticket creation, filtering, updating, and deletion
- Admin-only commenting
- Category, priority, and status support

## Tech Stack

- Python
- Flask
- MySQL
- Jinja templates

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and set your local values:

```env
FLASK_SECRET_KEY=replace-with-a-random-secret
DB_HOST=127.0.0.1
DB_USER=root
DB_PASSWORD=your-password
DB_NAME=helpdesk
```

4. Make sure your MySQL database contains the tables used by the app:
   `User`, `Ticket`, `Comment`, `Status`, `Priority`, and `Category`.

5. Run the app:

```bash
python app.py
```

The default local URL is `http://127.0.0.1:5000`.

## Security Note

Sensitive values such as the Flask secret key and database credentials should never be committed directly into source control. This repository is now set up to load them from environment variables instead.
