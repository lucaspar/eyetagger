// is development mode?
process.env.VUE_APP_DEBUG           = true

process.env.VUE_APP_DATASET_ROOT    = "/static/data/images"
process.env.VUE_APP_SENTRY_KEY      = "944a3d1092cd419c9c50cd8c29f32489"
process.env.VUE_APP_SENTRY_ORG      = "o124424"
process.env.VUE_APP_SENTRY_PROJECT  = "1401289"

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
        host: "0.0.0.0",
        port: "9000",
        proxy: {
            '/api*': {
                // Forward frontend dev server request for /api to django dev server
                target: 'http://localhost:8000/',
            },
            '/static/*': {
                // Forward frontend dev server request for /api to django dev server
                target: 'http://localhost:8000/',
            }
        },
        disableHostCheck: true,
    }
}
