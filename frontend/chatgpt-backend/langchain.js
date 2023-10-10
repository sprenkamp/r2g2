const express = require('express');
const compression = require('compression');
const { MongoClient } = require('mongodb');
const { MongoDBAtlasVectorSearch } = require('langchain/vectorstores/mongodb_atlas');
const { OpenAIEmbeddings } = require('langchain/embeddings/openai');
const { Configuration, OpenAIApi} = require("openai");
const {PromptTemplate} = require('langchain/prompts');
const {ChatOpenAI} = require('langchain/chat_models/openai');
const {ConversationalRetrievalQAChain} = require('langchain/chains');
const {BufferMemory} = require('langchain/memory')
const cors = require('cors');
const dotenv = require("dotenv");


const app = express();
dotenv.config()
app.use(express.json());
app.use(cors());
app.use(compression());

app.post('/chatbot', async (req, res) => {
    let client;
    try {
        // MongoDB
        const uri = process.env.MONGO_URL;
        const client = new MongoClient(uri);
        await client.connect();
        console.log('Connected to MongoDB');

        const namespace = 'scrape.telegram';
        const [dbName, colName] = namespace.split('.');
        const collection = client.db(dbName).collection(colName);

        const api_key = process.env.CHATGPT_TOKEN;
        const embeddings = new OpenAIEmbeddings({openAIApiKey:api_key});
        const vectorStore = new MongoDBAtlasVectorSearch(embeddings, {
            collection,
            embeddingKey: "embedding",
            indexName: "telegram_embedding",
            textKey: "messageText",
            }
        );

        // open ai api
        // const configuration = new Configuration({
        //     apiKey: api_key,
        // });
        // const openai = new OpenAIApi(configuration);

        const llm = new ChatOpenAI({ temperature: 0.2, model_name: 'gpt-3.5-turbo', openAIApiKey: api_key });
        const retriever = await vectorStore.asRetriever({
            searchType: "mmr",
            searchKwargs: {
            fetchK: 100,
            lambda: 0.5,
            },
        });

        const prompt_template = `Use the following pieces of context to answer the question at the end. 
        Combine the information from the context with your own general knowledge to provide a comprehensive and accurate answer. 
        Please be as specific as possible, also you are a friendly chatbot who is always polite.
        {content}
        Question: {question}`;
        const question = req.body.message;
        const retrieverOutput = await retriever.getRelevantDocuments(question);
        console.log(retrieverOutput)
        const documents = retrieverOutput.map((doc) => doc.pageContent);
        const content = documents.join('\n');
        const prompt = prompt_template.replace('{content}', content).replace('{question}', question);
        console.log(prompt)
        const chain = ConversationalRetrievalQAChain.fromLLM(
            llm,
            retriever,
            {   
                memory: new BufferMemory({
                    memoryKey: "chat_history",
                    returnMessages: true, // If using with a chat model
                }),
                questionGeneratorChainOptions: {
                    template: prompt
                },
            }
        );
        // const question = req.body.message;
        const answer = await chain.call({question});
        console.log(answer);
        return res.json({answer})

        // const userQuestion = req.body.message.toString();
        // const retrieverOutput = await retriever.getRelevantDocuments(userQuestion);
        // const documents = retrieverOutput.map((doc) => doc.pageContent);
        // const context = documents.join('\n');
        // // const prompt = prompt_template.replace('{context}', context).replace('{question}', userQuestion);
        // const prompt = new PromptTemplate({
        //     inputVariables: [context, userQuestion],
        //     template: prompt_template,
        // });
        // pass to chat
        // const response = await openai.createChatCompletion({
        //     model: "text-davinci-003", //text-davinci-003 gpt-3.5-turbo
        //     prompt,
        //     temperature: 0.2,
        //     max_tokens: 500,
        //   });
        //   console.log(response)
        //   const completion = response.data.choices[0].text;
        //   return res.status(200).json({
        //     completion,
        //   });

        } catch (error) {
            console.error('Error:', error);
            res.status(500).json({ error: 'Internal server error' });
        } finally {
            if (client) {
                await client.close();
                console.log('MongoDB connection closed');
            }
        }
    }
);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});

