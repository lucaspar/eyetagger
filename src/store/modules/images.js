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
        try {
            return state.annotations[imgID].annotation
        }
        catch(_) {
            return undefined
        }
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
    postAnnotations({ commit, state }) {

        console.log('Posting annotation to server');
        const annotations = Object.values(state.annotations).filter(v => v.is_dirty)
        console.log(annotations.length, " dirty annotations")

        if (annotations.length > 0) {
            imageService.postAnnotations(annotations)
                .then(response => {
                    commit('postAnnotations', response)
                })
        }

    },
    setAnnotation({ commit }, payload) {
        console.log("Setting new annotation locally")
        commit('setAnnotation', payload)
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
    postAnnotations(_, response) {
        console.log(response)
    },
    setAnnotation(state, payload) {
        // console.log(payload.imgID, payload.annotation)
        const id = payload.imgID
        if (state.annotations[id] === undefined) {
            state.annotations[id] = {}
        }
        state.annotations[id].imgID = id        // makes things simpler later
        state.annotations[id].is_dirty = true   // marks to be posted
        state.annotations[id].annotation = payload.annotation
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
