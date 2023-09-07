# r2g2

## Database (MongoDB)

|     database.collection      |       data description       |                                          columns                                           |                data volume                 |
|:----------------------------:|:----------------------------:|:------------------------------------------------------------------------------------------:|:------------------------------------------:|
|       scrape.telegram        |  message information  | chat, channel_id, messageDatetime, country, state, city, messageText, views, forwards, replies, reactions | 2,303,765 (Switzerland+Germany) 2023.09.07 |
|scrape.telegramChatsWithState| chats with country and state |country, state, city, chat|61|
|test.bertopic| Topic aggregation. Granularity: by date, country, state, topic. (sample data, only for testing) |date, country, state, cluster, count, update_time|14|

## Pipeline Design

## Architecture
