<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from 'vue-class-component';

@Options({
  components: {
    // 你不再需要在这里直接导入或注册 HelloWorld 组件，
    // 因为它不会被 App.vue 直接渲染。
    // 如果你将来需要在其他地方使用 HelloWorld，可以在其他组件中导入它。
  },
})
export default class App extends Vue {}
</script>

<style>
/*
  #app 的样式保留，它定义了整个应用的根样式。
  font-family, -webkit-font-smoothing, -moz-osx-font-smoothing,
  text-align, color, margin-top 等样式。
  如果你希望你的登录页和主页有不同的布局和样式，
  你可以在 UserLogin.vue 和 AppDashboard.vue 内部定义各自的样式。
*/
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center; /* 默认居中，如果登录页不需要，可以在登录页重写 */
  color: #2c3e50;
  margin-top: 60px; /* 默认顶部间距，如果登录页不需要，可以在登录页重写 */
}
</style>