<template>
  <div class="common-layout">
    <el-container class="dashboard-container">
      <SidebarMenu active-menu="bills" />

      <!-- 页面主要内容 -->
    </el-container>
  </div>
  <div class="show-item-container">
    <div>
      <el-button type="primary" @click="handleAdd">添加记账信息</el-button>
      <!-- 添加查询按钮 -->
      <el-button type="info" @click="showQueryDialog">查询记账信息</el-button>
    </div>
    <div>
      <el-card class="table-card">
        <el-table :data="tableData" style="width: 100%" stripe @sort-change="handleSortChange">
          <!-- 修改后的日期列 -->
          <el-table-column prop="create_time" label="日期" align="center"
            :formatter="(row) => formatTime(row.create_time)" sortable="custom" />
          <el-table-column prop="dollar" label="金额" align="center" sortable="custom"
            :sort-method="(a, b) => a.dollar - b.dollar">
          </el-table-column>
          <el-table-column prop="is_income" label="类型" width="120">
            <template #default="{ row }">
              <el-tag :type="row.is_income === 1 ? 'success' : 'danger'">
                {{ row.is_income === 1 ? '收入' : '支出' }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="plat" label="平台" align="center" sortable="custom" />
          <el-table-column prop="source" label="来源" align="center" sortable="custom" />
          <el-table-column label="操作" align="center">
            <template #default="scope">
              <el-button type="info" size="small" @click="handleView(scope.row)">查看</el-button>
              <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
              <el-button type="danger" size="small" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
          <template>
            <el-pagination background layout="prev, pager, next" :total="total" />
          </template>
        </el-table>
        <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage"
          :page-sizes="pageSizes" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total">
        </el-pagination>
      </el-card>
    </div>


    <!-- 查看详情对话框 -->
    <el-dialog v-model="viewDialogVisible" title="详细信息" width="30%" draggable overflow>
      <el-form :model="currentItem" label-width="80px">
        <el-form-item label="日期">
          <el-input v-model="currentItem.create_time" disabled />
        </el-form-item>
        <el-form-item label="金额">
          <el-input v-model="currentItem.dollar" disabled />
        </el-form-item>
        <el-form-item label="平台">
          <el-input v-model="currentItem.plat" disabled />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="currentItem.source" disabled />
        </el-form-item>
        <el-form-item label="细节">
          <el-input v-model="currentItem.detail" disabled />
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- 编辑详情对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑信息" width="30%" draggable overflow>
      <el-form :model="currentItem" label-width="80px">
        <el-form-item label="日期">
          <el-input v-model="currentItem.create_time" />
        </el-form-item>
        <el-form-item label="金额">
          <el-input v-model="currentItem.dollar" />
        </el-form-item>
        <el-form-item label="平台">
          <el-input v-model="currentItem.plat" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="currentItem.source" />
        </el-form-item>
        <el-form-item label="细节">
          <el-input v-model="currentItem.detail" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">提交</el-button>
      </template>
    </el-dialog>

    <!-- 添加--对话框 -->
    <el-dialog v-model="addDialogVisible" title="添加信息" width="30%" draggable overflow>
      <el-form :model="newItem" label-width="80px">
        <el-form-item label="金额">
          <el-input v-model="newItem.dollar" />
        </el-form-item>
        <el-form-item label="平台">
          <el-input v-model="newItem.plat" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="newItem.source" />
        </el-form-item>
        <el-form-item label="细节">
          <el-input v-model="newItem.detail" />
        </el-form-item>
        <el-form-item label="收支" v-model="is_income">
          <el-radio-group v-model="newItem.is_income">
            <el-radio value="1" label="收入">收入</el-radio>
            <el-radio value="0" label="支出">支出</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAddSubmit">提交</el-button>
      </template>
    </el-dialog>

    <!-- 查询对话框 -->
    <el-dialog v-model="queryDialogVisible" title="查询信息" width="30%" draggable overflow>
      <el-form :model="queryForm" label-width="80px">
        <el-form-item label="开始日期">
          <el-date-picker v-model="queryForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期">
          <el-date-picker v-model="queryForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
        <el-form-item label="收支">
          <el-radio-group v-model="queryForm.is_income">
            <el-radio value="1" label="收入">收入</el-radio>
            <el-radio value="0" label="支出">支出</el-radio>
            <el-radio value="" label="全部">全部</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="平台">
          <el-input v-model="queryForm.plat" placeholder="输入平台名称" />
        </el-form-item>
        <el-form-item label="来源">
          <el-input v-model="queryForm.source" placeholder="输入来源名称" />
        </el-form-item>
        <el-form-item label="细节">
          <el-input v-model="queryForm.detail" placeholder="输入细节关键词" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="queryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleQuery">查询</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import Cookies from 'js-cookie';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ref } from 'vue';

