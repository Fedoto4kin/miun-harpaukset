
module.exports = {
  entry: './main/src/components/index.js',
  // 2
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js'
  },
  // 3
  devServer: {
    contentBase: './main/dist',
    proxy: {
        '/api': {
            target: 'http://fedotochkin.ru',
            secure: false
        }
    }
  },
  module: {
  rules: [
    {
      test: /\.js$/,
      exclude: /node_modules/,
      use: {
        loader: "babel-loader"
      }
    },
    {
      test: /\.css$/,
      include: /node_modules/,
      use: ['style-loader', 'css-loader']
    }
  ]
  }
};
