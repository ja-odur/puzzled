const path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,

    entry:'./frontend/index.tsx',

    output: {
        path: path.resolve('./frontend/static/bundles/'),
        filename: '[name]-[hash].js'
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new webpack.HotModuleReplacementPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.tsx?$/,
                exclude: /node_modules/,
                use: ['awesome-typescript-loader']
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ['babel-loader']
            },
            {
                test: /\.sass$/,
                use: ['style-loader', 'css-loader', 'sass-loader']
            },
            {
                test: /\.(png|je?pg|webp|svg)$/,
                use: ['url-loader']
            },
            {
                test: /\.html$/,
                use: ['html-loader']
            },
            {
                enforce: "pre",
                test: /\.js$/,
                loader: "source-map-loader"
            }
        ]
    },

    resolve: {
        extensions: ['*', '.js', '.jsx', '.ts', '.tsx', '.scss', '.sass', '.png']
    },

};
