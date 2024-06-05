The solution to the exercise: Property Space Analysis API. 

## Getting Started

### Creating virtual environment

```bash
# For Python 3
python3 -m venv .venv
```

### Activating the virtual environment

```bash
source .venv/bin/activate
```

### Installing dependencies

```bash
pip install -r requirements.txt
```

### Setting up the database

For simplicity, we will use SQLite as the database, which is already configured in the settings.py file.

To run the migrations, execute the following command:

```bash
python manage.py migrate
```

To load the initial test data, execute the following command:

```bash
python manage.py loaddata api_testing_fixture.json
```

### Running the server

```bash
python manage.py runserver
```

The server will be running at http://localhost:8000

### Running the automated tests

```bash
python manage.py test
```

Note that the fixture `api_testing_fixture.json` is used to load the initial test data for the automated tests.
