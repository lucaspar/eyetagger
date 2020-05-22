import Vue from 'vue'
import store from '@/store'
import Router from 'vue-router'
import Home from '@/components/Home'
import Rest from '@/components/Rest'
import Login from '@/components/Login'
import ThankYou from '@/components/ThankYou'
import Annotation from '@/components/Annotation'
import Visualization from '@/components/Visualization'

Vue.use(Router)

const router = new Router({
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
            path: '/login',
            name: 'login',
            component: Login,
        },
        {
            path: '/thankyou',
            name: 'thankyou',
            component: ThankYou,
            meta: {
                requiresAuth: true
            },
        },
        {
            path: '/annotation',
            name: 'annotation',
            component: Annotation,
            meta: {
                requiresAuth: true
            },
        },
        {
            path: '/visualization',
            name: 'visualization',
            component: Visualization,
            meta: {
                requiresAuth: true
            },
        },
    ]
})

// authentication guard
router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        // this route requires auth, check if logged in
        // if not, redirect to login page.
        if (!store.getters.isLoggedIn) {
            next({ name: 'login' })
        } else {
            next()
        }
    }
    else {
        next()
    }
})

export default router
