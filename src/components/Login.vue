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
                <button class="button is-info" @click="login">
                Login
                </button>
            </p>
            </div>

        </div>
    </div>
</template>

<script>
export default {
    name: 'Login',
    data() {
        return {
            'username': "",
            'password': "",
        }
    },
    methods: {
        login() {
            const payload = {
                username: this.username,
                password: this.password,
            }
            this.$store.dispatch('auth/login', payload)
        },
        // Log the user out
        logout() {
            this.$store.dispatch('auth/logout')
        }
    },
}
</script>

<style scoped>
img {
    width: 250px;
}
</style>
