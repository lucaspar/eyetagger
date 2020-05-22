import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import images from './modules/images'
import messages from './modules/messages'
import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

export default new Vuex.Store({
    plugins: [createPersistedState({
        storage: window.sessionStorage,
    })],
    modules: {
        messages,
        images,
        auth,
    }
})
