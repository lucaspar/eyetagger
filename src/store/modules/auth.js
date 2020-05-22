import api from '@/services/api'

const state = {
    is_authenticated: false,
    user: {
        username: "Anonymous",
        auth_type: undefined,
    },
}

const getters = {
    is_authenticated: state => {
        return state.is_authenticated
    },
    username: state => {
        return state.user.username
    },
    auth_type: state => {
        return state.user.auth_type
    },
}

const actions = {
    login({ commit }, payload) {
        console.log(" > Logging in...:", payload);
        api.post(`auth/login/`, payload).then(      // trailing slash matters
            response => commit('login', response.data)
        )
    },
    logout({ commit }, payload) {
        console.log(" > Logging out...:", payload);
        api.post(`auth/logout/`, payload).then(     // trailing slash matters
            response => commit('logout', response.data)
        )
    },
}

const mutations = {
    login(state, response) {
        console.log("RESPONSE:", response.data);
        // state.is_authenticated = true
    },
    logout(state, response) {
        console.log("RESPONSE:", response);
        state.is_authenticated = false
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
