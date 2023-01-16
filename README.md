# Demo project "Micro Insta"

A demo app to **post photos** and comment on them.

## Technologies

- Python (FactAPI, TensorFlow, PyTest)
- PostgreSQL
- Amazon Web Services
- React
- Git, Docker, Kubernetes

## Implementation

Data is stored in a PostgreSQL database. **Api** service processes the data, it also utilizes **Face** service with a trained Neural Network to predict the age, gender and race of a person in an uploaded image. 
**Frontend** service provides a user interface.

'Bearer tokens' Authentication is used to authorize users.

Images are stored using **AWS s3** service.

API endpoints are covered by tests.


**Services**:
- **Api**: API written on *Python* using *FastAPI* framework
- **Face**: a *Python* application with a Neural Network, working with images
- **Frontend**: a *React* frontend application 
- **Postgres**: a postgresql database instance

The project is **dockerized**.

**Kubernetes** scripts are available in the `kubernetes/` folder.


The codebase is available on [GitHub](https://github.com/ilivy/udemyinsta).


## Development

### Local development

##### Postgres service
In the root project directory:
- run `docker-compose run -d --rm -p 5438:5432 postgres`
- create a database for the project (**Postgres** instance will be available at port `5438`)

##### Face service
In `face` directory:
- create a Python virtual environment by running `python3 -m venv venv`
- activate the virtual environment by running `source venv/bin/activate`
- run `pip install -r requirements.txt` to install dependencies
- run `uvicorn app.main:app --reload --port 8081` to start a server
- open [http://localhost:8081/docs](http://localhost:8081/docs) to view **the API** in your browser

##### API service
In `api` directory:
- create a Python virtual environment by running `python3 -m venv venv`
- activate the virtual environment by running `source venv/bin/activate`
- run `pip install -r requirements.txt` to install dependencies
- check the default configuration in `core/config.py`
- run `alembic upgrade head` to apply migrations to the database
- run `uvicorn app.main:app --reload` to start a server
- open [http://localhost:8000/docs](http://localhost:8000/docs) to view **the API** in your browser

##### Frontend service
In `frontend` directory:
- run `npm install`
- run `npm start`
Or using Docker service:
- run `docker-compose run -d --rm -p 3000:3000 --no-deps frontend`
- open [http://localhost:3000](http://localhost:3000) to view **the frontent** in your browser


### Development with Docker containers
In the root project directory:
- rename `env/api.env.dist` into `env/api.env` and `env/postgres.env.dist` into `env/postgres.env` to use env variables
- run `docker-compose up -d` to run all the containers
- create a database for the project (**Postgres** instance will be available at port `5438`)
- run `docker-compose run --rm api alembic upgrade head` to migrate the database
- or run `docker-compose run --rm alembic upgrade head` to migrate the database via a separate service **alembic**
- run api tests with `docker-compose run api pytest` (set database_url to a test one)
- run frontend tests with `docker-compose run frontend npm test`
- open [http://localhost:8000/docs](http://localhost:8000/docs) to view **the backend** in your browser
- open [http://localhost:3000](http://localhost:3000) to view **the API** in your browser


## Kubernetes

In `kubernetes/` directory:
- rename `environment.yml.dist` into `environment.yml` to use env variables
- from outside the folder (in the root project directory) run:
```bash
kubectl apply -f kubernetes/
```

