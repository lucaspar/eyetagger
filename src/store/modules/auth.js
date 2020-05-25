import axios from 'axios'
import api from '@/services/api'

const state = {
    is_authenticated: false,
    auth_token: undefined,
}

const getters = {
    is_authenticated: state => {
        return state.is_authenticated
    },
    auth_token: state => {
        return state.auth_token
    },
}

const actions = {
    login({ commit }, payload) {
        console.log(" > Logging in...:", payload);
        return api.post(`auth/token/login/`, payload).then(      // trailing slash matters
            response => commit('login', response.data)
        )
    },
    logout({ commit }) {
        console.log(" > Logging out...:");
        return api.post(`auth/token/logout/`).then(     // trailing slash matters
            response => commit('logout', response.data)
        )
    },
}

const mutations = {
    login(state, response) {
        console.log(response)
        if (response.auth_token) {
            state.is_authenticated = true
            state.auth_token = response.auth_token
            axios.defaults.headers.common = { 'Authorization': `Token ${state.auth_token}` }
            console.log(" > Authenticated :: ", state.auth_token);
        }
    },
    logout(state) {
        state.is_authenticated = false
        state.auth_token = undefined
        axios.defaults.headers.common = { 'Authorization': "" }
        console.log(" > Logged out!");
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
