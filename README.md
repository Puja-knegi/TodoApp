# FastAPI Todo App

This is a basic FastAPI project with PostgreSQL and SQLAlchemy.

## Setup & Installation

1. **Open PowerShell** in your project folder.

2. **Create a virtual environment:**

```bash
python -m venv venv
```

## Activate the virtual environment:

```bash
.\venv\Scripts\Activate
```

## Usage

```bash
uvicorn main:app --reload
```

## Structure

- `models/`, `db/`
- `main.py`: Entry point

## API Example

### `GET /`

Returns a simple message.

#### Response

```json
{
  "message": "Hello Avenir"
}
