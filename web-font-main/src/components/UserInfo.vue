<template>
  <div class="user-info">
    <el-card v-if="!loading && userInfo" class="info-card">
      <template #header>
        <div class="card-header">
          <h2>用户详细信息</h2>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="24">
          <div class="info-item">
            <span class="label">用户ID：</span>
            <span class="value">{{ userInfo.uid }}</span>
          </div>
          <div class="info-item">
            <span class="label">姓名：</span>
            <span class="value">{{ userInfo.name }}</span>
          </div>
          <div class="info-item">
            <span class="label">性别：</span>
            <span class="value">{{ userInfo.sex || '未设置' }}</span>
          </div>
          <div class="info-item">
            <span class="label">邮箱：</span>
            <span class="value">{{ userInfo.mail }}</span>
          </div>
          <div class="info-item">
            <span class="label">手机：</span>
            <span class="value">{{ userInfo.phone }}</span>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-skeleton v-if="loading" :rows="5" animated />
    <el-alert v-if="error" :title="error" type="error" show-icon />
  </div>
</template>

<script>
import Cookies from 'js-cookie';
import axios from 'axios';

export default {
    name: 'UserInfo',
    data() {
        return {
            userId: null,    // 用于存储用户ID
            userInfo: null,  // 用于存储用户信息
            loading: true,   // 用于显示加载状态
            error: null      // 用于存储错误信息
        };
    },
    created() {
        this.userId = Cookies.get('user_id');
        // 添加用户信息获取逻辑
        if (this.userId) {
            this.fetchUserInfo();
        } else {
            console.error('未找到用户ID');
            this.$router.push('/');
        }
        console.log(this.userInfo)  // 检查用户ID是否正确获取
    },
    methods: {
        async fetchUserInfo() {
            try {
                this.loading = true;
                const response = await axios.get(`http://127.0.0.1:5000/user/info/${this.userId}`, {
                    withCredentials: true
                });
                
                if (response.data.status === 'success') {
                    this.userInfo = { 
                        uid: response.data.result.uid,
                        name: response.data.result.name,
                        phone: response.data.result.phone,
                        mail: response.data.result.mail,
                        sex: response.data.result.sex
                    };
                }
            } catch (error) {
                console.error('获取用户信息失败:', error);
                this.error = '用户信息加载失败';
            } finally {
                this.loading = false;
            }
        }
    }
}

</script>

<style scoped>
.info-card {
  margin: 20px;
  max-width: 800px;
}

.card-header h2 {
  margin: 0;
  color: #409EFF;
}

.info-item {
  margin: 15px 0;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.label {
  font-weight: bold;
  color: #606266;
  margin-right: 10px;
}

.value {
  color: #303133;
}
</style>