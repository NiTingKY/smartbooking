<template>
  <div class="common-layout">
    <el-container class="dashboard-container">
      <SidebarMenu />

      <el-container class="main-content-area">

        <el-main class="dashboard-main-content">
          <div v-if="activeMenu === 'dashboard'" class="dashboard-content">
            <el-row :gutter="20" class="card-row">
              <el-col :span="8">
                <el-card class="box-card">
                  <div class="card-header">总收入</div>
                  <div class="text item">
                    <span class="value">{{ totalIncome }}</span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="box-card">
                  <div class="card-header">总支出</div>
                  <div class="text item">
                    <span class="value">{{ totalExpense }}</span>
                  </div>
                </el-card>
              </el-col>
              <el-col :span="8">
                <el-card class="box-card">
                  <div class="card-header">净收入</div>
                  <div class="text item">
                    <span class="value">{{ netIncome }}</span>
                  </div>
                </el-card>
              </el-col>
            </el-row>

            <el-row :gutter="20" class="chart-row">
              <el-col :span="12">
                <el-card class="box-card">
                  <div id="incomeChart" class="chart"></div>
                </el-card>
              </el-col>
              <el-col :span="12">
                <el-card class="box-card">
                  <div id="expenseChart" class="chart"></div>
                </el-card>
              </el-col>
            </el-row>

            <el-row :gutter="20" class="chart-row">
              <el-col :span="24">
                <el-card class="box-card">
                  <div class="card-header">最近账单</div>
                  <el-table :data="recentBills" style="width: 100%" stripe>
                    <el-table-column prop="create_time" label="日期" width="250" />
                    <el-table-column prop="is_income" label="类型" width="200">
                      <template #default="{ row }">
                        <el-tag :type="row.is_income === 1 ? 'success' : 'danger'">
                          {{ row.is_income === 1 ? '收入' : '支出' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="dollar" label="金额" width="200">
                      <template #default="{ row }">
                        ￥{{ (row.dollar || 0).toFixed(2) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="source" label="分类" width="200" />
                    <el-table-column prop="detail" label="备注" />
                  </el-table>
                </el-card>
              </el-col>
            </el-row>
          </div>

        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, nextTick,watch } from 'vue';
import axios from 'axios';
import Cookies from 'js-cookie';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts'; // 确保 echarts 被正确导入
// import SidebarMenu from '@/components/SidebarMenu.vue';


interface MonthlyData {
  year: number;
  month: number;
  total: number;
}

interface BillItem {
  id?: number; // 添加可选ID字段
  create_time: string;
  dollar: number;
  plat: string;
  source: string;
  detail: string;  // 补充缺失的属性定义
  is_income?: number;
}

export default defineComponent({
  name: 'AppDashboard',
  components: {
  },
  setup() {
    const recentBills = ref<BillItem[]>([]);
    const userId = ref<string | undefined>(Cookies.get('user_id'));

    axios.defaults.withCredentials = true;

    const currentDate = ref('');
    const activeMenu = ref('dashboard'); // 当前激活的菜单项

    // 初始化数据展示页面
    const totalIncome = ref('加载中...');
    const totalExpense = ref('加载中...');
    const netIncome = ref('加载中...');

    // 获取用户总收入和支出
    const fetchTotal = async (type: String) => {
      try {
        const instance = axios.create({ withCredentials: true });
        const response = await instance.get(`http://127.0.0.1:5000/analysis/total`, {
          params: { type },
          withCredentials: true
        });

        if (response.data.status === 'success') {
          // 完整更新用户信息
          if (type === 'income') {
            totalIncome.value = `${response.data.total.toFixed(2)}`;
          }
          else if (type === 'expense') {
            totalExpense.value = `${response.data.total.toFixed(2)}`;
          }
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        ElMessage.error('用户信息加载失败');
      }
    };


    // ECharts 图表实例
    let incomeChartInstance: echarts.ECharts | null = null;
    let expenseChartInstance: echarts.ECharts | null = null;

    // 菜单选择处理
    const handleMenuSelect = (index: string) => {
      activeMenu.value = index;
      // 在切换到数据概览时重新渲染图表
      if (index === 'dashboard') {
        nextTick(() => {
          initCharts(); // 传递用户ID
        });
      }
    };

    // 初始化图表
    const initCharts = async () => {  // 添加函数参数

      // 初始化收入支出折线图
      try {
        // 获取月度收入数据
        const incomeResponse = await axios.get(`http://127.0.0.1:5000/analysis/monthly`, {
          params: { type: 'monthly_income' },  // 参数改为对象形式
          withCredentials: true
        });

        // 获取月度支出数据
        const expenseResponse = await axios.get(`http://127.0.0.1:5000/analysis/monthly`, {
          params: { type: 'monthly_expense' },  // 参数改为对象形式
          withCredentials: true
        });

        const monthlyIncomeData = incomeResponse.data?.data || [];
        const monthlyExpenseData = expenseResponse.data?.data || [];

        // 处理带年份的月份格式（YYYY-MM）
        // 在initCharts函数中添加类型注解
        const incomeMonths = monthlyIncomeData.map((item: MonthlyData) =>
          `${item.year}-${String(item.month).padStart(2, '0')}`
        );
        const expenseMonths = monthlyExpenseData.map((item: MonthlyData) =>
          `${item.year}-${String(item.month).padStart(2, '0')}`
        );

        const incomeAmounts = monthlyIncomeData.map((item: MonthlyData) =>
          Number(item.total.toFixed(2))
        );

        const expenseAmounts = monthlyExpenseData.map((item: MonthlyData) =>
          Number(item.total.toFixed(2))
        );

        // 支出折线图
        if (document.getElementById('expenseChart')) {
          if (expenseChartInstance) {
            expenseChartInstance.dispose();
          }
          expenseChartInstance = echarts.init(document.getElementById('expenseChart') as HTMLElement);
          expenseChartInstance.setOption({
            title: { text: '月度支出趋势', left: 'center' },
            tooltip: {
              formatter: '￥{c}',
              axisPointer: {
                type: 'shadow'
              }
            },
            xAxis: {
              type: 'category',
              data: expenseMonths.length > 0 ? expenseMonths : ['暂无数据'],
              axisLabel: {
                rotate: 45
              }
            },
            yAxis: {
              type: 'value',
              axisLabel: {
                formatter: '￥{value}'
              }
            },
            series: [{
              name: '支出',
              type: 'line',
              smooth: false,
              data: expenseAmounts,
              itemStyle: {
                color: '#e74c3c'
              }
            }]
          });
        }

        // 收入折线图
        if (document.getElementById('incomeChart')) {
          if (incomeChartInstance) {
            incomeChartInstance.dispose(); // 销毁旧实例
          }
          incomeChartInstance = echarts.init(document.getElementById('incomeChart') as HTMLElement);
          incomeChartInstance.setOption({
            title: { text: '月度收入趋势', left: 'center' },
            tooltip: {
              formatter: '￥{c}',
              axisPointer: {
                type: 'shadow'
              }
            },
            xAxis: {
              type: 'category',
              data: incomeMonths.length > 0 ? incomeMonths : ['暂无数据'],
              axisLabel: {
                rotate: 45
              }
            },
            yAxis: {
              type: 'value',
              axisLabel: {
                formatter: '￥{value}'
              }
            },
            series: [{
              name: '支出',
              type: 'line',
              smooth: false,
              data: incomeAmounts,
              itemStyle: {
                color: '#3498db'
              }
            }]
          });
        }
      } catch (error) {
        console.error('获取月度数据失败:', error);
        ElMessage.error('支出数据加载失败');
      }
    };

    // 重新调整图表大小
    const handleResize = () => {
      incomeChartInstance?.resize();
      expenseChartInstance?.resize();
    };

    // 获取最近账单方法
    const fetchRecentBills = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/analysis/recent', {
          withCredentials: true
        });
        interface RecentBillItem {
          create_time: string;
          is_income: number;
          dollar: number;
          source: string;
          detail: string;
          currency: string;
        }

        // 修改数据映射部分
        recentBills.value = response.data.data.map((item: RecentBillItem) => ({
          ...item,
          currency: response.data.currency || 'CNY'
        }));
      } catch (error) {
        console.error('获取最近账单失败:', error);
        ElMessage.error('账单数据加载失败');
      }
    };


    // 获取当前日期
    const updateCurrentDate = () => {
      const date = new Date();
      currentDate.value = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
    };


    watch(userId, (newVal) => {
      if (!newVal) {
        // 清空所有数据
        totalIncome.value = '0.00';
        totalExpense.value = '0.00';
        netIncome.value = '0.00';
        recentBills.value = [];

        // 销毁图表实例
        incomeChartInstance?.dispose();
        expenseChartInstance?.dispose();
        incomeChartInstance = null;
        expenseChartInstance = null;
      }
    });


    // 生命周期钩子
    onMounted(() => {

      // 新增调试信息
      console.log('[DEBUG] 所有cookie:', document.cookie);
      console.log('[DEBUG] 请求凭据支持:', axios.defaults.withCredentials);

      console.log('[DEBUG] Cookie中获取的用户ID:', userId); // 新增调试日志


      // 初始化总收入支出数据
      Promise.all([
        fetchTotal('income'),
        fetchTotal('expense')
      ]).then(() => {
        const income = parseFloat(totalIncome.value) || 0;
        const expense = parseFloat(totalExpense.value) || 0;
        netIncome.value = `${(income - expense).toFixed(2)}`;
      });
      fetchRecentBills();
      updateCurrentDate();
      // 初始化图表
      nextTick(() => {
        initCharts();  // 传递从cookie获取的userId
      });
      // 监听窗口大小变化
      window.addEventListener('resize', handleResize);
    });

    return {
      currentDate,
      activeMenu,
      totalIncome,
      totalExpense,
      netIncome,
      recentBills,
      handleMenuSelect,
    };
  },
});
</script>

