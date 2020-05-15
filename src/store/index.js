import Vue from 'vue'
import Vuex from 'vuex'
import messages from './modules/messages'
import images from './modules/images'

Vue.use(Vuex)

export default new Vuex.Store({
    modules: {
        messages,
        images,
    }
})
