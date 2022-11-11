# Demo project "Micro Insta"

A demo system which allows users to **post pictures** with captions and add comments to existing posts.
A Neural Network can **predict a gender, a race and an age of persons** on the pictures

## Implementation

The data is stored in a PostgreSQL database instance. The **api** service processes the data, when saving images it calls the **face** service.
**Face** service utilises a trained Neural Network to predict person's data on the pictures. 
The **Frontend** service provides the user interface.

'Bearer tokens' Authentication is used to authorize users.

The images are stored using the **AWS s3** service.

The API endpoints are covered by tests.


The system consists of:
- **api service**: API written on *Python* using *FastAPI* framework
- **face service**: a *Python* application with a Neural Network, working with images
- **frontend service**: a *React* frontend application 
- **postgres service**: a postgresql database instance

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
- run tests with `docker-compose run api pytest` (set database_url to a test one)
- open [http://localhost:8000/docs](http://localhost:8000/docs) to view **the backend** in your browser
- open [http://localhost:3000](http://localhost:3000) to view **the API** in your browser


## Kubernetes

In `kubernetes/` directory:
- rename `environment.yml.dist` into `environment.yml` to use env variables
- from outside the folder (in the root project directory) run:
```bash
kubectl apply -f kubernetes/
```

