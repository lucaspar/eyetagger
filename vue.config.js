// const IS_PRODUCTION = process.env.NODE_ENV === 'production'
// process.env.VUE_APP_DATASET_ROOT = "http://jarviscore.resnet.nd.edu:8000/static/data/images"
process.env.VUE_APP_DATASET_ROOT = "/static/data/images"

module.exports = {
    outputDir: 'dist',
    assetsDir: 'static',
    // baseUrl: IS_PRODUCTION
    // ? 'http://cdn123.com'
    // : '/',
    // For Production, replace set baseUrl to CDN
    // And set the CDN origin to `yourdomain.com/static`
    // Whitenoise will serve once to CDN which will then cache
    // and distribute
    devServer: {
        host: "127.0.0.1",
        proxy: {
            '/api*': {
                // Forward frontend dev server request for /api to django dev server
                target: 'http://localhost:8000/',
            },
            // '/static/*': {
            //     // Forward frontend dev server request for /api to django dev server
            //     target: 'http://localhost:8000/',
            // }
        },
        disableHostCheck: true,
    }
}
