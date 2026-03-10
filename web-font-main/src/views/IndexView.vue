<template>
    <el-container class="common-layout">
        <!-- 左侧边栏 -->
        <el-aside width="220px" class="dashboard-sidebar">
            <div class="sidebar-header">
                <img :src="logoUrl" alt="智能记账系统" class="h-4 w-4 mr-2 object-contain" />
                <h1 class="text-xl font-bold text-gray-800">智能记账系统</h1>
            </div>
            <el-menu class="el-menu-vertical-demo" background-color="#ffffff" text-color="#303133"
                active-text-color="#409EFF" router>
                <el-menu-item :index="{ name: 'DashBoard' }">
                    <el-icon>
                        <HomeFilled />
                    </el-icon>
                    <span>OVERVIEW</span>
                </el-menu-item>
                <el-menu-item :index="{ name: 'ShowItem' }">
                    <el-icon>
                        <Document />
                    </el-icon>
                    <span>ITEMS</span>
                </el-menu-item>
                <el-menu-item :index="{ name: 'AiAssistant' }">
                    <el-icon>
                        <MagicStick />
                    </el-icon>
                    <span>AI ASSISTANT</span>
                </el-menu-item>
                <el-menu-item :index="{ name: 'UserInfo' }">
                    <el-icon>
                        <Document />
                    </el-icon>
                    <span>USER INFO</span>
                </el-menu-item>
            </el-menu>
            <!-- 侧边栏底部时间显示 -->
            <div class="sidebar-footer">
                <el-divider />
                <div class="current-time">{{ }}</div>
            </div>
        </el-aside>

        <!-- 右侧主内容区 -->
        <el-container class="main-content-area">
            <!-- 顶部用户信息栏 -->
            <el-header class="user-info-header">
                <!--显示模块名-->
                <div class="module-indicator">
                    <span class="current-module">{{ currentModule }}</span>
                </div>
                <div class="user-profile">
                    <img :src="avatarUrl" class="user-avatar" @click="showDialog = true">
                    <div class="user-meta">
                        <span class="user-name">{{ username }}</span>
                        <el-button type="text" @click="logout">退出登录</el-button>
                    </div>
                </div>
            </el-header>

            <!-- 子页面展示区域 -->
            <el-main>
                <router-view />
            </el-main>
        </el-container>
    </el-container>


    <el-dialog title="用户信息" v-model="showDialog" width="400px" draggable overflow>
        <div class="dialog-content">
            <div class="user-info">
                <img :src="avatarUrl" class="user-avatar" />
                <el-form :model="userInfo" label-width="80px">
                    <el-form-item label="用户名">
                        <el-input v-model="userInfo.name" :disabled="modifiable" />
                    </el-form-item>
                    <el-form-item label="性别">
                        <el-radio-group v-model="userInfo.sex" :disabled="modifiable">
                            <el-radio label="man" value="man">男</el-radio>
                            <el-radio label="woman" value="woman">女</el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <el-form-item label="手机号">
                        <el-input v-model="userInfo.phone" :disabled="modifiable" />
                    </el-form-item>
                    <el-form-item label="邮箱">
                        <el-input v-model="userInfo.mail" :disabled="modifiable" />
                    </el-form-item>
                    <el-form-item label="生日">
                        <el-date-picker v-model="userInfo.birth" type="date" placeholder="选择日期"
                            :disabled="modifiable"></el-date-picker>
                    </el-form-item>
                </el-form>
            </div>
        </div>
        <div class="dialog-actions">
            <el-button type="primary" @click="changeModifiable">编辑</el-button>
            <el-button type="primary" @click="closeShowDialog">{{ closeOrSubmit }}</el-button>
        </div>
    </el-dialog>
</template>


<script lang="ts">
// import { defineComponent } from 'vue';
import { HomeFilled, Document, MagicStick } from '@element-plus/icons-vue';
import { useRouter, useRoute } from 'vue-router'; // 引入 useRouter
import Cookies from 'js-cookie'; // 引入 js-cookie
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ref, onMounted, watch } from 'vue';


interface UserInfo {
    uid: number;
    account: string;
    name: string;
    phone: string;
    mail: string;
    sex: string;
    birth: string;
    photo_adr: string;
}


