# FROM dockerhub.nftgo.dev/data-api/api-admin:base
FROM python:3.9

USER root

WORKDIR /app

COPY src/ /app
COPY requirements.txt /tmp

# confirm
RUN pip install --retries=3 --timeout=5 -r /tmp/requirements.txt

ENV PYTHONPATH /app/src

CMD ["python", "subscribe.py"]
