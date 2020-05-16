import api from '@/services/api'

export default {

    fetchImages() {
        return api.get(`images/`).then(response => response.data)
    },

    postAnnotation(payload) {
        return api.post(`annotations/`, payload).then(response => response.data)
    },

}
