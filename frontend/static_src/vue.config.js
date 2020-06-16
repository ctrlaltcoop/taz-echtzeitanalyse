module.exports = {
  outputDir: '../static/app',
  publicPath: '/static/app/',
  devServer: {
    proxy: 'http://localhost:8000',
    disableHostCheck: true
  }
}
