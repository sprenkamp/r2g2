<!-- ChatBot.vue -->

<template>
    <div class="chatbox-container">
        <div class="container">
            <h1>
              Ai Chat Bot
            </h1>
            <div class="messageBox mt-8">
                <template v-for="(message, index) in messages" :key="index">
                    <div :class="message.from == 'user' ? 'messageFromUser' : 'messageFromChatGpt'">
                        <div :class="message.from == 'user' ? 'userMessageWrapper' : 'chatGptMessageWrapper'">
                            <div :class="message.from == 'user' ? 'userMessageContent' : 'chatGptMessageContent'">{{ message.data }}</div>
                        </div>
                    </div>
                </template>
            </div>
            <div class="inputContainer">
                <el-autocomplete
                  v-model="currentMessage"
                  :fetch-suggestions="querySearch"
                  clearable
                  placeholder="Ask me about the data"
                  @select="handleSelect"
                />
                <button
                    @click="sendMessage(currentMessage)"
                    class="askButton"
                >
                    Ask
                </button>
                <button class="askButton" @click="clearChatHistory">Clean</button>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatBox',
  data() {
    return {
      currentMessage: '',
      messages: [],
      tempHistory: [], // Temporary history storage
      tempHistoryIndex: 0,
      questions:[],
    };
  },
  methods: {
    async sendMessage(message) {
      this.messages.push({
        from: 'user',
        data: message,
      });
      await axios
        .post('http://localhost:3000/chatbot', {
          message: message,
        })
       .then((response) => {
        this.messages.push({
            from: 'chatGpt',
            data: response.data.data, // Access the 'data' property of the response object
        });
        });
    },
    async clearChatHistory() {
      this.messages = [];
    },
    async querySearch(queryString, cb) {
      const results = queryString ? this.questions.filter(this.createFilter(queryString)) : this.questions
      cb(results)
    },
    handleSelect(item) {
      console.log(item)
    },
    createFilter(queryString) {
      return (questions) =>
        questions.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0;
    },
  },
  async mounted() {
    this.questions = [
      { value: 'hello'},
      { value: 'sample'},
      { value: 'question template 1'},
      { value: 'question template 2'},
      { value: 'question template 3'},
      { value: 'question template 4'},
      // ... other data items ...
    ];
  },
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500&display=swap');

.chatbox-container {
  position: flex;
  bottom: 10px;
  right: 10px;
  z-index: 1000;
}
.container {
  width: 550px;
  height: 1000px;
  background-color: rgb(176, 246, 146);
  border-radius: 8px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  font-family: 'Roboto', sans-serif;
  border-radius: 18px;
}
h1 {
  font-size: 28px;
  font-weight: 500;
  text-align: center;
  color: #222;
  padding: 16px;
  margin: 0;
  background-color: #7bef5e;
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
  display: flex; }
.messageBox {
  max-height: 1000px;
  overflow-y: auto;
  padding: 0 16px;
  border-top: 1px solid #4afe5f;
  border-bottom: 1px solid #42ff25;
  flex-grow: 1;
}
.messageFromUser,
.messageFromChatGpt {
  display: flex;
  margin-bottom: 8px;
}
.userMessageWrapper,
.chatGptMessageWrapper {
  display: flex;
  flex-direction: column;
}
.userMessageWrapper {
  align-self: flex-end;
}

.chatGptMessageWrapper {
  align-self: flex-start;
}
.userMessageContent,
.chatGptMessageContent {
  max-width: 60%;
  padding: 8px 12px;
  border-radius: 18px;
  margin-bottom: 2px;
  font-size: 20px;
  line-height: 1.4;
}
.userMessageContent {
  background-color: #1877F2;
  color: white;
  border-top-left-radius: 0;
}
.chatGptMessageContent {
  background-color: #EDEDED;
  color: #222;
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
  background-color: #7bef5e;
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
.askButton {
  background-color: #1877F2;
  color: white;
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
  background-color: #145CB3;
}
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
</style>
