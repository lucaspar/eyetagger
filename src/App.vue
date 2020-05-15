<template>
    <div class="section" id="app">
        <b-navbar>
            <template slot="start">
                <h1 class="title is-2">Iris Annotation Tool</h1>
            </template>
            <template slot="end">
                <b-navbar-item><router-link :to="{ name: 'home' }">Home</router-link></b-navbar-item>
                <b-navbar-item><router-link :to="{ name: 'annotation' }">Annotation Demo</router-link></b-navbar-item>
                <b-navbar-item><router-link :to="{ name: 'visualization' }">Visualization Demo</router-link></b-navbar-item>
            </template>
        </b-navbar>
        <router-view />
    </div>
</template>

<script>
// import { mapState } from 'vuex'

export default {
    name: "App",
    created() {
        // get available images once app is created
        this.$store.dispatch('images/getImages')
    },
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
