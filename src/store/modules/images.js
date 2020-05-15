import imageService from '@/services/imageService'

const state = {
    images: [],
    annotations: {},
    sequential_counter: 0,
}

const getters = {
    images: state => {
        return state.images
    },
    annotation: (state, imgID) => {
        return state.annotations[imgID]
    },
    sequential_counter: state => {
        return state.sequential_counter
    }
}

const actions = {
    getImages({ commit }) {
        imageService.fetchImages()
            .then(images => {
                commit('setImages', images)
            })
    },
    postAnnotation({ commit }) {
        imageService.postAnnotation()
            .then((annotation, imgID) => {
                commit('setAnnotation', annotation, imgID)
            })
    },
    incSeqCounter({ commit }) {
        commit('incSeqCounter')
    },
    decSeqCounter({ commit }) {
        commit('decSeqCounter')
    },
    setSeqCounter({ commit }, new_val) {
        commit('setSeqCounter', new_val)
    }
}

const mutations = {
    setImages(state, images) {
        state.images = images
    },
    setAnnotation(state, annotation, imgID) {
        state.annotations[imgID] = annotation
    },
    incSeqCounter(state) {
        state.sequential_counter++
    },
    decSeqCounter(state) {
        state.sequential_counter--
    },
    setSeqCounter(state, new_val) {
        state.sequential_counter = new_val
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
