FROM python:3.8.1-slim

# set work directory
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip wheel \
    && pip install -r /tmp/requirements.txt \
    && pip cache purge \
    && rm -rf /root/.cache/pip

COPY ./src /usr/src/app/
