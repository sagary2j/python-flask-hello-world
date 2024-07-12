# Set base image (host OS)
FROM python:3.12-alpine

ENV AWS_DEFAULT_REGION=us-east-1

WORKDIR /app

RUN pip install boto3 flask
RUN apk update && apk add curl

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
