const state = {
    successes: [],
    errors: [],
}

const getters = {
    successes: state => state.successes,
    errors: state => state.errors,
}

const actions = {
    clearErrors({ commit }) {
        commit('clearErrors')
    },
    clearSuccesses({ commit }) {
        commit('clearSuccesses')
    },
    error({ commit }, message) {
        commit('pushError', message)
    },
    success({ commit }, message) {
        commit('pushSuccess', message)
    },
}

const mutations = {
    clearErrors(state) {
        state.errors = []
    },
    clearSuccesses(state) {
        state.successes = []
    },
    pushError(state, message) {
        state.errors.push(message)
    },
    pushSuccess(state, message) {
        state.successes.push(message)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
