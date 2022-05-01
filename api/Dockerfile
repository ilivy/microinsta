FROM python:3.9 as production

WORKDIR /appdir

RUN apt-get -y update && \
    apt-get -y upgrade

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app ./app
ENV PYTHONPATH=.

COPY alembic.ini .
COPY start.sh .
EXPOSE 8000

ENV ENVIRONMENT="dev"
ENV DATABASE_URL="postgresql://postgres:postgres@postgres:5432/postgres"
ENV JWT_SECRET="secret"
ENV AWS_ACCESS_KEY="secret"
ENV AWS_SECRET_KEY="secret"
ENV AWS_BUCKET_PHOTO="bucket"
ENV AWS_REGION="region"

# CMD [ "sh", "-c", "uvicorn app.main:app" ]
CMD [ "sh", "start.sh" ]


# For development build
FROM production as development

COPY pytest.ini .
COPY ./tests ./tests
