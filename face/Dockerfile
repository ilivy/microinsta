FROM python:3.8 as production

WORKDIR /appdir

RUN apt-get -y update && \
    apt-get -y upgrade

COPY requirements.txt .
RUN pip install -r requirements.txt
# RUN pip install git+https://github.com/rcmalli/keras-vggface.git

COPY ./app .
ENV PYTHONPATH=.

COPY start.sh .
EXPOSE 8081

CMD [ "sh", "-c", "uvicorn main:app --reload --host 0.0.0.0 --port 8081" ]
# CMD [ "sh", "start.sh" ]
