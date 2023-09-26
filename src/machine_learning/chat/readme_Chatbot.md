There are 2 versions of Chatbot available in this git repo.
Tumen_Chatbot_development_edition.py and Tumen_Chatbot_test_edition.
For the testing purposes of the chatbot alone through the terminal, the test version should be used.
The test version can be run through the VS code using an interactive window by running the code directly.
The user should have 3 local environments of ATLAS_TOKEN, ATLAS_USER and OPENAI_API_KEY

For the development version, user should download the file on the device and run it using uvicorn.
uvicorn Tumen_Chatbot_development_edition:app --reload
Than the user should go to the http://127.0.0.1:8000/docs

We are thinking of using docker to make all of the APIs to work together