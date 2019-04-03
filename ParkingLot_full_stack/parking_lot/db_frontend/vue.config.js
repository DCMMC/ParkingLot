module.exports = {
  assetsDir: 'static',
  // chainWebpack: config => {
  //   config.externals({
  //     'three': 'src/assets/js/three.min.js'
  //   })
  // },
  pages: {
    index: {
      entry: 'src/main.js',
      template: 'public/index.html',
      filename: 'index.html'
    },
    add_coach: {
      entry: 'src/add-coach.js',
      template: 'public/add-coach.html',
      filename: 'add-coach.html'
    },
    add_student: {
      entry: 'src/add-student.js',
      template: 'public/add-student.html',
      filename: 'add-student.html'
    },
    view_student: {
      entry: 'src/view-student.js',
      template: 'public/view-student.html',
      filename: 'view-student.html'
    },  
    view_coach: {
      entry: 'src/view-coach.js',
      template: 'public/view-coach.html',
      filename: 'view-coach.html'
    }
  }
}