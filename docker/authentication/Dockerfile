FROM python:3.12-slim

ENV TZ="Europe/Moscow"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /home/user/app
WORKDIR /home/user/app

ADD . .
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential python3-dev libpq-dev
RUN rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get purge -y --auto-remove gcc build-essential python3-dev

RUN chmod u+x ./entrypoint.sh
CMD ./entrypoint.sh