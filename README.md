# Covid-19 Dashboard API

A REST API client for the [Covid-19 Dasoboard](https://github.com/zeshuaro/covid-19-dashboard)

## Getting Started

### Create your `.env` file

Run the following command to generate a secret key first:

```sh
openssl rand -hex 32
```

Then add the followings to your `.env` file:

```
SECRET_KEY=<SECRET_KEY>
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_DAYS=<TOKEN_LIFETIME_IN_DAYS>
```

### Setup virtual environment if you haven't done so

```sh
virtualenv venv
source venv/bin/activate
```

### Install the dependencies

```sh
pip install -r requirements.txt
```

### Setup your database

The app relies on [Firestore](https://cloud.google.com/firestore) on Google Cloud Platform (GCP). Create a project on GCP and initialise your Firestore database in native mode. Make sure you also initialise [gcloud cli](https://cloud.google.com/sdk/gcloud/) with `gcloud init`.

Obtain a hashed password with the following python code:

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
password="your_password"
print(pwd_context.hash(password))
```

Finally on Firestore, create a `users` collection and add a document with the followng fields:

```json
{
    "username": "username",
    "hashed_password": "hashed_password",
    "disabled": false
}
```

### Run the app

```sh
uvicorn app.main:app --reload
```

Go to `http://127.0.0.1:8000/docs` for Swagger docs or `http://127.0.0.1:8000/redoc` for ReDoc
