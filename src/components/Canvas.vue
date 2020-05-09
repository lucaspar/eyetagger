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
import { fabric } from 'fabric'

export default {
    name: 'Canvas',
    props: {},
    data() {
        return {
            // the CanvasRenderingContext to turn canvas into a reactive component:
            paths_group: new fabric.Group(),
            context: null,
            image: null,
        }
    },
    mounted() {

        // get canvas
        const canvas = this.$refs['main-canvas']
        const fab_canvas = new fabric.Canvas(canvas)
        this.context = canvas.getContext('2d')

        // set up iris image
        const img = new window.Image()
        this.image = img
        img.src = iris_image_path
        img.onload = () => {

            // prepare canvas
            fab_canvas.isDrawingMode = true
            fab_canvas.setBackgroundImage(iris_image_path, fab_canvas.renderAll.bind(fab_canvas))
            fab_canvas.setDimensions({ width: img.naturalWidth, height: img.naturalHeight })
            fab_canvas.renderAll();

            // set brush properties
            fab_canvas.freeDrawingBrush.width = 20
            fab_canvas.freeDrawingBrush.color = "#f005"

        }

        fab_canvas.on('mouse:up', options => {

            console.log("Mouse Up event");

            // disolve existing group
            this.paths_group._restoreObjectsState()
            fab_canvas.remove(this.paths_group)

            // select all objects for re-grouping
            const objs = fab_canvas.getObjects().map( o => o.set('active', true) )
            this.paths_group = new fabric.Group(objs, {
                originX: 'center',
                originY: 'center',
            })
            const items = fab_canvas.getObjects()
            console.log("Objects count:", items.length);

            // cloning an object
            const new_item = fabric.util.object.clone(items[items.length-1])
            new_item.set("top", new_item.top + 5)
            new_item.set("left", new_item.left + 5)
            new_item.set("fill", "#0f0");
            console.log(new_item)
            fab_canvas.add(new_item)

        })

    },
}
</script>

<style scoped>
#main-canvas {
    width: 100%;
    height: 100%;
    display: block;
    margin: auto;
    border: 1px solid #09f;
    border-radius: 0.5em;
}
.cnv {
    width: 100%;
    height: 60vh;
}
.cnv > * {
    display: inline-block;
    margin: auto;
    border: 4px solid red;
}
</style>
