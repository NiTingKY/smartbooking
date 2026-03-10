import { createRouter, createWebHistory } from 'vue-router';
import UserLogin from '../views/UserLogin.vue';
import IndexView from '../views/IndexView.vue';
import ErrorPage from '../views/ErrorPage.vue';

import AppDashboard from '../components/AppDashboard.vue';
import ShowItem from '../components/ShowItem.vue';
import AiAssistant from '@/components/AiAssistant.vue';

import Cookies from 'js-cookie';
import UserInfo from '@/components/UserInfo.vue';

const routes = [
  {
    path: '/',
    name: 'UserLogin',
    component: UserLogin
  },
  {
    path: '/index',
    name: 'IndexView',
    component: IndexView,
    children: [
      {
        path: '',
        name: 'AppDashboard',
        component: AppDashboard,
      },
      {
        path: '/showItem',
        name: 'ShowItem',
        component: ShowItem
      },
      {
        path: '/dashBoard',
        name: 'DashBoard',
        component: AppDashboard
      },
      {
        path: '/ai-assistant',
        name: 'AiAssistant',
        component: AiAssistant
      },
      {
        path: '/userInfo',
        name: 'UserInfo',
        component: UserInfo
      }
      // 其他子路由...
    ]
  },
  {
    path: '/:pathMatch(.*)*', // 动态匹配任意路径
    name: 'NotFound',
    component: ErrorPage
  }
  // 其他子路由...
]


// 使用 createRouter 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes
});

// 可选：添加导航守卫，用于认证检查（推荐）
router.beforeEach((to, from, next) => {
  // 假设您在登录成功时将登录状态存储在 localStorage 中
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
    || Cookies.get('session_id');  // 添加cookie验证

  if (to.meta.requiresAuth && !isLoggedIn) {
    // 如果路由需要认证但用户未登录，重定向到登录页
    next('/');
  } else {
    // 否则，允许导航
    next();
  }
});



export default router;
