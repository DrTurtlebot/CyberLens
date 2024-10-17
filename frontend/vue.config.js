const { defineConfig } = require('@vue/cli-service');
const path = require('path');


module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
  },
  resolve: {
    alias: {
      '@src': path.resolve(__dirname, 'src'),
      '@widgets': path.resolve(__dirname, 'src/components/widgets'),
      '@pages': path.resolve(__dirname, 'src/components/pages'),
      '@atoms': path.resolve(__dirname, 'src/components/atoms'),
      '@molecules': path.resolve(__dirname, 'src/components/molecules'),
      '@organisms': path.resolve(__dirname, 'src/components/organisms'),
      '@assets': path.resolve(__dirname, 'src/assets'),
      '@scripts': path.resolve(__dirname, 'src/scripts'),
    },
  }
});