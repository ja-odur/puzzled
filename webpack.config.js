const path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

var config = require('./webpack.base.config.js');

config.entry = './frontend/index.tsx'

config.output.path = path.resolve('./frontend/static/webpack_bundles/')

// Add BundleTracker plugin
config.plugins =  config.plugins.concat([
        new BundleTracker({
          path: __dirname,
          filename: 'webpack-stats.json',
          entrypoints: false
        }),
    ]);

// Add a loader for JSX files
config.module.rules.push(
  {
    test: /\.js$/,
    exclude: /node_modules/,
    use: ['babel-loader']
  }
);

module.exports = config;
