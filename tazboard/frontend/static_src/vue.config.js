module.exports = {
  outputDir: '../static/app',
  publicPath: '/static/app/',
  devServer: {
    proxy: 'http://localhost:8000',
    disableHostCheck: true
  },
  configureWebpack: {
    externals: {
      moment: 'moment'
    }
  },
  pages: {
    index: {
      // entry for the page
      entry: 'src/main.ts',
      // the source template
      template: 'public/index.html',
      // output as dist/index.html
      filename: 'index.html',
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: 'die echtzeitanalyse',
      // chunks to include on this page, by default includes
      // extracted common chunks and vendor chunks.
      chunks: ['chunk-vendors', 'chunk-common', 'index']
    }
  }
}
