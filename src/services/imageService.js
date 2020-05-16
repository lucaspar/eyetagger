import api from '@/services/api'

export default {

    fetchImages() {
        return api.get(`images/`).then(response => response.data)
    },

    postAnnotations(payload) {
        console.log("SENDING PAYLOAD:", payload);
        return api.post(`annotations/`, payload).then(response => response.data)
    },

}
