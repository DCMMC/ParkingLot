const CopyWebpackPlugin = require('copy-webpack-plugin')
const path = require('path')

module.exports = {
  assetsDir: 'static',
  configureWebpack: {
    plugins: [
      new CopyWebpackPlugin([
        {
          from: path.resolve(__dirname, './models'),
          to: 'models',
          ignore: ['.*']
        }
      ]),
    ]
  },
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html'
    },
    client_indoor: {
      entry: 'src/client-indoor.js',
      template: 'public/client-indoor.html',
      filename: 'client-indoor.html'
    },
    client_outdoor: {
      entry: 'src/client-outdoor.js',
      template: 'public/client-outdoor.html',
      filename: 'client-outdoor.html'
    },
    admin: {
      entry: 'src/admin.js',
      template: 'public/admin.html',
      filename: 'admin.html'
    }
  }
}