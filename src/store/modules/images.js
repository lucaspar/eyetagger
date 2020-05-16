import imageService from '@/services/imageService'

const state = {
    images: [],
    annotations: {},
    sequential_counter: 0,
    canvas_image: undefined,
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
    },
    canvas_image: state => {
        return state.canvas_image
    },
}

const actions = {
    getImages({ commit }) {
        imageService.fetchImages()
            .then(images => {
                commit('setImages', images)
            })
    },
    postAnnotation({ commit }, payload) {
        console.log('Dispatched annotation payload');
        imageService.postAnnotation(payload)
            .then(response => {
                commit('postAnnotation', response)
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
    },
    setCanvasImage({ commit }, new_val) {
        commit('setCanvasImage', new_val)
    },
}

const mutations = {
    setImages(state, images) {
        state.images = images
    },
    postAnnotation(state, response) {
        console.log(response)
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
    setCanvasImage(state, new_val) {
        console.log("Updated canvas image:", new_val.imgStaticPath)
        state.canvas_image = new_val
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
