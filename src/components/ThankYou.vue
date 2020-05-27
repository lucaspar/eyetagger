<template>
    <div class="columns is-centered">
        <div class="column is-narrow has-text-centered">
            <img class="" src='@/assets/logo-iris.png'>
            <p class="title is-3">Thank you for your help!</p>
            <div :key="is_all_clean">
                <p v-if="is_all_clean">Your work has been submitted</p>
                <p v-else>Submitting your work, please wait...</p>
            </div>
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
        comp_annotations() {
            return this.annotations
        },
        is_all_clean() {
            const vals = Object.values(this.annotations)
            const sel = vals.filter(el => el.is_dirty).length

            return sel === 0
        },
    },
    methods: {
        post_annotations() {
            this.$store.dispatch('images/postAnnotations')
        },
    },
    created() {
        if (!this.is_all_clean) {
            this.post_annotations()
        }
    },
    watch: {
        // post annotations to server when they change
        comp_annotations: {
            handler: 'post_annotations',
            // immediate: true,
            deep: true,
        },
    },
}
</script>

<style scoped>
img {
    width: 250px;
}
</style>
