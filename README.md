# Demo project "Micro Insta"

A demo **web application** to post photos and comment on them.

REST API + microservice with Neural Network + Single Page Application.

## Technologies

- Python (FastAPI, TensorFlow, PyTest)
- PostgreSQL
- Amazon Web Services (s3)
- React
- Git, Docker, Kubernetes

## Implementation

**Api** is a RESTful application working with data, it also utilizes **Face** service with a trained Neural Network to predict the age, gender and race of a person in an uploaded image. The data is stored in a PostgreSQL database. **Frontend** service provides UI. 


'Bearer tokens' Authorization is used (JWT with secret).

Images are stored using **AWS s3** service.

API endpoints are covered by tests.


**Services**:
- **Api**: RESTful API written on *Python* using *FastAPI* framework
- **Face**: a *Python* application with a Neural Network, working with images
- **Frontend**: a *React* frontend application 
- **Postgres**: a postgresql database instance

The project is **dockerized**.

**Kubernetes** scripts are available in the `kubernetes/` directory.


The codebase is available on [GitHub](https://github.com/ilivy/microinsta).


## Development

### Local development

##### Postgres service
In the root project directory:
- run `docker-compose run -d --rm -p 5438:5432 postgres`

##### Face service
In `face` directory:
- create a Python virtual environment by running `python3 -m venv venv`
- activate the virtual environment by running `source venv/bin/activate`
- run `pip install -r requirements.txt` to install dependencies
- run `uvicorn app.main:app --reload --port 8081` to start a server
- open [http://localhost:8081/docs](http://localhost:8081/docs) to view **the API**

##### API service
In `api` directory:
- create a Python virtual environment by running `python3 -m venv venv`
- activate the virtual environment by running `source venv/bin/activate`
- run `pip install -r requirements.txt` to install dependencies
- check the default configuration in `core/config.py`
- run `alembic upgrade head` to apply migrations to the database
- run `uvicorn app.main:app --reload` to start a server
- open [http://localhost:8000/docs](http://localhost:8000/docs) to view **the API**

##### Frontend service
In `frontend` directory:
- run `npm install`
- run `npm start`
Or using Docker service:
- run `docker-compose run -d --rm -p 3000:3000 --no-deps frontend`
- open [http://localhost:3000](http://localhost:3000)


### Development with Docker containers
In the root project directory:
- rename `env/api.env.dist` into `env/api.env` and `env/postgres.env.dist` into `env/postgres.env` to use env variables
- run `docker-compose up -d`
- run `docker-compose run --rm api alembic upgrade head` to migrate the database
- or run `docker-compose run --rm alembic upgrade head` to migrate the database via a separate service **alembic**
- run api tests with `docker-compose run api pytest` (set database_url to a test one)
- run frontend tests with `docker-compose run frontend npm test`
- open [http://localhost:8000/docs](http://localhost:8000/docs) to view **the backend API**
- open [http://localhost:3000](http://localhost:3000) to access **the frontend**


## Kubernetes

In `kubernetes/` directory:
- rename `environment.yml.dist` into `environment.yml` to use env variables
- in the project root directory run:
```bash
kubectl apply -f kubernetes/
```

