const path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

var config = require('./webpack.base.config.js');

config.entry = './frontend/index.tsx';

config.output.path = path.resolve('./frontend/static/dist/');


config.plugins =  config.plugins.concat([
    new BundleTracker({
        path: __dirname,
        filename: 'webpack-stats-prod.json',
        entrypoints: false}
    ),

    // removes a lot of debugging code in React
    new webpack.DefinePlugin({
        'process.env': {
        'NODE_ENV': JSON.stringify('production')
    }}),

    // keeps hashes consistent between compilations
    new webpack.optimize.OccurrenceOrderPlugin(),
]);

config.optimization = {
    minimizer: [
        new UglifyJsPlugin({
            cache: true,
            parallel: true,
            uglifyOptions: {
                compress: true,
                ecma: 6,
                mangle: true
            },
            sourceMap: true,
        })
    ]
};

// Add a loader for JSX files
config.module.rules.push(
  {
    test: /\.js$/,
    exclude: /node_modules/,
    use: ['babel-loader'],
  }
);

module.exports = config;