export default {
  name: 'ShowItem',
  components: {
  },
  data() {
    return {
      currentPage: 1, //当前页
      total: 0, //总条数
      tableData: [], //当前页码的表格数据
      pageSize: 5, //当前页容量
      pageSizes: [5, 7, 10],
      items: [],
      userId: null,
      viewDialogVisible: false, // 控制查看对话框显示
      editDialogVisible: false, // 控制编辑对话框显示
      addDialogVisible: false, // 控制添加对话框显示
      queryDialogVisible: false, // 控制查询对话框显示
      newItem: {
        dollar: '',
        plat: '',
        source: '',
        detail: '',
        is_income: '',
      },
      currentItem: null, // 当前查看或编辑的项
      is_income: ref(1),
      queryForm: {
        start_date: '',
        end_date: '',
        is_income: '',
        plat: '',
        source: '',
        detail: ''
      }
    };
  },
  watch: {
    // items 变化时重新计算总记录数 和 当前页数据
    items: {
      handler(newVal) {
        this.total = newVal.length;
        this.currentPage = 1;
        this.handleCurrentChange(this.currentPage);
        this.getList();
      },
      immediate: true // 立即执行一次
    }
  },
  setup() {
    console.log('Setup function called');
    return {
    };
  },
  async created() {
    // 调用加载数据方法
    this.userId = Cookies.get('user_id');
    console.log('user_id:', this.userId);
    await this.loadData(this.userId);
    this.total = this.items.length;
    this.getList(); // 加载数据后获取当前页数据
  },
  methods: {
    handleSizeChange(val) {
      this.currentPage = 1;
      this.pageSize = val;
      this.getList();
    },
    //切换当前页
    handleCurrentChange(val) {
      this.currentPage = val;
      this.getList();
    },
    //获取表格数据  
    getList() {
      this.tableData = this.getNeedArr(this.items, this.pageSize)[this.currentPage - 1];
    },
    // 前端处理分页
    getNeedArr(array, size) {       //获取所需指定长度分割的数组;参数1为用于分割的总数组,参数2为分割数组后每个小数组的长度
      const length = array.length;
      //判断不是数组，或者size没有设置，size小于1，就返回空数组
      if (!length || !size || size < 1) {
        return [];
      }

      let index = 0; //用来表示切割元素的范围start
      let resIndex = 0; //用来递增表示输出数组的下标

      //根据length和size算出输出数组的长度，并且创建它。
      let result = new Array(Math.ceil(length / size));
      //进行循环
      while (index < length) {
        //循环过程中设置result[0]和result[1]的值。该值根据array.slice切割得到。
        result[resIndex++] = array.slice(index, (index += size));
      }
      //输出到新数组
      return result;
    },
    handleSortChange({ prop, order }) {
      if (order) {
        this.items.sort((a, b) => {
          // 日期字段特殊处理
          if (prop === 'create_time') {
            const dateA = new Date(a.create_time).getTime()
            const dateB = new Date(b.create_time).getTime()
            return order === 'ascending' ? dateA - dateB : dateB - dateA
          }
          if (prop === 'dollar') {
            // 金额字段直接比较
            return order === 'ascending' ? a.dollar - b.dollar : b.dollar - a.dollar
          }
          if (prop === 'plat') {
            // 平台字段直接比较
            return order === 'ascending' ? a.plat.localeCompare(b.plat) : b.plat.localeCompare(a.plat)
          }
          return order === 'ascending' ? a.plat.localeCompare(b.plat) : b.plat.localeCompare(a.plat)
        })
      }
      this.currentPage = 1;
      this,this.handleCurrentChange(this.currentPage);
      this.getList();
    },

    // 加载数据方法
    // 针对 ISO 格式日期的时间格式化函数
    formatTime(timestamp) {
      if (!timestamp) return '--';
      const date = new Date(timestamp);
      if (isNaN(date.getTime())) {
        console.error('无效时间戳:', timestamp);
        return '无效时间';
      }
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      const hour = String(date.getHours()).padStart(2, '0');
      const minute = String(date.getMinutes()).padStart(2, '0');
      return `${year}-${month}-${day} ${hour}:${minute}`;
    },
    async loadData(userId) {
      if (!userId) {
        throw new Error('未找到 user_id');
      }
      // 设置 axios 实例，开启 withCredentials
      const instance = axios.create({
        withCredentials: true
      });
      const response = await instance.get(
        `http://127.0.0.1:5000/items/select/${userId}`
      );
      console.log(response);
      if (response.status === 200) {
        this.items = response.data.filter(item => item.is_delete !== 1);
      }
    },
    handleAdd() {
      this.newItem = {
        dollar: '',
        plat: '',
        source: '',
        detail: ''
      };
      this.addDialogVisible = true; // 显示添加对话框
    },
    handleView(row) {
      this.currentItem = row; // 设置当前查看的项
      this.viewDialogVisible = true; // 显示查看对话框
    },
    handleEdit(row) {
      this.currentItem = { ...row }; // 复制一份数据，避免直接修改原数据
      this.editDialogVisible = true; // 显示编辑对话框
    },
    async handleDelete(row) {
      try {
        const value = await ElMessageBox.confirm(
          '确定删除该条记录吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning',
          }
        );
        console.log(value);
        if (value) {
          // 用户点击确定
          if (!row || !row.uid) {
            console.error('缺少有效的 item_id');
            ElMessage.error('删除失败');
            return;
          }
          const itemId = row.uid;
          console.log('删除的 item_id:', itemId);
          const url = `http://127.0.0.1:5000/items/delete/${itemId}`;
          // 复制当前行数据并设置 is_delete 为 1
          const response = await axios.delete(url);
          if (response.status === 200) {
            ElMessage.success('删除成功');
            // 重新加载数据
            await this.loadData(this.userId);
          }
        }
      } catch (error) {
        if (error === 'cancel') {
          // 用户点击取消
          ElMessage.info('已取消删除操作');
        } else {
          ElMessage.error('删除失败');
          console.error('删除失败:', error);
        }
      }
    },
    async handleAddSubmit() {
      try {
        const url = `http://127.0.0.1:5000/items/add`;
        const response = await axios.post(
          url, this.newItem, {
          withCredentials: true, // 确保携带 cookie
        }
        )
        if (response.status === 200) {
          ElMessage.success('添加成功');
          this.addDialogVisible = false; // 关闭对话框
          // 重新加载数据
          await this.loadData(this.userId);
        }
      }
      catch (error) {
        ElMessage.error('添加失败');
      }
    },
    async handleSubmit() {
      try {
        if (!this.currentItem || !this.currentItem.uid) {
          console.error('缺少有效的 item_id');
          return;
        }
        const itemId = this.currentItem.uid;
        const url = `http://127.0.0.1:5000/items/update/${itemId}`;
        const response = await axios.put(url, this.currentItem, {
          withCredentials: true, // 确保携带 cookie
        });
        if (response.status === 200) {
          ElMessage.success('提交成功');
        }
        // 可以在这里更新表格数据
        this.editDialogVisible = false;
        // 重新加载数据
        await this.loadData(this.userId);
      } catch (error) {
        ElMessage.error('提交失败');
      }
    },
    showQueryDialog() {
      this.queryDialogVisible = true;
    },
    async handleQuery() {
      try {
        const formData = {
          ...this.queryForm,
          user_id: this.userId
        };
        const instance = axios.create({
          withCredentials: true
        });
        console.log(formData); // 打印 formData 以检查值
        const response = await instance.post(
          `http://127.0.0.1:5000/items/select/selectByJson`,
          formData
        );
        if (response.status === 200) {
          this.items = response.data.filter(item => item.is_delete !== 1);
          this.queryDialogVisible = false;
          ElMessage.success('查询成功');
        }
      } catch (error) {
        ElMessage.error('查询失败');
        console.error('查询失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.show-item-container {
  padding: 20px;
}

.page-title {
  text-align: center;
  margin-bottom: 20px;
  color: #409EFF;
}

.table-card {
  margin: 0 auto;
  max-width: 1200px;
}

/* 新增金额颜色样式 */
:deep(.income) {
  color: #67C23A;
  font-weight: 500;
}

:deep(.expense) {
  color: #F56C6C;
  font-weight: 500;
}


</style>