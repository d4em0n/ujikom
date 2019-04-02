var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,

  entry: './inventory/sarana/static/js/index',

  output: {
      path: path.resolve('./inventory/sarana/static/bundles/'),
      filename: "[name]-[hash].js",
  },

  plugins: [
    new BundleTracker({filename: './inventory/webpack-stats.json'}),
  ],
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['babel-loader']
      },
      {
        test: /\.css$/,
        use: [
            {
                loader: 'css-loader',
                options: { modules: true }
            }
        ]
      }
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx']
  }

};