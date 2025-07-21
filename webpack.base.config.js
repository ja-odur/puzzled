const path = require('path');
const dotenv = require('dotenv');
var webpack = require('webpack');

function compact(items) {
    return items.filter(item => item);
}

const config = () => {

    const env = dotenv.config().parsed;

    const envKeys = Object.keys(env).reduce((prev, next) => {
        prev[`process.env.${next}`] = JSON.stringify(env[next]);
        return prev;
      }, {});

    return {
        context: __dirname,

        entry: './frontend/index.tsx',

        output: {
            path: path.resolve('./frontend/static/webpack_bundles/'),
            filename: '[name]-[hash].js'
        },

        plugins: [
            new webpack.DefinePlugin(envKeys)
        ],

        module: {
            rules: [
                {
                    test: /\.tsx?$/,
                    exclude: /node_modules/,
                    use: ['ts-loader']
                },
                {
                    test: /\.js$/,
                    exclude: /node_modules/,
                    use: ['babel-loader']
                },
                {
                  test: /\.(scss|sass)$/,
                  use: [
                    'style-loader',
                    'css-loader',
                    {
                      loader: 'sass-loader',
                      options: {
                        implementation: require('sass'),
                      },
                    },
                  ],
                },
                {
                    test: /\.(png|je?pg|webp)$/,
                    use: ['url-loader']
                },
                {
                    test: /\.html$/,
                    use: ['html-loader']
                },
                {
                    enforce: "pre",
                    test: /\.js$/,
                    loader: "source-map-loader",
                    exclude: /node_modules/  // 👈 add this line
                },
                // Fonts
                {
                    test: /\.(woff2|woff|ttf|eot|svg)$/,
                    // include: [/frontend\/fonts/],
                    use: compact([
                        {
                            loader: 'file-loader',
                            options: {
                                name: '[path][name].[ext]',
                            },
                        },
                    ]),
                },
            ]
        },

        resolve: {
            modules: ['node_modules'],
            extensions: ['*', '.js', '.jsx', '.ts', '.tsx', '.scss', '.sass', '.png']
        },

    };
};

module.exports = config();
