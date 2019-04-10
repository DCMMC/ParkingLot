module.exports = (api, projectOptions) => {
  api.chainWebpack(webpackConfig => {
    // see https://github.com/vuejs/vue-cli/issues/2463
    if (projectOptions.pages) {
      Object.keys(projectOptions.pages).forEach(page => {
      	console.log('remove ' + page)
        webpackConfig.plugins.delete(`preload-${page}`)
        webpackConfig.plugins.delete(`prefetch-${page}`)
      })
    }
  })
}
