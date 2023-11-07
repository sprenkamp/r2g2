<!-- ChatBot.vue -->

<template>
  <div class="container">
      <h1>
        <Icon icon="carbon:chat-bot" height="48"/>
        Chat Bot
        <!-- <el-button class="askButton" @click="clearChatHistory">Clean</el-button> -->
      </h1>
      <div class="messageBox mt-8">
        <template v-for="(message, index) in messages" :key="index">
            <div :class="message.from == 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
                <div :class="message.from == 'user' ? 'userMessageWrapper' : 'chatGptMessageWrapper'">
                    <div :class="message.from == 'user' ? 'userMessageContent' : 'chatGptMessageContent'">{{ message.data }}</div>
                </div>
            </div>
        </template>
        <div class="buttonContainer">
          <div class="buttonRow"> 
            <el-button type="primary" :icon="Apple" plain class="chatButton" @click="sendQuestion('question template 1')">Question 1</el-button>
            <el-button type="primary" :icon="Pear" plain class="chatButton" @click="sendQuestion('question template 2')">Question 2</el-button>
          </div>
          <div class="buttonRow"> 
            <el-button type="primary" :icon="Watermelon" plain class="chatButton" @click="sendQuestion('question template 3')">Question 3</el-button>
            <el-button type="primary" :icon="Lollipop" plain class="chatButton" @click="sendQuestion('question template 4')">Question 4</el-button>
          </div>
        </div>
      </div>
      <div class="inputContainer">
        <el-autocomplete
          v-model="currentMessage"
          :fetch-suggestions="querySearch"
          clearable
          placeholder="Ask me about the data"
          @select="handleSelect"
        >
          <template #append>
            <el-button
                @click="sendMessage(currentMessage)"
                class="askButton"
            >
              <Icon icon="ion:send" />
            </el-button>
          </template>
        </el-autocomplete>
      </div>
  </div>
</template>

<script setup lang="ts">
import {ref, defineProps} from 'vue'
import axios from 'axios';
import { Apple, Watermelon, Pear, Lollipop, Search} from '@element-plus/icons-vue'
import { Icon } from '@iconify/vue';

interface Message {
  from: string;
  data: string;
}

const currentMessage = ref('');
const messages = ref<Message[]>([]);
const questions = ref<{ value: string }[]>([]);
const select = ref('')
const answer = ref<string>('');
const props = {
  expandTrigger: 'hover' as const,
}
const prop = defineProps({
  selectedNews: [String, Array],
  selectedState: String,
  minDate: String,
  maxDate: String,
})
// const sendMessage = async (message: string) => {
//   messages.value.push({
//     from: 'user',
//     data: message,
//   });
//   try {
//     const response = await axios.post('http://localhost:3000/chatbot', {
//       message: message,
//     });
//     messages.value.push({
//       from: 'chatGpt',
//       data: response.data,
//     });
//     } catch (error) {
//       console.error(error);
//     }
// };

// code for chat_fastapi_app.py
const sendMessage = async (message: string) => {
  messages.value.push({
    from: 'user',
    data: message,
  });
  const requestBody = {
      start_date: prop.minDate !== "" ? prop.minDate : "null",
      end_date: prop.maxDate !== "" ? prop.maxDate : "null",
      country: "Switzerland",
      state: prop.selectedState !== "" ? prop.selectedState : "null",
      predicted_class: Array.isArray(prop.selectedNews) ? "null" : (prop.selectedNews !== "" ? prop.selectedNews : "null"),
      query: message,
      chat_history: [],
  };
  // const requestBody = {
  //   start_date: "2022-01-01",
  //   end_date: "2022-01-02",
  //   country: "Switzerland",
  //   state: "Zurich",
  //   predicted_class: "Education",
  //   query: "What are the biggest needs of refugees within the education sector?",
  //   chat_history: []
  // };
  try {
    console.log('requestBody:', requestBody);
    // const response = await axios.post('http://13.53.123.229:8080/query', requestBody);
    const response = await axios.post('https://bot.governmentasaplatform.ch/query', requestBody);
    messages.value.push({
      from: 'chatGpt',
      data: response.data[0],
    });
  } catch (error) {
    console.error(error);
  }
};