<style scoped>
/* 全局布局容器 */
.common-layout {
  min-height: 100vh;
  display: flex;
  /* 确保整个应用容器是flex布局 */
}

/* 仪表盘容器，用于左右分栏 */
.dashboard-container {
  flex: 1;
  /* 让容器占据所有可用空间 */
  background-color: #f0f2f5;
  /* 整体背景色，类似Gemini的浅灰色 */

}


.sidebar-header {
  display: flex;
  align-items: center;
  justify-content: center;
  /* Logo和标题居中 */
  padding: 0 20px 20px;
  /* 底部内边距 */
  border-bottom: 1px solid #eee;
  /* 底部边框 */
  margin-bottom: 20px;
}

.sidebar-header img {
  height: 36px;
  /* 调整 Logo 大小 */
  width: 36px;
  margin-right: 10px;
}

.sidebar-header h1 {
  font-size: 18px;
  color: #333;
}

.el-menu-vertical-demo {
  border-right: none;
  /* 移除Element Plus菜单默认边框 */
  flex-grow: 1;
  /* 让菜单占据剩余空间 */
}

.el-menu-item {
  height: 50px;
  /* 菜单项高度 */
  line-height: 50px;
  padding-left: 20px !important;
  /* 调整内边距 */
  color: #606266;
}

