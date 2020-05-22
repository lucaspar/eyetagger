<template>
    <div class="section" id="app">
        <b-navbar>
            <template slot="start">
                <h1 class="title is-2">Iris Annotation Tool</h1>
            </template>
            <template slot="end">
                <b-navbar-item><router-link :to="{ name: 'home' }">
                    Home
                </router-link></b-navbar-item>
                <b-navbar-item><router-link :to="{ name: 'annotation' }">
                    Annotation Demo
                </router-link></b-navbar-item>
                <b-navbar-item><router-link :to="{ name: 'visualization' }">
                    Visualization Demo
                </router-link></b-navbar-item>
                <b-navbar-item v-if="is_authenticated">
                    <router-link :to="{ name: 'login', params: { logout: true } }">Logout
                </router-link></b-navbar-item>
                <b-navbar-item v-else>
                    <router-link :to="{ name: 'login' }">Login
                </router-link></b-navbar-item>
            </template>
        </b-navbar>
        <router-view />
    </div>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'

export default {
    name: "App",
    computed: {
        ...mapState('auth', [
            'is_authenticated',
            'auth_token',
        ]),
    },
    created() {
        // get available images once app is created
        if (this.is_authenticated) {
            axios.defaults.headers.common = { 'Authorization': `Token ${this.auth_token}` }
            this.fetch_images()
        }
    },
    methods: {
        fetch_images() {
            if (this.is_authenticated) {
                this.$store.dispatch('images/getImages')
            }
            else {
                console.log("User not authenticated. Redirected to login.");
                this.$router.push({ name: 'login' })
            }
        }
    },
    watch: {
        is_authenticated: {
            handler: 'fetch_images',
        },
    }
    // computed: mapState({
    //     images: state => state.images.images
    // }),
    // methods: mapActions('messages', [
    //     'addMessage',
    //     'deleteMessage'
    // ]),
}
</script>

<style>
#app {
    font-family: "Avenir", Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    color: #2c3e50;
    margin-top: 60px;
    padding-top: 0;
}
</style>
