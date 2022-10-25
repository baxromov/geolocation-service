FROM python:3.9

WORKDIR geolocation_service

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get -y install kafkacat\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /geolocation_service/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /geolocation_service/requirements.txt

COPY . /geolocation_service

COPY entrypoint.sh /geolocation_service/entrypoint.sh
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "/geolocation_service/entrypoint.sh"]