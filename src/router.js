import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Rest from '@/components/Rest'
import Annotation from '@/components/Annotation'
import Visualization from '@/components/Visualization'

Vue.use(Router)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home,
        },
        {
            path: '/rest',
            name: 'rest',
            component: Rest,
        },
        {
            path: '/annotation',
            name: 'annotation',
            component: Annotation,
        },
        {
            path: '/visualization',
            name: 'visualization',
            component: Visualization,
        },
    ]
})
