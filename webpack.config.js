
module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
      minSize: 1,
      minChunks: 2
    }
  },

  entry: './main/src/components/index.js',
  // 2
  output: {
    path: __dirname + '/dist',
    publicPath: '/',
    filename: 'bundle.js',
    chunkFilename: '[name].bundle.js',
  },
  // 3
  devServer: {
    historyApiFallback: true,
    contentBase: './main/dist',
    proxy: {
        '/api': {
            target: 'http://test.fedotochkin.ru',
            secure: false,
            changeOrigin: true,
        },
        '/media': {
            target: 'http://test.fedotochkin.ru',
            secure: false,
            changeOrigin: true,
        },
        '/static': {
            target: 'http://test.fedotochkin.ru',
            secure: false,
            changeOrigin: true,
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
  },
};
