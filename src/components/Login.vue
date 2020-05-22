<template>
    <div class="columns is-centered">
        <div class="column is-narrow has-text-centered">
            <img class="" src='@/assets/logo-iris.png'>

            <div class="field">
            <p class="control has-icons-left has-icons-right">
                <input class="input" v-model="username" type="text" placeholder="Username">
                <span class="icon is-small is-left">
                <i class="fas fa-user"></i>
                </span>
            </p>
            </div>
            <div class="field">
            <p class="control has-icons-left">
                <input class="input" v-model="password" type="password" placeholder="Password">
                <span class="icon is-small is-left">
                <i class="fas fa-lock"></i>
                </span>
            </p>
            </div>
            <div class="field is-right">
            <p class="control is-pulled-right">
                <button class="button is-info" @click="run_login">
                Login
                </button>
            </p>
            </div>

        </div>
    </div>
</template>

<script>
// import { mapState } from 'vuex'

export default {
    name: 'Login',
    props: ['logout'],
    computed: {
        // ...mapState('auth', [
        //     'is_authenticated',
        //     'auth_token',
        // ]),
    },
    data() {
        return {
            'username': "",
            'password': "",
        }
    },
    created() {
        console.log("LOGOUT:", this.logout);

        if (this.logout) {
            this.run_logout()
        }
    },
    methods: {
        run_login() {
            const payload = {
                username: this.username,
                password: this.password,
            }
            this.$store.dispatch('auth/login', payload).then(() => {
                // if there is no error go to annotation view
                if (this.$store.getters.error == undefined) {
                    this.$router.push({ name: 'annotation' })
                }
            })
        },
        // Log the user out
        run_logout() {
            this.$store.dispatch('auth/logout').then(() => {
                // if there is no error go to home view
                if(!this.$store.getters.error){
                    this.$router.push({ name: 'home' })
                }
            })
        }
    },
}
</script>

<style scoped>
img {
    width: 250px;
}
</style>
