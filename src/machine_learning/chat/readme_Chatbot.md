There are 2 versions of Chatbot available in this git repo.
Tumen_Chatbot_development_edition.py and Tumen_Chatbot_test_edition.
For the testing purposes of the chatbot alone through the terminal, the test version should be used.
The test version can be run through the VS code using an interactive window by running the code directly.
The user should have 3 local environments of ATLAS_TOKEN, ATLAS_USER and OPENAI_API_KEY

For the development version, user should download the file on the device and run it using uvicorn.
uvicorn Tumen_Chatbot_development_edition:app --reload
Than the user should go to the http://127.0.0.1:8000/docs

We are thinking of using docker to make all of the APIs to work together

## Definition for chat bot API
|   parameter   |  type  | if user don't specify |                  description & example                  |  
|:-------------:|:------:|:---------------------:|:-------------------------------------------------------:|
|  start_date   | string |        'null'         |                    e.g. '2022-01-18'                    |  
|   end_date    | string |        'null'         |                    e.g.'2022-03-18'                     |  
|    country    | string |        'null'         |                   e.g. 'Switzerland'                    |   
|     state     | string |        'null'         |                      e.g. 'Zurich'                      |   
|     query     | string |        'null'         | current query. e.g. 'Can I get free clothes in Zurich?' |   
| query_history | array  |          []           |             conatins all historical query.              |   

if users do not select start_date/end_date/country/state, use 'null' as parameters to call API 
