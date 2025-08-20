const path = require('path');
const fs = require('fs');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = (env, argv) => {
  const isProduction = argv.mode === 'production';
  
  return {
    entry: './src/index.tsx',
    output: {
      path: path.resolve(__dirname, 'dist'),
      filename: 'bundle.js',
      clean: true,
    },
    resolve: {
      extensions: ['.ts', '.tsx', '.js', '.jsx'],
      alias: {
        '@': path.resolve(__dirname, 'src'),
      },
    },
    module: {
      rules: [
        {
          test: /\.(ts|tsx)$/,
          use: 'ts-loader',
          exclude: /node_modules/,
        },
        {
          test: /\.css$/,
          use: ['style-loader', 'css-loader'],
        },
        {
          test: /\.(png|jpg|jpeg|gif|svg)$/,
          type: 'asset/resource',
        },
      ],
    },
    plugins: [
      new HtmlWebpackPlugin({
        template: './src/index.html',
        filename: 'index.html',
      }),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: 'manifest.xml',
            to: 'manifest.xml',
          },
          {
            from: 'assets',
            to: 'assets',
          },
          {
            from: 'src/commands/commands.html',
            to: 'commands.html',
          },
          {
            from: 'src/login-dialog.html',
            to: 'login-dialog.html',
          },
          {
            from: 'src/auth-callback.html',
            to: 'auth-callback.html',
          },
        ],
      }),
    ],
    devServer: {
      static: {
        directory: path.join(__dirname, 'dist'),
      },
      compress: true,
      port: 3000,
      hot: true,
      client: {
        overlay: {
          errors: false,
          warnings: false,
        },
      },
      server: {
        type: 'https',
        options: {
          key: fs.readFileSync('./ssl/key.pem'),
          cert: fs.readFileSync('./ssl/cert.pem'),
        },
      },
      headers: {
        'Access-Control-Allow-Origin': '*',
      },
    },
    devtool: isProduction ? 'source-map' : 'eval-source-map',
    optimization: {
      minimize: isProduction,
    },
  };
};
