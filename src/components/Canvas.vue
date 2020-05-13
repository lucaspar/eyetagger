<template>
    <div class="cnv section columns is-multiline">
        <div class="right">
            <small>{{ iris_sample.id }}</small>
        </div>
        <div class="center column is-full">
            <h4 class="title is-4 has-text-centered">Iris {{ iris_sample.number }}</h4>
        </div>
        <div class="column is-full">
            <div class="columns is-centered">
                <div class="column is-2" id="control-panel">
                    <div class="columns is-multiline">
                        <div class="column is-6"><button class="button is-info" id="btn-previous">   <b-icon pack="fas" icon="chevron-left">     </b-icon> <span>Previous (Q)</span> </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-next">       <b-icon pack="fas" icon="chevron-right">    </b-icon> <span>Next (E)</span>     </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-undo">       <b-icon pack="fas" icon="undo">             </b-icon> <span>Undo (Z)</span>     </button>   </div>
                        <div class="column is-6"><button class="button is-info" id="btn-redo">       <b-icon pack="fas" icon="redo">             </b-icon> <span>Redo (X)</span>     </button>   </div>
                        <div class="column is-6 is-offset-3"><button class="button is-info" id="btn-brush">      <b-icon pack="fas" icon="brush">            </b-icon> <span>Brush</span>    </button>   </div>
                        <!-- <div class="column is-6"><button class="button is-info" id="btn-eraser">     <b-icon pack="fas" icon="eraser">           </b-icon> <span>Eraser</span>   </button>   </div> -->
                    </div>
                </div>
                <div class="column">
                    <canvas id="vis-canvas" ref="vis-canvas"/>
                </div>
                <div class="column">
                    <canvas id="main-canvas" ref="main-canvas"/>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
// import annotator from '@/services/annotator'
import iris_sample_path from '@/assets/iris-sample-single.png'
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
            iris_sample: {
                id: "checksum89abcdef",
                path: "location/in/server.png",
                number: 1,
            },
        }
    },
    mounted() {

        // get canvas
        const canvas = this.$refs['main-canvas']
        const main_canvas = new fabric.Canvas(canvas)
        const vis_canvas = new fabric.Canvas(this.$refs['vis-canvas'])
        this.context = canvas.getContext('2d')

        // set up iris image
        const img = new window.Image()
        this.image = img
        img.src = iris_sample_path
        img.onload = () => {

            // prepare visualization canvas
            vis_canvas.isDrawingMode = false
            vis_canvas.setBackgroundImage(iris_sample_path, vis_canvas.renderAll.bind(vis_canvas))
            vis_canvas.setDimensions({ width: img.naturalWidth, height: img.naturalHeight })
            // vis_canvas.renderAll();

            // prepare main canvas
            main_canvas.isDrawingMode = true
            main_canvas.setBackgroundImage(iris_sample_path, main_canvas.renderAll.bind(main_canvas))
            main_canvas.setDimensions({ width: img.naturalWidth, height: img.naturalHeight })
            main_canvas.renderAll();

            // set brush properties
            main_canvas.freeDrawingBrush.width = 20
            main_canvas.freeDrawingBrush.color = "#f005"

        }

        main_canvas.on('mouse:up', () => {

            // disolve existing group
            this.paths_group._restoreObjectsState()
            main_canvas.remove(this.paths_group)

            // select all objects for re-grouping
            const objs = main_canvas.getObjects().map( o => o.set('active', true) )
            this.paths_group = new fabric.Group(objs, {
                originX: 'center',
                originY: 'center',
            })
            const items = main_canvas.getObjects()
            console.log("Objects count:", items.length);

            // cloning an object
            // const new_item = fabric.util.object.clone(items[items.length-1])
            // new_item.set("top", new_item.top + 5)
            // new_item.set("left", new_item.left + 5)
            // new_item.set("fill", "#0f0");
            // main_canvas.add(new_item)

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
.right {
    text-align: right;
    position: absolute;
    margin: 1em;
    right: 0;
    top: 0;
}
button {
    width: 100%;
}
.cnv {
    padding-top: 0;
}
</style>
