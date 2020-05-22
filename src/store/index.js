import Vue from 'vue'
import Vuex from 'vuex'
import auth from './modules/auth'
import images from './modules/images'
import messages from './modules/messages'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        messages,
        images,
        auth,
    }
})
