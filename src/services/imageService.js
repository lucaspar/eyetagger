import api from '@/services/api'

export default {

    fetchImages(sessionUUID) {
        return api.get(`images/`, {
            sessionUUID,
        }).then(response => response.data)
    },

    postAnnotation(sessionUUID, imgID) {
        return api.post(`images/${imgID}`, {
            sessionUUID,
        }).then(response => response.data)
    },

}
