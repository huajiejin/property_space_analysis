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

### Setting up the environment variables

Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
echo "AUTH_TOKEN=changeme" > .env
```

The `AUTH_TOKEN` is used to authenticate the requests to the API. You can change it to any value you want.

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

The server will be running at port 8000 by default. You can find the API documentation at `http://localhost:8000/api/v1/docs`.

To manually test the API endpoints, you need to provide the `AUTH_TOKEN` in the request headers. 

To create a property space, you can use the following command:

```bash
curl -X POST -H "Authorization: Bearer changeme" -H "Content-Type: application/json" -d '{"name": "New Space for Testing", "address": {"street": "123 Test St", "city": "Test City", "state": "TS", "country": "U.S.", "postal_code": "12345"}}' http://localhost:8000/api/v1/property-spaces
```

To list all property spaces, you can use the following command:

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces
```

To get a property space by ID, you can use the following command:

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1
```

To get a property space by name, and apply the "year" filter, you can use the following command: 

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1?year=2021
```

For property space with ID 1, the response will be:

```json
{
  "name":"property space 1",
  "address":{
    "street":"123 Main St",
    "city":"San Francisco",
    "state":"CA",
    "country":"USA",
    "postal_code":"94105"
  },
  "number_of_units":3,
  "total_area":6000.0,
  "total_consumption":1000.0,
  "consumption_unit":"kWh"
}
```

If you change the year to 2022, and run it again, the response will be:

```json
{
  "name":"property space 1",
  "address":{
	"street":"123 Main St",
	"city":"San Francisco",
	"state":"CA",
	"country":"USA",
	"postal_code":"94105"
  },
  "number_of_units":3,
  "total_area":6000.0,
  "total_consumption":5000.0,
  "consumption_unit":"kWh"
}
```

Note that the total consumption has changed from 1000.0 to 5000.0. This is because the consumption data for the year 2022 is different from the year 2021. You can find the consumption data in the `api_testing_fixture.json` file.

To update a property space, you can use the following command:

```bash
curl -X PUT -H "Authorization: Bearer changeme" -H "Content-Type: application/json" -d '{"name": "Updated Space for Testing"}' http://localhost:8000/api/v1/property-spaces/1
```

To delete a property space, you can use the following command:

```bash
curl -X DELETE -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1
```

### Running the automated tests

```bash
python manage.py test
```

Note that the fixture `api_testing_fixture.json` is used to load the initial test data for the automated tests. Please do not delete this file.