.el-menu-item.is-active {
  background-color: #ecf5ff;
  /* 选中时的背景色 */
  color: #409EFF;
  /* 选中时的文字颜色 */
}

.el-menu-item:hover {
  background-color: #f6f6f6;
  /* 悬停时的背景色 */
}

.el-menu-item .el-icon {
  margin-right: 10px;
  font-size: 20px;
}

/* 主内容区域容器 */
.main-content-area {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* 头部样式 */
.dashboard-header {
  background-color: #ffffff;
  /* 头部背景白色 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  /* 头部阴影 */
  display: flex;
  justify-content: space-between;
  /* 左右两边对齐 */
  align-items: center;
  padding: 0 30px;
  /* 左右内边距 */
  height: 60px;
  /* 头部高度 */
  line-height: 60px;
  box-sizing: border-box;
}

.header-left {
  display: flex;
  align-items: center;
  /* 可以在这里添加其他左侧头部元素，如面包屑 */
}

.current-date {
  font-size: 14px;
  color: #909399;
  margin-right: 20px;
  /* 与右侧用户信息的间距 */
}

.header-right {
  display: flex;
  align-items: center;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  /* 圆形头像 */
  margin-right: 10px;
  object-fit: cover;
  /* 确保图片不变形 */
}

.user-name {
  font-size: 15px;
  color: #303133;
  margin-right: 15px;
}

.logout-button {
  height: 32px;
  /* 按钮高度 */
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 主要内容区域 */
.dashboard-main-content {
  padding: 30px;
  /* 主要内容的内边距 */
  overflow: hidden;
  /* 禁用容器溢出滚动
  /* 内容溢出时允许滚动 */
  background-color: #f0f2f5;
  /* 与整体容器背景色一致 */
}

/* 数据概览卡片和图表布局 */
.card-row {
  margin-bottom: 20px;
  /* 卡片行之间的间距 */
}

.chart-row {
  margin-bottom: 20px;
}

.box-card {
  border-radius: 8px;
  /* 卡片圆角 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  /* 卡片阴影 */
}

.card-header {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
}

.text.item .value {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  /* 主要数值颜色 */
}

.chart {
  width: 100%;
  height: 300px;
  /* 图表高度 */
}

/* 账单管理和AI助手页面的通用容器 */
.bills-container,
.ai-assistant-container {
  background-color: #ffffff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  min-height: calc(100vh - 120px - 60px - 60px);
  /* 减去头部、上下padding和可能存在的其他元素高度 */
  display: flex;
  flex-direction: column;
}


.input-area {
  display: flex;
  padding: 10px;
  border-top: 1px solid #e4e7ed;
  background-color: #fff;
}

.chat-input {
  flex: 1;
  margin-right: 10px;
}

.typing-indicator {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  padding: 5px 15px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background-color: #909399;
  border-radius: 50%;
  margin: 0 3px;
  animation: typing-bounce 0.6s infinite ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing-bounce {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}

.el-table {
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}
</style>
