The solution to the exercise: Property Space Analysis API. 

## Getting Started

### Creating virtual environment

```bash
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

The server will be running at port 8000 by default. You can find the API documentation at http://localhost:8000/api/v1/docs.

## API Endpoints

To manually test the API endpoints, you need to provide the `AUTH_TOKEN` in the request headers. 

To create a property space, you can use the following command:

```bash
curl -X POST -H "Authorization: Bearer changeme" -H "Content-Type: application/json" -d '{"name": "New Space for Testing", "address": {"street": "123 Test St", "city": "Test City", "state": "TS", "country": "U.S.", "postal_code": "12345"}}' http://localhost:8000/api/v1/property-spaces
```

Note: The length of the address fields should be between 2 and 64 characters. The length of the name field should be between 2 and 128 characters.

To list all property spaces, you can use the following command:

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces
```

To get a property space by ID, you can use the following command:

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1
```

To get a property space by ID and apply the "year" filter, you can use the following command: 

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1?year=2021
```

For property space with ID 1, if you have loaded data from `api_testing_fixture.json`, the response will be:

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

Note that the total consumption has changed from 1000.0 to 5000.0. This is because the consumption data for the year 2022 is different from the year 2021. You can find the consumption data in the `api_testing_fixture.json` file. For more details, please refer to the "[Sample Data](#sample-data)" section below.

To update a property space, you can use the following command:

```bash
curl -X PUT -H "Authorization: Bearer changeme" -H "Content-Type: application/json" -d '{"name": "Updated Space for Testing"}' http://localhost:8000/api/v1/property-spaces/1
```

To delete a property space, you can use the following command:

```bash
curl -X DELETE -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/property-spaces/1
```

To demonstrate the custom Exception handling, you can use the following command:

```bash
curl -H "Authorization: Bearer changeme" http://localhost:8000/api/v1/service-unavailable-exception
```

We intentionally raised a `ServiceUnavailableException` exception to demonstrate the custom exception handling. The response will be:

```json
{
  "message": "We are simulating a service unavailable exception. Please retry later"
}
```

## Running the automated tests

```bash
python manage.py test
```

Note that the fixture `api_testing_fixture.json` is used to load the initial test data for the automated tests. Please do not delete this file.


## Limitations and Future Suggestions


### Authentication and Authorization

- The API uses a basic token-based authentication for demonstration purposes. In a real-world scenario, a more secure and robust authentication method, such as OAuth2 or JWT, should be implemented.


### Extendability

- The project structure can be improved for better extensibility. Separate apps for each resource (e.g., property_space, address, unit_space, meter_data) would make the code more modular and maintainable. For demonstration purposes, everything is currently in a single app.
- For larger projects, the endpoints, schema, and exceptions should be split into separate files to improve organization and maintainability.


### Query Efficiency

- The API uses `prefetch_related` to avoid the `N + 1` problem when querying related objects. For better performance with large datasets in traditional SQL databases, redundant fields (e.g., total_area, total_consumption) can be added to models to store aggregated data. These fields can be updated regularly using signals or background tasks. This trade-off improves query efficiency at the cost of data consistency.
- Dedicated database indexes should be added to improve query performance for frequently accessed fields.
- Elasticsearch or other search engines can be used for complex search queries and aggregations.
- Caching can be implemented to reduce the load on the database for read-heavy applications.
- Pagination should be implemented for large datasets to improve performance and reduce the response size.


### Error Handling

- The API uses custom exception handling for demonstration purposes. In a real-world scenario, different types of exceptions should be handled more gracefully with structured error responses. All potential errors, their status codes, and messages should be documented in the API documentation.


### REST Framework Choices

- The project uses Django Ninja for the REST API due to its simplicity and ease of use. Other popular choices include Django REST Framework (DRF), which is widely adopted in the Django community. If extending an existing DRF project, it is better to stick with DRF for consistency.


## Additional Notes

While working on the assignment, I made a few assumptions due to the time constraints and to avoid disturbing you outside of work hours. I hope these are acceptable:

1. I assumed the model for meter data and unit space has a many-to-many relationship. Meter data shared between multiple unit spaces is divided equally among them. For example, if unit space 1 and unit space 2 both use meter data 1 (100 kWh), the total consumption for each space is considered 50 kWh.
2. I did not create a dummy user for authentication. Instead, I used a token-based mechanism, with the token set in the environment variable `AUTH_TOKEN`. I hope this is acceptable for the assignment.

## Sample Data

To help you understand the sample data in the `api_testing_fixture.json` file, here are the table views of the data:

**Property Space**
ID  | Name             | Address ID
--- | ---              | ---
1   | property space 1 | 1
2   | property space 2 | 2
3   | property space 3 | 3

**Address**
ID  | Street       | City         | State | Country | Postal Code
--- | ---          | ---          | ---   | ---     | ---
1   | 123 Main St  | San Francisco| CA    | USA     | 94105
2   | 456 Main St  | San Francisco| CA    | USA     | 94105
3   | 789 Main St  | San Francisco| CA    | USA     | 94105

**Unit Space**
ID  | Name         | Unit Type    | Area | Property Space ID
--- | ---          | ---          | ---  | ---
1   | unit space 1 | COMMON_AREA  | 1000 | 1
2   | unit space 2 | VACANT       | 2000 | 1
3   | unit space 3 | LEASED       | 3000 | 1
4   | unit space 4 | COMMON_AREA  | 4000 | 2
5   | unit space 5 | COMMON_AREA  | 5000 | 3

**Meter Data**
ID  | Meter Number | Meter Provider Name | Meter Source | Measurement Reading | Measurement Unit | Measurement Start Date | Measurement End Date
--- | ---          | ---                 | ---          | ---                 | ---              | ---                   | ---
1   | 1            | provider 1          | source 1     | 1000                | kWh              | 2021-01-01T00:00:00Z  | 2021-01-31T23:59:59Z
2   | 2            | provider 2          | source 2     | 2000                | kWh              | 2022-02-01T00:00:00Z  | 2022-02-28T23:59:59Z
3   | 3            | provider 3          | source 3     | 3000                | kWh              | 2022-03-01T00:00:00Z  | 2022-03-31T23:59:59Z
4   | 4            | provider 4          | source 4     | 4000                | kWh              | 2023-04-01T00:00:00Z  | 2023-04-30T23:59:59Z
5   | 5            | provider 5          | source 5     | 5000                | kWh              | 2024-05-01T00:00:00Z  | 2024-05-31T23:59:59Z
6   | 6            | provider 6          | source 6     | 6000                | kWh              | 2022-06-01T00:00:00Z  | 2022-06-30T23:59:59Z

**Meter Data - Unit Space**
ID | Meter Data ID | Unit Space ID
---| ---           | ---
1  | 1             | 1
2  | 2             | 2
3  | 3             | 3
4  | 4             | 4
5  | 5             | 5
6  | 6             | 4
7  | 6             | 5

