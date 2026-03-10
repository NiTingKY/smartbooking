<template>
  <div class="common-layout">
    <el-container class="dashboard-container">


      <el-container class="main-content-area">

        <el-main class="dashboard-main">
          <div v-if="activeMenu === 'ai-assistant'" class="ai-assistant-content">
            <div class="chat-container">
              <div class="history-toggle">
                <el-button type="primary" @click="toggleHistory">查看历史对话</el-button>
    
                <el-select v-model="selectedTask" placeholder="选择任务" style="margin-left: 10px" v-if="showHistory">
                  <el-option label="分析" value="analyze"></el-option>
                  <el-option label="总结" value="summarize"></el-option>
                </el-select>
              </div>
              <div v-if="showHistory" class="historical-messages">
                <div v-for="(msg, index) in historicalMessages" :key="index"
                  :class="['message-bubble', msg.role, { 'selected': selectedMessages.includes(index) }]">
                  <el-checkbox v-model="selectedMessages" :label="index" class="message-checkbox"></el-checkbox>
                  <el-avatar v-if="msg.role === 'assistant'" :src="geminiLogo" class="avatar"></el-avatar>
                  <div class="message-content-wrapper">
                    <div class="content" v-html="msg.content || 'No content'"></div>
                    <div class="timestamp">{{ formatTimestamp(msg.create_time) }}</div>
                  </div>
                  <el-avatar v-if="msg.role === 'user'" :src="userAvatar" class="avatar"></el-avatar>
                </div>
              </div>
              <div class="messages" v-else>
                <div v-for="(msg, index) in messages" :key="index" :class="['message-bubble', msg.role]">
                  <el-avatar v-if="msg.role === 'assistant'" :src="geminiLogo" class="avatar"></el-avatar>
                  <div class="message-content-wrapper">
                    <div class="content" v-html="msg.content"></div>
                    <div class="timestamp">{{ formatTimestamp(msg.timestamp) }}</div>
                  </div>
                  <el-avatar v-if="msg.role === 'user'" :src="userAvatar" class="avatar"></el-avatar>
                </div>
                <div v-if="isLoading" class="message-bubble assistant loading">
                  <el-avatar :src="geminiLogo" class="avatar"></el-avatar>
                  <div class="message-content-wrapper">
                    <div class="content">加载中...</div>
                  </div>
                </div>
              </div>

              <div class="chat-input-area">
                <el-upload class="upload-button" action="#" :show-file-list="false" :on-change="handleFileChange"
                  :auto-upload="false" :limit="1" accept=".jpg,.jpeg,.png">
                  <el-button type="primary" :icon="Picture" circle />
                </el-upload>

                <el-input v-model="inputMessage" placeholder="请输入消息..." class="chat-input-new"
                  @keyup.enter="sendMessage" rows="1" type="textarea" :autosize="{ minRows: 1, maxRows: 4 }"></el-input>
                <el-button type="primary" class="send-button-new" @click="sendMessage">
                  <el-icon>
                    <Promotion />
                  </el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */
import {
  HomeFilled,
  Document,
  MagicStick,
  Promotion,
  Picture
} from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import axios from 'axios';
import logo from '../assets/logo.png';
import geminiLogo from '../assets/aislogo.png';
import userAvatar from '../assets/photo.png';
import Cookies from 'js-cookie';

