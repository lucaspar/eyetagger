<template>
    <div class="columns is-centered">
        <div class="column is-narrow has-text-centered">
            <img class="" src='@/assets/logo-iris.png'>
            <p class="title is-3">Thank you for your help!</p>
            <p v-if="all_clean">Your work has been submitted</p>
            <p v-else>Submitting your work, please wait...</p>
        </div>
    </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
    name: 'Home',
    computed: {
        ...mapState('images', [
            'annotations',
        ]),
        all_clean: () => {
            return false
        },
    },
    props: {},
}
</script>

<style scoped>
img {
    width: 250px;
}
</style>
