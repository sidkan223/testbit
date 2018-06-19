FROM python:3

ENV RABBITMQ_URI="amqp://guest:guest@rabbitmq/%2F"
EXPOSE 9999

RUN pip install pika requests

WORKDIR /src
COPY monitor.py /src/

CMD python monitor.py