export default {
  name: 'AppDashboard',
  components: {
    HomeFilled,
    Document,
    MagicStick,
    Promotion,
    Picture,
  },
  data() {
    return {
      activeMenu: 'ai-assistant',
      logoUrl: logo,
      geminiLogo: geminiLogo,
      userAvatar: userAvatar,
      inputMessage: '',
      selectedFile: null,
      messages: [
        { role: 'assistant', content: '你好！我是你的智能记账助手，请告诉我你的收支情况或任何问题。', timestamp: new Date().toISOString() },
      ],
      billsData: [
        {
          date: '2025-05-10',
          type: '支出',
          category: '餐饮',
          amount: 50.0,
          detail: '午餐',
        },
        {
          date: '2025-05-09',
          type: '收入',
          category: '工资',
          amount: 5000.0,
          detail: '月工资',
        },
      ],
      overviewData: {
        income: 12000.00,
        expense: 8500.00,
        balance: 3500.00
      },
      userName: localStorage.getItem('userName') || '管理员',
      showHistory: false,
      historicalMessages: [],
      selectedTask: 'summarize', // Default to summarize
      selectedMessages: [], // Array to store indices of selected messages
      isLoading: false
    };
  },

  created(){
      this.user_id = Cookies.get('user_id');
      console.log('aaa',this.user_id);
    },

  methods: {
    created(){
      this.user_id = Cookies.get('user_id');
      console.log('aaa',this.user_id);
    },


    handleMenuSelect(key) {
      this.activeMenu = key;
    },
    deleteRow(index) {
      this.billsData.splice(index, 1);
    },
    handleFileChange(file) {
      this.selectedFile = file.raw;
      ElMessage.warning('当前 AI 不支持图片上传，功能开发中！');
    },
    formatTimestamp(timestamp) {
      if (!timestamp) return '';
      const date = new Date(timestamp);
      return date.toLocaleString('zh-CN', { hour12: false });
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) {
        ElMessage.warning('请输入消息。');
        return;
      }

      const userMessage = {
        role: 'user',
        content: this.inputMessage.trim(),
        timestamp: new Date().toISOString()
      };
      this.messages.push(userMessage);
      this.isLoading = true;

      try {
        const response = await axios.post('http://localhost:5000/api/ai/chat', {
          messages: this.messages
        }, {
          withCredentials: true,
        });

        if (response.data.status === 'success') {
          let aiResponse = response.data.data.reply;
          aiResponse = aiResponse.replace(/^\n+|\n+$/g, '').replace(/\n+/g, '\n');
          this.messages.push({
            role: 'assistant',
            content: aiResponse,
            timestamp: response.data.data.timestamp
          });
          ElMessage.success('AI 回复成功');
        } else {
          ElMessage.error(`AI 请求失败: ${response.data.message}`);
          this.messages.push({
            role: 'assistant',
            content: `错误: ${response.data.message}`,
            timestamp: new Date().toISOString()
          });
        }
      } catch (error) {
        ElMessage.error(`发送消息失败: ${error.message}`);
        this.messages.push({
          role: 'assistant',
          content: `错误: ${error.message}`,
          timestamp: new Date().toISOString()
        });
      } finally {
        this.isLoading = false;
      }

      this.inputMessage = '';
      this.selectedFile = null;

      this.$nextTick(() => {
        const messagesContainer = this.$el.querySelector('.messages');
        if (messagesContainer) {
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
      });
    },
    toggleHistory() {
      if (!this.showHistory) {
        this.fetchHistory();
      }
      this.showHistory = !this.showHistory;
      // Reset selected messages when toggling history view
      this.selectedMessages = [];
    },
    async fetchHistory() {
      try {
        const response = await axios.get('http://localhost:5000/api/ai/chat/history', {
          withCredentials: true,
          params: { 'user_id': this.user_id }
        });
        if (response.data.status === 'success') {
          this.historicalMessages = response.data.data;
        } else {
          ElMessage.error(`加载历史记录失败: ${response.data.message}`);
        }
      } catch (error) {
        ElMessage.error(`获取历史记录失败: ${error.message}`);
      }
    },
    async processHistory() {
      if (!this.showHistory || !this.historicalMessages.length) {
        ElMessage.warning('请先加载历史记录');
        return;
      }
      if (this.selectedMessages.length === 0) {
        ElMessage.warning('请至少选择一条历史记录');
        return;
      }
      this.isLoading = true;
      try {
        // Prepare selected messages
        const selectedMessagesData = this.selectedMessages.map(index => ({
          role: this.historicalMessages[index].role,
          content: this.historicalMessages[index].content
        }));
        console.log('Sending messages to process:', selectedMessagesData);
        const response = await axios.post('http://localhost:5000/api/ai/process_history', {
          'user_id': this.user_id ,
          task: this.selectedTask,
          messages: selectedMessagesData
        }, {
          withCredentials: true,
        });
        if (response.data.status === 'success') {
          this.messages.push({
            role: 'assistant',
            content: response.data.data.reply,
            timestamp: response.data.data.timestamp
          });
          ElMessage.success('历史记录处理成功');
          // Reset selection after processing
          this.selectedMessages = [];
        } else {
          ElMessage.error(`处理失败: ${response.data.message}`);
        }
      } catch (error) {
        console.error('Error in processHistory:', error);
        ElMessage.error(`发送处理请求失败: ${error.message}`);
      } finally {
        this.isLoading = false;
      }
      this.$nextTick(() => {
        const messagesContainer = this.$el.querySelector('.messages');
        if (messagesContainer) {
          messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
      });
    }
  },
  mounted() {
    this.userName = localStorage.getItem('userName') || '管理员';
  }
};
</script>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
}

