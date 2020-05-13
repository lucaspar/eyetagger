import api from '@/services/api'

export default {

    fetchMessages() {
        return api.get(`messages/`)
            .then(response => response.data)
    },
    postMessage(payload) {
        return api.post(`messages/`, payload)
            .then(response => response.data)
    },
    deleteMessage(msgId) {
        return api.delete(`messages/${msgId}`)
            .then(response => response.data)
    },

    // annotator methods:
    fetchImageList(sessionUUID) {
        return api.get(`images/list`, {
            sessionUUID,
        }).then(response => response.data)
    },
    fetchImage(sessionUUID, imgID) {
        return api.get(`images/${imgID}`, {
            sessionUUID,
        }).then(response => response.data)
    },
    postAnnotation(sessionUUID, imgID) {
        return api.post(`images/${imgID}`, {
            sessionUUID,
        }).then(response => response.data)
    },

}
