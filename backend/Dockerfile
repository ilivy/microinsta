FROM tiangolo/uvicorn-gunicorn-fastapi

# ARG USER_ID=1000
# ARG GROUP_ID=1000
# RUN addgroup --gid $GROUP_ID user
# RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
# USER user

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

ENV PRE_START_PATH = "/app/prestart.sh"

ENV POSTGRES_USER=postgresuser
ENV POSTGRES_PASSWORD=postgresuser
ENV DB_HOST = dbhost
ENV DB_PORT = 5432
ENV DB_NAME = dbname
ENV JWT_SECRET = replace-it-with-secret
ENV AWS_ACCESS_KEY = awskey
ENV AWS_SECRET_KEY = awssecret
ENV AWS_BUCKET_PHOTO = awsbucket
ENV AWS_REGION = awsregion

