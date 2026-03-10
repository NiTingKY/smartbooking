<template>
  <div class="login-container">
    <h2 class="login-title">欢迎登录</h2>
    <el-form :model="form" @submit.prevent="login" class="login-form" label-position="left" label-width="80px">
      <el-form-item label="账号">
        <el-input v-model="account" placeholder="请输入账号" size="large" clearable>
          <template #prefix>
            <el-icon>
              <user />
            </el-icon>
          </template>
        </el-input>
      </el-form-item>

      <el-form-item label="密码">
        <el-input v-model="password" type="password" placeholder="请输入密码" size="large" show-password>
          <template #prefix>
            <el-icon>
              <lock />
            </el-icon>
          </template>
        </el-input>
      </el-form-item>

      <div class="button-group">
        <el-button type="primary" size="large" native-type="submit" class="login-button">
          立即登录
        </el-button>
        <el-button type="info" size="large" class="register-button" @click="showRegisterDialog = true">
          注册账号
        </el-button>
      </div>
    </el-form>
  </div>

  <el-dialog v-model="showRegisterDialog" title="用户注册" width="500px">
    <el-form :model="registerForm" label-width="80px">
      <el-form-item label="用户名">
        <el-input v-model="registerForm.name" />
      </el-form-item>
      <el-form-item label="账号">
        <el-input v-model="registerForm.account" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="registerForm.password" type="password" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="registerForm.mail" type="email" />
      </el-form-item>
      <el-form-item label="手机">
        <el-input v-model="registerForm.phone" />
      </el-form-item>
      <el-form-item label="性别">
        <el-radio-group v-model="registerForm.sex">
          <el-radio label="man" value="man">男</el-radio>
          <el-radio label="woman" value="woman">女</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="生日">
        <el-date-picker v-model="registerForm.birth" type="date" placeholder="选择日期"></el-date-picker>
      </el-form-item>
      <el-button type="primary" @click="handleRegister">提交注册</el-button>
    </el-form>
  </el-dialog>
</template>

<script>
import axios from 'axios';
import { ElMessage } from 'element-plus';
import { ref, reactive } from 'vue'; // 引入 ref
import { useRouter } from 'vue-router'; // 引入 useRouter
import Cookies from 'js-cookie';

export default {
  // 在setup()中添加注册相关状态
  setup() {
    const account = ref(''); // 定义响应式数据
    const password = ref(''); // 定义响应式数据
    const router = useRouter(); // 获取路由实例

    const login = async () => {
      try {
        // 例如：await axios.post('/api/user/login', {
        const response = await axios.post('http://127.0.0.1:5000/user/login', {
          account: account.value, // 使用响应式数据
          password: password.value // 使用响应式数据
        }, {
          withCredentials: true  // 新增配置允许携带凭证
        });

        if (response.data.status === 'success') {
          Cookies.set('user_id', response.data.user.uid);
          router.push('/index'); // 登录成功后跳转到指定页面
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        ElMessage.error('登录失败，请检查网络或服务器');
        console.error(error);
      }
    };

    const showRegisterDialog = ref(false);
    const registerForm = reactive({
      name: '',
      account: '',
      password: '',
      mail: '',
      phone: '',
      sex: '',
      birth: ''
    });

    const handleRegister = async () => {
      try {
        const response = await axios.post('http://127.0.0.1:5000/user/register',
          registerForm,
          { withCredentials: true }
        );
        console.log(response)
        if (response.data.status === 'success') {
          ElMessage.success('注册成功');
          showRegisterDialog.value = false;
          Cookies.set('user_id', response.data.user.uid);
          router.push('/index');
        }
      } catch (error) {
        ElMessage.error('注册失败');
      }
    };

    return {
      account, // 暴露给模板
      password, // 暴露给模板
      login,

      registerForm,
      showRegisterDialog,
      handleRegister
    };
  }
};
</script>

<style scoped>
.login-container {
  width: 100%;
  max-width: 420px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  margin: 100px auto;
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #2c3e50;
}

.login-form {
  :deep(.el-form-item__label) {
    font-weight: 500;
    color: #606266;
    padding-right: 12px;
  }

  :deep(.el-form-item__content) {
    flex: 1;
  }

  :deep(.el-input) {
    width: 100%;
  }
}

.button-group {
  display: flex;
  flex-direction: row;  
  gap: 20px;           
  justify-content: space-between; 
}

.login-button,
.register-button {
  flex: 1;             
  white-space: nowrap; 
}

.el-icon {
  vertical-align: -2px;
}
</style>