// // code for langchain.js
// const sendMessage = async (message: string) => {
//   messages.value.push({
//     from: 'user',
//     data: message,
//   });
//   try {
//     const response = await axios.post('http://localhost:3000/chatbot', {
//       message: message,
//     });
//     messages.value.push({
//       from: 'chatGpt',
//       data: response.data.answer.text,
//     });
//   } catch (error) {
//     console.error(error);
//   }
// };

const clearChatHistory = () => {
  messages.value.splice(0, messages.value.length);
};

const querySearch = (queryString) => {
  const results = queryString ? questions.value.filter(createFilter(queryString)) : questions.value;
  return results;
};

const handleSelect = (item) => {
  console.log(item);
};

const createFilter = (queryString) => {
  return (questions) =>
  questions.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
};

const sendQuestion = (question) => {
  currentMessage.value = question;
  sendMessage(question);
};

questions.value = [
{ value: 'hello, how are you?' },
{ value: 'Can I find a job in Switzerland as a nurse?' },
{ value: 'Who is the president of USA?' },
// { value: 'question template 2' },
// { value: 'question template 3' },
// { value: 'question template 4' },
// ... other data items ...
];

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.container {
  width: auto;
  height: 500px;
  border-radius: 8px;
  border-color: #ffffff;
  box-shadow: 0 0 40px rgb(125, 125, 125);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
  border-radius: 18px;
  position: flex;
  bottom: 10px;
  right: 10px;
  flex-grow: 1;
  background-color: transparent;
  backdrop-filter: blur(5px);
}

h1 {
  font-size: 28px;
  font-weight: 500;
  text-align: center;
  color: #ffffff;
  padding: 16px;
  margin: 0;
  background-color: #a0cfff;
  border-bottom: 1px solid #e7e7e7;
}
.messageBox {
  padding: 10px;
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.messageFromUser,
.messageFromChatGpt {
  display: flex; 
}
.messageBox {
  max-height: 1000px;
  overflow-y: auto;
  padding: 0 16px;
  border-top: 1px solid #1d1d1d;
  border-bottom: 1px solid #ffffff;
  flex-grow: 1;
}
.messageFromUser,
.messageFromChatGpt {
  display: flex;
  margin-bottom: 8px;
}
.userMessageWrapper,
.userMessageWrapper {
  align-self: flex-end;
  display: flex;
  margin-right: 20%;
}
.chatGptMessageWrapper {
  align-self: flex-start;
  display: flex;
  margin-left: 20%; 
  flex-direction: column;
}
.userMessageContent,
.chatGptMessageContent {
  padding: 8px 12px;
  border-radius: 18px;
  margin-bottom: 2px;
  font-size: 15px;
  line-height: 1.2;
}
.userMessageContent {
  background-color: #409EFF;
  color: white;
  border-top-left-radius: 0;
}
.chatGptMessageContent {
  background-color: #e3e3e3;
  color: #000000;
  border-top-right-radius: 0;
}
.chatGptMessageTimestamp {
  font-size: 10px;
  color: #999;
  margin-top: 2px;
  align-self: flex-start;
}

.userMessageTimestamp {
  align-self: flex-end;
}
.inputContainer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 8px;
}
.el-autocomplete {
  flex-grow: 1;
  border: none;
  outline: none;
  padding: 12px;
  font-size: 18px;
  background-color: rgb(255, 255, 255);
  border-radius: 24px;
  margin-right: auto;
}
/* .askButton {
background-color: #a0cfff;
color: rgb(255, 255, 255);
font-size: 16px;
padding: 8px 16px;
border: none;
outline: none;
cursor: pointer;
border-radius: 20px;
transition: background-color 0.3s ease-in-out;
margin-left: 20px;
}
.askButton:hover {
background-color: #ffffff;
} */
@media (max-width: 480px) {
.container {
  width: 100%;
  max-width: none;
  border-radius: 0;
}
}
.messageBox {
  padding: 16px;
  flex-grow: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.messageFromUser,
.messageFromChatGpt {
  display: flex;
}
.buttonContainer {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px;
  margin-top: auto;
}
.buttonRow {
  display: flex;
  justify-content: center;
  margin-bottom: 8px;
}

</style>
