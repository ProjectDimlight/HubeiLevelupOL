const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
    transpileDependencies: true,
    outputDir: path.resolve(__dirname, '../server/public'),
    devServer:{
        proxy:{
            '^/echo': {
                target: 'ws://127.0.0.1:5001',
                ws: true,
                changeOrigin: true
            }
        }
    }
})
