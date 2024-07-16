## Hello World Flask Application Deployment using AWS ECS and AWS DynamoDB

This is a simple "Hello World" application that exposes two HTTP-based APIs:

* `PUT /hello/<username>`: Saves or updates the given user's name and date of birth in the database.
* `GET /hello/<username>`: Returns a hello message for the given user, including their birthday message if it's today or in the next N days.

Architecture
------------
![Architecture](https://github.com/sagary2j/python-flask-hello-world/blob/develop/architecture-ECS-flask.drawio.png)


Requirements
------------
* Docker(local)
* Terraform
* Python 3.8+
* Flask 2.0+
* SQLite3(local)
* AWS account for deployment
* AWS DynamoDB

Deployment Architecture
------------
* Cloud Platform: AWS (Amazon Web Services)
* Github Action: CI/CD Deployment.
* AWS ECS: To run the application as a containers in EC2.
* AWS DynamoDB: Amazon DynamoDB is a fully managed proprietary NoSQL database.
* AWS S3: For storing terraform state file.
* AWS CloudWatch: For logging and monitoring.

### 1. Contents
- `./applocal.py`
  - contains a Python Flask application, which is integrated with SQLite3
- `./app.py`
  - contains a Python Flask application, which is integrated with DynamoDB the same applicaion can be used to run locally except you need to have aws dynamodb database deployed already.
- `terraform/`
  - contains the terraform code necessary to deploy the application into AWS ECS
  
### 2. How to run and test locally

1. Install dependencies: `pip install flask sqlite3 boto3`
2. Run the application: `python applocal.py`
3. Run test: `python3 -m unittest tests/test_app.py`
3. Test the APIs using `curl` or a tool like Postman

### 3. How-to Deploy into AWS ECS using github action CI/CD and Terraform for IAC
General workflow: 
1. For the very 1st time, Run the `sh setup.sh` command which will create ECR repository and build, tag and push the image into it.
2. As soon as the changes are pushed into git repository branches like main and develop it will trigger the GHA CI/CD to build and deploy into ECS using Terraform
5. Terraform will output the alb url at the end of the GHA run.

## 4. Response Examples
```
Design and code a simple "Hello World" application that exposes the following HTTP-based APIs: 

Description: Saves/updates the given user's name and date of birth in the database. 
Request: PUT /hello/<username> { "dateOfBirth": "YYYY-MM-DD" }
Response: 204 No Content
 
Note:
<usemame> must contains only letters. 
YYYY-MM-DD must be a date before the today date. 

Description: Returns hello birthday message for the given user 
Request: Get /hello/<username> 
Response: 200 OK 

Response Examples: 
A. If username's birthday is in N days: { "message": "Hello, <username>! Your birthday is in N day(s)" } 
B. If username's birthday is today: { "message": "Hello, <username>! Happy birthday!" } 

```

## 4. Destroy the cluster
1. Run the command: `terraform destroy --auto-approve=true`
2. Delete the ECR repository and s3 bucket