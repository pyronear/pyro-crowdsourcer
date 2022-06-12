FROM python:3.8.1-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


COPY ./requirements.txt /tmp/requirements.txt

RUN apt-get update \
    && pip install --upgrade pip wheel \
    && pip install -r /tmp/requirements.txt \
    && pip cache purge \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /root/.cache/pip

COPY ./src src/

CMD ["gunicorn", "-b 0.0.0.0:80", "src.app:server"]
