import Vue from 'vue'
import Buefy from 'buefy';
import App from '@/App.vue'
import 'buefy/dist/buefy.css';

import store from '@/store'
import router from '@/router'

// font awesome
import '../node_modules/@fortawesome/fontawesome-free/js/all.js'

Vue.config.productionTip = false
Vue.use(Buefy, { defaultIconPack: 'fas' });

const vue = new Vue({
    router,
    store,
    render: h => h(App)
})

vue.$mount('#app')
