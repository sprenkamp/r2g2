# How to run the latest version vue interface of this project

This Readme file is a tutorial to tell you how to run openai, mongodb and vue server locally, including how to install required packages and run the server on your computer. All the example code assumes you are in the main folder of our project, that is *r2g2*. If you want to change something that in *frontend* folder, you should create a new github branch.

My computer environment is *Win10* and the compiler I use is *vscode*. First create a project folder on your computer, into that folder and run below code to copy the main branch of the project.

```sh
git clone https://github.com/sprenkamp/r2g2.git
```

## Folder Structure
Make sure you are in r2g2 folder.

1. The structure of the frontend folder:

```sh
cd frontend
cd frontend/chatgpt-backend
cd frontend/mongoDb-backend
cd frontend/r2g2_vue
```
| Path and Name | Function |
| ------- | ------- |
| /chatgpt-backend | code to connect openAi and our chatbot api |
| /mongoDB-backend |code to connect mongoDB database |
| /r2g2_vue        | code to build an interface with vue3 |

2. The structure of the vue project folder:

```sh
cd frontend/r2g2_vue/src
```
| Path and Name | Function |
| ------- | ------- |
| /assets | store basic style |
| /components | store all website components |
| /data | store used data file |
| /router | store api and router |
| App.vue | the root component |
| main.js | initializing file |
| plugins.js | global functions |

## Prerequisities

For local development and testing, please install all below requirement packages on your computer with the latest version.

1. Make sure you have installed Node.js of the 16.0 or higher version. You can download the latest version from https://nodejs.org/en. To check the Node.js version, run the code below:

```sh
cd frontend
node -v
```

2. Other requirement packages. 
> **Notice: **After you install the specified package according to the following method and run our webpage, you may still be prompted that the specified package is missing. Please follow the prompts to install it with 'npm install' and then let me know.

- For the main environment(including mongodb and openai):

```sh
cd frontend
rm -rf node_modules
rm package-lock.json
npm install axios compression cors express mongodb body-parser openai dotenv
npm install
```

- For the vue3 development environment:

```sh
cd frontend/r2g2_vue
npm install @element-plus/icons-vue @vue-leaflet/vue-leaflet axios chart.js chartjs-adapter-date-fns echarts element-plus leaflet vue vue-chartjs vue-i18n vue-leaflet vue-loading-overlay vue-router dotenv
```

## Run our code in development mode
The following is a guide on how to enter the development environment of our project for development and debugging. It is divided into three steps, namely starting the openai server, database server and web page.

### Run OpenAi server

Create a *.env* file in the *chatgpt-backend* folder with the following content:
```sh
CHATGPT_TOKEN=chatgpt_token
```
Replace *chatgpt_token* with our actual ChatGPT token. You can find it in our teams group conversation history or files. (Don't forget to add '' if the token is without '')

Then run the code below to start openai server:
```sh
cd frontend/chatgpt-backend
node index.js
```

Then, the server is running on port 3000 locally: http://localhost:3000/. Try to test it through the chatbot button on our website.

### Run MongoDB server

Create a *.env* file in the *mongoDB-backend* folder with the following content:
```sh
MONGO_URL=mongodb_url
```
Replace *mongodb_url* with our actual database url. You can find it in our mongodb database website or asking JY. (Don't forget to add '' if the token is without '')

Then run the code below to start mongodb server:
```sh
cd frontend/mongoDB-backend
node connect.js
```

Then, the server is running on port 8000 locally: http://localhost:8000/. Try to test it by derictly opening the url or through our website.

### Run Vue server

Run the client in development mode:

```sh
cd frontend/r2g2_vue
npm install
npm run dev
```

Then, copy and open the link in your browser: http://localhost:5173/. Try to test it by opening the url.
