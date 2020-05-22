import axios from 'axios'
import Cookies from 'js-cookie'

// axios.defaults.headers.common = { 'Authorization': `Bearer ${token}` }

export default axios.create({
    baseURL: '/api',
    timeout: 300,
    headers: {
        // 'Access-Control-Allow-Origin': '*',
        // 'Authorization': 'Token ' + this.store.getters['auth/is_authenticated'],
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken')
    }
})
