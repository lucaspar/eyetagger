import axios from 'axios'
import api from '@/services/api'
import * as Sentry from '@sentry/browser';

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
    login({ dispatch, commit }, payload) {
        return api.post(`auth/token/login/`, payload)
            .then(response => {
                console.log(response)
                if (response.data && response.data.auth_token) {
                    commit('login', response.data)
                    console.log(" > Authenticated :: ", state.auth_token);
                    dispatch('toasts/success', 'Hello!', { root: true })
                }
                else {
                    dispatch('toasts/error', 'Oops, couldn\'t authenticate. Try again.', { root: true })
                }
            }).catch(response => {
                Sentry.captureMessage("Failed login:", response)
                commit('toasts/error', 'Oops, try again', { root: true })
            })
    },
    logout({ dispatch, commit }) {
        return api.post(`auth/token/logout/`).then(     // trailing slash matters
            response => {
                commit('logout', response.data)
                dispatch('toasts/success', 'Bye!', { root: true })
            }
        )
    },
}

const mutations = {
    login(state, data) {
        state.is_authenticated = true
        state.auth_token = data.auth_token
        axios.defaults.headers.common = { 'Authorization': `Token ${state.auth_token}` }
    },
    logout(state) {
        state.is_authenticated = false
        state.auth_token = undefined
        axios.defaults.headers.common = { 'Authorization': "" }
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
