# A Scalable Spaced Repetition Vocabulary Learning App - Don't Remember
This is a spaced repetitive English vocabulary learning app coded by Flask and Postgres with a microservice architecture. The application is designed to provide users with a personalized and efficient learning experience, allowing them to track their progress, set personal goals, and collaborate with teams.


## Features
- User Signup/Login/Logout
- Review Word Card
- Planning Learning Aim
- Make a learning group with other users
- A CLI tool is provided for demo purposes.



## Tech Stack

- Backend: Python, Flask, Gunicorn, Docker
- Frontend: Python
- Database: Postgres
- Deployment: AWS ECS, AWS SQS, AWS Lambda
- Infrastructure Management: Terraform


## Architecture
<img src="/model/dont-remember-system-landscape-architecture.png" width="600" alt="System Landscape">
<img src="/model/dont-remember-software-system-architecture.png" width="400" alt="Software System Architecture"><br>

## Deployment
Getting Started
This app is optimized for AWS platform. To deploy the app, use the following commands:
```
terraform apply -var-file="secret.tfvars" -auto-approve
terraform apply -var-file="secret.tfvars" -auto-approve -parallelism=20
```
## Documentation
For detailed technical information, please refer to the report.

