# GAAP(Government as a Platform) Deployment
Welcome to the frontend code folder of the R2G2 platform. This README file will guide you on how to access our platform and how to deploy our frontend and backend services.

## Table of Contents

- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Frontend Deployment](#frontend-deployment)
- [Backend Deployment](#backend-deployment)

## Project Overview

Our project is a web application to mitigate the Ukrainian refugee crisis based on traditional and social media data. This readme fule will guide you deeply into our project, including overview, how we deploy our services and how to use this website. This project is a project with separate front-end and back-end, and we will perform some integration operations. 
If you want to run the project locally for development or testing purposes, please refer to the [Local Development Guide](README_local_develop.md) for detailed instructions.

- Frontend: Hosted on Netlify (a web deployment service platform). You can visit our website of the platform by [https://governmentasaplatform.ch](https://governmentasaplatform.ch)
- Backend: Including two parts(MongoDB database and ChatBot), we deployed both these two services on AWS EC2 instance

## Prerequisites

For successful deployment, you need these prerequisites.

- Netlify account and a single repositories to contain only frontend part code. You can visit our single repo [here](https://github.com/sprenkamp/r2g2_vue). (for frontend deployment)
- Unused domain and a certificate for the domain.
- AWS account. (for backend deployment)

## Frontend Deployment

Our front-end is deployed on netlify, a platform that provides free website hosting services and is very simple to operate.
As a website developer, if you want to modify the content or deploy it, you only need to complete the modification locally and submit it, and the platform will automatically redeploy it, which is very convenient.

## Backend Deployment

Compared to front-end deployment, back-end deployment requires more steps because our goal is to generate secure APIs that can be accessed by the front-end.

To deploy the backend on AWS, follow these steps:

1. Create two AWS EC2 instances, one is for database, one is for chatbot. Remember to store **keys** in your computer and give enough permission.
2. Setup environment for both instances. Here we chose to upload **file codes**, **requirment.txt** and the **.env** of each service rather than the whole repository. To upload files into instances, open terminal and use the code below:

```sh
scp -i /path/to/your-key.pem /path/to/connect.js ec2-user@example.com:/home/username/
```
where
- /path/to/your-key.pem: The path to the EC2 instance key file.
- /path/to/connect.js: The path to the local file you want to transfer.
- ec2-user@example.com: The public IPv4 DNS of the EC2 instance.
- /home/username/: The path to the target directory on the EC2 instance. Usually, /home/ec2-user/

3. Connect to the instance and do some configuration.

- Instance MongoDB
```sh
sudo yum update -y
sudo yum install -y nodejs npm
npm install mongodb express compression dotenv cors
npm install
sudo npm install -g pm2
pm2 start connect.js
pm2 startup
sudo env PATH=$PATH:/usr/bin /usr/local/lib/node_modules/pm2/bin/pm2 startup systemd -u ec2-user --hp /home/ec2-user
```
After the above operations, the database program will run on this instance and run automatically when the instance is restarted to prevent our platform from crashing.

- Instance chatbot
```sh
sudo yum install python3-pip
pip3 install -r requirements.txt
sudo nano /etc/systemd/system/myapp.service
sudo systemctl enable myapp.service
sudo systemctl start myapp.service
```