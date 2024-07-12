## Hello World Flask Application Deployment using AWS ECS and AWS DynamoDB
=======================

This is a simple "Hello World" application that exposes two HTTP-based APIs:

* `PUT /hello/<username>`: Saves or updates the given user's name and date of birth in the database.
* `GET /hello/<username>`: Returns a hello message for the given user, including their birthday message if it's today or in the next N days.

Requirements
------------
* Docker(local)
* Terraform
* Python 3.8+
* Flask 2.0+
* SQLite3(local)
* AWS account for deployment
* AWS DynamoDB

### 0. Contents
- `app/`
  - contains a Python Flask application, which is hooked up to DynamoDB
- `terraform/`
  - contains the terraform code necessary to deploy the application into AWS
  
### 1. Local Development Run

1. Install dependencies: `pip install flask sqlite3`
2. Run the application: `python applocal.py`
3. Run test: `python -m unittest tests/test_app.py`
3. Test the APIs using `curl` or a tool like Postman

### 2. How-to Deploy into AWS ECS using github action CI/CD and Terraform for IAC
general workflow: 
1. work and build the docker image
2. tag the docker image with the environment variable(see example below)
3. push the image to ecr repository(see example below)
4. run terraform init & plan, then apply
5. terraform will output the alb url at the end of the run

## 3. Steps
- Download and extract this repo


(docker)
- run this command in terminal:

export AWS_ID=$(aws sts get-caller-identity --query Account --output text) && export AWS_REGION=$(aws configure get region &&--output text) && export AWS_ECR=flask-docker-twingate

- run the shell script: setup.sh (this will connect and login to aws ecr)  
- from the app folder, run docker build
- tag the image:
docker tag $AWS_ECR:latest $AWS_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR:latest
- push the image to ecr repository:
docker push $AWS_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$AWS_ECR:latest


(terraform)
- once the image was uploded to ecr, enter the terraform directory and create a file "credentials", insert:

[default]
aws_access_key_id=<access_key>
aws_secret_access_key=<secret_access_key>
region=us-west-2
output=json

- set the access key & secret access key to the credentials file

- run:
terraform init
- after we initialized the working directory, run the plan:
terraform plan
- if the plan is without any errors, we can apply to create the stack
terraform apply

- after the run, terraform will output the alb url, use it.


