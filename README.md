# CRUD Notes Application

A FastAPI-based CRUD application for managing notes with a PostgreSQL database and Docker support.

## Features

- **Create, Read, Update, Delete** operations for notes
- **FastAPI** framework for high-performance API
- **PostgreSQL** database for data persistence
- **Docker & Docker Compose** support for easy deployment
- **Automated Testing** with pytest
- **CI/CD** integration with GitHub Actions

## Project Structure

```
app/
├── main.py           # FastAPI application entry point
├── models.py         # Database models
├── database.py       # Database connection and configuration
├── test_app.py       # Unit tests
├── requirements.txt  # Python dependencies
└── Dockerfile        # Docker configuration
.github/
└── workflows/
    └── ci.yml        # GitHub Actions CI/CD pipeline
```

## Prerequisites

- Python 3.11+
- Docker & Docker Compose
- PostgreSQL (or use Docker)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hamzacse/CRUD.git
   cd CRUD
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r app/requirements.txt
   ```

## Running the Application

### Local Development

```bash
cd app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker

```bash
docker build -t fastapi-notes app/
docker run -p 8000:8000 fastapi-notes
```

## API Endpoints

- `GET /notes` - Retrieve all notes
- `GET /notes/{id}` - Retrieve a specific note
- `POST /notes` - Create a new note
- `PUT /notes/{id}` - Update a note
- `DELETE /notes/{id}` - Delete a note

## Testing

Run tests using pytest:

```bash
pytest app/test_app.py -v
```

## Dependencies

- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- psycopg2-binary (PostgreSQL adapter)

## CI/CD

This project uses GitHub Actions for continuous integration. Tests are automatically run on every push to the main branch.

## Author

**hamzacse** - itshamzakhan2002@gmail.com

## License

This project is open source and available under the MIT License.