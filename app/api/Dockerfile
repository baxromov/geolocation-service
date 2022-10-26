FROM python:3.9

WORKDIR api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt-get update \
    && apt-get -y install kafkacat\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /api/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt

COPY . /api

COPY entrypoint.sh /api/entrypoint.sh
RUN chmod +x entrypoint.sh

#ENTRYPOINT ["sh", "/api/entrypoint.sh"]