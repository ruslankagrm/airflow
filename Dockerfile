FROM python:3.9.4-slim-buster

WORKDIR /airflow
COPY . .
RUN apt-get update && \
    apt-get install -y gcc make libffi-dev git g++ libsasl2-dev libsasl2-modules-gssapi-mit unixodbc unixodbc-dev && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*


RUN pip install -U pip


RUN pip install pipenv

COPY Pipfile.lock Pipfile /airflow/

RUN pipenv install Pipfile

EXPOSE 9000
