import Vue from 'vue'
import Buefy from 'buefy'
import App from '@/App.vue'
import 'buefy/dist/buefy.css'
import * as Sentry from '@sentry/browser'
import VueAWN from "vue-awesome-notifications"
import { Vue as VueIntegration } from '@sentry/integrations'
import '../node_modules/@fortawesome/fontawesome-free/js/all.js'
require("vue-awesome-notifications/dist/styles/style.css")

import store from '@/store'
import router from '@/router'

// if production mode, enable sentry
if (!process.env.VUE_APP_DEBUG) {
    const stry = {
        'key':      process.env.VUE_APP_SENTRY_KEY,
        'org':      process.env.VUE_APP_SENTRY_ORG,
        'project':  process.env.VUE_APP_SENTRY_PROJECT,
    }
    Sentry.init({
        dsn: 'https://' + stry.key + '@' + stry.org + '.ingest.sentry.io/' + stry.project,
        integrations: [new VueIntegration({ Vue, attachProps: true })],
    });
}

Vue.use(VueAWN, {})
Vue.config.productionTip = false
Vue.use(Buefy, { defaultIconPack: 'fas' });

const vue = new Vue({
    router,
    store,
    render: h => h(App)
})

vue.$mount('#app')
