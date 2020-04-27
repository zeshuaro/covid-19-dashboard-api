# Covid Dashboard API

## Getting Started

### Setup virtual environment if you haven't done so

```sh
virtualenv venv
source venv/bin/activate
```

### Install the dependencies

```sh
pip install -r requirements.txt
```

### Run the app

```sh
uvicorn app.main:app --reload
```

Go to `http://127.0.0.1:8000/docs` for Swagger docs or `http://127.0.0.1:8000/redoc` for ReDoc