export default {
    name: 'IndexView',

    setup() {
        const route = useRoute(); // 初始化route
        const username = ref('未登录用户'); // 使用响应式数据
        const currentModule = ref('数据概况'); // 默认模块名
        const avatarUrl = ref('/src/assets/avatar.png');
        const logoUrl = 'http://localhost:5000/static/ico_ai_jz.png'; // 替换为你的 logo 路径
        const router = useRouter(); // 将router初始化移至此处
        const showDialog = ref(false);
        const modifiable = ref(true);
        const closeOrSubmit = ref('关闭');


        const changeModifiable = () => {
            modifiable.value = !modifiable.value;
            if (modifiable.value) {
                closeOrSubmit.value = '关闭';
            }
            else {
                closeOrSubmit.value = '提交';
            }
        }

        // 提交修改信息
        const closeShowDialog = async () => {
            if (modifiable.value) {
                showDialog.value = false;
            } else {
                try {
                    const response = await axios.post('http://localhost:5000/user/updata', {
                        uid: userInfo.value.uid,
                        name: userInfo.value.name,
                        phone: userInfo.value.phone,
                        mail: userInfo.value.mail,
                        sex: userInfo.value.sex,
                        birth: userInfo.value.birth
                    }, {
                        withCredentials: true,
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });

                    if (response.data.status === 'success') {
                        ElMessage.success('修改成功');
                        modifiable.value = true;
                        showDialog.value = false;
                        // 更新本地存储的头像信息
                        // if (response.data.photo_adr) {
                        //     avatarUrl.value = response.data.photo_adr;
                        //     Cookies.set('avatarUrl', response.data.photo_adr);
                        // }
                    } else {
                        ElMessage.error(response.data.message || '修改失败');
                    }
                } catch (error) {
                    console.error('修改失败:', error);
                    ElMessage.error('网络请求异常');
                }
            }
        };


        // 用户信息响应式对象（包含完整字段）
        const userInfo = ref<UserInfo>({
            uid: 0,
            account: '',
            name: '未登录用户',
            phone: '',
            mail: '',
            sex: '',
            birth: '',
            photo_adr: '/src/assets/avatar.png'
        });

        const logout = () => {
            ElMessageBox.confirm('确定要退出登录吗？', '提示', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            }).then(() => {
                // 清除登录状态
                console.log('退出登录'); // 调试用，确保这里被调用
                Cookies.remove('user_id')
                // 跳转到登录页
                router.push('/')  // 修改 $router 为 router
            }).catch(() => {
                // 取消操作不做任何处理
            })
        }

        // 登录后获取用户信息
        const fetchUserInfo = async (userId: number) => {
            try {
                const instance = axios.create({ withCredentials: true });
                const response = await instance.get<{
                    status: string;
                    result: UserInfo;
                }>(`http://127.0.0.1:5000/user/info/${userId}`);
                if (response.data.status === 'success') {
                    // 完整更新用户信息
                    userInfo.value = {
                        ...response.data.result,  // 保留原有解构
                        uid: response.data.result?.uid || Number(userId) || 0  // 添加安全访问
                    };
                    userInfo.value = response.data.result;
                    username.value = userInfo.value.name;
                    avatarUrl.value = userInfo.value.photo_adr;
                    Cookies.set('avatarUrl', userInfo.value.photo_adr);
                }
            } catch (error) {
                console.error('获取用户信息失败:', error);
                ElMessage.error('用户信息加载失败');
            }
        };

        // 模块名称映射
        const getModuleName = (routeName: string): string => {
            const nameMap = {
                'DashBoard': '数据概况',
                'ShowItem': '账单管理',
                'AiAssistant': 'AI助手',
                'UserInfo': '用户信息'
            } as const;
            return nameMap[routeName as keyof typeof nameMap] || '未知模块';
        };


        onMounted(async () => {
            const userId = Number(Cookies.get('user_id'));
            if (userId) {
                await fetchUserInfo(userId);  // 现在这里可以正常调用了
            } else {
                router.push('/');
            }
        });

        watch(() => route.name, (newVal) => {
            currentModule.value = newVal ? getModuleName(newVal.toString()) : '未知模块';
        });


        return {
            logout,
            username, // 暴露用户名
            avatarUrl, // 暴露头像URL
            logoUrl, // 替换为你的 logo 路径
            currentModule, // 暴露当前模块名
            showDialog, // 暴露对话框状态
            userInfo, // 暴露用户信息
            modifiable,
            changeModifiable,
            closeOrSubmit,
            closeShowDialog,
        }
    },

    components: {
        HomeFilled,
        Document,
        MagicStick
    },

};
</script>

<style scoped>
/* 保持原有侧边栏样式 */
.dashboard-sidebar {
    background-color: #ffffff;
    box-shadow: 2px 0 6px rgba(0, 0, 0, 0.05);
    display: flex;
    flex-direction: column;
    padding: 20px 0;
    height: 100vh;
    /* 100% 视口高度 */

}

.sidebar-header {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 15px 15px;
    gap: 12px;
    /* 调整间距 */
    border-bottom: 1px solid #eee;
    margin-bottom: 20px;
}

.sidebar-header img {
    width: 32px !important;
    height: 32px !important;
    min-width: 32px;
}

.el-menu-vertical-demo {
    border-right: none;
    flex-grow: 1;
    height: 100vh
}

.el-menu-item {
    height: 50px;
    line-height: 50px;
    padding-left: 20px !important;
}

.module-indicator {
    order: -1;
    /* 强制左侧显示 */
    margin-right: auto;
    /* 左对齐 */
    padding-left: 20px;
    /* 添加左侧间距 */
}

.current-module {
    font-size: 18px;
    font-weight: 600;
    color: #409EFF;
}

.dashboard-header {
    background-color: #ffffff;
    /* 头部背景白色 */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    /* 头部阴影 */
    display: flex;
    justify-content: space-between;
    /* 左右对齐 */
    align-items: center;
    padding: 0 30px;
    /* 左右内边距 */
    height: 60px;
    /* 头部高度 */
    line-height: 60px;
    box-sizing: border-box;
}

.header-and-main {
    flex-direction: column;
    height: 100vh;
    /* 100% 视口高度 */
    overflow: hidden;
}

.user-info-header {
    justify-content: space-between;
    /* 改为两端对齐 */
    height: 80px !important;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    /* 新增右对齐 */
    background: #fff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

    .user-profile {
        display: flex;
        align-items: center;

        .user-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 15px;
            cursor: pointer;
        }

        .user-meta {
            display: flex;
            flex-direction: column;

            .user-name {
                font-weight: 500;
                margin-bottom: 5px;
            }
        }
    }
}

.sidebar-footer {
    padding: 15px;
    text-align: center;

    .current-time {
        font-size: 12px;
        color: #909399;
    }
}

.el-aside {
    height: 94vh;
    /* 固定高度 */
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
}

.dialog-content .user-avatar {
    width: 120px !important;
    height: 120px !important;
    border-radius: 50%;
    object-fit: cover;
    margin: 0 auto 20px;
}
</style>