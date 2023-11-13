# pipeline
## design logic
![img.png](pipeline.png)

## stage description
| stage | logic                                                                                | output                                                                 | status |
|-------|--------------------------------------------------------------------------------------|------------------------------------------------------------------------|--------|
| 1     | Filter new coming data using 'topicUpdateDate' field. Make bert topic prediction     | add 'predicted_class' field  in the scrape.telegram collection. String | DONE   |
| 2     | check how many data don't have topic labels                                          | print the number of messages that need to topic labels                 | DONE   |
| 3.1   | Filter new coming data and judge which message should have embedding. Generate embedding | add 'embedding' field in the scrape.telegram collection. Array         | DONE   |
| 3.2   | use new topic results to update value count table                                    | overwrite 'aggregate.TelegramCount' collection                         | DONE   |
| 4     | add completion label                                                                 | add 'topicUpdateDate' field in the scrape.telegram collection. String  | DONE   |

The pipeline relies on the following fields and relevant logic.     
- predicted_class: all messages have this field. Give 'Unknown' label if the topic is unclear.    
- embedding: only messages which meet certain requirements have this field.    
- topicUpdateDate: when finish topic prediction and embedding generation, add the completion label to each message in form of 'yyyy-mm-dd'   

Don't change the logic of these fields!!! Or the pipeline has the possibility to run incorrectly. 