.dashboard-container {
  width: 100%;
  display: flex;
}


.el-menu-item:hover {
  background-color: #f0f0f0 !important;
}

.main-content-area {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.dashboard-header {
  background-color: #f7f9fc;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e0e0e0;
  height: 60px;
}

.header-left h2 {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  margin-right: 20px;
  font-size: 16px;
  color: #555;
}

.dashboard-main {
  flex-grow: 1;
  padding: 20px;
  background-color: #f0f2f5;
  overflow-y: auto;
}

.overview-content {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.box-card {
  margin-bottom: 20px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.card-value {
  font-size: 28px;
  font-weight: bold;
  color: #409eff;
  margin: 10px 0 0;
}


.bills-content {
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.ai-assistant-content {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.chat-container {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  padding: 20px;
  height: 100%
}

.history-toggle {
  margin-bottom: 10px;
}

.historical-messages {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-bottom: 10px;
  min-height: 0;
}

.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 10px;
  margin-bottom: 10px;
  min-height: 0
}

.message-bubble {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}

.message-bubble.user {
  justify-content: flex-end;
  margin-right: auto;
}

.message-bubble.assistant {
  justify-content: flex-start;
  margin-left: auto;
  flex-direction: row;  /* 确保从左到右排列 */
}

.message-bubble .avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  flex-shrink: 0;
}

.message-bubble.user .avatar {
  margin-left: 10px;
  order: 2;
}

.message-bubble.assistant .avatar {
  margin-right: 10px;
  order: 1;
}

.message-bubble .message-content-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 70%;
  flex-grow: 0;
  flex-shrink: 1;
  order: 2;
}

.message-bubble .content {
  padding: 12px 18px;
  border-radius: 18px;
  font-size: 15px;
  line-height: 1.5;
  word-wrap: break-word;
  white-space: pre-wrap;
}

.message-bubble.user .content {
  background-color: #409EFF;
  color: #ffffff;
  border-bottom-right-radius: 4px;
}

.message-bubble.assistant .content {
  background-color: #e0e0e0;
  color: #303133;
  border-bottom-left-radius: 4px;
}

.message-bubble .timestamp {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  width: fit-content;
  align-self: flex-start;
}

.message-bubble.user .timestamp {
  align-self: flex-end;
}

.message-bubble.loading .content {
  background-color: #f0f0f0;
  color: #666;
  animation: pulse 1.5s infinite;
}

.message-bubble.selected {
  background-color: #e6f7ff;
}

.message-checkbox {
  margin-right: 10px;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }

  50% {
    opacity: 1;
  }

  100% {
    opacity: 0.6;
  }
}

.chat-input-area {
  display: flex;
  align-items: center;
  padding: 10px 0;
  border-top: 1px solid #e0e0e0;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.05);
  margin-top: auto;
}

.chat-input-new {
  flex-grow: 1;
  margin: 0 10px;
}

.chat-input-new .el-textarea__inner {
  resize: none;
  border-radius: 20px;
  padding: 10px 15px;
  min-height: 44px !important;
  font-size: 15px;
  border-color: #dcdfe6;
}

.chat-input-new .el-input__inner::placeholder {
  color: var(--input-placeholder) !important;
}

.chat-input-new .el-input__wrapper.is-focus {
  border-color: var(--gemini-primary) !important;
  box-shadow: 0 0 0 2px rgba(66, 133, 244, 0.2) !important;
}

.send-button-new {
  border-radius: 50% !important;
  width: 44px;
  height: 44px;
  padding: 0 !important;
  background-color: var(--gemini-primary) !important;
  border-color: var(--gemini-primary) !important;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  margin-right: 10px;
}

.send-button-new:hover {
  background-color: #3b7af0 !important;
  border-color: #3b7af0 !important;
}

.send-button-new[disabled] {
  background-color: #5a5a5a !important;
  border-color: #5a5a5a !important;
}

.upload-button {
  margin-left: 10px;
}

.upload-button .el-button {
  border-radius: 50% !important;
  width: 44px;
  height: 44px;
  padding: 0 !important;
  background-color: #909399 !important;
  border-color: #909399 !important;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.upload-button .el-button:hover {
  background-color: #a6a9ad !important;
  border-color: #a6a9ad !important;
}
</style>