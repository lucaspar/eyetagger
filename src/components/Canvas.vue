<template>
    <div class="cnv">
        <canvas
            id="main-canvas"
            ref="main-canvas"
            :config="{
                image: image
            }"
        ></canvas>
    </div>
</template>

<script>
// import annotator from '@/services/annotator'
import iris_image_path from '@/assets/iris-sample.png'

export default {
    name: 'Canvas',
    props: {},
    data() {
        return {
            // the CanvasRenderingContext to turn canvas into a reactive component:
            context: null,
            image: null,
        }
    },
    mounted() {

        // get canvas
        const canvas = this.$refs['main-canvas']
        this.context = canvas.getContext('2d')

        // set canvas dimensions
        canvas.width    = canvas.parentElement.clientWidth
        canvas.height   = canvas.parentElement.clientHeight

        // load image
        const img = new window.Image()
        this.image = img
        img.src = iris_image_path
        img.onload = () => {

            // resize canvas to image
            canvas.width = img.naturalWidth
            canvas.height = img.naturalHeight

            // draw on canvas
            this.context.drawImage(img, 0, 0)

        }

    },
}
</script>

<style scoped>
#main-canvas {
    border: 1px solid #09f;
    border-radius: 0.5em;
}
</style>
