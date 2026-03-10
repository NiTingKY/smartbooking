const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  // 新增或修改 publicPath
  publicPath: '/' // 如果您的Flask应用在根路径提供Vue应用
  // 如果您希望在子路径提供，例如 http://localhost:5000/app/，则设置为 '/app/'
})